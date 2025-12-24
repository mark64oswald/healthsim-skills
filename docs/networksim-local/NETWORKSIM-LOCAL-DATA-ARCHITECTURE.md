# NetworkSim-Local Data Architecture

**Version**: 0.1 (Planning)  
**Status**: Future - After NetworkSim Skills Complete  
**Last Updated**: 2024-12-24

---

## 1. Overview

This document defines the data architecture for NetworkSim-Local, the real-data infrastructure layer for healthcare provider, facility, and pharmacy information. The architecture follows the established PopulationSim-Local pattern using DuckDB for local storage.

---

## 2. Database Design

### 2.1 Database File Structure

```
mcp-servers/networksim-local/data/
├── networksim.duckdb           # Main database (all tables)
├── raw/                        # Source files (downloaded)
│   ├── nppes/
│   │   ├── NPPES_Data_Dissemination_January_2025.zip
│   │   └── npidata_pfile_20250106-20250112.csv
│   ├── cms/
│   │   ├── POS_OTHER_JAN25.csv
│   │   └── provider_of_services_current.csv
│   └── pharmacy/
│       └── pharmacy_directory_2025.csv
├── processed/                  # Cleaned/transformed (intermediate)
│   ├── providers_clean.parquet
│   ├── facilities_clean.parquet
│   └── pharmacies_clean.parquet
└── metadata/
    ├── load_log.json           # Data load history
    └── data_dictionary.md      # Field definitions
```

### 2.2 Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NETWORKSIM-LOCAL ERD                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐         ┌──────────────────┐                          │
│  │    providers     │         │ provider_locations│                          │
│  ├──────────────────┤         ├──────────────────┤                          │
│  │ npi (PK)         │────────►│ npi (FK)         │                          │
│  │ entity_type      │         │ location_type    │                          │
│  │ provider_name    │         │ address_line1    │                          │
│  │ credential       │         │ city             │                          │
│  │ gender           │         │ state            │                          │
│  │ taxonomy_1       │         │ zip              │                          │
│  │ taxonomy_2       │         │ county_fips      │──────┐                   │
│  │ taxonomy_3       │         │ zcta             │      │                   │
│  │ enumeration_date │         │ latitude         │      │                   │
│  │ last_update_date │         │ longitude        │      │                   │
│  │ deactivation_date│         └──────────────────┘      │                   │
│  │ source_file      │                                    │                   │
│  │ source_date      │                                    │                   │
│  └──────────────────┘                                    │                   │
│                                                          │                   │
│  ┌──────────────────┐         ┌──────────────────┐      │                   │
│  │    facilities    │         │ facility_locations│      │                   │
│  ├──────────────────┤         ├──────────────────┤      │                   │
│  │ ccn (PK)         │────────►│ ccn (FK)         │      │                   │
│  │ facility_type    │         │ address_line1    │      │                   │
│  │ facility_name    │         │ city             │      │                   │
│  │ ownership_type   │         │ state            │      │                   │
│  │ bed_count        │         │ zip              │      │                   │
│  │ medicare_status  │         │ county_fips      │──────┤                   │
│  │ accreditation    │         │ zcta             │      │                   │
│  │ source_file      │         │ latitude         │      │                   │
│  │ source_date      │         │ longitude        │      │                   │
│  └──────────────────┘         └──────────────────┘      │                   │
│                                                          │                   │
│  ┌──────────────────┐         ┌──────────────────┐      │                   │
│  │    pharmacies    │         │ pharmacy_locations│      │                   │
│  ├──────────────────┤         ├──────────────────┤      │  PopulationSim    │
│  │ ncpdp_id (PK)    │────────►│ ncpdp_id (FK)    │      │  ┌────────────┐   │
│  │ npi              │         │ address_line1    │      │  │  counties  │   │
│  │ pharmacy_name    │         │ city             │      │  ├────────────┤   │
│  │ pharmacy_type    │         │ state            │      └─►│ fips (PK)  │   │
│  │ chain_code       │         │ zip              │         │ county_name│   │
│  │ chain_name       │         │ county_fips      │─────────│ state_fips │   │
│  │ dispensing_class │         │ zcta             │         │ population │   │
│  │ specialty_flag   │         │ latitude         │         └────────────┘   │
│  │ mail_order_flag  │         │ longitude        │                          │
│  │ hours_of_operation│        └──────────────────┘                          │
│  │ source_file      │                                                       │
│  │ source_date      │                                                       │
│  └──────────────────┘                                                       │
│                                                                              │
│  ┌──────────────────┐         ┌──────────────────┐                          │
│  │  taxonomy_codes  │         │  specialty_mapping│                          │
│  ├──────────────────┤         ├──────────────────┤                          │
│  │ code (PK)        │────────►│ taxonomy_code    │                          │
│  │ classification   │         │ specialty_category│                          │
│  │ specialization   │         │ network_adequacy_ │                          │
│  │ definition       │         │   standard       │                          │
│  │ grouping         │         └──────────────────┘                          │
│  │ display_name     │                                                       │
│  └──────────────────┘                                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Table Specifications

### 3.1 Providers Table

**Source**: NPPES NPI Registry  
**Update Frequency**: Monthly  
**Estimated Rows**: ~3.3M (2.5M individual + 800K organization)

```sql
CREATE TABLE providers (
    -- Primary Key
    npi VARCHAR(10) PRIMARY KEY,
    
    -- Entity Type
    entity_type VARCHAR(1) NOT NULL,  -- '1' = Individual, '2' = Organization
    
    -- Name (Individual)
    provider_last_name VARCHAR(100),
    provider_first_name VARCHAR(50),
    provider_middle_name VARCHAR(50),
    provider_name_prefix VARCHAR(10),
    provider_name_suffix VARCHAR(10),
    provider_credential VARCHAR(50),
    
    -- Name (Organization)
    provider_organization_name VARCHAR(200),
    provider_other_organization_name VARCHAR(200),
    
    -- Demographics (Individual only)
    gender VARCHAR(1),  -- 'M', 'F', null for orgs
    
    -- Taxonomy/Specialty (up to 15 in NPPES, store top 3)
    taxonomy_code_1 VARCHAR(10),
    taxonomy_code_2 VARCHAR(10),
    taxonomy_code_3 VARCHAR(10),
    primary_taxonomy_switch_1 VARCHAR(1),  -- 'Y' if primary
    primary_taxonomy_switch_2 VARCHAR(1),
    primary_taxonomy_switch_3 VARCHAR(1),
    
    -- Status
    enumeration_date DATE,
    last_update_date DATE,
    npi_deactivation_date DATE,
    npi_reactivation_date DATE,
    deactivation_reason_code VARCHAR(2),
    
    -- Provider Details
    sole_proprietor VARCHAR(1),  -- 'X' = Yes, blank = No
    is_organization_subpart VARCHAR(1),
    parent_organization_lbn VARCHAR(200),
    parent_organization_tin VARCHAR(9),
    
    -- Authorized Official (Organizations)
    authorized_official_last_name VARCHAR(100),
    authorized_official_first_name VARCHAR(50),
    authorized_official_title VARCHAR(50),
    authorized_official_telephone VARCHAR(20),
    
    -- Other Identifiers (Medicare, Medicaid, etc.)
    -- Store as JSON for flexibility
    other_identifiers JSON,
    
    -- Metadata
    source_file VARCHAR(100) NOT NULL,
    source_date DATE NOT NULL,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_row_number INTEGER
);

-- Indexes
CREATE INDEX idx_providers_entity_type ON providers(entity_type);
CREATE INDEX idx_providers_taxonomy_1 ON providers(taxonomy_code_1);
CREATE INDEX idx_providers_last_name ON providers(provider_last_name);
CREATE INDEX idx_providers_org_name ON providers(provider_organization_name);
CREATE INDEX idx_providers_deactivation ON providers(npi_deactivation_date);
```

### 3.2 Provider Locations Table

**Source**: NPPES NPI Registry (address fields)  
**Update Frequency**: Monthly  
**Estimated Rows**: ~6.6M (2 addresses per provider typical)

```sql
CREATE TABLE provider_locations (
    -- Composite Key
    npi VARCHAR(10) NOT NULL,
    location_type VARCHAR(20) NOT NULL,  -- 'practice_1', 'practice_2', 'mailing'
    
    -- Address
    address_line_1 VARCHAR(100),
    address_line_2 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip VARCHAR(10),  -- 5 or 9 digit
    country_code VARCHAR(2) DEFAULT 'US',
    
    -- Phone/Fax
    telephone VARCHAR(20),
    fax VARCHAR(20),
    
    -- Geocoding (populated post-load)
    county_fips VARCHAR(5),
    zcta VARCHAR(5),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    geocode_quality VARCHAR(20),  -- 'exact', 'zip_centroid', 'city_centroid'
    
    -- Metadata
    source_file VARCHAR(100),
    source_date DATE,
    geocode_date DATE,
    
    PRIMARY KEY (npi, location_type),
    FOREIGN KEY (npi) REFERENCES providers(npi)
);

-- Indexes
CREATE INDEX idx_provider_loc_state ON provider_locations(state);
CREATE INDEX idx_provider_loc_zip ON provider_locations(zip);
CREATE INDEX idx_provider_loc_county ON provider_locations(county_fips);
CREATE INDEX idx_provider_loc_zcta ON provider_locations(zcta);
```

### 3.3 Facilities Table

**Source**: CMS Provider of Services (POS) file  
**Update Frequency**: Annual (quarterly updates available)  
**Estimated Rows**: ~50K

```sql
CREATE TABLE facilities (
    -- Primary Key
    ccn VARCHAR(10) PRIMARY KEY,  -- CMS Certification Number
    
    -- NPI (if available)
    npi VARCHAR(10),
    
    -- Basic Info
    facility_name VARCHAR(200) NOT NULL,
    doing_business_as VARCHAR(200),
    
    -- Classification
    facility_type VARCHAR(50) NOT NULL,  -- Standardized type
    facility_type_code VARCHAR(10),       -- CMS code
    subtype VARCHAR(50),
    
    -- Characteristics
    bed_count INTEGER,
    bed_count_certified INTEGER,
    operating_status VARCHAR(20),
    
    -- Ownership
    ownership_type VARCHAR(50),  -- 'Non-Profit', 'For-Profit', 'Government'
    ownership_subtype VARCHAR(50),
    chain_affiliation VARCHAR(200),
    
    -- Certification
    medicare_provider_type VARCHAR(50),
    medicaid_provider_type VARCHAR(50),
    accreditation_type VARCHAR(50),  -- 'TJC', 'DNV', 'HFAP', 'State'
    certification_date DATE,
    
    -- Contact
    administrator_name VARCHAR(100),
    telephone VARCHAR(20),
    
    -- Metadata
    source_file VARCHAR(100) NOT NULL,
    source_date DATE NOT NULL,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_facilities_type ON facilities(facility_type);
CREATE INDEX idx_facilities_npi ON facilities(npi);
CREATE INDEX idx_facilities_ownership ON facilities(ownership_type);
CREATE INDEX idx_facilities_beds ON facilities(bed_count);
```

### 3.4 Facility Locations Table

**Source**: CMS Provider of Services  
**Update Frequency**: Annual  
**Estimated Rows**: ~50K (1:1 with facilities typically)

```sql
CREATE TABLE facility_locations (
    -- Primary Key
    ccn VARCHAR(10) PRIMARY KEY,
    
    -- Address
    address_line_1 VARCHAR(100),
    address_line_2 VARCHAR(100),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip VARCHAR(10) NOT NULL,
    
    -- Geocoding
    county_fips VARCHAR(5),
    zcta VARCHAR(5),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    geocode_quality VARCHAR(20),
    
    -- Region (CMS)
    cms_region VARCHAR(2),
    
    -- Rural/Urban
    cbsa_code VARCHAR(5),
    rural_urban_status VARCHAR(20),  -- 'Urban', 'Rural', 'Super-Rural'
    
    -- Metadata
    source_file VARCHAR(100),
    source_date DATE,
    geocode_date DATE,
    
    FOREIGN KEY (ccn) REFERENCES facilities(ccn)
);

-- Indexes
CREATE INDEX idx_facility_loc_state ON facility_locations(state);
CREATE INDEX idx_facility_loc_county ON facility_locations(county_fips);
CREATE INDEX idx_facility_loc_rural ON facility_locations(rural_urban_status);
```

### 3.5 Pharmacies Table

**Source**: TBD (NCPDP, state boards, or commercial)  
**Update Frequency**: Quarterly  
**Estimated Rows**: ~65K

```sql
CREATE TABLE pharmacies (
    -- Primary Key
    ncpdp_id VARCHAR(10) PRIMARY KEY,
    
    -- NPI (if available)
    npi VARCHAR(10),
    
    -- Basic Info
    pharmacy_name VARCHAR(200) NOT NULL,
    doing_business_as VARCHAR(200),
    
    -- Classification
    pharmacy_type VARCHAR(50) NOT NULL,  -- 'Retail', 'Mail Order', 'Specialty', 'Compounding'
    dispensing_class VARCHAR(50),         -- 'Community', 'Institutional', 'Long-Term Care'
    
    -- Chain Info
    chain_code VARCHAR(10),
    chain_name VARCHAR(100),
    store_number VARCHAR(20),
    
    -- Specialty Indicators
    specialty_pharmacy_flag BOOLEAN DEFAULT FALSE,
    limited_distribution_flag BOOLEAN DEFAULT FALSE,
    mail_order_flag BOOLEAN DEFAULT FALSE,
    compounding_flag BOOLEAN DEFAULT FALSE,
    
    -- Services
    offers_delivery BOOLEAN,
    offers_immunizations BOOLEAN,
    offers_mtm BOOLEAN,  -- Medication Therapy Management
    language_capabilities VARCHAR(200),  -- Comma-separated
    
    -- Hours (as JSON for flexibility)
    hours_of_operation JSON,
    
    -- DEA (if available and legal to store)
    dea_number VARCHAR(9),
    
    -- Status
    active_status BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    source_file VARCHAR(100) NOT NULL,
    source_date DATE NOT NULL,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_pharmacies_npi ON pharmacies(npi);
CREATE INDEX idx_pharmacies_type ON pharmacies(pharmacy_type);
CREATE INDEX idx_pharmacies_chain ON pharmacies(chain_code);
CREATE INDEX idx_pharmacies_specialty ON pharmacies(specialty_pharmacy_flag);
CREATE INDEX idx_pharmacies_mail ON pharmacies(mail_order_flag);
```

### 3.6 Pharmacy Locations Table

```sql
CREATE TABLE pharmacy_locations (
    -- Primary Key
    ncpdp_id VARCHAR(10) PRIMARY KEY,
    
    -- Address
    address_line_1 VARCHAR(100),
    address_line_2 VARCHAR(100),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip VARCHAR(10) NOT NULL,
    
    -- Contact
    telephone VARCHAR(20),
    fax VARCHAR(20),
    
    -- Geocoding
    county_fips VARCHAR(5),
    zcta VARCHAR(5),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    geocode_quality VARCHAR(20),
    
    -- Metadata
    source_file VARCHAR(100),
    source_date DATE,
    geocode_date DATE,
    
    FOREIGN KEY (ncpdp_id) REFERENCES pharmacies(ncpdp_id)
);

-- Indexes
CREATE INDEX idx_pharmacy_loc_state ON pharmacy_locations(state);
CREATE INDEX idx_pharmacy_loc_county ON pharmacy_locations(county_fips);
CREATE INDEX idx_pharmacy_loc_zip ON pharmacy_locations(zip);
```

### 3.7 Reference Tables

#### Taxonomy Codes (NUCC)

```sql
CREATE TABLE taxonomy_codes (
    code VARCHAR(10) PRIMARY KEY,
    grouping VARCHAR(100),
    classification VARCHAR(100),
    specialization VARCHAR(100),
    definition TEXT,
    notes TEXT,
    display_name VARCHAR(200),
    
    -- Metadata
    effective_date DATE,
    deactivation_date DATE,
    source_version VARCHAR(20)
);

-- Mapping to network adequacy categories
CREATE TABLE specialty_mapping (
    taxonomy_code VARCHAR(10),
    specialty_category VARCHAR(50),      -- 'Primary Care', 'Cardiology', etc.
    specialty_subcategory VARCHAR(50),
    network_adequacy_standard VARCHAR(20),  -- Links to adequacy rules
    
    PRIMARY KEY (taxonomy_code, specialty_category),
    FOREIGN KEY (taxonomy_code) REFERENCES taxonomy_codes(code)
);
```

#### Facility Type Reference

```sql
CREATE TABLE facility_type_reference (
    facility_type_code VARCHAR(10) PRIMARY KEY,
    facility_type VARCHAR(50),
    description TEXT,
    cms_category VARCHAR(50),
    
    -- Network adequacy linkage
    adequacy_category VARCHAR(50),
    time_distance_standard_urban INTEGER,   -- minutes
    time_distance_standard_rural INTEGER
);
```

---

## 4. Data Transformations

### 4.1 NPPES Load Pipeline

```
NPPES Raw File (CSV, ~8GB)
         │
         ▼
┌─────────────────────────────┐
│ 1. Parse & Validate         │
│    - Check NPI format       │
│    - Validate state codes   │
│    - Handle encoding issues │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ 2. Filter                   │
│    - Active NPIs only       │
│    - US addresses only      │
│    - Exclude deactivated    │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ 3. Normalize                │
│    - Split to providers +   │
│      provider_locations     │
│    - Standardize taxonomy   │
│    - Clean phone numbers    │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ 4. Geocode                  │
│    - Batch to Census API    │
│    - Add county_fips, zcta  │
│    - Calculate lat/long     │
└─────────────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ 5. Load to DuckDB           │
│    - Upsert strategy        │
│    - Update metadata        │
│    - Rebuild indexes        │
└─────────────────────────────┘
```

### 4.2 Field Mappings: NPPES → Providers

| NPPES Column | Provider Column | Transformation |
|--------------|-----------------|----------------|
| NPI | npi | Direct |
| Entity Type Code | entity_type | Direct |
| Provider Last Name (Legal Name) | provider_last_name | Trim, uppercase |
| Provider First Name | provider_first_name | Trim, uppercase |
| Provider Credential Text | provider_credential | Parse, standardize |
| Provider Gender Code | gender | Direct |
| Healthcare Provider Taxonomy Code_1 | taxonomy_code_1 | Direct |
| Provider Enumeration Date | enumeration_date | Parse date |
| Last Update Date | last_update_date | Parse date |
| NPI Deactivation Date | npi_deactivation_date | Parse date |

---

## 5. PopulationSim Integration

### 5.1 Attach Pattern

```sql
-- In DuckDB, attach PopulationSim database
ATTACH '/path/to/populationsim.duckdb' AS pop (READ_ONLY);

-- Now can join across databases
SELECT 
    p.npi,
    p.provider_last_name,
    p.taxonomy_code_1,
    pl.county_fips,
    c.county_name,
    c.total_population,
    h.primary_care_physicians_rate
FROM providers p
JOIN provider_locations pl ON p.npi = pl.npi
JOIN pop.counties c ON pl.county_fips = c.fips
LEFT JOIN pop.health_indicators h ON c.fips = h.fips
WHERE p.taxonomy_code_1 LIKE '208D%';  -- General Practice
```

### 5.2 Provider Access Analysis

```sql
-- Calculate provider density by county
WITH provider_counts AS (
    SELECT 
        pl.county_fips,
        sm.specialty_category,
        COUNT(DISTINCT p.npi) as provider_count
    FROM providers p
    JOIN provider_locations pl ON p.npi = pl.npi
    JOIN specialty_mapping sm ON p.taxonomy_code_1 = sm.taxonomy_code
    WHERE p.npi_deactivation_date IS NULL
    GROUP BY pl.county_fips, sm.specialty_category
)
SELECT 
    pc.county_fips,
    c.county_name,
    c.total_population,
    pc.specialty_category,
    pc.provider_count,
    (pc.provider_count * 100000.0 / c.total_population) as providers_per_100k
FROM provider_counts pc
JOIN pop.counties c ON pc.county_fips = c.fips
ORDER BY providers_per_100k ASC;  -- Find underserved areas
```

---

## 6. MCP Tool Design

### 6.1 Provider Lookup Tool

```typescript
interface ProviderLookupInput {
  npi?: string;                    // Exact NPI lookup
  name?: string;                   // Partial name match
  specialty?: string;              // Specialty category or taxonomy
  state?: string;                  // 2-letter state code
  county_fips?: string;            // 5-digit FIPS
  zip?: string;                    // ZIP code
  city?: string;                   // City name
  include_inactive?: boolean;      // Include deactivated NPIs
  limit?: number;                  // Max results (default 100)
}

interface ProviderLookupOutput {
  providers: Provider[];
  total_count: number;
  query_metadata: {
    filters_applied: string[];
    data_vintage: string;
  };
}
```

### 6.2 Facility Lookup Tool

```typescript
interface FacilityLookupInput {
  ccn?: string;                    // Exact CCN lookup
  npi?: string;                    // Facility NPI
  name?: string;                   // Partial name match
  facility_type?: string;          // 'Hospital', 'SNF', 'ASC', etc.
  state?: string;
  county_fips?: string;
  min_beds?: number;
  max_beds?: number;
  ownership_type?: string;         // 'Non-Profit', 'For-Profit', 'Government'
  limit?: number;
}
```

### 6.3 Pharmacy Lookup Tool

```typescript
interface PharmacyLookupInput {
  ncpdp_id?: string;               // Exact NCPDP lookup
  npi?: string;                    // Pharmacy NPI
  name?: string;                   // Partial name match
  pharmacy_type?: string;          // 'Retail', 'Specialty', 'Mail Order'
  chain_name?: string;             // Chain affiliation
  state?: string;
  county_fips?: string;
  zip?: string;
  specialty_only?: boolean;        // Only specialty pharmacies
  limit?: number;
}
```

### 6.4 Network Builder Tool

```typescript
interface NetworkBuilderInput {
  geography: {
    states?: string[];
    counties?: string[];
    zips?: string[];
    radius_miles?: number;
    center_zip?: string;
  };
  specialties: string[];           // Required specialties
  facility_types?: string[];       // Required facility types
  include_pharmacies?: boolean;
  network_type?: string;           // 'HMO', 'PPO' (affects adequacy rules)
  validate_adequacy?: boolean;     // Check against standards
}

interface NetworkBuilderOutput {
  network: {
    providers: Provider[];
    facilities: Facility[];
    pharmacies: Pharmacy[];
  };
  adequacy_report?: {
    specialty: string;
    required: number;
    actual: number;
    meets_standard: boolean;
  }[];
  summary: {
    total_providers: number;
    total_facilities: number;
    total_pharmacies: number;
    coverage_area: string;
  };
}
```

---

## 7. Data Quality Framework

### 7.1 Validation Rules

```sql
-- NPI Check Digit Validation
CREATE OR REPLACE FUNCTION validate_npi(npi VARCHAR) RETURNS BOOLEAN AS $$
    -- Luhn algorithm for NPI validation
    -- Returns TRUE if valid, FALSE if invalid
$$;

-- Apply to all loads
SELECT npi, validate_npi(npi) as is_valid
FROM providers
WHERE NOT validate_npi(npi);
```

### 7.2 Completeness Tracking

```sql
CREATE TABLE data_quality_metrics (
    table_name VARCHAR(50),
    field_name VARCHAR(50),
    metric_date DATE,
    total_rows INTEGER,
    null_count INTEGER,
    completeness_pct DECIMAL(5,2),
    
    PRIMARY KEY (table_name, field_name, metric_date)
);

-- Populate after each load
INSERT INTO data_quality_metrics
SELECT 
    'providers' as table_name,
    'taxonomy_code_1' as field_name,
    CURRENT_DATE as metric_date,
    COUNT(*) as total_rows,
    COUNT(*) FILTER (WHERE taxonomy_code_1 IS NULL) as null_count,
    100.0 * COUNT(*) FILTER (WHERE taxonomy_code_1 IS NOT NULL) / COUNT(*) as completeness_pct
FROM providers;
```

---

## 8. Performance Considerations

### 8.1 Expected Query Patterns

| Query Type | Expected Frequency | Target Latency |
|------------|-------------------|----------------|
| Single NPI lookup | High | < 50ms |
| Name search | Medium | < 200ms |
| State + specialty | High | < 500ms |
| County + specialty | Medium | < 300ms |
| Network adequacy calc | Low | < 5s |
| Full table aggregation | Low | < 30s |

### 8.2 Indexing Strategy

**Primary indexes** (on table creation):
- All primary keys
- Foreign keys

**Secondary indexes** (for query performance):
- providers: taxonomy_code_1, entity_type, state (via locations)
- provider_locations: state, county_fips, zip
- facilities: facility_type, state (via locations)
- pharmacies: pharmacy_type, chain_code, state (via locations)

### 8.3 Estimated Database Size

| Table | Rows | Avg Row Size | Table Size |
|-------|------|--------------|------------|
| providers | 3.3M | 500 bytes | 1.6 GB |
| provider_locations | 6.6M | 200 bytes | 1.3 GB |
| facilities | 50K | 400 bytes | 20 MB |
| facility_locations | 50K | 200 bytes | 10 MB |
| pharmacies | 65K | 350 bytes | 23 MB |
| pharmacy_locations | 65K | 200 bytes | 13 MB |
| taxonomy_codes | 1K | 500 bytes | 500 KB |
| **Total** | | | **~3 GB** |

---

## 9. Related Documents

- [NetworkSim-Local Project Requirements](NETWORKSIM-LOCAL-PROJECT-REQUIREMENTS.md)
- [NetworkSim-Local Implementation Plan](NETWORKSIM-LOCAL-IMPLEMENTATION-PLAN.md)
- [NetworkSim-Local Data Sources](NETWORKSIM-LOCAL-DATA-SOURCES.md)
- [PopulationSim Data Architecture](../populationsim/POPULATIONSIM-DATA-ARCHITECTURE.md)

---

*Document Status: Planning - Schema subject to refinement during implementation*
