# NetworkSim-Local Data Research

**Session**: 1 - Data Research  
**Date**: 2024-12-24  
**Status**: Complete

## Executive Summary

This document analyzes the available public data sources for NetworkSim-Local and proposes a filtering strategy to create a manageable local database while maintaining comprehensive coverage for HealthSim use cases.

---

## 1. NPPES NPI Registry Analysis

### 1.1 Source Information

| Attribute | Value |
|-----------|-------|
| **URL** | https://download.cms.gov/nppes/NPI_Files.html |
| **Provider** | Centers for Medicare & Medicaid Services (CMS) |
| **Format** | CSV (comma-separated, quoted fields) |
| **Compressed Size** | ~1,048 MB (ZIP) |
| **Uncompressed Size** | ~9.3 GB |
| **Record Count** | ~8.6 million NPIs |
| **Update Frequency** | Monthly (full), Weekly (incremental) |
| **Cost** | Free (FOIA-disclosable) |

### 1.2 File Structure

The NPPES download ZIP contains:

```
NPPES_Data_Dissemination_[date].zip
├── npidata_pfile_[daterange].csv          # Main provider data (~9GB)
├── pl_pfile_[daterange].csv               # Practice Location Reference
├── othername_pfile_[daterange].csv        # Other Names Reference  
├── endpoint_pfile_[daterange].csv         # Endpoint Reference
├── NPPES_Data_Dissemination_Readme.pdf    # Documentation
├── NPPES_Data_Dissemination_CodeValues.pdf # Code definitions
└── npidata_pfile_[daterange]_FileHeader.csv # Column headers
```

### 1.3 Key Fields (Main Data File)

The main CSV has **330 columns** due to repeating groups. Critical fields:

| Field | Description | Example |
|-------|-------------|---------|
| `NPI` | 10-digit identifier | 1234567890 |
| `Entity Type Code` | 1=Individual, 2=Organization | 1 |
| `Provider Organization Name` | Org name (Type 2) | "Memorial Hospital" |
| `Provider Last Name` | Individual name (Type 1) | "Smith" |
| `Provider First Name` | Individual name (Type 1) | "John" |
| `Provider Credential Text` | Credentials | "MD, FACP" |
| `Provider Business Practice Location Address` | Street address | "123 Main St" |
| `Provider Business Practice Location Address City Name` | City | "Boston" |
| `Provider Business Practice Location Address State Name` | State | "MA" |
| `Provider Business Practice Location Address Postal Code` | ZIP | "02101" |
| `Healthcare Provider Taxonomy Code_1` | Primary specialty | "207R00000X" |
| `Healthcare Provider Primary Taxonomy Switch_1` | Primary flag | "Y" |
| `NPI Deactivation Date` | If deactivated | "05/15/2023" |
| `NPI Reactivation Date` | If reactivated | "" |

### 1.4 Taxonomy Codes

Provider specialties are encoded using the Healthcare Provider Taxonomy Code System (NUCC):

| Code | Description | Category |
|------|-------------|----------|
| 207R00000X | Internal Medicine | Allopathic Physicians |
| 207RC0000X | Cardiovascular Disease | Allopathic Physicians |
| 208D00000X | General Practice | Allopathic Physicians |
| 363L00000X | Nurse Practitioner | Nursing Service Providers |
| 332B00000X | Durable Medical Equipment | Suppliers |
| 3336C0003X | Community/Retail Pharmacy | Pharmacy |
| 282N00000X | General Acute Care Hospital | Hospitals |
| 261QM0801X | Mental Health Clinic | Clinics |

**Full taxonomy list**: https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40

### 1.5 Entity Type Distribution (Approximate)

| Entity Type | Count | Percentage |
|-------------|-------|------------|
| Type 1 (Individual) | ~7.2 million | 84% |
| Type 2 (Organization) | ~1.4 million | 16% |
| Deactivated | ~1.5 million | 17% |
| Active | ~7.1 million | 83% |

---

## 2. CMS Provider of Services (POS) File

### 2.1 Source Information

| Attribute | Value |
|-----------|-------|
| **URL** | https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities |
| **Provider** | CMS |
| **Format** | CSV |
| **Size** | ~50 MB |
| **Update Frequency** | Quarterly |
| **Cost** | Free |

### 2.2 Key Fields

| Field | Description |
|-------|-------------|
| `CCN` | CMS Certification Number (6-digit) |
| `PRVDR_NUM` | Provider Number |
| `FAC_NAME` | Facility Name |
| `CRTFD_BED_CNT` | Certified Bed Count |
| `GNRL_CNTL_TYPE_CD` | Ownership Type |
| `RSDNT_CNT` | Resident Count (teaching) |
| `STATE_CD` | State Code |
| `CITY_NAME` | City |
| `ZIP_CD` | ZIP Code |

### 2.3 Facility Types Included

- Short Term Acute Care Hospitals
- Critical Access Hospitals
- Long Term Care Hospitals
- Psychiatric Hospitals
- Rehabilitation Hospitals
- Skilled Nursing Facilities
- Home Health Agencies
- Hospice
- Ambulatory Surgical Centers

---

## 3. NCPDP Pharmacy Data - NOT AVAILABLE

**Important Finding**: The NCPDP dataQ pharmacy database is **proprietary** and requires a paid subscription. This is NOT a free public data source.

**Alternative**: Pharmacies with NPIs are included in the NPPES registry. We can filter by pharmacy taxonomy codes:

| Taxonomy Code | Description |
|---------------|-------------|
| 3336C0002X | Compounding Pharmacy |
| 3336C0003X | Community/Retail Pharmacy |
| 3336C0004X | Mail Order Pharmacy |
| 3336H0001X | Home Infusion Therapy Pharmacy |
| 3336I0012X | Institutional Pharmacy |
| 3336L0003X | Long Term Care Pharmacy |
| 3336M0002X | Nuclear Pharmacy |
| 3336N0007X | Non-Pharmacy Dispensing Site |
| 3336S0011X | Specialty Pharmacy |

---

## 4. Filtering Strategy

### 4.1 Goals

1. **Manageable Size**: Target < 500 MB for local database
2. **Comprehensive Coverage**: All active providers in key categories
3. **Geographic Flexibility**: All US states/territories
4. **Use Case Support**: Enable realistic provider lookups for all HealthSim products

### 4.2 Proposed Filters

#### Filter 1: Active Providers Only
- Exclude records where `NPI Deactivation Date` is populated AND `NPI Reactivation Date` is empty
- **Estimated reduction**: 17% → ~7.1 million records

#### Filter 2: US Locations Only
- Include only records with valid US state codes
- Exclude foreign addresses
- **Estimated reduction**: ~1% → ~7.0 million records

#### Filter 3: Column Selection
- Keep only essential columns (reduce from 330 to ~40)
- Drop repeating groups beyond first taxonomy
- **Estimated reduction**: 88% of file width

### 4.3 Column Selection

**Core Identity (10 columns)**:
- NPI
- Entity_Type_Code
- Provider_Organization_Name
- Provider_Last_Name
- Provider_First_Name
- Provider_Middle_Name
- Provider_Credential_Text
- Provider_Gender_Code
- Provider_Enumeration_Date
- Last_Update_Date

**Practice Location (10 columns)**:
- Provider_First_Line_Business_Practice_Location_Address
- Provider_Second_Line_Business_Practice_Location_Address
- Provider_Business_Practice_Location_Address_City_Name
- Provider_Business_Practice_Location_Address_State_Name
- Provider_Business_Practice_Location_Address_Postal_Code
- Provider_Business_Practice_Location_Address_Country_Code
- Provider_Business_Practice_Location_Address_Telephone_Number
- Provider_Business_Practice_Location_Address_Fax_Number

**Specialty (6 columns)**:
- Healthcare_Provider_Taxonomy_Code_1
- Provider_License_Number_1
- Provider_License_Number_State_Code_1
- Healthcare_Provider_Primary_Taxonomy_Switch_1
- Healthcare_Provider_Taxonomy_Group_1

**Organization Details (5 columns)**:
- Authorized_Official_Last_Name
- Authorized_Official_First_Name
- Authorized_Official_Telephone_Number
- Is_Sole_Proprietor
- Is_Organization_Subpart

### 4.4 Estimated Final Size

| Stage | Records | Columns | Est. Size |
|-------|---------|---------|-----------|
| Raw NPPES | 8.6M | 330 | 9.3 GB |
| Active Only | 7.1M | 330 | 7.7 GB |
| US Only | 7.0M | 330 | 7.6 GB |
| Selected Columns | 7.0M | 40 | ~1.0 GB |
| **DuckDB (compressed)** | 7.0M | 40 | **~200 MB** |

---

## 5. DuckDB Schema Design

### 5.1 Core Tables

```sql
-- Provider table (flattened, denormalized for query speed)
CREATE TABLE providers (
    npi VARCHAR(10) PRIMARY KEY,
    entity_type_code TINYINT,  -- 1=Individual, 2=Organization
    
    -- Names
    organization_name VARCHAR(200),
    last_name VARCHAR(50),
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    credential VARCHAR(50),
    gender_code CHAR(1),
    
    -- Primary Practice Location
    practice_address_1 VARCHAR(100),
    practice_address_2 VARCHAR(100),
    practice_city VARCHAR(50),
    practice_state CHAR(2),
    practice_zip VARCHAR(10),
    practice_phone VARCHAR(20),
    practice_fax VARCHAR(20),
    
    -- Primary Taxonomy
    taxonomy_code VARCHAR(15),
    taxonomy_description VARCHAR(200),
    license_number VARCHAR(30),
    license_state CHAR(2),
    
    -- Metadata
    enumeration_date DATE,
    last_update_date DATE,
    is_sole_proprietor BOOLEAN,
    is_subpart BOOLEAN
);

-- Taxonomy reference table
CREATE TABLE taxonomy_codes (
    code VARCHAR(15) PRIMARY KEY,
    classification VARCHAR(100),
    specialization VARCHAR(100),
    description VARCHAR(200),
    category VARCHAR(50)  -- Physician, Hospital, Pharmacy, etc.
);

-- Geographic index for fast location queries
CREATE INDEX idx_providers_state ON providers(practice_state);
CREATE INDEX idx_providers_zip ON providers(practice_zip);
CREATE INDEX idx_providers_taxonomy ON providers(taxonomy_code);
CREATE INDEX idx_providers_city_state ON providers(practice_city, practice_state);
```

### 5.2 Supplementary Tables

```sql
-- Facilities from POS file (hospitals, SNFs, etc.)
CREATE TABLE facilities (
    ccn VARCHAR(10) PRIMARY KEY,
    npi VARCHAR(10),  -- Link to providers table
    facility_name VARCHAR(200),
    facility_type VARCHAR(50),
    bed_count INTEGER,
    ownership_type VARCHAR(50),
    teaching_status BOOLEAN,
    address VARCHAR(100),
    city VARCHAR(50),
    state CHAR(2),
    zip VARCHAR(10),
    FOREIGN KEY (npi) REFERENCES providers(npi)
);

-- Provider category view for easy querying
CREATE VIEW provider_categories AS
SELECT 
    npi,
    CASE 
        WHEN taxonomy_code LIKE '207%' THEN 'Physician'
        WHEN taxonomy_code LIKE '208%' THEN 'Physician'
        WHEN taxonomy_code LIKE '363%' THEN 'Nurse Practitioner'
        WHEN taxonomy_code LIKE '364%' THEN 'Physician Assistant'
        WHEN taxonomy_code LIKE '3336%' THEN 'Pharmacy'
        WHEN taxonomy_code LIKE '282%' THEN 'Hospital'
        WHEN taxonomy_code LIKE '261%' THEN 'Clinic'
        WHEN taxonomy_code LIKE '332%' THEN 'DME Supplier'
        ELSE 'Other'
    END as category,
    taxonomy_code,
    taxonomy_description
FROM providers;
```

---

## 6. Query Patterns

### 6.1 Provider Lookup by NPI
```sql
SELECT * FROM providers WHERE npi = '1234567890';
```

### 6.2 Providers by Geography
```sql
-- By state
SELECT * FROM providers WHERE practice_state = 'CA' LIMIT 100;

-- By ZIP (prefix match for area)
SELECT * FROM providers WHERE practice_zip LIKE '902%';

-- By city/state
SELECT * FROM providers 
WHERE practice_city = 'Los Angeles' AND practice_state = 'CA';
```

### 6.3 Providers by Specialty
```sql
-- Cardiologists in Texas
SELECT * FROM providers 
WHERE taxonomy_code = '207RC0000X' AND practice_state = 'TX';

-- All pharmacies in a ZIP code
SELECT * FROM providers 
WHERE taxonomy_code LIKE '3336%' AND practice_zip LIKE '10001%';
```

### 6.4 Geographic Distribution
```sql
-- Provider count by state
SELECT practice_state, COUNT(*) as provider_count
FROM providers
GROUP BY practice_state
ORDER BY provider_count DESC;

-- Specialty distribution in a region
SELECT taxonomy_description, COUNT(*) as count
FROM providers
WHERE practice_state IN ('CA', 'OR', 'WA')
GROUP BY taxonomy_description
ORDER BY count DESC
LIMIT 20;
```

---

## 7. Data Update Strategy

### 7.1 Initial Load
1. Download latest monthly NPPES file
2. Download latest quarterly POS file
3. Run ETL pipeline to create DuckDB database
4. Verify record counts and data quality

### 7.2 Refresh Cycle
- **Recommended**: Monthly (aligned with NPPES releases)
- **Process**: Full replacement (simpler than incremental)
- **Automation**: Python script with date-based file naming

### 7.3 Version Tracking
```
data/processed/
├── nppes_2024_12.duckdb      # Current
├── nppes_2024_11.duckdb      # Previous (backup)
└── metadata.json              # Load dates, record counts
```

---

## 8. Next Steps (Session 2)

1. Create download automation scripts
2. Implement filtering and column selection
3. Build DuckDB database
4. Verify data quality
5. Create initial query templates

---

## Appendix A: Download URLs

```
# NPPES Monthly Full File
https://download.cms.gov/nppes/NPPES_Data_Dissemination_[Month]_[Year].zip

# Provider of Services
https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/provider-of-services-file-hospital-non-hospital-facilities
```

## Appendix B: References

- NPPES Data Dissemination: https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination
- Taxonomy Codes: https://www.nucc.org/
- NBER NPI Data: https://www.nber.org/research/data/national-plan-and-provider-enumeration-system-nppesnpi
- ResDAC NPPES Guide: https://resdac.org/articles/overview-nppesnpi-downloadable-file
