---
name: healthsim-trialsim
description: "Generate realistic clinical trial synthetic data including study definitions, sites, subjects, visits, adverse events, efficacy assessments, and disposition. Use when user requests: clinical trial data, CDISC/SDTM/ADaM datasets, trial scenarios (Phase I/II/III/IV), FDA submission test data, or specific therapeutic areas like oncology or biologics/CGT."
---

# TrialSim

**Status**: Active Development

TrialSim generates realistic synthetic clinical trial data for testing, training, and development purposes.

## Overview

TrialSim provides:
- Complete study lifecycle data (protocol to closeout)
- Multi-site, multi-country trial configurations
- Subject-level longitudinal data with realistic patterns
- Safety data (adverse events, labs, vitals)
- Efficacy endpoints (primary, secondary, exploratory)
- CDISC-compliant output (SDTM, ADaM)

## Trigger Phrases

Activate TrialSim when user mentions:
- "clinical trial" or "clinical study"
- "Phase I/II/III/IV" or "pivotal trial"
- "CDISC", "SDTM", "ADaM"
- "FDA submission data" or "regulatory data"
- "adverse events" or "safety data"
- "efficacy endpoints"
- Trial therapeutic areas (oncology, cardiology, etc.)
- SDTM domains (DM, AE, VS, LB, CM, EX, DS)

## Quick Links

### Core Skills

| Topic | Skill | Description |
|-------|-------|-------------|
| Domain Knowledge | [clinical-trials-domain.md](clinical-trials-domain.md) | Core trial concepts, phases, regulatory |
| Recruitment | [recruitment-enrollment.md](recruitment-enrollment.md) | Screening funnel, enrollment patterns |
| Phase 3 Trials | [phase3-pivotal.md](phase3-pivotal.md) | Pivotal registration trials |

### SDTM Domain Skills

| Domain | Skill | Description |
|--------|-------|-------------|
| DM | [domains/demographics-dm.md](domains/demographics-dm.md) | Subject demographics, treatment arms |
| AE | [domains/adverse-events-ae.md](domains/adverse-events-ae.md) | Adverse events with MedDRA coding |
| VS | [domains/vital-signs-vs.md](domains/vital-signs-vs.md) | Vital sign measurements |
| LB | [domains/laboratory-lb.md](domains/laboratory-lb.md) | Laboratory results with LOINC |
| CM | [domains/concomitant-meds-cm.md](domains/concomitant-meds-cm.md) | Concomitant medications with ATC |
| EX | [domains/exposure-ex.md](domains/exposure-ex.md) | Study drug exposure, dose modifications |
| DS | [domains/disposition-ds.md](domains/disposition-ds.md) | Subject disposition, discontinuation |
| MH | [domains/medical-history-mh.md](domains/medical-history-mh.md) | Medical history, comorbidities |
| Domain Index | [domains/README.md](domains/README.md) | All SDTM domains overview |

### Therapeutic Areas

| Area | Skill | Key Endpoints |
|------|-------|---------------|
| Oncology | [therapeutic-areas/oncology.md](therapeutic-areas/oncology.md) | RECIST, ORR, PFS, OS |
| Cardiovascular | [therapeutic-areas/cardiovascular.md](therapeutic-areas/cardiovascular.md) | MACE, CV outcomes |
| CNS | [therapeutic-areas/cns.md](therapeutic-areas/cns.md) | Cognitive scales, imaging |
| CGT | [therapeutic-areas/cgt.md](therapeutic-areas/cgt.md) | CAR-T, gene therapy |

### Real World Evidence

| Topic | Skill | Description |
|-------|-------|-------------|
| RWE Overview | [rwe/overview.md](rwe/overview.md) | RWE concepts, data sources |
| Synthetic Controls | [rwe/synthetic-control.md](rwe/synthetic-control.md) | External control arm generation |

## Output Formats

| Format | Skill | Use Case |
|--------|-------|----------|
| SDTM | [../../formats/cdisc-sdtm.md](../../formats/cdisc-sdtm.md) | Regulatory submission |
| ADaM | [../../formats/cdisc-adam.md](../../formats/cdisc-adam.md) | Statistical analysis |
| JSON | Default | API integration |
| CSV | [../../formats/csv.md](../../formats/csv.md) | Spreadsheet analysis |

## Core Entities

### Study
```json
{
  "study_id": "ABC-123-001",
  "protocol_title": "A Phase 3, Randomized, Double-Blind Study...",
  "phase": "Phase 3",
  "therapeutic_area": "Oncology",
  "indication": "Non-Small Cell Lung Cancer",
  "sponsor": "Example Pharma Inc.",
  "status": "Ongoing",
  "sites": [],
  "arms": []
}
```

### Subject
```json
{
  "subject_id": "001-0001",
  "site_id": "001",
  "screening_date": "2024-01-15",
  "randomization_date": "2024-01-22",
  "arm": "Treatment",
  "status": "Active",
  "demographics": {},
  "visits": [],
  "adverse_events": [],
  "efficacy_assessments": []
}
```

## Integration with Other Products

TrialSim integrates with other HealthSim products for complete clinical trial data:

| From | To | Integration Pattern |
|------|-----|---------------------|
| PatientSim | TrialSim | Patient → Subject (add consent, randomization, protocol visits) |
| NetworkSim | TrialSim | Provider → Investigator (add credentials, training, delegation log) |
| PopulationSim | TrialSim | Demographics → Recruitment pool (geographic, demographic eligibility) |

### Cross-Product: PatientSim

Trial subjects are patients with additional trial-specific data:

- [../patientsim/oncology/](../patientsim/oncology/) - Oncology trial subjects
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - CV outcomes trial subjects
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - CNS trial subjects
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Metabolic trial subjects

> **Integration Pattern:** Use PatientSim for baseline clinical characteristics. TrialSim adds protocol-specific assessments (RECIST, NYHA class changes), randomization, and SDTM-formatted data.

## Development Status

| Component | Status |
|-----------|--------|
| SKILL.md (this file) | ✅ Complete |
| clinical-trials-domain.md | ✅ Complete |
| recruitment-enrollment.md | ✅ Complete |
| phase3-pivotal.md | ✅ Complete |
| domains/ (DM, AE, VS, LB, CM, EX, DS, MH) | ✅ Complete |
| therapeutic-areas/ | ✅ Complete |
| rwe/ | ✅ Complete |
| phase1-dose-escalation.md | 📋 Planned |
| phase2-proof-of-concept.md | 📋 Planned |

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data
- [MemberSim](../membersim/SKILL.md) - Claims integration
- [Code Systems](../../references/code-systems.md) - Standard terminologies

## Usage Examples

### Example 1: Basic Phase 3 Trial

**Prompt:** "Generate a Phase 3 oncology trial with 200 subjects"

**Output:**
```json
{
  "study": {
    "study_id": "ONCO-2025-001",
    "protocol_title": "A Phase 3, Randomized, Double-Blind, Placebo-Controlled Study of ABC-123 in Advanced NSCLC",
    "phase": "Phase 3",
    "therapeutic_area": "Oncology",
    "indication": "Non-Small Cell Lung Cancer",
    "design": "Randomized, Double-Blind, Placebo-Controlled",
    "primary_endpoint": "Overall Survival",
    "target_enrollment": 200,
    "arms": [
      { "arm_id": "A", "name": "ABC-123 + SOC", "allocation_ratio": 1 },
      { "arm_id": "B", "name": "Placebo + SOC", "allocation_ratio": 1 }
    ]
  },
  "sites": [
    { "site_id": "001", "name": "Memorial Cancer Center", "country": "USA", "enrolled": 25 },
    { "site_id": "002", "name": "University Oncology", "country": "USA", "enrolled": 22 }
  ],
  "subjects": [
    {
      "subject_id": "001-0001",
      "site_id": "001",
      "arm": "A",
      "status": "Active",
      "randomization_date": "2025-01-15"
    }
  ]
}
```

### Example 2: Adverse Events with MedDRA

**Prompt:** "Generate adverse events for a 50-subject immunotherapy trial"

**Output:**
```json
{
  "domain": "AE",
  "adverse_events": [
    {
      "USUBJID": "IO-001-0023",
      "AESEQ": 1,
      "AETERM": "Fatigue",
      "AEDECOD": "Fatigue",
      "AEBODSYS": "General disorders and administration site conditions",
      "AESEV": "MILD",
      "AESER": "N",
      "AEREL": "POSSIBLY RELATED",
      "AESTDTC": "2025-02-10",
      "AEENDTC": "2025-02-18",
      "AEOUT": "RECOVERED/RESOLVED"
    },
    {
      "USUBJID": "IO-001-0007",
      "AESEQ": 1,
      "AETERM": "Immune-mediated colitis",
      "AEDECOD": "Colitis",
      "AEBODSYS": "Gastrointestinal disorders",
      "AESEV": "SEVERE",
      "AESER": "Y",
      "AESHOSP": "Y",
      "AEREL": "RELATED",
      "AEACN": "DRUG INTERRUPTED",
      "AESTDTC": "2025-03-05",
      "AEOUT": "NOT RECOVERED/NOT RESOLVED"
    }
  ]
}
```

### Example 3: Screening and Enrollment

**Prompt:** "Generate screening data with 30% screen failure rate for 100 subjects"

**Output:**
```json
{
  "screening_summary": {
    "total_screened": 143,
    "screen_passed": 100,
    "screen_failed": 43,
    "screen_failure_rate": 0.30
  },
  "screen_failures": [
    {
      "screening_id": "SCR-0015",
      "failure_reason": "Inclusion criteria not met",
      "failure_detail": "EGFR mutation negative",
      "screening_date": "2025-01-20"
    },
    {
      "screening_id": "SCR-0028",
      "failure_reason": "Exclusion criteria met",
      "failure_detail": "Prior immunotherapy within 6 months",
      "screening_date": "2025-01-25"
    }
  ]
}
```

### Example 4: DM Domain SDTM Output

**Prompt:** "Generate DM domain for 10 subjects as SDTM"

**Output:**
```json
{
  "domain": "DM",
  "records": [
    {
      "STUDYID": "ONCO-2025-001",
      "DOMAIN": "DM",
      "USUBJID": "ONCO-2025-001-001-0001",
      "SUBJID": "0001",
      "SITEID": "001",
      "RFSTDTC": "2025-01-22",
      "RFENDTC": null,
      "BRTHDTC": "1958-05-15",
      "AGE": 66,
      "AGEU": "YEARS",
      "SEX": "M",
      "RACE": "WHITE",
      "ETHNIC": "NOT HISPANIC OR LATINO",
      "ARMCD": "TRT",
      "ARM": "ABC-123 + SOC",
      "COUNTRY": "USA"
    }
  ]
}
```

### Example 5: Laboratory Results with LOINC

**Prompt:** "Generate LB domain with liver function tests for safety monitoring"

**Output:**
```json
{
  "domain": "LB",
  "records": [
    {
      "STUDYID": "SAFE-001",
      "DOMAIN": "LB",
      "USUBJID": "SAFE-001-001-0042",
      "LBSEQ": 1,
      "LBTESTCD": "ALT",
      "LBTEST": "Alanine Aminotransferase",
      "LBCAT": "CHEMISTRY",
      "LBORRES": "32",
      "LBORRESU": "U/L",
      "LBSTRESN": 32,
      "LBSTRESU": "U/L",
      "LBSTNRLO": 7,
      "LBSTNRHI": 56,
      "LBNRIND": "NORMAL",
      "LBLOINC": "1742-6",
      "LBBLFL": "Y",
      "VISITNUM": 2,
      "VISIT": "BASELINE"
    }
  ]
}
```
