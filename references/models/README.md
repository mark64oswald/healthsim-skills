# PopulationSim Models Reference

## Overview

This directory contains the canonical model definitions for PopulationSim. These models define the structure of inputs, outputs, and intermediate data used across all PopulationSim skills.

---

## Core Models

| Model | Description | Primary Use |
|-------|-------------|-------------|
| [PopulationProfile](population-profile.md) | Comprehensive population snapshot | Primary output of geographic analysis |
| [CohortSpecification](cohort-specification.md) | Cohort generation criteria | Input to cohort generation |
| [GeographicEntity](geographic-entity.md) | Geographic area identification | Location reference across all models |
| [SDOHProfile](sdoh-profile.md) | Social determinants composite | SDOH analysis and Z-code mapping |

---

## Model Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                     CohortSpecification                          │
│  (Input: defines what population to generate)                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GeographicEntity                             │
│  (Reference: identifies location at any level)                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌─────────────────────┐     ┌─────────────────────────────────────┐
│   PopulationProfile │     │           SDOHProfile               │
│  (Output: full      │◄────│  (Component: SDOH detail)           │
│   population data)  │     │                                     │
└─────────────────────┘     └─────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│              Downstream Products                                 │
│  PatientSim │ MemberSim │ RxMemberSim │ TrialSim                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Model Hierarchy

### Geographic Hierarchy

```
GeographicEntity
├── nation
├── region
├── division
├── state
├── county
├── msa (metropolitan statistical area)
├── tract
├── block_group
├── zcta
└── custom
```

### Profile Composition

```
PopulationProfile
├── geography: GeographicEntity
├── demographics
├── health_indicators
├── sdoh_profile: SDOHProfile
├── healthcare_access
├── utilization_patterns
└── metadata
```

### Cohort Definition

```
CohortSpecification
├── geography: GeographyConstraint
│   └── identifiers: GeographicEntity
├── demographics: DemographicConstraint
├── clinical_profile: ClinicalConstraint
├── sdoh_requirements: SDOHConstraint
├── size: SizeSpec
├── integration: IntegrationSpec
└── metadata
```

---

## Data Flow

### 1. Geographic Analysis Flow

```
User Request
    │
    ▼
GeographicEntity (identify location)
    │
    ▼
PopulationProfile (generate profile)
    │
    ├── Demographics from ACS
    ├── Health from CDC PLACES
    ├── SDOH from SVI/ADI
    └── Access from HPSA/provider data
```

### 2. Cohort Generation Flow

```
CohortSpecification (define criteria)
    │
    ▼
PopulationProfile (source data)
    │
    ▼
Cohort Generation (apply filters)
    │
    ├── Age/sex stratification
    ├── Clinical conditions
    ├── SDOH requirements
    └── Geographic constraints
    │
    ▼
Synthetic Population
    │
    ▼
Downstream Products
```

### 3. Cross-Product Integration Flow

```
PopulationProfile
    │
    ├──▶ PatientSim
    │    └── Patient demographics, conditions, Z-codes
    │
    ├──▶ MemberSim
    │    └── Member enrollment, plan selection
    │
    ├──▶ RxMemberSim
    │    └── Pharmacy patterns, adherence
    │
    └──▶ TrialSim
         └── Subject eligibility, diversity
```

---

## Common Patterns

### Identity Correlation

All models support identity correlation through the Person entity:

```json
{
  "identity": {
    "ssn": "123-45-6789",
    "person_id": "person-uuid-here"
  },
  "product_ids": {
    "patient_mrn": "MRN123456",
    "member_id": "MEM987654",
    "subject_id": "SUBJ-001"
  }
}
```

### Metadata Pattern

All models include consistent metadata:

```json
{
  "metadata": {
    "created_at": "2024-12-23T10:30:00Z",
    "version": "1.0",
    "data_sources": {},
    "generation_context": {}
  }
}
```

### Geographic Reference Pattern

All models reference geography consistently:

```json
{
  "geography": {
    "type": "county",
    "identifiers": {
      "fips": "48201",
      "name": "Harris County"
    }
  }
}
```

---

## Validation

### Required Fields

Each model specifies required vs optional fields. Required fields must be present for valid model instances.

### Value Constraints

- FIPS codes must be valid format and length
- Percentages must be 0.0-1.0
- Percentiles must be 1-100
- Rates must be non-negative
- Dates must be ISO 8601 format

### Referential Integrity

- Child geographies must be within parent
- Cohort geography must match profile geography
- Z-codes must be valid ICD-10-CM codes

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-23 | Initial model definitions |

---

## Related Documentation

- [Geography Codes](../geography-codes.md) - FIPS, CBSA codes
- [Census Variables](../census-variables.md) - ACS variable dictionary
- [CDC PLACES Indicators](../cdc-places-indicators.md) - Health measures
- [SVI Methodology](../svi-methodology.md) - Social Vulnerability Index
- [ADI Methodology](../adi-methodology.md) - Area Deprivation Index
- [Code Systems](../code-systems.md) - Medical coding standards
