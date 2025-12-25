# HealthSim Documentation Hub

The complete guide to generating realistic synthetic healthcare data with HealthSim.

---

## The HealthSim Ecosystem

HealthSim is a suite of products for generating synthetic healthcare data through natural conversation with Claude:

```text
                              HealthSim Ecosystem
    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │   ┌─────────────────────────────────────────────────────────┐   │
    │   │              healthsim-workspace (Skills)                │   │
    │   │   Scenarios, Formats, References, Documentation         │   │
    │   └─────────────────────────────────────────────────────────┘   │
    │                              │                                  │
    │   ┌──────────┬───────────────┼───────────────┬──────────┐       │
    │   ▼          ▼               ▼               ▼          ▼       │
    │ ┌────────┐┌────────┐┌──────────────┐┌────────────┐┌─────────┐   │
    │ │Patient ││Member  ││  RxMember    ││  TrialSim  ││ Network │   │
    │ │  Sim   ││  Sim   ││    Sim       ││            ││   Sim   │   │
    │ │Clinical││Claims  ││  Pharmacy    ││  Trials    ││Providers│   │
    │ └────────┘└────────┘└──────────────┘└────────────┘└─────────┘   │
    │              │               │               │                  │
    │              └───────────────┼───────────────┘                  │
    │                              ▼                                  │
    │   ┌─────────────────────────────────────────────────────────┐   │
    │   │              PopulationSim (Data Layer)                  │   │
    │   │   CDC PLACES, SVI, ADI - Embedded Real Population Data  │   │
    │   └─────────────────────────────────────────────────────────┘   │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Repository Overview

This is a **monorepo** containing all HealthSim skills, formats, references, and documentation.

| Component | Location | Description |
|-----------|----------|-------------|
| **Skills** | `skills/` | Product skills (patientsim, membersim, rxmembersim, trialsim, populationsim, networksim) |
| **Formats** | `formats/` | Output transformations (FHIR, HL7v2, X12, NCPDP, CDISC, CSV) |
| **References** | `references/` | Code systems, clinical rules, validation |
| **Getting Started** | `hello-healthsim/` | Tutorials, examples, setup guides |
| **Documentation** | `docs/` | Architecture, guides, processes |
| **Python Core** | `src/healthsim/` | Shared infrastructure |

---

## Quick Start

**New to HealthSim? Start here:**

| Step | Resource | Time |
|------|----------|------|
| 1. Setup | [hello-healthsim/README.md](../hello-healthsim/README.md) | 5 min |
| 2. First generation | [hello-healthsim/examples/](../hello-healthsim/examples/) | 10 min |
| 3. Understand Skills | [SKILL.md](../SKILL.md) | 15 min |
| 4. Explore products | [Product documentation](#documentation-by-product) | As needed |

---

## Documentation by Product

### PatientSim (Clinical Data)

| Document | Description |
|----------|-------------|
| [skills/patientsim/README.md](../skills/patientsim/README.md) | Product overview |
| [skills/patientsim/SKILL.md](../skills/patientsim/SKILL.md) | Complete skill reference |
| [hello-healthsim/examples/patientsim-examples.md](../hello-healthsim/examples/patientsim-examples.md) | Examples |

### MemberSim (Claims Data)

| Document | Description |
|----------|-------------|
| [skills/membersim/README.md](../skills/membersim/README.md) | Product overview |
| [skills/membersim/SKILL.md](../skills/membersim/SKILL.md) | Complete skill reference |
| [hello-healthsim/examples/membersim-examples.md](../hello-healthsim/examples/membersim-examples.md) | Examples |

### RxMemberSim (Pharmacy Data)

| Document | Description |
|----------|-------------|
| [skills/rxmembersim/README.md](../skills/rxmembersim/README.md) | Product overview |
| [skills/rxmembersim/SKILL.md](../skills/rxmembersim/SKILL.md) | Complete skill reference |
| [hello-healthsim/examples/rxmembersim-examples.md](../hello-healthsim/examples/rxmembersim-examples.md) | Examples |

### TrialSim (Clinical Trials)

| Document | Description |
|----------|-------------|
| [skills/trialsim/README.md](../skills/trialsim/README.md) | Product overview |
| [skills/trialsim/SKILL.md](../skills/trialsim/SKILL.md) | Complete skill reference |
| [hello-healthsim/examples/trialsim-examples.md](../hello-healthsim/examples/trialsim-examples.md) | Examples |

### PopulationSim (Demographics & SDOH)

| Document | Description |
|----------|-------------|
| [skills/populationsim/README.md](../skills/populationsim/README.md) | Product overview |
| [skills/populationsim/SKILL.md](../skills/populationsim/SKILL.md) | Complete skill reference |
| [skills/populationsim/data/README.md](../skills/populationsim/data/README.md) | Embedded data package |
| [hello-healthsim/examples/populationsim-examples.md](../hello-healthsim/examples/populationsim-examples.md) | Examples |

### NetworkSim (Provider Networks)

| Document | Description |
|----------|-------------|
| [skills/networksim/README.md](../skills/networksim/README.md) | Product overview |
| [skills/networksim/SKILL.md](../skills/networksim/SKILL.md) | Complete skill reference |
| [networksim-dual-version.md](networksim-dual-version.md) | Public vs private versions |
| [hello-healthsim/examples/networksim-examples.md](../hello-healthsim/examples/networksim-examples.md) | Examples |

---

## Documentation by Topic

### Getting Started

| Document | Description |
|----------|-------------|
| [hello-healthsim/README.md](../hello-healthsim/README.md) | Quick start guide |
| [hello-healthsim/CLAUDE-DESKTOP.md](../hello-healthsim/CLAUDE-DESKTOP.md) | Claude Desktop setup |
| [hello-healthsim/CLAUDE-CODE.md](../hello-healthsim/CLAUDE-CODE.md) | Claude Code CLI setup |
| [hello-healthsim/TROUBLESHOOTING.md](../hello-healthsim/TROUBLESHOOTING.md) | Common issues & fixes |
| [hello-healthsim/EXTENDING.md](../hello-healthsim/EXTENDING.md) | How to extend HealthSim |

### Output Formats

| Document | Formats |
|----------|---------|
| [formats/fhir-r4.md](../formats/fhir-r4.md) | FHIR R4, NDJSON |
| [formats/hl7v2-adt.md](../formats/hl7v2-adt.md) | HL7v2 ADT messages |
| [formats/x12-837.md](../formats/x12-837.md) | X12 837 claims |
| [formats/x12-835.md](../formats/x12-835.md) | X12 835 remittance |
| [formats/ncpdp-d0.md](../formats/ncpdp-d0.md) | NCPDP D.0 pharmacy |
| [formats/cdisc-sdtm.md](../formats/cdisc-sdtm.md) | CDISC SDTM |
| [formats/cdisc-adam.md](../formats/cdisc-adam.md) | CDISC ADaM |
| [formats/dimensional-analytics.md](../formats/dimensional-analytics.md) | Star schema |

### Reference Data

| Document | Description |
|----------|-------------|
| [references/data-models.md](../references/data-models.md) | Entity schemas |
| [references/code-systems.md](../references/code-systems.md) | ICD-10, CPT, LOINC, NDC |
| [references/clinical-rules.md](../references/clinical-rules.md) | Clinical business rules |

### Architecture & Development

| Document | Description |
|----------|-------------|
| [product-architecture.md](product-architecture.md) | Visual product relationships and workflows |
| [HEALTHSIM-ARCHITECTURE-GUIDE.md](HEALTHSIM-ARCHITECTURE-GUIDE.md) | Complete architecture guide |
| [HEALTHSIM-DEVELOPMENT-PROCESS.md](HEALTHSIM-DEVELOPMENT-PROCESS.md) | Development workflow |
| [skills/format-specification-v2.md](skills/format-specification-v2.md) | Skills format specification |
| [skills-template.md](skills-template.md) | SKILL.md template |
| [contributing.md](contributing.md) | Contribution guidelines |

---

## Examples by Use Case

| I want to... | Example Location |
|--------------|------------------|
| Generate a patient | [patientsim-examples.md](../hello-healthsim/examples/patientsim-examples.md) |
| Generate a claim | [membersim-examples.md](../hello-healthsim/examples/membersim-examples.md) |
| Generate pharmacy data | [rxmembersim-examples.md](../hello-healthsim/examples/rxmembersim-examples.md) |
| Generate trial data | [trialsim-examples.md](../hello-healthsim/examples/trialsim-examples.md) |
| Analyze population data | [populationsim-examples.md](../hello-healthsim/examples/populationsim-examples.md) |
| Generate provider networks | [networksim-examples.md](../hello-healthsim/examples/networksim-examples.md) |
| Generate cross-domain data | [cross-domain-examples.md](../hello-healthsim/examples/cross-domain-examples.md) |

---

## Navigation by Role

### For Users (generating data)

1. [Quick Start](../hello-healthsim/README.md) - Get set up
2. [SKILL.md](../SKILL.md) - Understand what you can generate
3. [Examples](../hello-healthsim/examples/) - Copy-paste prompts
4. [Troubleshooting](../hello-healthsim/TROUBLESHOOTING.md) - Fix issues

### For Developers (extending HealthSim)

1. [Extension Guide](../hello-healthsim/EXTENDING.md) - How to extend
2. [Skills Template](skills-template.md) - Create new skills
3. [Architecture Guide](HEALTHSIM-ARCHITECTURE-GUIDE.md) - System design
4. [Contributing](contributing.md) - Submit changes

---

## Getting Help

| Resource | Use For |
|----------|---------|
| [Troubleshooting Guide](../hello-healthsim/TROUBLESHOOTING.md) | Common issues |
| [GitHub Issues](https://github.com/mark64oswald/healthsim-workspace/issues) | Bug reports, feature requests |

---

*HealthSim generates synthetic test data only. Never use for actual patient care or real PHI.*
