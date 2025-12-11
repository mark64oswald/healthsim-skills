---
name: healthsim-patientsim
description: "Generate realistic clinical patient data including demographics, encounters, diagnoses, medications, labs, and vitals. Use when user requests: (1) patient records or clinical data, (2) EMR test data, (3) specific clinical scenarios like diabetes or heart failure, (4) HL7v2 or FHIR patient resources."
---

# PatientSim - Clinical Patient Data Generation

## Overview

PatientSim generates realistic synthetic clinical data for EMR/EHR testing, including:
- Patient demographics
- Encounters (inpatient, outpatient, emergency, observation)
- Diagnoses (ICD-10-CM)
- Procedures (CPT, ICD-10-PCS)
- Medications (with RxNorm codes)
- Lab results (with LOINC codes)
- Vital signs

## Quick Start

### Simple Patient

**Request:** "Generate a patient"

```json
{
  "mrn": "MRN00000001",
  "name": { "given_name": "John", "family_name": "Smith" },
  "birth_date": "1975-03-15",
  "gender": "M",
  "address": {
    "street_address": "123 Main Street",
    "city": "Springfield",
    "state": "IL",
    "postal_code": "62701"
  }
}
```

### Clinical Scenario

**Request:** "Generate a diabetic patient with complications"

Claude loads [diabetes-management.md](diabetes-management.md) and produces a complete clinical picture.

## Scenario Skills

Load the appropriate scenario based on user request:

| Scenario | Trigger Phrases | File |
|----------|-----------------|------|
| **ADT Workflow** | admission, discharge, transfer, ADT, patient movement | [adt-workflow.md](adt-workflow.md) |
| **Diabetes Management** | diabetes, A1C, glucose, metformin, insulin | [diabetes-management.md](diabetes-management.md) |
| **Heart Failure** | CHF, HFrEF, HFpEF, BNP, ejection fraction | [heart-failure.md](heart-failure.md) |
| **Chronic Kidney Disease** | CKD, eGFR, dialysis, nephropathy | [chronic-kidney-disease.md](chronic-kidney-disease.md) |
| **Sepsis/Acute Care** | sepsis, infection, ICU, critical care | [sepsis-acute-care.md](sepsis-acute-care.md) |
| **Orders & Results** | lab order, radiology, ORM, ORU, results | [orders-results.md](orders-results.md) |
| **Oncology** | | |
| ↳ Breast Cancer | breast cancer, mastectomy, ER positive, HER2, tamoxifen | [oncology/breast-cancer.md](oncology/breast-cancer.md) |
| ↳ Lung Cancer | lung cancer, NSCLC, EGFR, ALK, immunotherapy | [oncology/lung-cancer.md](oncology/lung-cancer.md) |
| ↳ Colorectal Cancer | colon cancer, rectal cancer, FOLFOX, colonoscopy | [oncology/colorectal-cancer.md](oncology/colorectal-cancer.md) |
| ↳ Oncology Domain | oncology, cancer staging, chemotherapy, tumor markers | [oncology/oncology-domain.md](oncology/oncology-domain.md) |

## Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| age | int or range | 18-90 | Patient age or range |
| gender | M/F/O/U | weighted | M=49%, F=51% |
| conditions | list | none | Specific diagnoses to include |
| severity | string | moderate | mild, moderate, severe |
| encounters | int | 1 | Number of encounters to generate |
| timeline | string | 1 year | How far back to generate history |

## Output Entities

### Patient
Demographics extending the Person model with MRN.

### Encounter
Clinical visit with class (I/O/E/U/OBS), timing, location, providers.

### Diagnosis
ICD-10-CM code with type (admitting, working, final), dates.

### Medication
Drug with RxNorm code, dose, route, frequency, status.

### LabResult
Test with LOINC code, value, units, reference range, abnormal flag.

### VitalSign
Observation with temperature, HR, RR, BP, SpO2, height, weight.

See [data-models.md](../../references/data-models.md) for complete schemas.

## Clinical Coherence Rules

PatientSim ensures generated data is clinically realistic:

1. **Age-appropriate conditions**: No pediatric conditions in adults, geriatric conditions require appropriate age
2. **Gender-appropriate conditions**: Prostate conditions for males only, pregnancy for females only
3. **Medication indications**: Drugs match diagnoses (metformin requires diabetes)
4. **Lab coherence**: Values align with conditions (elevated A1C with diabetes)
5. **Temporal consistency**: Diagnoses before treatments, labs after orders

See [validation-rules.md](../../references/validation-rules.md) for complete rules.

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| FHIR R4 | "as FHIR", "FHIR bundle" | Interoperability |
| HL7v2 ADT | "as HL7", "ADT message" | Legacy EMR |
| CSV | "as CSV" | Analytics |

## Examples

### Example 1: Basic Patient with Encounter

**Request:** "Generate a 45-year-old male with an office visit for hypertension"

**Output:**
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Michael", "family_name": "Johnson" },
    "birth_date": "1980-06-22",
    "gender": "M"
  },
  "encounter": {
    "encounter_id": "ENC0000000001",
    "patient_mrn": "MRN00000001",
    "class_code": "O",
    "status": "finished",
    "admission_time": "2025-01-15T09:30:00",
    "discharge_time": "2025-01-15T10:00:00",
    "chief_complaint": "Blood pressure follow-up"
  },
  "diagnoses": [
    {
      "code": "I10",
      "description": "Essential hypertension",
      "type": "final",
      "diagnosed_date": "2024-06-15"
    }
  ],
  "medications": [
    {
      "name": "Lisinopril",
      "code": "104376",
      "dose": "10 mg",
      "route": "PO",
      "frequency": "QD",
      "status": "active"
    }
  ],
  "vitals": {
    "observation_time": "2025-01-15T09:35:00",
    "systolic_bp": 138,
    "diastolic_bp": 88,
    "heart_rate": 72,
    "temperature": 98.4,
    "spo2": 98
  }
}
```

### Example 2: Complex Multi-Condition Patient

**Request:** "Generate a 68-year-old female with diabetes, hypertension, and CKD stage 3"

Claude combines patterns from multiple scenario skills to generate a coherent patient with:
- Multiple chronic diagnoses with appropriate onset dates
- Medications for each condition (metformin, lisinopril, etc.)
- Quarterly encounters over 2 years
- Labs showing disease progression (A1C, eGFR trends)
- Comorbidity interactions (CKD affecting medication choices)

## Related Skills

### Chronic Disease
- [diabetes-management.md](diabetes-management.md) - Diabetes scenarios
- [heart-failure.md](heart-failure.md) - Heart failure scenarios
- [chronic-kidney-disease.md](chronic-kidney-disease.md) - CKD scenarios

### Acute Care
- [adt-workflow.md](adt-workflow.md) - ADT workflow scenarios
- [sepsis-acute-care.md](sepsis-acute-care.md) - Acute care scenarios
- [orders-results.md](orders-results.md) - Orders and results

### Oncology
- [oncology/oncology-domain.md](oncology/oncology-domain.md) - Foundational oncology knowledge
- [oncology/breast-cancer.md](oncology/breast-cancer.md) - Breast cancer scenarios
- [oncology/lung-cancer.md](oncology/lung-cancer.md) - Lung cancer scenarios (NSCLC/SCLC)
- [oncology/colorectal-cancer.md](oncology/colorectal-cancer.md) - Colorectal cancer scenarios

### Output Formats
- [../../formats/fhir-r4.md](../../formats/fhir-r4.md) - FHIR transformation
- [../../formats/hl7v2-adt.md](../../formats/hl7v2-adt.md) - HL7v2 ADT messages
- [../../formats/hl7v2-orm.md](../../formats/hl7v2-orm.md) - HL7v2 Order messages
- [../../formats/hl7v2-oru.md](../../formats/hl7v2-oru.md) - HL7v2 Results messages

### Reference Data
- [../../references/oncology/](../../references/oncology/) - Oncology codes, medications, regimens
