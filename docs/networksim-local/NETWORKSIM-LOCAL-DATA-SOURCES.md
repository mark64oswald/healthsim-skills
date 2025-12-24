# NetworkSim-Local Data Sources

**Version**: 0.1 (Planning)  
**Status**: Future - Research Complete  
**Last Updated**: 2024-12-24

---

## 1. Overview

This document catalogs public data sources for NetworkSim-Local, including download locations, file formats, update frequencies, and usage notes. All sources are publicly available and free for use.

---

## 2. Provider Data Sources

### 2.1 NPPES NPI Registry

**Primary source for provider identification**

| Attribute | Value |
|-----------|-------|
| **Publisher** | CMS (Centers for Medicare & Medicaid Services) |
| **URL** | https://download.cms.gov/nppes/NPI_Files.html |
| **Format** | CSV (zipped) |
| **Size** | ~8GB uncompressed (full file), ~500MB weekly delta |
| **Update Frequency** | Weekly (Sundays), Monthly full file |
| **License** | Public domain |
| **Records** | ~8M total, ~3.3M active |

**Key Fields Available**:
- NPI (10-digit identifier)
- Entity Type (Individual vs Organization)
- Provider Name (Legal and Other)
- Credentials
- Taxonomy Codes (up to 15)
- Practice Location Address
- Mailing Address
- Phone/Fax
- Enumeration Date
- Deactivation Status

**Download Options**:
1. **Full Replacement Monthly File** - Complete dataset (~8GB)
2. **Weekly Update File** - Changes only (~100-500MB)
3. **Deactivation File** - Deactivated NPIs only

**Usage Notes**:
- Individual providers (Entity Type 1) include physicians, NPs, PAs, etc.
- Organization providers (Entity Type 2) include practices, hospitals, pharmacies
- Some organizations have both Type 1 and Type 2 NPIs
- Taxonomy codes use NUCC Healthcare Provider Taxonomy Code Set
- Address quality varies; many are billing addresses, not practice locations

**Sample Download Command**:
```bash
# Full monthly file
wget https://download.cms.gov/nppes/NPPES_Data_Dissemination_January_2025.zip

# Weekly update
wget https://download.cms.gov/nppes/NPPES_Weekly/npidata_pfile_20250106-20250112.zip
```

---

### 2.2 NUCC Healthcare Provider Taxonomy Code Set

**Reference data for provider specialties**

| Attribute | Value |
|-----------|-------|
| **Publisher** | NUCC (National Uniform Claim Committee) |
| **URL** | https://nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40 |
| **Format** | CSV, Excel |
| **Size** | ~500KB |
| **Update Frequency** | Semi-annual (January, July) |
| **License** | Free for use (attribution requested) |
| **Records** | ~900 codes |

**Key Fields**:
- Code (10-character alphanumeric)
- Grouping (e.g., "Allopathic & Osteopathic Physicians")
- Classification (e.g., "Internal Medicine")
- Specialization (e.g., "Cardiovascular Disease")
- Definition
- Notes

**Usage Notes**:
- Hierarchical structure: Grouping → Classification → Specialization
- Not all combinations exist
- Some codes deprecated over time
- Cross-reference with NPPES taxonomy fields

---

### 2.3 Medicare Provider Enrollment Data

**Supplemental provider information**

| Attribute | Value |
|-----------|-------|
| **Publisher** | CMS |
| **URL** | https://data.cms.gov/provider-data/ |
| **Format** | CSV |
| **Update Frequency** | Quarterly |
| **License** | Public domain |

**Useful Datasets**:

1. **Physician Compare** (being replaced by Care Compare)
   - ~1.2M individual physicians
   - Includes specialty, group affiliation, hospital affiliation
   - PAC ID linking

2. **Medicare Opt-Out Physicians**
   - Physicians who don't accept Medicare
   - ~40,000 records

3. **Provider Enrollment Affiliation**
   - Links between individual and organizational NPIs
   - Useful for building practice rosters

---

## 3. Facility Data Sources

### 3.1 CMS Provider of Services (POS) File

**Primary source for Medicare-certified facilities**

| Attribute | Value |
|-----------|-------|
| **Publisher** | CMS |
| **URL** | https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/provider-of-services-file |
| **Format** | CSV |
| **Size** | ~100MB |
| **Update Frequency** | Quarterly |
| **License** | Public domain |
| **Records** | ~75,000 facilities |

**Facility Types Included**:
- Hospitals (acute, psychiatric, rehabilitation, children's)
- Skilled Nursing Facilities (SNF)
- Home Health Agencies
- Hospice
- Ambulatory Surgical Centers (ASC)
- End-Stage Renal Disease (ESRD) facilities
- Rural Health Clinics (RHC)
- Federally Qualified Health Centers (FQHC)
- Outpatient Physical Therapy
- Portable X-Ray Suppliers

**Key Fields**:
- CCN (CMS Certification Number)
- Facility Name
- Address
- Facility Type
- Certification Date
- Bed Count (where applicable)
- Ownership Type
- Accreditation (TJC, DNV, etc.)
- Medicare participation status

**Usage Notes**:
- CCN is 6 characters: first 2 = state, next 4 = facility identifier
- Bed counts only for inpatient facilities
- Some facilities have multiple CCNs (e.g., distinct part SNF in hospital)

---

### 3.2 Hospital General Information

**Detailed hospital characteristics**

| Attribute | Value |
|-----------|-------|
| **Publisher** | CMS |
| **URL** | https://data.cms.gov/provider-data/dataset/xubh-q36u |
| **Format** | CSV, JSON API |
| **Update Frequency** | Quarterly |
| **Records** | ~6,500 hospitals |

**Key Fields**:
- Facility ID (CCN)
- Facility Name
- Address
- Phone
- Hospital Type (Acute Care, Critical Access, etc.)
- Hospital Ownership
- Emergency Services (Yes/No)
- Meets EHR Criteria

---

### 3.3 Other CMS Facility Files

| Dataset | Records | Key Use |
|---------|---------|---------|
| Nursing Home Compare | ~15,000 | SNF details, ratings |
| Home Health Compare | ~11,000 | HHA details |
| Hospice Compare | ~5,500 | Hospice details |
| Dialysis Facility Compare | ~7,500 | ESRD facilities |
| FQHC/RHC Data | ~15,000 | Community health centers |

---

## 4. Pharmacy Data Sources

### 4.1 NCPDP Provider Database

**Industry standard pharmacy identification**

| Attribute | Value |
|-----------|-------|
| **Publisher** | NCPDP (National Council for Prescription Drug Programs) |
| **URL** | https://www.ncpdp.org/Resources/Provider-Identification-Number.aspx |
| **Format** | Proprietary (licensed) |
| **Update Frequency** | Weekly |
| **License** | **Paid subscription required** |
| **Records** | ~80,000 pharmacies |

**Key Fields**:
- NCPDP Provider ID (7 digits)
- NPI
- Store Name
- Address
- Store Number
- Chain Code
- Dispensing Class
- Specialty Indicators

**Usage Notes**:
- NCPDP ID is the standard pharmacy identifier for claims
- License fee varies by use case
- **Alternative**: Extract pharmacy NPIs from NPPES (free, but less detailed)

---

### 4.2 NPPES Pharmacy Extraction

**Free alternative to NCPDP**

| Attribute | Value |
|-----------|-------|
| **Source** | NPPES NPI Registry (filtered) |
| **Cost** | Free |
| **Records** | ~65,000 pharmacies with Type 2 NPI |

**Extraction Method**:
```sql
-- Extract pharmacies from NPPES
SELECT *
FROM nppes_raw
WHERE entity_type = '2'  -- Organization
AND (
    taxonomy_code_1 LIKE '333%' OR  -- Pharmacy taxonomy codes
    taxonomy_code_2 LIKE '333%' OR
    taxonomy_code_3 LIKE '333%'
);
```

**Taxonomy Codes for Pharmacies**:
- 333600000X - Pharmacy
- 3336C0002X - Clinic Pharmacy
- 3336C0003X - Community/Retail Pharmacy
- 3336C0004X - Compounding Pharmacy
- 3336H0001X - Home Infusion Therapy Pharmacy
- 3336I0012X - Institutional Pharmacy
- 3336L0003X - Long Term Care Pharmacy
- 3336M0002X - Mail Order Pharmacy
- 3336N0007X - Nuclear Pharmacy
- 3336S0011X - Specialty Pharmacy

**Limitations**:
- No NCPDP ID (must cross-reference)
- No chain affiliation
- No specialty pharmacy designations beyond taxonomy
- Less complete than NCPDP database

---

### 4.3 State Pharmacy Board Data

**State-level pharmacy licensing**

Many state pharmacy boards publish licensed pharmacy lists:

| State | URL | Format | Notes |
|-------|-----|--------|-------|
| California | https://www.pharmacy.ca.gov/about/verify_lic.shtml | Search/API | License verification |
| Texas | https://www.pharmacy.texas.gov/dbsearch/ | Search | Limited bulk access |
| Florida | https://mqa-internet.doh.state.fl.us/MQASearchServices/HealthCareProviders | Search | Multi-profession |
| New York | https://www.op.nysed.gov/verification-search | Search | License verification |

**Usage Notes**:
- Most states don't offer bulk downloads
- Would need to scrape or use individual lookups
- Data quality and completeness varies widely
- **Recommendation**: Use NPPES + manual specialty pharmacy list

---

### 4.4 Specialty Pharmacy Networks

**Limited distribution drug networks**

| Network | Pharmacies | Access |
|---------|------------|--------|
| Specialty Pharmacy Certification Board (SPCB) | ~500 certified | Public list |
| URAC Specialty Pharmacy | ~400 accredited | Public list |
| ACHC Specialty Pharmacy | ~300 accredited | Public list |
| Manufacturer Hub Programs | Varies | Often proprietary |

**Usage Notes**:
- Specialty pharmacies are a small subset (~1,500 unique)
- Many limited distribution drugs require specific network membership
- Consider maintaining curated specialty pharmacy list

---

## 5. Geographic Reference Data

### 5.1 Census Geographic Data

**For geocoding and boundary definitions**

| Dataset | URL | Use |
|---------|-----|-----|
| ZCTA to County Crosswalk | https://www.census.gov/programs-surveys/geography/technical-documentation/records-layout/zcta-county-record-layout.html | ZIP to county mapping |
| County FIPS Codes | https://www.census.gov/library/reference/code-lists/ansi.html | Standardized county IDs |
| CBSA Definitions | https://www.census.gov/programs-surveys/metro-micro.html | Urban/rural classification |

### 5.2 Census Geocoder

**Free geocoding API**

| Attribute | Value |
|-----------|-------|
| **URL** | https://geocoding.geo.census.gov/geocoder/ |
| **Format** | REST API, Batch upload |
| **Rate Limit** | 10,000/day (batch), unlimited (single) |
| **Cost** | Free |

**Batch Processing**:
```bash
# Upload CSV with addresses, get back with coordinates
curl -X POST \
  -F "addressFile=@addresses.csv" \
  -F "benchmark=Public_AR_Current" \
  -F "vintage=Census2020_Current" \
  https://geocoding.geo.census.gov/geocoder/locations/addressbatch
```

---

## 6. Data Source Summary

### 6.1 Phase 1 Sources (Essential)

| Source | Entity Type | Records | Cost | Priority |
|--------|-------------|---------|------|----------|
| NPPES Full File | Providers | 3.3M | Free | Must |
| NUCC Taxonomy | Reference | 900 | Free | Must |
| CMS POS File | Facilities | 75K | Free | Must |
| NPPES Pharmacy Extract | Pharmacies | 65K | Free | Must |
| Census Geocoder | Geocoding | N/A | Free | Must |

### 6.2 Phase 2 Sources (Enhancement)

| Source | Entity Type | Records | Cost | Priority |
|--------|-------------|---------|------|----------|
| Hospital General Info | Hospitals | 6.5K | Free | Should |
| Nursing Home Compare | SNFs | 15K | Free | Should |
| Medicare Provider Enrollment | Affiliations | Varies | Free | Should |
| Specialty Pharmacy Lists | Pharmacies | 1.5K | Free | Should |

### 6.3 Deferred Sources (Evaluation Needed)

| Source | Entity Type | Records | Cost | Priority |
|--------|-------------|---------|------|----------|
| NCPDP Provider Database | Pharmacies | 80K | $$ | Could |
| State Licensing Data | Various | Varies | Free | Could |
| DEA Registration | Prescribers | 1.5M | $$ | Could |

---

## 7. Data Refresh Strategy

### 7.1 Recommended Schedule

| Data Type | Refresh Frequency | Method |
|-----------|-------------------|--------|
| NPPES (providers) | Monthly | Full replacement |
| NUCC Taxonomy | Semi-annual | Full replacement |
| CMS POS (facilities) | Quarterly | Full replacement |
| Pharmacy data | Quarterly | Full replacement |
| Geocoding | On new addresses | Incremental |

### 7.2 Automation Approach

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA REFRESH PIPELINE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐     ┌────────────┐  │
│  │  1. Download │ ───► │  2. Validate │ ──► │ 3. Transform│  │
│  │  Source Files│      │  & Clean     │     │ & Geocode   │  │
│  └──────────────┘      └──────────────┘     └────────────┘  │
│                                                     │        │
│                                                     ▼        │
│  ┌──────────────┐      ┌──────────────┐     ┌────────────┐  │
│  │  6. Archive  │ ◄─── │  5. Notify   │ ◄── │ 4. Load to │  │
│  │  Old Data    │      │  & Log       │     │ DuckDB     │  │
│  └──────────────┘      └──────────────┘     └────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Initial Approach**: Manual downloads and loads  
**Future**: Scheduled automation with notification

---

## 8. Known Data Quality Issues

### 8.1 NPPES Issues

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Outdated addresses | Medium | Cross-reference with Medicare enrollment |
| Missing taxonomy codes | Low | Default to most common for entity type |
| Duplicate organizational NPIs | Low | Use most recent update |
| Inconsistent name formatting | Medium | Normalize during load |

### 8.2 Facility Data Issues

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Stale closure information | Medium | Check Medicare enrollment status |
| Missing bed counts (ASCs) | Low | Expected - not applicable |
| Inconsistent facility types | Low | Map to standardized types |

### 8.3 Pharmacy Data Issues

| Issue | Impact | Mitigation |
|-------|--------|------------|
| No NCPDP ID without license | High | Use NPI as primary key |
| Missing chain affiliations | Medium | Manual curation for major chains |
| Specialty classification incomplete | Medium | Use accreditation lists |

---

## 9. Related Documents

- [NetworkSim-Local Project Requirements](NETWORKSIM-LOCAL-PROJECT-REQUIREMENTS.md)
- [NetworkSim-Local Data Architecture](NETWORKSIM-LOCAL-DATA-ARCHITECTURE.md)
- [NetworkSim-Local Implementation Plan](NETWORKSIM-LOCAL-IMPLEMENTATION-PLAN.md)
- [PopulationSim Data Sources](../populationsim/data-sources-reference.md)

---

*Document Status: Research Complete - Sources validated as of December 2024*
