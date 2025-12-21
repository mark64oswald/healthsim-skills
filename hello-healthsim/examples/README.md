# HealthSim Examples

Detailed examples demonstrating HealthSim capabilities across all products and clinical domains.

---

## Learning Path: Simple to Complex

### Level 1: Getting Started (5 minutes)

Start here to verify your setup and learn the basics.

| Example | Prompt | What You Learn |
|---------|--------|----------------|
| Simple Patient | "Generate a patient" | Basic PatientSim output |
| Office Visit Claim | "Generate a professional claim for an office visit" | Basic MemberSim output |
| Prescription Fill | "Generate a pharmacy claim for lisinopril" | Basic RxMemberSim output |
| Phase 3 Trial | "Generate a Phase 3 oncology trial with 20 subjects" | Basic TrialSim output |

See: [PatientSim Example 1](patientsim-examples.md#example-1-simple-patient), [MemberSim Example 1](membersim-examples.md#example-1-simple-office-visit-claim), [RxMemberSim Example 1](rxmembersim-examples.md#example-1-simple-generic-prescription), [TrialSim Quick Start](trialsim-examples.md#quick-start-examples)

---

### Level 2: Clinical Domains (10-15 minutes)

Learn to generate data for specific clinical conditions.

| Domain | Example Prompt | Guide |
|--------|----------------|-------|
| **Diabetes** | "Generate a 62-year-old with Type 2 diabetes and A1C of 8.5" | [PatientSim Example 2](patientsim-examples.md#example-2-diabetic-patient) |
| **Heart Failure** | "Generate a patient with HFrEF and NYHA Class III" | [PatientSim Example 3](patientsim-examples.md#example-3-heart-failure-patient) |
| **CKD** | "Generate a patient with Stage 4 CKD" | [PatientSim Example 4](patientsim-examples.md#example-4-ckd-patient) |
| **Oncology** | "Generate a Stage IIA breast cancer patient" | [Oncology Examples](oncology-examples.md) |
| **Behavioral Health** | "Generate a psychotherapy claim for depression" | [MemberSim](membersim-examples.md) |

---

### Level 2.5: Clinical Trials (15 minutes)

Generate clinical trial data with CDISC compliance.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Phase 3 Trial** | "Generate Phase 3 oncology trial with 100 subjects" | [TrialSim Quick Start](trialsim-examples.md#quick-start-examples) |
| **Dose Escalation** | "Generate Phase 1 3+3 dose escalation study" | [Phase 1 Examples](trialsim-examples.md#phase-i-dose-escalation-examples) |
| **Adverse Events** | "Generate AEs with MedDRA coding for 50 subjects" | [TrialSim AE Example](trialsim-examples.md#example-2-generate-adverse-events) |
| **SDTM Output** | "Generate DM and AE domains as SDTM" | [SDTM Domain Examples](trialsim-examples.md#sdtm-domain-output-examples) |
| **Trial Analytics** | "Generate trial data as star schema for DuckDB" | [Dimensional Analytics](trialsim-examples.md#dimensional-analytics-examples) |

---

### Level 3: Claims & Adjudication (15 minutes)

Understand healthcare payment workflows.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Paid Claim** | "Generate a paid claim with copay applied" | [MemberSim Example 1](membersim-examples.md#example-1-simple-office-visit-claim) |
| **Denied Claim** | "Generate a denied MRI claim requiring prior auth" | [MemberSim Example 2](membersim-examples.md#example-2-denied-claim) |
| **Facility Claim** | "Generate a hospital admission claim with DRG" | [MemberSim Example 3](membersim-examples.md#example-3-facility-claim-with-drg) |
| **Deductible Applied** | "Generate a claim where deductible applies" | [MemberSim Example 4](membersim-examples.md#example-4-claim-with-deductible) |

---

### Level 4: Pharmacy & DUR (15 minutes)

Test pharmacy benefit workflows and drug utilization review.

| Scenario | Example Prompt | Guide |
|----------|----------------|-------|
| **Drug Interaction** | "Generate a pharmacy claim with drug-drug interaction" | [RxMemberSim Example 2](rxmembersim-examples.md#example-2-drug-interaction-alert) |
| **Early Refill** | "Generate a pharmacy claim rejected for early refill" | [RxMemberSim Example 3](rxmembersim-examples.md#example-3-early-refill-rejection) |
| **Step Therapy** | "Generate a step therapy rejection" | [RxMemberSim Example 4](rxmembersim-examples.md#example-4-step-therapy) |
| **Specialty Drug** | "Generate a specialty pharmacy claim with PA" | [RxMemberSim Example 5](rxmembersim-examples.md#example-5-specialty-pharmacy) |

---

### Level 5: Output Formats (15 minutes)

Transform data to healthcare standards.

| Format | Example Prompt | Guide |
|--------|----------------|-------|
| **FHIR R4** | "Generate a diabetic patient as FHIR Bundle" | [Format Examples - FHIR](format-examples.md#fhir-r4-examples) |
| **C-CDA** | "Generate a discharge summary as C-CDA" | [Format Examples - C-CDA](format-examples.md#c-cda-examples) |
| **HL7v2 ADT** | "Generate an admission as ADT A01 message" | [Format Examples - HL7v2](format-examples.md#hl7v2-examples) |
| **X12 837** | "Generate a professional claim as X12 837P" | [Format Examples - X12](format-examples.md#x12-examples) |
| **CSV** | "Generate 10 patients as CSV" | [Format Examples - CSV](format-examples.md#csv-examples) |

---

### Level 6: Cross-Domain Scenarios (20 minutes)

Create realistic end-to-end test data spanning multiple products.

| Scenario | What You Get | Guide |
|----------|--------------|-------|
| **Patient + Claims + Rx** | Diabetic patient with office visit and pharmacy claims | [Cross-Domain Example 1](cross-domain-examples.md#example-1-patient-with-medical-and-pharmacy-claims) |
| **Hospitalization Episode** | Inpatient admission, follow-up, discharge meds | [Cross-Domain Example 2](cross-domain-examples.md#example-2-hospitalization-with-follow-up) |
| **Prior Auth Flow** | Rejection → PA submission → Approval → Fill | [Cross-Domain Example 3](cross-domain-examples.md#example-3-prior-auth-flow) |
| **Value-Based Care** | Patient with quality measures and care gaps | [Cross-Domain Example 4](cross-domain-examples.md#example-4-value-based-care-report) |
| **Trial + EMR Linkage** | Trial subject linked to PatientSim medical history | [Cross-Domain Example 5](cross-domain-examples.md#example-5-clinical-trial-subject-with-emr-linkage) |
| **Trial + Provider Network** | Trial site linked to NetworkSim facilities | [Cross-Domain Example 6](cross-domain-examples.md#example-6-trial-subject-with-site-provider-linkage) |
| **Trial Analytics** | Cross-product dimensional analytics | [Cross-Domain Example 7](cross-domain-examples.md#example-7-cross-product-dimensional-analytics) |

---

## Example Files by Product

| Guide | Description | Examples |
|-------|-------------|----------|
| [PatientSim Examples](patientsim-examples.md) | Clinical data generation | Patients, diagnoses, medications, labs |
| [MemberSim Examples](membersim-examples.md) | Claims and payer data | Professional, facility, adjudication |
| [RxMemberSim Examples](rxmembersim-examples.md) | Pharmacy data | Prescriptions, DUR alerts, copay cards |
| [TrialSim Examples](trialsim-examples.md) | Clinical trial data | SDTM domains, AEs, efficacy, sites |
| [Oncology Examples](oncology-examples.md) | Cancer-specific scenarios | Staging, treatment, biomarkers |
| [Cross-Domain Examples](cross-domain-examples.md) | Multi-product scenarios | End-to-end test data |
| [Format Examples](format-examples.md) | Output transformations | FHIR, HL7v2, X12, C-CDA, SDTM, CSV |

---

## Quick Reference: Example Prompts by Domain

### Chronic Disease

```text
Generate a 65-year-old with Type 2 diabetes, hypertension, and hyperlipidemia
Generate a patient with heart failure and reduced ejection fraction
Generate a patient with Stage 3b CKD and diabetes
```

### Oncology

```text
Generate a Stage IIB ER-positive breast cancer patient with treatment plan
Generate a non-small cell lung cancer patient with EGFR mutation
Generate a colorectal cancer patient with liver metastases
```

### Acute Care & Emergency

```text
Generate a sepsis patient with ICU admission
Generate an ED chest pain patient with HEART score workup
Generate a hip replacement patient with pre-op and post-op care
```

### Clinical Trials

```text
Generate a Phase 3 oncology trial with 200 subjects randomized 2:1
Generate adverse events with MedDRA coding for 100 subjects
Generate DM and AE domains as SDTM for a Phase 2 trial
Generate a Phase 1 dose escalation study with 3+3 design
Generate tumor response data with RECIST 1.1 assessments
Generate trial data as star schema for DuckDB analytics
```

### Maternal & Pediatric

```text
Generate a 28-week pregnant patient with gestational diabetes
Generate a postpartum patient with preeclampsia
Generate pediatric vaccination records for a 2-year-old
```

### Behavioral Health

```text
Generate a psychotherapy claim for major depressive disorder
Generate a substance abuse IOP claim
Generate a telehealth psychiatry visit claim
```

### Claims & Payment

```text
Generate a paid claim with deductible and coinsurance applied
Generate a denied claim for prior authorization required
Generate a claim with out-of-network penalties
```

### Pharmacy

```text
Generate a pharmacy claim with drug-drug interaction alert
Generate a specialty drug claim requiring prior authorization
Generate a copay card transaction for a brand medication
```

---

## How to Use These Examples

Each example in the guides includes:

1. **The Prompt** - Exact text to send to Claude
2. **Expected Output** - Sample JSON/format response
3. **Key Points** - What to notice in the output
4. **Variations** - How to modify the request for different scenarios

## Tips for Success

1. **Start simple** - Begin with Level 1 examples to verify your setup
2. **Be specific** - "62-year-old diabetic with A1C 9.5" beats "sick patient"
3. **Request format early** - "Generate as FHIR..." not "convert to FHIR"
4. **Combine domains** - Use cross-domain prompts for realistic test data
5. **Check consistency** - Verify diagnoses, medications, and claims align
