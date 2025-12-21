# TrialSim Examples

Generate synthetic clinical trial data for testing CDISC-compliant systems, regulatory submission pipelines, and clinical data management tools.

> **TrialSim generates synthetic clinical trial data only.** This is test data for software development, not actual clinical research data. The trial designs, adverse event patterns, and efficacy results are simulated for realistic software testing scenarios.

---

## Quick Start Examples

### Example 1: Generate a Simple Phase III Trial

```
Generate a Phase III oncology trial with 200 subjects
```

This creates:
- Study design with treatment arms
- 200 randomized subjects with demographics
- Baseline characteristics
- Randomization to treatment arms

### Example 2: Generate Adverse Events

```
Generate adverse events for a Phase III immunotherapy trial with 150 subjects
```

This creates:
- Treatment-emergent adverse events (TEAEs)
- Serious adverse events (SAEs)
- Immune-related adverse events (irAEs)
- MedDRA-coded terms with severity grades

### Example 3: Generate Screen Failures

```
Generate screening data with 30% screen failure rate for 100 randomized subjects
```

This creates:
- Complete screening funnel (identified → randomized)
- Screen failure reasons by category
- Eligibility assessments

---

## Phase-Specific Examples

### Phase I: Dose Escalation

```
Generate a Phase I dose escalation study with 3+3 design, 5 dose levels
```

**What you get:**
- Dose cohorts (3-6 subjects per level)
- Dose-limiting toxicity (DLT) events
- Maximum tolerated dose (MTD) determination
- PK sampling schedule

### Phase II: Proof of Concept

```
Generate a Phase II proof-of-concept trial with 80 subjects, 2:1 randomization
```

**What you get:**
- Randomized subjects (53 treatment, 27 control)
- Preliminary efficacy signals
- Safety profile
- Dose-response data

### Phase III: Pivotal Trial

```
Generate a Phase III pivotal trial for first-line metastatic NSCLC with 500 subjects
```

**What you get:**
- Large randomized population
- Multiple sites (20-50+)
- Primary and secondary endpoints
- Complete safety database
- Regulatory-ready data structure


---

## Therapeutic Area Examples

### Oncology

```
Generate an oncology trial for Stage IV melanoma with RECIST assessments
```

**What you get:**
- Tumor measurements per RECIST 1.1
- Best overall response (CR, PR, SD, PD)
- Progression-free survival data
- Overall survival data
- Tumor response kinetics

### Cardiovascular

```
Generate a cardiovascular outcomes trial with MACE endpoint
```

**What you get:**
- Major Adverse Cardiovascular Events (MACE)
- Component events (CV death, MI, stroke)
- Time-to-event data
- Heart failure hospitalizations
- Cardiac biomarkers (troponin, BNP)

### CNS/Neurology

```
Generate a Phase III Alzheimer's disease trial with cognitive endpoints
```

**What you get:**
- ADAS-Cog scores over time
- MMSE assessments
- CDR-SB ratings
- MRI volumetric data
- Amyloid PET results

### Cell & Gene Therapy

```
Generate a CAR-T cell therapy trial with long-term follow-up
```

**What you get:**
- Single-dose administration
- Cytokine release syndrome (CRS) events
- Neurotoxicity (ICANS) assessments
- Complete response rates
- Duration of response
- 5-year follow-up visits

---

## Safety Data Examples

### Basic Adverse Events

```
Generate adverse events for 100 subjects with typical chemotherapy toxicities
```

**Output includes:**
- MedDRA-coded preferred terms
- CTCAE severity grades (1-5)
- Seriousness criteria
- Causality assessment
- Outcome (resolved, ongoing, fatal)
- Action taken (dose modification, discontinuation)

### Immune-Related Adverse Events

```
Generate immune-related adverse events for a checkpoint inhibitor trial
```

**Output includes:**
- Thyroid disorders (hypo/hyperthyroidism)
- Colitis
- Pneumonitis
- Hepatitis
- Skin reactions
- Rare irAEs (myocarditis, nephritis)

---

## Efficacy Data Examples

### Tumor Response (Oncology)

```
Generate RECIST 1.1 tumor assessments for 50 subjects with responses
```

**Output includes:**
- Target lesion measurements
- Non-target lesion assessments
- New lesion detection
- Overall response per visit
- Best overall response
- Confirmation of response

### Survival Data

```
Generate overall survival data for a 400-subject trial with median OS of 18 months
```

**Output includes:**
- Time-to-event for each subject
- Censoring status
- Death dates where applicable
- Kaplan-Meier survival estimates
- Hazard ratio calculations


---

## Enrollment & Recruitment Examples

### Screening Funnel

```
Generate a complete screening funnel for 200 randomized subjects
```

**Output includes:**
- Identified candidates
- Pre-screened subjects
- Consented subjects
- Screen passed/failed
- Randomized subjects
- Conversion rates at each stage

### Screen Failures

```
Generate 50 screen failures for an oncology trial with detailed reasons
```

**Output includes:**
- Failure reasons by category
- I/E criterion that failed
- Actual vs. required values
- Screening assessments performed

---

## Format Examples

### Export to SDTM

```
Generate a Phase III trial and export as SDTM datasets
```

**Output includes:**
- DM (Demographics)
- AE (Adverse Events)
- CM (Concomitant Medications)
- DS (Disposition)
- EX (Exposure)
- LB (Laboratory)
- MH (Medical History)
- SV (Subject Visits)
- VS (Vital Signs)

### Export to ADaM

```
Generate analysis datasets for a survival trial
```

**Output includes:**
- ADSL (Subject-Level)
- ADAE (Adverse Event Analysis)
- ADTTE (Time-to-Event Analysis)
- ADLB (Laboratory Analysis)

---

## Quick Reference

### Trial Generation Requests

| Request | What You Get |
|---------|--------------|
| "Phase III trial" | Large randomized study with full data |
| "oncology trial" | Cancer-specific with RECIST, survival |
| "200 subjects" | Specified enrollment size |
| "with screen failures" | Include screening funnel |
| "with adverse events" | Safety data generation |
| "as SDTM" | FDA submission format |

### Common Parameters

| Parameter | Example Values |
|-----------|----------------|
| Phase | "Phase I", "Phase II", "Phase III", "Phase IV" |
| Indication | "NSCLC", "breast cancer", "heart failure", "Alzheimer's" |
| Size | "100 subjects", "500 subjects" |
| Randomization | "1:1", "2:1", "3:2:1" |
| Control | "placebo", "standard of care", "active comparator" |
| Endpoint | "OS", "PFS", "ORR", "MACE" |

### Therapeutic Area Triggers

| Say This | Get This |
|----------|----------|
| "oncology", "cancer", "tumor" | RECIST, tumor response, survival |
| "cardiovascular", "heart", "MACE" | CV outcomes, cardiac biomarkers |
| "CNS", "neuro", "Alzheimer's" | Cognitive scales, imaging |
| "gene therapy", "CAR-T", "CGT" | Long-term follow-up, gene expression |

---

## Tips for Best Results

1. **Be specific about indication** - "Stage IV NSCLC" generates better data than just "cancer"

2. **Specify key design elements** - Randomization ratio, control arm, primary endpoint

3. **Request in stages** - Generate study design first, then subjects, then safety/efficacy

4. **Use therapeutic area context** - Oncology trials get RECIST; CV trials get MACE

5. **Ask for specific formats** - "as SDTM" or "as ADaM" for regulatory-ready output

---

## See Also

- [Clinical Trials Domain](../../skills/trialsim/clinical-trials-domain.md) - Core concepts
- [Phase III Pivotal](../../skills/trialsim/phase3-pivotal.md) - Detailed Phase III patterns
- [Recruitment & Enrollment](../../skills/trialsim/recruitment-enrollment.md) - Screening funnels
