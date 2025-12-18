---
name: phase3-pivotal-trial
description: "Generate Phase III pivotal trial data with realistic multi-site enrollment, randomization, visit schedules, safety monitoring, and efficacy endpoints. Use for: Phase 3 trials, pivotal studies, registration trials, NDA/BLA submission data."
---

# Phase III Pivotal Trial Scenario

## Overview

Generate realistic Phase III pivotal trial data suitable for:
- FDA submission package testing (NDA/BLA)
- Clinical data management system validation
- SDTM/ADaM transformation testing
- Statistical analysis workflow development
- EDC system testing

Phase III trials are confirmatory studies designed to demonstrate efficacy and safety in a broad patient population to support regulatory approval.

## Trigger Phrases

Activate this scenario when user mentions:
- "Phase III trial" or "Phase 3 trial"
- "pivotal trial" or "pivotal study"
- "registration trial"
- "confirmatory trial"
- "NDA" or "BLA" submission data
- "multi-center trial"
- "randomized controlled trial" (large scale)

## Phase III Characteristics

| Characteristic | Typical Range | Default |
|----------------|---------------|---------|
| Subject Count | 300-3000+ | 450 |
| Site Count | 50-200 | 75 |
| Countries | 10-30 | 15 |
| Treatment Arms | 2-3 | 2 (active + placebo) |
| Randomization Ratio | 1:1, 2:1, 3:1 | 2:1 |
| Study Duration | 2-4 years | 30 months |
| Treatment Duration | 6-24 months | 12 months |
| Follow-up | 0-24 months | 6 months |
| Blinding | Double-blind | Double-blind |

## Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| study_id | string | auto | Study identifier (e.g., "ABC-123-301") |
| therapeutic_area | string | "oncology" | Disease area |
| indication | string | "NSCLC" | Specific indication |
| subject_count | int | 450 | Total subjects to generate |
| site_count | int | 75 | Number of investigator sites |
| treatment_arms | list | 2 arms | Arm definitions |
| randomization_ratio | string | "2:1" | Allocation ratio |
| visit_schedule | list | 8 visits | Visit definitions |
| primary_endpoint | string | "PFS" | Primary efficacy measure |
| ae_rate | float | 0.65 | Proportion with any AE |
| sae_rate | float | 0.08 | SAE proportion |
| discontinuation_rate | float | 0.15 | Early termination rate |
| seed | int | random | Reproducibility seed |

## Default Visit Schedule

| Visit | Name | Window | Key Assessments |
|-------|------|--------|-----------------|
| 1 | Screening | Day -28 to -1 | Consent, I/E, Labs, Imaging |
| 2 | Baseline/Randomization | Day 1 | Randomization, First Dose |
| 3 | Week 4 | Day 28 +/- 7 | Safety, Labs |
| 4 | Week 8 | Day 56 +/- 7 | Safety, Labs, Efficacy |
| 5 | Week 12 | Day 84 +/- 7 | Safety, Labs, Imaging |
| 6 | Week 24 | Day 168 +/- 14 | Safety, Labs, Efficacy, Imaging |
| 7 | Week 48 | Day 336 +/- 14 | Safety, Labs, Efficacy, Imaging |
| 8 | End of Treatment | Variable | Final safety, Labs |
| 9 | Follow-up | 30 days post-EOT | Safety follow-up |

## Site Distribution Pattern

### By Region (Default: Global Trial)

| Region | Sites | Subjects | Countries |
|--------|-------|----------|-----------|
| North America | 25 | 35% | USA, Canada |
| Western Europe | 20 | 25% | UK, Germany, France, Spain |
| Eastern Europe | 15 | 20% | Poland, Romania, Czech |
| Asia-Pacific | 10 | 15% | Japan, Korea, Taiwan |
| Rest of World | 5 | 5% | Brazil, Australia |

### Site Enrollment Patterns

```
High-enrolling sites (10%):    15-25 subjects each
Average sites (60%):           5-15 subjects each
Low-enrolling sites (30%):     1-5 subjects each
```

## Safety Monitoring Patterns

### Adverse Event Distribution

| Category | Rate | Details |
|----------|------|---------|
| Any AE | 65% | At least one AE |
| Drug-related AE | 45% | Possibly, probably, or definitely related |
| Grade 3+ AE | 20% | Severe or life-threatening |
| SAE | 8% | Serious adverse events |
| Fatal AE | 1-2% | Death (varies by indication) |
| AE leading to discontinuation | 5% | Stopped treatment due to AE |

### Common AE Pattern (Oncology Example)

| Adverse Event | Active Arm | Placebo Arm |
|---------------|------------|-------------|
| Fatigue | 45% | 25% |
| Nausea | 35% | 15% |
| Diarrhea | 30% | 10% |
| Decreased appetite | 25% | 12% |
| Rash | 20% | 5% |
| Peripheral neuropathy | 15% | 3% |

### SAE Categories

| Type | Rate | Typical Events |
|------|------|----------------|
| Disease-related | 3% | Progression, complications |
| Treatment-related | 2% | Neutropenia, hepatotoxicity |
| Other medical | 2% | Infections, falls |
| Procedure-related | 1% | Biopsy complications |

## Efficacy Endpoint Patterns

### Time-to-Event Endpoints

For survival/PFS endpoints:

| Arm | Median (months) | HR | p-value |
|-----|-----------------|----|---------|
| Active | 12.5 | 0.65 | <0.001 |
| Control | 7.8 | ref | - |

### Response Endpoints (Oncology)

| Response | Active Arm | Control Arm |
|----------|------------|-------------|
| CR | 8% | 2% |
| PR | 32% | 15% |
| SD | 35% | 40% |
| PD | 20% | 38% |
| NE | 5% | 5% |

**ORR (CR+PR):** Active 40% vs Control 17%

## Discontinuation Patterns

| Reason | Rate | Timing Pattern |
|--------|------|----------------|
| Completed | 70% | Full treatment + follow-up |
| Disease Progression | 12% | Ongoing, peaks mid-study |
| Adverse Event | 5% | Early + ongoing |
| Withdrawal by Subject | 4% | Early (first 8 weeks) |
| Death | 3% | Throughout |
| Protocol Deviation | 2% | Variable |
| Lost to Follow-up | 2% | Late study |
| Other | 2% | Variable |

## Output Example

### Canonical JSON (Abbreviated)

```json
{
  "study": {
    "study_id": "ABC-123-301",
    "sponsor": "PharmaCorp Inc",
    "title": "A Phase III, Randomized, Double-Blind, Placebo-Controlled Study of Drug X in Patients with Advanced NSCLC",
    "phase": "III",
    "therapeutic_area": "Oncology",
    "indication": "Advanced Non-Small Cell Lung Cancer",
    "design": "Randomized, Double-Blind, Placebo-Controlled",
    "planned_enrollment": 450,
    "actual_enrollment": 452,
    "randomization_ratio": "2:1",
    "treatment_arms": [
      {
        "arm_code": "A",
        "arm_name": "Drug X 200mg BID",
        "arm_type": "EXPERIMENTAL"
      },
      {
        "arm_code": "B",
        "arm_name": "Placebo BID",
        "arm_type": "PLACEBO_COMPARATOR"
      }
    ],
    "primary_endpoint": "Progression-Free Survival",
    "study_start_date": "2024-01-15",
    "primary_completion_date": "2026-06-30"
  },
  "sites": [
    {
      "site_id": "001",
      "site_name": "University Oncology Center",
      "country": "USA",
      "city": "Boston",
      "investigator": "Dr. Sarah Johnson",
      "target_enrollment": 20,
      "actual_enrollment": 18
    }
  ],
  "subjects": [
    {
      "subject_id": "ABC-123-301-001-001",
      "site_id": "001",
      "demographics": {
        "age": 62,
        "sex": "F",
        "race": "WHITE"
      },
      "consent_date": "2024-03-15",
      "randomization_date": "2024-03-22",
      "treatment_arm": "A",
      "disposition": "COMPLETED"
    }
  ],
  "visits": [
    {
      "subject_id": "ABC-123-301-001-001",
      "visit_name": "Week 4",
      "visit_date": "2024-04-19",
      "visit_status": "COMPLETED"
    }
  ],
  "adverse_events": [
    {
      "subject_id": "ABC-123-301-001-001",
      "ae_term": "Fatigue",
      "severity": "MILD",
      "serious": false,
      "causality": "PROBABLY RELATED",
      "start_date": "2024-04-01",
      "outcome": "RECOVERED/RESOLVED"
    }
  ],
  "efficacy": {
    "primary_analysis": {
      "endpoint": "PFS",
      "active_median_months": 12.5,
      "control_median_months": 7.8,
      "hazard_ratio": 0.65,
      "p_value": 0.0001
    }
  }
}
```

## SDTM Output Mapping

| Canonical Entity | SDTM Domain(s) |
|------------------|----------------|
| Study | TS, TA, TE, TV |
| Site | Custom (not standard SDTM) |
| Subject | DM |
| Visit | SV |
| Adverse Event | AE |
| Concomitant Med | CM |
| Medical History | MH |
| Vital Signs | VS |
| Labs | LB |
| Efficacy | TR, RS (tumor) or custom |
| Disposition | DS |
| Exposure | EX |

## Generation Examples

### Example 1: Small Phase III Trial

**Request:** "Generate a Phase III trial with 50 subjects across 5 sites"

Claude will generate:
- Study definition with 50 planned subjects
- 5 sites (1-2 high enrollers, 3-4 average)
- 50 subjects with full demographics
- Visits per schedule (8+ per subject = 400+ visit records)
- ~30 subjects with at least one AE
- ~4 subjects with SAEs
- ~7-8 early discontinuations

### Example 2: Oncology Trial with SDTM Output

**Request:** "Generate a Phase III NSCLC trial with 10 subjects, output as SDTM DM and AE"

Claude will:
1. Generate canonical trial data
2. Transform subjects to DM domain variables
3. Transform adverse events to AE domain variables
4. Output SDTM-formatted CSV content

### Example 3: Safety Database for Specific Signal

**Request:** "Generate Phase III trial data with high rate of hepatotoxicity events"

Claude will:
- Increase liver-related AE frequency (25% vs typical 5%)
- Include ALT/AST elevations in lab data
- Add Hy's Law cases (2-3 subjects)
- Appropriate discontinuation for hepatotoxicity

## Validation Rules

TrialSim validates Phase III data for:

1. **Enrollment Logic**
   - Consent before randomization
   - Screening within window
   - Site enrollment within capacity

2. **Visit Compliance**
   - Visits within protocol windows
   - Required assessments present
   - Proper sequence (no Week 8 before Week 4)

3. **Safety Data**
   - AE dates within treatment period
   - SAE criteria properly applied
   - Causality consistent with timing

4. **Efficacy Data**
   - Assessment dates match visit schedule
   - Response criteria properly derived
   - Progression documented correctly

5. **Disposition**
   - End date after all other dates
   - Reason consistent with data (e.g., AE if discontinued for AE)
   - Death date matches fatal AE date

## Related Skills

- [../domain/clinical-trials-domain.md](../domain/clinical-trials-domain.md) - Core domain knowledge
- [../domain/recruitment-enrollment.md](../domain/recruitment-enrollment.md) - Screening patterns
- [../../formats/dimensional-analytics.md](../../formats/dimensional-analytics.md) - Analytics output
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10, MedDRA codes
