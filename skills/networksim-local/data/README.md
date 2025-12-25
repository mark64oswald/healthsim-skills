# NetworkSim-Local Data Directory

**IMPORTANT**: This directory contains LOCAL data files that are NOT committed to Git.

## Directory Structure

```
data/
├── README.md          # This file (committed)
├── .gitignore         # Excludes data files (committed)
├── raw/               # Downloaded source files (local only)
│   ├── nppes/         # NPPES NPI Registry files
│   └── pos/           # Provider of Services files
└── processed/         # DuckDB database (local only)
    └── networksim.duckdb
```

## Data Sources

### NPPES NPI Registry

| Attribute | Value |
|-----------|-------|
| URL | https://download.cms.gov/nppes/NPI_Files.html |
| File | `NPPES_Data_Dissemination_[Month]_[Year].zip` |
| Size | ~1 GB compressed, ~9 GB uncompressed |
| Update | Monthly (full replacement) |

**Download Steps**:
1. Visit https://download.cms.gov/nppes/NPI_Files.html
2. Download "NPPES Data Dissemination" (Version 1 or V2)
3. Extract to `data/raw/nppes/`
4. Run `setup/build-database.py`

### Provider of Services (POS)

| Attribute | Value |
|-----------|-------|
| URL | https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities |
| File | Provider of Services File - Hospital & Non-Hospital Facilities |
| Size | ~50 MB |
| Update | Quarterly |

**Download Steps**:
1. Visit the CMS data portal
2. Search for "Provider of Services File"
3. Download CSV export
4. Save to `data/raw/pos/`

## Building the Database

```bash
cd skills/networksim-local
python setup/build-database.py
```

This will:
1. Read raw NPPES CSV files
2. Apply filters (active providers, US only)
3. Select relevant columns
4. Create DuckDB database at `data/processed/networksim.duckdb`

## Estimated Sizes

| File | Raw Size | Processed Size |
|------|----------|----------------|
| NPPES CSV | ~9 GB | N/A |
| DuckDB (providers) | N/A | ~200 MB |
| POS CSV | ~50 MB | N/A |
| DuckDB (facilities) | N/A | ~10 MB |
| **Total** | ~9 GB | **~210 MB** |

## Refresh Schedule

- **NPPES**: Monthly (first week of each month)
- **POS**: Quarterly

## Data Not Included

The following data sources were evaluated but NOT included:

- **NCPDP Pharmacy Database**: Proprietary, requires paid subscription
  - Pharmacies with NPIs are available in NPPES as alternative

---

*Last Updated: 2024-12-24*
