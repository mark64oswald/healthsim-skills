# NetworkSim-Local

**Real Provider Data Integration for HealthSim**

> ⚠️ **Experimental**: This is an independent implementation from NetworkSim, exploring real NPPES data integration versus synthetic generation.

---

## Overview

NetworkSim-Local provides **actual provider, facility, and pharmacy data** from public CMS sources, enabling HealthSim to generate synthetic healthcare scenarios with real-world provider grounding.

| Aspect | NetworkSim (v1.0) | NetworkSim-Local |
|--------|-------------------|------------------|
| **Data source** | Claude generates | Real NPPES/CMS files |
| **NPI** | Synthetic (valid format) | Real NPIs from registry |
| **Addresses** | Plausible | Actual practice locations |
| **Specialties** | Correct codes | Real taxonomy assignments |
| **Storage** | None (on-demand) | Local DuckDB database |

---

## Data Sources

| Source | Description | Update Frequency |
|--------|-------------|------------------|
| **NPPES NPI Registry** | 8.6M+ provider records | Monthly |
| **CMS Provider of Services** | Hospital/facility characteristics | Quarterly |
| **NUCC Taxonomy Codes** | Specialty classification | Semi-annual |

---

## Quick Start

### 1. Prerequisites

```bash
# Python 3.9+
pip install -r setup/requirements.txt
```

### 2. Download Data

```bash
# Download and filter NPPES data
python setup/download-nppes.py

# Download taxonomy codes
python setup/download-taxonomy.py

# Build DuckDB database
python setup/build-local-db.py
```

### 3. Verify Installation

```bash
# Run validation queries
python setup/validate-db.py
```

---

## Usage

### Provider Lookup

```
Find the provider with NPI 1234567890
```

**Response includes**:
- Provider name and credentials
- Practice location
- Primary specialty (from NPPES taxonomy)
- Source attribution: "NPPES Registry, November 2025"

### Geographic Search

```
Find cardiologists in San Diego, CA
```

### Facility Lookup

```
What hospitals are in Cook County, IL?
```

---

## Directory Structure

```
networksim-local/
├── SKILL.md              # Master skill file
├── README.md             # This file
├── developer-guide.md    # Detailed setup guide
│
├── data/                 # LOCAL ONLY - not in git
│   ├── README.md         # Download instructions
│   ├── .gitignore        # Excludes data files
│   ├── nppes/            # Raw NPPES CSV files
│   ├── cms-pos/          # CMS Provider of Services
│   ├── taxonomy/         # NUCC taxonomy codes
│   └── networksim-local.duckdb  # Processed database
│
├── setup/                # Setup scripts (in git)
│   ├── download-nppes.py
│   ├── filter-providers.py
│   ├── build-local-db.py
│   └── requirements.txt
│
├── skills/               # Lookup skills
│   ├── provider-lookup.md
│   ├── facility-lookup.md
│   └── geographic-search.md
│
└── queries/              # SQL templates
    ├── provider-by-npi.sql
    └── providers-by-specialty.sql
```

---

## Data Coverage

### Current Filtering Strategy

- **Active providers only** (no deactivation date)
- **Top 10 states**: CA, TX, NY, FL, IL, PA, OH, GA, NC, MI
- **Estimated records**: ~3 million
- **Database size**: ~700MB (Parquet/DuckDB)

### Provider Types Included

- ✅ Physicians (MD, DO)
- ✅ Nurse Practitioners
- ✅ Physician Assistants
- ✅ Pharmacies
- ✅ Hospitals
- ✅ Ambulatory Surgery Centers
- ✅ Skilled Nursing Facilities
- ✅ Home Health Agencies
- ✅ Laboratories

---

## Cross-Product Integration

NetworkSim-Local integrates with other HealthSim products:

| Product | Integration |
|---------|-------------|
| **PatientSim** | Real NPIs for attending/referring physicians |
| **MemberSim** | Actual provider networks by geography |
| **RxMemberSim** | Real pharmacy NPIs and locations |
| **PopulationSim** | Geographic correlation with demographics |
| **TrialSim** | Principal investigator lookups |

---

## Session History

| Session | Focus | Status |
|---------|-------|--------|
| Session 1 | Data Research | ✅ Complete |
| Session 2 | Setup Scripts & Data Load | ✅ Complete |
| Session 3 | Provider Skills | 🔲 Pending |
| Session 4 | Facility Skills | 🔲 Pending |
| Session 5 | Integration | 🔲 Pending |
| Session 6 | Documentation | 🔲 Pending |

## Current Database Stats

| Metric | Value |
|--------|-------|
| **Total Providers** | 8,937,975 |
| **Individuals** | 7,063,800 |
| **Organizations** | 1,874,175 |
| **Database Size** | 1,735 MB |
| **States Covered** | All 56 |

---

## Important Notes

1. **Data is LOCAL only** - Never commit NPPES/CMS data to git
2. **No PHI** - NPPES is public FOIA data, no patient information
3. **Independent from NetworkSim** - This is an experimental parallel implementation
4. **Update manually** - Download new NPPES monthly file as needed

---

## License

Data sources are public domain (CMS/FOIA). Setup scripts and skills are part of HealthSim.
