# HealthSim Workspace

**Synthetic healthcare data generation through natural language conversation.**

HealthSim generates realistic, clinically coherent healthcare data for testing, training, and development—from simple patient records to complete care journeys spanning clinical, claims, pharmacy, and clinical trial domains.

---

## I Want To...

| Goal | Start Here | Products Used |
|------|------------|---------------|
| **Get started quickly** | [hello-healthsim/](hello-healthsim/README.md) | All products |
| **Generate patient clinical data** | [PatientSim SKILL.md](skills/patientsim/SKILL.md) | PatientSim |
| **Generate claims/billing data** | [MemberSim SKILL.md](skills/membersim/SKILL.md) | MemberSim |
| **Generate pharmacy data** | [RxMemberSim SKILL.md](skills/rxmembersim/SKILL.md) | RxMemberSim |
| **Generate clinical trial data** | [TrialSim SKILL.md](skills/trialsim/SKILL.md) | TrialSim |
| **Analyze population demographics** | [PopulationSim SKILL.md](skills/populationsim/SKILL.md) | PopulationSim |
| **Generate provider networks** | [NetworkSim SKILL.md](skills/networksim/SKILL.md) | NetworkSim |
| **Generate a complete patient journey** | [Product Architecture](docs/product-architecture.md#common-workflows) | Multiple |
| **Use real geographic health data** | [PopulationSim v2.0](#populationsim-v20---data-driven-generation) | PopulationSim + others |
| **Generate patient + claims together** | [Product Architecture](docs/product-architecture.md#2-patient-with-claims) | PatientSim + MemberSim |
| **Plan a clinical trial** | [TrialSim SKILL.md](skills/trialsim/SKILL.md#trial-support) | TrialSim + PopulationSim |
| **Output as FHIR/HL7/X12** | [Output Formats](#output-formats) | Any product |
| **Extend or customize** | [EXTENDING.md](hello-healthsim/EXTENDING.md) | Framework |

---

## Products Overview

| Product | What It Generates | Key Scenarios | Standards |
|---------|-------------------|---------------|-----------|
| **[PatientSim](skills/patientsim/README.md)** | Clinical/EMR data | Diabetes, heart failure, oncology, maternal, behavioral health | FHIR R4, HL7v2, C-CDA |
| **[MemberSim](skills/membersim/README.md)** | Claims/payer data | Professional claims, facility claims, prior auth, accumulators | X12 837/835/834 |
| **[RxMemberSim](skills/rxmembersim/README.md)** | Pharmacy/PBM data | Retail fills, specialty drugs, DUR alerts, manufacturer programs | NCPDP D.0 |
| **[TrialSim](skills/trialsim/README.md)** | Clinical trial data | Phase I-III, adverse events, efficacy endpoints, SDTM domains | CDISC SDTM/ADaM |
| **[PopulationSim](skills/populationsim/README.md)** | Demographics/SDOH | County profiles, health disparities, cohort specifications | Census, CDC PLACES |
| **[NetworkSim](skills/networksim/README.md)** | Provider networks | Providers, facilities, pharmacies, network configurations | NPPES, NPI |

---

## Quick Examples

```plaintext
# Basic
Generate a patient
Generate a professional claim for an office visit
Generate a pharmacy claim for metformin

# Clinical scenarios
Generate a 65-year-old diabetic with HFpEF and CKD Stage 3
Generate a denied MRI claim requiring prior authorization
Generate a drug-drug interaction alert for warfarin and aspirin

# Clinical trials
Generate a Phase III oncology trial with 200 subjects as SDTM
Generate adverse events for an immunotherapy trial with MedDRA coding

# Data-driven (with PopulationSim v2.0)
Generate 50 diabetic patients for Harris County, TX with real prevalence data
Profile San Diego County health indicators and SDOH factors

# Output formats
Generate a diabetic patient as FHIR Bundle
Generate an inpatient admission as ADT A01 HL7v2 message
Generate a professional claim as X12 837P
```

See [hello-healthsim/examples/](hello-healthsim/examples/) for detailed examples with expected outputs.

---

## PopulationSim v2.0 - Data-Driven Generation

**NEW**: PopulationSim v2.0 embeds 148 MB of real CDC/Census data, enabling **evidence-based synthetic data generation** grounded in actual population statistics.

| Data Source | Coverage | Records | Key Use |
|-------------|----------|---------|---------|
| CDC PLACES 2024 | 100% US counties + tracts | 86,665 | Disease prevalence (40 measures) |
| CDC SVI 2022 | 100% US counties + tracts | 87,264 | Social vulnerability (16 indicators) |
| HRSA ADI 2023 | 100% US block groups | 242,336 | Area deprivation |

**What This Enables:**

```plaintext
# Instead of generic data:
"Generate 10 diabetic patients" → Generic 10.2% national prevalence

# With PopulationSim v2.0:
"Generate 10 diabetic patients in Harris County, TX" →
  - Uses actual 12.1% diabetes rate from CDC PLACES
  - Applies 72% minority population from SVI  
  - Includes real comorbidity correlations
  - Tracks data provenance in output
```

**Cross-Product Data Flow**: PopulationSim data grounds generation in PatientSim (demographics, conditions), MemberSim (utilization, risk), RxMemberSim (adherence), and TrialSim (feasibility, diversity).

See: [PopulationSim SKILL.md](skills/populationsim/SKILL.md) | [Data Package README](skills/populationsim/data/README.md)

---

## Cross-Product Integration

HealthSim products work together to generate complete healthcare data journeys:

```
Person (Base Identity)
   │
   ├── PatientSim → Patient → Clinical encounters, labs, meds
   │        ↓
   ├── MemberSim → Member → Claims, adjudication, accumulators  
   │        ↓
   ├── RxMemberSim → RxMember → Pharmacy claims, DUR, formulary
   │
   └── TrialSim → Subject → Protocol visits, AEs, efficacy (if enrolled)

   NetworkSim provides: Providers, facilities, pharmacies for all products
   PopulationSim provides: Demographics, health rates, SDOH for all products
```

**Example: Heart Failure Patient Journey**

| Day | Product | Event | Output |
|-----|---------|-------|--------|
| 0 | PatientSim | ED visit, HF diagnosis | Encounter, labs, meds |
| 3 | PatientSim | Inpatient discharge | Discharge summary |
| 5 | MemberSim | Facility claim | 837I (DRG 291) |
| 3 | RxMemberSim | Discharge Rx fills | NCPDP claims |
| 30 | PatientSim | Cardiology follow-up | Office encounter |
| 32 | MemberSim | Professional claim | 837P (99214) |

See [Cross-Product Integration Guide](docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#83-cross-product-integration) | [Product Architecture Diagrams](docs/product-architecture.md)

---

## Output Formats

| Format | Request With | Use Case | Products |
|--------|--------------|----------|----------|
| JSON | (default) | API testing | All |
| FHIR R4 | "as FHIR" | Interoperability | PatientSim |
| C-CDA | "as C-CDA" | Clinical documents | PatientSim |
| HL7v2 | "as HL7", "as ADT" | Legacy EMR | PatientSim |
| X12 837/835 | "as 837", "as X12" | Claims | MemberSim |
| X12 834 | "as 834" | Enrollment | MemberSim |
| NCPDP D.0 | "as NCPDP" | Pharmacy | RxMemberSim |
| CDISC SDTM | "as SDTM" | Trial submission | TrialSim |
| CDISC ADaM | "as ADaM" | Trial analysis | TrialSim |
| Star Schema | "as star schema" | BI analytics | All |
| CSV | "as CSV" | Spreadsheets | All |

See [formats/](formats/) for transformation specifications.

---

## Clinical Scenarios

### PatientSim Scenarios

| Domain | Skill | Key Use Cases |
|--------|-------|---------------|
| Diabetes | [diabetes-management.md](skills/patientsim/diabetes-management.md) | Type 1/2, A1C, insulin, complications |
| Heart Failure | [heart-failure.md](skills/patientsim/heart-failure.md) | HFrEF/HFpEF, NYHA, GDMT |
| CKD | [chronic-kidney-disease.md](skills/patientsim/chronic-kidney-disease.md) | Stages 1-5, dialysis |
| Oncology | [oncology/](skills/patientsim/oncology/) | Breast, lung, colorectal cancer |
| Maternal | [maternal-health.md](skills/patientsim/maternal-health.md) | Prenatal, GDM, preeclampsia |
| Behavioral | [behavioral-health.md](skills/patientsim/behavioral-health.md) | Depression, anxiety, SUD |
| Acute Care | [sepsis-acute-care.md](skills/patientsim/sepsis-acute-care.md) | Sepsis, ICU |
| Pediatrics | [pediatrics/](skills/patientsim/pediatrics/) | Asthma, otitis media |

### TrialSim Scenarios

| Domain | Skill | Key Use Cases |
|--------|-------|---------------|
| Phase 1 | [phase1-dose-escalation.md](skills/trialsim/phase1-dose-escalation.md) | FIH, 3+3, BOIN, MTD |
| Phase 2 | [phase2-proof-of-concept.md](skills/trialsim/phase2-proof-of-concept.md) | Simon's, futility |
| Phase 3 | [phase3-pivotal.md](skills/trialsim/phase3-pivotal.md) | Registration trials |
| SDTM Domains | [domains/](skills/trialsim/domains/) | DM, AE, VS, LB, CM, EX, DS |
| Therapeutic | [therapeutic-areas/](skills/trialsim/therapeutic-areas/) | Oncology, CV, CNS, CGT |

---

## Repository Structure

```
healthsim-workspace/
├── SKILL.md                    # Master skill file (Claude entry point)
├── README.md                   # This file
│
├── hello-healthsim/            # Getting started (tutorials, setup)
│   ├── README.md              # Quick start guide
│   └── examples/              # Detailed examples by product
│
├── skills/                     # Product skills (domain knowledge)
│   ├── patientsim/            # Clinical/EMR (12 scenarios)
│   ├── membersim/             # Claims/payer (8 scenarios)
│   ├── rxmembersim/           # Pharmacy/PBM (8 scenarios)
│   ├── trialsim/              # Clinical trials (20+ skills)
│   ├── populationsim/         # Demographics/SDOH + embedded data
│   └── networksim/            # Provider networks
│
├── formats/                    # Output transformations (12 formats)
├── references/                 # Shared terminology, code systems
├── docs/                       # Architecture, guides, processes
├── src/healthsim/              # Python infrastructure
└── tests/                      # Test suite (476 tests)
```

---

## Setup

### Claude Desktop (Recommended)

Add to a Claude Project or configure as MCP server:

```json
{
  "mcpServers": {
    "healthsim": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/healthsim-workspace"]
    }
  }
}
```

### Claude Code

```bash
cd healthsim-workspace
claude
```

See [hello-healthsim/](hello-healthsim/) for detailed setup instructions.

---

## Use Cases

| Use Case | Description |
|----------|-------------|
| **API Testing** | Generate FHIR resources, X12 transactions, NCPDP claims |
| **Training Data** | Create diverse patient populations for ML models |
| **Product Demos** | Generate realistic scenarios for demonstrations |
| **Load Testing** | Bulk data generation for performance testing |
| **Workflow Validation** | Test claims processing, pharmacy adjudication |
| **Education** | Learn healthcare data structures and relationships |
| **Trial Planning** | Feasibility analysis, site selection, diversity planning |

---

## Documentation

| Topic | Location |
|-------|----------|
| Quick Start | [hello-healthsim/](hello-healthsim/README.md) |
| Master Skill Reference | [SKILL.md](SKILL.md) |
| Product Architecture | [docs/product-architecture.md](docs/product-architecture.md) |
| Architecture Guide | [docs/HEALTHSIM-ARCHITECTURE-GUIDE.md](docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) |
| Extension Guide | [hello-healthsim/EXTENDING.md](hello-healthsim/EXTENDING.md) |
| Skills Format Spec | [docs/skills/format-specification-v2.md](docs/skills/format-specification-v2.md) |
| Contributing | [docs/contributing.md](docs/contributing.md) |

---

## Key Features

- **Clinical Coherence**: Age/gender-appropriate conditions, medications match diagnoses, labs correlate with disease state
- **Proper Healthcare Codes**: ICD-10, CPT, LOINC, NDC, RxNorm, MedDRA, taxonomy codes
- **Realistic Business Logic**: Claims adjudication, accumulators, prior auth, DUR alerts, formulary tiers
- **Data-Driven Generation**: Ground synthetic data in real CDC/Census population statistics
- **Multiple Output Formats**: FHIR, HL7v2, C-CDA, X12, NCPDP, CDISC SDTM/ADaM

---

## Links

- [Getting Started](hello-healthsim/README.md)
- [Full Reference (SKILL.md)](SKILL.md)
- [HL7 FHIR R4](https://hl7.org/fhir/R4/)
- [X12 Standards](https://x12.org/)
- [NCPDP Standards](https://www.ncpdp.org/)
- [CDISC Standards](https://www.cdisc.org/)

---

*HealthSim generates synthetic test data only. Never use for actual patient care or real PHI.*
