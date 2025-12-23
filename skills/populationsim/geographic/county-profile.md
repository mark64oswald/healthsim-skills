---
name: county-profile
description: >
  Generate comprehensive county-level population profiles including demographics,
  health indicators, and SDOH indices. Use for county profiling, regional planning,
  service area analysis, or county comparisons. Triggers: "county profile",
  "demographics for [county]", "health indicators for [county]", "profile [county]".
---

# County Profile Skill

## Overview

The county-profile skill generates comprehensive PopulationProfile objects for US counties, combining Census ACS demographics, CDC PLACES health indicators, and SDOH indices (SVI, ADI) into a unified profile.

**Primary Use Cases**:
- Regional health department planning
- Service area demographic analysis
- Health plan market assessment
- County-to-county comparisons
- Foundation for cohort definition

---

## Trigger Phrases

- "Profile [county name]"
- "County profile for [county]"
- "Demographics for [county name], [state]"
- "Health indicators for [county]"
- "Show me [county] population data"
- "Compare [county A] and [county B]"
- "What's the population of [county]?"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `county` | string | Yes | - | County name or FIPS code |
| `state` | string | Conditional | - | Required if county name is ambiguous |
| `include_health` | boolean | No | true | Include CDC PLACES health indicators |
| `include_sdoh` | boolean | No | true | Include SVI and ADI indices |
| `include_access` | boolean | No | true | Include healthcare access metrics |
| `compare_to` | string | No | - | County to compare against |
| `benchmark` | string | No | "state" | Comparison benchmark: "state", "national", "none" |

---

## Generation Patterns

### Pattern 1: Single County Profile

**Input**: "Profile San Diego County"

**Process**:
1. Resolve county identifier → FIPS 06073
2. Pull ACS demographics (S0101, B03002, S1901, S2701)
3. Pull CDC PLACES health measures
4. Pull SVI scores for county
5. Calculate county-level ADI aggregate
6. Assemble PopulationProfile

**Output**: Complete PopulationProfile for San Diego County

### Pattern 2: County Comparison

**Input**: "Compare Harris County TX to Los Angeles County CA"

**Process**:
1. Generate profiles for both counties
2. Calculate differences and ratios
3. Identify notable disparities
4. Apply benchmark comparisons

**Output**: Two profiles with comparison table

### Pattern 3: County with Specific Focus

**Input**: "Show diabetes-related metrics for Cook County IL"

**Process**:
1. Generate base county profile
2. Expand health indicators section with diabetes-related measures
3. Include diabetes-correlated SDOH factors
4. Add comorbidity context

**Output**: Profile with diabetes focus

---

## Output Schema

```json
{
  "geography": {
    "type": "county",
    "fips": "06073",
    "name": "San Diego County",
    "state": "CA",
    "state_fips": "06",
    "region": "West",
    "division": "Pacific",
    "urban_rural": "metro",
    "cbsa_code": "41740",
    "cbsa_name": "San Diego-Chula Vista-Carlsbad, CA"
  },
  "demographics": {
    "total_population": 3286069,
    "population_density": 775.2,
    "land_area_sq_mi": 4239.7,
    "median_age": 37.1,
    "age_distribution": {
      "0-4": 0.059,
      "5-17": 0.151,
      "18-24": 0.098,
      "25-34": 0.157,
      "35-44": 0.139,
      "45-54": 0.119,
      "55-64": 0.117,
      "65-74": 0.095,
      "75+": 0.066
    },
    "sex_distribution": {
      "male": 0.495,
      "female": 0.505
    },
    "race_ethnicity": {
      "white_nh": 0.434,
      "hispanic": 0.339,
      "asian": 0.124,
      "black": 0.052,
      "aian": 0.008,
      "nhpi": 0.005,
      "two_or_more": 0.038
    },
    "median_household_income": 102285,
    "per_capita_income": 49377,
    "poverty_rate": 0.103,
    "education": {
      "less_than_hs": 0.112,
      "hs_graduate": 0.178,
      "some_college": 0.281,
      "bachelors_plus": 0.429
    }
  },
  "health_indicators": {
    "source": "CDC_PLACES_2024",
    "methodology": "age_adjusted",
    "chronic_conditions": {
      "diabetes": 0.095,
      "obesity": 0.280,
      "hypertension": 0.285,
      "high_cholesterol": 0.318,
      "chd": 0.048,
      "stroke": 0.028,
      "copd": 0.043,
      "asthma": 0.095,
      "ckd": 0.028,
      "depression": 0.195,
      "arthritis": 0.215,
      "cancer": 0.058
    },
    "health_behaviors": {
      "smoking": 0.098,
      "binge_drinking": 0.178,
      "physical_inactivity": 0.182,
      "short_sleep": 0.352
    },
    "prevention": {
      "annual_checkup": 0.785,
      "dental_visit": 0.685,
      "cholesterol_screening": 0.872,
      "colorectal_screening": 0.682,
      "mammography": 0.798
    },
    "health_status": {
      "fair_poor_health": 0.148,
      "poor_mental_health_days": 0.128,
      "poor_physical_health_days": 0.102
    }
  },
  "sdoh_indices": {
    "svi": {
      "source": "CDC_SVI_2022",
      "overall": 0.42,
      "themes": {
        "socioeconomic": 0.38,
        "household_composition": 0.45,
        "minority_language": 0.52,
        "housing_transportation": 0.35
      },
      "interpretation": "moderate"
    },
    "adi": {
      "source": "ADI_2021",
      "national_percentile": 35,
      "state_decile": 4,
      "interpretation": "low_moderate"
    }
  },
  "healthcare_access": {
    "insurance_coverage": {
      "insured_rate": 0.929,
      "uninsured_rate": 0.071,
      "coverage_type": {
        "employer": 0.518,
        "medicare": 0.152,
        "medicaid": 0.181,
        "individual": 0.078,
        "military": 0.058,
        "uninsured": 0.071
      }
    },
    "provider_availability": {
      "pcp_per_100k": 82.4,
      "dentist_per_100k": 89.2,
      "mental_health_per_100k": 215.8
    },
    "facility_access": {
      "hospitals": 28,
      "fqhcs": 47,
      "urgent_care": 142
    }
  },
  "comparison": {
    "benchmark": "state",
    "benchmark_name": "California",
    "notable_differences": [
      {
        "metric": "diabetes_prevalence",
        "county_value": 0.095,
        "benchmark_value": 0.101,
        "difference": -0.006,
        "interpretation": "below_average"
      }
    ]
  },
  "metadata": {
    "generated_at": "2024-12-23T10:00:00Z",
    "data_vintage": {
      "census": "ACS_2022_5yr",
      "health": "CDC_PLACES_2024",
      "svi": "CDC_SVI_2022",
      "adi": "ADI_2021"
    },
    "reliability": {
      "overall": "high",
      "notes": "Large population county with reliable estimates"
    }
  }
}
```

---

## Examples

### Example 1: Basic County Profile

**Request**: "Profile Harris County, Texas"

**Response**:

**Harris County, TX (FIPS 48201) Population Profile**

| Category | Value | vs Texas |
|----------|-------|----------|
| **Population** | 4,731,145 | Largest in TX |
| **Median Age** | 34.4 | Younger than state (35.8) |
| **Median Income** | $67,706 | Above state ($67,321) |
| **Poverty Rate** | 13.8% | Above state (13.1%) |

**Race/Ethnicity**:
- Hispanic: 43.8%
- White NH: 28.5%
- Black: 19.4%
- Asian: 7.3%

**Health Indicators** (CDC PLACES):
| Condition | Harris | Texas | National |
|-----------|--------|-------|----------|
| Diabetes | 12.4% | 11.8% | 10.1% ⚠️ |
| Obesity | 33.8% | 33.2% | 32.1% |
| Uninsured | 18.2% | 17.5% | 8.8% ⚠️ |

**SDOH Indices**:
- SVI Overall: 0.68 (moderate-high vulnerability)
- ADI National: 58th percentile

---

### Example 2: County Comparison

**Request**: "Compare Maricopa County AZ to Clark County NV"

**Response**:

**County Comparison: Maricopa vs Clark**

| Metric | Maricopa, AZ | Clark, NV | Difference |
|--------|--------------|-----------|------------|
| Population | 4,420,568 | 2,265,461 | +2.15M |
| Median Age | 38.1 | 38.4 | -0.3 |
| Median Income | $82,134 | $68,879 | +$13,255 |
| Poverty Rate | 10.8% | 12.1% | -1.3% |
| Diabetes | 10.2% | 11.8% | -1.6% ✓ |
| Obesity | 30.4% | 28.2% | +2.2% |
| Uninsured | 9.8% | 11.2% | -1.4% ✓ |
| SVI Overall | 0.51 | 0.62 | -0.11 ✓ |

**Key Findings**:
- Maricopa has higher income and lower poverty
- Maricopa has lower diabetes prevalence
- Clark has lower obesity but higher uninsured
- Maricopa has lower social vulnerability overall

---

### Example 3: Focused Profile

**Request**: "Show cardiovascular health metrics for Cuyahoga County, Ohio"

**Response**:

**Cuyahoga County, OH - Cardiovascular Health Profile**

**Demographics Context**:
- Population: 1,249,352
- Median Age: 40.2 (older than state average)
- 65+ Population: 18.4%

**Cardiovascular Conditions** (CDC PLACES):
| Condition | Cuyahoga | Ohio | National | Status |
|-----------|----------|------|----------|--------|
| Coronary Heart Disease | 6.8% | 6.4% | 5.4% | ⚠️ High |
| Stroke | 3.8% | 3.5% | 3.0% | ⚠️ High |
| Hypertension | 35.2% | 33.8% | 32.4% | ⚠️ High |
| High Cholesterol | 34.1% | 32.8% | 31.2% | ⚠️ High |

**CV Risk Factors**:
| Factor | Cuyahoga | Ohio | National |
|--------|----------|------|----------|
| Obesity | 34.8% | 35.2% | 32.1% |
| Smoking | 19.2% | 19.8% | 14.1% |
| Physical Inactivity | 27.4% | 26.2% | 22.8% |
| Diabetes | 12.8% | 12.1% | 10.1% |

**SDOH Context**:
- SVI: 0.72 (high vulnerability)
- Socioeconomic Theme: 0.78 (high)
- Uninsured: 5.8%

**Implications for HealthSim**:
When generating patients from Cuyahoga County, expect:
- Higher rates of CV conditions and risk factors
- Multiple comorbidities common (HTN + DM + HLD)
- Higher smoking history prevalence
- SDOH factors: higher rates of economic barriers

---

## Validation Rules

### Input Validation
- County name must match Census gazetteer or valid FIPS
- State required for ambiguous county names (e.g., "Washington County" exists in 30 states)
- FIPS code must be 5 digits and valid

### Output Validation
- [ ] Population > 0
- [ ] All percentages between 0 and 1
- [ ] Age distribution sums to ~1.0
- [ ] Race/ethnicity sums to ~1.0
- [ ] Health indicators within realistic ranges
- [ ] SVI between 0 and 1
- [ ] Data vintage noted in metadata

### Reliability Thresholds
| Population | Estimate Type | Reliability |
|------------|---------------|-------------|
| > 65,000 | ACS 1-year | High |
| 20,000-65,000 | ACS 5-year | Moderate |
| < 20,000 | ACS 5-year | Use with caution |

---

## Related Skills

- [census-tract-analysis.md](census-tract-analysis.md) - Granular tract-level analysis
- [metro-area-profile.md](metro-area-profile.md) - MSA aggregate profiles
- [custom-region-builder.md](custom-region-builder.md) - Multi-county regions
- [cohort-specification.md](../cohorts/cohort-specification.md) - Define cohorts from profiles
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Disease deep dives

---

## Data Sources

| Data Element | Source | Vintage | Geography |
|--------------|--------|---------|-----------|
| Demographics | Census ACS | 2022 5-year | County |
| Health Indicators | CDC PLACES | 2024 release | County |
| SVI | CDC/ATSDR | 2022 | County (from tracts) |
| ADI | HRSAdmin | 2021 | County (from block groups) |
| Provider Data | HRSA AHRF | 2023 | County |
