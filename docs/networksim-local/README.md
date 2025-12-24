# NetworkSim-Local Documentation

**Status**: Future Project (Planning Complete)  
**Prerequisite**: NetworkSim (skills-based) must be completed first  
**Last Updated**: 2024-12-24

---

## Overview

NetworkSim-Local is the planned data infrastructure layer for the HealthSim ecosystem, providing access to **real** healthcare provider, facility, and pharmacy data from public sources. While NetworkSim (skills-based) generates synthetic entities and provides reference knowledge, NetworkSim-Local stores and queries actual data.

### Relationship to NetworkSim

```
┌────────────────────────────────────────────────────────────────┐
│                     NETWORKSIM ECOSYSTEM                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NetworkSim (Skills)              NetworkSim-Local              │
│  ┌─────────────────────┐          ┌─────────────────────┐      │
│  │ • Reference Knowledge│          │ • NPPES Provider Data│      │
│  │ • Synthetic Providers│   +      │ • CMS Facility Data  │      │
│  │ • Synthetic Facilities│         │ • Pharmacy Directory │      │
│  │ • Network Patterns   │          │ • Geocoded Locations │      │
│  └─────────────────────┘          └─────────────────────┘      │
│           │                                │                    │
│           └────────────┬───────────────────┘                    │
│                        ▼                                        │
│               Combined Capabilities:                            │
│               • Real NPIs for synthetic encounters              │
│               • Geographic provider distribution                │
│               • Network adequacy calculations                   │
│               • Cross-product enhancement                       │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Documents in This Folder

| Document | Purpose | Status |
|----------|---------|--------|
| [NETWORKSIM-LOCAL-PROJECT-REQUIREMENTS.md](NETWORKSIM-LOCAL-PROJECT-REQUIREMENTS.md) | Functional and non-functional requirements | Complete |
| [NETWORKSIM-LOCAL-DATA-ARCHITECTURE.md](NETWORKSIM-LOCAL-DATA-ARCHITECTURE.md) | Database schema, ERD, table specifications | Complete |
| [NETWORKSIM-LOCAL-DATA-SOURCES.md](NETWORKSIM-LOCAL-DATA-SOURCES.md) | Public data source inventory and details | Complete |
| [NETWORKSIM-LOCAL-IMPLEMENTATION-PLAN.md](NETWORKSIM-LOCAL-IMPLEMENTATION-PLAN.md) | Phased implementation approach | Complete |

---

## Key Technical Decisions

### Architecture
- **Database**: DuckDB (follows PopulationSim-Local pattern)
- **Interface**: MCP server (TypeScript)
- **Integration**: Attachable to PopulationSim database for geographic joins

### Data Sources (All Free/Public)
- **Providers**: NPPES NPI Registry (~3.3M active)
- **Facilities**: CMS Provider of Services (~75K)
- **Pharmacies**: NPPES extraction + curation (~65K)
- **Reference**: NUCC Taxonomy codes

### Estimated Scope
- **Database Size**: ~3GB
- **Implementation Time**: 4-6 weeks
- **Refresh Frequency**: Monthly (providers), Quarterly (facilities/pharmacies)

---

## Prerequisites Before Implementation

1. ✅ NetworkSim skills-based implementation complete (in progress)
2. ✅ PopulationSim-Local operational (complete)
3. ✅ Data sources researched and documented (complete)
4. ⏳ NetworkSim Phase 5 (documentation) complete

---

## When to Start

NetworkSim-Local implementation should begin **after**:
- NetworkSim Phases 1-5 complete
- All NetworkSim skills tested and documented
- Cross-product integration verified

The planning documents in this folder provide a complete roadmap for implementation when the time comes.

---

## Quick Reference: Data Volumes

| Entity | Source | Records | Update |
|--------|--------|---------|--------|
| Individual Providers | NPPES | ~2.5M | Monthly |
| Organization Providers | NPPES | ~800K | Monthly |
| Hospitals | CMS POS | ~6,500 | Quarterly |
| SNFs | CMS POS | ~15,000 | Quarterly |
| Other Facilities | CMS POS | ~50,000 | Quarterly |
| Pharmacies | NPPES Extract | ~65,000 | Quarterly |
| Specialty Pharmacies | Curated | ~1,500 | Quarterly |

---

## Related Documentation

- [NetworkSim Project Plan](../networksim/NETWORKSIM-PROJECT-PLAN.md) - Skills-based product
- [PopulationSim-Local](../../mcp-servers/populationsim-local/) - Pattern to follow
- [HealthSim Architecture Guide](../HEALTHSIM-ARCHITECTURE-GUIDE.md) - Overall architecture

---

*This folder contains planning documents only. Implementation will occur after NetworkSim (skills-based) is complete.*
