# NetworkSim-Local Developer Guide

**Version**: 0.1.0  
**Status**: Development

## Prerequisites

- Python 3.9+
- DuckDB (`pip install duckdb`)
- ~10 GB free disk space (for raw data processing)
- Internet connection (for initial data download)

## Quick Start

```bash
# 1. Navigate to NetworkSim-Local
cd skills/networksim-local

# 2. Install dependencies
pip install duckdb

# 3. Download NPPES data (manual - see below)

# 4. Build database
python setup/build-database.py

# 5. Verify
python -c "import duckdb; con = duckdb.connect('data/processed/networksim.duckdb'); print(con.execute('SELECT COUNT(*) FROM providers').fetchone())"
```

## Step-by-Step Setup

### Step 1: Download NPPES Data

1. Visit: https://download.cms.gov/nppes/NPI_Files.html

2. Download the **Monthly NPPES Downloadable File** (Version 1 or V2)
   - File name: `NPPES_Data_Dissemination_[Month]_[Year].zip`
   - Size: ~1 GB compressed

3. Extract the ZIP file

4. Move/copy the main data file to:
   ```
   skills/networksim-local/data/raw/nppes/npidata_pfile_YYYYMMDD-YYYYMMDD.csv
   ```

**Directory structure after download**:
```
data/
├── raw/
│   └── nppes/
│       ├── npidata_pfile_20050523-20241208.csv   # Main data (~9 GB)
│       ├── pl_pfile_20050523-20241208.csv        # Practice locations
│       ├── othername_pfile_20050523-20241208.csv # Other names
│       └── endpoint_pfile_20050523-20241208.csv  # Endpoints
└── processed/
    └── (database will be created here)
```

### Step 2: Build the Database

Run the build script:

```bash
python setup/build-database.py
```

**Expected output**:
```
NetworkSim-Local Database Builder
==================================================
Input:  /path/to/npidata_pfile_20050523-20241208.csv
Output: /path/to/data/processed/networksim.duckdb

Step 1: Reading NPPES CSV (this may take several minutes)...
   Loaded 7,012,345 active US providers

Step 2: Creating indexes...
   Created 6 indexes

Step 3: Creating views...
   Created provider_categories view

Step 4: Computing statistics...

   Provider Distribution:
     Physician (Allopathic): 1,234,567
     Nurse Practitioner: 456,789
     Pharmacy: 123,456
     ...

==================================================
Database built successfully!
  Records:  7,012,345
  Size:     198.4 MB
  Location: /path/to/data/processed/networksim.duckdb
```

**Build time**: 5-15 minutes depending on hardware.

### Step 3: Verify the Database

```python
import duckdb

con = duckdb.connect('data/processed/networksim.duckdb')

# Check record count
print(con.execute('SELECT COUNT(*) FROM providers').fetchone())
# Expected: (7000000+,)

# Sample query
print(con.execute('''
    SELECT npi, organization_name, practice_city, practice_state
    FROM providers
    WHERE entity_type_code = 2  -- Organizations
    AND practice_state = 'CA'
    LIMIT 5
''').fetchall())

con.close()
```

## Command Line Options

```bash
# Specify custom NPPES file
python setup/build-database.py --nppes-file /path/to/npidata.csv

# Specify custom output location
python setup/build-database.py --output /path/to/output.duckdb

# Quiet mode (minimal output)
python setup/build-database.py --quiet
```

## Database Schema

### Tables

**providers** - Main provider table (~7M records)
```sql
CREATE TABLE providers (
    npi VARCHAR(10) PRIMARY KEY,
    entity_type_code TINYINT,
    organization_name VARCHAR(200),
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    name_prefix VARCHAR(10),
    name_suffix VARCHAR(10),
    credential VARCHAR(50),
    gender_code CHAR(1),
    practice_address_1 VARCHAR(100),
    practice_address_2 VARCHAR(100),
    practice_city VARCHAR(50),
    practice_state CHAR(2),
    practice_zip VARCHAR(10),
    practice_country VARCHAR(2),
    practice_phone VARCHAR(20),
    practice_fax VARCHAR(20),
    taxonomy_code VARCHAR(15),
    license_number VARCHAR(30),
    license_state CHAR(2),
    is_primary_taxonomy VARCHAR(1),
    enumeration_date VARCHAR(10),
    last_update_date VARCHAR(10),
    deactivation_date VARCHAR(10),
    reactivation_date VARCHAR(10),
    is_sole_proprietor VARCHAR(1),
    is_subpart VARCHAR(1),
    auth_official_last_name VARCHAR(50),
    auth_official_first_name VARCHAR(50),
    auth_official_phone VARCHAR(20)
);
```

**load_metadata** - Database metadata
```sql
CREATE TABLE load_metadata (
    key VARCHAR PRIMARY KEY,
    value VARCHAR
);
```

### Views

**provider_categories** - Provider type classification
```sql
CREATE VIEW provider_categories AS
SELECT 
    npi,
    entity_type_code,
    organization_name,
    last_name,
    first_name,
    practice_state,
    practice_city,
    taxonomy_code,
    provider_category  -- Derived: 'Physician', 'Hospital', 'Pharmacy', etc.
FROM providers;
```

### Indexes

- `idx_npi` - Primary lookup
- `idx_state` - State-based queries
- `idx_zip` - ZIP code queries
- `idx_taxonomy` - Specialty queries
- `idx_city_state` - City/state combination
- `idx_entity_type` - Individual vs Organization

## Query Examples

### Python Usage

```python
import duckdb

def get_provider(npi: str) -> dict:
    """Look up a provider by NPI."""
    con = duckdb.connect('data/processed/networksim.duckdb', read_only=True)
    result = con.execute(
        'SELECT * FROM providers WHERE npi = ?', 
        [npi]
    ).fetchone()
    con.close()
    return result

def find_providers_by_state(state: str, limit: int = 100) -> list:
    """Find providers in a state."""
    con = duckdb.connect('data/processed/networksim.duckdb', read_only=True)
    results = con.execute(
        'SELECT * FROM providers WHERE practice_state = ? LIMIT ?',
        [state, limit]
    ).fetchall()
    con.close()
    return results

def find_pharmacies(zip_prefix: str) -> list:
    """Find pharmacies by ZIP prefix."""
    con = duckdb.connect('data/processed/networksim.duckdb', read_only=True)
    results = con.execute('''
        SELECT * FROM providers 
        WHERE taxonomy_code LIKE '3336%'
        AND practice_zip LIKE ?
    ''', [f'{zip_prefix}%']).fetchall()
    con.close()
    return results
```

### SQL Query Templates

See `queries/provider-queries.sql` for comprehensive query templates.

## Data Refresh

### Monthly Update Process

1. Download new NPPES monthly file
2. Extract to `data/raw/nppes/`
3. Run: `python setup/build-database.py`
4. Old database is automatically replaced

### Recommended Schedule

- **Frequency**: Monthly (first week)
- **Trigger**: New NPPES release notification
- **Duration**: ~15 minutes

## Troubleshooting

### "No NPPES file found"

Ensure the CSV file is in `data/raw/nppes/` and matches the pattern `npidata_pfile_*.csv`.

### Out of Memory

DuckDB processes large files efficiently, but if you have < 8GB RAM:
```bash
# Increase DuckDB memory limit
export DUCKDB_MEMORY_LIMIT=4GB
python setup/build-database.py
```

### Slow Build

- Ensure SSD storage (not HDD)
- Close other applications
- Expected time: 5-15 minutes on modern hardware

### Database Corruption

Delete and rebuild:
```bash
rm data/processed/networksim.duckdb
python setup/build-database.py
```

## Integration Notes

### MCP Server Usage

The DuckDB database can be queried via the `healthsim-duckdb` MCP server:

```python
# In conversation
"Query the NetworkSim-Local database: SELECT COUNT(*) FROM providers WHERE practice_state = 'TX'"
```

### Cross-Product Integration

When generating synthetic data in PatientSim/MemberSim:
1. Query NetworkSim-Local for real providers in target geography
2. Use real NPIs in synthetic encounters
3. Maintain referential integrity

## File Inventory

```
networksim-local/
├── README.md               # Product overview
├── SKILL.md                # Master skill definition
├── developer-guide.md      # This file
├── data-research.md        # Data source analysis
├── data/
│   ├── README.md           # Data directory documentation
│   ├── .gitignore          # Excludes data files
│   ├── raw/                # Downloaded source files (local)
│   └── processed/          # DuckDB database (local)
├── setup/
│   └── build-database.py   # ETL script
├── queries/
│   └── provider-queries.sql # SQL templates
└── skills/                 # (Future: detailed skill files)
```

---

*Part of the HealthSim Platform*
