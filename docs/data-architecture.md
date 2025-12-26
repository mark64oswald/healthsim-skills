# HealthSim Data Architecture

## Overview

HealthSim uses DuckDB as its unified data store for:
- **State Management**: Scenario persistence and retrieval
- **Reference Data**: PopulationSim demographic datasets
- **Analytics** (Phase 2): Star schema for OHDSI-style analysis

## Database Location

```
~/.healthsim/healthsim.duckdb
```

The database is created automatically on first use. A separate test database is used during testing to isolate test data from production scenarios.

---

## Schema Layers

### Layer 1: Canonical Data Model

Source of truth for all generated entities. Tables mirror the JSON canonical model.

| Table | Description | Source Product |
|-------|-------------|----------------|
| patients | Patient demographics | PatientSim |
| encounters | Visits, admissions | PatientSim |
| diagnoses | ICD-10 codes | PatientSim |
| procedures | CPT/ICD-PCS codes | PatientSim |
| medications | Active/historical meds | PatientSim |
| lab_results | Lab values | PatientSim |
| vital_signs | Vitals | PatientSim |
| clinical_notes | Notes/documents | PatientSim |
| members | Health plan members | MemberSim |
| claims | Claim headers | MemberSim |
| claim_lines | Claim line items | MemberSim |
| prescriptions | Rx fills | RxMemberSim |
| subjects | Trial subjects | TrialSim |
| trial_visits | Trial visit data | TrialSim |

### Layer 2: State Management

Organizes entities into named scenarios for save/load/share operations.

| Table | Description |
|-------|-------------|
| scenarios | Scenario metadata (name, description, timestamps) |
| scenario_entities | Links entities to scenarios (stores full entity JSON) |
| scenario_tags | Tag-based organization |

### Layer 3: Reference Data

Read-only datasets loaded from PopulationSim for generation support.

| Table | Source | Records | Coverage |
|-------|--------|---------|----------|
| ref_cdc_places_tract | CDC PLACES 2024 | ~85,000 | All US census tracts |
| ref_cdc_places_county | CDC PLACES 2024 | ~3,200 | All US counties |
| ref_svi_tract | SVI 2022 | ~85,000 | All US census tracts |
| ref_svi_county | SVI 2022 | ~3,200 | All US counties |
| ref_adi_blockgroup | ADI 2021 | ~242,000 | All US block groups |

---

## Provenance Tracking

All canonical tables include provenance columns for traceability:

```sql
created_at          TIMESTAMP   -- When the entity was created
source_type         VARCHAR     -- 'generated', 'loaded', 'derived'
source_system       VARCHAR     -- 'patientsim', 'membersim', etc.
skill_used          VARCHAR     -- Skill that generated the entity
generation_seed     INTEGER     -- For reproducibility
```

---

## Querying

Direct SQL queries are supported via the DuckDB MCP server or Python:

```sql
-- Find all diabetic patients in a scenario
SELECT p.* 
FROM patients p
JOIN scenario_entities se ON p.patient_id = se.entity_id
JOIN scenarios s ON se.scenario_id = s.scenario_id
WHERE s.name = 'diabetes-cohort'
  AND se.entity_type = 'patient';

-- Query reference data for population health indicators
SELECT 
    county_name,
    AVG(diabetes_crude_prev) as avg_diabetes_rate,
    AVG(obesity_crude_prev) as avg_obesity_rate
FROM ref_cdc_places_county 
WHERE state_abbr = 'CA'
GROUP BY county_name
ORDER BY avg_diabetes_rate DESC;

-- Cross-reference patient location with SDOH data
SELECT 
    p.patient_id,
    p.given_name,
    svi.rpl_themes as vulnerability_score
FROM patients p
JOIN ref_svi_tract svi ON p.census_tract = svi.fips
WHERE svi.rpl_themes > 0.75;
```

---

## Python API

### State Management

```python
from healthsim.state import save_scenario, load_scenario, list_scenarios

# Save a scenario
scenario_id = save_scenario(
    name='diabetes-cohort',
    entities={
        'patients': [patient1, patient2, ...],
        'encounters': [enc1, enc2, ...]
    },
    description='Type 2 Diabetes test cohort',
    tags=['diabetes', 'chronic', 'testing']
)

# Load a scenario
scenario = load_scenario('diabetes-cohort')
patients = scenario['entities']['patients']

# List scenarios by tag
scenarios = list_scenarios(tag='diabetes')
```

### JSON Export/Import

```python
from healthsim.state import export_scenario_to_json, import_scenario_from_json

# Export for sharing
path = export_scenario_to_json('diabetes-cohort')
# Creates ~/Downloads/diabetes-cohort.json

# Import from file
import_scenario_from_json(Path('shared-scenario.json'))
```

### Database Access

```python
from healthsim.db import get_connection

with get_connection() as conn:
    result = conn.execute("""
        SELECT COUNT(*) FROM ref_cdc_places_tract
        WHERE diabetes_crude_prev > 15
    """).fetchone()
    print(f"High diabetes prevalence tracts: {result[0]}")
```

---

## Migration from JSON

If you have existing JSON scenarios from before the DuckDB migration:

```bash
# Check migration status
python scripts/migrate_json_to_duckdb.py --status

# Dry run (preview only)
python scripts/migrate_json_to_duckdb.py --dry-run

# Execute migration (creates backup automatically)
python scripts/migrate_json_to_duckdb.py
```

The migration tool:
- Discovers scenarios in `~/.healthsim/scenarios/`
- Creates a backup at `~/.healthsim/scenarios_backup/`
- Imports each scenario to DuckDB
- Verifies migration success

See [Migration Guide](./state-management/migration.md) for details.

---

## Schema Versioning

Schema versions are tracked in a `schema_version` table:

```sql
SELECT * FROM schema_version;
-- version | applied_at
-- 1       | 2024-12-26 10:30:00
```

Migrations are applied automatically when the database is opened if the schema is outdated.

---

## Performance Characteristics

| Operation | Typical Performance |
|-----------|---------------------|
| Save scenario (100 entities) | < 100ms |
| Load scenario (100 entities) | < 50ms |
| List scenarios | < 10ms |
| Reference data query (indexed) | < 50ms |
| Full table scan (250K rows) | < 500ms |

DuckDB's columnar storage provides excellent compression:
- Reference data: 5-7x compression vs CSV
- Scenario data: 3-5x compression vs JSON

---

## Related Documentation

- [State Management Skill](../skills/common/state-management.md) - Conversational interface
- [State Management Specification](./state-management/specification.md) - MCP tool details
- [PopulationSim Skill](../skills/populationsim/SKILL.md) - Reference data usage
- [HEALTHSIM-ARCHITECTURE-GUIDE.md](./HEALTHSIM-ARCHITECTURE-GUIDE.md) - Overall architecture
