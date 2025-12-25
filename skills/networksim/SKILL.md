---
name: networksim
description: |
  Healthcare network knowledge and entity generation. Reference information about 
  network types, plan structures, pharmacy benefits, and PBM operations. Synthetic 
  generation of providers, facilities, pharmacies, and network configurations.
  Cross-product integration for realistic healthcare data generation.
  
  Trigger phrases: "network type", "HMO vs PPO", "generate provider", "generate facility",
  "generate pharmacy", "plan structure", "pharmacy benefit", "PBM", "network adequacy",
  "provider for encounter", "pharmacy for prescription"
version: "1.0"
status: "Active"
products:
  - patientsim
  - membersim
  - rxmembersim
  - trialsim
  - populationsim
---

# NetworkSim

## Overview

NetworkSim provides healthcare network knowledge and synthetic entity generation for the HealthSim ecosystem. Unlike other products that generate transaction data (encounters, claims, prescriptions), NetworkSim focuses on the structural elements that support those transactions:

1. **Reference Knowledge** - Network types, plan structures, pharmacy benefits, PBM operations
2. **Synthetic Generation** - Providers, facilities, pharmacies, network configurations
3. **Integration Patterns** - Cross-product enhancement for realistic data

## When to Use NetworkSim

| Need | Skill Category | Example Prompt |
|------|---------------|----------------|
| Understand network types | reference/ | "Explain the difference between HMO and PPO" |
| Learn about plan structures | reference/ | "What components make up a health plan benefit?" |
| Understand pharmacy benefits | reference/ | "Explain pharmacy tier structures" |
| Generate a provider | synthetic/ | "Generate a cardiologist in Houston" |
| Generate a facility | synthetic/ | "Generate a 200-bed community hospital" |
| Generate a pharmacy | synthetic/ | "Generate a specialty pharmacy in Boston" |
| Use a network template | patterns/ | "Create an HMO network configuration" |
| Enhance PatientSim | integration/ | "Generate a provider for this encounter" |
| Enhance MemberSim | integration/ | "Add network context to this claim" |
| Enhance RxMemberSim | integration/ | "Generate a pharmacy for this prescription" |

---

## Skill Categories

### Reference Knowledge (reference/)

Educational content about healthcare networks, plan structures, and pharmacy benefits. Use these skills to understand concepts before generating synthetic data.

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| [network-types](reference/network-types.md) | HMO, PPO, EPO, POS, HDHP definitions and comparisons | "explain HMO", "difference between PPO and EPO", "network types" |
| [plan-structures](reference/plan-structures.md) | Benefit design concepts: deductibles, copays, coinsurance | "plan structure", "deductible vs copay", "out-of-pocket max" |
| [pharmacy-benefit-concepts](reference/pharmacy-benefit-concepts.md) | Tier structures, formulary types, pharmacy networks | "tier structure", "formulary", "preferred pharmacy" |
| [pbm-operations](reference/pbm-operations.md) | PBM functions: claims processing, rebates, formulary management | "what is a PBM", "pharmacy benefit manager", "BIN PCN" |
| [utilization-management](reference/utilization-management.md) | Prior authorization, step therapy, quantity limits | "prior authorization", "step therapy", "quantity limits" |
| [specialty-pharmacy](reference/specialty-pharmacy.md) | Specialty drug distribution, hub model, REMS | "specialty pharmacy", "limited distribution", "hub model" |
| [network-adequacy](reference/network-adequacy.md) | Access standards, time/distance, provider ratios | "network adequacy", "access standards", "time distance" |

### Synthetic Generation (synthetic/)

Generate realistic synthetic healthcare entities. Each skill produces canonical JSON that can be transformed to various output formats.

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| [synthetic-provider](synthetic/synthetic-provider.md) | Generate provider entities with NPI, credentials, taxonomy | "generate provider", "create physician", "synthetic NPI" |
| [synthetic-facility](synthetic/synthetic-facility.md) | Generate facility entities with CCN, beds, services | "generate hospital", "create facility", "synthetic ASC" |
| [synthetic-pharmacy](synthetic/synthetic-pharmacy.md) | Generate pharmacy entities with NCPDP, type, services | "generate pharmacy", "create drugstore", "specialty pharmacy" |
| [synthetic-network](synthetic/synthetic-network.md) | Generate network configurations with provider rosters | "generate network", "create provider network", "build roster" |
| [synthetic-plan](synthetic/synthetic-plan.md) | Generate plan benefit structures | "generate plan", "create benefit design", "synthetic benefits" |
| [synthetic-pharmacy-benefit](synthetic/synthetic-pharmacy-benefit.md) | Generate pharmacy benefit designs | "generate pharmacy benefit", "create formulary tier" |

### Patterns & Templates (patterns/)

Reusable configuration patterns for common network and benefit structures. Use these as starting points for customization.

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| [hmo-network-pattern](patterns/hmo-network-pattern.md) | Typical HMO network structure | "HMO network pattern", "gatekeeper model" |
| [ppo-network-pattern](patterns/ppo-network-pattern.md) | Typical PPO network structure | "PPO network pattern", "open access" |
| [tiered-network-pattern](patterns/tiered-network-pattern.md) | Narrow/tiered network structures | "tiered network", "narrow network", "high performance" |
| [pharmacy-benefit-patterns](patterns/pharmacy-benefit-patterns.md) | Common PBM configurations | "pharmacy benefit pattern", "4-tier", "5-tier" |
| [specialty-distribution-pattern](patterns/specialty-distribution-pattern.md) | Hub vs retail routing | "specialty distribution", "hub model", "limited distribution" |

### Cross-Product Integration (integration/)

Enhance other HealthSim products with network context. These skills bridge NetworkSim entities into other product workflows.

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| [provider-for-encounter](integration/provider-for-encounter.md) | Generate provider for PatientSim encounter | "provider for this encounter", "attending physician for" |
| [network-for-member](integration/network-for-member.md) | Add network context to MemberSim member | "network for this member", "plan network" |
| [pharmacy-for-rx](integration/pharmacy-for-rx.md) | Generate pharmacy for RxMemberSim prescription | "pharmacy for this prescription", "dispensing pharmacy" |
| [benefit-for-claim](integration/benefit-for-claim.md) | Add benefit context to MemberSim claim | "benefit for this claim", "cost sharing" |
| [formulary-for-rx](integration/formulary-for-rx.md) | Add formulary context to RxMemberSim | "formulary for this drug", "tier for medication" |

---

## Quick Start Examples

### Example 1: Network Type Reference

```
User: What's the difference between an HMO and a PPO?

Claude: [Routes to reference/network-types.md]

HMO (Health Maintenance Organization) and PPO (Preferred Provider Organization) 
differ primarily in flexibility and cost:

| Aspect | HMO | PPO |
|--------|-----|-----|
| Network | Must use in-network providers | Can use any provider |
| Referrals | Required for specialists | Not required |
| PCP Required | Yes | No |
| Out-of-Network | Not covered (except emergency) | Covered at higher cost |
| Premiums | Lower | Higher |
| Cost Sharing | Lower | Higher |

HMOs work best for people who want lower costs and don't mind the gatekeeper model.
PPOs suit those who value flexibility and are willing to pay more for it.
```

### Example 2: Generate a Provider

```
User: Generate a cardiologist in San Diego

Claude: [Routes to synthetic/synthetic-provider.md]

{
  "npi": "1234567890",
  "entity_type": "individual",
  "provider": {
    "last_name": "Martinez",
    "first_name": "Elena",
    "credential": "MD, FACC",
    "gender": "F"
  },
  "taxonomy": {
    "code": "207RC0000X",
    "classification": "Internal Medicine",
    "specialization": "Cardiovascular Disease",
    "display_name": "Cardiologist"
  },
  "practice_location": {
    "address_line_1": "4567 Cardiovascular Way",
    "address_line_2": "Suite 300",
    "city": "San Diego",
    "state": "CA",
    "zip": "92121",
    "county": "San Diego",
    "phone": "858-555-0142"
  },
  "hospital_affiliations": [
    {
      "name": "Scripps Memorial Hospital La Jolla",
      "ccn": "050678",
      "privileges": ["Admitting", "Surgical"]
    }
  ],
  "accepting_new_patients": true,
  "languages": ["English", "Spanish"]
}
```

### Example 3: Cross-Product Integration

```
User: Generate a provider for this heart failure patient's cardiology referral

Claude: [Routes to integration/provider-for-encounter.md]

Based on the patient's heart failure diagnosis (I50.9) and location in Harris County, TX,
I'll generate an appropriate cardiologist:

{
  "npi": "1987654321",
  "entity_type": "individual",
  "provider": {
    "last_name": "Patel",
    "first_name": "Vikram",
    "credential": "MD, FACC, FHFSA",
    "gender": "M"
  },
  "taxonomy": {
    "code": "207RC0001X",
    "classification": "Internal Medicine",
    "specialization": "Advanced Heart Failure and Transplant Cardiology",
    "display_name": "Heart Failure Specialist"
  },
  "practice_location": {
    "city": "Houston",
    "state": "TX",
    "county_fips": "48201"
  },
  "integration_context": {
    "source_product": "patientsim",
    "matched_on": ["diagnosis_category", "geography"],
    "patient_diagnosis": "I50.9",
    "referral_reason": "Heart failure management"
  }
}
```

---

## Related Products

NetworkSim integrates with all other HealthSim products:

| Product | NetworkSim Provides | Integration Skill |
|---------|--------------------|--------------------|
| **PatientSim** | Providers for encounters, facilities for admissions | [provider-for-encounter](integration/provider-for-encounter.md) |
| **MemberSim** | Network context for claims, benefit structures | [network-for-member](integration/network-for-member.md) |
| **RxMemberSim** | Pharmacies for prescriptions, formulary concepts | [pharmacy-for-rx](integration/pharmacy-for-rx.md) |
| **TrialSim** | Sites and investigators for trials | [provider-for-encounter](integration/provider-for-encounter.md) |
| **PopulationSim** | Geographic context for provider distribution | [network-adequacy](reference/network-adequacy.md) |

---

## Boundary Rules

Understanding what NetworkSim owns vs. what other products own:

### NetworkSim Owns

- Network type knowledge and definitions
- Provider/facility/pharmacy entity generation
- Network configuration patterns
- Benefit design concepts (structure, not pricing)
- PBM operational concepts

### Other Products Own

| Responsibility | Owner Product |
|----------------|---------------|
| Claim processing logic | MemberSim |
| Claim adjudication | MemberSim |
| Formulary drug coverage decisions | RxMemberSim |
| Drug-specific PA criteria | RxMemberSim |
| Encounter generation | PatientSim |
| Clinical documentation | PatientSim |
| Geographic/demographic data | PopulationSim |
| SDOH indicators | PopulationSim |

### Collaboration Pattern

When generating data that spans boundaries:

1. **NetworkSim** generates the structural entity (provider, facility, pharmacy)
2. **Other product** consumes that entity in its workflow
3. **Identity correlation** maintained via NPI, CCN, NCPDP identifiers

---

## Output Formats

NetworkSim entities can be output in multiple formats:

| Format | Use Case | Available For |
|--------|----------|---------------|
| Canonical JSON | Default, cross-product integration | All entities |
| FHIR R4 | Interoperability | Providers, Facilities, Pharmacies |
| NPPES-style CSV | Bulk provider data | Providers |
| CMS POS-style | Facility reporting | Facilities |
| NCPDP-style | Pharmacy data exchange | Pharmacies |

---

## Documentation

- [README](README.md) - Product overview and quick start
- [Developer Guide](developer-guide.md) - Technical reference and workflows
- [Prompt Guide](prompt-guide.md) - Example prompts by category

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12 | Initial release with reference and synthetic skills |

---

*NetworkSim is part of the HealthSim ecosystem. For overall architecture, see the [HealthSim Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md).*
