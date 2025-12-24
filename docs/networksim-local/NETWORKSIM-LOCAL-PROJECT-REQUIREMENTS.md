# NetworkSim-Local Project Requirements

**Version**: 0.1 (Planning)  
**Status**: Future - After NetworkSim Skills Complete  
**Last Updated**: 2024-12-24  
**Prerequisite**: NetworkSim (skills-based) must be complete first

---

## 1. Executive Summary

NetworkSim-Local is the data infrastructure layer for the HealthSim ecosystem, providing access to real healthcare provider, facility, and pharmacy data from public sources. While NetworkSim (skills-based) generates synthetic entities and provides reference knowledge, NetworkSim-Local stores and queries actual data from sources like the NPPES NPI Registry, CMS Provider files, and pharmacy directories.

### Relationship to NetworkSim

| Component | Purpose | Data Type |
|-----------|---------|-----------|
| **NetworkSim (Skills)** | Knowledge + synthetic generation | Generated/synthetic |
| **NetworkSim-Local** | Real data lookups + geographic grounding | Real/public data |

### Value Proposition

1. **Geographic Realism** - Real providers in real locations
2. **Valid Identifiers** - Actual NPIs, DEA numbers, state licenses
3. **Specialty Distribution** - Authentic provider mix by geography
4. **Network Modeling** - Build realistic networks from real providers
5. **Cross-Product Enhancement** - Ground PatientSim, MemberSim, RxMemberSim in real infrastructure

---

## 2. Core Requirements

### 2.1 Functional Requirements

#### FR-1: Provider Data Access
- **FR-1.1**: Query providers by NPI (exact lookup)
- **FR-1.2**: Query providers by geography (state, county, city, ZIP)
- **FR-1.3**: Query providers by specialty/taxonomy code
- **FR-1.4**: Query providers by name (partial match)
- **FR-1.5**: Query providers by credential type (MD, DO, NP, PA, etc.)
- **FR-1.6**: Filter by active/inactive status
- **FR-1.7**: Return provider with full demographic and credential details

#### FR-2: Facility Data Access
- **FR-2.1**: Query facilities by CCN/Medicare ID
- **FR-2.2**: Query facilities by geography
- **FR-2.3**: Query facilities by type (hospital, SNF, ASC, etc.)
- **FR-2.4**: Query facilities by bed count/size
- **FR-2.5**: Query facilities by ownership type
- **FR-2.6**: Return facility with location and characteristic details

#### FR-3: Pharmacy Data Access
- **FR-3.1**: Query pharmacies by NCPDP ID
- **FR-3.2**: Query pharmacies by NPI
- **FR-3.3**: Query pharmacies by geography
- **FR-3.4**: Query pharmacies by type (retail, specialty, mail order)
- **FR-3.5**: Query pharmacies by chain affiliation
- **FR-3.6**: Return pharmacy with dispensing and location details

#### FR-4: Geographic Integration
- **FR-4.1**: Join provider data with PopulationSim geographic data
- **FR-4.2**: Calculate provider density by geography
- **FR-4.3**: Identify HPSAs/MUAs with provider coverage
- **FR-4.4**: Support time/distance calculations (future)

#### FR-5: Network Building
- **FR-5.1**: Select providers for network based on criteria
- **FR-5.2**: Validate network adequacy by specialty/geography
- **FR-5.3**: Export network roster in standard formats
- **FR-5.4**: Compare networks by provider overlap

### 2.2 Non-Functional Requirements

#### NFR-1: Data Currency
- Data refreshed quarterly (minimum) from source files
- Clearly document data vintage in all queries
- Support incremental updates where sources allow

#### NFR-2: Performance
- Single NPI lookup: < 100ms
- Geographic query (1000 results): < 1 second
- Specialty + geography query: < 2 seconds
- Full table scans avoided via proper indexing

#### NFR-3: Storage
- DuckDB database file (portable, no server required)
- Target size: < 5GB for core data
- Support for attached databases (PopulationSim integration)

#### NFR-4: Data Quality
- Validate all NPIs against check digit algorithm
- Flag incomplete records
- Track data lineage to source files
- Document known data quality issues by source

---

## 3. Data Scope

### 3.1 In Scope (Phase 1)

| Data Type | Source | Records (Est.) | Update Freq |
|-----------|--------|----------------|-------------|
| Individual Providers | NPPES NPI | ~2.5M active | Monthly |
| Organization Providers | NPPES NPI | ~800K active | Monthly |
| Hospital Facilities | CMS POS | ~6,500 | Annual |
| SNF Facilities | CMS POS | ~15,000 | Annual |
| ASC Facilities | CMS POS | ~5,500 | Annual |
| Retail Pharmacies | NCPDP/State | ~60,000 | Quarterly |

### 3.2 In Scope (Phase 2)

| Data Type | Source | Records (Est.) | Update Freq |
|-----------|--------|----------------|-------------|
| Specialty Pharmacies | Specialty networks | ~1,500 | Quarterly |
| FQHC/RHC | CMS | ~15,000 | Annual |
| Home Health Agencies | CMS | ~11,000 | Annual |
| Dialysis Facilities | CMS | ~7,500 | Annual |
| Lab/Imaging Centers | State licensing | Variable | Variable |

### 3.3 Out of Scope

- Real-time eligibility/credentialing status
- Individual provider schedule/availability
- Actual contracted rates (proprietary)
- Quality scores from commercial sources
- Patient attribution data

---

## 4. Integration Requirements

### 4.1 PopulationSim Integration

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                         │
├─────────────────────────────────────────────────────────────┤
│  PopulationSim-Local          NetworkSim-Local              │
│  ┌─────────────────┐          ┌─────────────────┐           │
│  │ Geographic Data │◄────────►│ Provider Data   │           │
│  │ - Counties      │  JOIN    │ - NPIs          │           │
│  │ - ZCTAs         │  ON      │ - Addresses     │           │
│  │ - Health Data   │  FIPS/   │ - Specialties   │           │
│  │ - Demographics  │  ZIP     │ - Facilities    │           │
│  └─────────────────┘          └─────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

**Key Join Points**:
- Provider ZIP → ZCTA → County → State
- Facility address → Geocoded coordinates → ZCTA/County
- Provider taxonomy → Specialty category → Network adequacy standards

### 4.2 NetworkSim Skills Integration

NetworkSim-Local enhances NetworkSim skills:

| NetworkSim Skill | NetworkSim-Local Enhancement |
|------------------|------------------------------|
| synthetic-provider | Use real NPI as template, generate synthetic attributes |
| synthetic-facility | Use real facility as template, modify characteristics |
| network-adequacy | Calculate actual adequacy from real provider data |
| provider-for-encounter | Look up real providers in geography |

### 4.3 Cross-Product Integration

| Product | NetworkSim-Local Provides |
|---------|---------------------------|
| PatientSim | Real provider NPIs for encounters |
| MemberSim | Real facility CCNs for claims |
| RxMemberSim | Real pharmacy NCPDPs for claims |
| TrialSim | Real site/investigator NPIs |

---

## 5. Technical Architecture

### 5.1 MCP Server Pattern

Follow PopulationSim-Local pattern:

```
healthsim-workspace/
└── mcp-servers/
    └── networksim-local/
        ├── package.json
        ├── tsconfig.json
        ├── src/
        │   ├── index.ts          # MCP server entry
        │   ├── tools/
        │   │   ├── provider-lookup.ts
        │   │   ├── facility-lookup.ts
        │   │   ├── pharmacy-lookup.ts
        │   │   └── network-builder.ts
        │   └── data/
        │       └── loaders/      # Data loading scripts
        └── data/
            ├── raw/              # Downloaded source files
            ├── processed/        # Cleaned/transformed
            └── networksim.duckdb # Main database
```

### 5.2 Database Schema (High-Level)

```sql
-- Core entity tables
CREATE TABLE providers (
    npi VARCHAR(10) PRIMARY KEY,
    entity_type VARCHAR(1),  -- '1' individual, '2' organization
    -- ... full schema in data architecture doc
);

CREATE TABLE facilities (
    ccn VARCHAR(10) PRIMARY KEY,
    facility_type VARCHAR(50),
    -- ... full schema in data architecture doc
);

CREATE TABLE pharmacies (
    ncpdp_id VARCHAR(10) PRIMARY KEY,
    npi VARCHAR(10),
    -- ... full schema in data architecture doc
);

-- Geographic linking tables
CREATE TABLE provider_locations (
    npi VARCHAR(10),
    location_type VARCHAR(20),  -- 'practice', 'mailing'
    address_line1 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip VARCHAR(10),
    county_fips VARCHAR(5),
    zcta VARCHAR(5)
);
```

### 5.3 Query Patterns

**Pattern 1: Direct Lookup**
```sql
SELECT * FROM providers WHERE npi = '1234567890';
```

**Pattern 2: Geographic Search**
```sql
SELECT p.*, pl.city, pl.state
FROM providers p
JOIN provider_locations pl ON p.npi = pl.npi
WHERE pl.state = 'TX' 
  AND p.taxonomy_1 LIKE '207R%'  -- Internal Medicine
LIMIT 100;
```

**Pattern 3: PopulationSim Join**
```sql
-- Attach PopulationSim database
ATTACH 'populationsim.duckdb' AS pop;

SELECT 
    p.npi, p.provider_name, pl.county_fips,
    c.county_name, c.total_population,
    h.diabetes_prevalence
FROM providers p
JOIN provider_locations pl ON p.npi = pl.npi
JOIN pop.counties c ON pl.county_fips = c.fips
JOIN pop.health_indicators h ON c.fips = h.fips
WHERE p.taxonomy_1 LIKE '207RE%'  -- Endocrinology
  AND h.diabetes_prevalence > 12.0;
```

---

## 6. Data Quality Requirements

### 6.1 Validation Rules

| Field | Rule | Action on Failure |
|-------|------|-------------------|
| NPI | Valid check digit | Reject record |
| State | Valid 2-letter code | Reject record |
| ZIP | 5 or 9 digits | Truncate to 5, warn if invalid |
| Taxonomy | Valid NUCC code | Flag, allow |
| CCN | 6 digits | Reject record |
| NCPDP | Valid format | Reject record |

### 6.2 Completeness Standards

| Entity | Required Fields | Target Completeness |
|--------|-----------------|---------------------|
| Provider | NPI, Name, State | 100% |
| Provider | Taxonomy, Address | 95% |
| Facility | CCN, Name, State, Type | 100% |
| Facility | Bed count, Ownership | 90% |
| Pharmacy | NCPDP, Name, State | 100% |
| Pharmacy | Store hours, Chain | 80% |

### 6.3 Data Lineage

Every record must track:
- Source file name
- Source file date
- Load timestamp
- Row number in source (for debugging)

---

## 7. Security & Privacy

### 7.1 Data Classification

All data in NetworkSim-Local is **Public Data**:
- NPPES is public record
- CMS Provider files are public
- No PHI is stored or processed

### 7.2 Access Controls

- Local file access only (no network exposure)
- MCP server runs in user context
- No authentication required (local use)

### 7.3 Sensitive Field Handling

While public, some fields warrant care:
- Provider personal addresses (use practice address preference)
- Sole proprietor information (flag appropriately)
- Sanction/exclusion data (document source carefully)

---

## 8. Success Criteria

### 8.1 Functional Success

- [ ] Query any US provider by NPI in < 100ms
- [ ] Search providers by specialty + geography
- [ ] Search facilities by type + geography
- [ ] Search pharmacies by type + geography
- [ ] Join with PopulationSim data seamlessly
- [ ] Generate realistic provider rosters for networks

### 8.2 Data Quality Success

- [ ] > 99% of active NPIs from NPPES loaded
- [ ] > 95% of providers geocoded to county
- [ ] All facilities matched to CMS data
- [ ] Data vintage clearly documented

### 8.3 Integration Success

- [ ] MCP server registered and functional
- [ ] Claude can query via natural language
- [ ] NetworkSim skills can leverage real data
- [ ] Cross-product workflows demonstrated

---

## 9. Dependencies

### 9.1 Prerequisites

| Dependency | Status | Notes |
|------------|--------|-------|
| NetworkSim (skills) | In Progress | Must complete Phase 1-4 first |
| PopulationSim-Local | Complete | Required for geographic integration |
| DuckDB infrastructure | Complete | Established pattern |
| MCP server framework | Complete | Follow existing pattern |

### 9.2 External Dependencies

| Dependency | Risk | Mitigation |
|------------|------|------------|
| NPPES data availability | Low | Monthly public releases |
| CMS file format changes | Medium | Version data loaders |
| NCPDP access | Medium | Evaluate alternatives |
| Geocoding service | Low | Use Census geocoder (free) |

---

## 10. Open Questions

### Resolved
- ✅ Separate from NetworkSim skills (confirmed)
- ✅ Use DuckDB (follow PopulationSim pattern)
- ✅ MCP server architecture (confirmed)

### Pending
- ❓ Best source for retail pharmacy data (NCPDP licensing cost?)
- ❓ Include prescriber DEA data? (registration required)
- ❓ State licensing integration scope (50 different systems)
- ❓ Refresh automation approach (manual vs scheduled)

---

## 11. Related Documents

- [NetworkSim Project Plan](../networksim/NETWORKSIM-PROJECT-PLAN.md)
- [NetworkSim Architecture](../networksim/NETWORKSIM-ARCHITECTURE-CONSISTENCY.md)
- [PopulationSim Data Architecture](../populationsim/POPULATIONSIM-DATA-ARCHITECTURE.md)
- [HealthSim Architecture Guide](../HEALTHSIM-ARCHITECTURE-GUIDE.md)
- [NetworkSim-Local Data Architecture](NETWORKSIM-LOCAL-DATA-ARCHITECTURE.md)
- [NetworkSim-Local Implementation Plan](NETWORKSIM-LOCAL-IMPLEMENTATION-PLAN.md)
- [NetworkSim-Local Data Sources](NETWORKSIM-LOCAL-DATA-SOURCES.md)

---

*Document Status: Planning - Not yet approved for implementation*
