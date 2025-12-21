---
name: rwe-overview
description: |
  Foundational concepts for Real World Evidence generation including data sources, 
  regulatory context, and study design considerations. Triggers: "RWE", 
  "real world evidence", "real world data", "RWD", "observational".
---

# Real World Evidence Overview

Foundational knowledge for generating real world evidence (RWE) from synthetic real world data (RWD).

---

## For Claude

This is a **foundation skill** for RWE generation. Apply this when users request real world evidence, external controls, or observational data.

**Always apply this skill when you see:**
- References to real world evidence or real world data
- External control arm requests
- Observational study designs
- Claims data analysis

---

## Definitions

| Term | Definition |
|------|------------|
| **Real World Data (RWD)** | Data relating to patient health routinely collected outside clinical trials |
| **Real World Evidence (RWE)** | Clinical evidence derived from analysis of RWD |

## RWD Sources

| Source | Data Type | HealthSim Product |
|--------|-----------|-------------------|
| Electronic Health Records | Clinical notes, labs, diagnoses | PatientSim |
| Claims/Billing | Encounters, procedures, costs | MemberSim |
| Pharmacy | Prescriptions, fills, adherence | RxMemberSim |

---

## Regulatory Context

### FDA RWE Program Framework (2018)

1. Determine if RWD is fit for regulatory purpose
2. Assess if study design can provide adequate evidence
3. Evaluate regulatory conclusion from RWE

### Accepted Use Cases

| Use Case | Regulatory Acceptance |
|----------|----------------------|
| **External control arms** | Growing, especially rare disease |
| **Label expansion** | Case-by-case |
| **Post-marketing commitments** | Common |
| **Rare disease programs** | High acceptance |

---

## RWE Study Designs

| Design | Description | Use Case |
|--------|-------------|----------|
| **Cohort** | Follow exposed/unexposed groups | Comparative effectiveness |
| **Case-control** | Compare cases vs controls | Rare outcomes |
| **External control** | Trial vs external comparator | Single-arm trials |
| **Hybrid** | Randomized + external | Augments trial power |

---

## Data Quality Considerations

| Dimension | Definition |
|-----------|------------|
| **Relevance** | Does data answer the question? |
| **Reliability** | Is data accurate and complete? |
| **Accrual** | How/when was data collected? |
| **Linkage** | Can data sources be combined? |

---

## Related Skills

- [Synthetic Control](synthetic-control.md) - Generate external control arms
- [Clinical Trials Domain](../clinical-trials-domain.md) - Trial design concepts

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial RWE overview skill |
