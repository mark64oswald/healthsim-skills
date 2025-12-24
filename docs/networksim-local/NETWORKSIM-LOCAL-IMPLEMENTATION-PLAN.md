# NetworkSim-Local Implementation Plan

**Version**: 0.1 (Planning)  
**Status**: Future - After NetworkSim Skills Complete  
**Last Updated**: 2024-12-24  
**Estimated Duration**: 4-6 weeks (after prerequisites)

---

## 1. Prerequisites

Before starting NetworkSim-Local implementation:

| Prerequisite | Status | Notes |
|--------------|--------|-------|
| NetworkSim (skills-based) complete | In Progress | Must finish Phases 1-5 |
| PopulationSim-Local operational | Complete | Pattern to follow |
| MCP server framework understood | Complete | TypeScript pattern |
| DuckDB expertise | Complete | From PopulationSim |
| Data sources researched | Complete | See DATA-SOURCES.md |

---

## 2. Implementation Phases

### Phase Overview

| Phase | Focus | Duration | Key Deliverables |
|-------|-------|----------|------------------|
| Phase 1 | Infrastructure Setup | 1 week | Directory, MCP server shell, database |
| Phase 2 | Provider Data | 1-2 weeks | NPPES load, provider tables, geocoding |
| Phase 3 | Facility Data | 1 week | CMS POS load, facility tables |
| Phase 4 | Pharmacy Data | 1 week | Pharmacy tables, specialty curation |
| Phase 5 | Integration & Polish | 1 week | PopulationSim integration, testing |

---

## 3. Phase 1: Infrastructure Setup

**Duration**: 1 week  
**Goal**: Establish project structure and basic MCP server

### 3.1 Tasks

| Task | Description | Estimated Hours |
|------|-------------|-----------------|
| 1.1 | Create directory structure | 1 |
| 1.2 | Initialize Node.js project | 1 |
| 1.3 | Configure TypeScript | 1 |
| 1.4 | Create MCP server entry point | 2 |
| 1.5 | Create DuckDB connection module | 2 |
| 1.6 | Create placeholder tools | 4 |
| 1.7 | Configure Claude Desktop integration | 2 |
| 1.8 | Test basic connectivity | 2 |
| 1.9 | Document setup process | 2 |

### 3.2 Directory Structure to Create

```
healthsim-workspace/
└── mcp-servers/
    └── networksim-local/
        ├── package.json
        ├── tsconfig.json
        ├── README.md
        ├── src/
        │   ├── index.ts              # MCP server entry
        │   ├── db/
        │   │   └── connection.ts     # DuckDB connection
        │   ├── tools/
        │   │   ├── provider-lookup.ts
        │   │   ├── facility-lookup.ts
        │   │   ├── pharmacy-lookup.ts
        │   │   └── network-builder.ts
        │   └── loaders/
        │       ├── nppes-loader.ts
        │       ├── cms-loader.ts
        │       └── pharmacy-loader.ts
        ├── data/
        │   ├── raw/                  # Downloaded source files
        │   ├── processed/            # Intermediate files
        │   └── networksim.duckdb     # Main database
        └── scripts/
            ├── download-sources.sh
            ├── load-all.sh
            └── validate-data.sh
```

### 3.3 Deliverables

- [ ] MCP server responds to Claude Desktop
- [ ] DuckDB database created (empty)
- [ ] Placeholder tools return "not implemented"
- [ ] README documents local setup
- [ ] Package.json with all dependencies

### 3.4 Verification

```bash
# Verify MCP server starts
cd mcp-servers/networksim-local
npm run build
npm start

# Verify in Claude Desktop
"List the tools available from networksim-local"
```

---

## 4. Phase 2: Provider Data

**Duration**: 1-2 weeks  
**Goal**: Load NPPES data with geocoding

### 4.1 Tasks

| Task | Description | Estimated Hours |
|------|-------------|-----------------|
| 2.1 | Download NPPES full file | 2 |
| 2.2 | Create provider schema in DuckDB | 2 |
| 2.3 | Build NPPES parsing logic | 8 |
| 2.4 | Create provider table loader | 4 |
| 2.5 | Create provider_locations loader | 4 |
| 2.6 | Load NUCC taxonomy reference | 2 |
| 2.7 | Implement Census geocoder integration | 8 |
| 2.8 | Batch geocode provider addresses | 8 |
| 2.9 | Create provider-lookup tool | 4 |
| 2.10 | Create specialty-search tool | 4 |
| 2.11 | Test provider queries | 4 |
| 2.12 | Document data quality metrics | 2 |

### 4.2 Schema Creation

```sql
-- Execute via loader or migration script
CREATE TABLE IF NOT EXISTS providers (
    npi VARCHAR(10) PRIMARY KEY,
    entity_type VARCHAR(1) NOT NULL,
    provider_last_name VARCHAR(100),
    provider_first_name VARCHAR(50),
    provider_organization_name VARCHAR(200),
    provider_credential VARCHAR(50),
    gender VARCHAR(1),
    taxonomy_code_1 VARCHAR(10),
    taxonomy_code_2 VARCHAR(10),
    taxonomy_code_3 VARCHAR(10),
    enumeration_date DATE,
    last_update_date DATE,
    npi_deactivation_date DATE,
    source_file VARCHAR(100),
    source_date DATE,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS provider_locations (
    npi VARCHAR(10),
    location_type VARCHAR(20),
    address_line_1 VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip VARCHAR(10),
    county_fips VARCHAR(5),
    zcta VARCHAR(5),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    PRIMARY KEY (npi, location_type)
);
```

### 4.3 NPPES Processing Pipeline

```
┌───────────────────────────────────────────────────────────────┐
│                    NPPES LOAD PIPELINE                         │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  1. Download & Extract                                         │
│     wget https://download.cms.gov/nppes/NPPES_*.zip           │
│     unzip to data/raw/nppes/                                  │
│                                                                │
│  2. Stream Parse (avoid loading 8GB into memory)              │
│     - Read CSV in chunks (100K rows)                          │
│     - Validate NPI check digit                                │
│     - Filter: US addresses only, active only                  │
│                                                                │
│  3. Transform                                                  │
│     - Split into providers + provider_locations               │
│     - Normalize names (uppercase, trim)                       │
│     - Parse dates                                             │
│     - Extract up to 3 taxonomy codes                          │
│                                                                │
│  4. Geocode (batch)                                           │
│     - Extract unique addresses                                │
│     - Submit to Census geocoder (10K/batch)                   │
│     - Join results back to locations                          │
│                                                                │
│  5. Load to DuckDB                                            │
│     - COPY INTO from Parquet (fastest)                        │
│     - Create indexes                                          │
│     - Update load log                                         │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

### 4.4 Provider Lookup Tool Implementation

```typescript
// src/tools/provider-lookup.ts
export const providerLookupTool = {
  name: "lookup_provider",
  description: "Look up healthcare providers by NPI, name, specialty, or location",
  inputSchema: {
    type: "object",
    properties: {
      npi: { type: "string", description: "Exact 10-digit NPI" },
      name: { type: "string", description: "Partial name match" },
      specialty: { type: "string", description: "Specialty category or taxonomy code" },
      state: { type: "string", description: "2-letter state code" },
      county_fips: { type: "string", description: "5-digit FIPS code" },
      zip: { type: "string", description: "5-digit ZIP" },
      city: { type: "string", description: "City name" },
      entity_type: { type: "string", enum: ["individual", "organization"] },
      include_inactive: { type: "boolean", default: false },
      limit: { type: "integer", default: 100, maximum: 1000 }
    }
  },
  async execute(params: ProviderLookupParams): Promise<ProviderResult[]> {
    // Build dynamic SQL based on params
    // Execute query
    // Return results
  }
};
```

### 4.5 Deliverables

- [ ] 3.3M+ active providers loaded
- [ ] 6.6M+ provider locations loaded
- [ ] 80%+ addresses geocoded to county
- [ ] Provider lookup tool functional
- [ ] Query latency < 500ms for typical searches
- [ ] Load log with data vintage documented

---

## 5. Phase 3: Facility Data

**Duration**: 1 week  
**Goal**: Load CMS facility data

### 5.1 Tasks

| Task | Description | Estimated Hours |
|------|-------------|-----------------|
| 3.1 | Download CMS POS file | 1 |
| 3.2 | Create facility schema | 2 |
| 3.3 | Build CMS parsing logic | 4 |
| 3.4 | Create facility loader | 4 |
| 3.5 | Geocode facility addresses | 4 |
| 3.6 | Create facility-lookup tool | 4 |
| 3.7 | Create facility-type reference | 2 |
| 3.8 | Test facility queries | 2 |
| 3.9 | Document facility types | 2 |

### 5.2 Facility Type Mapping

```sql
-- Map CMS facility types to standardized categories
INSERT INTO facility_type_reference VALUES
('01', 'Hospital', 'Short Term Acute Care Hospital', 'Hospital'),
('02', 'Hospital', 'Long Term Acute Care Hospital', 'Hospital'),
('03', 'Hospital', 'Rehabilitation Hospital', 'Hospital'),
('04', 'Hospital', 'Psychiatric Hospital', 'Hospital'),
('05', 'Hospital', 'Children''s Hospital', 'Hospital'),
('06', 'SNF', 'Skilled Nursing Facility', 'Post-Acute'),
('07', 'NF', 'Nursing Facility', 'Post-Acute'),
('08', 'HHA', 'Home Health Agency', 'Home-Based'),
('09', 'Hospice', 'Hospice', 'Home-Based'),
('10', 'ASC', 'Ambulatory Surgical Center', 'Ambulatory'),
('11', 'ESRD', 'End Stage Renal Disease Facility', 'Ambulatory'),
('12', 'RHC', 'Rural Health Clinic', 'Primary Care'),
('13', 'FQHC', 'Federally Qualified Health Center', 'Primary Care');
```

### 5.3 Deliverables

- [ ] 75K+ facilities loaded
- [ ] All facility types mapped
- [ ] Facility lookup tool functional
- [ ] Bed count data accurate where applicable

---

## 6. Phase 4: Pharmacy Data

**Duration**: 1 week  
**Goal**: Load pharmacy data and curate specialty pharmacies

### 6.1 Tasks

| Task | Description | Estimated Hours |
|------|-------------|-----------------|
| 4.1 | Extract pharmacies from NPPES | 4 |
| 4.2 | Create pharmacy schema | 2 |
| 4.3 | Classify by taxonomy code | 4 |
| 4.4 | Curate specialty pharmacy list | 8 |
| 4.5 | Identify major chains | 4 |
| 4.6 | Geocode pharmacy addresses | 4 |
| 4.7 | Create pharmacy-lookup tool | 4 |
| 4.8 | Test pharmacy queries | 2 |

### 6.2 Pharmacy Classification Logic

```typescript
// Classify pharmacy by taxonomy code
function classifyPharmacy(taxonomyCodes: string[]): PharmacyClassification {
  const classifications = {
    '3336C0003X': { type: 'Retail', specialty: false },
    '3336M0002X': { type: 'Mail Order', specialty: false },
    '3336S0011X': { type: 'Specialty', specialty: true },
    '3336H0001X': { type: 'Home Infusion', specialty: true },
    '3336C0004X': { type: 'Compounding', specialty: false },
    '3336L0003X': { type: 'Long Term Care', specialty: false },
    '3336N0007X': { type: 'Nuclear', specialty: true },
    '3336I0012X': { type: 'Institutional', specialty: false },
  };
  
  // Find most specific match
  for (const code of taxonomyCodes) {
    if (classifications[code]) {
      return classifications[code];
    }
  }
  return { type: 'Retail', specialty: false };  // Default
}
```

### 6.3 Major Chain Identification

```typescript
// Match pharmacy names to chain codes
const chainPatterns = [
  { pattern: /CVS|CAREMARK/i, chain: 'CVS', code: 'CVS' },
  { pattern: /WALGREEN/i, chain: 'Walgreens', code: 'WAG' },
  { pattern: /WALMART|SAM.S CLUB/i, chain: 'Walmart', code: 'WMT' },
  { pattern: /RITE AID/i, chain: 'Rite Aid', code: 'RAD' },
  { pattern: /KROGER|FRED MEYER|RALPH/i, chain: 'Kroger', code: 'KRO' },
  { pattern: /COSTCO/i, chain: 'Costco', code: 'COS' },
  { pattern: /PUBLIX/i, chain: 'Publix', code: 'PUB' },
  { pattern: /H.E.B|HEB/i, chain: 'HEB', code: 'HEB' },
  { pattern: /ALDI/i, chain: 'ALDI', code: 'ALD' },
  { pattern: /EXPRESS SCRIPTS|ACCREDO/i, chain: 'Express Scripts', code: 'ESI' },
  { pattern: /OPTUMRX|BRIOVA/i, chain: 'OptumRx', code: 'OPT' },
];
```

### 6.4 Specialty Pharmacy Curation

Sources for specialty pharmacy identification:
1. Taxonomy code 3336S0011X
2. URAC accredited list
3. ACHC accredited list  
4. Known limited distribution network members

### 6.5 Deliverables

- [ ] 65K+ pharmacies loaded
- [ ] Pharmacy types classified
- [ ] Major chains identified
- [ ] 1,500+ specialty pharmacies flagged
- [ ] Pharmacy lookup tool functional

---

## 7. Phase 5: Integration & Polish

**Duration**: 1 week  
**Goal**: PopulationSim integration, testing, documentation

### 7.1 Tasks

| Task | Description | Estimated Hours |
|------|-------------|-----------------|
| 5.1 | Implement PopulationSim attach | 4 |
| 5.2 | Create joined query examples | 4 |
| 5.3 | Implement network-builder tool | 8 |
| 5.4 | Create adequacy calculation | 4 |
| 5.5 | Write integration tests | 4 |
| 5.6 | Performance optimization | 4 |
| 5.7 | Write developer documentation | 4 |
| 5.8 | Create hello-healthsim examples | 4 |
| 5.9 | Update cross-product references | 2 |
| 5.10 | Final testing and polish | 4 |

### 7.2 PopulationSim Integration Query

```typescript
// Example: Find providers in underserved areas
async function findProvidersInUnderservedAreas(specialty: string): Promise<ProviderWithContext[]> {
  const query = `
    ATTACH 'path/to/populationsim.duckdb' AS pop (READ_ONLY);
    
    SELECT 
      p.npi,
      p.provider_last_name,
      p.provider_first_name,
      p.taxonomy_code_1,
      pl.city,
      pl.state,
      pl.county_fips,
      c.county_name,
      c.total_population,
      h.primary_care_physicians_rate,
      CASE WHEN h.primary_care_physicians_rate < 50 THEN 'Underserved' ELSE 'Adequate' END as access_status
    FROM providers p
    JOIN provider_locations pl ON p.npi = pl.npi
    JOIN pop.counties c ON pl.county_fips = c.fips
    LEFT JOIN pop.health_indicators h ON c.fips = h.fips
    WHERE p.taxonomy_code_1 LIKE $1
      AND p.npi_deactivation_date IS NULL
      AND h.primary_care_physicians_rate < 50
    ORDER BY h.primary_care_physicians_rate ASC
    LIMIT 100
  `;
  
  return db.all(query, [specialty + '%']);
}
```

### 7.3 Network Builder Tool

```typescript
export const networkBuilderTool = {
  name: "build_provider_network",
  description: "Build a provider network for specified geography and specialties",
  inputSchema: {
    type: "object",
    properties: {
      states: { type: "array", items: { type: "string" } },
      counties: { type: "array", items: { type: "string" } },
      required_specialties: { 
        type: "array", 
        items: { type: "string" },
        description: "Specialty categories to include (e.g., 'Primary Care', 'Cardiology')" 
      },
      include_facilities: { type: "boolean", default: true },
      include_pharmacies: { type: "boolean", default: true },
      network_type: { 
        type: "string", 
        enum: ["HMO", "PPO", "EPO"],
        description: "Network type for adequacy validation"
      },
      validate_adequacy: { type: "boolean", default: false }
    },
    required: ["required_specialties"]
  },
  async execute(params): Promise<NetworkBuildResult> {
    // 1. Query providers by specialty and geography
    // 2. Query facilities if requested
    // 3. Query pharmacies if requested
    // 4. Validate adequacy if requested
    // 5. Return network roster with summary
  }
};
```

### 7.4 Deliverables

- [ ] PopulationSim attach working
- [ ] Joined queries demonstrable
- [ ] Network builder functional
- [ ] Integration tests passing
- [ ] Developer documentation complete
- [ ] Hello-healthsim examples added
- [ ] Performance targets met

---

## 8. Success Criteria

### 8.1 Functional

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Provider lookup by NPI | < 100ms | Query timing |
| Provider search (state + specialty) | < 500ms | Query timing |
| Facility lookup by CCN | < 100ms | Query timing |
| Pharmacy lookup by type | < 500ms | Query timing |
| Network build (1 state) | < 5s | Query timing |
| PopulationSim join queries | Work seamlessly | Integration test |

### 8.2 Data Quality

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Active providers loaded | > 3M | Row count |
| Providers geocoded to county | > 80% | Completeness check |
| Facilities loaded | > 50K | Row count |
| Pharmacies loaded | > 60K | Row count |
| Specialty pharmacies identified | > 1,000 | Specialty flag count |

### 8.3 Documentation

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| README complete | Yes | Review |
| Tool documentation | All tools | Review |
| Hello-healthsim examples | 3+ examples | Count |
| Data source documentation | Complete | Review |

---

## 9. Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| NPPES file format change | Low | High | Version loaders, test with each release |
| Geocoding rate limits | Medium | Medium | Batch processing, cache results |
| Database size too large | Low | Medium | Partition by state if needed |
| Poor address quality | Medium | Medium | Fallback to ZIP centroid |
| Missing pharmacy data | Medium | High | Use NPPES + manual curation |

---

## 10. Dependencies

### 10.1 Technical Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Node.js | 18+ | Runtime |
| TypeScript | 5.x | Development |
| DuckDB Node | 0.9+ | Database |
| @anthropic-ai/sdk | Latest | MCP protocol |
| csv-parser | Latest | NPPES parsing |
| fast-csv | Latest | CSV streaming |

### 10.2 External Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| NPPES data availability | Stable | Monthly release |
| Census geocoder | Stable | Free API |
| CMS data files | Stable | Quarterly release |

---

## 11. Post-Implementation

### 11.1 Maintenance Tasks

| Task | Frequency | Owner |
|------|-----------|-------|
| NPPES refresh | Monthly | Manual |
| Facility data refresh | Quarterly | Manual |
| Specialty pharmacy curation | Quarterly | Manual |
| Performance monitoring | Ongoing | Automated |

### 11.2 Future Enhancements

| Enhancement | Priority | Notes |
|-------------|----------|-------|
| Automated data refresh | Medium | Schedule downloads |
| More facility types | Low | Add HHA, hospice, etc. |
| Provider affiliation linking | Medium | Connect individual to org |
| Quality/ratings integration | Low | CMS Star ratings |
| Historical data tracking | Low | Track changes over time |

---

## 12. Related Documents

- [NetworkSim-Local Project Requirements](NETWORKSIM-LOCAL-PROJECT-REQUIREMENTS.md)
- [NetworkSim-Local Data Architecture](NETWORKSIM-LOCAL-DATA-ARCHITECTURE.md)
- [NetworkSim-Local Data Sources](NETWORKSIM-LOCAL-DATA-SOURCES.md)
- [PopulationSim-Local Implementation](../populationsim/implementation-notes.md)

---

*Document Status: Planning - Subject to revision during implementation*
