---
name: healthsim-populationsim
description: >
  PopulationSim provides population-level intelligence using public data sources.
  Use this skill for ANY request involving: (1) population demographics or profiles,
  (2) geographic health patterns or disparities, (3) social determinants of health (SDOH),
  (4) SVI or ADI analysis, (5) cohort definition or specification, (6) clinical trial
  feasibility, site selection, or enrollment projection, (7) service area analysis,
  (8) health equity assessment, (9) census data or ACS variables, (10) CDC PLACES health indicators.
---

# PopulationSim - Population Intelligence & Cohort Generation

## Overview

PopulationSim provides population-level intelligence using public data sources (Census ACS, CDC PLACES, Social Vulnerability Index, Area Deprivation Index) to enable:

1. **Standalone Analysis**: Geographic profiling, health disparities analysis, population comparisons
2. **Cross-Product Integration**: Cohort specifications that drive realistic data generation in PatientSim, MemberSim, RxMemberSim, and TrialSim

**Key Differentiator**: Unlike other HealthSim products that generate synthetic records, PopulationSim analyzes real population characteristics and creates specifications for generation.

## Quick Reference

| I want to... | Use This Skill | Key Triggers |
|--------------|----------------|--------------|
| **Data Access (v2.0)** | | |
| Look up exact data values | `data-access/data-lookup.md` | "what is the exact", "look up", "from PLACES" |
| Resolve FIPS codes | `data-access/geography-lookup.md` | "FIPS for", "which county is", "list counties in MSA" |
| Aggregate geographic data | `data-access/data-aggregation.md` | "aggregate tracts", "metro total", "combine counties" |
| **Geographic Intelligence** | | |
| Profile a county or region | `geographic/county-profile.md` | "county profile", "demographics for", "health indicators" |
| Analyze census tracts | `geographic/census-tract-analysis.md` | "tract level", "granular", "hotspots" |
| Profile a metro area | `geographic/metro-area-profile.md` | "metro", "MSA", "metropolitan" |
| Define custom region | `geographic/custom-region-builder.md` | "service area", "combine", "custom region" |
| **Health Patterns** | | |
| Analyze disease prevalence | `health-patterns/chronic-disease-prevalence.md` | "diabetes rate", "prevalence", "CDC PLACES" |
| Analyze health behaviors | `health-patterns/health-behavior-patterns.md` | "smoking rate", "obesity", "physical activity" |
| Assess healthcare access | `health-patterns/healthcare-access-analysis.md` | "uninsured", "provider ratio", "access" |
| Identify health disparities | `health-patterns/health-outcome-disparities.md` | "disparities", "equity", "by race" |
| **SDOH Analysis** | | |
| Analyze SVI | `sdoh/svi-analysis.md` | "SVI", "social vulnerability", "vulnerable" |
| Analyze ADI | `sdoh/adi-analysis.md` | "ADI", "area deprivation", "deprived" |
| Analyze economics | `sdoh/economic-indicators.md` | "poverty", "income", "unemployment" |
| Analyze community factors | `sdoh/community-factors.md` | "housing", "transportation", "food access" |
| **Cohort Definition** | | |
| Define a cohort | `cohorts/cohort-specification.md` | "define cohort", "cohort spec", "population segment" |
| Build demographics | `cohorts/demographic-distribution.md` | "age distribution", "demographics for cohort" |
| Build clinical profile | `cohorts/clinical-prevalence-profile.md` | "comorbidity rates", "clinical profile" |
| Build SDOH profile | `cohorts/sdoh-profile-builder.md` | "SDOH profile", "Z-code rates" |
| **Trial Support** | | |
| Estimate trial feasibility | `trial-support/feasibility-estimation.md` | "feasibility", "eligible population" |
| Select trial sites | `trial-support/site-selection-support.md` | "site selection", "best locations" |
| Project enrollment | `trial-support/enrollment-projection.md` | "enrollment timeline", "recruitment rate" |

## Trigger Phrases

### Data Access (v2.0)
- "What is the exact [measure] in [geography]?"
- "Look up [measure] from CDC PLACES"
- "What's the FIPS code for [county]?"
- "Which counties are in the [metro] MSA?"
- "Aggregate tract data for [county]"

### Geographic Intelligence
- "What's the population profile for [county/region]?"
- "Show me demographics for [geography]"
- "Compare [region A] to [region B]"
- "Analyze census tracts in [area] with high vulnerability"
- "Profile the [metro area] MSA"

### Health Patterns
- "What's the diabetes prevalence in [geography]?"
- "Show health disparities by race in [region]"
- "Compare chronic disease rates across [geographies]"
- "What are the smoking rates in [county]?"
- "Which counties have the highest obesity?"

### SDOH Analysis
- "What's the SVI for [geography]?"
- "Show me high-deprivation areas in [state]"
- "Analyze social determinants in [region]"
- "Which tracts have transportation barriers?"
- "Find food deserts in [county]"

### Cohort Definition
- "Define a cohort of diabetics in underserved California areas"
- "Create a population specification for high-risk heart failure patients"
- "Build a cohort spec for PatientSim generation"
- "Specify a population segment for claims testing"
- "What are the comorbidity rates for diabetics?"

### Trial Support
- "Estimate feasibility for a T2DM trial"
- "How many patients are eligible for [criteria]?"
- "Rank trial sites for cardiovascular outcomes study"
- "Best locations for diabetes trial enrollment"
- "Project enrollment for 2,000 subjects across 40 sites"

## Output Types

### PopulationProfile

Geographic entity with demographics, health indicators, and SDOH indices:

```json
{
  "geography": {
    "type": "county",
    "fips": "06073",
    "name": "San Diego County",
    "state": "CA",
    "region": "Pacific"
  },
  "demographics": {
    "total_population": 3286069,
    "median_age": 37.1,
    "age_distribution": {
      "0-17": 0.21,
      "18-64": 0.62,
      "65+": 0.17
    },
    "race_ethnicity": {
      "white_nh": 0.43,
      "hispanic": 0.34,
      "asian": 0.12,
      "black": 0.05,
      "other": 0.06
    },
    "median_household_income": 102285,
    "poverty_rate": 0.103
  },
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "diabetes_prevalence": 0.095,
    "obesity_prevalence": 0.280,
    "hypertension_prevalence": 0.285,
    "depression_prevalence": 0.195,
    "smoking_prevalence": 0.098
  },
  "sdoh_indices": {
    "svi_overall": 0.42,
    "svi_themes": {
      "socioeconomic": 0.38,
      "household_composition": 0.45,
      "minority_language": 0.52,
      "housing_transportation": 0.35
    },
    "adi_national_rank": 35
  },
  "healthcare_access": {
    "uninsured_rate": 0.071,
    "pcp_per_100k": 82.4,
    "insurance_mix": {
      "employer": 0.52,
      "medicare": 0.15,
      "medicaid": 0.18,
      "individual": 0.08,
      "uninsured": 0.07
    }
  }
}
```

### CohortSpecification

Generation input for other HealthSim products:

```json
{
  "cohort_id": "houston_diabetics_2024",
  "name": "Houston Metro Diabetic Adults",
  "target_size": 10000,
  "geography": {
    "type": "msa",
    "cbsa_code": "26420",
    "name": "Houston-The Woodlands-Sugar Land, TX"
  },
  "demographics": {
    "age": {
      "min": 18, "max": 85, "mean": 58.4,
      "brackets": { "18-44": 0.18, "45-64": 0.42, "65-74": 0.28, "75+": 0.12 }
    },
    "sex": { "male": 0.48, "female": 0.52 },
    "race_ethnicity": { "white_nh": 0.28, "black": 0.22, "hispanic": 0.38, "asian": 0.08 }
  },
  "clinical_profile": {
    "primary_condition": { "icd10": "E11", "name": "Type 2 Diabetes" },
    "comorbidities": {
      "I10": { "name": "Hypertension", "rate": 0.71 },
      "E78": { "name": "Hyperlipidemia", "rate": 0.68 },
      "E66": { "name": "Obesity", "rate": 0.62 }
    }
  },
  "sdoh_profile": {
    "poverty_rate": 0.18,
    "uninsured_rate": 0.16,
    "food_insecurity": 0.15,
    "svi_mean": 0.58
  },
  "z_code_rates": {
    "Z59.6": { "name": "Low income", "rate": 0.18 },
    "Z59.41": { "name": "Food insecurity", "rate": 0.15 }
  },
  "insurance_mix": {
    "medicare": 0.38, "medicaid": 0.22, "commercial": 0.32, "uninsured": 0.08
  }
}
```

## Cross-Product Integration

### Integration Flow

```
                    ┌─────────────────────┐
                    │   PopulationSim     │
                    │  CohortSpecification│
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │ PatientSim  │     │ MemberSim   │     │  TrialSim   │
    │ - patients  │     │ - members   │     │ - subjects  │
    │ - diagnoses │     │ - claims    │     │ - diversity │
    │ - SDOH codes│     │ - plans     │     │ - sites     │
    └──────┬──────┘     └──────┬──────┘     └─────────────┘
           │                   │
           └─────────┬─────────┘
                     ▼
              ┌─────────────┐
              │ RxMemberSim │
              │ - Rx claims │
              │ - adherence │
              └─────────────┘
```

### Integration Patterns

| PopulationSim Output | Receiving Product | Result |
|----------------------|-------------------|--------|
| CohortSpecification | PatientSim | Patients matching demographic/clinical profile |
| CohortSpecification | MemberSim | Members with realistic plan/utilization mix |
| CohortSpecification | TrialSim | Diverse trial subjects meeting FDA guidance |
| PopulationProfile | NetworkSim | Service area provider network design |

## Data Sources (Embedded v2.0)

PopulationSim includes an embedded data package (148 MB) with 100% US coverage:

| Source | File | Records | Data Year |
|--------|------|---------|-----------|
| CDC PLACES (County) | `data/county/places_county_2024.csv` | 3,143 | 2022 BRFSS |
| CDC PLACES (Tract) | `data/tract/places_tract_2024.csv` | 83,522 | 2022 BRFSS |
| SVI (County) | `data/county/svi_county_2022.csv` | 3,144 | 2018-2022 ACS |
| SVI (Tract) | `data/tract/svi_tract_2022.csv` | 84,120 | 2018-2022 ACS |
| ADI (Block Group) | `data/block_group/adi_blockgroup_2023.csv` | 242,336 | 2019-2023 ACS |
| Geography Crosswalks | `data/crosswalks/*.csv` | Various | 2023 Census |

### DuckDB Reference Tables

For SQL-based analysis, reference data is also available in the DuckDB database:

| Table | Source | Purpose |
|-------|--------|---------|
| `ref_cdc_places_tract` | CDC PLACES | Tract-level health indicators |
| `ref_cdc_places_county` | CDC PLACES | County-level health indicators |
| `ref_svi_tract` | CDC SVI | Tract-level vulnerability |
| `ref_svi_county` | CDC SVI | County-level vulnerability |
| `ref_adi_blockgroup` | ADI | Block group deprivation |

See [Data Architecture](../../docs/data-architecture.md) for details.

## Directory Structure

```
skills/populationsim/
├── SKILL.md                           # This file - master router
├── README.md                          # Product overview
├── population-intelligence-domain.md  # Core domain knowledge
│
├── data/                              # Embedded Data Package (v2.0)
│   ├── README.md                      # Data dictionary
│   ├── county/                        # County-level files
│   ├── tract/                         # Tract-level files
│   ├── block_group/                   # Block group files (ADI)
│   └── crosswalks/                    # FIPS and CBSA mappings
│
├── data-access/                       # Data Access Skills (v2.0)
│   ├── README.md                      # Category overview
│   ├── data-lookup.md                 # Direct value lookups
│   ├── geography-lookup.md            # FIPS code resolution
│   └── data-aggregation.md            # Geographic aggregation
│
├── geographic/                        # Geographic Intelligence
│   ├── README.md                      # Category overview
│   ├── county-profile.md              # County-level profiles
│   ├── census-tract-analysis.md       # Tract-level analysis
│   ├── metro-area-profile.md          # MSA/CBSA profiles
│   └── custom-region-builder.md       # Custom region aggregation
│
├── health-patterns/                   # Health Analysis
│   ├── README.md                      # Category overview
│   ├── chronic-disease-prevalence.md  # Disease burden analysis
│   ├── health-behavior-patterns.md    # Risk factor analysis
│   ├── healthcare-access-analysis.md  # Coverage and access
│   └── health-outcome-disparities.md  # Disparity analysis
│
├── sdoh/                              # Social Determinants
│   ├── README.md                      # SDOH framework overview
│   ├── svi-analysis.md                # Social Vulnerability Index
│   ├── adi-analysis.md                # Area Deprivation Index
│   ├── economic-indicators.md         # Income, poverty, employment
│   └── community-factors.md           # Housing, transportation, food
│
├── cohorts/                           # Cohort Definition
│   ├── README.md                      # CohortSpecification schema
│   ├── cohort-specification.md        # Complete cohort definition
│   ├── demographic-distribution.md    # Age, sex, race distributions
│   ├── clinical-prevalence-profile.md # Comorbidity patterns
│   └── sdoh-profile-builder.md        # SDOH and Z-code rates
│
└── trial-support/                     # Clinical Trial Support
    ├── README.md                      # Trial integration overview
    ├── feasibility-estimation.md      # Eligible population modeling
    ├── site-selection-support.md      # Site network optimization
    └── enrollment-projection.md       # Timeline projections
```

## Quick Examples

### Example 1: County Health Profile

**Request:** "Profile San Diego County health indicators"

**Response:**

San Diego County, CA (FIPS 06073) Population Profile:

**Demographics** (ACS 2022 5-year):
- Total Population: 3,286,069
- Median Age: 37.1 years
- Race/Ethnicity: 43% White NH, 34% Hispanic, 12% Asian, 5% Black

**Health Indicators** (CDC PLACES 2024):
- Diabetes: 9.5% (vs 10.1% national)
- Obesity: 28.0% (vs 32.1% national)
- Hypertension: 28.5% (vs 32.4% national)

**SDOH Indices**:
- SVI Overall: 0.42 (moderate vulnerability)
- ADI National Rank: 35th percentile

### Example 2: Cohort for PatientSim

**Request:** "Define a cohort of high-risk diabetics in underserved California"

**Response:** Creates CohortSpecification with:
- Geography: CA census tracts with SVI ≥ 0.70
- Demographics: Hispanic 58%, mean age 58.4
- Comorbidities: HTN 71%, obesity 62%
- SDOH: Rx cost barrier 31%, food insecurity 22%

### Example 3: Trial Feasibility

**Request:** "Feasibility for T2DM trial: age 40-70, HbA1c 8-11%"

**Response:**

| Stage | Population | Conversion |
|-------|------------|------------|
| T2DM Prevalent | 34.2M | - |
| Age 40-70 | 24.8M | 72.5% |
| HbA1c 8-11% | 7.4M | 29.8% |
| After exclusions | 4.2M | - |

**Top Metros**: Houston (128K), Miami (115K), Los Angeles (108K)

## Related Products

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data
- [MemberSim](../membersim/SKILL.md) - Health plan member data
- [RxMemberSim](../rxmembersim/SKILL.md) - Pharmacy data
- [TrialSim](../trialsim/SKILL.md) - Clinical trial data
- [NetworkSim](../networksim/SKILL.md) - Provider networks

## Domain Knowledge

For detailed concepts and methodology, see:
- [Population Intelligence Domain](population-intelligence-domain.md) - Geographic hierarchy, census data, SDOH frameworks
