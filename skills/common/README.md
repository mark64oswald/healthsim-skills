# Common Skills

Cross-product skills that apply to all HealthSim products. These skills handle infrastructure concerns like state management, database operations, and identity correlation.

## Quick Reference

| Skill | Use When | Key Features |
|-------|----------|--------------|
| [State Management](state-management.md) | Saving/loading cohorts | DuckDB persistence, cohort naming, tags |
| [DuckDB Skill](duckdb-skill.md) | Database queries and operations | SQL queries, schema management |
| [Identity Correlation](identity-correlation.md) | Linking entities across products | SSN correlation, Person↔Patient/Member/Subject |

## State Management

The state management skill handles cohort persistence across all HealthSim products:

```
Save this cohort as "diabetes-cohort-jan-2025"
Load cohort "test-population"
List all cohorts
Get summary for the current cohort
```

Key concepts:
- **Cohorts** are named snapshots of generated data
- **Auto-persist** automatically saves entities as they're generated
- **Tags** enable organization and filtering

See [state-management.md](state-management.md) for full details.

## DuckDB Operations

The DuckDB skill provides direct database access:

```
Query the patients table for diabetics
Show me the schema for the encounters table
Count members by plan type
```

Key concepts:
- **main schema** - Generated entities (patients, members, claims, etc.)
- **network schema** - Real NPPES provider data (8.9M+ providers)
- **population schema** - Real CDC/Census data (416K+ rows)

See [duckdb-skill.md](duckdb-skill.md) for full details.

## Identity Correlation

The identity correlation skill links entities across products:

```
Link this patient to their member record
Find all claims for patient MRN00012345
Show trial subjects with their EMR records
```

Key concepts:
- **SSN** is the universal correlator across Person entities
- **Person** is the root entity (PatientSim)
- **Patient/Member/RxMember/Subject** are domain-specific views

See [identity-correlation.md](identity-correlation.md) for full details.

## Cross-Product Identity Model

```
                    ┌─────────────┐
                    │   Person    │
                    │   (SSN)     │
                    └──────┬──────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐    ┌───────▼──────┐    ┌──────▼──────┐
│   Patient   │    │    Member    │    │   Subject   │
│ (PatientSim)│    │ (MemberSim)  │    │ (TrialSim)  │
│    MRN      │    │  Member ID   │    │   USUBJID   │
└─────────────┘    └──────────────┘    └─────────────┘
       │                   │
       │           ┌───────▼──────┐
       │           │  RxMember    │
       │           │(RxMemberSim) │
       │           │  Cardholder  │
       │           └──────────────┘
       │
┌──────▼──────┐
│  Provider   │
│ (NetworkSim)│
│    NPI      │
└─────────────┘
```

## Usage Examples

### Saving Generated Data

```
Generate 50 diabetic patients with claims
Save as cohort "diabetes-claims-demo" with tags "demo", "diabetes"
```

### Cross-Product Queries

```sql
-- Find all encounters and claims for a patient
SELECT p.mrn, e.encounter_date, c.claim_id
FROM patients p
JOIN encounters e ON p.id = e.patient_id
JOIN claims c ON e.encounter_id = c.encounter_id
WHERE p.mrn = 'MRN00012345';
```

### Loading Reference Data

```
Look up cardiologists in San Diego County
Find facilities with oncology services
Get SVI data for ZIP 92101
```

## Related Documentation

- [Data Architecture Guide](../../docs/data-architecture.md)
- [HealthSim Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md)
- [MCP Server Configuration](../../packages/mcp-server/README.md)

---

*Common skills are foundational infrastructure used by all HealthSim products.*
