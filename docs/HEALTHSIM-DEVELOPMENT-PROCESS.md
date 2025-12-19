---
name: healthsim-development-process
description: "Standard workflow for developing HealthSim skills and products. Read before creating new skills."
---

# HealthSim Development Process

**Version**: 3.0  
**Last Updated**: 2025-12-18  
**Purpose**: Standard workflow for developing HealthSim skills and products

---

## 1. Development Philosophy

### Design → Super-Prompt → Implement

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     DESIGN      │────►│  SUPER-PROMPT   │────►│   IMPLEMENT     │
│ Claude Desktop  │     │  Claude Desktop │     │  Claude Code    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Key Principles

- **Follow existing patterns** - Review similar files before creating new ones
- **Progressive disclosure** - Master skill routes to detailed skills
- **Extend, don't duplicate** - Reference canonical models
- **Test frequently** - Verify after each change
- **Document as you go** - Update CHANGELOG.md every session

---

## 2. Environment Setup

### Clone the Repository

```bash
git clone https://github.com/mark64oswald/healthsim-workspace.git
cd healthsim-workspace
```

### VS Code Workspace

```bash
code healthsim.code-workspace
```

### Python Environment (Optional)

```bash
cd packages/core
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

---

## 3. Skills Development

### Creating a New Skill

1. Create file in `skills/{product}/` (flat structure)
2. Add YAML frontmatter with name, description, triggers
3. Include required sections
4. Add at least 2 examples
5. Link from product SKILL.md
6. Update CHANGELOG.md

### Required Skill Sections

1. **Overview** - What this skill does
2. **Trigger Phrases** - When to activate
3. **Parameters** - Configurable options
4. **Generation Patterns** - Domain knowledge
5. **Examples** - At least 2 complete examples
6. **Validation Rules** - How to verify output
7. **Related Skills** - Links to related content

### File Locations

| Skill Type | Location |
|------------|----------|
| Product overview | `skills/{product}/SKILL.md` |
| Scenarios | `skills/{product}/{scenario}.md` |
| Subcategories | `skills/{product}/{category}/{scenario}.md` |
| Formats | `formats/{format}.md` (SHARED - not in product folder) |
| References | `references/{topic}.md` (SHARED - not in product folder) |

### Link Patterns

From `skills/{product}/`:

| Target | Pattern |
|--------|---------|
| Same folder | `[file.md](file.md)` |
| Subcategory | `[category/file.md](category/file.md)` |
| Root formats | `[../../formats/fhir-r4.md](../../formats/fhir-r4.md)` |
| Root references | `[../../references/code-systems.md](../../references/code-systems.md)` |

---

## 4. Git Workflow

### Commit Message Format

```
[Product] Brief description

Examples:
[TrialSim] Add Phase 3 pivotal trial skill
[MemberSim] Fix accumulator calculation example
[Docs] Clarify directory structure
```

### Standard Workflow

```bash
git add .
git commit -m "[Product] Description"
git push
```

### After Every Implementation Session

- [ ] `git status` - Review changes
- [ ] Update CHANGELOG.md
- [ ] `git add` - Stage files
- [ ] `git commit` - With proper message format
- [ ] `git push` - Push to remote

---

## 5. Quality Gates

### New Skill Checklist

- [ ] YAML frontmatter with `name` and `description`
- [ ] `description` includes trigger phrases
- [ ] At least 2 complete examples with JSON output
- [ ] Linked from product `SKILL.md` routing table
- [ ] hello-healthsim example added
- [ ] CHANGELOG.md updated
- [ ] All links valid (test relative paths)

### New Product Checklist

- [ ] Directory created: `skills/{product}/`
- [ ] Product `SKILL.md` created with routing table
- [ ] At least one scenario skill created
- [ ] Master `SKILL.md` updated with routing
- [ ] VS Code workspace file updated
- [ ] Architecture guide updated
- [ ] hello-healthsim quickstart added

---

## 6. Super-Prompt Template

Every super-prompt should include:

```markdown
# [Feature Name] Implementation Super-Prompt

## Context
- Product: {PatientSim | MemberSim | RxMemberSim | TrialSim}
- Phase: {X of Y}

## Reference Documents
Read these files FIRST:
1. `/path/to/architecture-guide.md`
2. `/path/to/similar-skill.md`

## Pre-Flight Checklist
- [ ] I have read all reference documents
- [ ] I understand the directory structure rules
- [ ] I know which files to create/modify

## Deliverables

### Files to Create
| File | Path | Purpose |
|------|------|---------|
| {file1} | `skills/{product}/{file1}.md` | {purpose} |

### Files to Modify
| File | Path | Change |
|------|------|--------|
| SKILL.md | `skills/{product}/SKILL.md` | Add routing |

## Implementation Steps

### Step 1: {First Task}
1. {action}
2. **Verify**: {check}

## Post-Flight Checklist
- [ ] All files have YAML frontmatter
- [ ] All links valid
- [ ] CHANGELOG.md updated

## Success Criteria
1. {criterion}
2. {criterion}
```

---

## Quick Reference

### Folder Structure

```
healthsim-workspace/
├── skills/           # Domain knowledge (Skills)
│   ├── patientsim/
│   ├── membersim/
│   ├── rxmembersim/
│   ├── trialsim/
│   ├── populationsim/
│   └── networksim/
├── packages/         # Python packages (infrastructure)
│   ├── core/
│   ├── patientsim/
│   ├── membersim/
│   └── rxmembersim/
├── formats/          # Output formats (SHARED)
├── references/       # Reference data (SHARED)
├── docs/             # Documentation
├── hello-healthsim/  # Tutorials
└── scripts/          # Utility scripts
```

### Common Verification Commands

```bash
# Check structure
ls -la skills/{product}/

# Verify no nested directories
find skills/{product} -type d

# Check frontmatter
head -4 skills/{product}/*.md
```

---

**Repository**: https://github.com/mark64oswald/healthsim-workspace

*End of Document*
