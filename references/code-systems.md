# Code Systems Reference

Standard medical codes for generating realistic healthcare data.

## Table of Contents

- [Code System URIs](#code-system-uris)
- [ICD-10-CM Diagnosis Codes](#icd-10-cm-diagnosis-codes)
- [CPT Procedure Codes](#cpt-procedure-codes)
- [LOINC Lab Codes](#loinc-lab-codes)
- [Medication Reference Data](#medication-reference-data)
- [Place of Service Codes](#place-of-service-codes)
- [Revenue Codes](#revenue-codes)
- [Modifier Codes](#modifier-codes)
- [Plan and Benefit Codes](#plan-and-benefit-codes)

---

## Code System URIs

| System | URI | Version Pattern |
|--------|-----|-----------------|
| ICD-10-CM | `http://hl7.org/fhir/sid/icd-10-cm` | FY{YYYY} |
| ICD-10-PCS | `http://hl7.org/fhir/sid/icd-10-pcs` | FY{YYYY} |
| CPT | `http://www.ama-assn.org/go/cpt` | {YYYY} |
| HCPCS | `http://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets` | {YYYY} |
| LOINC | `http://loinc.org` | 2.x |
| RxNorm | `http://www.nlm.nih.gov/research/umls/rxnorm` | {YYYYMMDD} |
| NDC | `http://hl7.org/fhir/sid/ndc` | - |
| SNOMED CT | `http://snomed.info/sct` | US Edition |
| CVX | `http://hl7.org/fhir/sid/cvx` | - |

---

## ICD-10-CM Diagnosis Codes

### Endocrine/Metabolic (E00-E89)

| Code | Display | Category | Age | Gender |
|------|---------|----------|-----|--------|
| E08.9 | Diabetes due to underlying condition | DM Secondary | Any | Any |
| E10.9 | Type 1 diabetes without complications | DM Type 1 | Any | Any |
| E10.65 | Type 1 diabetes with hyperglycemia | DM Type 1 | Any | Any |
| E11.9 | Type 2 diabetes without complications | DM Type 2 | 10+ | Any |
| E11.21 | Type 2 diabetes with diabetic nephropathy | DM Type 2 | 18+ | Any |
| E11.22 | Type 2 diabetes with diabetic CKD | DM Type 2 | 18+ | Any |
| E11.40 | Type 2 diabetes with diabetic neuropathy | DM Type 2 | 18+ | Any |
| E11.65 | Type 2 diabetes with hyperglycemia | DM Type 2 | 10+ | Any |
| E66.01 | Morbid obesity due to excess calories | Obesity | Any | Any |
| E66.9 | Obesity, unspecified | Obesity | Any | Any |
| E78.00 | Pure hypercholesterolemia, unspecified | Lipids | 18+ | Any |
| E78.1 | Pure hyperglyceridemia | Lipids | 18+ | Any |
| E78.2 | Mixed hyperlipidemia | Lipids | 18+ | Any |
| E78.5 | Hyperlipidemia, unspecified | Lipids | 18+ | Any |
| E03.9 | Hypothyroidism, unspecified | Thyroid | Any | Any |
| E05.90 | Thyrotoxicosis, unspecified | Thyroid | Any | Any |

### Cardiovascular (I00-I99)

| Code | Display | Category | Age | Gender |
|------|---------|----------|-----|--------|
| I10 | Essential hypertension | HTN | 18+ | Any |
| I11.9 | Hypertensive heart disease without heart failure | HTN | 40+ | Any |
| I20.9 | Angina pectoris, unspecified | CAD | 30+ | Any |
| I21.9 | Acute myocardial infarction, unspecified | MI | 30+ | Any |
| I25.10 | Atherosclerotic heart disease of native coronary artery | CAD | 30+ | Any |
| I25.110 | Atherosclerotic heart disease with unstable angina | CAD | 30+ | Any |
| I48.91 | Unspecified atrial fibrillation | Arrhythmia | 40+ | Any |
| I48.92 | Unspecified atrial flutter | Arrhythmia | 40+ | Any |
| I50.9 | Heart failure, unspecified | CHF | 30+ | Any |
| I50.22 | Chronic systolic heart failure | CHF | 40+ | Any |
| I50.32 | Chronic diastolic heart failure | CHF | 50+ | Any |
| I63.9 | Cerebral infarction, unspecified | Stroke | 40+ | Any |
| I82.401 | Acute embolism and thrombosis of unspecified deep veins of right lower extremity | DVT | 18+ | Any |

### Respiratory (J00-J99)

| Code | Display | Category | Age | Gender |
|------|---------|----------|-----|--------|
| J06.9 | Acute upper respiratory infection, unspecified | URI | Any | Any |
| J18.9 | Pneumonia, unspecified organism | Pneumonia | Any | Any |
| J44.1 | COPD with acute exacerbation | COPD | 40+ | Any |
| J44.9 | COPD, unspecified | COPD | 40+ | Any |
| J45.20 | Mild intermittent asthma, uncomplicated | Asthma | Any | Any |
| J45.30 | Mild persistent asthma, uncomplicated | Asthma | Any | Any |
| J45.40 | Moderate persistent asthma, uncomplicated | Asthma | Any | Any |
| J45.50 | Severe persistent asthma, uncomplicated | Asthma | Any | Any |

### Musculoskeletal (M00-M99)

| Code | Display | Category | Age | Gender |
|------|---------|----------|-----|--------|
| M17.11 | Primary osteoarthritis, right knee | OA | 40+ | Any |
| M17.12 | Primary osteoarthritis, left knee | OA | 40+ | Any |
| M54.5 | Low back pain | Back | 18+ | Any |
| M79.3 | Panniculitis, unspecified | Pain | Any | Any |
| M05.79 | Rheumatoid arthritis with rheumatoid factor, unspecified site | RA | 18+ | Any |
| M06.9 | Rheumatoid arthritis, unspecified | RA | 18+ | Any |
| M81.0 | Age-related osteoporosis without current pathological fracture | Osteoporosis | 50+ | Any |

### Mental Health (F00-F99)

| Code | Display | Category | Age | Gender |
|------|---------|----------|-----|--------|
| F32.1 | Major depressive disorder, single episode, moderate | Depression | 12+ | Any |
| F32.9 | Major depressive disorder, single episode, unspecified | Depression | 12+ | Any |
| F33.0 | Major depressive disorder, recurrent, mild | Depression | 12+ | Any |
| F41.1 | Generalized anxiety disorder | Anxiety | 12+ | Any |
| F41.9 | Anxiety disorder, unspecified | Anxiety | Any | Any |
| F10.20 | Alcohol dependence, uncomplicated | SUD | 18+ | Any |
| F17.210 | Nicotine dependence, cigarettes, uncomplicated | Tobacco | 12+ | Any |

### Genitourinary (N00-N99)

| Code | Display | Category | Age | Gender |
|------|---------|----------|-----|--------|
| N18.3 | Chronic kidney disease, stage 3 | CKD | 40+ | Any |
| N18.4 | Chronic kidney disease, stage 4 | CKD | 40+ | Any |
| N18.5 | Chronic kidney disease, stage 5 | CKD | 40+ | Any |
| N39.0 | Urinary tract infection, site not specified | UTI | Any | Any |
| N40.0 | Benign prostatic hyperplasia without lower urinary tract symptoms | BPH | 45+ | Male |
| N40.1 | Benign prostatic hyperplasia with lower urinary tract symptoms | BPH | 45+ | Male |

### Neoplasms (C00-D49)

| Code | Display | Category | Age | Gender |
|------|---------|----------|-----|--------|
| C34.90 | Malignant neoplasm of unspecified part of unspecified bronchus or lung | Lung CA | 40+ | Any |
| C50.919 | Malignant neoplasm of unspecified site of unspecified female breast | Breast CA | 25+ | Female |
| C61 | Malignant neoplasm of prostate | Prostate CA | 40+ | Male |
| C18.9 | Malignant neoplasm of colon, unspecified | Colon CA | 40+ | Any |

### Preventive/Administrative (Z00-Z99)

| Code | Display | Category | Age | Gender |
|------|---------|----------|-----|--------|
| Z00.00 | Encounter for general adult medical examination without abnormal findings | Preventive | 18+ | Any |
| Z00.129 | Encounter for routine child health examination without abnormal findings | Preventive | 0-17 | Any |
| Z23 | Encounter for immunization | Immunization | Any | Any |
| Z12.31 | Encounter for screening mammogram for malignant neoplasm of breast | Screening | 40+ | Female |
| Z12.11 | Encounter for screening for malignant neoplasm of colon | Screening | 45+ | Any |
| Z87.891 | Personal history of nicotine dependence | History | 18+ | Any |

---

## CPT Procedure Codes

### Evaluation & Management (99202-99499)

| Code | Display | Typical Charge | Time | Setting |
|------|---------|----------------|------|---------|
| 99202 | Office visit, new patient, straightforward | $75-125 | 15-29 min | Office |
| 99203 | Office visit, new patient, low complexity | $125-175 | 30-44 min | Office |
| 99204 | Office visit, new patient, moderate complexity | $175-250 | 45-59 min | Office |
| 99205 | Office visit, new patient, high complexity | $250-350 | 60-74 min | Office |
| 99211 | Office visit, established patient, minimal | $25-50 | 5 min | Office |
| 99212 | Office visit, established patient, straightforward | $50-80 | 10-19 min | Office |
| 99213 | Office visit, established patient, low complexity | $80-130 | 20-29 min | Office |
| 99214 | Office visit, established patient, moderate complexity | $130-200 | 30-39 min | Office |
| 99215 | Office visit, established patient, high complexity | $200-300 | 40-54 min | Office |
| 99281 | Emergency dept visit, self-limited | $75-150 | - | ED |
| 99282 | Emergency dept visit, low severity | $150-250 | - | ED |
| 99283 | Emergency dept visit, moderate severity | $250-400 | - | ED |
| 99284 | Emergency dept visit, high severity | $400-600 | - | ED |
| 99285 | Emergency dept visit, high severity with threat to life | $600-900 | - | ED |
| 99385 | Preventive visit, new patient, 18-39 years | $150-250 | - | Office |
| 99386 | Preventive visit, new patient, 40-64 years | $175-275 | - | Office |
| 99395 | Preventive visit, established patient, 18-39 years | $125-200 | - | Office |
| 99396 | Preventive visit, established patient, 40-64 years | $150-225 | - | Office |

### Laboratory (80000-89999)

| Code | Display | Typical Charge | LOINC |
|------|---------|----------------|-------|
| 80048 | Basic metabolic panel | $25-75 | 24321-2 |
| 80053 | Comprehensive metabolic panel | $35-100 | 24323-8 |
| 80061 | Lipid panel | $35-100 | 24331-1 |
| 82947 | Glucose, quantitative | $10-30 | 2345-7 |
| 82962 | Glucose, blood by glucose monitoring device | $5-15 | 2339-0 |
| 83036 | Hemoglobin A1c | $25-75 | 4548-4 |
| 84443 | Thyroid stimulating hormone (TSH) | $30-80 | 3016-3 |
| 84439 | Free thyroxine (T4) | $25-75 | 3024-7 |
| 85025 | Complete blood count with differential | $20-60 | 58410-2 |
| 85027 | Complete blood count, automated | $15-50 | 57021-8 |
| 81001 | Urinalysis with microscopy | $15-40 | 24356-8 |
| 81003 | Urinalysis, automated without microscopy | $10-25 | 5803-2 |
| 82565 | Creatinine | $10-30 | 2160-0 |
| 84132 | Potassium | $10-25 | 2823-3 |
| 84295 | Sodium | $10-25 | 2951-2 |

### Radiology (70000-79999)

| Code | Display | Typical Charge | Setting |
|------|---------|----------------|---------|
| 71046 | Chest X-ray, 2 views | $75-200 | Any |
| 71250 | CT thorax without contrast | $300-800 | Any |
| 71260 | CT thorax with contrast | $400-1000 | Any |
| 72148 | MRI lumbar spine without contrast | $500-1500 | Any |
| 73721 | MRI joint of lower extremity without contrast | $500-1500 | Any |
| 74176 | CT abdomen/pelvis without contrast | $400-1000 | Any |
| 77067 | Screening mammography, bilateral | $150-400 | Any |
| 76856 | Ultrasound, pelvic, complete | $150-400 | Any |

### Medicine (90000-99199)

| Code | Display | Typical Charge | Setting |
|------|---------|----------------|---------|
| 90471 | Immunization administration, first | $20-40 | Office |
| 90472 | Immunization administration, each additional | $15-30 | Office |
| 90658 | Influenza vaccine, IIV, 0.5 mL | $25-50 | Office |
| 90715 | Tdap vaccine | $40-80 | Office |
| 93000 | Electrocardiogram, complete | $30-100 | Office |
| 93005 | Electrocardiogram, tracing only | $20-50 | Office |
| 93306 | Echocardiogram, complete | $250-800 | Office |
| 96372 | Therapeutic injection, subcutaneous or intramuscular | $25-75 | Office |

### Surgery - Musculoskeletal (20000-29999)

| Code | Display | Typical Charge | Setting |
|------|---------|----------------|---------|
| 20610 | Arthrocentesis, aspiration and/or injection, major joint | $100-300 | Office |
| 27447 | Total knee arthroplasty | $15000-35000 | Hospital |
| 27130 | Total hip arthroplasty | $15000-35000 | Hospital |
| 29881 | Arthroscopy, knee, surgical, meniscectomy | $3000-8000 | ASC |

---

## LOINC Lab Codes

### Chemistry Panel

| LOINC | Component | Unit | Reference Range |
|-------|-----------|------|-----------------|
| 2345-7 | Glucose | mg/dL | 70-100 |
| 2339-0 | Glucose [Mass/volume] in Blood by Automated test strip | mg/dL | 70-100 |
| 2160-0 | Creatinine | mg/dL | 0.7-1.3 |
| 3094-0 | BUN | mg/dL | 7-20 |
| 33914-3 | eGFR | mL/min/1.73m2 | >60 |
| 2951-2 | Sodium | mmol/L | 136-145 |
| 2823-3 | Potassium | mmol/L | 3.5-5.0 |
| 2075-0 | Chloride | mmol/L | 98-106 |
| 2028-9 | CO2 | mmol/L | 23-29 |
| 17861-6 | Calcium | mg/dL | 8.5-10.5 |
| 1751-7 | Albumin | g/dL | 3.5-5.0 |
| 2885-2 | Protein, total | g/dL | 6.0-8.0 |
| 1975-2 | Bilirubin, total | mg/dL | 0.1-1.2 |
| 1920-8 | AST (SGOT) | U/L | 10-40 |
| 1742-6 | ALT (SGPT) | U/L | 7-56 |
| 6768-6 | Alkaline phosphatase | U/L | 44-147 |

### Lipid Panel

| LOINC | Component | Unit | Optimal |
|-------|-----------|------|---------|
| 2093-3 | Cholesterol, total | mg/dL | <200 |
| 2085-9 | HDL cholesterol | mg/dL | >40 |
| 2089-1 | LDL cholesterol | mg/dL | <100 |
| 2571-8 | Triglycerides | mg/dL | <150 |
| 13458-5 | VLDL cholesterol | mg/dL | <30 |

### Hematology

| LOINC | Component | Unit | Reference Range |
|-------|-----------|------|-----------------|
| 6690-2 | WBC | 10*3/uL | 4.5-11.0 |
| 789-8 | RBC | 10*6/uL | 4.2-5.9 |
| 718-7 | Hemoglobin | g/dL | 12.0-17.5 |
| 4544-3 | Hematocrit | % | 36-51 |
| 787-2 | MCV | fL | 80-100 |
| 785-6 | MCH | pg | 27-33 |
| 786-4 | MCHC | g/dL | 32-36 |
| 788-0 | RDW | % | 11.5-14.5 |
| 777-3 | Platelets | 10*3/uL | 150-400 |
| 770-8 | Neutrophils % | % | 40-70 |
| 736-9 | Lymphocytes % | % | 20-40 |
| 5905-5 | Monocytes % | % | 2-8 |
| 713-8 | Eosinophils % | % | 1-4 |
| 706-2 | Basophils % | % | 0-1 |

### Diabetes Monitoring

| LOINC | Component | Unit | Target |
|-------|-----------|------|--------|
| 4548-4 | Hemoglobin A1c | % | <7.0 |
| 2345-7 | Glucose, fasting | mg/dL | 70-100 |
| 1558-6 | Glucose, post-meal | mg/dL | <140 |
| 14749-6 | Glucose, random | mg/dL | 70-140 |
| 53049-3 | Glucose mean 30 days | mg/dL | - |

### Thyroid

| LOINC | Component | Unit | Reference Range |
|-------|-----------|------|-----------------|
| 3016-3 | TSH | mIU/L | 0.4-4.0 |
| 3024-7 | Free T4 | ng/dL | 0.8-1.8 |
| 3053-6 | Free T3 | pg/mL | 2.3-4.2 |
| 3026-2 | T4, total | ug/dL | 4.5-12.0 |

### Urinalysis

| LOINC | Component | Value Type |
|-------|-----------|------------|
| 5803-2 | pH | 5.0-8.0 |
| 5811-5 | Specific gravity | 1.005-1.030 |
| 5804-0 | Protein | Neg/Trace/1+/2+/3+ |
| 5792-7 | Glucose | Neg/Trace/1+/2+/3+ |
| 5794-3 | Hemoglobin | Neg/Trace/1+/2+/3+ |
| 5799-2 | Leukocyte esterase | Neg/Trace/1+/2+/3+ |
| 5802-4 | Nitrite | Neg/Pos |
| 5797-6 | Ketones | Neg/Trace/1+/2+/3+ |

---

## Medication Reference Data

### Diabetes Medications

| Generic Name | Brand | RxNorm | NDC (example) | Strength | Route |
|--------------|-------|--------|---------------|----------|-------|
| Metformin | Glucophage | 6809 | 00087607101 | 500mg, 850mg, 1000mg | oral |
| Metformin ER | Glucophage XR | 860975 | 00087607305 | 500mg, 750mg, 1000mg | oral |
| Glipizide | Glucotrol | 4821 | 00069015501 | 5mg, 10mg | oral |
| Glimepiride | Amaryl | 25789 | 00088221001 | 1mg, 2mg, 4mg | oral |
| Sitagliptin | Januvia | 593411 | 00006027731 | 25mg, 50mg, 100mg | oral |
| Empagliflozin | Jardiance | 1545653 | 00597016701 | 10mg, 25mg | oral |
| Liraglutide | Victoza | 897122 | 00169436011 | 18mg/3mL pen | subcut |
| Semaglutide | Ozempic | 1991302 | 00169418112 | 2mg/1.5mL pen | subcut |
| Insulin glargine | Lantus | 261542 | 00088221905 | 100 units/mL | subcut |
| Insulin lispro | Humalog | 86009 | 00002751601 | 100 units/mL | subcut |

### Cardiovascular Medications

| Generic Name | Brand | RxNorm | NDC (example) | Strength | Route |
|--------------|-------|--------|---------------|----------|-------|
| Lisinopril | Prinivil, Zestril | 29046 | 00310019010 | 5mg, 10mg, 20mg, 40mg | oral |
| Amlodipine | Norvasc | 17767 | 00069153030 | 2.5mg, 5mg, 10mg | oral |
| Losartan | Cozaar | 52175 | 00006095131 | 25mg, 50mg, 100mg | oral |
| Metoprolol succinate | Toprol-XL | 866924 | 00186101589 | 25mg, 50mg, 100mg, 200mg | oral |
| Carvedilol | Coreg | 20352 | 00007416020 | 3.125mg, 6.25mg, 12.5mg, 25mg | oral |
| Atorvastatin | Lipitor | 83367 | 00071015523 | 10mg, 20mg, 40mg, 80mg | oral |
| Rosuvastatin | Crestor | 301542 | 00310075590 | 5mg, 10mg, 20mg, 40mg | oral |
| Furosemide | Lasix | 4603 | 00039000701 | 20mg, 40mg, 80mg | oral |
| Warfarin | Coumadin | 11289 | 00056017075 | 1mg-10mg | oral |
| Apixaban | Eliquis | 1364430 | 00003089421 | 2.5mg, 5mg | oral |

### Pain/Anti-inflammatory

| Generic Name | Brand | RxNorm | NDC (example) | Strength | Route | Schedule |
|--------------|-------|--------|---------------|----------|-------|----------|
| Ibuprofen | Advil, Motrin | 5640 | 00573015001 | 200mg, 400mg, 600mg, 800mg | oral | - |
| Naproxen | Naprosyn, Aleve | 7258 | 00004621002 | 250mg, 375mg, 500mg | oral | - |
| Acetaminophen | Tylenol | 161 | 00045049650 | 325mg, 500mg, 650mg | oral | - |
| Tramadol | Ultram | 10689 | 00045086060 | 50mg, 100mg | oral | IV |
| Hydrocodone/APAP | Vicodin, Norco | 856980 | 00074306114 | 5/325mg, 7.5/325mg, 10/325mg | oral | II |
| Oxycodone | OxyContin | 7804 | 59011044020 | 5mg, 10mg, 15mg, 20mg, 30mg | oral | II |

### Respiratory

| Generic Name | Brand | RxNorm | NDC (example) | Strength | Route |
|--------------|-------|--------|---------------|----------|-------|
| Albuterol HFA | ProAir, Ventolin | 745679 | 00173068220 | 90mcg/actuation | inhalation |
| Fluticasone/Salmeterol | Advair Diskus | 896188 | 00173069700 | 100/50, 250/50, 500/50 | inhalation |
| Budesonide/Formoterol | Symbicort | 896188 | 00186037020 | 80/4.5, 160/4.5 | inhalation |
| Montelukast | Singulair | 88249 | 00006027531 | 4mg, 5mg, 10mg | oral |
| Prednisone | Deltasone | 8640 | 00591543201 | 5mg, 10mg, 20mg | oral |

### Mental Health

| Generic Name | Brand | RxNorm | NDC (example) | Strength | Route |
|--------------|-------|--------|---------------|----------|-------|
| Sertraline | Zoloft | 36437 | 00049490066 | 25mg, 50mg, 100mg | oral |
| Escitalopram | Lexapro | 321988 | 00456202001 | 5mg, 10mg, 20mg | oral |
| Fluoxetine | Prozac | 4493 | 00777310602 | 10mg, 20mg, 40mg | oral |
| Bupropion XL | Wellbutrin XL | 993503 | 00173072155 | 150mg, 300mg | oral |
| Alprazolam | Xanax | 596 | 00009009101 | 0.25mg, 0.5mg, 1mg, 2mg | oral | IV |
| Lorazepam | Ativan | 6470 | 00187062101 | 0.5mg, 1mg, 2mg | oral | IV |

### Gastrointestinal

| Generic Name | Brand | RxNorm | NDC (example) | Strength | Route |
|--------------|-------|--------|---------------|----------|-------|
| Omeprazole | Prilosec | 7646 | 00186100131 | 20mg, 40mg | oral |
| Pantoprazole | Protonix | 40790 | 00008084101 | 20mg, 40mg | oral |
| Ondansetron | Zofran | 26225 | 00173044200 | 4mg, 8mg | oral |

---

## Place of Service Codes

| Code | Name | Description |
|------|------|-------------|
| 11 | Office | Physician office |
| 12 | Home | Patient's home |
| 13 | Assisted Living | Assisted living facility |
| 19 | Off Campus-Outpatient Hospital | Off-campus hospital outpatient |
| 21 | Inpatient Hospital | Hospital inpatient |
| 22 | On Campus-Outpatient Hospital | Hospital outpatient |
| 23 | Emergency Room - Hospital | Hospital emergency room |
| 24 | Ambulatory Surgical Center | ASC |
| 31 | Skilled Nursing Facility | SNF |
| 32 | Nursing Facility | Nursing facility |
| 33 | Custodial Care Facility | Custodial care |
| 34 | Hospice | Hospice facility |
| 41 | Ambulance - Land | Ground ambulance |
| 49 | Independent Clinic | Freestanding clinic |
| 50 | Federally Qualified Health Center | FQHC |
| 53 | Community Mental Health Center | CMHC |
| 61 | Comprehensive Inpatient Rehab | Inpatient rehab |
| 62 | Comprehensive Outpatient Rehab | Outpatient rehab |
| 65 | End-Stage Renal Disease Facility | Dialysis |
| 71 | Public Health Clinic | State/local health clinic |
| 72 | Rural Health Clinic | RHC |
| 81 | Independent Laboratory | Lab |

---

## Revenue Codes

### Common Facility Revenue Codes

| Code | Description | Category |
|------|-------------|----------|
| 0100 | All-inclusive rate | Room |
| 0110 | Room & board - private | Room |
| 0120 | Room & board - semi-private | Room |
| 0121 | Room & board - semi-private (2 bed) | Room |
| 0150 | Intensive care | Room |
| 0200 | Intensive care | ICU |
| 0250 | Pharmacy | Pharmacy |
| 0251 | Pharmacy - generic | Pharmacy |
| 0252 | Pharmacy - non-generic | Pharmacy |
| 0258 | Pharmacy - IV solutions | Pharmacy |
| 0260 | IV therapy | IV |
| 0270 | Medical/surgical supplies | Supplies |
| 0300 | Laboratory | Lab |
| 0301 | Laboratory - chemistry | Lab |
| 0302 | Laboratory - immunology | Lab |
| 0305 | Laboratory - hematology | Lab |
| 0320 | Radiology - diagnostic | Radiology |
| 0324 | Radiology - diagnostic - CT | Radiology |
| 0329 | Radiology - diagnostic - other | Radiology |
| 0350 | CT scan | Radiology |
| 0360 | OR services | Surgery |
| 0370 | Anesthesia | Surgery |
| 0390 | Blood storage and processing | Blood |
| 0400 | Other imaging | Radiology |
| 0410 | Respiratory services | Respiratory |
| 0420 | Physical therapy | Therapy |
| 0430 | Occupational therapy | Therapy |
| 0440 | Speech therapy | Therapy |
| 0450 | Emergency room | ED |
| 0456 | Emergency room - urgent | ED |
| 0459 | Emergency room - other | ED |
| 0500 | Outpatient services | Outpatient |
| 0510 | Clinic | Outpatient |
| 0610 | MRI | Radiology |
| 0636 | Drugs requiring specific ID - admin | Pharmacy |
| 0710 | Recovery room | Surgery |
| 0720 | Labor/delivery | OB |
| 0730 | EKG/ECG | Cardiology |
| 0750 | Gastro-intestinal services | GI |
| 0761 | Treatment room | Outpatient |
| 0762 | Observation room | Outpatient |
| 0790 | Telemedicine | Telehealth |
| 0942 | Ambulance - ground | Transport |

---

## Modifier Codes

### Common CPT Modifiers

| Modifier | Description | Use Case |
|----------|-------------|----------|
| 25 | Significant, separately identifiable E/M | E/M with procedure |
| 26 | Professional component | Radiology interpretation |
| TC | Technical component | Radiology technical |
| 50 | Bilateral procedure | Both sides |
| 51 | Multiple procedures | 2nd+ procedure |
| 52 | Reduced services | Partial procedure |
| 59 | Distinct procedural service | Separate procedure |
| 76 | Repeat procedure, same physician | Re-do same day |
| 77 | Repeat procedure, different physician | Re-do different MD |
| 79 | Unrelated procedure during postop | New problem in global |
| LT | Left side | Laterality |
| RT | Right side | Laterality |
| GY | Item/service statutorily excluded | Non-covered |
| GA | Waiver of liability on file | ABN signed |

### Place of Service Modifiers

| Modifier | Description |
|----------|-------------|
| PO | Services provided in off-campus provider-based department |
| 95 | Synchronous telemedicine service |
| GT | Interactive audio/video telecommunications |

---

## Plan and Benefit Codes

### Plan Types

| Code | Name | Description |
|------|------|-------------|
| HMO | Health Maintenance Organization | Managed care, PCP required, referrals needed, in-network only |
| PPO | Preferred Provider Organization | Flexible network, no PCP required, OON covered at higher cost |
| EPO | Exclusive Provider Organization | No PCP/referral required, in-network only |
| POS | Point of Service | PCP required, referrals for in-network, OON available |
| HDHP | High Deductible Health Plan | High deductible, HSA-eligible, IRS contribution limits |
| INDEMNITY | Indemnity/Fee-for-Service | Traditional plan, any provider, reimbursement-based |

### Metal Tiers (ACA Marketplace)

| Tier | Actuarial Value | Member Cost Share | Typical Deductible |
|------|-----------------|-------------------|-------------------|
| bronze | 60% | 40% | $6,000+ |
| silver | 70% | 30% | $3,000-4,000 |
| gold | 80% | 20% | $1,000-1,500 |
| platinum | 90% | 10% | $0-500 |

### Network Requirement Codes

| Code | Description |
|------|-------------|
| in_network_only | No OON coverage except emergency |
| in_network_preferred | OON covered at higher cost sharing |

### Network Tier Codes

| Code | Description |
|------|-------------|
| in_network | Contracted provider, standard cost sharing |
| out_of_network | Non-contracted provider, higher cost sharing |
| tier_1 | Preferred providers, lowest cost |
| tier_2 | Participating providers, moderate cost |
| tier_3 | Out-of-network, highest cost |

### Service Type Codes

| Code | Description | Typical Cost Sharing |
|------|-------------|---------------------|
| pcp_visit | Primary care office visit | Copay $20-40 |
| specialist_visit | Specialist office visit | Copay $40-75 |
| urgent_care | Urgent care center visit | Copay $50-100 |
| emergency_room | Emergency department | Copay $150-500 |
| inpatient | Hospital inpatient stay | Coinsurance 20% or per-day copay |
| outpatient_surgery | Ambulatory surgery | Copay $200-500 or coinsurance |
| lab_work | Laboratory services | $0 or subject to deductible |
| xray | X-ray imaging | Subject to deductible |
| advanced_imaging | MRI, CT, PET scans | Subject to deductible + coinsurance |
| mental_health_outpatient | Outpatient mental health | Copay $25-50 |
| mental_health_inpatient | Inpatient psychiatric | Same as inpatient |
| physical_therapy | Physical therapy visit | Copay $40-60 per visit |
| preventive | Preventive care services | 100% covered, no cost sharing |
| telehealth | Virtual/telemedicine visit | $0-25 copay |
| ambulance | Ambulance transport | Copay $150-300 or coinsurance |
| skilled_nursing | Skilled nursing facility | Coinsurance, day limit |
| home_health | Home health services | Coinsurance |

### Cost Sharing Type Codes

| Code | Description | Example |
|------|-------------|---------|
| copay | Fixed dollar amount | $25 per visit |
| coinsurance | Percentage of allowed amount | 20% after deductible |
| covered_100 | No member cost sharing | Preventive care |

### Pharmacy Tier Codes

| Tier | Name | Description | Typical Copay |
|------|------|-------------|---------------|
| 1 | Preferred Generic | Lowest-cost generic drugs | $10-15 |
| 2 | Non-Preferred Generic | Other generic drugs | $20-30 |
| 3 | Preferred Brand | Formulary brand-name drugs | $40-60 |
| 4 | Non-Preferred Brand | Non-formulary brand drugs | $75-100 |
| 5 | Specialty | Biologics, specialty drugs | 20-30% coinsurance |

### Accumulator Type Codes

| Code | Description |
|------|-------------|
| deductible | Medical deductible accumulator |
| oop_max | Medical out-of-pocket maximum |
| rx_deductible | Pharmacy deductible (if separate) |
| rx_oop_max | Pharmacy out-of-pocket maximum |

### Coverage Tier Codes

| Code | Description | X12 834 HD05 |
|------|-------------|--------------|
| EMP | Employee only | EMP |
| ESP | Employee + spouse | ESP |
| ECH | Employee + child(ren) | ECH |
| FAM | Employee + family | FAM |
| TWO | Employee + one dependent | TWO |

### Relationship Codes (X12)

| Code | Description |
|------|-------------|
| 18 | Self (subscriber) |
| 01 | Spouse |
| 19 | Child |
| 20 | Employee |
| 21 | Unknown |
| 39 | Organ donor |
| 40 | Cadaver donor |
| 53 | Life partner |
| G8 | Other relationship |

### Enrollment Reason Codes

| Code | Description | QLE |
|------|-------------|-----|
| new_hire | New employee enrollment | No |
| open_enrollment | Annual open enrollment | No |
| qle | Qualifying life event | Yes |
| cobra | COBRA continuation | Yes |
| special_enrollment | Special enrollment period | Yes |
| reinstatement | Reinstatement of coverage | No |

### Qualifying Life Events (QLE)

| Code | Description | Enrollment Window |
|------|-------------|-------------------|
| marriage | Marriage | 30-60 days |
| divorce | Divorce/legal separation | 30-60 days |
| birth | Birth of child | 30 days |
| adoption | Adoption/foster placement | 30 days |
| death | Death of dependent | 30-60 days |
| loss_of_coverage | Loss of other coverage | 60 days |
| move | Relocation affecting network | 60 days |
| employment_change | Change in employment status | 30 days |
| dependent_age_out | Dependent aging off plan | 30 days |

### IRS HDHP Limits (2025)

| Parameter | Individual | Family |
|-----------|------------|--------|
| Minimum Deductible | $1,650 | $3,300 |
| Maximum OOP | $8,300 | $16,600 |
| HSA Contribution Limit | $4,300 | $8,550 |
| Catch-up (55+) | +$1,000 | +$1,000 |
