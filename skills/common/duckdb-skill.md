---
name: healthsim-duckdb
description: |
  DuckDB-based unified data architecture for HealthSim. Provides persistent storage 
  for canonical entities across all products, enabling cross-product queries and 
  scenario management. Use for loading scenarios, saving scenarios, querying 
  the canonical data model, and token-efficient scenario operations.
status: Active
version: "1.2"
---

# HealthSim DuckDB Skill

## Overview

The HealthSim DuckDB skill provides persistent storage and query capabilities for all canonical entities generated across the HealthSim product suite. It serves as the operational data store for scenarios and enables cross-product analytics.

**Status**: Active  
**Schema Version**: 1.2  
**Database**: `healthsim.duckdb` (in workspace root)

## Trigger Phrases

### Scenario Management
- "Load scenario into DuckDB"
- "Save scenario to database"
- "Persist these entities"
- "Get summary of scenario"
- "List my scenarios"

### Querying
- "Query the canonical model"
- "Show patients with claims"
- "Cross-product query for..."
- "Query scenario for..."
- "Show me [entities] where..."

### Export/Import
- "Export scenario to JSON"
- "Import scenario from JSON"

## Database Schema

### Schema Version 1.2 Updates

As of version 1.2, all canonical tables include a `scenario_id` column that links entities directly to their source scenario. This enables efficient scenario-scoped queries without joining through `scenario_entities`.

### Provenance Columns (All Canonical Tables)

Every canonical table includes these columns for provenance tracking:

```sql
scenario_id VARCHAR,        -- Links to scenarios.scenario_id (v1.2+)
source_type VARCHAR,        -- 'loaded', 'generated', 'derived'
source_system VARCHAR,      -- 'patientsim', 'membersim', etc.
skill_used VARCHAR,         -- Skill that guided generation
created_at TIMESTAMP,       -- When entity was created
```

### Table Summary (41 Tables)

| Layer | Tables | Description |
|-------|--------|-------------|
| **Core** | persons, providers, facilities | Shared entities |
| **PatientSim** | patients, encounters, diagnoses, procedures, lab_results, medications, allergies, vitals | Clinical/EMR |
| **MemberSim** | members, accumulators, claims, claim_lines, authorizations | Payer/Claims |
| **RxMemberSim** | rx_members, prescriptions, pharmacy_claims, dur_alerts, pharmacies | Pharmacy/PBM |
| **TrialSim** | studies, sites, treatment_arms, subjects, adverse_events, visit_schedule, actual_visits, disposition_events | Clinical Trials |
| **PopulationSim** | geographic_entities, population_profiles, health_indicators, sdoh_indices, cohort_specifications | Demographics/SDOH |
| **NetworkSim** | networks, network_providers, network_facilities, provider_specialties | Provider Networks |
| **State Mgmt** | scenarios, scenario_entities, scenario_tags | Scenario Tracking |

### Cross-Product Relationships

```
Person (Core) ─────────────────────────────────────────────────
    │
    ├── Patient (PatientSim) via person_id
    │       └── Encounter → Diagnosis, Procedure, Lab, Medication
    │
    ├── Member (MemberSim) via person_id
    │       └── Claim → ClaimLine
    │
    ├── RxMember (RxMemberSim) via person_id
    │       └── Prescription → PharmacyClaim
    │
    └── Subject (TrialSim) via person_id
            └── AdverseEvent, ActualVisit
```

## Auto-Persist API

The auto-persist pattern provides token-efficient scenario management. Instead of returning all data after persist operations, it returns a compact summary (~500 tokens).

### persist()

Persist entities to canonical tables with automatic naming.

```python
from healthsim.state import persist

result = persist(
    entities={'patients': [...], 'encounters': [...]},
    context='diabetes cohort San Diego',  # Used for auto-naming
    tags=['diabetes', 'training']
)

# Returns PersistResult:
# - scenario_id: UUID
# - scenario_name: 'diabetes-cohort-20241227'
# - summary: ScenarioSummary (~500 tokens)
# - entity_ids: {'patients': [...], 'encounters': [...]}
```

### get_summary()

Load scenario summary without full data (~500 tokens vs potentially 50K+).

```python
from healthsim.state import get_summary

summary = get_summary('diabetes-cohort-20241227')

# Returns ScenarioSummary:
# - scenario_id, scenario_name
# - entity_counts: {'patients': 100, 'encounters': 250}
# - statistics: {'age_range': [35, 78], 'gender_distribution': {...}}
# - samples: {'patients': [3 sample patients], ...}
```

### query_scenario()

Run SQL queries against scenario data with pagination.

```python
from healthsim.state import query_scenario

results = query_scenario(
    'diabetes-cohort-20241227',
    "SELECT given_name, family_name, birth_date FROM patients WHERE gender = 'F'",
    limit=20,
    offset=0
)

# Returns QueryResult:
# - rows: List of result rows
# - columns: Column names
# - total_count: Total matching rows
# - page_size: Current page size
# - has_more: Whether more pages exist
```

**Security**: Only SELECT queries are allowed. Any attempt to use INSERT, UPDATE, DELETE, DROP, etc. will raise a ValueError.

## Example Queries

### 1. Scenario-Scoped Query (v1.2+)

Query data from a specific scenario:

```sql
-- Find all female patients in a specific scenario
SELECT given_name, family_name, birth_date, gender
FROM patients
WHERE scenario_id = 'abc123-...'
  AND gender = 'female'
ORDER BY family_name;
```

### 2. Cross-Product Patient Journey

```sql
SELECT 
    per.given_name || ' ' || per.family_name as patient_name,
    m.plan_name,
    e.encounter_type,
    e.start_datetime,
    c.total_billed,
    c.total_patient_resp
FROM persons per
JOIN members m ON per.person_id = m.person_id
JOIN patients p ON per.person_id = p.person_id
JOIN encounters e ON p.patient_id = e.patient_id
JOIN claims c ON e.encounter_id = c.encounter_id
WHERE per.family_name = 'Thompson'
  AND per.scenario_id = 'abc123-...';
```

### 3. Trial Subject with Clinical History

```sql
SELECT 
    sub.usubjid,
    sub.arm_code,
    st.protocol_number,
    p.mrn,
    COUNT(DISTINCT e.encounter_id) as prior_encounters
FROM subjects sub
JOIN studies st ON sub.study_id = st.study_id
JOIN patients p ON sub.patient_id = p.patient_id
LEFT JOIN encounters e ON p.patient_id = e.patient_id
WHERE sub.scenario_id = 'abc123-...'
GROUP BY sub.usubjid, sub.arm_code, st.protocol_number, p.mrn;
```

### 4. Population Health by Geography

```sql
SELECT 
    g.county_name,
    g.state_name,
    h.pct_diabetes,
    h.pct_obesity,
    s.svi_overall
FROM geographic_entities g
JOIN health_indicators h ON g.geo_id = h.geo_id
JOIN sdoh_indices s ON g.geo_id = s.geo_id
WHERE h.pct_diabetes > 12
ORDER BY s.svi_overall DESC
LIMIT 10;
```

### 5. Pharmacy Claims with DUR Alerts

```sql
SELECT 
    rm.cardholder_id,
    pc.drug_name,
    pc.service_date,
    pc.patient_pay,
    da.dur_type,
    da.message
FROM rx_members rm
JOIN pharmacy_claims pc ON rm.rx_member_id = pc.rx_member_id
LEFT JOIN dur_alerts da ON pc.pharmacy_claim_id = da.pharmacy_claim_id
WHERE da.severity = '1'  -- Severe alerts
  AND rm.scenario_id = 'abc123-...';
```

### 6. Entity Statistics for Summary

```sql
-- Get entity counts for a scenario
SELECT 
    'patients' as entity_type,
    COUNT(*) as count
FROM patients
WHERE scenario_id = 'abc123-...'
UNION ALL
SELECT 'encounters', COUNT(*) FROM encounters WHERE scenario_id = 'abc123-...'
UNION ALL
SELECT 'claims', COUNT(*) FROM claims WHERE scenario_id = 'abc123-...';
```

## Tools

### Scenario Loader (`tools/scenario_loader.py`)

Load JSON scenario files into DuckDB.

```bash
python tools/scenario_loader.py <scenario_path> [--db healthsim.duckdb]
```

### Scenario Saver (`tools/scenario_saver.py`)

Export scenarios from DuckDB to JSON files.

```bash
python tools/scenario_saver.py <scenario_name> [--output ./exports]
```

## MCP Integration

Access via the `healthsim-duckdb` MCP server:

```python
# Query the database
result = await mcp.query("SELECT * FROM persons LIMIT 10")
```

## Entity Types (38 Total)

| Product | Entity Types |
|---------|--------------|
| Core | person, provider, facility |
| PatientSim | patient, encounter, diagnosis, procedure, lab_result, medication, allergy, vital |
| MemberSim | member, accumulator, claim, claim_line, authorization |
| RxMemberSim | rx_member, prescription, pharmacy_claim, dur_alert, pharmacy |
| TrialSim | study, site, treatment_arm, subject, adverse_event, visit_schedule, actual_visit, disposition_event |
| PopulationSim | geographic_entity, population_profile, health_indicator, sdoh_index, cohort_specification |
| NetworkSim | network, network_provider, network_facility, provider_specialty |

## Related Documentation

- [DuckDB Schema Reference](docs/healthsim-duckdb-schema.md)
- [Auto-Persist Architecture](docs/healthsim-auto-persist-architecture.html)
- [State Management Skill](skills/common/state-management.md)
- [Tools README](tools/README.md)
- [Data Models Reference](references/data-models.md)

## Validation Rules

| Rule | Description |
|------|-------------|
| person_id required | All product entities must link to a person |
| scenario_id required | All canonical entities must have scenario_id (v1.2+) |
| SSN format | XXX-XX-XXXX for universal correlation |
| NPI format | 10-digit with Luhn check digit |
| FIPS codes | 2-digit state, 5-digit county, 11-digit tract |
| Date formats | ISO 8601 (YYYY-MM-DD) |
| SELECT only | Query API only allows SELECT statements |
