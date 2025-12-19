---
name: cdisc-adam-format
description: "Transform TrialSim canonical data to CDISC ADaM analysis datasets. Use when user requests: ADaM output, analysis datasets, statistical analysis format."
---

# CDISC ADaM Format

Transform TrialSim canonical JSON to CDISC Analysis Data Model (ADaM) datasets.

## Overview

ADaM datasets are derived from SDTM and optimized for statistical analysis. This skill creates analysis-ready datasets from TrialSim data.

## Core ADaM Datasets

### ADSL (Subject-Level Analysis Dataset)

One record per subject with all baseline and treatment information.

| ADaM Variable | Source | Description |
|---------------|--------|-------------|
| STUDYID | Study.study_id | Study identifier |
| USUBJID | Subject.subject_id | Unique subject identifier |
| SUBJID | Subject.subject_number | Subject number |
| SITEID | Site.site_id | Site identifier |
| TRT01P | Subject.planned_treatment | Planned treatment |
| TRT01A | Subject.actual_treatment | Actual treatment |
| TRTSDT | Subject.first_dose_date | Treatment start date |
| TRTEDT | Subject.last_dose_date | Treatment end date |
| AGE | Subject.age_at_consent | Age at consent |
| AGEGR1 | Derived | Age group (<65/>=65) |
| SEX | Subject.sex | Sex |
| RACE | Subject.race | Race |
| SAFFL | Derived | Safety population flag |
| ITTFL | Derived | ITT population flag |
| EFFFL | Derived | Efficacy population flag |

### ADAE (Adverse Event Analysis Dataset)

One record per adverse event with analysis flags.

| ADaM Variable | Source | Description |
|---------------|--------|-------------|
| STUDYID | Study.study_id | Study identifier |
| USUBJID | Subject.subject_id | Unique subject identifier |
| AESEQ | AdverseEvent.sequence | Sequence number |
| AEDECOD | AdverseEvent.meddra_pt | MedDRA preferred term |
| AEBODSYS | AdverseEvent.meddra_soc | System organ class |
| TRTEMFL | Derived | Treatment-emergent flag |
| AESEV | AdverseEvent.severity | Severity |
| AESER | AdverseEvent.serious | Serious flag |
| AEREL | AdverseEvent.causality | Relationship |
| ASTDT | AdverseEvent.start_date | Analysis start date |
| AENDT | AdverseEvent.end_date | Analysis end date |

### ADEFF (Efficacy Analysis Dataset)

Structure depends on endpoint type. Example for continuous endpoint:

| ADaM Variable | Source | Description |
|---------------|--------|-------------|
| STUDYID | Study.study_id | Study identifier |
| USUBJID | Subject.subject_id | Unique subject identifier |
| PARAMCD | Endpoint.code | Parameter code |
| PARAM | Endpoint.name | Parameter name |
| AVAL | Assessment.value | Analysis value |
| BASE | Derived | Baseline value |
| CHG | Derived | Change from baseline |
| PCHG | Derived | Percent change from baseline |
| AVISIT | Visit.visit_name | Analysis visit |
| ADT | Assessment.date | Analysis date |
| ANL01FL | Derived | Analysis flag |

## Derivation Rules

### Population Flags

```
SAFFL = "Y" if subject received at least one dose of study drug
ITTFL = "Y" if subject was randomized (regardless of treatment received)
EFFFL = "Y" if subject has at least one post-baseline efficacy assessment
```

### Treatment-Emergent AE

```
TRTEMFL = "Y" if AE started on or after first dose date
         AND (AE started before last dose date + 30 days OR end date is missing)
```

### Change from Baseline

```
CHG = AVAL - BASE
PCHG = (CHG / BASE) * 100  (where BASE != 0)
```

## Example Output

**ADSL (CSV)**:
```csv
STUDYID,USUBJID,SUBJID,SITEID,TRT01P,TRT01A,TRTSDT,AGE,AGEGR1,SEX,RACE,SAFFL,ITTFL,EFFFL
TRIAL-001,TRIAL-001-001-0001,0001,001,Treatment,Treatment,2024-01-15,52,<65,M,WHITE,Y,Y,Y
TRIAL-001,TRIAL-001-001-0002,0002,001,Placebo,Placebo,2024-01-18,48,<65,F,BLACK,Y,Y,Y
TRIAL-001,TRIAL-001-002-0001,0001,002,Treatment,Treatment,2024-01-20,68,>=65,M,WHITE,Y,Y,Y
```

**ADAE (CSV)**:
```csv
STUDYID,USUBJID,AESEQ,AEDECOD,AEBODSYS,TRTEMFL,AESEV,AESER,AEREL,ASTDT,AENDT
TRIAL-001,TRIAL-001-001-0001,1,Headache,Nervous system disorders,Y,MILD,N,POSSIBLE,2024-02-01,2024-02-03
TRIAL-001,TRIAL-001-001-0001,2,Nausea,Gastrointestinal disorders,Y,MODERATE,N,PROBABLE,2024-02-15,2024-02-17
```

## Related Skills

- [TrialSim SKILL](../skills/trialsim/SKILL.md) - Source data generation
- [CDISC SDTM Format](cdisc-sdtm.md) - Tabulation datasets
- [clinical-trials-domain.md](../skills/trialsim/clinical-trials-domain.md) - Domain knowledge
