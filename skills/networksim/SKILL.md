---
name: networksim
description: Healthcare provider network data generation and analysis using real NPPES, CMS, and HRSA data
version: 2.0.0
status: active
---

# NetworkSim Master Skill

## Overview

**NetworkSim** provides comprehensive healthcare provider network data including individual providers, facilities, pharmacies, and quality metrics. Built on real CMS National Provider Identifier (NPI) Registry data with 8.9M active US providers, Medicare Provider of Services data with 77K facilities, and CMS quality ratings.

**Key Capabilities**:
- Search providers by specialty, location, and credentials
- Find healthcare facilities with bed counts and quality ratings
- Locate pharmacies by type and geography
- Analyze provider density and network adequacy
- Cross-reference with population health data (PopulationSim)

**Data Sources**:
- **NPPES**: 8.9M providers (97.77% with county FIPS)
- **Provider of Services**: 77K facilities across all types
- **Hospital Compare**: 5.4K hospitals with CMS star ratings
- **Physician Compare**: 1.5M physicians with quality metrics
- **AHRF**: County-level healthcare resource data

---

## Trigger Phrases

NetworkSim activates when users request provider or network data:

- "Find [specialty] providers in [location]"
- "Search for hospitals near [ZIP code]"
- "Locate pharmacies in [county]"
- "Show me provider networks in [state]"
- "Analyze provider density in [region]"
- "Find facilities with [beds] beds"
- "Search for [quality rating]-star hospitals"

---

## Product Architecture

### Data Organization

NetworkSim data is stored in the `network` schema of `healthsim.duckdb`:

```
network/
├── providers          (8.9M records)  - Individual + organizational providers
├── facilities         (77K records)   - Hospitals, nursing homes, clinics
├── hospital_quality   (5.4K records)  - CMS Hospital Compare ratings
├── physician_quality  (1.5M records)  - CMS Physician Compare metrics
└── ahrf_county        (3K records)    - Area Health Resources Files
```

### Cross-Product Integration

NetworkSim integrates with other HealthSim products:

**PopulationSim**: Geographic JOIN via county_fips for demographic analysis
**PatientSim**: Assign providers to patient encounters by specialty/location
**MemberSim**: Build provider networks for health plan claims  
**RxMemberSim**: Link prescriptions to pharmacy locations
**TrialSim**: Identify trial sites and recruiting physicians

---

## Query Skills

### Provider & Facility Search

**[provider-search](query/provider-search.md)** - Search for healthcare providers
- Find providers by specialty, location, credentials
- Filter by taxonomy codes (207Q*, 208D*, 332*, etc.)
- Search individual practitioners or organizations
- Cross-reference with demographic data

**[facility-search](query/facility-search.md)** - Search for healthcare facilities
- Find hospitals, nursing homes, clinics by location
- Filter by bed count, ownership type, facility type
- Join with quality ratings from Hospital Compare
- Analyze facility distribution

**[pharmacy-search](query/pharmacy-search.md)** - Search for retail and specialty pharmacies
- Find pharmacies by type (retail, specialty, mail-order)
- Search by geography (state, county, ZIP)
- Analyze pharmacy density and access
- Integration with RxMemberSim for prescription fills

### Network Analysis (Complete - Session 6) ✅

**[npi-validation](query/npi-validation.md)** - Validate NPI format and checksums
- Validate 10-digit NPIs using Luhn algorithm
- Batch validation for multiple NPIs
- Provider lookup by NPI with full details
- Python implementation with checksum validation

**[network-roster](query/network-roster.md)** - Generate provider network rosters
- Create rosters from search criteria
- Multi-specialty network development
- Export to CSV, JSON, Excel formats
- Network adequacy metrics integration

**[provider-density](query/provider-density.md)** - Calculate provider-to-population ratios
- Density calculations per 100K population
- Compare to HRSA and industry benchmarks
- Healthcare desert identification
- Multi-specialty distribution analysis

**[coverage-analysis](query/coverage-analysis.md)** - Analyze network adequacy and gaps
- CMS/NCQA compliance assessment
- Specialty gap analysis
- Network adequacy scoring
- Recruitment priority identification

### Quality-Based Queries (Complete - Session 7) ✅

**[hospital-quality-search](query/hospital-quality-search.md)** - Search hospitals by CMS star ratings
- Filter by 1-5 star ratings or "Not Available"
- Quality tier network development (Premium/Preferred/Standard)
- Geographic quality distribution analysis
- Quality gap identification by county

**[physician-quality-search](query/physician-quality-search.md)** - Search physicians by quality indicators
- Credential-based filtering (MD, DO, NP, PA)
- Specialty board certification inference
- Hospital affiliation quality proxies
- Framework for MIPS/satisfaction metrics

### Advanced Analytics (Coming Soon - Session 8)

**network-adequacy** - Calculate time/distance network adequacy
**healthcare-deserts** - Identify underserved areas
**specialty-distribution** - Analyze specialty mix by geography
**provider-demographics** - Analyze provider workforce characteristics

---

## Data Standards

NetworkSim supports multiple healthcare data standards:

### Provider Identifiers
- **NPI**: 10-digit National Provider Identifier (primary key)
- **Taxonomy Codes**: NUCC Healthcare Provider Taxonomy (332*, 207*, 163*, etc.)
- **State License Numbers**: Where available

### Facility Identifiers
- **CCN**: CMS Certification Number (6 characters)
- **Facility Type Codes**: POS file type codes (01=Hospital, 21=SNF, etc.)

### Quality Metrics
- **Hospital Star Ratings**: 1-5 scale from CMS Hospital Compare
- **MIPS Scores**: Merit-based Incentive Payment System scores

### Geographic Standards
- **County FIPS**: 5-digit Federal Information Processing Standard codes
- **State Codes**: 2-letter USPS abbreviations
- **ZIP Codes**: 5 or 9-digit postal codes

---

## Common Workflows

### Workflow 1: Build Primary Care Network for Texas

```markdown
1. Find PCPs in target counties (provider-search)
2. Filter by quality metrics (physician-quality-search)
3. Generate network roster (network-roster)
4. Analyze coverage adequacy (coverage-analysis)
5. Export to standard format (network-export)
```

### Workflow 2: Identify Healthcare Deserts

```markdown
1. Calculate provider density by county (provider-density)
2. Cross-reference with diabetes prevalence (PopulationSim)
3. Identify high-need, low-access areas (healthcare-deserts)
4. Find nearest facilities (facility-search)
5. Generate gap analysis report
```

### Workflow 3: Pharmacy Network Development

```markdown
1. Find retail pharmacies by geography (pharmacy-search)
2. Analyze pharmacy density (provider-density)
3. Identify specialty pharmacy capabilities
4. Build network roster (network-roster)
5. Integrate with prescription data (RxMemberSim)
```

---

## Data Quality

### Geographic Coverage
- **97.77% county FIPS coverage** for providers (8.7M of 8.9M)
- Missing FIPS primarily: military addresses (APO/FPO), PO Box-only
- **3,213 counties covered** (100% of PopulationSim + 70 additional)

### Provider Data Quality
- **NPI format**: 100% valid (10 digits)
- **Entity types**: 85% Individual (Type 1), 15% Organization (Type 2)
- **Taxonomy codes**: 99%+ have primary taxonomy (taxonomy_1)
- **No duplicate NPIs**: Verified via automated testing

### Facility Data Quality
- **77,302 facilities** across all types
- **7% have quality ratings** (hospitals only)
- **Bed counts**: Available for hospitals and nursing homes
- **Missing county_fips**: Facility table needs geographic enrichment

### Known Limitations
- Gender field not populated in current data
- Some specialty taxonomies incomplete
- Facilities lack direct county FIPS (use city/state or provider linkage)

---

## Performance Benchmarks

All benchmarks measured on MacBook Pro with 1.65 GB database:

| Query Type | Avg Time | Notes |
|------------|----------|-------|
| Provider count | <100ms | Simple filters |
| Geographic + specialty | 200-500ms | With county JOIN |
| Cross-product analytics | 500ms-1s | Population + network |
| Pharmacy density | 20-50ms | Taxonomy filter |
| Facility quality JOIN | 200-400ms | Hospital Compare |
| Full test suite (12 tests) | <200ms | Average 13.8ms/test |

**Optimization Tips**:
- Filter by taxonomy_1 early for specialty searches
- Use county_fips instead of city names
- Add entity_type_code to WHERE clause
- LIMIT results appropriately

---

## Validation & Testing

NetworkSim includes comprehensive automated testing:

**Test Suite**: `scenarios/networksim/tests/test_data_quality.py`
- 18 tests covering provider data, geography, facilities, quality metrics
- Tests run in <1 second
- All tests passing (100% success rate)

**Search Skills Tests**: `scenarios/networksim/scripts/test_search_skills.py`
- 12 end-to-end query tests
- Validates all search patterns from skill documentation
- Performance benchmarks included

Run tests:
```bash
cd scenarios/networksim
pytest tests/
python scripts/test_search_skills.py
```

---

## Related Skills

### HealthSim Core
- **[healthsim-master](../healthsim-master-SKILL.md)** - HealthSim platform overview
- **[populationsim](../populationsim/SKILL.md)** - Demographic and SDOH data

### Other Products
- **[patientsim](../patientsim/SKILL.md)** - Assign providers to encounters
- **[membersim](../membersim/SKILL.md)** - Claims with network providers
- **[rxmembersim](../rxmembersim/SKILL.md)** - Pharmacy fills
- **[trialsim](../trialsim/SKILL.md)** - Trial site selection

---

## Development Status

**Version**: 2.0.0  
**Status**: Phase 2 Complete (Query Skills), Phase 3 Ready

### Phase 1: Data Infrastructure ✅ Complete
- [x] Session 1-3: NPPES data acquisition and import (8.9M providers)
- [x] Session 4: Geographic enrichment and validation (97.77% coverage)

### Phase 2: Query Skills Development ✅ Complete
- [x] Session 5: Provider & facility search skills ✅
- [x] Session 6: Network & analysis skills ✅
- [x] Session 7: Quality-based query skills ✅

### Phase 3: Integration & Advanced Analytics
- [ ] Session 8-10: Advanced analysis skills
- [ ] Session 11-12: Cross-product integration

### Future Enhancements
1. Add taxonomy_codes reference table for human-readable specialty names
2. Enrich facilities table with county_fips for better geographic JOINs
3. Geospatial capabilities using DuckDB spatial extensions
4. Historical quality trend analysis using multi-year CMS data
5. Provider-facility linkage via NPI relationships
6. Distance calculations for radius-based searches

---

## Documentation

**Architecture**: `docs/NETWORKSIM-ARCHITECTURE.md`  
**Master Plan**: `docs/NETWORKSIM-V2-MASTER-PLAN.md`  
**Data README**: `scenarios/networksim/DATA-README.md`  
**Session Reports**: `scenarios/networksim/SESSION-*-SUMMARY.md`

---

## Support & Feedback

NetworkSim is part of the HealthSim open-source project.

**GitHub**: [healthsim-workspace](https://github.com/mark64oswald/healthsim-workspace)  
**Issues**: Report bugs or request features via GitHub Issues  
**Contact**: mark@rewirehealth.com

---

*Last Updated: December 27, 2025*  
*Version: 2.0.0 - Phase 1 Complete*
