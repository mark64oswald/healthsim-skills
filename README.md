# HealthSim Workspace

**The unified repository for the HealthSim product family.**

This repository contains everything for HealthSim:
- **Skills** - Structured markdown documents that Claude uses to generate clinically coherent healthcare data
- **Formats** - Output transformation specs (FHIR, C-CDA, HL7v2, X12, NCPDP, CDISC)
- **References** - Shared terminology, code systems, and clinical rules
- **Packages** - Python infrastructure (MCP servers, validation, dimensional output)

---

## Quick Start

**New to HealthSim?** Start here: **[hello-healthsim/](hello-healthsim/README.md)**

The getting started guide includes:
- Installation and configuration
- Your first 5 minutes with HealthSim
- Detailed examples for all products
- How to extend the framework

---

## What Can HealthSim Generate?

| Product | What It Creates | Example Request |
|---------|-----------------|-----------------|
| **PatientSim** | Clinical/EMR data | "Generate a 65-year-old diabetic with recent labs" |
| **MemberSim** | Claims/payer data | "Generate a denied MRI claim requiring prior auth" |
| **RxMemberSim** | Pharmacy/PBM data | "Generate a drug interaction alert for warfarin" |

### Clinical Domains

| Domain | Scenario | Example Use Cases |
|--------|----------|-------------------|
| **Diabetes** | diabetes-management.md | Type 1/2, A1C monitoring, insulin therapy, complications |
| **Heart Failure** | heart-failure.md | HFrEF/HFpEF, NYHA staging, GDMT, decompensation |
| **Chronic Kidney Disease** | chronic-kidney-disease.md | CKD stages 1-5, dialysis, transplant, comorbidities |
| **Oncology** | oncology/*.md | Breast, lung, colorectal cancer; staging, chemo, biomarkers |
| **Maternal Health** | maternal-health.md | Prenatal care, GDM, preeclampsia, L&D, postpartum |
| **Behavioral Health** | behavioral-health.md | Depression, anxiety, SUD, psychotherapy, PHP/IOP |
| **Acute Care** | sepsis-acute-care.md | Sepsis, ICU, antibiotics, critical care |
| **Emergency** | ed-chest-pain.md | Chest pain, ACS workup, HEART score, troponin |
| **Surgical** | elective-joint.md | Hip/knee replacement, pre-op, post-op, PT |
| **ADT Workflows** | adt-workflow.md | Admission, transfer, discharge, bed management |

### Output Formats

| Format | Request With | Use Case |
|--------|--------------|----------|
| JSON | (default) | API testing, general use |
| FHIR R4 | "as FHIR", "as FHIR Bundle" | Modern interoperability |
| C-CDA | "as C-CDA", "as CCD" | Clinical documents, HIE |
| HL7v2 | "as HL7", "as ADT message" | Legacy EMR integration |
| X12 837/835 | "as 837", "as X12 claim" | Claims submission |
| X12 834 | "as 834", "enrollment file" | Benefit enrollment |
| NCPDP D.0 | "as NCPDP" | Pharmacy transactions |
| CSV | "as CSV" | Analytics, spreadsheets |
| SQL | "as SQL" | Database loading |

---

## Repository Structure

```
healthsim-common/
├── SKILL.md                    # Master skill file (start here)
├── README.md                   # This file
│
├── hello-healthsim/            # Getting started guide
│   ├── README.md              # Quick start
│   ├── CLAUDE-DESKTOP.md      # Claude Desktop setup
│   ├── CLAUDE-CODE.md         # Claude Code CLI setup
│   ├── EXTENDING.md           # How to customize
│   ├── TROUBLESHOOTING.md     # Common issues
│   └── examples/              # Detailed examples
│
├── skills/                  # Domain-specific generation
│   ├── patientsim/            # Clinical data (9 scenarios + 3 oncology)
│   │   ├── SKILL.md
│   │   ├── diabetes-management.md
│   │   ├── heart-failure.md
│   │   ├── maternal-health.md
│   │   ├── oncology/          # Cancer-specific scenarios
│   │   └── ...
│   ├── membersim/             # Claims data (8 scenarios)
│   │   ├── SKILL.md
│   │   ├── professional-claims.md
│   │   ├── behavioral-health.md
│   │   └── ...
│   └── rxmembersim/           # Pharmacy data (8 scenarios)
│       ├── SKILL.md
│       ├── retail-pharmacy.md
│       ├── specialty-pharmacy.md
│       └── ...
│
├── formats/                    # Output transformations (12 files)
│   ├── fhir-r4.md
│   ├── ccda-format.md
│   ├── hl7v2-adt.md
│   ├── x12-837.md
│   └── ...
│
├── references/                 # Shared knowledge (11 files + subdirs)
│   ├── data-models.md         # Entity schemas
│   ├── code-systems.md        # ICD-10, CPT, LOINC, NDC
│   ├── clinical-rules.md      # Clinical business rules
│   ├── pediatric-dosing.md    # Pediatric medication dosing
│   ├── mental-health-reference.md  # Behavioral health codes
│   ├── oncology/              # Oncology reference data
│   └── ccda/                   # C-CDA template references
│
├── docs/                       # Shared developer documentation
│   ├── README.md              # Documentation index
│   ├── architecture/          # System architecture
│   ├── mcp/                   # MCP integration
│   ├── state-management/      # State management
│   ├── skills/                # Skills format specs
│   ├── extensions/            # Extension guides
│   └── contributing.md        # Contribution guidelines
│
├── src/healthsim/              # Core Python modules
│   ├── benefits/              # Accumulator tracking (deductibles, OOPM)
│   ├── config/                # Settings and logging
│   ├── dimensional/           # Data warehouse output (DuckDB, Databricks)
│   ├── formats/               # Format base classes
│   ├── generation/            # Distributions, reproducibility, cohorts
│   ├── person/                # Demographics and identifiers
│   ├── state/                 # Workspace persistence and provenance
│   ├── temporal/              # Timeline and period utilities
│   └── validation/            # Validation framework
│
├── tests/                      # Python test suite (476 tests)
│
└── pyproject.toml             # Python package config
```

---

## Example Usage

### Basic Examples (Start Here)

```
Generate a patient
Generate a professional claim for an office visit
Generate a pharmacy claim for metformin
```

### Clinical Domain Examples

| Domain | Example Prompt |
|--------|----------------|
| **Diabetes** | "Generate a 62-year-old with poorly controlled Type 2 diabetes and A1C of 9.5" |
| **Heart Failure** | "Generate a patient with HFrEF, NYHA Class III, on GDMT therapy" |
| **CKD** | "Generate a patient with Stage 4 CKD and diabetes" |
| **Oncology** | "Generate a Stage IIB ER-positive breast cancer patient with treatment plan" |
| **Maternal** | "Generate a 32-week pregnant patient with gestational diabetes" |
| **Behavioral** | "Generate a telehealth psychotherapy claim for depression" |
| **Emergency** | "Generate an ED chest pain patient with HEART score workup" |

### Claims & Pharmacy Examples

| Type | Example Prompt |
|------|----------------|
| **Paid Claim** | "Generate a paid professional claim for an office visit" |
| **Denied Claim** | "Generate a denied MRI claim requiring prior authorization" |
| **Facility Claim** | "Generate an inpatient heart failure admission with DRG" |
| **DUR Alert** | "Generate a pharmacy claim with drug-drug interaction alert" |
| **Prior Auth** | "Generate a PA approval workflow for specialty drug" |

### Output Format Examples

| Format | Example Prompt |
|--------|----------------|
| **FHIR** | "Generate a diabetic patient as a FHIR Bundle" |
| **C-CDA** | "Generate a discharge summary as C-CDA" |
| **HL7v2** | "Generate an admission as an ADT A01 message" |
| **X12 837** | "Generate a professional claim as X12 837P" |

### Cross-Domain Scenarios

```
Generate a diabetic patient with their office visit claim and metformin pharmacy claim
Generate a breast cancer patient with infusion facility claim and oral chemo pharmacy claim
Generate a heart failure patient with hospital admission, follow-up visit, and discharge medications
```

See [hello-healthsim/examples/](hello-healthsim/examples/) for detailed examples with expected outputs.

---

## Key Features

### Clinical Coherence
- Diagnoses appropriate for age and gender
- Medications match conditions
- Lab values correlate with disease state
- Comorbidities follow real-world patterns

### Proper Healthcare Codes
- ICD-10-CM diagnosis codes
- CPT/HCPCS procedure codes
- LOINC lab codes
- NDC drug codes
- RxNorm medication codes

### Realistic Business Logic
- Claims adjudication with proper CARC/RARC codes
- Deductible and OOP accumulator tracking
- Prior authorization workflows
- DUR alerts and overrides
- Formulary tier pricing

### Multiple Output Formats
- FHIR R4 resources and bundles
- HL7v2 messages (ADT, ORM, ORU)
- X12 transactions (834, 837, 835, 270/271)
- NCPDP pharmacy claims
- CSV for analytics

---

## Configuration

### Claude Desktop

Add SKILL.md to a Claude Project, or configure as MCP server:

```json
{
  "mcpServers": {
    "healthsim": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/healthsim-common"]
    }
  }
}
```

### Claude Code

Run from the healthsim-common directory:

```bash
cd healthsim-common
claude
```

See [hello-healthsim/](hello-healthsim/) for detailed setup instructions.

---

## Use Cases

- **API Testing** - Generate FHIR resources to test healthcare APIs
- **Training Data** - Create diverse patient populations for ML models
- **Product Demos** - Generate realistic scenarios for demonstrations
- **Load Testing** - Bulk data generation for performance testing
- **Workflow Validation** - Test claims processing and pharmacy workflows
- **Education** - Learn healthcare data structures and relationships

---

## Documentation

### Getting Started
- **[hello-healthsim/](hello-healthsim/)** - 5-minute quick start for all products
- **[SKILL.md](SKILL.md)** - Master skill file with full reference

### Developer Documentation (Shared Across Products)
- **[MCP Integration](docs/mcp/integration-guide.md)** - MCP server integration guide
- **[State Management](docs/state-management/user-guide.md)** - Save/load and session management
- **[Extension Philosophy](docs/extensions/philosophy.md)** - How to extend HealthSim
- **[Skills Format](docs/skills/format-specification-v2.md)** - Skills format specification
- **[Quick Reference](docs/extensions/quick-reference.md)** - Fast lookup for all extension types
- **[Contributing](docs/contributing.md)** - Development guidelines

### Reference
- **[skills/](skills/)** - Clinical scenarios organized by product
- **[formats/](formats/)** - Output format transformations (FHIR, HL7v2, X12, NCPDP)
- **[references/](references/)** - Code systems, clinical rules, terminology

### Architecture
- **[Layered Architecture](docs/architecture/layered-pattern.md)** - System design patterns
- **[HealthSim Core Spec](docs/architecture/healthsim-common-spec.md)** - Shared infrastructure specification

---

## Contributing

See [hello-healthsim/EXTENDING.md](hello-healthsim/EXTENDING.md) for how to add new scenarios, formats, and code systems.

For detailed development guidelines, see [docs/contributing.md](docs/contributing.md).

---

## License

MIT

---

## Links

- [Getting Started Guide](hello-healthsim/README.md)
- [Full Reference (SKILL.md)](SKILL.md)
- [HL7 FHIR R4](https://hl7.org/fhir/R4/)
- [X12 Standards](https://x12.org/)
- [NCPDP Standards](https://www.ncpdp.org/)

---

*HealthSim generates synthetic test data only. Never use for actual patient care or real PHI.*
