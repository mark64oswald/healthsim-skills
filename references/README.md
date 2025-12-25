# Reference Data

Domain knowledge and reference data for HealthSim data generation.

## Overview

Reference data provides the foundation for realistic healthcare data generation. These files define code systems, clinical rules, domain-specific terminology, and validation constraints.

## Reference Categories

### Code Systems & Terminology

| File | Description |
|------|-------------|
| [code-systems.md](code-systems.md) | ICD-10, CPT, LOINC, NDC, SNOMED mappings |
| [terminology.md](terminology.md) | Healthcare terminology definitions |
| [hl7v2-segments.md](hl7v2-segments.md) | HL7v2 segment definitions |
| [geography-codes.md](geography-codes.md) | State, county, FIPS codes |

### Clinical Domain Knowledge

| File | Description |
|------|-------------|
| [clinical-domain.md](clinical-domain.md) | Clinical workflow patterns |
| [clinical-rules.md](clinical-rules.md) | Clinical decision support rules |
| [pediatric-dosing.md](pediatric-dosing.md) | Weight-based medication dosing |
| [mental-health-reference.md](mental-health-reference.md) | Behavioral health domain |

### Data Models

| File | Description |
|------|-------------|
| [data-models.md](data-models.md) | Core entity schemas |
| [generation-patterns.md](generation-patterns.md) | Data generation strategies |
| [validation-rules.md](validation-rules.md) | Cross-field validation |

### Population & SDOH

| File | Description |
|------|-------------|
| [census-variables.md](census-variables.md) | Census/ACS variable mappings |
| [cdc-places-indicators.md](cdc-places-indicators.md) | CDC PLACES health measures |
| [svi-methodology.md](svi-methodology.md) | Social Vulnerability Index |
| [adi-methodology.md](adi-methodology.md) | Area Deprivation Index |

### Oncology Reference Data

Located in [oncology/](oncology/):

| File | Description | Records |
|------|-------------|---------|
| [oncology-icd10-codes.csv](oncology/oncology-icd10-codes.csv) | Cancer diagnosis codes | 115 |
| [oncology-medications.csv](oncology/oncology-medications.csv) | Chemotherapy agents | 90 |
| [oncology-regimens.csv](oncology/oncology-regimens.csv) | Treatment protocols | 48 |
| [oncology-tumor-markers.csv](oncology/oncology-tumor-markers.csv) | Lab markers | 31 |
| [oncology-staging-templates.yaml](oncology/oncology-staging-templates.yaml) | TNM staging | YAML |

### C-CDA Reference Data

Located in [ccda/](ccda/):

| File | Description |
|------|-------------|
| [ccda-template-oids.csv](ccda/ccda-template-oids.csv) | OID identifiers |
| [ccda-section-requirements.csv](ccda/ccda-section-requirements.csv) | Section specs |
| [ccda-code-systems.csv](ccda/ccda-code-systems.csv) | Code system mappings |
| [ccda-loinc-lab-panels.csv](ccda/ccda-loinc-lab-panels.csv) | Lab panel codes |
| [ccda-snomed-problem-mappings.csv](ccda/ccda-snomed-problem-mappings.csv) | Problem mappings |
| [ccda-vital-signs-loinc.csv](ccda/ccda-vital-signs-loinc.csv) | Vital sign codes |

### Data Models (models/)

Located in [models/](models/):

| File | Description |
|------|-------------|
| [population-profile.md](models/population-profile.md) | Population profile schema |
| [cohort-specification.md](models/cohort-specification.md) | Cohort definition schema |
| [geographic-entity.md](models/geographic-entity.md) | Geographic entity schema |
| [sdoh-profile.md](models/sdoh-profile.md) | SDOH indicators schema |

## Usage

Reference data is consumed by Skills during generation:

```
User Request → Skill → Reference Data → Generated Output
                          ↓
              Code lookups, validation rules,
              clinical patterns, terminology
```

## Adding Reference Data

1. Determine category (code systems, clinical, population)
2. Use consistent file format (CSV for tabular, YAML for hierarchical, MD for documentation)
3. Include header row for CSV files
4. Add entry to this README
5. Reference from relevant Skills

---

*See [docs/HEALTHSIM-ARCHITECTURE-GUIDE.md](../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) for reference data integration patterns.*
