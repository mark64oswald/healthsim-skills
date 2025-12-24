---
name: healthsim-trialsim
description: "Generate realistic clinical trial synthetic data including study definitions, sites, subjects, visits, adverse events, efficacy assessments, and disposition. Use when user requests: clinical trial data, CDISC/SDTM/ADaM datasets, trial scenarios (Phase I/II/III/IV), FDA submission test data, or specific therapeutic areas like oncology or biologics/CGT."
---

# TrialSim

**Status**: Active Development

TrialSim generates realistic synthetic clinical trial data for testing, training, and development purposes.

## For Claude

Use this skill when the user requests clinical trial data, CDISC-compliant datasets, or regulatory submission test data. This is the primary skill for generating realistic synthetic clinical trial data.

**When to apply this skill:**

- User mentions clinical trials, studies, or protocols
- User requests CDISC, SDTM, or ADaM datasets
- User specifies trial phases (Phase I, II, III, IV)
- User mentions FDA/EMA submission data or regulatory requirements
- User asks for adverse events, safety data, or efficacy endpoints
- User mentions specific therapeutic areas (oncology, cardiovascular, CNS)
- User requests SDTM domains (DM, AE, VS, LB, CM, EX, DS, MH)

**Key capabilities:**

- Generate complete study definitions with protocol parameters
- Create multi-site, multi-country trial configurations
- Produce subject-level longitudinal data with realistic patterns
- Generate safety data (adverse events, labs, vitals) with MedDRA/LOINC coding
- Create efficacy endpoints for various therapeutic areas
- Output CDISC-compliant formats (SDTM, ADaM)

For specific trial phases, therapeutic areas, or SDTM domains, load the appropriate skill from the tables below.

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

### Trial Phase Skills

| Phase | Skill | Description |
|-------|-------|-------------|
| Phase 1 | [phase1-dose-escalation.md](phase1-dose-escalation.md) | FIH, dose escalation, MTD (3+3, BOIN, CRM) |
| Phase 2 | [phase2-proof-of-concept.md](phase2-proof-of-concept.md) | POC, dose-ranging, futility (Simon's, MCP-Mod) |
| Phase 3 | [phase3-pivotal.md](phase3-pivotal.md) | Pivotal registration trials, NDA/BLA |

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
| Dimensional | [../../formats/dimensional-analytics.md](../../formats/dimensional-analytics.md) | BI dashboards, analytics |
| JSON | Default | API integration |
| CSV | [../../formats/csv.md](../../formats/csv.md) | Spreadsheet analysis |

## Data Models & References

| Resource | Location | Description |
|----------|----------|-------------|
| Canonical Models | [../../references/data-models.md#trialsim-models](../../references/data-models.md#trialsim-models) | 15 entity schemas (Subject, Study, Site, AE, etc.) |
| Dimensional Schema | [../../formats/dimensional-analytics.md#trialsim-clinical-trial-analytics](../../formats/dimensional-analytics.md#trialsim-clinical-trial-analytics) | Star schema for BI (7 dims, 6 facts) |
| Code Systems | [../../references/code-systems.md](../../references/code-systems.md) | MedDRA, LOINC, ATC |

## Core Entities

TrialSim uses 15 canonical entity schemas. See [Data Models Reference](../../references/data-models.md#trialsim-models) for complete JSON schemas.

### Entity Overview

| Entity | SDTM Domain | Description |
|--------|-------------|-------------|
| Subject | DM | Trial participant (extends Person) |
| Study | TS | Protocol definition |
| Site | - | Investigational site |
| TreatmentArm | TA | Study arm definition |
| VisitSchedule | TV | Protocol visits |
| ActualVisit | SV | Subject visit occurrence |
| Randomization | DM/SE | Subject randomization |
| AdverseEvent | AE | Safety events with MedDRA |
| Exposure | EX | Study drug dosing |
| ConcomitantMed | CM | Prior/concomitant meds with ATC |
| TrialLab | LB | Lab results with LOINC |
| EfficacyAssessment | RS/TR | Response assessments |
| MedicalHistory | MH | Pre-existing conditions |
| DispositionEvent | DS | Subject disposition |
| ProtocolDeviation | DV | Protocol deviations |

### Key Entity Examples

**Study:**
```json
{
  "study_id": "ABC-123-001",
  "protocol_title": "A Phase 3, Randomized, Double-Blind Study...",
  "phase": "Phase 3",
  "therapeutic_area": "Oncology",
  "indication": "Non-Small Cell Lung Cancer",
  "sponsor": "Example Pharma Inc.",
  "status": "Ongoing"
}
```

**Subject (with cross-product linking):**
```json
{
  "subject_id": "0001",
  "usubjid": "ABC-123-001-001-0001",
  "site_id": "001",
  "patient_ref": "MRN-12345",
  "screening_date": "2024-01-15",
  "randomization_date": "2024-01-22",
  "treatment_arm": "TRT",
  "status": "Active"
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

### Cross-Product: PopulationSim (Demographics & SDOH) - v2.0 Data Integration

PopulationSim v2.0 provides **embedded real-world data** for evidence-based trial planning, site selection, and diversity compliance. When geographies are specified, TrialSim uses actual CDC PLACES, SVI, and ADI data to ground feasibility estimates and enrollment projections.

#### Data-Driven Trial Planning Pattern

**Step 1: Look up real population data for potential sites**
```
# For site feasibility in Houston metro (Harris County, FIPS: 48201)
Read from: skills/populationsim/data/county/places_county_2024.csv
→ DIABETES_CrudePrev: 12.1% (for diabetes trial)
→ CHD_CrudePrev: 6.4% (for CV outcomes trial)
→ CANCER_CrudePrev: 6.2% (for oncology trial)
→ TotalPopulation: 4,731,145

Read from: skills/populationsim/data/county/svi_county_2022.csv
→ RPL_THEMES: 0.68 (moderate-high vulnerability)
→ EP_MINRTY: 72.1% (supports diversity requirements)
```

**Step 2: Apply to site feasibility estimation**
```json
{
  "site_feasibility": {
    "county_fips": "48201",
    "county_name": "Harris County, TX",
    "indication": "Type 2 Diabetes",
    "eligible_population": {
      "total_population": 4731145,
      "disease_prevalence": 0.121,
      "prevalent_patients": 572467,
      "age_eligible_18_75": 458974,
      "funnel_to_screenable": 0.05,
      "annual_screenable": 22949
    },
    "diversity_metrics": {
      "minority_percentage": 0.721,
      "meets_fda_diversity_guidance": true
    },
    "data_provenance": {
      "source": "CDC_PLACES_2024",
      "data_year": 2022
    }
  }
}
```

**Step 3: Generate realistic enrollment projections**
- Site catchment based on real prevalence (not national averages)
- Diversity enrollment reflecting actual demographics
- Screening-to-randomization rates adjusted for SVI (access barriers)

#### Embedded Data Sources for Trial Planning

| Source | File | Use in TrialSim |
|--------|------|-----------------|
| CDC PLACES County | `populationsim/data/county/places_county_2024.csv` | Disease prevalence for feasibility |
| CDC PLACES Tract | `populationsim/data/tract/places_tract_2024.csv` | Catchment area analysis |
| SVI County | `populationsim/data/county/svi_county_2022.csv` | Diversity planning, access barriers |
| SVI Tract | `populationsim/data/tract/svi_tract_2022.csv` | Site-level vulnerability context |
| Geography Crosswalk | `populationsim/data/crosswalks/cbsa_definitions.csv` | Metro area site clustering |

#### Trial-Specific Applications

| Application | Data Used | TrialSim Integration |
|-------------|-----------|---------------------|
| **Site Feasibility** | PLACES disease prevalence + population | Eligible patient pool sizing |
| **Diversity Planning** | SVI EP_MINRTY, demographics | FDA diversity guidance compliance |
| **Enrollment Projection** | PLACES + SVI access indicators | Screening/randomization rates |
| **Site Selection** | Multi-county PLACES comparison | Optimal site network design |
| **Catchment Analysis** | Tract-level PLACES | Drive-time eligible population |

#### Example: Data-Grounded Phase III Site Selection

**Request:** "Identify top 5 US counties for a Phase III NASH trial based on patient availability"

**Data Lookup Process:**
```
Query places_county_2024.csv for:
  - High OBESITY_CrudePrev (NASH proxy)
  - High DIABETES_CrudePrev (comorbidity)
  - Large TotalPopulation (volume)

Query svi_county_2022.csv for:
  - EP_MINRTY (diversity potential)
  - EP_UNINSUR (access consideration)
```

**Output with Provenance:**
```json
{
  "recommended_sites": [
    {
      "rank": 1,
      "county_fips": "48201",
      "name": "Harris County, TX",
      "obesity_prevalence": 0.328,
      "diabetes_prevalence": 0.121,
      "population": 4731145,
      "minority_pct": 0.721,
      "estimated_eligible": 45000,
      "diversity_score": "excellent"
    }
  ],
  "data_provenance": {
    "sources": ["CDC_PLACES_2024", "CDC_SVI_2022"],
    "methodology": "prevalence_weighted_ranking"
  }
}
```

#### Integration with Trial-Support Skills

| PopulationSim Skill | TrialSim Application | Data Source |
|---------------------|---------------------|-------------|
| [data-lookup.md](../populationsim/data-access/data-lookup.md) | Exact prevalence for feasibility | CDC PLACES 2024 |
| [county-profile.md](../populationsim/geographic/county-profile.md) | Site catchment demographics | PLACES + SVI |
| [svi-analysis.md](../populationsim/sdoh/svi-analysis.md) | Diversity and access analysis | CDC SVI 2022 |
| [feasibility-estimation.md](../populationsim/trial-support/feasibility-estimation.md) | Protocol feasibility funnel | All sources |
| [diversity-planning.md](../populationsim/trial-support/diversity-planning.md) | FDA diversity compliance | SVI demographics |

> **Key Principle:** When planning trials, always ground feasibility and diversity estimates in real PopulationSim data. This enables evidence-based site selection and realistic enrollment projections.

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
| phase1-dose-escalation.md | ✅ Complete |
| phase2-proof-of-concept.md | ✅ Complete |

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data
- [MemberSim](../membersim/SKILL.md) - Claims integration
- [Code Systems](../../references/code-systems.md) - Standard terminologies

## Output Formats

TrialSim supports multiple output formats:

| Format | Use Case | Skill Reference |
|--------|----------|-----------------|
| **Canonical JSON** | Internal processing, API integration | [data-models.md](../../references/data-models.md#trialsim-models) |
| **CDISC SDTM** | Regulatory submission, FDA/EMA | [cdisc-sdtm.md](../../formats/cdisc-sdtm.md) |
| **CDISC ADaM** | Analysis datasets, statistical programming | [cdisc-adam.md](../../formats/cdisc-adam.md) |
| **Dimensional (Star Schema)** | Analytics, BI dashboards, DuckDB/Databricks | [dimensional-analytics.md](../../formats/dimensional-analytics.md#trialsim-clinical-trial-analytics) |

### Dimensional Analytics

For trial operations analytics and BI dashboards, request dimensional output:

```
Generate Phase III trial with 100 subjects as star schema for DuckDB
```

This produces:
- **Dimensions**: dim_study, dim_site, dim_subject, dim_treatment_arm, dim_visit_schedule, dim_meddra, dim_lab_test
- **Facts**: fact_enrollment, fact_visit, fact_adverse_event, fact_exposure, fact_efficacy, fact_lab_result

See [dimensional-analytics.md](../../formats/dimensional-analytics.md#trialsim-clinical-trial-analytics) for full DDL and example queries.

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
