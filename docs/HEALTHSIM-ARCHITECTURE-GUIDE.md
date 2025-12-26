---
name: healthsim-architecture-guide
description: "Authoritative reference for HealthSim architecture, patterns, and conventions. Read this first when developing new skills or products."
---

# HealthSim Architecture Guide

**Version**: 3.0  
**Last Updated**: 2025-12-18  
**Purpose**: Authoritative reference for HealthSim architecture, patterns, and conventions.

---

## Table of Contents

1. [Philosophy](#1-philosophy)
2. [Product Family](#2-product-family)
3. [Directory Organization](#3-directory-organization)
4. [Skills Architecture](#4-skills-architecture)
5. [Canonical Data Models](#5-canonical-data-models)
6. [Output Formats](#6-output-formats)
7. [MCP Integration](#7-mcp-integration)
   - [Data Architecture](#75-data-architecture)
8. [Extension Patterns](#8-extension-patterns)

---

## 1. Philosophy

### 1.1 Core Principles

**Conversation-First / Configuration via Conversation**

HealthSim replaces traditional programming with conversational AI. Users describe what they need; Claude generates realistic synthetic healthcare data using domain knowledge encoded in Skills.

**Why This Matters**
- No coding required for data generation
- Natural language is more accessible than APIs
- Domain expertise lives in Skills, not code
- Iteration is conversational, not compile-debug cycles

### 1.2 Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Single Unified Repository** | Users clone once, get everything |
| **Skills as Knowledge, Not Code** | Skills contain domain knowledge; Claude generates data |
| **Progressive Disclosure** | Master skill routes to detailed skills |
| **Format-Agnostic Generation** | Generate canonical JSON first, then transform |
| **Skills + Packages Organization** | Skills for domain knowledge; Packages for Python infrastructure |
| **MCP for I/O Only** | MCP servers handle file/database ops; generation is conversational |

---

## 2. Product Family

### 2.1 Current Products

| Product | Domain | Primary Standards | Status |
|---------|--------|-------------------|--------|
| **PatientSim** | Clinical/EMR | FHIR R4, HL7v2, C-CDA | Active |
| **MemberSim** | Payer/Claims | X12 837/835, 834, 270/271 | Active |
| **RxMemberSim** | Pharmacy/PBM | NCPDP D.0 | Active |
| **TrialSim** | Clinical Trials | CDISC SDTM/ADaM | Active |
| **PopulationSim** | Demographics/SDOH | Census, ACS, SDOH indices | Active |
| **NetworkSim** | Provider Networks | NPPES, NPI, taxonomy | Planned |

### 2.2 Product Relationships

```
                    ┌─────────────────┐
                    │  PopulationSim  │
                    │  (Demographics) │
                    └────────┬────────┘
                             │ provides population patterns
                             ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│ NetworkSim  │◄───│   PatientSim    │───►│  TrialSim   │
│ (Providers) │    │   (Clinical)    │    │  (Trials)   │
└──────┬──────┘    └────────┬────────┘    └─────────────┘
       │                    │
       │    ┌───────────────┼───────────────┐
       │    │               │               │
       ▼    ▼               ▼               ▼
┌─────────────────┐  ┌─────────────┐
│   MemberSim     │  │ RxMemberSim │
│   (Claims)      │  │ (Pharmacy)  │
└─────────────────┘  └─────────────┘
```

---

## 3. Directory Organization

### 3.1 Repository Structure

HealthSim uses a **single unified repository** (`healthsim-workspace`) with clear separation.

```
healthsim-workspace/
├── SKILL.md                           # Master entry point (routing)
├── README.md                          # Repository overview
├── CHANGELOG.md                       # Version history
├── pyproject.toml                     # Workspace-level Python config
├── healthsim.code-workspace           # VS Code workspace file
│
├── docs/                              # Documentation
│   ├── README.md
│   ├── HEALTHSIM-ARCHITECTURE-GUIDE.md    # This document
│   ├── HEALTHSIM-DEVELOPMENT-PROCESS.md
│   ├── HEALTHSIM-PROJECT-INSTRUCTIONS.md
│   └── contributing.md
│
├── references/                        # Shared reference data
│   ├── code-systems.md               # ICD-10, CPT, LOINC, NDC
│   ├── terminology.md
│   ├── clinical-rules.md
│   └── validation-rules.md
│
├── formats/                           # Output format transformations (SHARED)
│   ├── fhir-r4.md
│   ├── hl7v2-adt.md
│   ├── x12-837.md
│   ├── ncpdp-d0.md
│   ├── cdisc-sdtm.md                 # For TrialSim
│   ├── cdisc-adam.md                 # For TrialSim
│   └── dimensional-analytics.md
│
├── skills/                            # Domain-specific scenario skills
│   ├── common/
│   │   └── state-management.md
│   │
│   ├── patientsim/                    # Clinical scenarios
│   │   ├── SKILL.md
│   │   ├── diabetes-management.md
│   │   ├── oncology/                 # Subcategory (allowed)
│   │   └── pediatrics/               # Subcategory (allowed)
│   │
│   ├── membersim/                     # Payer/claims scenarios
│   │   ├── SKILL.md
│   │   └── professional-claims.md
│   │
│   ├── rxmembersim/                   # Pharmacy scenarios
│   │   ├── SKILL.md
│   │   └── retail-pharmacy.md
│   │
│   ├── trialsim/                      # Clinical trials (Active)
│   │   ├── SKILL.md
│   │   ├── clinical-trials-domain.md
│   │   ├── phase3-pivotal.md
│   │   └── therapeutic-areas/        # Subcategory (allowed)
│   │
│   ├── populationsim/                 # Demographics/SDOH (Active)
│   │   ├── SKILL.md
│   │   └── README.md
│   │
│   └── networksim/                    # Provider networks (Planned)
│       ├── SKILL.md
│       └── README.md
│
├── hello-healthsim/                   # Tutorials and examples
│   ├── README.md
│   ├── CLAUDE-DESKTOP.md
│   ├── CLAUDE-CODE.md
│   └── examples/
│
├── packages/                          # Python packages (infrastructure)
│   ├── README.md
│   ├── core/                          # Shared Python library
│   │   ├── pyproject.toml
│   │   ├── src/healthsim/
│   │   └── tests/
│   ├── patientsim/                    # PatientSim MCP/utilities
│   ├── membersim/                     # MemberSim MCP/utilities
│   └── rxmembersim/                   # RxMemberSim MCP/utilities
│
├── demos/                             # Interactive demos
│
└── scripts/                           # Utility scripts
    └── smoke_test.py
```

### 3.2 Key Organization Principles

| Principle | Implementation |
|-----------|----------------|
| **Skills are flat** | Scenario files directly in `skills/{product}/` |
| **Formats are shared** | ALL output formats in root `formats/` |
| **References are shared** | ALL reference data in root `references/` |
| **Subcategories allowed** | Use sparingly (oncology/, pediatrics/, therapeutic-areas/) |
| **Python is separate** | Python packages in `packages/`, not mixed with skills |

### 3.3 What NOT to Create

These subdirectories should **NOT** exist:
- `skills/{product}/scenarios/` - Put scenarios directly in product folder
- `skills/{product}/domain/` - Put domain files directly in product folder
- `skills/{product}/formats/` - Formats go in root `formats/`
- `skills/{product}/models/` - Schemas defined inline in skills

---

## 4. Skills Architecture

### 4.1 Skill Types

| Type | Purpose | Location |
|------|---------|----------|
| **Master Skill** | Entry point, routing | `SKILL.md` (root) |
| **Product Skill** | Product overview | `skills/{product}/SKILL.md` |
| **Scenario Skill** | Specific use case | `skills/{product}/*.md` |
| **Format Skill** | Output transformation | `formats/*.md` |
| **Reference Skill** | Code lookups, rules | `references/*.md` |

### 4.2 Required YAML Frontmatter

Every skill MUST have:

```yaml
---
name: {skill-name}
description: "{What this skill does}. Use when user requests: {trigger 1}, {trigger 2}."
---
```

### 4.3 Standard Skill Sections

1. **Overview** - What this skill does
2. **Trigger Phrases** - When to activate
3. **Parameters** - Configurable options
4. **Generation Patterns** - Domain knowledge
5. **Examples** - At least 2 complete examples
6. **Validation Rules** - How to verify output
7. **Related Skills** - Links to related content

---

## 5. Canonical Data Models

### 5.1 Entity Extension Pattern

| Product | Base | Extended Entity |
|---------|------|-----------------|
| PatientSim | Person | Patient |
| MemberSim | Person | Member |
| RxMemberSim | Member | RxMember |
| TrialSim | Patient | Subject |
| PopulationSim | Person | PopulationMember |
| NetworkSim | - | Provider |

### 5.2 Standard Code Systems

| Data Type | Code System |
|-----------|-------------|
| Diagnoses | ICD-10-CM |
| Procedures | CPT/HCPCS |
| Labs | LOINC |
| Medications | NDC/RxNorm |
| Providers | NPI |
| Trial Domains | CDISC |

---

## 6. Output Formats

### 6.1 Healthcare Standards

| Format | Skill | Use Case |
|--------|-------|----------|
| FHIR R4 | `formats/fhir-r4.md` | Modern interoperability |
| C-CDA | `formats/ccda-format.md` | Clinical documents |
| HL7v2 | `formats/hl7v2-*.md` | Legacy EMR |
| X12 | `formats/x12-*.md` | Claims, enrollment |
| NCPDP | `formats/ncpdp-d0.md` | Pharmacy |
| CDISC SDTM | `formats/cdisc-sdtm.md` | Trial regulatory |
| CDISC ADaM | `formats/cdisc-adam.md` | Trial analysis |

### 6.2 Export Formats

| Format | Skill | Use Case |
|--------|-------|----------|
| CSV | `formats/csv.md` | Spreadsheets |
| SQL | `formats/sql.md` | Database loading |
| Dimensional | `formats/dimensional-analytics.md` | Star schema |

---

## 7. MCP Integration

### 7.1 Philosophy

**MCP is for I/O only.** Data generation happens in conversation; MCP handles:
- File system operations
- Database operations
- External services

### 7.2 What Does NOT Need MCP

- Generating synthetic data
- Formatting data
- Explaining schemas
- Validating structures

---

## 7.5 Data Architecture

### 7.5.1 Storage Backend

HealthSim uses **DuckDB** as its unified data store:

| Layer | Purpose | Tables |
|-------|---------|--------|
| **Canonical** | Source of truth for entities | patients, encounters, claims, etc. |
| **State Management** | Scenario organization | scenarios, scenario_entities, scenario_tags |
| **Reference** | PopulationSim datasets | ref_cdc_places_*, ref_svi_*, ref_adi_* |

**Location**: `~/.healthsim/healthsim.duckdb`

### 7.5.2 State Management

Scenarios are named snapshots containing:
- All generated entities (patients, encounters, claims, etc.)
- Full provenance (source_type, source_system, skill_used)
- User metadata (name, description, tags)

**API**:
```python
from healthsim.state import save_scenario, load_scenario, list_scenarios

scenario_id = save_scenario(name='my-cohort', entities={...})
scenario = load_scenario('my-cohort')
```

### 7.5.3 Sharing Scenarios

Export to JSON for portability:
```python
from healthsim.state import export_scenario_to_json, import_scenario_from_json

export_scenario_to_json('my-cohort')  # → ~/Downloads/my-cohort.json
import_scenario_from_json(Path('shared.json'))
```

See [Data Architecture](data-architecture.md) for complete documentation.

---

## 8. Extension Patterns

### 8.1 Adding a New Skill

1. Create file in `skills/{product}/`
2. Add YAML frontmatter with triggers
3. Include at least 2 examples
4. Link from product SKILL.md
5. Add hello-healthsim example

### 8.2 Adding a New Product

1. Create `skills/{newproduct}/` directory
2. Create product SKILL.md
3. Update master SKILL.md routing
4. Update VS Code workspace
5. Add hello-healthsim quickstart

### 8.3 Cross-Product Integration

When generating data that spans multiple products (e.g., a patient journey from clinical encounter to claims to pharmacy), follow these patterns:

**Identity Correlation:**
See `references/data-models.md` → "Cross-Product Identity Correlation" section for:
- Entity inheritance model (Person → Patient/Member/RxMember)
- Identity linking keys (SSN as universal correlator)
- Cross-product identity JSON pattern
- Event correlation timing across products

**Shared Domain Knowledge:**
- Place foundational concepts in `references/` (e.g., `oncology-domain.md`)
- Reference data (codes, medications) goes in `references/{domain}/`

**Cross-Referencing:**
- All scenario skills include "Related Skills" sections with cross-product links
- Each link includes an integration pattern note explaining when to use each product's skill

**Current Cross-Product Mappings:**

| Domain | PatientSim | MemberSim | RxMemberSim | TrialSim | Shared Reference |
|--------|------------|-----------|-------------|----------|------------------|
| Oncology | `oncology/*.md` | `facility-claims.md` | `specialty-pharmacy.md` | `therapeutic-areas/oncology.md` | `references/oncology-domain.md` |
| Cardiovascular | `heart-failure.md`, `ed-chest-pain.md` | `facility-claims.md` | `retail-pharmacy.md` | `therapeutic-areas/cardiovascular.md` | - |
| CNS/Behavioral | `behavioral-health.md` | `behavioral-health.md` | `retail-pharmacy.md` | `therapeutic-areas/cns.md` | `references/mental-health-reference.md` |
| Diabetes | `diabetes-management.md` | `professional-claims.md` | `retail-pharmacy.md`, `specialty-pharmacy.md` | - | - |
| CKD | `chronic-kidney-disease.md` | `facility-claims.md` | `specialty-pharmacy.md` | - | - |
| Maternal | `maternal-health.md` | `facility-claims.md` | `retail-pharmacy.md` | - | - |
| Surgical | `elective-joint.md` | `facility-claims.md`, `prior-authorization.md` | `retail-pharmacy.md` | - | - |

**Integration Pattern Examples:**

| Scenario | PatientSim | → MemberSim | → RxMemberSim |
|----------|------------|-------------|---------------|
| HF Admission | Inpatient encounter, meds, labs | Facility claim (DRG 291-293) | Discharge Rx fills (0-3 days) |
| Diabetes Visit | Office encounter, A1C | Professional claim (99214) | Rx fills same day |
| Oncology | Treatment regimen | Infusion claims (J-codes) | Oral oncolytic fills |
| Joint Replacement | Surgical episode | Prior auth → Facility claim (DRG 469-470) | Post-op pain meds |

**Best Practice:** When creating a new scenario skill, check if related skills exist in other products. Add bidirectional cross-references with integration pattern guidance.

### 8.4 Checklist

- [ ] YAML frontmatter with name and description
- [ ] Trigger phrases included
- [ ] At least 2 complete examples
- [ ] Links use correct relative paths
- [ ] CHANGELOG.md updated

---

**Repository**: https://github.com/mark64oswald/healthsim-workspace

*End of Document*
