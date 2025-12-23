---
name: sdoh-profile-builder
description: >
  Build SDOH profiles for cohorts including social vulnerability indices,
  economic factors, and Z-code assignment rates. Translates population SDOH
  data into individual-level generation parameters. Triggers: "SDOH profile",
  "social factors for cohort", "Z-code rates", "vulnerability profile".
---

# SDOH Profile Builder Skill

## Overview

The sdoh-profile-builder skill creates comprehensive SDOH profiles for cohorts by translating population-level social determinant data into individual-level generation parameters. It produces Z-code assignment rates and social factor distributions that drive realistic synthetic patient generation.

**Primary Use Cases**:
- Add SDOH dimension to cohorts
- Set Z-code rates for PatientSim
- Model social vulnerability
- Support health equity analysis

---

## Trigger Phrases

- "SDOH profile for [geography/population]"
- "Social factors for this cohort"
- "What Z-codes should we assign?"
- "Vulnerability profile for [area]"
- "Build SDOH characteristics for [cohort]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | Geographic scope |
| `population_type` | string | No | "general" | "general", "medicaid", "medicare", "uninsured" |
| `svi_threshold` | float | No | - | Filter by SVI (0-1) |
| `include_z_codes` | bool | No | true | Include Z-code mapping |

---

## SDOH Framework

### Five Domains

| Domain | Factors | ICD-10 Z-Code Range |
|--------|---------|---------------------|
| **Economic Stability** | Income, employment, food, housing costs | Z55-Z59 |
| **Education Access** | Literacy, language, early childhood | Z55.x |
| **Healthcare Access** | Insurance, providers, transportation | Z59.82, Z75.x |
| **Neighborhood** | Housing, transportation, safety, environment | Z59.0-Z59.1 |
| **Social/Community** | Social support, discrimination, incarceration | Z60.x, Z62.x, Z65.x |

### SVI to SDOH Mapping

| SVI Theme | SDOH Factors | Typical Indicators |
|-----------|--------------|-------------------|
| Socioeconomic | Income, employment, insurance | Poverty rate, uninsured |
| Household Composition | Age vulnerability, disability, single parent | Elder %, disabled % |
| Minority/Language | Acculturation, discrimination | Limited English, minority % |
| Housing/Transportation | Housing quality, mobility | No vehicle, crowding |

---

## Z-Code Reference

### Economic Z-Codes (Z59)

| Code | Description | Prevalence Driver |
|------|-------------|-------------------|
| Z59.00 | Homelessness, unspecified | Housing status |
| Z59.01 | Sheltered homelessness | Housing status |
| Z59.02 | Unsheltered homelessness | Housing status |
| Z59.1 | Inadequate housing | Housing quality |
| Z59.41 | Food insecurity | Food access, income |
| Z59.6 | Low income | Poverty rate |
| Z59.7 | Insufficient social insurance | Uninsured rate |
| Z59.81 | Housing instability | Renter %, cost burden |
| Z59.82 | Transportation insecurity | No vehicle % |
| Z59.86 | Financial insecurity | Income instability |
| Z59.87 | Material hardship | Multiple factors |

### Education Z-Codes (Z55)

| Code | Description | Prevalence Driver |
|------|-------------|-------------------|
| Z55.0 | Illiteracy/low-level literacy | Education attainment |
| Z55.1 | Schooling unavailable | Rural, access |
| Z55.2 | Failed school examinations | Education outcome |
| Z55.3 | Underachievement in school | Education outcome |
| Z55.4 | Educational maladjustment | School issues |
| Z55.5 | Less than HS | HS diploma % |
| Z55.9 | Education problems, unspecified | General |

### Social Z-Codes (Z60)

| Code | Description | Prevalence Driver |
|------|-------------|-------------------|
| Z60.0 | Phase of life problem | Age-related |
| Z60.2 | Living alone | Household composition |
| Z60.3 | Acculturation difficulty | Limited English |
| Z60.4 | Social exclusion/rejection | Minority status |
| Z60.5 | Target of discrimination | Minority status |
| Z60.9 | Social environment problems | General |

---

## Output Schema

```json
{
  "sdoh_profile": {
    "cohort_context": {
      "geography": "Bronx County, NY",
      "population_type": "medicaid",
      "svi_overall": 0.94
    },
    
    "vulnerability_indices": {
      "svi_overall": 0.94,
      "svi_socioeconomic": 0.96,
      "svi_household_composition": 0.88,
      "svi_minority_language": 0.98,
      "svi_housing_transportation": 0.92,
      "adi_national_percentile": 89
    },
    
    "domain_profiles": {
      "economic_stability": {
        "poverty_rate": 0.28,
        "deep_poverty_rate": 0.14,
        "unemployment_rate": 0.09,
        "food_insecurity": 0.18,
        "housing_cost_burden": 0.52,
        "summary": "high_vulnerability"
      },
      "education_access": {
        "no_hs_diploma": 0.22,
        "limited_english": 0.24,
        "early_childhood_access": 0.68,
        "summary": "moderate_vulnerability"
      },
      "healthcare_access": {
        "uninsured_rate": 0.08,
        "no_usual_source_of_care": 0.14,
        "transportation_barrier": 0.12,
        "provider_shortage": false,
        "summary": "moderate_vulnerability"
      },
      "neighborhood": {
        "crowded_housing": 0.08,
        "no_vehicle": 0.52,
        "mobile_home": 0.01,
        "vacant_housing": 0.06,
        "summary": "high_vulnerability"
      },
      "social_community": {
        "living_alone_elderly": 0.28,
        "single_parent": 0.38,
        "limited_social_support": 0.22,
        "discrimination_exposure": 0.18,
        "summary": "high_vulnerability"
      }
    },
    
    "z_code_rates": {
      "economic": {
        "Z59.6": { "name": "Low income", "rate": 0.28, "confidence": "high" },
        "Z59.41": { "name": "Food insecurity", "rate": 0.18, "confidence": "high" },
        "Z59.81": { "name": "Housing instability", "rate": 0.14, "confidence": "moderate" },
        "Z59.82": { "name": "Transportation insecurity", "rate": 0.12, "confidence": "high" },
        "Z59.00": { "name": "Homelessness", "rate": 0.02, "confidence": "moderate" }
      },
      "education": {
        "Z55.5": { "name": "Less than HS", "rate": 0.22, "confidence": "high" },
        "Z55.0": { "name": "Low literacy", "rate": 0.08, "confidence": "low" }
      },
      "social": {
        "Z60.3": { "name": "Acculturation difficulty", "rate": 0.24, "confidence": "high" },
        "Z60.2": { "name": "Living alone", "rate": 0.12, "confidence": "moderate" },
        "Z60.4": { "name": "Social exclusion", "rate": 0.08, "confidence": "low" }
      }
    },
    
    "composite_z_code_assignment": {
      "any_z_code": 0.48,
      "one_z_code": 0.22,
      "two_z_codes": 0.14,
      "three_plus_z_codes": 0.12
    },
    
    "health_impact_expectations": {
      "delayed_care_due_to_cost": 0.18,
      "delayed_care_due_to_transport": 0.12,
      "medication_nonadherence_cost": 0.14,
      "missed_appointments": 0.16,
      "ed_for_primary_care": 0.22
    },
    
    "generation_parameters": {
      "z_code_assignment_method": "probabilistic",
      "correlation_model": "clustered",
      "notes": "Z-codes cluster by household/economic factors"
    }
  },
  
  "validation": {
    "sources": ["CDC_SVI_2022", "ACS_2022", "USDA_Food_Atlas"],
    "confidence": "high"
  }
}
```

---

## Examples

### Example 1: High-Vulnerability Population

**Request**: "SDOH profile for Detroit Medicaid population"

**Response**:

**Detroit Medicaid SDOH Profile**

**Vulnerability Summary**:
- SVI Overall: 0.89 (High)
- ADI National: 84th percentile

**Domain Scores**:
| Domain | Score | Key Factor |
|--------|-------|------------|
| Economic | 0.92 | Poverty 34% |
| Education | 0.78 | No HS 18% |
| Healthcare Access | 0.62 | Transport barrier 18% |
| Neighborhood | 0.88 | No vehicle 28% |
| Social | 0.82 | Single parent 42% |

**Z-Code Assignment Rates**:
| Code | Description | Rate |
|------|-------------|------|
| Z59.6 | Low income | 34% |
| Z59.41 | Food insecurity | 22% |
| Z59.82 | Transportation insecurity | 18% |
| Z59.81 | Housing instability | 16% |
| Z55.5 | Less than HS | 18% |
| Z60.2 | Living alone | 14% |

**Multi-Z-Code Distribution**:
- No Z-codes: 42%
- 1 Z-code: 24%
- 2 Z-codes: 18%
- 3+ Z-codes: 16%

**Health Impact**:
| Outcome | Expected Rate |
|---------|---------------|
| Missed appointments | 22% |
| Medication nonadherence | 18% |
| ED for primary care | 28% |

---

### Example 2: Moderate-Vulnerability Suburban

**Request**: "SDOH profile for suburban Phoenix"

**Response**:

**Suburban Phoenix (Maricopa excl. Phoenix city) SDOH Profile**

**Vulnerability Summary**:
- SVI Overall: 0.38 (Low-Moderate)
- ADI National: 32nd percentile

**Domain Scores**:
| Domain | Score | Key Factor |
|--------|-------|------------|
| Economic | 0.34 | Poverty 9% |
| Education | 0.28 | No HS 8% |
| Healthcare Access | 0.42 | Uninsured 9% |
| Neighborhood | 0.32 | Sprawl, car-dependent |
| Social | 0.36 | Moderate support |

**Z-Code Assignment Rates**:
| Code | Description | Rate |
|------|-------------|------|
| Z59.6 | Low income | 9% |
| Z59.82 | Transportation insecurity | 4% |
| Z59.41 | Food insecurity | 6% |
| Z55.5 | Less than HS | 8% |

**Multi-Z-Code Distribution**:
- No Z-codes: 78%
- 1 Z-code: 14%
- 2+ Z-codes: 8%

---

### Example 3: Rural FQHC Service Area

**Request**: "SDOH profile for rural Appalachian FQHC catchment"

**Response**:

**Rural Appalachian FQHC SDOH Profile**

**Vulnerability Summary**:
- SVI Overall: 0.82 (High)
- ADI National: 88th percentile

**Key SDOH Factors**:
| Factor | Rate | vs National |
|--------|------|-------------|
| Poverty | 28% | +16.5% |
| No HS Diploma | 18% | +6% |
| Uninsured | 12% | +3.8% |
| No Vehicle | 9% | +0.8% |
| Limited English | 2% | -6% |
| Food Insecurity | 18% | +7% |

**Z-Code Assignment Rates**:
| Code | Description | Rate | Notes |
|------|-------------|------|-------|
| Z59.6 | Low income | 28% | Primary driver |
| Z59.41 | Food insecurity | 18% | Food desert |
| Z59.82 | Transportation | 14% | Distance to care |
| Z55.5 | Less than HS | 18% | Education gap |
| Z59.1 | Inadequate housing | 8% | Housing quality |
| Z60.2 | Living alone | 16% | Elderly isolation |

**Unique Rural Factors**:
- Distance to hospital: 32 miles average
- Distance to pharmacy: 18 miles average
- Broadband access: 62% (telehealth barrier)
- Provider shortage: HPSA score 18

**Health Impact**:
| Factor | Impact |
|--------|--------|
| Delayed care (distance) | 28% |
| Medication mail-order | 42% |
| Telehealth eligible | 58% |

---

## Z-Code Assignment Logic

### Correlation Clusters

Z-codes tend to cluster together:

**Economic Hardship Cluster**:
```
Z59.6 (Low income) often co-occurs with:
  - Z59.41 (Food insecurity) - 65% correlation
  - Z59.81 (Housing instability) - 58% correlation
  - Z59.82 (Transportation) - 52% correlation
```

**Social Isolation Cluster**:
```
Z60.2 (Living alone) often co-occurs with:
  - Z60.0 (Phase of life problem) - 42% correlation
  - Z59.82 (Transportation) - 38% correlation
```

**Immigration/Language Cluster**:
```
Z60.3 (Acculturation difficulty) often co-occurs with:
  - Z55.0 (Low literacy) - 48% correlation
  - Z59.6 (Low income) - 42% correlation
```

### Generation Algorithm

```
1. Determine base Z-code probability from SVI/SDOH indicators
2. Apply population-type modifier (Medicaid +20%, Medicare +10%)
3. Apply condition modifier (chronic disease +15%)
4. Generate Z-codes with correlation clustering
5. Limit to realistic maximum (typically 1-3 Z-codes)
```

---

## Validation Rules

### Input Validation
- Geography must be valid
- Population type must be recognized
- SVI threshold 0-1 if specified

### Output Validation
- [ ] All rates between 0 and 1
- [ ] Z-code rates match SDOH indicators
- [ ] Multi-Z-code distribution sums to 1.0
- [ ] Clustering patterns realistic

---

## Related Skills

- [cohort-specification.md](cohort-specification.md) - Full cohort
- [svi-analysis.md](../sdoh/svi-analysis.md) - SVI source
- [adi-analysis.md](../sdoh/adi-analysis.md) - ADI source
- [economic-indicators.md](../sdoh/economic-indicators.md) - Economic detail
- [community-factors.md](../sdoh/community-factors.md) - Community factors
