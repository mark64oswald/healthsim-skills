---
name: clinical-trials-domain
description: "Core domain knowledge for clinical trial data generation including trial phases, CDISC standards, regulatory requirements, safety/efficacy patterns, and cross-product integration. Referenced by all TrialSim scenario skills."
---

# Clinical Trials Domain Knowledge

## Overview

This skill provides foundational domain knowledge for generating realistic clinical trial data. It covers regulatory frameworks, trial design patterns, CDISC standards, and data generation rules that ensure synthetic trial data is plausible and standards-compliant.

## Trial Phases

### Phase I - Safety and Pharmacokinetics

**Purpose:** Establish initial safety profile and determine dosing

| Characteristic | Typical Value |
|----------------|---------------|
| Subject Count | 20-100 |
| Duration | 6-12 months |
| Population | Healthy volunteers (or patients for oncology) |
| Primary Endpoints | MTD, DLT, PK parameters |
| Design | Dose escalation (3+3, mTPI, BOIN) |

**Key Data Elements:**
- Dose limiting toxicities (DLTs)
- Pharmacokinetic sampling (dense PK)
- Maximum tolerated dose (MTD) determination
- Single ascending dose (SAD) / Multiple ascending dose (MAD)

### Phase II - Efficacy Signal and Dose Selection

**Purpose:** Evaluate efficacy and refine dosing

| Characteristic | Typical Value |
|----------------|---------------|
| Subject Count | 100-300 |
| Duration | 1-2 years |
| Population | Patients with target condition |
| Primary Endpoints | Efficacy biomarker, response rate |
| Design | Randomized, controlled (may be single-arm in oncology) |

**Key Data Elements:**
- Preliminary efficacy signals
- Dose-response relationship
- Safety in target population
- Optimal dose selection for Phase III

### Phase III - Confirmatory/Pivotal

**Purpose:** Confirm efficacy and safety for registration

| Characteristic | Typical Value |
|----------------|---------------|
| Subject Count | 300-3000+ |
| Duration | 2-4 years |
| Population | Broader patient population |
| Primary Endpoints | Clinical outcomes, PROs |
| Design | Randomized, double-blind, controlled |

**Key Data Elements:**
- Primary efficacy endpoint(s)
- Comprehensive safety database
- Subgroup analyses
- Risk-benefit assessment

### Phase IV - Post-Marketing

**Purpose:** Long-term safety, real-world effectiveness

| Characteristic | Typical Value |
|----------------|---------------|
| Subject Count | 1000-10000+ |
| Duration | Years |
| Population | Broad, real-world |
| Primary Endpoints | Safety signals, effectiveness |
| Design | Observational, pragmatic |

**Key Data Elements:**
- Rare adverse events
- Long-term outcomes
- Drug utilization patterns
- Comparative effectiveness

## Trial Design Types

### Parallel Design

Standard design with subjects randomized to treatment arms maintained throughout.

```
Randomization
    ├── Arm A (Treatment) ──────────────────► End of Study
    └── Arm B (Control) ────────────────────► End of Study
```

**Use When:** Standard efficacy/safety evaluation

### Crossover Design

Subjects receive both treatments in sequence with washout period.

```
Randomization
    ├── Sequence AB: Treatment A → Washout → Treatment B → End
    └── Sequence BA: Treatment B → Washout → Treatment A → End
```

**Use When:**
- Chronic, stable conditions
- Treatments with reversible effects
- Reduced sample size needed

### Adaptive Design

Prospectively planned modifications based on interim data.

**Types:**
- Sample size re-estimation
- Response adaptive randomization
- Seamless Phase II/III
- Biomarker-driven enrichment

### Decentralized Trials (DCT)

Remote/hybrid trials with reduced site visits.

**Elements:**
- eConsent
- Remote monitoring devices
- Telemedicine visits
- Home health visits
- Direct-to-patient drug shipping

### Master Protocols

**Basket Trial:** Single drug, multiple tumor types
**Umbrella Trial:** Single tumor type, multiple drugs
**Platform Trial:** Multiple drugs, adaptive additions/graduations

## CDISC Standards Overview

### CDASH (Clinical Data Acquisition Standards Harmonization)

Standard for data collection on Case Report Forms (CRFs).

**Key Concepts:**
- Core variables (highly recommended)
- Supplemental variables (recommended)
- Common data collection standards

### SDTM (Study Data Tabulation Model)

Standard for organizing raw collected data.

**Structure:**
- Domains (datasets for related data)
- Variables (columns with standard names)
- Controlled terminology (standard values)
- Define-XML (metadata specification)

### ADaM (Analysis Data Model)

Standard for analysis-ready datasets.

**Key Datasets:**
- ADSL (Subject-Level Analysis Dataset)
- ADAE (Adverse Events Analysis Dataset)
- ADTTE (Time-to-Event Analysis Dataset)
- BDS (Basic Data Structure) for findings

**Key Variables:**
- PARAMCD/PARAM (parameter identification)
- AVAL/AVALC (analysis values)
- ANL01FL (analysis population flags)
- BASE, CHG (baseline and change)

## Key Entity Definitions

### Study

```json
{
  "study_id": "ABC-123-001",
  "sponsor": "PharmaCorp",
  "title": "A Phase III Study of Drug X in Patients with Condition Y",
  "phase": "III",
  "design": "randomized, double-blind, placebo-controlled",
  "therapeutic_area": "Oncology",
  "indication": "Advanced Non-Small Cell Lung Cancer",
  "planned_enrollment": 450,
  "treatment_arms": [
    {"arm_code": "A", "arm_name": "Drug X 200mg", "ratio": 2},
    {"arm_code": "B", "arm_name": "Placebo", "ratio": 1}
  ],
  "primary_endpoint": "Progression-Free Survival",
  "study_start_date": "2024-01-15",
  "planned_end_date": "2027-06-30"
}
```

### Site (Investigator Site)

```json
{
  "site_id": "001",
  "site_name": "University Medical Center",
  "investigator": {
    "name": "Dr. Jane Smith",
    "npi": "1234567890"
  },
  "country": "USA",
  "state": "PA",
  "city": "Pittsburgh",
  "target_enrollment": 25,
  "actual_enrollment": 22,
  "site_status": "active",
  "first_subject_in": "2024-03-10",
  "irb_approval_date": "2024-02-01"
}
```

### Subject

```json
{
  "subject_id": "ABC-123-001-001",
  "usubjid": "ABC-123-001-001",
  "site_id": "001",
  "screening_number": "SCR-001",
  "demographics": {
    "age": 62,
    "sex": "F",
    "race": "WHITE",
    "ethnicity": "NOT HISPANIC OR LATINO",
    "country": "USA"
  },
  "consent_date": "2024-03-15",
  "screening_date": "2024-03-15",
  "randomization_date": "2024-03-22",
  "treatment_arm": "A",
  "actual_arm": "A",
  "study_status": "COMPLETED",
  "end_date": "2024-12-15",
  "disposition": "COMPLETED"
}
```

### Adverse Event

```json
{
  "ae_id": "AE001",
  "subject_id": "ABC-123-001-001",
  "ae_term": "Nausea",
  "ae_preferred_term": "Nausea",
  "ae_soc": "Gastrointestinal disorders",
  "start_date": "2024-04-01",
  "end_date": "2024-04-05",
  "severity": "MODERATE",
  "serious": false,
  "causality": "POSSIBLY RELATED",
  "action_taken": "DOSE NOT CHANGED",
  "outcome": "RECOVERED/RESOLVED"
}
```

### Visit

```json
{
  "visit_id": "V003",
  "subject_id": "ABC-123-001-001",
  "visit_name": "Week 4",
  "visit_number": 3,
  "scheduled_date": "2024-04-19",
  "actual_date": "2024-04-20",
  "visit_type": "SCHEDULED",
  "assessments_completed": ["VS", "LB", "AE", "CM"],
  "protocol_deviation": false
}
```

## Safety Data Patterns

### Adverse Event Severity

| Grade | Severity | Description |
|-------|----------|-------------|
| 1 | MILD | Awareness of symptoms, easily tolerated |
| 2 | MODERATE | Discomfort, interference with usual activity |
| 3 | SEVERE | Significant interference, may require intervention |
| 4 | LIFE-THREATENING | Urgent intervention required |
| 5 | DEATH | Death related to AE |

### Causality Assessment

| Category | Description |
|----------|-------------|
| NOT RELATED | Event clearly due to other cause |
| UNLIKELY | Little evidence of relationship |
| POSSIBLY RELATED | Could be related but uncertain |
| PROBABLY RELATED | High likelihood of relationship |
| DEFINITELY RELATED | Clear causal relationship |

### Serious Adverse Event (SAE) Criteria

An AE is serious if it:
- Results in death
- Is life-threatening
- Requires inpatient hospitalization or prolongation
- Results in persistent/significant disability
- Is a congenital anomaly/birth defect
- Requires intervention to prevent permanent impairment

### Common AE Distribution by Phase

| Phase | Overall AE Rate | SAE Rate | Discontinuation for AE |
|-------|-----------------|----------|------------------------|
| I | 70-90% | 5-10% | 5-15% |
| II | 60-80% | 3-8% | 5-10% |
| III | 50-70% | 2-5% | 3-8% |

### AE Pattern by SOC (Example: Small Molecule Oncology)

| System Organ Class | Frequency |
|--------------------|-----------|
| Gastrointestinal disorders | 60% |
| General disorders | 50% |
| Skin and subcutaneous tissue | 40% |
| Infections and infestations | 35% |
| Blood and lymphatic system | 30% |
| Nervous system disorders | 25% |

## Efficacy Data Patterns

### Response Criteria Examples

**RECIST 1.1 (Solid Tumors):**
- CR: Complete Response (target lesions disappeared)
- PR: Partial Response (>=30% decrease)
- SD: Stable Disease
- PD: Progressive Disease (>=20% increase)

**Time-to-Event Endpoints:**
- Progression-Free Survival (PFS)
- Overall Survival (OS)
- Disease-Free Survival (DFS)
- Time to Progression (TTP)

### Typical Response Rates (Oncology)

| Setting | ORR Range | Median PFS |
|---------|-----------|------------|
| 1L Metastatic | 30-60% | 8-16 months |
| 2L+ Metastatic | 15-35% | 4-8 months |
| Immunotherapy | 20-40% | Variable |
| Targeted Therapy | 40-70% | 10-18 months |

## Discontinuation Patterns

### Common Discontinuation Reasons

| Reason | SDTM DSDECOD | Typical Rate |
|--------|--------------|--------------|
| Completed | COMPLETED | 70-85% |
| Adverse Event | ADVERSE EVENT | 3-8% |
| Disease Progression | DISEASE PROGRESSION | 5-15% |
| Withdrawal by Subject | WITHDRAWAL BY SUBJECT | 2-5% |
| Lost to Follow-up | LOST TO FOLLOW-UP | 1-3% |
| Protocol Deviation | PROTOCOL DEVIATION | 1-2% |
| Death | DEATH | 0-5% |
| Physician Decision | PHYSICIAN DECISION | 1-2% |

### Timing Patterns

- Early discontinuation (first 25% of study): Higher in Phase I
- Mid-study discontinuation: Often disease progression
- Late discontinuation: Mostly completed, some AE-related

## Cross-Product Connections

### PatientSim Integration

| PatientSim Entity | TrialSim Entity | Mapping |
|-------------------|-----------------|---------|
| Patient | Subject | 1:1 (subject extends patient) |
| Demographics | DM Domain | Direct mapping |
| Diagnoses | MH Domain | Medical history |
| Medications | CM Domain | Concomitant meds |
| Lab Results | LB Domain | Labs (if pre-trial) |
| Encounters | Trial Visits | Different context |

### MemberSim Integration

Trial-related services can generate claims:
- Screening visits
- Protocol-required procedures
- SAE hospitalizations
- Follow-up visits

**Note:** Study drug administration is typically sponsor-covered, not billed to insurance.

### RxMemberSim Integration

- Concomitant medications may appear in pharmacy claims
- Rescue medications for AEs
- Supportive care medications

## SDTM Domain Reference

### Trial Design Domains

| Domain | Name | Description |
|--------|------|-------------|
| TS | Trial Summary | Key protocol parameters |
| TA | Trial Arms | Treatment arm definitions |
| TE | Trial Elements | Study periods/epochs |
| TV | Trial Visits | Scheduled visit definitions |
| TI | Trial Inclusion/Exclusion | I/E criteria |

### Demographics Domain (DM)

| Variable | Label | Example |
|----------|-------|---------|
| STUDYID | Study Identifier | ABC-123 |
| USUBJID | Unique Subject ID | ABC-123-001-001 |
| SUBJID | Subject ID | 001 |
| SITEID | Site ID | 001 |
| AGE | Age | 62 |
| AGEU | Age Units | YEARS |
| SEX | Sex | F |
| RACE | Race | WHITE |
| ETHNIC | Ethnicity | NOT HISPANIC OR LATINO |
| ARM | Planned Arm | Drug X 200mg |
| ACTARM | Actual Arm | Drug X 200mg |
| RFSTDTC | First Study Treatment | 2024-03-25 |
| RFENDTC | Last Study Treatment | 2024-12-10 |

### Adverse Events Domain (AE)

| Variable | Label | Example |
|----------|-------|---------|
| AETERM | Reported Term | Nausea |
| AEDECOD | Dictionary Term | Nausea |
| AEBODSYS | Body System/SOC | Gastrointestinal disorders |
| AESEV | Severity | MODERATE |
| AESER | Serious | N |
| AEREL | Causality | POSSIBLY RELATED |
| AEACN | Action Taken | DOSE NOT CHANGED |
| AEOUT | Outcome | RECOVERED/RESOLVED |
| AESTDTC | Start Date | 2024-04-01 |
| AEENDTC | End Date | 2024-04-05 |

### Other Key Domains

| Domain | Name | Key Variables |
|--------|------|---------------|
| CM | Concomitant Meds | CMTRT, CMDOSE, CMDOSU, CMSTDTC |
| MH | Medical History | MHTERM, MHDECOD, MHSTDTC |
| VS | Vital Signs | VSTEST, VSORRES, VSORRESU, VSDTC |
| LB | Laboratory | LBTEST, LBORRES, LBORNRLO/HI, LBDTC |
| EX | Exposure | EXTRT, EXDOSE, EXDOSU, EXSTDTC |
| DS | Disposition | DSDECOD, DSCAT, DSSTDTC |
| SV | Subject Visits | VISIT, VISITNUM, SVSTDTC |
| DV | Protocol Deviations | DVTERM, DVCAT, DVSTDTC |

## Controlled Terminology

### Common CDISC Controlled Terms

**Sex (DM.SEX):** M, F, U (undifferentiated)

**Race (DM.RACE):**
- AMERICAN INDIAN OR ALASKA NATIVE
- ASIAN
- BLACK OR AFRICAN AMERICAN
- NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER
- WHITE
- MULTIPLE
- OTHER
- UNKNOWN

**AE Severity (AE.AESEV):** MILD, MODERATE, SEVERE, LIFE THREATENING, FATAL

**AE Outcome (AE.AEOUT):**
- RECOVERED/RESOLVED
- RECOVERING/RESOLVING
- NOT RECOVERED/NOT RESOLVED
- RECOVERED/RESOLVED WITH SEQUELAE
- FATAL
- UNKNOWN

**Disposition (DS.DSDECOD):**
- COMPLETED
- ADVERSE EVENT
- DEATH
- LOST TO FOLLOW-UP
- PHYSICIAN DECISION
- PROTOCOL DEVIATION
- PREGNANCY
- WITHDRAWAL BY SUBJECT
- LACK OF EFFICACY

## See Also

- [../SKILL.md](../SKILL.md) - TrialSim overview and routing
- [recruitment-enrollment.md](recruitment-enrollment.md) - Recruitment patterns
- [../scenarios/phase3-pivotal.md](../scenarios/phase3-pivotal.md) - Phase III trial scenario
- [../../references/code-systems.md](../../references/code-systems.md) - Code system references
