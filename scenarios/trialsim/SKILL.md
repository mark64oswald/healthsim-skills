---
name: healthsim-trialsim
description: "Generate realistic clinical trial synthetic data including study definitions, sites, subjects, visits, adverse events, efficacy assessments, and disposition. Use when user requests: clinical trial data, CDISC/SDTM/ADaM datasets, trial scenarios (Phase I/II/III/IV), FDA submission test data, or specific therapeutic areas like oncology or biologics/CGT."
---

# TrialSim - Clinical Trial Data Generation

## Overview

TrialSim generates realistic synthetic clinical trial data for pharmaceutical and biologics/cell & gene therapy trials. It produces CDISC-compliant formats (SDTM, ADaM) suitable for FDA submission testing, clinical data management system validation, and analytics platform development.

**Key Capabilities:**
- Study protocol definitions with treatment arms and visit schedules
- Multi-site enrollment with realistic recruitment patterns
- Subject randomization and treatment assignment
- Scheduled and unscheduled visit data
- Adverse event generation with severity and causality
- Efficacy endpoint measurements
- Disposition and discontinuation patterns
- CDISC SDTM and ADaM output formats

## Trigger Phrases

Activate TrialSim when user mentions:
- "clinical trial" or "clinical study"
- "CDISC", "SDTM", "ADaM", "CDASH"
- "Phase I", "Phase II", "Phase III", "Phase IV" (or "Phase 1/2/3/4")
- "pivotal trial", "registration trial"
- "FDA submission", "NDA", "BLA", "IND"
- "trial subjects", "study participants"
- "adverse events", "safety data"
- "efficacy endpoints", "primary endpoint"
- "randomization", "treatment arm"
- "oncology trial", "biologics trial", "CGT trial"
- "Define-XML", "ODM-XML"

## Scenario Skills

Load the appropriate scenario based on user request:

| Scenario | Trigger Phrases | File | Status |
|----------|-----------------|------|--------|
| **Phase III Pivotal** | phase 3, pivotal, registration, NDA, BLA | [scenarios/phase3-pivotal.md](scenarios/phase3-pivotal.md) | Active |
| **Phase I Dose Escalation** | phase 1, dose escalation, FIH, first-in-human | scenarios/phase1-dose-escalation.md | Planned |
| **Phase II Proof of Concept** | phase 2, PoC, proof of concept, dose finding | scenarios/phase2-poc.md | Planned |
| **Adaptive Design** | adaptive, platform trial, master protocol, basket, umbrella | scenarios/adaptive-design.md | Planned |

## Domain Skills

Reference domain knowledge for generation patterns:

| Domain | Description | File | Status |
|--------|-------------|------|--------|
| **Clinical Trials Domain** | Core trial concepts, phases, CDISC standards, entity definitions | [domain/clinical-trials-domain.md](domain/clinical-trials-domain.md) | Active |
| **Recruitment & Enrollment** | Screening funnel, consent, eligibility, screen failures | [domain/recruitment-enrollment.md](domain/recruitment-enrollment.md) | Placeholder |

## Therapeutic Areas

Therapeutic area-specific trial patterns:

| Therapeutic Area | Description | File | Status |
|------------------|-------------|------|--------|
| **Oncology** | Solid tumors, hematologic malignancies, RECIST, tumor response | therapeutic-areas/oncology-trials.md | Planned |
| **Biologics/CGT** | Cell therapy, gene therapy, CAR-T, manufacturing | therapeutic-areas/biologics-cgt.md | Planned |
| **Cardiovascular** | CV outcomes, MACE endpoints, heart failure | therapeutic-areas/cardiovascular-trials.md | Planned |
| **CNS/Neurology** | Alzheimer's, Parkinson's, MS, cognitive endpoints | therapeutic-areas/cns-trials.md | Planned |

## Output Formats

| Format | Description | File | Status |
|--------|-------------|------|--------|
| **SDTM** | Study Data Tabulation Model domains | formats/sdtm-output.md | Planned |
| **ADaM** | Analysis Data Model datasets | formats/adam-output.md | Planned |
| **ODM-XML** | Operational Data Model | formats/odm-xml.md | Planned |
| **Define-XML** | Dataset definitions for FDA submission | formats/define-xml.md | Planned |
| **Dimensional** | Star schema for analytics | [../../formats/dimensional-analytics.md](../../formats/dimensional-analytics.md) | Shared |

## Key Entities

TrialSim generates these core entities:

| Entity | Description | SDTM Domain |
|--------|-------------|-------------|
| **Study** | Protocol definition, design, objectives | TS, TA, TE, TV |
| **Site** | Investigator site with country, enrollment capacity | - |
| **Subject** | Trial participant (extends Patient) | DM |
| **TreatmentArm** | Randomization arm assignment | TA |
| **Randomization** | Subject randomization record | DM.ARM, DM.ACTARM |
| **Visit** | Scheduled/unscheduled visit occurrence | SV |
| **AdverseEvent** | Safety event with severity, causality | AE |
| **ConcomitantMed** | Non-study medications | CM |
| **MedicalHistory** | Pre-existing conditions | MH |
| **VitalSign** | Trial vital sign measurements | VS |
| **LabResult** | Central/local lab results | LB |
| **EfficacyAssessment** | Primary/secondary endpoint data | Custom (TR, RS, etc.) |
| **Disposition** | Study completion/discontinuation | DS |
| **ProtocolDeviation** | Protocol non-compliance events | DV |

## Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| study_phase | string | "III" | Trial phase (I, II, III, IV) |
| therapeutic_area | string | "oncology" | Disease area |
| subject_count | int | 100 | Number of subjects to generate |
| site_count | int | 10 | Number of investigator sites |
| treatment_arms | int | 2 | Number of treatment arms |
| visit_schedule | list | protocol-defined | Visit windows and assessments |
| ae_rate | float | 0.6 | Proportion of subjects with AEs |
| discontinuation_rate | float | 0.15 | Early termination rate |
| seed | int | random | For reproducible generation |

## Cross-Product Integration

### Patient to Subject Transformation

TrialSim subjects extend PatientSim patients:

```
PatientSim Patient          TrialSim Subject
├── person_id        →      ├── person_id (same)
├── mrn              →      ├── mrn (if available)
├── demographics     →      ├── demographics
├── medical_history  →      ├── medical_history (MH domain)
└── medications      →      └── concomitant_meds (CM domain)
                            ├── subject_id (USUBJID)
                            ├── consent_date (RFICDTC)
                            ├── randomization_date (RANDDT)
                            ├── treatment_arm (ARM/ACTARM)
                            └── trial_status
```

### Claims Integration (MemberSim)

Trial-related healthcare services generate claims:
- Screening visits → Professional claims
- Treatment administration → Facility claims (if infusion)
- Lab work → Lab claims
- Serious adverse events → Inpatient claims

### Pharmacy Integration (RxMemberSim)

- Concomitant medications appear in pharmacy claims
- Study drug is tracked separately (not in pharmacy claims)

## SDTM Domain Reference

Quick reference for CDISC SDTM domains generated:

| Category | Domains | Description |
|----------|---------|-------------|
| **Trial Design** | TS, TA, TE, TV, TI | Study parameters, arms, elements, visits |
| **Demographics** | DM, SC | Subject demographics, characteristics |
| **Interventions** | EX, CM, SU | Exposure, concomitant meds, substance use |
| **Events** | AE, DS, MH, CE, DV | Adverse events, disposition, history, deviations |
| **Findings** | VS, LB, EG, PE | Vitals, labs, ECG, physical exam |
| **Special Purpose** | SV, CO | Subject visits, comments |

See [domain/clinical-trials-domain.md](domain/clinical-trials-domain.md) for detailed SDTM specifications.

## Examples

### Example 1: Simple Phase III Trial

**Request:** "Generate a small Phase III oncology trial with 10 subjects"

**Output:** See [../../hello-healthsim/trialsim-quickstart.md](../../hello-healthsim/trialsim-quickstart.md)

### Example 2: With SDTM Output

**Request:** "Generate trial data and output as SDTM DM and AE domains"

Claude will:
1. Generate canonical trial data
2. Transform to SDTM format
3. Output DM.csv and AE.csv with proper variable names

## Validation Rules

TrialSim validates generated data for:

1. **Protocol Compliance**: Visits within windows, required assessments present
2. **Temporal Consistency**: Consent → Randomization → Treatment → Disposition
3. **CDISC Conformance**: Variable names, controlled terminology, required fields
4. **Clinical Plausibility**: Age-appropriate conditions, realistic lab ranges
5. **Referential Integrity**: Subject IDs consistent across domains

## Related Skills

- [domain/clinical-trials-domain.md](domain/clinical-trials-domain.md) - Core domain knowledge
- [domain/recruitment-enrollment.md](domain/recruitment-enrollment.md) - Recruitment patterns
- [../../formats/dimensional-analytics.md](../../formats/dimensional-analytics.md) - Analytics output
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10, MedDRA, LOINC codes
