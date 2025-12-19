---
name: healthsim-populationsim
description: "Generate synthetic population demographics and SDOH data. Status: PLANNED - Not yet implemented."
---

# PopulationSim

**Status**: Planned - Not yet implemented

PopulationSim will generate synthetic population demographics and social determinants of health (SDOH) data.

## Planned Features

- Census-based demographic distributions
- Geographic patterns (urban/rural, regional)
- SDOH indices and factors
- Income and education distributions
- Housing and transportation access
- Healthcare access patterns
- Cohort generation for other HealthSim products

## Integration Points

| Integrates With | Provides |
|-----------------|----------|
| PatientSim | Demographic patterns for patient generation |
| MemberSim | Geographic distribution for member populations |
| RxMemberSim | Pharmacy access patterns |
| TrialSim | Population-level trial recruitment pools |
| NetworkSim | Service area demographics |

## Planned Data Sources

- US Census Bureau data
- American Community Survey (ACS)
- Area Deprivation Index (ADI)
- Social Vulnerability Index (SVI)
- CDC/ATSDR Environmental Justice Index

## Development Roadmap

1. Define core demographic entity model
2. Implement census-based distribution patterns
3. Add SDOH index calculations
4. Create geographic cohort generation
5. Build integration patterns with other products

See [Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) for details.

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data
- [MemberSim](../membersim/SKILL.md) - Health plan member data
- [NetworkSim](../networksim/SKILL.md) - Provider network data
