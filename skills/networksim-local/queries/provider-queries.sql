-- NetworkSim-Local: Provider Query Templates
-- For use with DuckDB database

-- ============================================================
-- BASIC LOOKUPS
-- ============================================================

-- Lookup provider by NPI
SELECT 
    npi,
    entity_type_code,
    COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
    credential,
    taxonomy_code,
    practice_address_1,
    practice_city,
    practice_state,
    practice_zip,
    practice_phone
FROM providers 
WHERE npi = ?;  -- Parameter: NPI (10-digit string)


-- Search providers by name (organization)
SELECT 
    npi,
    organization_name,
    taxonomy_code,
    practice_city,
    practice_state
FROM providers 
WHERE entity_type_code = '2'
  AND organization_name ILIKE '%' || ? || '%'
LIMIT 50;  -- Parameter: search term


-- Search providers by name (individual)
SELECT 
    npi,
    last_name,
    first_name,
    credential,
    taxonomy_code,
    practice_city,
    practice_state
FROM providers 
WHERE entity_type_code = '1'
  AND (last_name ILIKE ? || '%' OR first_name ILIKE ? || '%')
LIMIT 50;  -- Parameters: last name, first name


-- ============================================================
-- GEOGRAPHIC SEARCHES
-- ============================================================

-- Providers by state
SELECT 
    npi,
    COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
    credential,
    taxonomy_code,
    practice_city,
    practice_zip
FROM providers 
WHERE practice_state = ?
LIMIT 100;  -- Parameter: state code (e.g., 'CA')


-- Providers by city and state
SELECT 
    npi,
    COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
    credential,
    taxonomy_code,
    practice_address_1,
    practice_zip,
    practice_phone
FROM providers 
WHERE practice_city ILIKE ?
  AND practice_state = ?
LIMIT 100;  -- Parameters: city, state


-- Providers by ZIP code (prefix match for area)
SELECT 
    npi,
    COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
    credential,
    taxonomy_code,
    practice_city,
    practice_zip,
    practice_phone
FROM providers 
WHERE practice_zip LIKE ? || '%'
LIMIT 100;  -- Parameter: ZIP prefix (e.g., '921' for San Diego area)


-- ============================================================
-- SPECIALTY SEARCHES
-- ============================================================

-- Providers by taxonomy code (exact)
SELECT 
    npi,
    COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
    credential,
    taxonomy_code,
    practice_city,
    practice_state,
    practice_phone
FROM providers 
WHERE taxonomy_code = ?
LIMIT 100;  -- Parameter: taxonomy code (e.g., '207RC0000X')


-- Providers by taxonomy prefix (specialty group)
SELECT 
    npi,
    COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
    credential,
    taxonomy_code,
    practice_city,
    practice_state
FROM providers 
WHERE taxonomy_code LIKE ? || '%'
LIMIT 100;  -- Parameter: taxonomy prefix (e.g., '207R' for internal medicine)


-- Providers by specialty in location
SELECT 
    npi,
    COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
    credential,
    taxonomy_code,
    practice_address_1,
    practice_city,
    practice_zip,
    practice_phone
FROM providers 
WHERE taxonomy_code LIKE ? || '%'
  AND practice_state = ?
ORDER BY practice_city
LIMIT 100;  -- Parameters: taxonomy prefix, state


-- ============================================================
-- FACILITY SEARCHES
-- ============================================================

-- Hospitals by state
SELECT 
    npi,
    organization_name,
    taxonomy_code,
    practice_address_1,
    practice_city,
    practice_zip,
    practice_phone
FROM providers 
WHERE taxonomy_code LIKE '282%'  -- Hospital taxonomy codes
  AND practice_state = ?
ORDER BY organization_name;  -- Parameter: state


-- Pharmacies by location
SELECT 
    npi,
    organization_name,
    taxonomy_code,
    practice_address_1,
    practice_city,
    practice_zip,
    practice_phone
FROM providers 
WHERE taxonomy_code LIKE '3336%'  -- Pharmacy taxonomy codes
  AND practice_city ILIKE ?
  AND practice_state = ?
ORDER BY organization_name;  -- Parameters: city, state


-- Clinics by type and location
SELECT 
    npi,
    organization_name,
    taxonomy_code,
    practice_address_1,
    practice_city,
    practice_zip,
    practice_phone
FROM providers 
WHERE taxonomy_code LIKE '261Q%'  -- Clinic taxonomy codes
  AND practice_state = ?
ORDER BY practice_city, organization_name;  -- Parameter: state


-- ============================================================
-- ANALYTICS QUERIES
-- ============================================================

-- Provider count by state
SELECT 
    practice_state,
    COUNT(*) as provider_count
FROM providers
GROUP BY practice_state
ORDER BY provider_count DESC;


-- Provider count by category
SELECT 
    provider_category,
    COUNT(*) as count
FROM provider_categories
GROUP BY provider_category
ORDER BY count DESC;


-- Specialty distribution in a state
SELECT 
    taxonomy_code,
    COUNT(*) as count
FROM providers
WHERE practice_state = ?
GROUP BY taxonomy_code
ORDER BY count DESC
LIMIT 20;  -- Parameter: state


-- Providers by city (top cities in state)
SELECT 
    practice_city,
    COUNT(*) as provider_count
FROM providers
WHERE practice_state = ?
GROUP BY practice_city
ORDER BY provider_count DESC
LIMIT 20;  -- Parameter: state


-- ============================================================
-- CROSS-PRODUCT INTEGRATION QUERIES
-- ============================================================

-- Random provider for PatientSim (attending physician)
SELECT 
    npi,
    last_name,
    first_name,
    credential,
    taxonomy_code,
    practice_city,
    practice_state
FROM providers 
WHERE entity_type_code = '1'  -- Individual
  AND taxonomy_code LIKE '207%'  -- Physician
  AND practice_state = ?
ORDER BY RANDOM()
LIMIT 1;  -- Parameter: state


-- Random pharmacy for RxMemberSim
SELECT 
    npi,
    organization_name,
    practice_address_1,
    practice_city,
    practice_state,
    practice_zip,
    practice_phone
FROM providers 
WHERE taxonomy_code LIKE '3336%'  -- Pharmacy
  AND practice_zip LIKE ? || '%'
ORDER BY RANDOM()
LIMIT 1;  -- Parameter: ZIP prefix


-- Random hospital for MemberSim claim
SELECT 
    npi,
    organization_name,
    practice_address_1,
    practice_city,
    practice_state,
    practice_zip,
    practice_phone
FROM providers 
WHERE taxonomy_code LIKE '282N%'  -- General acute care hospital
  AND practice_state = ?
ORDER BY RANDOM()
LIMIT 1;  -- Parameter: state
