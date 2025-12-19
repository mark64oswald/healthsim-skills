---
name: healthsim-networksim
description: "Generate synthetic provider networks and facility data. Status: PLANNED - Not yet implemented."
---

# NetworkSim

**Status**: Planned - Not yet implemented

NetworkSim will generate synthetic provider network and facility data.

## Planned Features

- Provider generation (NPI, specialty, credentials)
- Network configurations (PPO, HMO, EPO, POS)
- Facility data (hospitals, clinics, pharmacies, labs)
- Geographic coverage patterns
- Contract and reimbursement structures
- Credentialing and enrollment status
- Network adequacy metrics

## Integration Points

| Integrates With | Provides |
|-----------------|----------|
| PatientSim | Attending/referring providers for encounters |
| MemberSim | Network providers for claims, prior auth |
| RxMemberSim | Pharmacy network, prescribers |
| TrialSim | Sites, investigators, research staff |
| PopulationSim | Service area alignment |

## Planned Entity Types

### Provider
- NPI (Type 1 - Individual)
- Specialty and subspecialty
- Credentials and certifications
- Practice locations
- Network participation

### Facility
- NPI (Type 2 - Organization)
- Facility type (hospital, clinic, ASC, etc.)
- Services offered
- Accreditation status
- Network participation

### Network
- Network type (PPO, HMO, etc.)
- Geographic coverage
- Provider directory
- Tiered structures
- Narrow network configurations

## Development Roadmap

1. Define provider entity model (align with NPPES)
2. Implement specialty distribution patterns
3. Add facility types and services
4. Create network configuration patterns
5. Build geographic coverage logic
6. Integrate with other products

See [Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) for details.

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Clinical patient data
- [MemberSim](../membersim/SKILL.md) - Claims with provider references
- [PopulationSim](../populationsim/SKILL.md) - Service area demographics
- [Code Systems](../../references/code-systems.md) - NPI, taxonomy codes
