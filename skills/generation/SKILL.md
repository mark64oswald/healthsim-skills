---
name: Generative Framework
description: Conversation-driven specification and execution of healthcare data generation at scale
triggers:
  - build profile
  - create profile
  - generate cohort
  - build journey
  - create journey
  - generate journey
  - batch generate
  - quick generate
  - distribution
  - specify
  - at scale
---

# Generative Framework Skills

Use these skills when building specifications for data generation or executing batch generation.

## Quick Reference

| Skill | Use When | Location |
|-------|----------|----------|
| **Profile Builder** | Defining population characteristics for batch generation | [builders/profile-builder.md](builders/profile-builder.md) |
| **Journey Builder** | Defining temporal event sequences | [builders/journey-builder.md](builders/journey-builder.md) |
| **Quick Generate** | Simple single-entity generation | [builders/quick-generate.md](builders/quick-generate.md) |
| **Profile Executor** | Executing a profile specification | [executors/profile-executor.md](executors/profile-executor.md) |
| **Journey Executor** | Executing a journey specification | [executors/journey-executor.md](executors/journey-executor.md) |
| **Cross-Domain Sync** | Coordinating cross-product generation | [executors/cross-domain-sync.md](executors/cross-domain-sync.md) |

## Trigger Phrases

### Building Specifications

- "Build a profile for 100 Medicare members"
- "Create a journey for diabetic patients"
- "Specify a commercial cohort with CHF"
- "Define a surgical episode journey"

### Executing Specifications

- "Generate patients from this profile"
- "Execute the diabetic journey for 50 patients"
- "Run batch generation for this cohort"

### Using Templates

- "Use the Medicare diabetic template"
- "Start with the surgical episode journey"
- "Generate using the commercial healthy profile"

## Workflow Overview

### 1. Build a Profile (Optional)

```
Build a profile for 200 Medicare Advantage members:
- Age 65-85, normal distribution centered at 74
- 40% with Type 2 diabetes
- 30% with heart failure
- San Diego County geography
```

### 2. Build a Journey (Optional)

```
Create a first-year diabetic journey:
- Initial diagnosis visit with labs
- Metformin prescription
- Quarterly follow-ups with A1c
- Possible titration to second agent
```

### 3. Execute Generation

```
Generate the cohort using this profile and journey
Save as scenario "ma-diabetic-cohort-2025"
```

## Distribution Types

| Type | Use Case | Example |
|------|----------|---------|
| `categorical` | Discrete choices | Gender: M/F/Other |
| `normal` | Bell curve | Age centered at 72 |
| `log_normal` | Skewed positive | Healthcare costs |
| `uniform` | Equal probability | Random day in range |
| `explicit` | Specific values | Exactly these NDCs |

See [distributions/distribution-types.md](distributions/distribution-types.md) for details.

## Journey Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| `linear` | Simple sequence | Office visit → Lab → Follow-up |
| `branching` | Decision points | ER → Admit OR Discharge |
| `protocol` | Trial schedules | Cycle 1 Day 1, Day 8, Day 15 |
| `lifecycle` | Long-term patterns | New member first year |

See the [journeys/](journeys/) folder for pattern details.

## Integration with Products

The Generative Framework orchestrates all HealthSim products:

| When Generating | Products Involved | Cross-Domain Triggers |
|-----------------|-------------------|----------------------|
| Patient cohort | PatientSim, NetworkSim | Provider assignment |
| Member claims | MemberSim, PatientSim, NetworkSim | Encounter → Claim |
| Pharmacy fills | RxMemberSim, PatientSim, NetworkSim | Rx → Fill, DUR check |
| Trial subjects | TrialSim, PatientSim, NetworkSim | Subject ↔ Patient linking |

## Templates

Pre-built profiles and journeys for common use cases:

### Profile Templates

- [medicare-diabetic.md](templates/profiles/medicare-diabetic.md) - Medicare T2DM cohort
- [commercial-healthy.md](templates/profiles/commercial-healthy.md) - Commercial healthy adults
- [medicaid-pediatric.md](templates/profiles/medicaid-pediatric.md) - Medicaid children

### Journey Templates

- [diabetic-first-year.md](templates/journeys/diabetic-first-year.md) - New T2DM diagnosis year 1
- [surgical-episode.md](templates/journeys/surgical-episode.md) - Elective surgery episode
- [new-member-onboarding.md](templates/journeys/new-member-onboarding.md) - New member first 90 days

## Related Skills

- **[State Management](../common/state-management.md)** - Save/load generated scenarios
- **[Identity Correlation](../common/identity-correlation.md)** - Cross-product entity linking
- **[PopulationSim](../populationsim/SKILL.md)** - Real-world demographic data
- **[NetworkSim](../networksim/SKILL.md)** - Real provider assignments

---

*Implementation Status: Foundation phase. See [CURRENT-WORK.md](../../CURRENT-WORK.md) for details.*
