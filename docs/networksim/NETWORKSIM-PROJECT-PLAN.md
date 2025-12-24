# NetworkSim Project Plan

**Version**: 1.0  
**Created**: 2024-12-24  
**Status**: Planning Complete → Ready for Implementation

---

## 1. Executive Summary

NetworkSim serves as the **healthcare network knowledge and pattern library** for the HealthSim ecosystem. Unlike other HealthSim products that generate transaction data (encounters, claims, prescriptions), NetworkSim provides:

1. **Reference Knowledge** - Deep understanding of network types, plan structures, pharmacy benefits, and PBM operations
2. **Synthetic Generation** - Realistic but synthetic providers, facilities, pharmacies, and network configurations  
3. **Integration Patterns** - Cross-product enhancement for realistic provider assignments

### Strategic Decision: Two-Track Development

| Track | Purpose | Repository | Data |
|-------|---------|------------|------|
| **Public** | Reference knowledge + synthetic generation | healthsim-workspace | None (patterns only) |
| **Private** | Full implementation with real data | networksim-local | NPPES, POS, HPSA, etc. |

This plan covers **Track 1 (Public)** only. Track 2 will be developed separately.

---

## 2. Overlap Analysis: NetworkSim vs. Existing Products

### 2.1 MemberSim Overlap Analysis

**What MemberSim Already Has:**

| Component | MemberSim Location | Content |
|-----------|-------------------|---------|
| Plan Types | `core/plan.py` | HMO, PPO, EPO, POS, HDHP as string enum |
| Plan Model | `core/plan.py` | Deductibles, copays, coinsurance, OOP max |
| Network Flags | `Plan.requires_pcp`, `Plan.requires_referral` | Boolean flags for HMO behavior |
| Sample Plans | `SAMPLE_PLANS` dict | PPO_GOLD, HMO_STANDARD, HDHP_HSA examples |
| Provider Reference | `Claim.provider_npi`, `Claim.facility_npi` | NPI fields on claims |

**What NetworkSim Will Add (No Overlap):**

| Component | NetworkSim Scope | Value Added |
|-----------|------------------|-------------|
| Network Type **Knowledge** | WHY HMO vs PPO matters, behavioral implications | Deeper understanding, not just labels |
| Network **Configurations** | Tiered networks, narrow networks, EPO specifics | Generation patterns |
| Provider **Generation** | Realistic provider entities with specialties | Replace placeholder NPIs |
| Facility **Generation** | Hospitals, ASCs, SNFs with characteristics | Rich facility data |
| Network **Adequacy** | Time/distance standards, access metrics | Compliance context |
| Access **Disparity** | HPSA, MUA, provider desert concepts | PopulationSim integration |

**Boundary Rule**: 
- NetworkSim owns **network KNOWLEDGE and ENTITY GENERATION**
- MemberSim owns **claim PROCESSING using network context**

### 2.2 RxMemberSim Overlap Analysis

**What RxMemberSim Already Has:**

| Component | RxMemberSim Location | Content |
|-----------|---------------------|---------|
| Formulary Tiers | `formulary/` | 4-tier structure (Generic → Specialty) |
| Pharmacy Model | `MOD-011 Pharmacy` | NPI, pharmacy_type, chain_code |
| PBM Concepts | Throughout | BIN/PCN/Group, claim adjudication |
| Prior Auth | `prior_auth/` | PA workflows, ePA transactions |
| Specialty Pharmacy | `specialty/` | Hub model, REMS, copay assistance |
| DUR | `dur/` | Drug interactions, dose alerts |

**What NetworkSim Will Add (No Overlap):**

| Component | NetworkSim Scope | Value Added |
|-----------|------------------|-------------|
| Pharmacy Benefit **Design Concepts** | Benefit structure patterns, plan design rationale | Educational context |
| Pharmacy **Network Types** | Preferred vs non-preferred, mail order, specialty | Configuration patterns |
| PBM **Operational Models** | High-level PBM function explanation | Domain knowledge |
| Pharmacy **Generation** | Realistic pharmacy entities (chain, independent, specialty) | Replace placeholders |
| Specialty Distribution | Hub vs retail vs provider-administered patterns | Routing logic |

**Boundary Rule**:
- NetworkSim owns **pharmacy benefit KNOWLEDGE and PHARMACY ENTITY GENERATION**
- RxMemberSim owns **pharmacy claim PROCESSING and FORMULARY APPLICATION**

### 2.3 Clear Responsibility Matrix

| Domain | NetworkSim Owns | Other Product Owns |
|--------|-----------------|-------------------|
| **Network Types** | Knowledge, definitions, behavioral patterns | MemberSim: applying to claims |
| **Plan Benefits** | Design concepts, structure patterns | MemberSim: adjudication rules |
| **Providers** | Entity generation, specialty distribution | PatientSim: encounter assignment |
| **Facilities** | Entity generation, service capabilities | PatientSim: encounter location |
| **Pharmacies** | Entity generation, network classification | RxMemberSim: claim routing |
| **Formulary** | Tier structure concepts | RxMemberSim: drug coverage rules |
| **PBM** | Operational model concepts | RxMemberSim: claim processing |
| **Prior Auth** | Concept explanation | MemberSim/RxMemberSim: workflows |

---

## 3. Scope Definition

### 3.1 In Scope

**Reference Knowledge (Educational)**
- Network type definitions and behavioral implications
- Plan structure concepts and design patterns
- Pharmacy benefit design principles
- PBM operational model overview
- Utilization management concepts (PA, step therapy, QL)
- Specialty pharmacy models
- Network adequacy standards
- Access disparity concepts (HPSA, MUA, provider deserts)

**Synthetic Generation (Patterns)**
- Provider entity generation (NPI, name, specialty, credentials, location)
- Facility entity generation (hospital, ASC, SNF, etc.)
- Pharmacy entity generation (retail chain, independent, mail, specialty)
- Network configuration templates (HMO, PPO, tiered, narrow)
- Plan benefit templates (basic structures)
- Pharmacy benefit templates (tier structures)

**Integration Patterns**
- Provider-for-encounter (PatientSim)
- Network-for-member (MemberSim)
- Pharmacy-for-claim (RxMemberSim)
- Site-for-trial (TrialSim)
- Access-for-population (PopulationSim)

### 3.2 Out of Scope (Public Version)

- Real provider data (NPPES) - deferred to networksim-local
- Real facility data (POS) - deferred to networksim-local
- Real shortage area data (HPSA) - deferred to networksim-local
- Real plan data (MA Landscape, Exchange PUFs) - deferred to networksim-local
- Fake company names pretending to be real
- Actual claim adjudication logic (MemberSim/RxMemberSim responsibility)
- Formulary drug coverage rules (RxMemberSim responsibility)

---

## 4. Skill Architecture

```
skills/networksim/
├── SKILL.md                              # Master router
├── README.md                             # Product overview (updated)
│
├── reference/                            # KNOWLEDGE SKILLS
│   ├── network-types.md                  # HMO, PPO, EPO, POS, HDHP definitions
│   ├── plan-structures.md                # Benefit design concepts
│   ├── pharmacy-benefit-concepts.md      # Tier structures, formulary concepts
│   ├── pbm-operations.md                 # PBM function overview
│   ├── specialty-pharmacy.md             # Hub model, REMS, specialty distribution
│   ├── utilization-management.md         # PA, step therapy, quantity limits
│   └── network-adequacy.md               # Time/distance, access standards
│
├── synthetic/                            # GENERATION SKILLS
│   ├── synthetic-provider.md             # Generate provider entities
│   ├── synthetic-facility.md             # Generate facility entities
│   ├── synthetic-pharmacy.md             # Generate pharmacy entities
│   ├── synthetic-network.md              # Generate network configurations
│   ├── synthetic-plan.md                 # Generate plan benefit structures
│   └── synthetic-pharmacy-benefit.md     # Generate pharmacy benefit designs
│
├── patterns/                             # TEMPLATE SKILLS
│   ├── hmo-network-pattern.md            # Typical HMO structure
│   ├── ppo-network-pattern.md            # Typical PPO structure
│   ├── tiered-network-pattern.md         # Narrow/tiered network
│   ├── pharmacy-benefit-patterns.md      # Common PBM configurations
│   └── specialty-distribution-pattern.md # Hub vs retail routing
│
├── integration/                          # CROSS-PRODUCT SKILLS
│   ├── provider-for-encounter.md         # PatientSim integration
│   ├── network-for-member.md             # MemberSim integration
│   ├── benefit-for-claim.md              # MemberSim claims
│   ├── pharmacy-for-rx.md                # RxMemberSim integration
│   └── formulary-concepts-for-rx.md      # RxMemberSim formulary context
│
└── data-sources-reference.md             # Where real data lives (for local version)
```

### 4.1 Skill Dependencies

```
                    ┌─────────────────┐
                    │    SKILL.md     │
                    │ (Master Router) │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   reference/    │ │   synthetic/    │ │   patterns/     │
│   (Knowledge)   │ │  (Generation)   │ │  (Templates)    │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  integration/   │
                    │ (Cross-Product) │
                    └─────────────────┘
```

---

## 5. Implementation Phases

### Phase 1: Foundation + Reference Knowledge
**Duration**: 1-2 sessions  
**Goal**: Establish structure and educational content

| ID | Task | Type | Priority | Status |
|----|------|------|----------|--------|
| 1.1 | Create directory structure | Setup | Must | ⬜ Not Started |
| 1.2 | Update SKILL.md (master router) | Skill | Must | ⬜ Not Started |
| 1.3 | Update README.md | Doc | Must | ⬜ Not Started |
| 1.4 | Write network-types.md | Reference | Must | ⬜ Not Started |
| 1.5 | Write plan-structures.md | Reference | Must | ⬜ Not Started |
| 1.6 | Write pharmacy-benefit-concepts.md | Reference | Must | ⬜ Not Started |
| 1.7 | Write pbm-operations.md | Reference | Should | ⬜ Not Started |
| 1.8 | Write utilization-management.md | Reference | Should | ⬜ Not Started |
| 1.9 | Write specialty-pharmacy.md | Reference | Should | ⬜ Not Started |
| 1.10 | Write network-adequacy.md | Reference | Could | ⬜ Not Started |

### Phase 2: Synthetic Generation
**Duration**: 1-2 sessions  
**Goal**: Provider, facility, pharmacy generation capabilities

| ID | Task | Type | Priority | Status |
|----|------|------|----------|--------|
| 2.1 | Write synthetic-provider.md | Generator | Must | ⬜ Not Started |
| 2.2 | Write synthetic-facility.md | Generator | Must | ⬜ Not Started |
| 2.3 | Write synthetic-pharmacy.md | Generator | Must | ⬜ Not Started |
| 2.4 | Write synthetic-network.md | Generator | Should | ⬜ Not Started |
| 2.5 | Write synthetic-plan.md | Generator | Should | ⬜ Not Started |
| 2.6 | Write synthetic-pharmacy-benefit.md | Generator | Could | ⬜ Not Started |

### Phase 3: Patterns + Templates
**Duration**: 1 session  
**Goal**: Reusable configuration patterns

| ID | Task | Type | Priority | Status |
|----|------|------|----------|--------|
| 3.1 | Write hmo-network-pattern.md | Pattern | Should | ⬜ Not Started |
| 3.2 | Write ppo-network-pattern.md | Pattern | Should | ⬜ Not Started |
| 3.3 | Write pharmacy-benefit-patterns.md | Pattern | Should | ⬜ Not Started |
| 3.4 | Write tiered-network-pattern.md | Pattern | Could | ⬜ Not Started |
| 3.5 | Write specialty-distribution-pattern.md | Pattern | Could | ⬜ Not Started |

### Phase 4: Cross-Product Integration
**Duration**: 1-2 sessions  
**Goal**: Connect NetworkSim to other products

| ID | Task | Type | Priority | Status |
|----|------|------|----------|--------|
| 4.1 | Write provider-for-encounter.md | Integration | Must | ⬜ Not Started |
| 4.2 | Write network-for-member.md | Integration | Must | ⬜ Not Started |
| 4.3 | Write pharmacy-for-rx.md | Integration | Must | ⬜ Not Started |
| 4.4 | Write benefit-for-claim.md | Integration | Should | ⬜ Not Started |
| 4.5 | Write formulary-concepts-for-rx.md | Integration | Should | ⬜ Not Started |
| 4.6 | Update PatientSim cross-references | Integration | Must | ⬜ Not Started |
| 4.7 | Update MemberSim cross-references | Integration | Must | ⬜ Not Started |
| 4.8 | Update RxMemberSim cross-references | Integration | Must | ⬜ Not Started |

### Phase 5: Documentation + Testing
**Duration**: 1 session  
**Goal**: Polish and verify

| ID | Task | Type | Priority | Status |
|----|------|------|----------|--------|
| 5.1 | Write data-sources-reference.md | Doc | Should | ⬜ Not Started |
| 5.2 | Add hello-healthsim examples | Doc | Must | ⬜ Not Started |
| 5.3 | Update HEALTHSIM-ARCHITECTURE-GUIDE.md | Doc | Must | ⬜ Not Started |
| 5.4 | Update master SKILL.md cross-references | Doc | Must | ⬜ Not Started |
| 5.5 | Verify all skill frontmatter | QA | Must | ⬜ Not Started |
| 5.6 | Test sample generation requests | QA | Must | ⬜ Not Started |

---

## 6. Skill Specifications

### 6.1 Reference Skills

#### network-types.md
**Purpose**: Define network types with behavioral implications

**Content Outline**:
- HMO: Definition, PCP requirement, referral patterns, in-network only
- PPO: Definition, flexibility, in/out-of-network cost sharing
- EPO: Definition, hybrid characteristics
- POS: Definition, point-of-service decisions
- HDHP: Definition, HSA compatibility, high deductible thresholds
- Comparison table with cost/flexibility tradeoffs
- When to use each type in generation

**Cross-references**: MemberSim plan model, synthetic-network.md

#### pharmacy-benefit-concepts.md
**Purpose**: Explain pharmacy benefit design (complements RxMemberSim)

**Content Outline**:
- Tier structure concepts (why tiers exist, typical configurations)
- Open vs closed formulary
- Preferred vs non-preferred networks
- Mail order benefits
- Specialty pharmacy requirements
- Accumulator designs
- **NOT included**: Drug-specific coverage (RxMemberSim owns this)

**Cross-references**: RxMemberSim formulary skills, synthetic-pharmacy-benefit.md

### 6.2 Synthetic Generation Skills

#### synthetic-provider.md
**Purpose**: Generate realistic synthetic provider entities

**Generation Capabilities**:
- Valid NPI format (Luhn-compliant with SYNTHETIC marker)
- Realistic names (culturally appropriate by geography)
- Specialty assignment (weighted by national distribution)
- Credentials (MD, DO, NP, PA with appropriate specialties)
- Practice address (realistic for specified geography)
- Taxonomy codes (valid NUCC codes)
- Provider type (Type 1 individual)

**Provenance**: All output flagged `"provenance": "SYNTHETIC"`

#### synthetic-pharmacy.md
**Purpose**: Generate realistic synthetic pharmacy entities

**Generation Capabilities**:
- Valid NPI format
- Pharmacy classification (retail chain, retail independent, mail, specialty)
- Chain affiliation patterns (CVS, Walgreens, etc. as patterns not actual)
- Services offered (compounding, specialty, immunizations)
- Hours and access patterns
- Network participation indicators

### 6.3 Integration Skills

#### provider-for-encounter.md
**Purpose**: How PatientSim requests providers from NetworkSim

**Integration Pattern**:
```
PatientSim: "I need an endocrinologist in San Diego for a diabetes patient"
           ↓
NetworkSim: Generates provider with:
           - Specialty: Endocrinology (207RE0101X)
           - Location: San Diego County
           - Credentials: MD or DO
           - NPI: Valid synthetic
           ↓
PatientSim: Uses provider in encounter
```

---

## 7. Quality Gates

### Pre-Implementation Checklist
- [x] Overlap analysis complete
- [x] Scope clearly defined
- [x] Boundary rules established with other products
- [x] Skill architecture designed
- [x] Phase plan created
- [ ] Super-prompt created for implementation

### Per-Phase Completion Criteria

**Phase Complete When**:
- [ ] All "Must" priority tasks complete
- [ ] All skills have YAML frontmatter
- [ ] All skills have ≥2 examples
- [ ] Cross-references verified
- [ ] Git commit with descriptive message

### Final Completion Criteria
- [ ] All phases complete
- [ ] CHANGELOG.md updated
- [ ] README.md accurate
- [ ] Master SKILL.md routes correctly
- [ ] hello-healthsim examples work
- [ ] Architecture guide updated
- [ ] VS Code workspace updated if needed

---

## 8. Risk Mitigation

### Risk 1: Overlap with MemberSim/RxMemberSim
**Mitigation**: 
- Clear boundary rules in Section 2
- Reference skills EXPLAIN concepts, don't IMPLEMENT logic
- Review each skill against boundary rules before committing

### Risk 2: Context Window Overflow
**Mitigation**:
- Create implementation super-prompt with chunked tasks
- Process one phase per session
- Save progress to status document after each session

### Risk 3: Scope Creep
**Mitigation**:
- "Out of Scope" section clearly defined
- Real data features deferred to networksim-local
- Stick to patterns/knowledge, not fake company data

---

## 9. Success Metrics

| Metric | Target |
|--------|--------|
| Reference skills complete | 7 skills |
| Synthetic generation skills | 6 skills |
| Pattern skills | 5 skills |
| Integration skills | 5 skills |
| Cross-product references updated | 3 products |
| Hello-healthsim examples | ≥3 examples |
| All skill frontmatter valid | 100% |

---

## 10. Next Steps

1. **Review this plan** - Confirm scope and boundaries
2. **Create super-prompt** - Detailed implementation instructions for Phase 1
3. **Begin Phase 1** - Foundation + Reference Knowledge
4. **Track progress** - Update NETWORKSIM-IMPLEMENTATION-STATUS.md after each session

---

## Appendix A: Skill Template

```markdown
---
name: networksim-[skill-name]
description: "[Brief description with trigger phrases]"
version: "1.0"
status: "Active"
---

# [Skill Name]

## Overview
[2-3 sentence description]

## Trigger Phrases
- "[Example trigger 1]"
- "[Example trigger 2]"

## [Main Content Sections]

## Examples

### Example 1: [Title]
**Request**: "[User request]"
**Response**: [Generated output]

### Example 2: [Title]
**Request**: "[User request]"
**Response**: [Generated output]

## Related Skills
- [skill-name.md](path) - Description
- [skill-name.md](path) - Description
```

---

*Document Version: 1.0 | Last Updated: 2024-12-24*
