# Hello HealthSim!

**Get up and running with synthetic healthcare data generation in 5 minutes.**

HealthSim is a skill-based framework that enables Claude to generate realistic synthetic healthcare data through natural conversation. No coding required - just describe what you need.

## What You'll Build

By the end of this guide, you'll be able to generate:

- **Clinical Data** - Patients with realistic diagnoses, medications, and lab results
- **Claims Data** - Professional and facility claims with proper adjudication
- **Pharmacy Data** - Prescriptions, pharmacy claims, and drug utilization alerts

All through simple natural language requests like:
> "Generate a 65-year-old diabetic patient with hypertension and their recent office visit claim"

---

## Prerequisites

Before starting, ensure you have:

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Git | 2.0+ | `git --version` |
| Claude Desktop **or** Claude Code | Latest | See installation links below |
| Anthropic API Key (for Claude Code) | - | [Get API Key](https://console.anthropic.com/) |

### Install Claude (Choose One)

**Option A: Claude Desktop** (Recommended for beginners)
- Download from [claude.ai/download](https://claude.ai/download)
- Requires Claude Pro subscription for extended usage

**Option B: Claude Code** (For developers)
```bash
# Install via npm
npm install -g @anthropic-ai/claude-code

# Or via Homebrew (macOS)
brew install claude-code
```

---

## Quick Start

### Step 1: Clone the Repository

```bash
# Clone HealthSim skills
git clone https://github.com/mark64oswald/healthsim-skills.git

# Navigate to the project
cd healthsim-skills
```

### Step 2: Configure Claude

Choose your Claude environment and follow the appropriate guide:

| Environment | Guide | Best For |
|-------------|-------|----------|
| Claude Desktop | [CLAUDE-DESKTOP.md](CLAUDE-DESKTOP.md) | Interactive exploration, non-developers |
| Claude Code | [CLAUDE-CODE.md](CLAUDE-CODE.md) | Developers, automation, CI/CD |

### Step 3: Verify Installation

Once configured, test with this simple prompt:

```
Generate a patient with Type 2 diabetes
```

You should see output like:
```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Maria", "family_name": "Garcia" },
    "birth_date": "1962-05-14",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "E11.9", "description": "Type 2 diabetes mellitus without complications" }
  ],
  "medications": [
    { "name": "Metformin", "dose": "1000 mg", "frequency": "BID" }
  ]
}
```

**Congratulations!** You're ready to generate healthcare data!

---

## Your First 5 Minutes

Try these examples to explore HealthSim's capabilities:

### Example 1: Generate a Patient (PatientSim)

```
Generate a 72-year-old male with heart failure and COPD, including recent labs
```

### Example 2: Generate a Claim (MemberSim)

```
Generate a paid professional claim for a cardiology office visit
```

### Example 3: Generate a Pharmacy Claim (RxMemberSim)

```
Generate a pharmacy claim for lisinopril with a drug interaction alert
```

### Example 4: Cross-Domain Generation

```
Generate a diabetic patient with their recent office visit claim and pharmacy claims for their medications
```

### Example 5: Format Transformation

```
Generate an HL7 ADT^A01 admission message for a patient with pneumonia
```

See [examples/](examples/) for more detailed examples with expected outputs.

---

## Hello, Diabetes!

Let's explore a common chronic disease scenario with output format variations.

### Basic Diabetic Patient

```
Generate a 58-year-old female with Type 2 diabetes
```

This generates a patient with:

- Diagnosis (E11.9 Type 2 diabetes)
- Common comorbidities (hypertension, hyperlipidemia)
- Appropriate medications (metformin, lisinopril, atorvastatin)
- Relevant labs (A1C, glucose, creatinine)

### With Complications

```
Generate a diabetic patient with nephropathy and retinopathy
```

This adds diabetic complications with appropriate staging and specialist referrals.

### As FHIR Bundle

```
Generate a diabetic patient as a FHIR Bundle
```

Same clinical content, but formatted as FHIR R4 resources - perfect for testing FHIR APIs.

### As CSV for Analytics

```
Generate 10 diabetic patients as CSV
```

Generates tabular data suitable for spreadsheets and analytics tools.

---

## Hello, Claims!

Now let's generate claims data with different payment scenarios.

### Paid Claim (Basic)

```
Generate a paid professional claim for a primary care office visit
```

This generates:

- Member information
- Claim with CPT 99213/99214 (E&M code)
- Adjudication with copay applied
- CARC/RARC adjustment codes

### Denied Claim

```
Generate a denied professional claim for an MRI requiring prior authorization
```

This generates a claim with denial reason CO-15 (prior auth required) and appeal information.

### Facility Claim with DRG

```
Generate an inpatient admission claim for heart failure with DRG
```

This generates an 837I institutional claim with DRG assignment and length-of-stay based payment.

### As X12 837P Format

```
Generate a professional claim as X12 837P
```

Same claim data, but in EDI X12 format - perfect for testing claims processing systems.

---

## Hello, Pharmacy!

Generate pharmacy claims with clinical interventions.

### Simple Prescription Fill

```
Generate a pharmacy claim for atorvastatin 20mg
```

This generates:

- Prescription details (NDC, quantity, days supply)
- Pharmacy claim (BIN, PCN, cardholder ID)
- Pricing (ingredient cost, dispensing fee, copay)
- Tier information (generic = Tier 1)

### Drug Interaction Alert

```
Generate a pharmacy claim for warfarin that triggers a drug interaction alert with aspirin
```

This generates a DUR (Drug Utilization Review) alert with:

- Interaction severity (DD - Drug-Drug)
- Clinical significance
- Pharmacist recommendation

### Prior Authorization Required

```
Generate a specialty pharmacy claim for Humira requiring prior authorization
```

This generates the PA workflow for high-cost biologics with clinical criteria.

### As NCPDP Format

```
Generate a pharmacy claim as NCPDP D.0
```

Same pharmacy data in NCPDP telecommunications standard format.

---

## Hello, Oncology!

PatientSim includes comprehensive oncology scenario skills for generating realistic cancer patient journeys with accurate staging, biomarkers, and treatment protocols.

### Breast Cancer Patient

```
Generate a 55-year-old female with Stage IIA ER-positive, HER2-negative breast cancer
```

This generates a complete breast cancer patient with:

- TNM staging (T2 N0 M0)
- Biomarkers (ER 95%, PR 80%, HER2 1+, Ki-67 15%)
- Molecular subtype (Luminal A)
- Oncotype DX score and chemotherapy benefit assessment
- Surgical details (lumpectomy, sentinel node biopsy)
- Treatment plan (surgery → radiation → hormonal therapy)

### Lung Cancer with Targeted Therapy

```
Generate a 68-year-old male with Stage IV NSCLC, EGFR exon 19 deletion positive, with brain metastases
```

This generates biomarker-driven lung cancer treatment:

- Comprehensive molecular testing (EGFR, ALK, ROS1, PD-L1)
- Brain metastases management (SRS)
- Targeted therapy selection (osimertinib for EGFR mutation)
- Surveillance imaging schedule

### Colorectal Cancer with Biomarkers

```
Generate a 58-year-old with Stage III colon cancer, MSI-high status
```

This generates colorectal cancer with genomic context:

- MSI/MMR testing results
- RAS/BRAF mutation status
- Genetic counseling referral (Lynch syndrome evaluation)
- Adjuvant chemotherapy (CAPOX) with duration

### Cancer Patient with Comorbidities

```
Generate a 70-year-old with Stage IIIB colon cancer who has CKD Stage 3b and Type 2 diabetes requiring chemotherapy dose adjustments
```

This generates multi-morbid oncology patients:

- Chemotherapy dose modifications for renal function
- Multi-specialty care coordination
- Enhanced monitoring protocols

See [examples/oncology-examples.md](examples/oncology-examples.md) for detailed oncology examples with complete outputs.

---

## Hello, Analytics!

HealthSim data can be loaded directly into analytics databases. You have flexibility in how you structure the data - from simple flat tables to full star schemas.

### Local Analytics with DuckDB

Perfect for local development, testing, and demos. No authentication required.

**Simple tables:**

```
Generate 10 diabetic patients and load them into DuckDB
```

**Star schema for BI dashboards:**

```
Generate 10 patients in dimensional format for DuckDB with fact and dimension tables
```

This creates properly normalized analytics tables with:

- Dimension tables (dim_patient, dim_diagnosis, dim_medication, dim_date)
- Fact tables (fact_encounters, fact_lab_results)
- Pre-calculated metrics (age bands, LOS, readmission flags)

### Enterprise Analytics with Databricks

For production analytics, team collaboration, and large-scale testing.

**Prerequisites:** Authenticate via Databricks CLI first:

```bash
databricks auth profiles  # Verify authentication
```

**Load to Databricks:**

```
Generate 10 patients in dimensional format for Databricks, catalog 'dev_catalog', schema 'gold'
```

Claude will:

1. Generate the dimensional data
2. Create tables (if needed)
3. Load via SQL Statements API
4. Report success with row counts

### Claims Analytics

Same flexibility works for claims and pharmacy data:

```
Generate 20 members with claims in star schema format for DuckDB
```

```
Generate pharmacy data with prescription fills as a fact table, load to Databricks
```

See [../formats/dimensional-analytics.md](../formats/dimensional-analytics.md) for complete star schema definitions and sample queries.

---

## What's Included

```
healthsim-skills/
├── SKILL.md                    # Master skill file (start here)
├── scenarios/
│   ├── patientsim/            # Clinical/EMR data generation
│   │   ├── diabetes-management.md
│   │   ├── heart-failure.md
│   │   └── ...
│   ├── membersim/             # Claims/payer data generation
│   │   ├── professional-claims.md
│   │   ├── facility-claims.md
│   │   └── ...
│   └── rxmembersim/           # Pharmacy/PBM data generation
│       ├── retail-pharmacy.md
│       ├── dur-alerts.md
│       └── ...
├── formats/                    # Output format transformations
│   ├── fhir-r4.md
│   ├── hl7v2-adt.md
│   ├── x12-837.md
│   ├── dimensional-analytics.md  # DuckDB/Databricks star schemas
│   └── ...
├── references/                 # Code systems and rules
│   ├── data-models.md
│   ├── code-systems.md
│   └── ...
└── hello-healthsim/           # You are here!
```

---

## Next Steps

Once you're comfortable with basic generation:

### Learn More
- [SKILL.md](../SKILL.md) - Complete feature reference
- [examples/](examples/) - Detailed examples with outputs
- [docs/integration-guide.md](../docs/integration-guide.md) - Cross-skill data flows

### Extend HealthSim
- [EXTENDING.md](EXTENDING.md) - Add new scenarios, formats, and code systems

### Get Help
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [GitHub Issues](https://github.com/mark64oswald/healthsim-skills/issues) - Report bugs or request features

---

## Quick Reference Card

### PatientSim (Clinical Data)

| Request | What You Get |
|---------|--------------|
| "diabetic patient" | Patient + diabetes diagnoses + meds + labs |
| "heart failure patient" | Patient + CHF + GDMT medications + BNP |
| "admission for pneumonia" | ADT event + encounter + orders |

### MemberSim (Claims Data)

| Request | What You Get |
|---------|--------------|
| "office visit claim" | 837P professional claim + adjudication |
| "inpatient claim" | 837I facility claim + DRG + payment |
| "denied claim" | Claim + denial reason + appeal info |

### RxMemberSim (Pharmacy Data)

| Request | What You Get |
|---------|--------------|
| "pharmacy claim for metformin" | NCPDP claim + pricing + copay |
| "drug interaction alert" | Claim + DUR response + clinical info |
| "specialty drug claim" | High-cost drug + prior auth + copay assistance |

### Oncology (PatientSim)

| Request | What You Get |
|---------|--------------|
| "breast cancer patient" | Patient + staging + biomarkers + treatment plan |
| "lung cancer EGFR positive" | Patient + molecular testing + targeted therapy |
| "colon cancer MSI-high" | Patient + genomic testing + adjuvant chemo |
| "cancer with comorbidities" | Multi-morbid patient + dose adjustments |

### Format Requests

| Add This | Output Format |
|----------|---------------|
| "as FHIR" | FHIR R4 Bundle |
| "as HL7" | HL7v2 message |
| "as 837" | X12 837 EDI |
| "as CSV" | CSV file format |
| "for DuckDB" | SQL for local analytics |
| "for Databricks" | SQL loaded to Databricks |
| "in star schema" | Dimensional fact/dimension tables |

---

## Success! What Now?

You've just unlocked the ability to generate realistic healthcare test data through conversation. Here are some ideas:

1. **Test Your APIs** - Generate FHIR resources to test your healthcare APIs
2. **Train ML Models** - Create diverse patient populations for training data
3. **Demo Your Product** - Generate realistic scenarios for product demos
4. **Load Test Systems** - Generate bulk data for performance testing
5. **Validate Workflows** - Test claims adjudication and pharmacy workflows

**Happy generating!**

---

*HealthSim is designed for generating synthetic test data only. Never use for actual patient care or real PHI.*
