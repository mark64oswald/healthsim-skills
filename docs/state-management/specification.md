# State Management Technical Specification

This document defines the API interfaces and data formats for the State Management capability.

## Overview

State Management enables users to save and load workspace scenarios - complete snapshots of all generated entities (patients, encounters, claims, etc.) with full provenance tracking.

**Storage Backend**: DuckDB embedded database  
**Storage Location**: `~/.healthsim/healthsim.duckdb`  
**Export Format**: JSON (for sharing)

---

## API Reference

### save_scenario

Saves entities as a named scenario.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Unique scenario name (kebab-case recommended) |
| entities | object | Yes | Dict of entity_type → entity list |
| description | string | No | Scenario description |
| tags | array[string] | No | Tags for organization |
| overwrite | boolean | No | Replace existing (default: false) |

#### Returns

```json
{
  "scenario_id": "uuid-string",
  "name": "scenario-name",
  "entity_count": 42,
  "entities_by_type": {
    "patient": 5,
    "encounter": 15,
    "diagnosis": 22
  }
}
```

#### Python Usage

```python
from healthsim.state import save_scenario

scenario_id = save_scenario(
    name='diabetes-cohort',
    entities={
        'patients': [patient1, patient2],
        'encounters': [enc1, enc2, enc3]
    },
    description='Type 2 Diabetes test cohort',
    tags=['diabetes', 'testing']
)
```

---

### load_scenario

Loads a scenario from the database.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Scenario name or UUID |

#### Returns

```json
{
  "scenario_id": "uuid-string",
  "name": "scenario-name",
  "description": "...",
  "entities": {
    "patients": [...],
    "encounters": [...]
  },
  "tags": ["tag1", "tag2"],
  "created_at": "2024-12-26T10:30:00Z"
}
```

#### Python Usage

```python
from healthsim.state import load_scenario

scenario = load_scenario('diabetes-cohort')
patients = scenario['entities']['patients']
```

---

### list_scenarios

Lists available scenarios with optional filtering.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tag | string | No | Filter by tag |
| search | string | No | Search in name/description |
| limit | integer | No | Max results (default: 100) |

#### Returns

```json
{
  "scenarios": [
    {
      "scenario_id": "uuid-string",
      "name": "scenario-name",
      "description": "...",
      "entity_count": 42,
      "tags": ["tag1"],
      "created_at": "2024-12-26T10:30:00Z"
    }
  ],
  "total_count": 5
}
```

#### Python Usage

```python
from healthsim.state import list_scenarios

# List all
scenarios = list_scenarios()

# Filter by tag
diabetes_scenarios = list_scenarios(tag='diabetes')

# Search
matches = list_scenarios(search='cohort')
```

---

### delete_scenario

Deletes a scenario (metadata and links, not underlying entity data).

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Scenario name or UUID |

#### Python Usage

```python
from healthsim.state import delete_scenario

delete_scenario('old-scenario')
```

---

### export_scenario_to_json

Exports a scenario to JSON file for sharing.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Scenario name or UUID |
| output_path | string/Path | No | Where to save (default: ~/Downloads/{name}.json) |

#### Returns

Path to the exported file.

#### Python Usage

```python
from healthsim.state import export_scenario_to_json

path = export_scenario_to_json('diabetes-cohort')
# Returns: ~/Downloads/diabetes-cohort.json

# Custom location
path = export_scenario_to_json('diabetes-cohort', output_path='/tmp/export.json')
```

---

### import_scenario_from_json

Imports a JSON scenario file.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| file_path | string/Path | Yes | Path to JSON file |
| name | string | No | Override scenario name |
| overwrite | boolean | No | Replace existing (default: false) |

#### Python Usage

```python
from healthsim.state import import_scenario_from_json
from pathlib import Path

scenario_id = import_scenario_from_json(Path('shared-scenario.json'))

# With name override
scenario_id = import_scenario_from_json(
    Path('data.json'),
    name='imported-cohort',
    overwrite=True
)
```

---

## Database Schema

### scenarios

Stores scenario metadata.

```sql
CREATE TABLE scenarios (
    scenario_id   UUID PRIMARY KEY,
    name          VARCHAR UNIQUE NOT NULL,
    description   VARCHAR,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata      JSON
);
```

### scenario_entities

Links entities to scenarios with full entity data.

```sql
CREATE TABLE scenario_entities (
    id            INTEGER PRIMARY KEY,
    scenario_id   UUID NOT NULL REFERENCES scenarios(scenario_id),
    entity_type   VARCHAR NOT NULL,
    entity_id     UUID NOT NULL,
    entity_data   JSON NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### scenario_tags

Tag-based organization.

```sql
CREATE TABLE scenario_tags (
    id            INTEGER PRIMARY KEY,
    scenario_id   UUID NOT NULL REFERENCES scenarios(scenario_id),
    tag           VARCHAR NOT NULL,
    UNIQUE(scenario_id, tag)
);
```

---

## JSON Export Format

Exported JSON files follow this structure for interoperability:

```json
{
  "schema_version": "1.0",
  "scenario_id": "uuid-string",
  "name": "scenario-name",
  "description": "Optional description",
  "created_at": "2024-12-26T10:30:00Z",
  "tags": ["tag1", "tag2"],
  "entities": {
    "patients": [
      {
        "patient_id": "uuid",
        "mrn": "MRN001",
        "given_name": "John",
        "family_name": "Doe",
        "birth_date": "1980-01-15",
        "...": "..."
      }
    ],
    "encounters": [...],
    "diagnoses": [...],
    "medications": [...],
    "lab_results": [...],
    "vital_signs": [...],
    "procedures": [...],
    "clinical_notes": [...]
  }
}
```

### Supported Entity Types

| Type | Description |
|------|-------------|
| patients | Patient demographics |
| encounters | Visits, admissions |
| diagnoses | ICD-10 diagnoses |
| procedures | CPT/ICD-PCS procedures |
| medications | Medication records |
| lab_results | Lab values |
| vital_signs | Vitals |
| clinical_notes | Notes/documents |
| members | Health plan members |
| claims | Claim headers |
| claim_lines | Claim line items |
| prescriptions | Rx fills |
| subjects | Trial subjects |
| trial_visits | Trial visit data |

---

## Migration from Legacy JSON

If you have existing scenarios in `~/.healthsim/scenarios/`:

```bash
# Check status
python scripts/migrate_json_to_duckdb.py --status

# Preview migration
python scripts/migrate_json_to_duckdb.py --dry-run

# Execute migration
python scripts/migrate_json_to_duckdb.py
```

The migration tool automatically:
1. Discovers JSON files in `~/.healthsim/scenarios/`
2. Creates backup at `~/.healthsim/scenarios_backup/`
3. Imports each scenario to DuckDB
4. Verifies migration success

---

## See Also

- [State Management User Guide](user-guide.md)
- [Data Architecture](../data-architecture.md)
- [State Management Skill](../../skills/common/state-management.md)
