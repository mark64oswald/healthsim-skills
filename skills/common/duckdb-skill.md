---
name: healthsim-duckdb
description: |
  DuckDB-based unified data architecture for HealthSim. Provides persistent storage 
  for canonical entities across all products, enabling cross-product queries and 
  scenario management. Use for loading scenarios, saving scenarios, and querying 
  the canonical data model.
status: Active
version: "1.0"
---

# HealthSim DuckDB Skill

## Overview

The HealthSim DuckDB skill provides persistent storage and query capabilities for all canonical entities generated across the HealthSim product suite. It serves as the operational data store for scenarios and enables cross-product analytics.

**Status**: Active  
**Database**: `healthsim.duckdb` (in workspace root)

## Trigger Phrases

- "Load scenario into DuckDB"
- "Save scenario to database"
- "Query the canonical model"
- "Show patients with claims"
- "Cross-product query for..."
- "Export scenario to JSON"
- "Import scenario from JSON"

## Database Schema

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

## Tools

### Scenario Loader (`tools/scenario_loader.py`)

Load JSON scenario files into DuckDB.

```bash
python tools/scenario_loader.py <scenario_path> [--db healthsim.duckdb]
```

**Example**:
```bash
python tools/scenario_loader.py scenarios/saved/bob-thompson-er-visit
```

### Scenario Saver (`tools/scenario_saver.py`)

Export scenarios from DuckDB to JSON files.

```bash
python tools/scenario_saver.py <scenario_name> [--output ./exports]
```

**Example**:
```bash
python tools/scenario_saver.py "bob-thompson-er-visit" -o ./exports
```

## Example Queries

### 1. Cross-Product Patient Journey

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
WHERE per.family_name = 'Thompson';
```

### 2. Trial Subject with Clinical History

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
GROUP BY sub.usubjid, sub.arm_code, st.protocol_number, p.mrn;
```

### 3. Population Health by Geography

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

### 4. Pharmacy Claims with DUR Alerts

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
WHERE da.severity = '1';  -- Severe alerts
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
- [Tools README](tools/README.md)
- [Data Models Reference](references/data-models.md)

## Validation Rules

| Rule | Description |
|------|-------------|
| person_id required | All product entities must link to a person |
| SSN format | XXX-XX-XXXX for universal correlation |
| NPI format | 10-digit with Luhn check digit |
| FIPS codes | 2-digit state, 5-digit county, 11-digit tract |
| Date formats | ISO 8601 (YYYY-MM-DD) |
