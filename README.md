# HealthSim Skills

**Generate realistic synthetic healthcare data through natural conversation with Claude.**

A Skills-first synthetic healthcare data generation system. This repository replaces traditional Python libraries with Claude Skills - structured markdown documents that Claude uses to generate clinically coherent, realistic healthcare data.

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

### Output Formats

| Format | Request With |
|--------|--------------|
| JSON | (default) |
| FHIR R4 | "as FHIR", "as FHIR Bundle" |
| HL7v2 | "as HL7", "as ADT message" |
| X12 837/835 | "as 837", "as X12 claim" |
| NCPDP D.0 | "as NCPDP" |
| CSV | "as CSV" |

---

## Repository Structure

```
healthsim-skills/
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
├── scenarios/                  # Domain-specific generation
│   ├── patientsim/            # Clinical data (6 scenarios)
│   │   ├── SKILL.md
│   │   ├── diabetes-management.md
│   │   ├── heart-failure.md
│   │   └── ...
│   ├── membersim/             # Claims data (7 scenarios)
│   │   ├── SKILL.md
│   │   ├── professional-claims.md
│   │   ├── value-based-care.md
│   │   └── ...
│   └── rxmembersim/           # Pharmacy data (8 scenarios)
│       ├── SKILL.md
│       ├── retail-pharmacy.md
│       ├── manufacturer-programs.md
│       └── ...
│
├── formats/                    # Output transformations (11 files)
│   ├── fhir-r4.md
│   ├── hl7v2-adt.md
│   ├── x12-837.md
│   └── ...
│
├── references/                 # Shared knowledge (5 files)
│   ├── data-models.md         # Entity schemas
│   ├── code-systems.md        # ICD-10, CPT, LOINC, NDC
│   ├── clinical-rules.md      # Clinical business rules
│   ├── validation-rules.md    # Data validation
│   └── terminology.md         # Abbreviations reference
│
└── docs/                       # Additional documentation
    ├── integration-guide.md
    └── testing-patterns.md
```

---

## Example Usage

### Simple Patient Generation

```
Generate a patient with Type 2 diabetes
```

```json
{
  "patient": {
    "mrn": "MRN00000001",
    "name": { "given_name": "Maria", "family_name": "Garcia" },
    "birth_date": "1965-08-22",
    "gender": "F"
  },
  "diagnoses": [
    { "code": "E11.9", "description": "Type 2 diabetes mellitus without complications" }
  ],
  "medications": [
    { "name": "Metformin", "dose": "1000 mg", "frequency": "BID" }
  ],
  "labs": [
    { "test": "HbA1c", "value": "7.2", "unit": "%" }
  ]
}
```

### Claims with Adjudication

```
Generate a paid professional claim for an office visit with deductible applied
```

### Pharmacy with DUR Alert

```
Generate a pharmacy claim that triggers a drug-drug interaction alert
```

### Cross-Domain Scenario

```
Generate a heart failure patient with their hospital admission claim and discharge medications
```

See [hello-healthsim/examples/](hello-healthsim/examples/) for many more examples.

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
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/healthsim-skills"]
    }
  }
}
```

### Claude Code

Run from the healthsim-skills directory:

```bash
cd healthsim-skills
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

## Contributing

See [hello-healthsim/EXTENDING.md](hello-healthsim/EXTENDING.md) for how to add new scenarios, formats, and code systems.

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
