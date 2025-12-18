# HealthSim Architecture Guide

**Version**: 2.0  
**Last Updated**: 2025-12-17  
**Purpose**: Authoritative reference for HealthSim architecture, patterns, and conventions.

---

## Table of Contents

1. [Philosophy](#1-philosophy)
2. [Product Family](#2-product-family)
3. [Architecture Layers](#3-architecture-layers)
4. [Directory Organization](#4-directory-organization)
5. [Skills Architecture](#5-skills-architecture)
6. [Canonical Data Models](#6-canonical-data-models)
7. [Output Formats](#7-output-formats)
8. [MCP Integration](#8-mcp-integration)
9. [Cross-Product Patterns](#9-cross-product-patterns)
10. [Extension Patterns](#10-extension-patterns)

---

## 1. Philosophy

### 1.1 Core Principles

**Conversation-First / Configuration via Conversation**
```
Traditional:  User → Code → Library → Models → Output
HealthSim:    User → Natural Language → Claude + Skills → Structured Output
```

HealthSim replaces traditional programming with conversational AI. Users describe what they need; Claude generates realistic synthetic healthcare data using domain knowledge encoded in Skills.

**Why This Matters**
- No coding required for data generation
- Natural language is more accessible than APIs
- Domain expertise lives in Skills, not code
- Iteration is conversational, not compile-debug cycles

### 1.2 Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Skills as Knowledge, Not Code** | Skills contain domain knowledge and generation patterns; Claude generates data dynamically |
| **Progressive Disclosure** | Master skill routes to detailed skills; load only what's needed |
| **Format-Agnostic Generation** | Generate canonical data first, then transform to any output format |
| **Common + Domain Organization** | Shared components in core; domain-specific in product folders |
| **MCP for I/O Only** | MCP servers handle file/database operations; generation is conversational |
| **Minimal Python** | Simple scripts only (validation, format helpers); no Python libraries |

### 1.3 What HealthSim Is NOT

- **Not a Python library** - No `pip install healthsim`
- **Not an API** - No REST endpoints or SDK
- **Not a database** - Generates data on demand, doesn't store it
- **Not clinical decision support** - Synthetic test data only

---

## 2. Product Family

### 2.1 Current Products

| Product | Domain | Primary Standards | Key Entities |
|---------|--------|-------------------|--------------|
| **PatientSim** | Clinical/EMR | FHIR R4, HL7v2, C-CDA | Patient, Encounter, Diagnosis, Procedure, Lab, Medication |
| **MemberSim** | Payer/Claims | X12 837/835, 834, 270/271 | Member, Claim, Payment, Accumulator, Prior Auth |
| **RxMemberSim** | Pharmacy/PBM | NCPDP D.0 | Prescription, PharmacyClaim, Formulary, DUR Alert |

### 2.2 Planned Products

| Product | Domain | Primary Data Sources | Key Entities |
|---------|--------|---------------------|--------------|
| **PopulationSim** | Demographics/SDOH | Census, ACS, SDOH indices | Population, Cohort, Geography, Demographics |
| **NetworkSim** | Provider/Payer Networks | NPPES, CMS, State data | Provider, Network, Facility, Contract, Geography |

### 2.3 Product Relationships

```
                    ┌─────────────────┐
                    │  PopulationSim  │
                    │  (Demographics) │
                    └────────┬────────┘
                             │ provides population patterns
                             ▼
┌─────────────┐    ┌─────────────────┐
│ NetworkSim  │◄───│   PatientSim    │
│ (Providers) │    │   (Clinical)    │
└──────┬──────┘    └────────┬────────┘
       │                    │
       │    ┌───────────────┼───────────────┐
       │    │               │               │
       ▼    ▼               ▼               ▼
┌─────────────────┐  ┌─────────────┐  ┌─────────────┐
│   MemberSim     │  │ RxMemberSim │  │   (Future)  │
│   (Claims)      │  │ (Pharmacy)  │  │             │
└─────────────────┘  └─────────────┘  └─────────────┘
```

**Key Integration Points:**
- PatientSim patients can become MemberSim members (add coverage)
- PatientSim medications can generate RxMemberSim pharmacy claims
- PopulationSim demographics inform all patient generation
- NetworkSim providers referenced across all claims

---

## 3. Architecture Layers

### 3.1 Layer Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER CONVERSATION                             │
│  "Generate 50 diabetic patients typical of Pittsburgh, PA"          │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          SKILLS LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  SCENARIO    │  │  REFERENCE   │  │     FORMAT               │  │
│  │  SKILLS      │  │  SKILLS      │  │     SKILLS               │  │
│  │              │  │              │  │                          │  │
│  │ • Diabetes   │  │ • ICD-10     │  │ • FHIR R4                │  │
│  │ • Heart Fail │  │ • CPT        │  │ • HL7v2                  │  │
│  │ • Claims     │  │ • LOINC      │  │ • X12                    │  │
│  │ • Pharmacy   │  │ • NDC        │  │ • NCPDP                  │  │
│  │ • Trials     │  │ • CDISC      │  │ • CSV/SQL                │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     CANONICAL DATA MODELS                            │
│  JSON Schemas defining structure for all entities                   │
│  • Person (shared)  • Patient  • Member  • Subject                  │
│  • Encounter  • Claim  • Prescription  • Visit                      │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      MCP SERVERS (I/O Only)                          │
│  • File System: Save CSV, JSON, Parquet                             │
│  • Database: DuckDB, Databricks, PostgreSQL                         │
│  • GitHub: Version control, sharing                                 │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 Layer Responsibilities

| Layer | Responsibility | Implementation |
|-------|----------------|----------------|
| **Conversation** | User intent capture, clarification | Claude natural language |
| **Skills** | Domain knowledge, generation patterns | Markdown files with YAML |
| **Canonical Models** | Entity structure, validation | JSON Schema |
| **MCP/Output** | File I/O, database loading | MCP servers, simple scripts |

---

## 4. Directory Organization

### 4.1 Repository Structure

```
healthsim-common/
├── SKILL.md                           # Master entry point (triggers routing)
├── README.md                          # Repository overview
├── CHANGELOG.md                       # Version history
├── pyproject.toml                     # Python package configuration
│
├── src/                               # Python source code
│   └── healthsim/                     # Core library package
│       ├── __init__.py                # Package exports
│       ├── benefits/                  # Accumulator infrastructure
│       ├── dimensional/               # Star schema transformers
│       ├── state/                     # Workspace & provenance tracking
│       ├── validation/                # Validation framework
│       └── ...                        # Additional modules
│
├── tests/                             # Python unit tests
│
├── docs/                              # Documentation
│   ├── README.md                      # Documentation index
│   ├── HEALTHSIM-ARCHITECTURE-GUIDE.md    # This document
│   ├── architecture/                  # Architecture deep-dives
│   ├── extensions/                    # Extension guides
│   ├── mcp/                          # MCP server documentation
│   ├── skills/                       # Skills authoring guides
│   └── state-management/             # State handling patterns
│
├── references/                        # Shared reference data
│   ├── code-systems.md               # ICD-10, CPT, LOINC, NDC, RxNorm
│   ├── terminology.md                # Healthcare terminology
│   ├── clinical-rules.md             # Clinical business rules
│   ├── validation-rules.md           # All validation rules
│   ├── hl7v2-segments.md             # HL7v2 segment definitions
│   ├── data-models.md                # Entity schemas
│   ├── clinical-domain.md            # Clinical domain knowledge
│   ├── generation-patterns.md        # Data generation patterns
│   ├── mental-health-reference.md    # Mental health codes/rules
│   ├── oncology-domain.md            # Oncology domain knowledge
│   ├── pediatric-dosing.md           # Pediatric medication dosing
│   └── oncology/                     # Oncology reference data
│       └── README.md
│
├── formats/                           # Output format transformations
│   ├── fhir-r4.md                    # FHIR R4 bundles/resources
│   ├── ccda-format.md                # C-CDA clinical documents
│   ├── hl7v2-adt.md                  # HL7v2 ADT messages
│   ├── hl7v2-orm.md                  # HL7v2 order messages
│   ├── hl7v2-oru.md                  # HL7v2 result messages
│   ├── x12-834.md                    # X12 enrollment
│   ├── x12-837.md                    # X12 claims
│   ├── x12-835.md                    # X12 remittance
│   ├── x12-270-271.md                # X12 eligibility
│   ├── ncpdp-d0.md                   # NCPDP pharmacy
│   ├── csv.md                        # CSV export
│   ├── sql.md                        # SQL INSERT statements
│   └── dimensional-analytics.md      # Star schema for analytics
│
├── skills/                            # Domain-specific scenario skills
│   ├── common/                        # Shared skills
│   │   └── state-management.md
│   │
│   ├── patientsim/
│   │   ├── SKILL.md                  # PatientSim overview
│   │   ├── diabetes-management.md
│   │   ├── heart-failure.md
│   │   ├── chronic-kidney-disease.md
│   │   ├── sepsis-acute-care.md
│   │   ├── ed-chest-pain.md
│   │   ├── elective-joint.md
│   │   ├── maternal-health.md
│   │   ├── behavioral-health.md
│   │   ├── adt-workflow.md
│   │   ├── orders-results.md
│   │   ├── oncology/                 # Oncology scenarios
│   │   │   ├── README.md
│   │   │   ├── breast-cancer.md
│   │   │   ├── lung-cancer.md
│   │   │   └── colorectal-cancer.md
│   │   └── pediatrics/               # Pediatric scenarios
│   │       ├── README.md
│   │       ├── acute-otitis-media.md
│   │       └── childhood-asthma.md
│   │
│   ├── membersim/
│   │   ├── SKILL.md                  # MemberSim overview
│   │   ├── plan-benefits.md
│   │   ├── enrollment-eligibility.md
│   │   ├── professional-claims.md
│   │   ├── facility-claims.md
│   │   ├── prior-authorization.md
│   │   ├── accumulator-tracking.md
│   │   ├── value-based-care.md
│   │   └── behavioral-health.md
│   │
│   ├── rxmembersim/
│   │   ├── SKILL.md                  # RxMemberSim overview
│   │   ├── retail-pharmacy.md
│   │   ├── specialty-pharmacy.md
│   │   ├── dur-alerts.md
│   │   ├── formulary-management.md
│   │   ├── rx-prior-auth.md
│   │   ├── rx-accumulator.md
│   │   ├── rx-enrollment.md
│   │   └── manufacturer-programs.md
│   │
│   ├── trialsim/                      # (Planned) Clinical trials
│   │   ├── SKILL.md
│   │   ├── study-design.md
│   │   ├── subject-enrollment.md
│   │   └── cdisc-output.md
│   │
│   ├── populationsim/                 # (Planned) Population generation
│   │   ├── SKILL.md
│   │   ├── census-demographics.md
│   │   ├── sdoh-factors.md
│   │   └── geographic-patterns.md
│   │
│   └── networksim/                    # (Planned) Provider networks
│       ├── SKILL.md
│       ├── provider-networks.md
│       ├── payer-networks.md
│       └── geographic-coverage.md
│
├── hello-healthsim/                   # Tutorials and examples
│   ├── README.md                     # Tutorial index
│   ├── CLAUDE-DESKTOP.md             # Claude Desktop guide
│   ├── CLAUDE-CODE.md                # Claude Code guide
│   ├── EXTENDING.md                  # Extension tutorial
│   ├── TROUBLESHOOTING.md            # Common issues
│   └── examples/                     # Example outputs
│       ├── README.md
│       ├── patientsim-examples.md
│       ├── membersim-examples.md
│       ├── rxmembersim-examples.md
│       ├── oncology-examples.md
│       ├── format-examples.md
│       └── cross-domain-examples.md
│
└── scripts/                           # Helper scripts
    └── smoke_test.py                 # Integration smoke tests
```

### 4.2 VS Code Workspace Organization

The `healthsim.code-workspace` file organizes folders for development:

```json
{
  "folders": [
    { "name": "healthsim-common", "path": "./healthsim-common" },
    { "name": "patientsim", "path": "./healthsim-common/skills/patientsim" },
    { "name": "membersim", "path": "./healthsim-common/skills/membersim" },
    { "name": "rxmembersim", "path": "./healthsim-common/skills/rxmembersim" },
    { "name": "common", "path": "./healthsim-common/skills/common" }
    // Planned products (uncomment when implemented):
    // { "name": "trialsim", "path": "./healthsim-common/skills/trialsim" },
    // { "name": "populationsim", "path": "./healthsim-common/skills/populationsim" },
    // { "name": "networksim", "path": "./healthsim-common/skills/networksim" }
  ]
}
```

---

## 5. Skills Architecture

### 5.1 Skill Types

| Type | Purpose | Location | Example |
|------|---------|----------|---------|
| **Master Skill** | Entry point, routing | `SKILL.md` (root) | Routes to product skills |
| **Product Skill** | Product overview | `skills/{product}/SKILL.md` | PatientSim overview |
| **Scenario Skill** | Specific use case | `skills/{product}/*.md` | `diabetes-management.md` |
| **Reference Skill** | Code lookups, rules | `references/*.md` | `code-systems.md` |
| **Format Skill** | Output transformation | `formats/*.md` | `fhir-r4.md` |

### 5.2 Skill File Format

Every skill MUST have YAML frontmatter:

```yaml
---
name: healthsim-diabetes-management
description: >
  Generate realistic Type 2 Diabetes patient scenarios including diagnosis,
  medication escalation, lab patterns, and complications. Use when user requests:
  (1) diabetic patients, (2) A1C/glucose testing, (3) diabetes medications like
  metformin or insulin, (4) diabetic complications, or (5) HEDIS diabetes measures.
---
```

### 5.3 Standard Skill Template

```markdown
---
name: {skill-name}
description: >
  {What this skill does}. Use when user requests: (1) {trigger 1}, (2) {trigger 2},
  (3) {trigger 3}. Part of HealthSim {product} synthetic data generation.
---

# {Skill Title}

## Overview

{Brief description of what this skill generates and when to use it}

## Trigger Phrases

Activate this skill when user mentions:
- {phrase 1}
- {phrase 2}
- {phrase 3}

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| {param} | {type} | {default} | {description} |

## Generation Patterns

### {Pattern Category 1}

{Knowledge and rules for generating this aspect}

### {Pattern Category 2}

{Knowledge and rules for generating this aspect}

## Output Schema

```json
{
  "entity_type": {
    "field1": "type",
    "field2": "type"
  }
}
```

## Examples

### Example 1: {Scenario Name}

**Request:** "{example request}"

**Output:**
```json
{example output}
```

## Validation Rules

- {Rule 1}
- {Rule 2}

## Related Skills

- [{Related Skill 1}](path/to/skill.md) - {when to use}
```

---

## 6. Canonical Data Models

### 6.1 Model Philosophy

- **Single source of truth**: Define each entity once
- **Extend, don't duplicate**: Domain entities extend common base
- **JSON Schema**: All models defined as JSON Schema
- **Validation-ready**: Schema supports automated validation

### 6.2 Common Base Entities

**Person** (shared across all products)
```json
{
  "person_id": "string (UUID)",
  "name": {
    "given_name": "string",
    "family_name": "string",
    "middle_name": "string (optional)",
    "prefix": "string (optional)",
    "suffix": "string (optional)"
  },
  "birth_date": "date (YYYY-MM-DD)",
  "gender": "string (M|F|O|U)",
  "address": {
    "street_address": "string",
    "city": "string",
    "state": "string (2-letter)",
    "postal_code": "string",
    "country": "string (default: US)"
  },
  "phone": "string (optional)",
  "email": "string (optional)"
}
```

### 6.3 Domain Entity Extensions

| Product | Base Entity | Extended Entity | Added Fields |
|---------|-------------|-----------------|--------------|
| PatientSim | Person | Patient | mrn, encounters, diagnoses, medications |
| MemberSim | Person | Member | member_id, plan, coverage, accumulators |
| RxMemberSim | Member | RxMember | rx_bin, rx_pcn, rx_group, formulary |
| PopulationSim | Person | PopulationMember | census_tract, sdoh_indices, demographics |
| NetworkSim | - | Provider | npi, specialty, networks, facilities |

### 6.4 Entity Relationships

```
Person (base)
  ├── Patient (PatientSim)
  │     ├── extends to → Member (MemberSim)
  │     │                  └── extends to → RxMember (RxMemberSim)
  │
  └── PopulationMember (PopulationSim)

Provider (NetworkSim)
  ├── referenced by → Encounter (PatientSim)
  └── referenced by → Claim (MemberSim)
```

---

## 7. Output Formats

### 7.1 Default Output

By default, Claude outputs data as **JSON** matching the canonical data model.

### 7.2 Healthcare Standard Formats

| Format | Skill | Trigger Phrases | Use Case |
|--------|-------|-----------------|----------|
| FHIR R4 | `formats/fhir-r4.md` | "as FHIR", "FHIR bundle" | Modern interoperability |
| C-CDA | `formats/ccda-format.md` | "as C-CDA", "CCD" | Clinical documents |
| HL7v2 ADT | `formats/hl7v2-adt.md` | "as HL7", "ADT message" | Legacy EMR |
| HL7v2 ORM | `formats/hl7v2-orm.md` | "order message" | Orders |
| HL7v2 ORU | `formats/hl7v2-oru.md` | "result message" | Results |
| X12 834 | `formats/x12-834.md` | "as 834", "enrollment" | Benefit enrollment |
| X12 837 | `formats/x12-837.md` | "as 837", "claim file" | Claims submission |
| X12 835 | `formats/x12-835.md` | "as 835", "remittance" | Payment posting |
| X12 270/271 | `formats/x12-270-271.md` | "eligibility check" | Eligibility |
| NCPDP D.0 | `formats/ncpdp-d0.md` | "as NCPDP" | Pharmacy |

### 7.3 Export Formats

| Format | Skill | Use Case |
|--------|-------|----------|
| CSV | `formats/csv.md` | Spreadsheets, bulk data |
| SQL INSERT | `formats/sql.md` | Database loading |
| Dimensional | `formats/dimensional-analytics.md` | Star schema, analytics |

---

## 8. MCP Integration

### 8.1 Philosophy

**MCP is for I/O only.** Data generation happens in conversation; MCP handles:
- File system operations (save, read)
- Database operations (load, query)
- External services (GitHub)

### 8.2 MCP Servers Used

| Server | Purpose | When Used |
|--------|---------|-----------|
| **File System** | Save generated data | Always for file output |
| **DuckDB** | Local analytics | SQL queries, dimensional models |
| **Databricks** | Cloud analytics | Production data loading |
| **PostgreSQL** | Relational storage | Application databases |
| **GitHub** | Version control | Publishing datasets |

### 8.3 Database Loading Pattern

```
1. Generate data in conversation (JSON)
2. Transform to SQL INSERT statements (using formats/sql.md)
3. Execute via MCP database server
4. Verify with SELECT count(*)
```

### 8.4 What Does NOT Need MCP

These operations are pure conversation (no MCP):
- Generating synthetic data
- Formatting data (JSON, CSV inline)
- Explaining schemas and rules
- Validating data structures
- Answering healthcare questions

---

## 9. Cross-Product Patterns

### 9.1 Entity Linking

When generating data across products, maintain referential integrity:

```json
{
  "patient": {
    "mrn": "MRN001",
    "person_id": "P-12345"
  },
  "member": {
    "member_id": "MEM001",
    "person_id": "P-12345"  // Same person
  },
  "subject": {
    "subject_id": "SUBJ-001",
    "patient_ref": "MRN001"  // Links to patient
  }
}
```

### 9.2 Timeline Consistency

Ensure temporal coherence across products:

```
Patient Timeline:
  Birth (1960) → Diagnosis (2020) → Encounter (2024) → Claim (2024)

Trial Timeline:
  Screening → Consent → Randomization → Visits → End of Treatment → Follow-up

Claims Timeline:
  Service Date → Claim Submission → Adjudication → Payment
```

### 9.3 Code System Consistency

Use consistent code systems across products:

| Data Type | Code System | Example |
|-----------|-------------|---------|
| Diagnoses | ICD-10-CM | E11.9 |
| Procedures | CPT/HCPCS | 99213 |
| Labs | LOINC | 4548-4 |
| Medications | NDC/RxNorm | 00071015523 |
| Providers | NPI | 1234567890 |
| Facilities | NPI | 9876543210 |

---

## 10. Extension Patterns

### 10.1 Adding a New Scenario

1. Create skill file in `skills/{product}/`
2. Follow standard skill template
3. Include YAML frontmatter with triggers
4. Add examples with expected output
5. Link from product SKILL.md
6. Add to hello-healthsim examples

### 10.2 Adding a New Format

1. Create format file in `formats/`
2. Define mapping from canonical model
3. Include transformation rules
4. Add complete examples
5. Update master SKILL.md format table

### 10.3 Adding a New Product

1. Create `skills/{newproduct}/` directory
2. Create product SKILL.md overview
3. Define canonical entities (extend common where possible)
4. Create initial scenario skills
5. Add to master SKILL.md product table
6. Update VS Code workspace
7. Add hello-healthsim examples

### 10.4 Extension Checklist

When adding any new component:

- [ ] YAML frontmatter with name and description
- [ ] Clear trigger phrases
- [ ] At least 2 complete examples
- [ ] JSON schema for entities
- [ ] Validation rules
- [ ] Links to related skills
- [ ] Updated documentation index
- [ ] hello-healthsim example added

---

## Document Metadata

**Document**: HealthSim Architecture Guide  
**Version**: 2.0  
**Maintainer**: HealthSim Team  
**Last Review**: 2025-12-17

**Related Documents**:
- [Development Process](HEALTHSIM-DEVELOPMENT-PROCESS.md)
- [Contributing Guide](contributing.md)
- [Hello HealthSim Tutorial](../hello-healthsim/README.md)

---

*End of Document*
