# HealthSim Claude Project Instructions

*Condensed guardrails for consistent development. Full details in docs/HEALTHSIM-ARCHITECTURE-GUIDE.md and docs/HEALTHSIM-DEVELOPMENT-PROCESS.md*

---

## Core Philosophy

**Conversation-First**: HealthSim generates synthetic healthcare data via natural language + Skills. No Python libraries or APIs - Skills contain domain knowledge, Claude generates data dynamically.

**Design → Super-Prompt → Implement**: Design thoroughly in Claude Desktop, create comprehensive super-prompts, execute systematically in Claude Code.

---

## Repository Structure

**Single Repository**: `healthsim-workspace` (https://github.com/mark64oswald/healthsim-workspace)

```
healthsim-workspace/
├── SKILL.md                    # Master routing skill
├── docs/                       # Architecture, process docs
├── references/                 # Code systems, validation rules (shared)
├── formats/                    # Output formats: FHIR, X12, CDISC, etc. (shared)
├── skills/                     # Domain-specific scenario skills
│   ├── common/                 # Shared skills
│   ├── patientsim/             # Clinical/EMR scenarios
│   ├── membersim/              # Payer/claims scenarios
│   ├── rxmembersim/            # Pharmacy/PBM scenarios
│   ├── trialsim/               # Clinical trials scenarios
│   ├── populationsim/          # Demographics/SDOH
│   └── networksim/             # Provider networks (planned)
├── hello-healthsim/            # Tutorials and examples
├── packages/                   # Python packages (infrastructure)
│   ├── core/                   # Shared library
│   ├── patientsim/             # PatientSim MCP/utilities
│   ├── membersim/              # MemberSim MCP/utilities
│   └── rxmembersim/            # RxMemberSim MCP/utilities
├── demos/                      # Interactive demos
└── scripts/                    # Utility scripts
```

---

## Architecture Rules

### Skills Organization

| Location | Content |
|----------|---------|
| `skills/{product}/` | Scenario and domain skills (flat structure) |
| `skills/{product}/{subcategory}/` | Allowed for logical groupings (oncology/, pediatrics/) |
| `formats/` | ALL output formats (shared, not product-specific) |
| `references/` | ALL reference data (shared, not product-specific) |

### DO NOT Create These Subdirectories

- `skills/{product}/scenarios/` - Put scenarios directly in product folder
- `skills/{product}/domain/` - Put domain files directly in product folder
- `skills/{product}/formats/` - Use root `formats/` instead
- `skills/{product}/models/` - Schemas defined inline in skills

### Skills Must Have

- YAML frontmatter with `name` and `description` (include trigger phrases)
- Sections: Overview, Trigger Phrases, Parameters table, Generation Patterns, Examples (≥2), Validation Rules, Related Skills

### Data Models

- Generate canonical JSON first, then transform to output format
- Extend common entities (Person → Patient → Member → Subject)
- Use standard code systems: ICD-10, CPT, LOINC, NDC, NPI, CDISC

### MCP = I/O Only

File system, database, GitHub operations. Generation happens in conversation.

---

## Products

| Product | Domain | Standards | Skills Location | Package Location |
|---------|--------|-----------|-----------------|------------------|
| PatientSim | Clinical/EMR | FHIR, HL7v2, C-CDA | `skills/patientsim/` | `packages/patientsim/` |
| MemberSim | Payer/Claims | X12 837/835/834 | `skills/membersim/` | `packages/membersim/` |
| RxMemberSim | Pharmacy/PBM | NCPDP D.0 | `skills/rxmembersim/` | `packages/rxmembersim/` |
| TrialSim | Clinical Trials | CDISC SDTM/ADaM | `skills/trialsim/` | - |
| PopulationSim | Demographics/SDOH | Census, ACS | `skills/populationsim/` | - |
| NetworkSim | Provider Networks | NPPES, NPI | `skills/networksim/` | - |

---

## Development Workflow

### Every Super-Prompt Must Include

1. Context + reference documents to read
2. Pre-flight checklist
3. Specific deliverables (files to create/modify)
4. Step-by-step implementation with verification
5. Post-flight checklist
6. Success criteria

### After Every Implementation Session

- [ ] Test with sample generation request
- [ ] Update CHANGELOG.md
- [ ] Verify documentation links
- [ ] Git add → commit (descriptive message) → push

### Commit Message Format

```
[Product] Brief description

Examples:
[TrialSim] Add Phase 3 pivotal trial skill
[MemberSim] Fix accumulator calculation example
[Docs] Clarify directory structure
```

---

## Quality Gates

### New Skill Checklist

- [ ] YAML frontmatter with `name` and `description` (triggers included)
- [ ] At least 2 complete examples with JSON output
- [ ] Linked from product SKILL.md routing table
- [ ] Cross-product check: Related skills identified, bidirectional links added
- [ ] hello-healthsim example added
- [ ] CHANGELOG.md updated

### New Product Checklist

- [ ] Directory: `skills/{product}/`
- [ ] Product SKILL.md created
- [ ] Master SKILL.md updated with routing
- [ ] Cross-product review: All existing products checked for integration
- [ ] VS Code workspace updated
- [ ] Architecture guide updated (including cross-product mapping)
- [ ] hello-healthsim quickstart added

---

## Link Patterns

From within `skills/{product}/`:

| Target | Pattern |
|--------|---------|
| Same folder | `[file.md](file.md)` |
| Subcategory | `[category/file.md](category/file.md)` |
| Root formats | `[../../formats/fhir-r4.md](../../formats/fhir-r4.md)` |
| Root references | `[../../references/code-systems.md](../../references/code-systems.md)` |
| Hello examples | `[../../hello-healthsim/examples/quickstart.md](../../hello-healthsim/examples/quickstart.md)` |

---

## Key Reminders

- **Single repo**: Clone `healthsim-workspace` to get everything
- **Follow existing patterns**: Review similar files before creating new ones
- **Cross-product integration**: Check for related skills in other products, add bidirectional references
- **Skills are flat**: Scenarios go directly in product folder, not nested
- **Formats are shared**: All formats in root `formats/`, never in product folders
- **Packages for Python**: Python infrastructure in `packages/`, not in `skills/`
- **Progressive disclosure**: Master skill routes to detailed skills
- **Extend, don't duplicate**: Reference canonical models
- **Test frequently**: Verify after each change
- **Document as you go**: CHANGELOG.md every session

---

*GitHub: https://github.com/mark64oswald/healthsim-workspace*
