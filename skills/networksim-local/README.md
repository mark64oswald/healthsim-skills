# NetworkSim-Local

**Version**: 0.1.0 (Development)  
**Status**: In Development  
**Parent**: HealthSim Platform

## Overview

NetworkSim-Local is an **independent, experimental** implementation that integrates real-world provider data from public CMS sources. Unlike NetworkSim (which generates synthetic provider data), NetworkSim-Local queries actual NPPES registry data stored locally.

## Key Differentiators

| Aspect | NetworkSim v1.0 | NetworkSim-Local |
|--------|-----------------|------------------|
| Data Source | Claude synthesis | Real NPPES/CMS data |
| NPI Values | Synthetic (valid format) | Actual NPIs from registry |
| Addresses | Plausible | Real practice locations |
| Specialties | Correct codes | Actual taxonomy assignments |
| Storage | None (on-demand) | Local DuckDB database |
| Repository | healthsim-workspace | healthsim-workspace (code only) |

## Design Principles

1. **Independence**: No coupling to NetworkSim - can evolve separately
2. **Code in Git, Data Local**: Scripts and skills committed; data files `.gitignore`d
3. **Real Data First**: Query actual records; synthesize only as fallback
4. **Provenance Tracking**: Every response indicates data source

## Data Sources

| Source | Provider | Size | Update Cycle | Cost |
|--------|----------|------|--------------|------|
| NPPES NPI Registry | CMS | ~1GB compressed | Monthly/Weekly | Free |
| Provider of Services | CMS | ~50MB | Quarterly | Free |
| ~~NCPDP dataQ~~ | ~~NCPDP~~ | ~~N/A~~ | ~~N/A~~ | ~~Proprietary~~ |

**Note**: NCPDP pharmacy database is proprietary. Pharmacies with NPIs are available in NPPES.

## Directory Structure

```
networksim-local/
├── README.md                 # This file
├── SKILL.md                  # Master skill (routes to detailed skills)
├── developer-guide.md        # Setup and development guide
├── data/                     # LOCAL ONLY - .gitignore'd
│   ├── README.md             # Documents download process (committed)
│   ├── .gitignore            # Excludes *.csv, *.parquet, *.duckdb
│   ├── raw/                  # Downloaded source files
│   └── processed/            # DuckDB database
├── setup/                    # Download and ETL scripts (committed)
│   ├── download-nppes.py
│   ├── filter-providers.py
│   └── build-database.py
├── skills/                   # Lookup and analysis skills
│   ├── provider-lookup.md
│   ├── facility-lookup.md
│   ├── pharmacy-lookup.md
│   └── geographic-analysis.md
└── queries/                  # SQL query templates
    ├── provider-by-npi.sql
    ├── providers-by-geography.sql
    └── specialty-distribution.sql
```

## Getting Started

See [developer-guide.md](developer-guide.md) for setup instructions.

## Relationship to Other Products

- **NetworkSim**: Parallel implementation (synthetic) - no dependency
- **PopulationSim**: Geographic grounding via FIPS codes
- **PatientSim/MemberSim/RxMemberSim**: Can reference real NPIs for encounters

---

*Part of the HealthSim Platform - Conversation-First Synthetic Healthcare Data*
