# HealthSim Workspace

**Synthetic healthcare data generation through natural language conversation.**

HealthSim generates realistic, clinically coherent healthcare data for testing, training, and development—from simple patient records to complete care journeys spanning clinical, claims, pharmacy, and clinical trial domains.

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

## Getting Started

New to HealthSim? Start here:

| Resource | Description |
|----------|-------------|
| **[Hello HealthSim](hello-healthsim/README.md)** | Quick start guide with setup instructions and first steps |
| **[Examples by Product](hello-healthsim/examples/)** | Detailed examples with expected outputs for each product |
| **[Extending HealthSim](hello-healthsim/EXTENDING.md)** | How to add new clinical scenarios, skills, and output formats |

The examples folder contains ready-to-use prompts organized by product:
- [PatientSim Examples](hello-healthsim/examples/patientsim-examples.md) - Clinical data generation
- [MemberSim Examples](hello-healthsim/examples/membersim-examples.md) - Claims and payer data
- [RxMemberSim Examples](hello-healthsim/examples/rxmembersim-examples.md) - Pharmacy data
- [TrialSim Examples](hello-healthsim/examples/trialsim-examples.md) - Clinical trial data
- [PopulationSim Examples](hello-healthsim/examples/populationsim-examples.md) - Demographics and SDOH
- [NetworkSim Examples](hello-healthsim/examples/networksim-examples.md) - Provider networks

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

## State Management

HealthSim includes a state management system for persisting and restoring workspaces:

| Feature | Description |
|---------|-------------|
| **Scenario Storage** | Named snapshots saved to DuckDB database |
| **Provenance Tracking** | Records how each entity was created |
| **JSON Export/Import** | Share scenarios as portable JSON files |
| **SQL Queries** | Advanced users can query scenarios directly |

**Tools:**
- `save_scenario` - Save workspace to named scenario
- `load_scenario` - Restore workspace from scenario
- `list_scenarios` - List saved scenarios with optional filtering
- `export_scenario_to_json` - Export for sharing
- `import_scenario_from_json` - Import shared scenarios

See [State Management Guide](docs/state-management/) | [Data Architecture](docs/data-architecture.md)

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
├── packages/                   # Python infrastructure
│   ├── core/                  # Shared healthsim-core library
│   ├── patientsim/            # PatientSim package
│   ├── membersim/             # MemberSim package
│   └── rxmembersim/           # RxMemberSim package
└── scripts/                    # Utility scripts and tests
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
| Data Architecture | [docs/data-architecture.md](docs/data-architecture.md) |
| Architecture Guide | [docs/HEALTHSIM-ARCHITECTURE-GUIDE.md](docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) |
| State Management | [docs/state-management/](docs/state-management/) |
| Extension Guide | [hello-healthsim/EXTENDING.md](hello-healthsim/EXTENDING.md) |
| Skills Format Spec | [docs/skills/format-specification-v2.md](docs/skills/format-specification-v2.md) |
| Contributing | [docs/contributing.md](docs/contributing.md) |

---

## Key Features

- **Clinical Coherence**: Age/gender-appropriate conditions, medications match diagnoses, labs correlate with disease state
- **Proper Healthcare Codes**: ICD-10, CPT, LOINC, NDC, RxNorm, MedDRA, taxonomy codes
- **Realistic Business Logic**: Claims adjudication, accumulators, prior auth, DUR alerts, formulary tiers
- **Data-Driven Generation**: Ground synthetic data in real CDC/Census population statistics (via PopulationSim)
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
