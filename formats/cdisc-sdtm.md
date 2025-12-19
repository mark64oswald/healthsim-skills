---
name: cdisc-sdtm-format
description: "Transform TrialSim canonical data to CDISC SDTM domain datasets. Use when user requests: SDTM output, regulatory submission format, clinical trial tabulations."
---

# CDISC SDTM Format

Transform TrialSim canonical JSON to CDISC Study Data Tabulation Model (SDTM) datasets.

## Overview

SDTM is the FDA-required format for clinical trial data submissions. This skill maps TrialSim entities to standard SDTM domains.

## Core SDTM Domains

### Demographics (DM)

Maps Subject entity to DM domain.

| SDTM Variable | Source | Description |
|---------------|--------|-------------|
| STUDYID | Study.study_id | Study identifier |
| DOMAIN | "DM" | Domain abbreviation |
| USUBJID | Subject.subject_id | Unique subject identifier |
| SUBJID | Subject.subject_number | Subject number within site |
| SITEID | Site.site_id | Site identifier |
| RFSTDTC | Subject.first_dose_date | First dose date |
| RFENDTC | Subject.last_dose_date | Last dose date |
| AGE | Subject.age_at_consent | Age at consent |
| AGEU | "YEARS" | Age units |
| SEX | Subject.sex | Sex (M/F) |
| RACE | Subject.race | Race |
| ETHNIC | Subject.ethnicity | Ethnicity |
| ARMCD | Subject.arm_code | Treatment arm code |
| ARM | Subject.arm_name | Treatment arm name |
| COUNTRY | Site.country | Country |

### Adverse Events (AE)

Maps AdverseEvent entity to AE domain.

| SDTM Variable | Source | Description |
|---------------|--------|-------------|
| STUDYID | Study.study_id | Study identifier |
| DOMAIN | "AE" | Domain abbreviation |
| USUBJID | Subject.subject_id | Unique subject identifier |
| AESEQ | AdverseEvent.sequence | Sequence number |
| AETERM | AdverseEvent.reported_term | Reported term |
| AEDECOD | AdverseEvent.meddra_pt | MedDRA preferred term |
| AEBODSYS | AdverseEvent.meddra_soc | MedDRA system organ class |
| AESEV | AdverseEvent.severity | Severity (MILD/MODERATE/SEVERE) |
| AESER | AdverseEvent.serious | Serious (Y/N) |
| AEREL | AdverseEvent.causality | Relationship to study drug |
| AEACN | AdverseEvent.action_taken | Action taken |
| AEOUT | AdverseEvent.outcome | Outcome |
| AESTDTC | AdverseEvent.start_date | Start date |
| AEENDTC | AdverseEvent.end_date | End date |

### Concomitant Medications (CM)

Maps ConcomitantMedication entity to CM domain.

| SDTM Variable | Source | Description |
|---------------|--------|-------------|
| STUDYID | Study.study_id | Study identifier |
| DOMAIN | "CM" | Domain abbreviation |
| USUBJID | Subject.subject_id | Unique subject identifier |
| CMSEQ | ConcomitantMedication.sequence | Sequence number |
| CMTRT | ConcomitantMedication.medication_name | Medication name |
| CMDECOD | ConcomitantMedication.who_drug_code | WHO Drug code |
| CMINDC | ConcomitantMedication.indication | Indication |
| CMDOSE | ConcomitantMedication.dose | Dose |
| CMDOSU | ConcomitantMedication.dose_unit | Dose unit |
| CMROUTE | ConcomitantMedication.route | Route |
| CMSTDTC | ConcomitantMedication.start_date | Start date |
| CMENDTC | ConcomitantMedication.end_date | End date |

### Subject Visits (SV)

Maps Visit entity to SV domain.

| SDTM Variable | Source | Description |
|---------------|--------|-------------|
| STUDYID | Study.study_id | Study identifier |
| DOMAIN | "SV" | Domain abbreviation |
| USUBJID | Subject.subject_id | Unique subject identifier |
| VISITNUM | Visit.visit_number | Visit number |
| VISIT | Visit.visit_name | Visit name |
| VISITDY | Visit.planned_day | Planned study day |
| SVSTDTC | Visit.actual_date | Actual visit date |

## Example Output

**DM Domain (CSV)**:
```csv
STUDYID,DOMAIN,USUBJID,SUBJID,SITEID,RFSTDTC,AGE,AGEU,SEX,RACE,ARMCD,ARM,COUNTRY
TRIAL-001,DM,TRIAL-001-001-0001,0001,001,2024-01-15,52,YEARS,M,WHITE,TRT,Treatment,USA
TRIAL-001,DM,TRIAL-001-001-0002,0002,001,2024-01-18,48,YEARS,F,BLACK OR AFRICAN AMERICAN,PBO,Placebo,USA
```

**AE Domain (CSV)**:
```csv
STUDYID,DOMAIN,USUBJID,AESEQ,AETERM,AEDECOD,AEBODSYS,AESEV,AESER,AEREL,AESTDTC,AEENDTC
TRIAL-001,AE,TRIAL-001-001-0001,1,Headache,Headache,Nervous system disorders,MILD,N,POSSIBLE,2024-02-01,2024-02-03
TRIAL-001,AE,TRIAL-001-001-0001,2,Nausea,Nausea,Gastrointestinal disorders,MODERATE,N,PROBABLE,2024-02-15,2024-02-17
```

## Related Skills

- [TrialSim SKILL](../skills/trialsim/SKILL.md) - Source data generation
- [CDISC ADaM Format](cdisc-adam.md) - Analysis datasets
- [clinical-trials-domain.md](../skills/trialsim/clinical-trials-domain.md) - Domain knowledge
