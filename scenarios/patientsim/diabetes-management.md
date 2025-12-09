# Diabetes Management Scenario

## Trigger Phrases

- diabetic patient
- diabetes
- T2DM
- Type 2 diabetes
- A1C
- blood sugar
- metformin
- insulin
- hyperglycemia
- glucose control

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| age_range | range | 45-75 | Any valid adult range |
| control_status | string | moderate | well-controlled, moderate, poorly-controlled |
| duration_years | range | 0-20 | Years since diagnosis |
| complications | list | none | nephropathy, retinopathy, neuropathy, cardiovascular |

## Disease Progression Stages

### Stage 1: Pre-diabetes
- **A1C Range**: 5.7% - 6.4%
- **Duration**: 1-5 years without intervention
- **Codes**: R73.03 (Prediabetes)
- **Medications**: Lifestyle modification only

### Stage 2: New Diagnosis
- **A1C Range**: 6.5% - 8.5%
- **Codes**: E11.9 (Type 2 diabetes without complications)
- **Medications**: Metformin 500mg BID, titrate to 1000mg BID
- **Initial Labs**: A1C, CMP, lipid panel, UA with microalbumin
- **Follow-up**: 2 weeks phone, 4-6 weeks office, then q3 months

### Stage 3: Early Management (0-3 years)
- **A1C Target**: < 7.0%
- **Medications**: Metformin + possible second agent
- **Monitoring**: A1C every 3 months until stable, then every 6 months

### Stage 4: Medication Escalation (3-10 years)
- **A1C Range**: Variable, may be above target
- **Add Medications**:
  - SGLT2 inhibitors (empagliflozin, dapagliflozin)
  - GLP-1 receptor agonists (semaglutide, dulaglutide)
  - DPP-4 inhibitors (sitagliptin, linagliptin)
- **Considerations**: Cardiovascular or renal benefit preferred agents

### Stage 5: Complex Regimens (10+ years)
- **Insulin Required**: Basal insulin (glargine, degludec)
- **Possible Addition**: Bolus insulin for meals
- **A1C Target**: May relax to < 8.0% in elderly
- **Higher Complication Rate**: Check for nephropathy, retinopathy

## Comorbidities

| Comorbidity | Probability | ICD-10 Codes | Notes |
|-------------|-------------|--------------|-------|
| Hypertension | 75% | I10, I11.9 | Nearly universal in T2DM |
| Hyperlipidemia | 70% | E78.5, E78.0 | Statin therapy indicated |
| Obesity | 85% | E66.9, E66.01 | BMI > 30 common |
| CKD Stage 3+ | 40% | N18.3, N18.4 | Increases with duration > 10 years |
| CAD | 30% | I25.10 | Major cause of mortality |
| Retinopathy | 25% | E11.3x | Annual eye exams required |
| Neuropathy | 35% | E11.4x | Check monofilament yearly |

## Lab Patterns by Control Status

### Well-Controlled
```json
{
  "a1c": { "min": 6.0, "max": 7.0, "flag": null },
  "fasting_glucose": { "min": 80, "max": 120, "flag": null },
  "creatinine": { "min": 0.8, "max": 1.2, "flag": null },
  "egfr": { "min": 60, "max": 120, "flag": null },
  "urine_microalbumin": { "min": 0, "max": 30, "flag": null }
}
```

### Moderate Control
```json
{
  "a1c": { "min": 7.0, "max": 8.5, "flag": "H" },
  "fasting_glucose": { "min": 120, "max": 180, "flag": "H" },
  "creatinine": { "min": 1.0, "max": 1.5, "flag": null },
  "egfr": { "min": 45, "max": 90, "flag": null },
  "urine_microalbumin": { "min": 30, "max": 300, "flag": "H" }
}
```

### Poorly Controlled
```json
{
  "a1c": { "min": 8.5, "max": 12.0, "flag": "H" },
  "fasting_glucose": { "min": 180, "max": 350, "flag": "HH" },
  "creatinine": { "min": 1.3, "max": 2.5, "flag": "H" },
  "egfr": { "min": 30, "max": 60, "flag": "L" },
  "urine_microalbumin": { "min": 300, "max": 3000, "flag": "HH" }
}
```

## Medication Patterns

### First-Line Therapy
```json
{
  "name": "Metformin",
  "code": "860975",
  "dose": "1000 mg",
  "route": "PO",
  "frequency": "BID",
  "indication": "E11.9"
}
```

### Add-On Therapies (by priority)

1. **SGLT2 Inhibitor** (if CKD or CVD risk)
```json
{
  "name": "Empagliflozin",
  "code": "1545653",
  "dose": "10 mg",
  "route": "PO",
  "frequency": "QD",
  "indication": "E11.65"
}
```

2. **GLP-1 Receptor Agonist** (if weight loss desired)
```json
{
  "name": "Semaglutide",
  "code": "1991302",
  "dose": "0.5 mg",
  "route": "SubQ",
  "frequency": "Weekly",
  "indication": "E11.65"
}
```

3. **Basal Insulin** (if A1C > 10% or significant hyperglycemia)
```json
{
  "name": "Insulin Glargine",
  "code": "274783",
  "dose": "10 units",
  "route": "SubQ",
  "frequency": "QHS",
  "indication": "E11.65"
}
```

## Encounter Patterns

### Routine Follow-Up
- **Frequency**: Every 3-6 months
- **CPT Code**: 99213 or 99214
- **Labs**: A1C, BMP
- **Class Code**: O (Outpatient)

### New Diagnosis Visit
- **CPT Code**: 99215 or 99205
- **Labs**: A1C, CMP, lipid panel, UA with microalbumin, TSH
- **Education**: Diabetes self-management, nutrition referral
- **Follow-up Schedule**:
  - Phone check at 2 weeks
  - Office visit at 4-6 weeks
  - Quarterly thereafter

### Annual Comprehensive Visit
- **CPT Code**: 99214 or 99215
- **Labs**: A1C, CMP, lipid panel, UA with microalbumin
- **Referrals**: Ophthalmology (dilated eye exam), Podiatry (foot exam)
- **Screenings**: Depression (PHQ-9), foot monofilament exam

## Example Output

### Poorly Controlled Type 2 Diabetes with Complications

```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Robert", "family_name": "Martinez" },
    "birth_date": "1960-04-12",
    "gender": "M"
  },
  "diagnoses": [
    { "code": "E11.65", "description": "Type 2 diabetes with hyperglycemia", "diagnosed_date": "2015-03-20" },
    { "code": "E11.22", "description": "Type 2 diabetes with diabetic CKD", "diagnosed_date": "2022-08-15" },
    { "code": "I10", "description": "Essential hypertension", "diagnosed_date": "2014-11-10" },
    { "code": "E78.5", "description": "Hyperlipidemia", "diagnosed_date": "2015-06-22" },
    { "code": "N18.3", "description": "Chronic kidney disease, stage 3", "diagnosed_date": "2022-08-15" }
  ],
  "medications": [
    { "name": "Metformin", "dose": "1000 mg", "frequency": "BID", "status": "active" },
    { "name": "Empagliflozin", "dose": "10 mg", "frequency": "QD", "status": "active" },
    { "name": "Insulin Glargine", "dose": "30 units", "frequency": "QHS", "status": "active" },
    { "name": "Lisinopril", "dose": "20 mg", "frequency": "QD", "status": "active" },
    { "name": "Atorvastatin", "dose": "40 mg", "frequency": "QHS", "status": "active" }
  ],
  "labs": [
    { "test_name": "HbA1c", "loinc_code": "4548-4", "value": "9.2", "unit": "%", "flag": "H" },
    { "test_name": "Glucose", "loinc_code": "2345-7", "value": "215", "unit": "mg/dL", "flag": "H" },
    { "test_name": "Creatinine", "loinc_code": "2160-0", "value": "1.6", "unit": "mg/dL", "flag": "H" },
    { "test_name": "eGFR", "loinc_code": "48642-3", "value": "48", "unit": "mL/min/1.73m2", "flag": "L" },
    { "test_name": "Urine Microalbumin", "loinc_code": "14957-5", "value": "180", "unit": "mg/L", "flag": "H" }
  ],
  "encounter": {
    "class_code": "O",
    "chief_complaint": "Diabetes follow-up, A1C elevated",
    "admission_time": "2025-01-15T09:00:00"
  }
}
```

## Related Skills

- [SKILL.md](SKILL.md) - PatientSim overview
- [chronic-kidney-disease.md](chronic-kidney-disease.md) - CKD scenarios (common comorbidity)
- [heart-failure.md](heart-failure.md) - Heart failure scenarios
- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - ICD-10, LOINC codes
