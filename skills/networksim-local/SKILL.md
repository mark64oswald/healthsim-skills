---
name: NetworkSim-Local
description: Real-world provider data lookup using NPPES NPI Registry. Query actual provider NPIs, addresses, specialties from local DuckDB database. Triggers include "real provider", "NPPES lookup", "actual NPI", "real NPI", "provider database", "lookup provider", "find real provider".
version: 0.1.0
status: development
category: data-lookup
---

# NetworkSim-Local

Real-world provider data from the NPPES NPI Registry stored in a local DuckDB database.

## Overview

NetworkSim-Local provides access to **actual provider data** from CMS's National Plan and Provider Enumeration System (NPPES). Unlike NetworkSim (which generates synthetic providers), this product queries real NPI records.

**Key Capabilities**:
- Look up real providers by NPI
- Search providers by geography (state, city, ZIP)
- Filter by specialty/taxonomy
- Access actual practice addresses and phone numbers
- Query ~7 million active US providers

## Trigger Phrases

- "Look up real provider..."
- "Find actual NPI for..."
- "NPPES lookup..."
- "Search real providers in..."
- "What's the real NPI for..."
- "Find providers in [city/state] from NPPES"
- "Query the provider database for..."

## Data Source

| Attribute | Value |
|-----------|-------|
| Source | CMS NPPES NPI Registry |
| Records | ~7 million active US providers |
| Update Frequency | Monthly |
| Storage | Local DuckDB (~200 MB) |

## Quick Examples

### Provider Lookup by NPI
```
User: "Look up NPI 1234567890 from NPPES"

Response: "From the NPPES registry:
- Provider: John Smith, MD
- NPI: 1234567890
- Specialty: Internal Medicine (207R00000X)
- Practice: 123 Medical Center Dr, Boston, MA 02101
- Phone: (617) 555-1234"
```

### Geographic Search
```
User: "Find cardiologists in San Diego from NPPES"

Response: "NPPES shows 847 cardiologists in San Diego, CA.
Here are the first 10:
1. Dr. Maria Garcia, MD - 207RC0000X - La Jolla
2. Dr. James Chen, MD - 207RC0000X - Downtown
..."
```

### Pharmacy Lookup
```
User: "Find real pharmacies near ZIP 10001"

Response: "NPPES shows 156 pharmacies in the 10001 ZIP area:
1. CVS Pharmacy #1234 - NPI: 1234567890 - 42nd St
2. Walgreens #5678 - NPI: 0987654321 - 34th St
..."
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `npi` | string | For lookup | 10-digit NPI to look up |
| `state` | string | For geo search | 2-letter state code |
| `city` | string | Optional | City name |
| `zip` | string | Optional | ZIP code (5-digit or prefix) |
| `taxonomy` | string | Optional | Provider taxonomy code |
| `category` | string | Optional | Provider category (Physician, Hospital, etc.) |
| `limit` | integer | Optional | Max results (default: 20) |

## Provider Categories

The database includes these provider types:

| Category | Taxonomy Prefix | Example |
|----------|-----------------|---------|
| Physician (Allopathic) | 207%, 208% | Internal Medicine, Cardiology |
| Physician (Osteopathic) | 204% | Family Medicine DO |
| Nurse Practitioner | 363L% | Adult NP, Family NP |
| Physician Assistant | 363A% | Medical PA |
| Pharmacy | 3336% | Retail, Mail Order, Specialty |
| Hospital | 282% | General Acute, Psychiatric |
| Clinic | 261Q% | Urgent Care, Mental Health |
| DME Supplier | 332% | Medical Equipment |

## Setup Requirements

**Prerequisites**: DuckDB database must be built from NPPES data.

1. Download NPPES: https://download.cms.gov/nppes/NPI_Files.html
2. Extract to: `skills/networksim-local/data/raw/nppes/`
3. Run: `python setup/build-database.py`

See [developer-guide.md](developer-guide.md) for detailed setup.

## Integration with HealthSim

NetworkSim-Local provides real NPIs that can be referenced by:

- **PatientSim**: Use real provider NPIs in encounter records
- **MemberSim**: Reference actual provider networks
- **RxMemberSim**: Link prescriptions to real pharmacies
- **PopulationSim**: Correlate provider density with population data

## Provenance

All responses from NetworkSim-Local include data source attribution:

- ✓ "From NPPES registry (as of [date])"
- ✓ Real NPI, verified format
- ✓ Actual practice address
- ✓ Taxonomy code from registry

## Limitations

- Data is as current as last NPPES download (monthly refresh)
- No prescription/claims history (just provider registration)
- Deactivated providers are excluded
- Non-US providers are excluded

## Related Skills

- [provider-lookup.md](skills/provider-lookup.md) - Detailed provider lookup
- [geographic-analysis.md](skills/geographic-analysis.md) - Provider distribution analysis
- [pharmacy-lookup.md](skills/pharmacy-lookup.md) - Pharmacy-specific queries

## See Also

- [NetworkSim](../networksim/SKILL.md) - Synthetic provider generation (parallel implementation)
- [PopulationSim](../populationsim/SKILL.md) - Geographic and demographic data
