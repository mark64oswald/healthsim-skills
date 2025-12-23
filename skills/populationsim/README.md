# PopulationSim Skills

**Product**: PopulationSim - Population Intelligence & Cohort Generation  
**Status**: Active Development  
**Last Updated**: December 2024

---

## Overview

PopulationSim provides population-level intelligence using public data sources to enable geographic profiling, health disparities analysis, and cohort specification for synthetic data generation across the HealthSim ecosystem.

**Key Value Propositions**:

1. **Standalone Intelligence**: Profile geographies, analyze health patterns, assess SDOH
2. **Cross-Product Integration**: Create cohort specifications that drive PatientSim, MemberSim, and TrialSim
3. **Research Support**: Clinical trial diversity planning, site selection, feasibility assessment

**Unique Differentiator**: PopulationSim analyzes real population characteristics (from public data) and outputs specifications, not synthetic records.

---

## Quick Reference

| I want to... | Skill | Key Triggers |
|--------------|-------|--------------|
| Profile a county | `geographic/county-profile.md` | "county profile", "demographics for" |
| Analyze tracts | `geographic/census-tract-analysis.md` | "tract level", "hotspots" |
| Profile metro area | `geographic/metro-area-profile.md` | "metro", "MSA" |
| Build custom region | `geographic/custom-region-builder.md` | "service area", "combine" |
| Check disease prevalence | `health-patterns/chronic-disease-prevalence.md` | "diabetes rate", "prevalence" |
| Analyze behaviors | `health-patterns/health-behavior-patterns.md` | "smoking", "obesity" |
| Assess access | `health-patterns/healthcare-access-analysis.md` | "uninsured", "provider ratio" |
| Find disparities | `health-patterns/health-outcome-disparities.md` | "disparities", "equity" |
| Analyze SVI | `sdoh/svi-analysis.md` | "SVI", "social vulnerability" |
| Analyze ADI | `sdoh/adi-analysis.md` | "ADI", "area deprivation" |
| Check economics | `sdoh/economic-indicators.md` | "poverty", "income" |
| Check community | `sdoh/community-factors.md` | "housing", "transportation" |
| Define cohort | `cohorts/cohort-specification.md` | "define cohort", "cohort spec" |
| Cohort → PatientSim | `cohorts/patientsim-cohort.md` | "generate patients" |
| Cohort → MemberSim | `cohorts/membersim-cohort.md` | "generate members" |
| Cohort → TrialSim | `cohorts/trialsim-cohort.md` | "trial recruitment" |
| Plan diversity | `trial-support/diversity-planning.md` | "diversity", "FDA diversity" |
| Select sites | `trial-support/site-selection.md` | "site selection", "rank sites" |
| Assess feasibility | `trial-support/feasibility-assessment.md` | "feasibility", "enrollment" |

---

## Directory Structure

```
skills/populationsim/
├── SKILL.md                           # Master router
├── README.md                          # This file
├── population-intelligence-domain.md  # Core domain knowledge
│
├── geographic/                        # Geographic Intelligence Skills
│   ├── README.md                      # Category overview
│   ├── county-profile.md              # County-level analysis
│   ├── census-tract-analysis.md       # Tract-level granular analysis
│   ├── metro-area-profile.md          # MSA/CBSA aggregations
│   └── custom-region-builder.md       # User-defined regions
│
├── health-patterns/                   # Health Pattern Analysis Skills
│   ├── README.md                      # Category overview
│   ├── chronic-disease-prevalence.md  # CDC PLACES conditions
│   ├── health-behavior-patterns.md    # Risk behaviors
│   ├── healthcare-access-analysis.md  # Insurance, providers
│   └── health-outcome-disparities.md  # Equity analysis
│
├── sdoh/                              # SDOH Analysis Skills
│   ├── README.md                      # Category overview
│   ├── svi-analysis.md                # CDC Social Vulnerability Index
│   ├── adi-analysis.md                # Area Deprivation Index
│   ├── economic-indicators.md         # Income, poverty, employment
│   └── community-factors.md           # Housing, transportation, food
│
├── cohorts/                           # Cohort Definition Skills
│   ├── README.md                      # Category overview
│   ├── cohort-specification.md        # Core spec format
│   ├── patientsim-cohort.md           # PatientSim integration
│   ├── membersim-cohort.md            # MemberSim integration
│   └── trialsim-cohort.md             # TrialSim integration
│
└── trial-support/                     # Clinical Trial Support Skills
    ├── README.md                      # Category overview
    ├── diversity-planning.md          # FDA diversity requirements
    ├── site-selection.md              # Site ranking algorithm
    └── feasibility-assessment.md      # Protocol feasibility
```

---

## Skill Category Summaries

### Geographic Intelligence

**Purpose**: Profile geographic areas from nation to census tract level.

**Key Features**:
- County profiles with demographics, health, SDOH
- Census tract granular analysis for hotspot detection
- Metro area (MSA/CBSA) aggregate profiles
- Custom region building for service areas

**Data Sources**: Census ACS, FIPS codes, CBSA definitions

---

### Health Pattern Analysis

**Purpose**: Analyze health indicators, behaviors, and disparities using CDC PLACES data.

**Key Features**:
- Chronic disease prevalence (27 CDC PLACES measures)
- Health behavior patterns (smoking, obesity, physical activity)
- Healthcare access assessment (insurance, provider ratios)
- Health outcome disparities by demographic group

**Data Sources**: CDC PLACES, BRFSS, HRSA

---

### SDOH Analysis

**Purpose**: Assess social determinants of health using established indices.

**Key Features**:
- CDC Social Vulnerability Index (4 themes, 16 variables)
- Area Deprivation Index (national/state rankings)
- Economic indicators (income, poverty, unemployment)
- Community factors (housing, transportation, food access)

**Data Sources**: CDC/ATSDR SVI, HRSAdmin ADI, Census ACS

---

### Cohort Definition

**Purpose**: Create specifications that drive synthetic data generation in other products.

**Key Features**:
- Core cohort specification JSON format
- PatientSim integration (patients matching demographics/conditions)
- MemberSim integration (members with plan/utilization mix)
- TrialSim integration (diverse trial recruitment pools)

**Output**: CohortSpecification JSON consumed by generation products

---

### Trial Support

**Purpose**: Support clinical trial planning with population intelligence.

**Key Features**:
- FDA diversity guidance analysis and gap detection
- Trial site ranking by disease prevalence and diversity
- Protocol feasibility assessment with enrollment projections

**Integration**: Direct handoff to TrialSim for subject generation

---

## Canonical Data Models

### PopulationProfile

Geographic entity with demographics, health, and SDOH:

```json
{
  "geography": {
    "type": "county",
    "fips": "06073",
    "name": "San Diego County",
    "state": "CA"
  },
  "demographics": {
    "total_population": 3286069,
    "median_age": 37.1,
    "race_ethnicity": { "white_nh": 0.43, "hispanic": 0.34 }
  },
  "health_indicators": {
    "diabetes_prevalence": 0.095,
    "obesity_prevalence": 0.280
  },
  "sdoh_indices": {
    "svi_overall": 0.42,
    "adi_national_rank": 35
  },
  "healthcare_access": {
    "uninsured_rate": 0.071,
    "pcp_per_100k": 82.4
  }
}
```

### CohortSpecification

Generation input for other HealthSim products:

```json
{
  "cohort_id": "CA-HIGHRISK-DM-001",
  "geography_filter": {
    "base": "state:CA",
    "constraint": "svi_overall >= 0.70"
  },
  "population_filter": {
    "age_range": [40, 75],
    "conditions": ["E11"]
  },
  "demographic_profile": {
    "race_ethnicity": { "hispanic": 0.58 },
    "mean_age": 58.4
  },
  "clinical_profile": {
    "comorbidities": { "hypertension": 0.71 }
  },
  "sdoh_profile": {
    "rx_cost_barrier": 0.31
  },
  "target_product": "PatientSim"
}
```

---

## Data Sources

| Source | Provider | Content | Geography |
|--------|----------|---------|-----------|
| American Community Survey | Census Bureau | Demographics, economics | Tract → Nation |
| CDC PLACES | CDC | 27 health measures | County, Tract |
| Social Vulnerability Index | CDC/ATSDR | 16 SDOH variables | Tract |
| Area Deprivation Index | HRSAdmin | Neighborhood deprivation | Block Group |

### Data Vintage

All PopulationSim outputs include metadata noting data vintage:
- Census: ACS 2022 5-year estimates
- Health: CDC PLACES 2024 release
- SVI: CDC SVI 2022
- ADI: 2021 rankings

---

## Cross-Product Integration

### PopulationSim as Upstream Input

```
┌─────────────────────┐
│   PopulationSim     │
│  (Intelligence &    │
│   Cohort Specs)     │
└─────────┬───────────┘
          │ CohortSpecification
    ┌─────┴─────┬─────────┬─────────┐
    ▼           ▼         ▼         ▼
┌──────┐  ┌──────┐  ┌────────┐  ┌────────┐
│Patient│  │Member│  │RxMember│  │TrialSim│
│  Sim │  │ Sim  │  │  Sim   │  │        │
└──────┘  └──────┘  └────────┘  └────────┘
```

### Integration Examples

**Population → Patients**:
```
User: "Define a cohort of high-risk diabetics in CA, then generate 100 patients"

PopulationSim → CohortSpecification (demographics, comorbidities, SDOH)
PatientSim → 100 patients matching the specification
```

**Population → Trial**:
```
User: "Plan diversity for Phase III NASH trial, generate 500 subjects"

PopulationSim → Diversity targets, site rankings
TrialSim → 500 subjects meeting diversity goals
```

---

## Using PopulationSim

### Natural Language (Recommended)

Describe what you need:

```
"Profile San Diego County health indicators"

"What's the diabetes prevalence in Texas border counties?"

"Define a cohort of underserved heart failure patients in the Southeast"

"Plan diversity for a 500-subject oncology trial"
```

### Explicit Skill Reference

For precision:

```
"Using county-profile.md, analyze Harris County, TX"

"Apply svi-analysis.md to find vulnerable tracts in Los Angeles"

"Use diversity-planning.md for FDA diversity in NASH trial"
```

---

## Validation Notes

### Data Quality Indicators

PopulationSim outputs include reliability indicators:

| Indicator | Meaning |
|-----------|---------|
| ✓ High confidence | CV < 15%, large population |
| ~ Moderate confidence | CV 15-30%, adequate sample |
| ⚠️ Use with caution | CV > 30%, small population |

### Validation Checklist

Before using PopulationSim output:

- [ ] Verify geography FIPS codes are correct
- [ ] Check data vintage matches your needs
- [ ] Review margin of error for small populations
- [ ] Confirm health indicators are age-adjusted for comparisons
- [ ] Validate cohort spec matches target product requirements

---

## Related Documentation

| Document | Location |
|----------|----------|
| Domain Knowledge | `population-intelligence-domain.md` |
| Master SKILL | `SKILL.md` |
| Architecture Guide | `../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` |
| Cross-Product Examples | `../../hello-healthsim/examples/cross-domain-examples.md` |

---

## Related Products

| Product | Relationship |
|---------|--------------|
| **PatientSim** | Receives CohortSpecification for patient generation |
| **MemberSim** | Receives CohortSpecification for member generation |
| **RxMemberSim** | Receives population profiles via MemberSim |
| **TrialSim** | Receives diversity specs for subject generation |
| **NetworkSim** | Receives service area profiles for network design |

---

*For detailed domain concepts, see [Population Intelligence Domain](population-intelligence-domain.md).*
