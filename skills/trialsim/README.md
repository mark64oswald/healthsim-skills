# TrialSim Skills

Clinical trial synthetic data generation skills for HealthSim.

## Directory Structure

```
skills/trialsim/
├── README.md                          # This file
├── SKILL.md                           # Product router
├── clinical-trials-domain.md          # Core domain knowledge
├── recruitment-enrollment.md          # Recruitment funnel
│
├── phase1-dose-escalation.md          # Phase I scenarios
├── phase2-proof-of-concept.md         # Phase II scenarios
├── phase3-pivotal.md                  # Phase III scenarios
├── phase4-postmarket.md               # Phase IV scenarios
├── adaptive-design.md                 # Adaptive trial designs
├── rare-disease.md                    # Small population trials
│
├── therapeutic-areas/                 # Indication-specific skills
│   ├── README.md                      # Therapeutic area index
│   ├── oncology.md                    # Solid tumors, RECIST
│   ├── cardiovascular.md              # MACE, CV outcomes
│   ├── cns.md                         # Neurological endpoints
│   └── cgt.md                         # Cell & Gene Therapy
│
└── rwe/                               # Real World Evidence
    ├── README.md                      # RWE concepts index
    ├── overview.md                    # RWE fundamentals
    └── synthetic-control.md           # External control generation
```

**Note:** TrialSim uses subdirectories for complex, related skill groups (therapeutic areas, RWE). This matches PatientSim's pattern with `oncology/` and `pediatrics/` subdirectories.

## Quick Reference

| I want to generate... | Skill | Key Triggers |
|-----------------------|-------|--------------|
| A Phase III pivotal trial | `phase3-pivotal.md` | "Phase 3", "pivotal", "registrational", "confirmatory" |
| A first-in-human study | `phase1-dose-escalation.md` | "Phase 1", "dose escalation", "first-in-human", "MTD" |
| A proof-of-concept trial | `phase2-proof-of-concept.md` | "Phase 2", "proof of concept", "exploratory", "dose finding" |
| An oncology trial | `therapeutic-areas/oncology.md` | "oncology", "cancer", "tumor", "RECIST", "ORR" |
| A cardiovascular trial | `therapeutic-areas/cardiovascular.md` | "cardiovascular", "MACE", "heart failure", "CV outcome" |
| A CNS/neurology trial | `therapeutic-areas/cns.md` | "CNS", "neurology", "Alzheimer's", "Parkinson's", "MS" |
| A cell/gene therapy trial | `therapeutic-areas/cgt.md` | "gene therapy", "CAR-T", "cell therapy", "CGT" |
| Recruitment/screening data | `recruitment-enrollment.md` | "screening", "enrollment", "screen failure", "consent" |
| External control arm | `rwe/synthetic-control.md` | "synthetic control", "external control", "RWE" |
| Adverse events and safety | `clinical-trials-domain.md` | "adverse events", "AE", "safety", "SAE" |

## Implementation Status

| Skill | Status | Notes |
|-------|--------|-------|
| clinical-trials-domain.md | ✅ Complete | Core domain knowledge |
| phase3-pivotal.md | ✅ Complete | Comprehensive Phase III |
| recruitment-enrollment.md | ✅ Complete | Screening funnel, I/E |
| therapeutic-areas/oncology.md | ✅ Complete | RECIST, survival |
| therapeutic-areas/cardiovascular.md | ✅ Complete | MACE, HF |
| therapeutic-areas/cns.md | ✅ Complete | Cognitive, imaging |
| therapeutic-areas/cgt.md | ✅ Complete | CAR-T, gene therapy |
| rwe/overview.md | ✅ Complete | RWE concepts |
| rwe/synthetic-control.md | ✅ Complete | External controls |
| phase1-dose-escalation.md | 📋 Planned | Phase 2 |
| phase2-proof-of-concept.md | 📋 Planned | Phase 2 |
| phase4-postmarket.md | 📋 Planned | Phase 3 |
| adaptive-design.md | 📋 Planned | Phase 3 |
| rare-disease.md | 📋 Planned | Phase 3 |

## Development Roadmap

See [TrialSim Development Guide v3.0](../../docs/trialsim-development-guide-v3.md) for complete roadmap.

**Phase 1 (Foundation):** Domain knowledge, Phase 3 pivotal ✅
**Phase 2 (Core Scenarios):** Recruitment, additional phases
**Phase 3 (Therapeutic Depth):** Indication-specific skills
**Phase 4 (Advanced):** RWE, adaptive designs, rare disease

## Related Documentation

- [HealthSim Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md)
- [Hello HealthSim Examples](../../hello-healthsim/examples/)
- [CDISC SDTM Format](../../formats/cdisc-sdtm.md)
