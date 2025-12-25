-- NetworkSim-Local Query Templates
-- These queries work with the DuckDB database built from NPPES data

--------------------------------------------------------------------------------
-- PROVIDER LOOKUP QUERIES
--------------------------------------------------------------------------------

-- Lookup provider by NPI
-- Usage: Replace :npi with actual NPI value
SELECT 
    npi,
    entity_type_code,
    CASE WHEN entity_type_code = 1 THEN 
        CONCAT(first_name, ' ', last_name, COALESCE(', ' || credential, ''))
    ELSE organization_name END as provider_name,
    taxonomy_code,
    practice_address_1,
    practice_city,
    practice_state,
    practice_zip,
    practice_phone
FROM providers 
WHERE npi = :npi;


-- Lookup provider with category
SELECT p.*, pc.provider_category
FROM providers p
JOIN provider_categories pc ON p.npi = pc.npi
WHERE p.npi = :npi;


--------------------------------------------------------------------------------
-- GEOGRAPHIC QUERIES
--------------------------------------------------------------------------------

-- Providers by state
SELECT * FROM providers 
WHERE practice_state = :state
LIMIT 100;


-- Providers by city and state
SELECT * FROM providers
WHERE practice_city = :city 
  AND practice_state = :state
ORDER BY last_name, first_name
LIMIT 100;


-- Providers by ZIP code (exact or prefix)
SELECT * FROM providers
WHERE practice_zip LIKE :zip_pattern  -- e.g., '90210' or '902%'
LIMIT 100;


-- Provider count by state
SELECT 
    practice_state,
    COUNT(*) as provider_count
FROM providers
GROUP BY practice_state
ORDER BY provider_count DESC;


--------------------------------------------------------------------------------
-- SPECIALTY/TAXONOMY QUERIES
--------------------------------------------------------------------------------

-- Providers by taxonomy code
SELECT * FROM providers
WHERE taxonomy_code = :taxonomy_code
AND practice_state = :state
LIMIT 100;


-- Providers by category (using view)
SELECT * FROM provider_categories
WHERE provider_category = :category  -- e.g., 'Physician (Allopathic)'
AND practice_state = :state
LIMIT 100;


-- Find pharmacies in a ZIP code area
SELECT * FROM providers
WHERE taxonomy_code LIKE '3336%'  -- All pharmacy types
AND practice_zip LIKE :zip_prefix  -- e.g., '100%' for NYC
LIMIT 50;


-- Find hospitals by state
SELECT * FROM providers
WHERE taxonomy_code LIKE '282%'  -- All hospital types
AND practice_state = :state;


-- Specialty distribution by state
SELECT 
    pc.provider_category,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM provider_categories pc
WHERE pc.practice_state = :state
GROUP BY pc.provider_category
ORDER BY count DESC;


--------------------------------------------------------------------------------
-- ENTITY TYPE QUERIES
--------------------------------------------------------------------------------

-- Individual providers (Type 1) only
SELECT * FROM providers
WHERE entity_type_code = 1
AND practice_state = :state
LIMIT 100;


-- Organizations (Type 2) only
SELECT * FROM providers
WHERE entity_type_code = 2
AND practice_state = :state
LIMIT 100;


-- Entity type distribution
SELECT 
    CASE entity_type_code 
        WHEN 1 THEN 'Individual'
        WHEN 2 THEN 'Organization'
    END as entity_type,
    COUNT(*) as count
FROM providers
GROUP BY entity_type_code;


--------------------------------------------------------------------------------
-- STATISTICAL QUERIES
--------------------------------------------------------------------------------

-- Provider counts by category
SELECT 
    provider_category,
    COUNT(*) as count
FROM provider_categories
GROUP BY provider_category
ORDER BY count DESC;


-- Top cities by provider count
SELECT 
    practice_city,
    practice_state,
    COUNT(*) as provider_count
FROM providers
GROUP BY practice_city, practice_state
ORDER BY provider_count DESC
LIMIT 20;


-- Recently updated providers
SELECT * FROM providers
WHERE last_update_date >= :since_date
ORDER BY last_update_date DESC
LIMIT 100;


--------------------------------------------------------------------------------
-- METADATA QUERIES
--------------------------------------------------------------------------------

-- Database load information
SELECT * FROM load_metadata;


-- Total record count
SELECT COUNT(*) as total_providers FROM providers;


-- Database summary
SELECT 
    (SELECT value FROM load_metadata WHERE key = 'load_date') as load_date,
    (SELECT value FROM load_metadata WHERE key = 'source_file') as source_file,
    (SELECT COUNT(*) FROM providers) as total_providers,
    (SELECT COUNT(*) FROM providers WHERE entity_type_code = 1) as individuals,
    (SELECT COUNT(*) FROM providers WHERE entity_type_code = 2) as organizations;
