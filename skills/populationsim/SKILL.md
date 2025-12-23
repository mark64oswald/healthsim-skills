---
name: healthsim-populationsim
description: >
  PopulationSim provides population-level intelligence using public data sources.
  Use this skill for ANY request involving: (1) population demographics or profiles,
  (2) geographic health patterns or disparities, (3) social determinants of health (SDOH),
  (4) SVI or ADI analysis, (5) cohort definition or specification, (6) clinical trial
  diversity planning or site selection, (7) service area analysis, (8) health equity assessment,
  (9) census data or ACS variables, (10) CDC PLACES health indicators.
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
| Profile a county or region | `geographic/county-profile.md` | "county profile", "demographics for", "health indicators" |
| Analyze census tracts | `geographic/census-tract-analysis.md` | "tract level", "granular", "hotspots" |
| Profile a metro area | `geographic/metro-area-profile.md` | "metro", "MSA", "metropolitan" |
| Define custom region | `geographic/custom-region-builder.md` | "service area", "combine", "custom region" |
| Analyze disease prevalence | `health-patterns/chronic-disease-prevalence.md` | "diabetes rate", "prevalence", "CDC PLACES" |
| Analyze health behaviors | `health-patterns/health-behavior-patterns.md` | "smoking rate", "obesity", "physical activity" |
| Assess healthcare access | `health-patterns/healthcare-access-analysis.md` | "uninsured", "provider ratio", "access" |
| Identify health disparities | `health-patterns/health-outcome-disparities.md` | "disparities", "equity", "by race" |
| Analyze SVI | `sdoh/svi-analysis.md` | "SVI", "social vulnerability", "vulnerable" |
| Analyze ADI | `sdoh/adi-analysis.md` | "ADI", "area deprivation", "deprived" |
| Analyze economics | `sdoh/economic-indicators.md` | "poverty", "income", "unemployment" |
| Analyze community factors | `sdoh/community-factors.md` | "housing", "transportation", "food access" |
| Define a cohort | `cohorts/cohort-specification.md` | "define cohort", "cohort spec", "population segment" |
| Generate patients from cohort | `cohorts/patientsim-cohort.md` | "generate patients", "PatientSim cohort" |
| Generate members from cohort | `cohorts/membersim-cohort.md` | "generate members", "MemberSim cohort" |
| Plan trial recruitment | `cohorts/trialsim-cohort.md` | "trial recruitment", "enrollment pool" |
| Plan trial diversity | `trial-support/diversity-planning.md` | "diversity", "FDA diversity", "representation" |
| Select trial sites | `trial-support/site-selection.md` | "site selection", "rank sites", "feasibility" |
| Assess protocol feasibility | `trial-support/feasibility-assessment.md` | "feasibility", "enrollment projection" |

## Trigger Phrases

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

### Trial Support
- "Plan diversity for a Phase III oncology trial"
- "Rank trial sites for cardiovascular outcomes study"
- "Assess feasibility for 500 subjects across 10 sites"
- "Which metros have the best recruitment potential?"

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
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "data_vintage": {
      "census": "ACS_2022_5yr",
      "health": "CDC_PLACES_2024",
      "svi": "CDC_SVI_2022"
    }
  }
}
```

### CohortSpecification

Generation input for other HealthSim products:

```json
{
  "cohort_id": "CA-HIGHRISK-DM-001",
  "name": "High-Risk Diabetics - California Underserved",
  "description": "Adults 40-75 with T2D in high-SVI California census tracts",
  "geography_filter": {
    "base": "state:CA",
    "constraint": "svi_overall >= 0.70",
    "resolved_units": {
      "type": "census_tract",
      "count": 1847
    }
  },
  "population_filter": {
    "age_range": [40, 75],
    "conditions": ["E11"],
    "sdoh_risk": "high"
  },
  "estimated_real_population": 412000,
  "demographic_profile": {
    "race_ethnicity": {
      "hispanic": 0.582,
      "white_nh": 0.184,
      "asian": 0.121,
      "black": 0.078,
      "other": 0.035
    },
    "mean_age": 58.4,
    "female_pct": 0.52
  },
  "clinical_profile": {
    "comorbidities": {
      "hypertension": 0.712,
      "obesity": 0.624,
      "hyperlipidemia": 0.589,
      "depression": 0.281,
      "ckd": 0.243
    },
    "avg_a1c": 8.2
  },
  "sdoh_profile": {
    "rx_cost_barrier": 0.312,
    "limited_english": 0.284,
    "food_insecurity": 0.224,
    "transportation_barrier": 0.181
  },
  "target_product": "PatientSim",
  "generation_options": {
    "count": 500,
    "include_encounter_history": true,
    "include_sdoh_zcodes": true,
    "include_medications": true
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

### Integration Examples

**PopulationSim → PatientSim**:
```
"Define a cohort of high-risk diabetics in underserved California, 
then generate 500 patients matching that profile"
```

**PopulationSim → TrialSim**:
```
"Plan diversity for a Phase III NASH trial with 800 subjects,
then generate subjects matching FDA diversity guidance"
```

**Full Chain**:
```
"Profile San Diego County demographics and health patterns,
define a heart failure cohort from high-SVI tracts,
generate 100 patients with realistic claims history"
```

## Data Sources

| Source | Provider | Data Type | Update Frequency |
|--------|----------|-----------|------------------|
| American Community Survey | Census Bureau | Demographics, economics | Annual |
| CDC PLACES | CDC | Health indicators (27 measures) | Annual |
| Social Vulnerability Index | CDC/ATSDR | SDOH composite (16 variables) | Biennial |
| Area Deprivation Index | HRSAdmin | Neighborhood deprivation | Annual |

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
- Depression: 19.5% (vs 18.6% national) ⚠️ Above national

**SDOH Indices**:
- SVI Overall: 0.42 (moderate vulnerability)
- ADI National Rank: 35th percentile

**Healthcare Access**:
- Uninsured: 7.1%
- PCPs per 100K: 82.4

### Example 2: Cohort for PatientSim

**Request:** "Define a cohort of high-risk diabetics in underserved California for PatientSim"

**Response:**

```json
{
  "cohort_id": "CA-HIGHRISK-DM-001",
  "name": "High-Risk Diabetics - California Underserved",
  "geography_filter": {
    "base": "state:CA",
    "constraint": "svi_overall >= 0.70"
  },
  "population_filter": {
    "age_range": [40, 75],
    "conditions": ["E11"]
  },
  "estimated_real_population": 412000,
  "demographic_profile": {
    "hispanic": 0.58,
    "mean_age": 58.4
  },
  "clinical_profile": {
    "hypertension": 0.71,
    "obesity": 0.62
  },
  "sdoh_profile": {
    "rx_cost_barrier": 0.31,
    "food_insecurity": 0.22
  },
  "target_product": "PatientSim"
}
```

This cohort specification can be passed to PatientSim to generate 500 synthetic patients matching these characteristics.

### Example 3: Trial Diversity Planning

**Request:** "Plan diversity for a 500-subject Phase III NASH trial"

**Response:**

**NASH Trial Diversity Analysis**

Disease Prevalence by Group:
- Hispanic: 22.1% (highest risk)
- White NH: 14.3%
- Black: 13.8%
- Asian: 8.9%

**Recommended Enrollment Targets** (vs Industry Typical):
| Group | Target | Industry Typical | Gap |
|-------|--------|------------------|-----|
| Hispanic | 35% (175) | 12% | +23% ✓ |
| White NH | 35% (175) | 72% | -37% ✓ |
| Black | 15% (75) | 8% | +7% ✓ |
| Asian | 10% (50) | 3% | +7% ✓ |
| Age 65+ | 25% (125) | 15% | +10% ✓ |

**Top Metro Sites** (by NASH prevalence + diversity):
1. Houston (7.2% NASH, diversity score 0.89)
2. Dallas (6.8% NASH, diversity score 0.86)
3. Los Angeles (6.5% NASH, diversity score 0.92)

## Directory Structure

```
skills/populationsim/
├── SKILL.md                           # This file - master router
├── README.md                          # Product overview
├── population-intelligence-domain.md  # Core domain knowledge
│
├── geographic/                        # Geographic Intelligence
│   ├── README.md
│   ├── county-profile.md
│   ├── census-tract-analysis.md
│   ├── metro-area-profile.md
│   └── custom-region-builder.md
│
├── health-patterns/                   # Health Analysis
│   ├── README.md
│   ├── chronic-disease-prevalence.md
│   ├── health-behavior-patterns.md
│   ├── healthcare-access-analysis.md
│   └── health-outcome-disparities.md
│
├── sdoh/                              # Social Determinants
│   ├── README.md
│   ├── svi-analysis.md
│   ├── adi-analysis.md
│   ├── economic-indicators.md
│   └── community-factors.md
│
├── cohorts/                           # Cohort Definition
│   ├── README.md
│   ├── cohort-specification.md
│   ├── patientsim-cohort.md
│   ├── membersim-cohort.md
│   └── trialsim-cohort.md
│
└── trial-support/                     # Clinical Trial Support
    ├── README.md
    ├── diversity-planning.md
    ├── site-selection.md
    └── feasibility-assessment.md
```

## Related Products

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data (receives CohortSpecification)
- [MemberSim](../membersim/SKILL.md) - Health plan member data (receives CohortSpecification)
- [RxMemberSim](../rxmembersim/SKILL.md) - Pharmacy data (receives CohortSpecification via MemberSim)
- [TrialSim](../trialsim/SKILL.md) - Clinical trial data (receives diversity specs)
- [NetworkSim](../networksim/SKILL.md) - Provider networks (receives service area profiles)

## Domain Knowledge

For detailed concepts and methodology, see:
- [Population Intelligence Domain](population-intelligence-domain.md) - Geographic hierarchy, census data, SDOH frameworks
