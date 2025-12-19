---
name: clinical-trials-domain
description: "Core domain knowledge for clinical trial data generation including trial phases, CDISC standards, regulatory requirements, safety/efficacy patterns, and cross-product integration. Referenced by all TrialSim scenario skills."
---

# Clinical Trials Domain Knowledge

This skill provides foundational domain knowledge for clinical trial synthetic data generation.

## Trial Phases

| Phase | Purpose | Typical Size | Duration |
|-------|---------|--------------|----------|
| Phase 1 | Safety, dosing | 20-100 | 6-12 months |
| Phase 2 | Efficacy signal, dose optimization | 100-500 | 1-2 years |
| Phase 3 | Confirmatory efficacy, safety | 300-3000+ | 2-4 years |
| Phase 4 | Post-marketing surveillance | 1000+ | Ongoing |

## CDISC Standards Overview

### SDTM (Study Data Tabulation Model)
Standard format for submitting clinical trial data to FDA/regulatory agencies.

Key domains:
- **DM** - Demographics
- **AE** - Adverse Events
- **CM** - Concomitant Medications
- **EX** - Exposure
- **LB** - Laboratory Results
- **VS** - Vital Signs
- **DS** - Disposition
- **MH** - Medical History
- **EG** - ECG Results
- **PE** - Physical Examination

### ADaM (Analysis Data Model)
Analysis-ready datasets derived from SDTM.

Key datasets:
- **ADSL** - Subject-Level Analysis Dataset
- **ADAE** - Adverse Event Analysis Dataset
- **ADLB** - Laboratory Analysis Dataset
- **ADEFF** - Efficacy Analysis Dataset
- **ADTTE** - Time-to-Event Analysis Dataset

## Regulatory Considerations

### ICH-GCP Compliance
- Informed consent documentation
- Protocol deviation tracking
- Source data verification
- Audit trail requirements

### Safety Reporting
- SAE (Serious Adverse Event) timelines
- SUSAR (Suspected Unexpected Serious Adverse Reaction)
- DSMB (Data Safety Monitoring Board) reviews

## Cross-Product Integration

### PatientSim → TrialSim
When converting a PatientSim patient to a TrialSim subject:
- Add informed consent record
- Add screening assessments
- Add randomization assignment
- Map diagnoses to inclusion/exclusion criteria
- Convert encounters to study visits

### NetworkSim → TrialSim
When using NetworkSim provider as investigator:
- Add medical license verification
- Add GCP training certification
- Add site delegation log entries
- Add financial disclosure

## See Also

- [Phase 3 Pivotal Trials](phase3-pivotal.md)
- [Recruitment & Enrollment](recruitment-enrollment.md)
- [SDTM Format](../../formats/cdisc-sdtm.md)
- [ADaM Format](../../formats/cdisc-adam.md)
