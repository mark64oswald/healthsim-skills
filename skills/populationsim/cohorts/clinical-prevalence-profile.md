---
name: clinical-prevalence-profile
description: >
  Build clinical profiles with disease prevalence, comorbidity patterns, and
  severity distributions for cohorts. Uses CDC PLACES, MEPS, and clinical
  literature. Triggers: "clinical profile", "comorbidity rates", "disease
  prevalence for cohort", "severity distribution".
---

# Clinical Prevalence Profile Skill

## Overview

The clinical-prevalence-profile skill creates comprehensive clinical profiles for cohorts, including primary condition prevalence, comorbidity patterns, severity distributions, and medication expectations. It combines population health data with clinical evidence to produce realistic clinical cohort specifications.

**Primary Use Cases**:
- Define disease-specific cohorts
- Set comorbidity expectations
- Establish severity distributions
- Guide medication patterns

---

## Trigger Phrases

- "Clinical profile for [condition] patients"
- "Comorbidity rates for diabetics"
- "What conditions co-occur with heart failure?"
- "Severity distribution for [condition]"
- "Build clinical profile for [population]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `condition` | string | Yes | - | Primary condition (ICD-10 or name) |
| `geography` | string | No | "national" | Geographic scope |
| `age_range` | array | No | [18, 100] | Age filter |
| `include_medications` | bool | No | true | Include Rx patterns |
| `severity_detail` | bool | No | true | Include severity breakdown |

---

## Comorbidity Data Sources

| Source | Content | Use For |
|--------|---------|---------|
| CDC PLACES | Population prevalence | Geographic rates |
| MEPS | Healthcare utilization | Comorbidity pairs |
| CMS CCW | Medicare claims | 65+ populations |
| Clinical Literature | Evidence-based rates | Condition-specific |

---

## Major Condition Profiles

### Type 2 Diabetes (E11)

**Comorbidity Rates**:
| Condition | ICD-10 | Rate | Correlation |
|-----------|--------|------|-------------|
| Hypertension | I10 | 71% | High |
| Hyperlipidemia | E78.5 | 68% | High |
| Obesity | E66.9 | 62% | High |
| Depression | F32.9 | 28% | Moderate |
| CKD Stage 3+ | N18.3+ | 24% | High |
| CAD | I25.10 | 18% | Moderate |
| Neuropathy | G62.9 | 22% | High |
| Retinopathy | H35.0 | 16% | High |
| Heart Failure | I50.9 | 12% | Moderate |

**Severity Distribution**:
| Category | ICD-10 Codes | Rate |
|----------|--------------|------|
| Without complications | E11.9 | 35% |
| With kidney | E11.2x | 18% |
| With ophthalmic | E11.3x | 12% |
| With neurological | E11.4x | 16% |
| With peripheral | E11.5x | 8% |
| With multiple | E11.65 | 11% |

### Heart Failure (I50)

**Comorbidity Rates**:
| Condition | ICD-10 | Rate | Correlation |
|-----------|--------|------|-------------|
| Hypertension | I10 | 82% | High |
| CAD | I25.10 | 58% | High |
| Atrial Fibrillation | I48 | 42% | High |
| Diabetes | E11 | 38% | Moderate |
| CKD | N18 | 42% | High |
| COPD | J44 | 28% | Moderate |
| Anemia | D64.9 | 32% | Moderate |
| Depression | F32.9 | 24% | Moderate |

**Severity Distribution**:
| Type | ICD-10 | Rate |
|------|--------|------|
| HFrEF (reduced EF) | I50.2x | 45% |
| HFpEF (preserved EF) | I50.3x | 40% |
| Unspecified | I50.9 | 15% |

### COPD (J44)

**Comorbidity Rates**:
| Condition | ICD-10 | Rate | Correlation |
|-----------|--------|------|-------------|
| Hypertension | I10 | 52% | Moderate |
| Heart Failure | I50 | 22% | Moderate |
| CAD | I25.10 | 28% | Moderate |
| Diabetes | E11 | 18% | Low |
| Depression | F32.9 | 28% | Moderate |
| Anxiety | F41.1 | 32% | High |
| Osteoporosis | M81 | 18% | Moderate |
| Lung Cancer | C34 | 4% | High |

### Depression (F32)

**Comorbidity Rates**:
| Condition | ICD-10 | Rate | Correlation |
|-----------|--------|------|-------------|
| Anxiety | F41.1 | 62% | High |
| Chronic Pain | G89 | 38% | Moderate |
| Substance Use | F10-F19 | 24% | Moderate |
| Diabetes | E11 | 18% | Moderate |
| Hypertension | I10 | 32% | Low |
| Obesity | E66 | 28% | Moderate |
| Insomnia | G47.0 | 48% | High |

---

## Output Schema

```json
{
  "clinical_profile": {
    "cohort_context": {
      "geography": "Harris County, TX",
      "age_range": [40, 85],
      "population_type": "chronic_disease"
    },
    
    "primary_condition": {
      "code": "E11",
      "name": "Type 2 Diabetes Mellitus",
      "prevalence_in_cohort": 1.0,
      "prevalence_in_geography": 0.128,
      "affected_population": 412000
    },
    
    "severity_distribution": {
      "without_complications": {
        "codes": ["E11.9"],
        "rate": 0.35,
        "typical_a1c": "<7.5%"
      },
      "mild_complications": {
        "codes": ["E11.21", "E11.31", "E11.41"],
        "rate": 0.32,
        "typical_a1c": "7.5-8.5%"
      },
      "moderate_complications": {
        "codes": ["E11.22", "E11.32", "E11.42", "E11.51"],
        "rate": 0.22,
        "typical_a1c": "8.5-10%"
      },
      "severe_complications": {
        "codes": ["E11.65", "E11.52", "E11.69"],
        "rate": 0.11,
        "typical_a1c": ">10%"
      }
    },
    
    "comorbidities": {
      "I10": {
        "name": "Essential Hypertension",
        "rate": 0.71,
        "correlation": "high",
        "onset_pattern": "concurrent_or_prior"
      },
      "E78.5": {
        "name": "Hyperlipidemia, unspecified",
        "rate": 0.68,
        "correlation": "high",
        "onset_pattern": "concurrent"
      },
      "E66.9": {
        "name": "Obesity, unspecified",
        "rate": 0.62,
        "correlation": "high",
        "onset_pattern": "prior"
      },
      "F32.9": {
        "name": "Major depressive disorder",
        "rate": 0.28,
        "correlation": "moderate",
        "onset_pattern": "variable"
      },
      "N18.3": {
        "name": "CKD Stage 3",
        "rate": 0.18,
        "correlation": "high",
        "onset_pattern": "subsequent"
      }
    },
    
    "multimorbidity_distribution": {
      "primary_only": 0.08,
      "plus_1_comorbidity": 0.18,
      "plus_2_comorbidities": 0.28,
      "plus_3_comorbidities": 0.26,
      "plus_4_or_more": 0.20
    },
    
    "common_comorbidity_clusters": [
      {
        "name": "Metabolic Syndrome",
        "conditions": ["E11", "I10", "E78.5", "E66"],
        "prevalence": 0.42
      },
      {
        "name": "Cardiometabolic",
        "conditions": ["E11", "I10", "I25.10"],
        "prevalence": 0.18
      },
      {
        "name": "Diabetes with Complications",
        "conditions": ["E11.65", "N18.3", "H35.0"],
        "prevalence": 0.12
      }
    ],
    
    "medications": {
      "antidiabetics": {
        "metformin": 0.72,
        "sulfonylurea": 0.28,
        "sglt2_inhibitor": 0.22,
        "glp1_agonist": 0.18,
        "dpp4_inhibitor": 0.14,
        "insulin_any": 0.34
      },
      "cardiovascular": {
        "ace_arb": 0.68,
        "statin": 0.64,
        "beta_blocker": 0.32,
        "calcium_channel": 0.24,
        "diuretic": 0.28
      },
      "other": {
        "aspirin": 0.42,
        "antidepressant": 0.24,
        "ppi": 0.28
      },
      "polypharmacy": {
        "1_3_meds": 0.12,
        "4_6_meds": 0.28,
        "7_9_meds": 0.32,
        "10_plus": 0.28
      }
    },
    
    "lab_expectations": {
      "a1c": { "mean": 7.8, "std": 1.4, "range": [5.7, 14.0] },
      "fasting_glucose": { "mean": 142, "std": 42, "range": [70, 350] },
      "ldl": { "mean": 102, "std": 32, "range": [40, 220] },
      "egfr": { "mean": 72, "std": 24, "range": [15, 120] },
      "creatinine": { "mean": 1.2, "std": 0.4, "range": [0.6, 4.0] }
    }
  },
  
  "validation": {
    "sources": ["CDC_PLACES_2024", "MEPS_2021", "CMS_CCW", "ADA_Standards"],
    "confidence": "high"
  }
}
```

---

## Examples

### Example 1: Heart Failure Profile

**Request**: "Clinical profile for heart failure patients in Florida"

**Response**:

**Heart Failure Clinical Profile - Florida**

**Primary Condition**: I50 (Heart Failure)
- Prevalence in FL: 3.8% (age 45+)
- Affected population: ~820,000

**HF Type Distribution**:
| Type | Rate | Mean Age | Male % |
|------|------|----------|--------|
| HFrEF (I50.2x) | 45% | 68 | 58% |
| HFpEF (I50.3x) | 40% | 74 | 42% |
| Unspecified | 15% | 72 | 50% |

**Top Comorbidities**:
| Condition | Rate | Clinical Notes |
|-----------|------|----------------|
| Hypertension (I10) | 82% | Often causative |
| CAD (I25.10) | 58% | Ischemic etiology |
| AFib (I48) | 42% | Bidirectional relationship |
| CKD (N18) | 42% | Cardiorenal syndrome |
| Diabetes (E11) | 38% | Worsens prognosis |
| COPD (J44) | 28% | Complicates Dx |

**Medication Patterns**:
| Class | Rate | Key Drugs |
|-------|------|-----------|
| ACE/ARB/ARNI | 78% | Entresto, Lisinopril |
| Beta Blocker | 82% | Carvedilol, Metoprolol |
| Diuretic | 72% | Furosemide, Bumetanide |
| MRA | 42% | Spironolactone |
| SGLT2i | 28% | Dapagliflozin, Empagliflozin |
| Digoxin | 18% | Declining use |

---

### Example 2: COPD with Comorbidities

**Request**: "Comorbidity clustering for COPD patients"

**Response**:

**COPD Comorbidity Clusters**

**Cluster 1: Cardiovascular-Dominant (38%)**
```
COPD (J44) + HTN (I10) + CAD (I25) + HF (I50)
Mean age: 72, Male: 58%
High mortality risk
```

**Cluster 2: Metabolic (24%)**
```
COPD (J44) + DM (E11) + HTN (I10) + Obesity (E66)
Mean age: 64, Male: 48%
Moderate severity
```

**Cluster 3: Anxiety-Depression (22%)**
```
COPD (J44) + Anxiety (F41) + Depression (F32) + Insomnia (G47)
Mean age: 58, Female: 62%
Younger, worse QoL
```

**Cluster 4: Isolated COPD (16%)**
```
COPD (J44) minimal comorbidity
Mean age: 62, Male: 52%
Lower complexity
```

---

### Example 3: Pediatric Asthma

**Request**: "Clinical profile for pediatric asthma"

**Response**:

**Pediatric Asthma Clinical Profile**

**Primary Condition**: J45 (Asthma)
- Prevalence (0-17): 8.4%
- Peak prevalence age: 5-11 years

**Severity Distribution**:
| Severity | ICD-10 | Rate | Controller Need |
|----------|--------|------|-----------------|
| Intermittent | J45.20 | 42% | PRN only |
| Mild Persistent | J45.30 | 28% | Low-dose ICS |
| Moderate Persistent | J45.40 | 22% | Medium ICS |
| Severe Persistent | J45.50 | 8% | High ICS + add-on |

**Comorbidities**:
| Condition | Rate | Notes |
|-----------|------|-------|
| Allergic Rhinitis (J30) | 62% | Atopic march |
| Eczema (L20) | 28% | Atopic triad |
| Food Allergy (T78.1) | 14% | Elevated risk |
| Obesity (E66) | 22% | Worsens control |
| GERD (K21) | 12% | Trigger |

**Medications**:
| Class | Rate |
|-------|------|
| SABA (albuterol) | 95% |
| ICS | 58% |
| ICS/LABA combo | 22% |
| LTRA (montelukast) | 32% |
| Biologics | 4% |

---

## Validation Rules

### Rate Checks
- [ ] All rates between 0 and 1
- [ ] Comorbidity rates clinically plausible
- [ ] Severity distribution sums to ~1.0

### Consistency Checks
- [ ] Medications match conditions
- [ ] Lab ranges appropriate for condition
- [ ] Age patterns match epidemiology

---

## Related Skills

- [cohort-specification.md](cohort-specification.md) - Full cohort
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Population rates
- [health-outcome-disparities.md](../health-patterns/health-outcome-disparities.md) - Demographic variation
