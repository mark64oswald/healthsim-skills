---
name: healthsim-trialsim
description: "Generate realistic clinical trial synthetic data including study definitions, sites, subjects, visits, adverse events, efficacy assessments, and disposition. Use when user requests: clinical trial data, CDISC/SDTM/ADaM datasets, trial scenarios (Phase I/II/III/IV), FDA submission test data, or specific therapeutic areas like oncology or biologics/CGT."
---

# TrialSim

**Status**: In Development

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

## Quick Links

| Topic | Skill | Description |
|-------|-------|-------------|
| Domain Knowledge | [clinical-trials-domain.md](clinical-trials-domain.md) | Core trial concepts, phases, regulatory |
| Recruitment | [recruitment-enrollment.md](recruitment-enrollment.md) | Screening funnel, enrollment patterns |
| Phase 3 Trials | [phase3-pivotal.md](phase3-pivotal.md) | Pivotal registration trials |
| Oncology | [therapeutic-areas/oncology-trials.md](therapeutic-areas/oncology-trials.md) | Oncology-specific patterns |

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

### Therapeutic Area Skills

| Area | PatientSim Skill | TrialSim Skill |
|------|------------------|----------------|
| Oncology | `oncology/*.md` | `therapeutic-areas/oncology.md` |
| Cardiovascular | `heart-failure.md` | `therapeutic-areas/cardiovascular.md` |
| CNS/Neurology | `behavioral-health.md` | `therapeutic-areas/cns.md` |

## Development Status

| Component | Status |
|-----------|--------|
| SKILL.md (this file) | ✅ Complete |
| clinical-trials-domain.md | 🔄 In Progress |
| recruitment-enrollment.md | 📋 Planned |
| phase3-pivotal.md | 🔄 In Progress |
| formats/cdisc-sdtm.md | 📋 Planned |
| formats/cdisc-adam.md | 📋 Planned |

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data
- [MemberSim](../membersim/SKILL.md) - Claims integration
- [Code Systems](../../references/code-systems.md) - Standard terminologies
