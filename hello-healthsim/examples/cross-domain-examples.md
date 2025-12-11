# Cross-Domain Examples

Generate data that spans multiple HealthSim products for realistic end-to-end scenarios.

---

## Example 1: Patient with Medical and Pharmacy Claims

### Prompt
```
Generate a diabetic patient with their recent office visit claim and pharmacy claim for metformin
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "member_id": "MEM001234",
    "name": { "given_name": "Maria", "family_name": "Santos" },
    "birth_date": "1968-05-22",
    "gender": "F"
  },
  "clinical_data": {
    "diagnoses": [
      { "code": "E11.9", "description": "Type 2 diabetes mellitus without complications" },
      { "code": "I10", "description": "Essential hypertension" },
      { "code": "E78.5", "description": "Hyperlipidemia" }
    ],
    "medications": [
      { "name": "Metformin", "dose": "1000 mg", "frequency": "BID" },
      { "name": "Lisinopril", "dose": "20 mg", "frequency": "QD" },
      { "name": "Atorvastatin", "dose": "20 mg", "frequency": "QD" }
    ],
    "recent_labs": [
      { "test": "HbA1c", "value": "7.4", "unit": "%", "date": "2025-01-15" },
      { "test": "Creatinine", "value": "0.9", "unit": "mg/dL", "date": "2025-01-15" }
    ]
  },
  "professional_claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "E11.9",
    "other_diagnoses": ["I10", "E78.5"],
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "description": "Office visit, established, moderate complexity",
        "charge_amount": 175.00
      },
      {
        "line_number": 2,
        "procedure_code": "36415",
        "description": "Venipuncture",
        "charge_amount": 15.00
      }
    ],
    "total_charges": 190.00,
    "adjudication": {
      "status": "paid",
      "allowed_amount": 138.00,
      "copay": 30.00,
      "paid_amount": 108.00
    }
  },
  "pharmacy_claims": [
    {
      "claim_id": "RX20250115000001",
      "member_id": "MEM001234",
      "service_date": "2025-01-15",
      "ndc": "00093101901",
      "drug_name": "Metformin 1000mg Tablet",
      "quantity": 60,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00,
        "plan_paid": 5.50
      }
    },
    {
      "claim_id": "RX20250115000002",
      "member_id": "MEM001234",
      "service_date": "2025-01-15",
      "ndc": "00093505601",
      "drug_name": "Lisinopril 20mg Tablet",
      "quantity": 30,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00,
        "plan_paid": 3.00
      }
    },
    {
      "claim_id": "RX20250115000003",
      "member_id": "MEM001234",
      "service_date": "2025-01-15",
      "ndc": "00071015523",
      "drug_name": "Atorvastatin 20mg Tablet",
      "quantity": 30,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00,
        "plan_paid": 4.50
      }
    }
  ],
  "consistency_check": {
    "member_id_match": true,
    "diagnoses_match": true,
    "medications_to_rx_match": true,
    "service_dates_aligned": true
  }
}
```

### Key Points
- Same `member_id` across all claims
- Clinical diagnoses match claim diagnoses
- Medications in clinical data have corresponding pharmacy claims
- Quantity 60 for metformin = BID dosing for 30 days

---

## Example 2: Hospitalization with Follow-Up

### Prompt
```
Generate a heart failure patient with inpatient admission, follow-up visit, and related pharmacy claims
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000002",
    "member_id": "MEM002345",
    "name": { "given_name": "James", "family_name": "Wilson" },
    "birth_date": "1952-11-08",
    "gender": "M"
  },
  "episode_timeline": [
    { "event": "Admission", "date": "2025-01-05" },
    { "event": "Discharge", "date": "2025-01-09" },
    { "event": "Follow-up Visit", "date": "2025-01-16" },
    { "event": "Medication Fills", "date": "2025-01-09" }
  ],
  "facility_claim": {
    "claim_id": "CLM20250109000001",
    "claim_type": "INSTITUTIONAL",
    "bill_type": "111",
    "member_id": "MEM002345",
    "admit_date": "2025-01-05",
    "discharge_date": "2025-01-09",
    "length_of_stay": 4,
    "principal_diagnosis": "I50.23",
    "drg": {
      "code": "291",
      "description": "Heart Failure and Shock with MCC"
    },
    "total_charges": 28500.00,
    "adjudication": {
      "status": "paid",
      "drg_payment": 12500.00,
      "deductible": 500.00,
      "coinsurance": 2400.00,
      "paid_amount": 9600.00
    }
  },
  "follow_up_claim": {
    "claim_id": "CLM20250116000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM002345",
    "service_date": "2025-01-16",
    "place_of_service": "11",
    "principal_diagnosis": "I50.23",
    "claim_lines": [
      {
        "procedure_code": "99215",
        "description": "Post-discharge follow-up, high complexity",
        "charge_amount": 225.00
      }
    ],
    "adjudication": {
      "status": "paid",
      "allowed_amount": 165.00,
      "copay": 40.00,
      "paid_amount": 125.00
    }
  },
  "pharmacy_claims": [
    {
      "claim_id": "RX20250109000001",
      "service_date": "2025-01-09",
      "ndc": "00078060061",
      "drug_name": "Entresto 97/103mg Tablet",
      "quantity": 60,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 3,
        "patient_pay": 75.00,
        "note": "New start at discharge"
      }
    },
    {
      "claim_id": "RX20250109000002",
      "service_date": "2025-01-09",
      "ndc": "00378395201",
      "drug_name": "Carvedilol 25mg Tablet",
      "quantity": 60,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00
      }
    },
    {
      "claim_id": "RX20250109000003",
      "service_date": "2025-01-09",
      "ndc": "00591555601",
      "drug_name": "Furosemide 40mg Tablet",
      "quantity": 60,
      "days_supply": 30,
      "response": {
        "status": "paid",
        "tier": 1,
        "patient_pay": 10.00
      }
    }
  ],
  "quality_measures": {
    "transition_of_care": {
      "follow_up_within_7_days": true,
      "medication_reconciliation": true,
      "discharge_instructions_provided": true
    }
  }
}
```

### Key Points
- Timeline shows logical sequence
- Follow-up within 7 days (quality measure)
- Discharge medications align with GDMT for HF
- Entresto (brand) on Tier 3 with higher copay
- DRG 291 matches principal diagnosis

---

## Example 3: Prior Auth Flow

### Prompt
```
Generate a complete prior authorization flow: initial denial, PA submission, approval, and successful fill
```

### Expected Output
```json
{
  "member": {
    "member_id": "MEM003456",
    "name": { "given_name": "Lisa", "family_name": "Chen" },
    "plan_code": "HMO-STANDARD"
  },
  "prior_auth_timeline": [
    { "event": "Initial claim rejected", "date": "2025-01-10" },
    { "event": "PA submitted", "date": "2025-01-10" },
    { "event": "PA approved", "date": "2025-01-13" },
    { "event": "Claim approved", "date": "2025-01-13" }
  ],
  "initial_rejection": {
    "claim_id": "RX20250110000001",
    "service_date": "2025-01-10",
    "ndc": "00002140280",
    "drug_name": "Trulicity 1.5mg Pen",
    "response": {
      "status": "rejected",
      "reject_code": "75",
      "reject_message": "Prior Authorization Required"
    }
  },
  "prior_auth_request": {
    "pa_id": "PA20250110000001",
    "request_date": "2025-01-10",
    "drug_name": "Trulicity 1.5mg",
    "ndc": "00002140280",
    "diagnosis": "E11.65",
    "clinical_information": {
      "current_medications": ["Metformin 1000mg BID"],
      "a1c_value": "8.9%",
      "a1c_date": "2025-01-05",
      "metformin_trial_duration": "6 months",
      "contraindications": "None",
      "prescriber_rationale": "A1C not at goal despite maximum metformin. GLP-1 RA preferred for cardiovascular benefit."
    },
    "submission_method": "ePA"
  },
  "prior_auth_decision": {
    "pa_id": "PA20250110000001",
    "decision_date": "2025-01-13",
    "status": "approved",
    "approval_details": {
      "effective_date": "2025-01-13",
      "expiration_date": "2026-01-13",
      "approved_quantity": "4 pens per 28 days",
      "override_code": "08",
      "auth_number": "AUTH20250113001"
    }
  },
  "successful_claim": {
    "claim_id": "RX20250113000001",
    "service_date": "2025-01-13",
    "ndc": "00002140280",
    "drug_name": "Trulicity 1.5mg Pen",
    "quantity": 4,
    "days_supply": 28,
    "prior_auth_number": "AUTH20250113001",
    "response": {
      "status": "paid",
      "ingredient_cost_paid": 875.00,
      "patient_pay_amount": 125.00,
      "tier": 4,
      "message": "Prior authorization on file"
    }
  }
}
```

### Key Points
- Complete PA workflow from rejection to approval
- Clinical information justifies approval
- Override code 08 = Prior authorization on file
- PA auth number links rejection to approval
- 1-year approval typical for chronic medications

---

## Example 4: Value-Based Care Report

### Prompt
```
Generate a diabetic patient with quality measure compliance status and care gaps
```

### Expected Output
```json
{
  "patient": {
    "member_id": "MEM004567",
    "name": { "given_name": "Robert", "family_name": "Martinez" },
    "birth_date": "1960-03-15",
    "gender": "M",
    "pcp_npi": "1234567890",
    "attributed_provider": "Dr. Sarah Johnson"
  },
  "clinical_summary": {
    "diagnoses": [
      { "code": "E11.65", "description": "Type 2 diabetes with hyperglycemia" },
      { "code": "I10", "description": "Essential hypertension" },
      { "code": "E78.5", "description": "Hyperlipidemia" }
    ],
    "most_recent_labs": {
      "a1c": { "value": "7.8", "date": "2024-11-20" },
      "ldl": { "value": "118", "date": "2024-11-20" },
      "creatinine": { "value": "1.1", "date": "2024-11-20" }
    },
    "most_recent_vitals": {
      "blood_pressure": "142/88",
      "date": "2024-12-15"
    }
  },
  "quality_measures": {
    "measurement_year": 2025,
    "applicable_measures": [
      {
        "measure_id": "CDC-HBD",
        "measure_name": "Hemoglobin A1c Control for Patients with Diabetes",
        "target": "A1C < 8.0%",
        "status": "compliant",
        "evidence": { "a1c": "7.8%", "date": "2024-11-20" }
      },
      {
        "measure_id": "CDC-BPD",
        "measure_name": "Blood Pressure Control for Patients with Diabetes",
        "target": "BP < 140/90",
        "status": "non_compliant",
        "evidence": { "bp": "142/88", "date": "2024-12-15" },
        "care_gap": true
      },
      {
        "measure_id": "CDC-EYE",
        "measure_name": "Eye Exam for Patients with Diabetes",
        "target": "Retinal exam in measurement year",
        "status": "non_compliant",
        "last_exam": "2023-02-10",
        "care_gap": true
      },
      {
        "measure_id": "SPD",
        "measure_name": "Statin Therapy for Patients with Diabetes",
        "target": "On statin therapy",
        "status": "compliant",
        "evidence": { "medication": "Atorvastatin 40mg", "active": true }
      }
    ]
  },
  "care_gaps": [
    {
      "gap": "Blood Pressure Control",
      "recommendation": "Schedule follow-up to address BP. Consider medication adjustment.",
      "priority": "high"
    },
    {
      "gap": "Diabetic Eye Exam",
      "recommendation": "Refer to ophthalmology for dilated retinal exam",
      "priority": "high",
      "overdue_by": "23 months"
    }
  ],
  "risk_score": {
    "hcc_categories": [
      { "hcc": 19, "description": "Diabetes with Complications", "source": "E11.65" }
    ],
    "raf_score": 1.125,
    "risk_level": "moderate"
  }
}
```

### Key Points
- Quality measures match actual HEDIS specs
- Care gaps identified with actionable recommendations
- HCC risk score for payment adjustment
- Combines clinical data with payer quality program

---

## Example 5: Oncology Patient Journey

### Prompt
```
Generate a breast cancer patient with clinical data, facility infusion claim, and oral chemotherapy pharmacy claim
```

### Expected Output
```json
{
  "patient": {
    "mrn": "MRN00000005",
    "member_id": "MEM005678",
    "name": { "given_name": "Jennifer", "family_name": "Thompson" },
    "birth_date": "1968-04-12",
    "gender": "F"
  },
  "clinical_data": {
    "cancer_diagnosis": {
      "code": "C50.911",
      "description": "Malignant neoplasm of unspecified site of right female breast",
      "diagnosed_date": "2024-10-15"
    },
    "staging": {
      "tnm": { "t": "T2", "n": "N1", "m": "M0" },
      "ajcc_stage": "IIB",
      "stage_date": "2024-10-20"
    },
    "biomarkers": {
      "er_status": "positive",
      "er_percent": 85,
      "pr_status": "positive",
      "pr_percent": 60,
      "her2_status": "negative",
      "her2_score": "1+",
      "ki67_percent": 18
    },
    "treatment_plan": {
      "surgery": { "type": "Lumpectomy", "date": "2024-11-01" },
      "chemotherapy": "TC (Docetaxel + Cyclophosphamide)",
      "radiation": "Whole breast radiation planned",
      "hormonal_therapy": "Anastrozole planned post-chemo"
    }
  },
  "facility_claim": {
    "claim_id": "CLM20250115000005",
    "claim_type": "INSTITUTIONAL",
    "facility_type": "outpatient_hospital",
    "member_id": "MEM005678",
    "service_date": "2025-01-15",
    "principal_diagnosis": "C50.911",
    "claim_lines": [
      {
        "line_number": 1,
        "revenue_code": "0335",
        "procedure_code": "96413",
        "hcpcs_code": "J9171",
        "description": "Docetaxel injection, 1mg",
        "units": 120,
        "charge_amount": 4800.00
      },
      {
        "line_number": 2,
        "revenue_code": "0335",
        "procedure_code": "96415",
        "description": "Chemotherapy infusion, additional hour",
        "units": 1,
        "charge_amount": 250.00
      },
      {
        "line_number": 3,
        "revenue_code": "0250",
        "hcpcs_code": "J2405",
        "description": "Ondansetron injection (antiemetic)",
        "units": 8,
        "charge_amount": 120.00
      }
    ],
    "prior_auth": {
      "auth_number": "PA20241101-54321",
      "status": "approved"
    },
    "adjudication": {
      "status": "paid",
      "allowed_amount": 4200.00,
      "deductible": 0.00,
      "coinsurance": 840.00,
      "paid_amount": 3360.00
    }
  },
  "pharmacy_claim": {
    "claim_id": "RX20250115000005",
    "member_id": "MEM005678",
    "service_date": "2025-01-15",
    "ndc": "00310075090",
    "drug_name": "Anastrozole 1mg Tablet",
    "quantity": 30,
    "days_supply": 30,
    "prescriber_npi": "1234567890",
    "pharmacy_type": "retail",
    "response": {
      "status": "paid",
      "tier": 2,
      "patient_pay": 15.00,
      "plan_paid": 42.00,
      "note": "Hormonal therapy for ER+ breast cancer"
    }
  },
  "care_coordination": {
    "oncologist": "Dr. Michael Rodriguez",
    "treatment_center": "Regional Cancer Center",
    "next_infusion": "2025-02-05",
    "labs_due": "2025-01-29"
  },
  "consistency_check": {
    "diagnosis_code_match": true,
    "treatment_matches_biomarkers": true,
    "prior_auth_on_file": true,
    "hormonal_therapy_appropriate": true
  }
}
```

### Key Points

- Clinical staging (T2 N1 M0 = Stage IIB) matches treatment intensity
- Biomarkers (ER+, PR+, HER2-) justify hormonal therapy selection
- Docetaxel J-code (J9171) with revenue code 0335 (chemotherapy)
- Anastrozole (hormonal therapy) matches ER-positive status
- Prior authorization required for infusion chemotherapy
- Cross-product consistency: clinical → facility claim → pharmacy claim

---

## More Examples

These cross-domain examples show how HealthSim maintains consistency across products. Use them as templates for your own complex scenarios.

See also:
- [Format Examples](format-examples.md) - Transform cross-domain data to standards
- [Oncology Examples](oncology-examples.md) - Detailed oncology patient scenarios
