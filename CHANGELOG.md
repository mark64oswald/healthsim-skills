# Changelog

All notable changes to healthsim-common (Skills repository) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- **[Packages]** Package dependency alignment (2025-12-25)
  - Renamed packages/core from `healthsim-common` to `healthsim-core` to match dependency references
  - Updated membersim, patientsim, rxmembersim to use `healthsim-core>=1.0.0`
  - Removed git+ remote references in favor of local package references
  - All 1,289 tests now passing (476 core + 447 patientsim + 190 membersim + 176 rxmembersim)

- **[PopulationSim]** CSV data file parsing issues (2024-12-25)
  - Removed UTF-8 BOM from `svi_tract_2022.csv` that corrupted first column header
  - Cleaned `adi_blockgroup_2023.csv`: removed R export index column and unnecessary quotes
  - All 9 data files now have consistent, clean header formatting

### Changed

- **[Hello-HealthSim]** Consolidated PopulationSim examples (2025-12-25)
  - Removed redundant `hello-healthsim/populationsim/` folder (1,386 lines)
  - Enhanced `populationsim-examples.md` with v2.0 data-first information
  - All products now use consistent `examples/product-examples.md` pattern

- **[NetworkSim]** Post-implementation polish (2024-12-24)
  - Updated root README.md: NetworkSim status changed from "planned" to active
  - Added NetworkSim cross-product section to RxMemberSim SKILL.md
  - Verified all cross-product references in place across ecosystem

### Added

- **[Docs]** Documentation completeness improvements (2025-12-25)
  - Created `formats/README.md` - Index of all 15 output format files
  - Created `packages/core/CLAUDE.md` - Claude context for core package
  - Comprehensive audit report: `docs/archive/audits/COMPREHENSIVE-AUDIT-2025-12-25.md`
  - Removed duplicate skill templates from `docs/skills/`

- **[NetworkSim]** Phase 1 Complete - Foundation and Reference Knowledge (2024-12-24)
  - Directory structure: `skills/networksim/` with reference/, synthetic/, patterns/, integration/ subdirectories
  - Core documentation:
    - `SKILL.md` - Master router with all skill categories (~280 lines)
    - `README.md` - Comprehensive product overview with examples (~450 lines)
    - `developer-guide.md` - Shell with Quick Start complete
    - `prompt-guide.md` - Shell with Reference section complete
  - Reference skills (7 total, ~2,200 lines):
    - `network-types.md` - HMO, PPO, EPO, POS, HDHP definitions and comparisons
    - `plan-structures.md` - Deductibles, copays, coinsurance, OOP max, accumulators
    - `pharmacy-benefit-concepts.md` - Tier structures, formulary types, pharmacy networks
    - `pbm-operations.md` - Claims processing, BIN/PCN routing, rebates
    - `utilization-management.md` - Prior authorization, step therapy, quantity limits
    - `specialty-pharmacy.md` - Hub model, REMS, limited distribution
    - `network-adequacy.md` - Time/distance standards, provider ratios, ECPs
  - Updated master `SKILL.md` with NetworkSim scenarios table (status: Active)
  - Total Phase 1: ~3,450 lines of content

- **[NetworkSim]** Phase 2 Complete - Synthetic Generation Skills (2024-12-24)
  - Created `skills/networksim/synthetic/` directory with 6 generation skills:
    - `synthetic-provider.md` (~480 lines) - Provider entities with NPI, credentials, taxonomy
      - Canonical JSON schema for individual and organizational providers
      - Common taxonomy codes by specialty (Primary Care, Cardiology, Orthopedics, Oncology, Mental Health, Emergency)
      - NPI generation with Luhn algorithm validation
      - 4 examples: basic cardiologist, interventional specialist, nurse practitioner, group practice
      - Cross-product integration patterns for PatientSim, MemberSim, RxMemberSim, TrialSim
    - `synthetic-facility.md` (~500 lines) - Facility entities with CCN, beds, services
      - Facility types: Acute Care, Critical Access, Psychiatric, SNF, ASC, ESRD, RHC/FQHC
      - CCN generation rules by state and facility type
      - 4 examples: urban teaching hospital, critical access, ASC, skilled nursing facility
      - Hospital characteristics: ownership, teaching status, trauma level, accreditation
    - `synthetic-pharmacy.md` (~520 lines) - Pharmacy entities with NCPDP, DEA, services
      - Pharmacy types: Retail (chain, grocery, mass merchant, independent), Specialty, Mail-Order, Institutional
      - NCPDP Provider ID and DEA number generation with validation
      - 4 examples: retail chain (CVS), oncology specialty, independent rural, PBM mail-order
      - Specialty pharmacy services: clinical management, hub services, REMS certification
    - `synthetic-network.md` (~400 lines) - Network configurations with rosters
      - Network types by access model (HMO, PPO, EPO, POS) and breadth (Broad, Standard, Narrow)
      - Tier structure configuration (1-4 tiers with quality/cost criteria)
      - 4 examples: standard PPO, tiered HMO, narrow ACA Exchange, Medicare Advantage
      - Adequacy standards and provider count tracking
    - `synthetic-plan.md` (~550 lines) - Plan benefit structures
      - Market segments: Commercial, Exchange (metal tiers), Medicare, Medicaid
      - Complete cost sharing schemas (deductibles, copays, coinsurance, OOP max)
      - Medical benefits by service type with cost sharing rules
      - 4 examples: commercial PPO, HDHP with HSA, ACA Silver, Medicare Advantage
      - HSA/HRA eligibility, CSR variants, Part D benefit phases
    - `synthetic-pharmacy-benefit.md` (~550 lines) - Pharmacy benefit designs
      - Tier structures (2-6 tier configurations with cost sharing models)
      - Clinical programs: Prior Authorization, Step Therapy, Quantity Limits, DUR
      - Specialty programs: biosimilar, copay assistance, site of care
      - Part D specific schema with benefit phases and LIS status
      - 4 examples: standard 4-tier, Part D, HDHP-compatible, specialty-focused
  - All skills include:
    - YAML frontmatter with name, description, trigger phrases, cross-product references
    - Canonical JSON schemas with field definitions
    - Generation parameters (required and optional)
    - 4+ comprehensive examples at varying complexity levels
    - Cross-product integration patterns
    - Validation rules tables
  - Total Phase 2: ~3,000 lines of content

- **[NetworkSim]** Phase 5 Complete - Documentation and Examples (2024-12-24)
  - Completed `skills/networksim/developer-guide.md` (~650 lines)
    - Core Concepts: Network Types, Provider Taxonomy, Facility Types, Pharmacy Classification
    - All 4 Common Workflows with diagrams and examples
    - Complete Output Formats with full JSON schemas
    - All 5 Integration Points documented
    - 8 Best Practices with examples
    - Troubleshooting guide with common issues
  - Completed `skills/networksim/prompt-guide.md` (~700 lines)
    - 30+ Reference Knowledge prompts (6 categories)
    - 25+ Synthetic Generation prompts (providers, facilities, pharmacies, networks)
    - 15+ Cross-Product Integration prompts (all 5 products)
    - Advanced multi-entity and network analysis prompts
    - Tips for effective prompting with examples
  - Created `hello-healthsim/examples/networksim-examples.md` (~400 lines)
    - Quick reference examples for all skill categories
    - Cross-product integration examples
    - Network pattern examples
  - Updated `hello-healthsim/examples/README.md`
    - Added Level 2.7 for NetworkSim
    - Added NetworkSim to product table
    - Added provider network prompts to quick reference
  - Total Phase 5: ~1,750 lines of documentation

- **[NetworkSim]** Phase 4 Complete - Integration Skills (2024-12-24)
  - Created `skills/networksim/integration/` directory with 5 integration skills:
    - `README.md` - Integration architecture and usage guide
    - `provider-for-encounter.md` (~450 lines) - PatientSim/TrialSim provider generation
      - Diagnosis-to-specialty mapping
      - Procedure-to-specialty mapping
      - Provider role assignment (Attending, Consulting, Proceduralist)
      - Examples: HF admission, orthopedic surgery, ED visit, trial PI
    - `network-for-member.md` (~500 lines) - MemberSim network status determination
      - Network lookup and tier assignment
      - In-network/out-of-network determination
      - Tiered network cost sharing
      - Emergency exception handling (No Surprises Act)
      - Examples: PPO in-network, tiered preferred, HMO OON denied
    - `pharmacy-for-rx.md` (~480 lines) - RxMemberSim pharmacy routing
      - Specialty vs retail routing logic
      - Mail order eligibility
      - Limited distribution pharmacy assignment
      - REMS compliance verification
      - Examples: acute retail, maintenance mail, oncology specialty, REMS drug
    - `benefit-for-claim.md` (~550 lines) - MemberSim/RxMemberSim cost sharing
      - Deductible, copay, coinsurance calculation
      - Accumulator tracking and updates
      - OOP max application
      - Service-type cost sharing rules
      - Examples: copay visit, deductible lab, inpatient, OON, preventive
    - `formulary-for-rx.md` (~520 lines) - RxMemberSim formulary coverage
      - Formulary status and tier lookup
      - Prior authorization criteria by drug class
      - Step therapy protocol application
      - Quantity limit enforcement
      - Examples: generic covered, brand ST, specialty PA, excluded drug
  - All integration skills include:
    - Cross-product input/output contracts
    - Decision trees and routing logic
    - Complete adjudication examples
    - Validation rules
  - Total Phase 4: ~2,500 lines of content

- **[NetworkSim]** Phase 3 Complete - Pattern/Template Skills (2024-12-24)
  - Created `skills/networksim/patterns/` directory with 5 pattern skills:
    - `README.md` - Category overview and pattern usage guide
    - `hmo-network-pattern.md` (~450 lines) - HMO/Gatekeeper model templates
      - Pattern variants: Staff Model, Group Model, IPA Model, Network Model
      - Base template with PCP requirements, referral configuration
      - PCP payment and panel management templates
      - Complete Medicare Advantage HMO example
    - `ppo-network-pattern.md` (~500 lines) - PPO/Open access templates
      - Pattern variants: Standard PPO, Value PPO, Premium PPO, National PPO
      - In-network/out-of-network cost sharing templates
      - UCR vs Medicare-based reimbursement patterns
      - Complete commercial PPO example (Illinois)
    - `tiered-network-pattern.md` (~550 lines) - Quality/cost tiered networks
      - Tiering approaches: Quality-Based, Cost-Based, Hybrid
      - Network breadth patterns: Broad, Standard, Narrow, Ultra-Narrow
      - ACA Exchange network pattern with ECP requirements
      - Centers of Excellence pattern (transplant, bariatric, orthopedic, cardiac, cancer)
      - Complete Texas large employer tiered network example
    - `pharmacy-benefit-patterns.md` (~600 lines) - Tier structures and formularies
      - Tier patterns: 2-tier through 6-tier configurations
      - Cost sharing models: Copay-only, Coinsurance, Hybrid, HDHP/HSA
      - Formulary approaches: Open, Incentive, Closed, Exclusion List
      - Clinical program templates: Standard and Enhanced
      - Complete large employer 4-tier example
    - `specialty-distribution-pattern.md` (~550 lines) - Specialty pharmacy distribution
      - Distribution models: Open, Limited, Exclusive
      - Hub patterns: Full-Service, Limited (BI/PA), Hub + Dispensing
      - Site-of-care patterns: Buy and Bill, White Bagging, Home Infusion, AIC
      - Site-of-care optimization program template
      - REMS distribution pattern with certification requirements
      - Complete oncology drug distribution example
  - All patterns include:
    - Multiple variants for common sub-types
    - JSON templates with placeholders
    - Complete configuration examples
    - Validation checklists
    - Cross-references to related skills
  - Total Phase 3: ~2,650 lines of content

- **[NetworkSim-Local]** Planning Documentation Complete (2024-12-24)
  - Created `docs/networksim-local/` directory with comprehensive planning:
    - `README.md` - Overview and document index
    - `NETWORKSIM-LOCAL-PROJECT-REQUIREMENTS.md` - Functional/non-functional requirements
    - `NETWORKSIM-LOCAL-DATA-ARCHITECTURE.md` - DuckDB schema, MCP tools, PopulationSim integration
    - `NETWORKSIM-LOCAL-DATA-SOURCES.md` - NPPES, CMS POS, NCPDP, geocoding sources
    - `NETWORKSIM-LOCAL-IMPLEMENTATION-PLAN.md` - 5-phase implementation plan (4-6 weeks)
  - Total planning documentation: ~2,400 lines
  - Ready for implementation after NetworkSim skills complete

### Changed

- **[PopulationSim]** Trial Support Skills v2.0 Update (2024-12-24)
  - Updated all trial-support skills with embedded data references:
    - `feasibility-estimation.md` - Added CDC PLACES lookup for prevalence, SVI for retention
    - `site-selection-support.md` - Added data-driven site scoring with provenance
    - `enrollment-projection.md` - Added SDOH-adjusted retention modeling
    - `diversity-planning.md` - Added SVI minority population % for FDA Diversity Action Plans
    - `README.md` - Updated Data Sources section with v2.0 embedded files
  - All skills now explicitly reference embedded data files and include provenance tracking
  - Version markers added to YAML frontmatter

- **[Documentation]** Main README PopulationSim v2.0 Highlight (2024-12-24)
  - Added prominent "PopulationSim v2.0 - Data-Driven Generation" section
  - Includes data source table (148 MB across 3 sources)
  - Shows before/after example of data-driven generation
  - Cross-product integration summary with links

- **[MemberSim]** PopulationSim v2.0 Data Integration (2024-12-23)
  - Updated SKILL.md with comprehensive "Cross-Product: PopulationSim v2.0" section
  - Added data-driven generation pattern with embedded data lookup
  - Added SDOH impact on member generation (plan selection, adherence)
  - Added example: Medicare Advantage panel generation for Maricopa County, AZ
  - Added provenance tracking for actuarial realism

- **[RxMemberSim]** PopulationSim v2.0 Data Integration (2024-12-23)
  - Updated SKILL.md with comprehensive "Cross-Product: PopulationSim v2.0" section
  - Added data-driven pharmacy pattern with real prevalence rates
  - Added SDOH impact on adherence and generic utilization
  - Added example: Diabetic pharmacy claims for rural Appalachian county
  - Added provenance tracking for medication patterns

- **[TrialSim]** PopulationSim v2.0 Data Integration (2024-12-23)
  - Updated SKILL.md with comprehensive "Cross-Product: PopulationSim v2.0" section
  - Added data-driven trial planning pattern with site feasibility
  - Added embedded data sources for trial planning
  - Added example: Phase III site selection with real prevalence data
  - Linked to trial-support skills with v2.0 data references

- **[PopulationSim]** Canonical Model v2.0 with Per-Field Provenance (2024-12-23)
  - Updated `models/population-profile-schema.md` to version 2.0:
    - Added `$defs/dataProvenance` schema for source tracking
    - Added `provenancedNumber`, `provenancedInteger`, `provenancedRate` types
    - Added `healthMeasure` with confidence intervals and provenance
    - Added `sviMeasure` and `adiMeasure` composite types
    - Added `dataSourceSummary` for metadata aggregation
    - Every data field now tracks: source, data_year, methodology, file_reference
  - Added comprehensive example instance with full provenance
  - Added simplified output mode for applications not requiring provenance
  - Added Provenance Source Reference table
  - Completes Session 4 of PopulationSim v2.0 roadmap

### Added

- **[PopulationSim]** Phase 2 - Skills Integration with Embedded Data (2024-12-23)
  - Created new `data-access/` skill category:
    - `data-access/README.md` - Category overview and data provenance principles
    - `data-access/data-lookup.md` - Direct data file access patterns for PLACES, SVI, ADI
    - `data-access/geography-lookup.md` - FIPS code resolution and crosswalk queries
    - `data-access/data-aggregation.md` - Tract→county, county→metro aggregation patterns
  - Updated master `SKILL.md` with:
    - New data-access category in Quick Reference table
    - Data Access trigger phrases
    - Embedded data package in Data Sources section
    - Updated directory structure with data/ and data-access/ folders
  - Updated skills with "Data Sources (Embedded v2.0)" sections:
    - `geographic/county-profile.md` - Column mappings and lookup patterns
    - `sdoh/svi-analysis.md` - SVI column reference and lookup pattern
    - `sdoh/adi-analysis.md` - ADI suppression code handling
    - `cohorts/cohort-specification.md` - Data-first specification pattern
    - `cohorts/sdoh-profile-builder.md` - SDOH data sources and Z-code mapping
  - Created/updated reference documentation:
    - `references/data-sources.md` - NEW: Consolidated data source reference (212 lines)
    - `references/cdc-places-measures.md` - Added embedded file locations and column conventions
    - `references/svi-variables.md` - Added embedded file locations and column conventions
  - All skills now reference exact file paths and column names for embedded data package
  - Verified with 6 test queries confirming data-first generation works

- **[PopulationSim]** Embedded Data Package v2.0 - Phase 1 Complete (2024-12-23)
  - Created `skills/populationsim/data/` directory with real-world datasets:
    - **CDC PLACES 2024**: County (3,143 records, 4.8 MB) and Tract (83,522 records, 67 MB)
    - **CDC/ATSDR SVI 2022**: Tract (84,120 records, 61 MB) and County (aggregated, 3,144 records)
    - **Geography Crosswalks**: State (51), County (3,144), Tract-to-County (84,120)
  - Data sources provide 100% US geographic coverage with:
    - 40 health outcome measures (diabetes, obesity, COPD, depression, etc.)
    - 16 social vulnerability indicators across 4 themes
    - Demographics including race/ethnicity, age, income, education, insurance
  - Comprehensive `data/README.md` documentation including:
    - Data source descriptions and methodology
    - Column schemas for all datasets
    - Join keys and usage examples
    - Citation requirements
    - Data vintage and refresh schedule
  - **Note**: ADI block group data requires manual registration at neighborhoodatlas.medicine.wisc.edu
  - Total data package size: 132 MB

### Changed

- **[Cross-Product]** Bidirectional PopulationSim Cross-References (2024-12-23)
  - Added PopulationSim integration sections to all product SKILL.md files:
    - `skills/patientsim/SKILL.md` - Demographics & SDOH foundations for patient generation
    - `skills/membersim/SKILL.md` - Demographics & Market Intelligence for member generation
    - `skills/rxmembersim/SKILL.md` - Medication utilization patterns by population
    - `skills/trialsim/SKILL.md` - Feasibility & Diversity planning for trial design
  - Each section includes: integration table, pattern description, concrete example
  - Completes bidirectional cross-references between PopulationSim and all products

- **[PopulationSim]** Version 1.0 Complete - Status Updated to Active (2024-12-23)
  - Updated product status from "In Development" to "Active" across all documentation
  - Files updated:
    - `docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` - Product table and directory tree
    - `docs/CROSS-PRODUCT-INTEGRATION-GAPS.md` - Gap #1 status updated (Partial - PopulationSim Active)
    - `SKILL.md` - Product table and section headers
    - `README.md` - Directory tree
    - `docs/HEALTHSIM-PROJECT-INSTRUCTIONS.md` - Directory tree
    - `CLAUDE-CODE-CONTEXT.md` - Product table
  - PopulationSim v1 includes: population profiles, cohort specifications, SDOH analysis, health disparities, SVI/ADI integration, trial feasibility support

- **[TrialSim]** Version 1.0 Complete - Status Updated to Active (2024-12-23)
  - Updated product status from "In Development" to "Active"
  - Files updated:
    - `docs/HEALTHSIM-ARCHITECTURE-GUIDE.md` - Product table and directory tree
    - `SKILL.md` - Product table and section headers
  - TrialSim v1 includes: CDISC SDTM domains, therapeutic areas, trial phases, adverse events, efficacy endpoints, dimensional analytics

### Added

- **[PopulationSim]** Documentation Audit Gaps Resolved (2024-12-23)
  - YAML frontmatter added to 7 documentation/integration files:
    - `data-sources.md`, `developer-guide.md`, `prompt-guide.md`
    - `integration/patientsim-integration.md`, `membersim-integration.md`
    - `integration/trialsim-integration.md`, `cross-product-integration.md`
  - Product status updated: "planned" → "In Development"
  - `hello-healthsim/examples/populationsim-examples.md` created with 4 examples:
    - County Population Profile (Maricopa County, AZ)
    - SDOH Vulnerability Analysis (Rural Georgia)
    - Cohort Specification (Houston Diabetes Prevention)
    - Trial Feasibility Analysis (NASH multi-site)
  - Added Level 2.6 Population Intelligence to hello-healthsim/examples/README.md

- **[PopulationSim]** Complete Implementation (Phases 7-10) - Reference Data, Models, Integration, Documentation
  - Phase 7: Reference Data (6 files in `references/`)
    - `geography-codes.md` - FIPS (state/county/tract/block group), CBSA, urban/rural classification
    - `census-variables.md` - ACS variable naming, demographics, economic, housing tables
    - `cdc-places-indicators.md` - 27 measures (outcomes, prevention, behaviors, status)
    - `svi-methodology.md` - 4 themes, 16 variables, percentile calculation, interpretation
    - `adi-methodology.md` - 17 variables, 2 factor domains, national percentile/state decile
    - `code-systems.md` - Updated with geographic codes and SDOH Z-codes sections
  - Phase 8: Model Schemas (5 files in `references/models/`)
    - `population-profile.md` - Primary output model with complete field definitions
    - `cohort-specification.md` - Input model for population subsetting criteria
    - `geographic-entity.md` - Census hierarchy, FIPS/CBSA identification
    - `sdoh-profile.md` - Comprehensive SDOH with Z-code mapping formulas
    - `README.md` - Model index with relationship diagram
  - Phase 9: Cross-Product Integration (5 files in `skills/populationsim/integration/`)
    - `cross-product-integration.md` - Architecture overview, data flow patterns, identity correlation
    - `patientsim-integration.md` - Demographic/SDOH mapping to FHIR resources
    - `membersim-integration.md` - Insurance, enrollment, claims generation patterns
    - `trialsim-integration.md` - Feasibility, diversity planning, enrollment simulation
    - `README.md` - Integration guide index
  - Phase 10: Documentation & Examples (8 files)
    - `developer-guide.md` - Quick start, core concepts, skill reference, workflows
    - `data-sources.md` - ACS, CDC PLACES, SVI, ADI, USDA source details
    - `prompt-guide.md` - Example prompts for all skill categories
    - `hello-healthsim/populationsim/` - 5 example files
      - `README.md` - Getting started guide
      - `01-basic-profile.md` - County population profile example
      - `02-sdoh-analysis.md` - Social vulnerability analysis example
      - `03-cohort-definition.md` - Target population definition example
      - `04-trial-feasibility.md` - Clinical trial feasibility example
  - Key Additions:
    - Z-code prevalence estimation formulas (SDOH factor × multiplier)
    - SDOH-adjusted utilization patterns by SVI quartile
    - Insurance mix interpretation by population profile type
    - Trial retention modeling with SDOH risk factors
    - Complete JSON schema examples for all models

- **[PopulationSim]** Complete Implementation (Phases 1-6) - 22 Skills
  - Phase 1: Foundation Layer
    - `skills/populationsim/SKILL.md` - Master router with quick reference tables
    - `skills/populationsim/README.md` - Product overview and value proposition
    - `skills/populationsim/population-intelligence-domain.md` - Core domain knowledge
  - Phase 2: Geographic Intelligence Skills (5 files)
    - `geographic/README.md` - Category overview with PopulationProfile schema
    - `geographic/county-profile.md` - Comprehensive county-level profiles
    - `geographic/census-tract-analysis.md` - Granular tract-level analysis
    - `geographic/metro-area-profile.md` - MSA/CBSA metropolitan profiles
    - `geographic/custom-region-builder.md` - User-defined region aggregation
  - Phase 3: Health Pattern Analysis Skills (5 files)
    - `health-patterns/README.md` - CDC PLACES 27 measures overview
    - `health-patterns/chronic-disease-prevalence.md` - Disease burden analysis
    - `health-patterns/health-behavior-patterns.md` - Risk factor analysis
    - `health-patterns/healthcare-access-analysis.md` - Coverage and access gaps
    - `health-patterns/health-outcome-disparities.md` - Health equity analysis
  - Phase 4: SDOH Analysis Skills (5 files)
    - `sdoh/README.md` - SDOH framework with Z-code mapping
    - `sdoh/svi-analysis.md` - CDC Social Vulnerability Index (4 themes, 16 variables)
    - `sdoh/adi-analysis.md` - Area Deprivation Index (block group level)
    - `sdoh/economic-indicators.md` - Income, poverty, employment analysis
    - `sdoh/community-factors.md` - Housing, transportation, food, environment
  - Phase 5: Cohort Definition Skills (5 files)
    - `cohorts/README.md` - CohortSpecification object schema
    - `cohorts/cohort-specification.md` - Complete cohort definition master skill
    - `cohorts/demographic-distribution.md` - Age, sex, race/ethnicity distributions
    - `cohorts/clinical-prevalence-profile.md` - Comorbidity patterns (DM, HF, COPD, depression)
    - `cohorts/sdoh-profile-builder.md` - SDOH to Z-code mapping and rates
  - Phase 6: Trial Support Skills (4 files)
    - `trial-support/README.md` - TrialSim integration overview
    - `trial-support/feasibility-estimation.md` - Eligible population funnel modeling
    - `trial-support/site-selection-support.md` - Site network optimization
    - `trial-support/enrollment-projection.md` - Timeline and rate projections
  - Key Features:
    - Complete PopulationProfile and CohortSpecification JSON schemas
    - Evidence-based comorbidity matrices for major chronic conditions
    - SDOH domain indicators with ICD-10 Z-code mapping
    - Eligibility funnel model with conversion rates
    - Site scoring framework (density, diversity, competition, access)
    - Enrollment curve modeling with seasonal/competition factors
    - Integration points for PatientSim, MemberSim, and TrialSim

- **[TrialSim]** Complete Canonical Data Models - 15 Entities
  - `references/data-models.md` - Full TrialSim entity schemas added
    - Subject (extends Person with USUBJID, patient_ref cross-product link)
    - Study, Site, TreatmentArm, VisitSchedule, ActualVisit, Randomization
    - AdverseEvent with full MedDRA hierarchy (SOC/HLGT/HLT/PT/LLT)
    - Exposure with dose modification tracking
    - ConcomitantMed with full ATC hierarchy
    - TrialLab with LOINC and CTCAE toxicity grading
    - EfficacyAssessment (RECIST, irRECIST, RANO, NYHA, ADAS-Cog, EDSS)
    - MedicalHistory, DispositionEvent, ProtocolDeviation
  - Entity relationship diagram and cross-product linking patterns
  - USUBJID construction rules (STUDYID-SITEID-SUBJID)

- **[TrialSim]** Dimensional Analytics Star Schema - 7 Dimensions, 6 Facts
  - `formats/dimensional-analytics.md` - Full TrialSim star schema added
    - Dimensions: dim_study, dim_site, dim_subject, dim_treatment_arm, 
      dim_visit_schedule, dim_meddra, dim_lab_test
    - Facts: fact_enrollment, fact_visit, fact_adverse_event, fact_exposure,
      fact_efficacy, fact_lab_result
    - Complete SQL DDL for DuckDB and Databricks
    - Six analytics query examples (enrollment velocity, AE rates, ORR, 
      visit compliance, dose intensity, lab abnormalities)
    - Cross-product analytics examples (baseline vs response, prior therapy impact)
    - Star schema diagram

- **[Hello-HealthSim]** TrialSim Cross-Product Examples
  - `hello-healthsim/examples/cross-domain-examples.md` - 3 new examples
    - Trial Subject with EMR Linkage (TrialSim + PatientSim)
    - Trial Site with Provider Linkage (TrialSim + NetworkSim)
    - Cross-Product Dimensional Analytics queries
  - `hello-healthsim/examples/trialsim-examples.md` - Dimensional analytics section
    - DuckDB star schema examples
    - Databricks enterprise loading examples
    - Safety surveillance dashboard setup
    - Complete trial analytics package workflow

- **[Skills]** TrialSim SKILL.md Output Formats Section
  - Added Output Formats table (Canonical JSON, SDTM, ADaM, Dimensional)
  - Dimensional analytics quick reference with trigger phrases
  - Links to full format documentation

- **[Docs]** TrialSim Documentation Suite
  - `TRIALSIM-PROMPT-GUIDE.md` - Comprehensive usage guide with example prompts
    - Prompt patterns by use case (trial phases, domains, therapeutic areas)
    - Output format requests (JSON, SDTM, ADaM, CSV)
    - Combining skills patterns and cross-product integration
    - Troubleshooting and validation prompts
  - `TRIALSIM-DEVELOPER-GUIDE.md` - Developer reference v3.0
    - Current implementation status (20 skills complete)
    - Skill template with all required sections
    - CDISC standards reference (domains, variable prefixes, MedDRA)
    - Cross-product integration patterns
    - Development roadmap (Phase 3+ priorities)

- **[Hello-HealthSim]** Enhanced TrialSim Examples - Phase 3
  - Complete rewrite of trialsim-examples.md (328 → 806 lines)
  - Phase I examples: 3+3, BOIN, CRM, SAD/MAD, expansion cohorts
  - Phase II examples: Simon's two-stage, minimax, MCP-Mod dose-ranging
  - Phase III examples: Superiority, non-inferiority, multi-regional, DSMB
  - All 8 SDTM domain output examples with CSV format
  - ADaM analysis dataset examples (ADSL, ADAE, ADTTE, ADLB)
  - Comprehensive quick reference tables and tips

- **[Formats]** Enhanced CDISC ADaM Format - Phase 3
  - Complete rewrite of formats/cdisc-adam.md (120 → 633 lines)
  - Full ADSL variable mappings with all population flags
  - ADAE with treatment-emergent and first occurrence flags
  - ADTTE for survival analysis (OS, PFS, DOR, TTR)
  - ADLB with baseline, change from baseline, shift analysis
  - ADTR for tumor response (RECIST 1.1)
  - ADRS for best overall response analysis
  - Derivation rules and transformation examples

- **[Formats]** Enhanced CDISC SDTM Format - Batch 4
  - Complete rewrite of formats/cdisc-sdtm.md (112 → 702 lines)
  - Added all 8 SDTM domain mappings: DM, AE, CM, LB, VS, EX, DS, MH
  - Variable mappings with source fields and controlled terminology references
  - JSON → SDTM transformation examples for each domain
  - Domain-level and cross-domain validation rules
  - Controlled terminology tables (SEX, RACE, ETHNIC, ROUTE, FREQ, etc.)
  - Links to domain skills and related format skills

- **[TrialSim]** Trial Phase Skills - Batch 3 (Comprehensive Phase Coverage)
  - phase1-dose-escalation.md - First-in-human, SAD/MAD, MTD determination
    - Dose escalation designs: 3+3, BOIN, CRM, mTPI, Keyboard
    - PK/PD sampling patterns, DLT assessment criteria
    - Sentinel dosing, expansion cohorts, RP2D determination
  - phase2-proof-of-concept.md - POC, dose-ranging, efficacy signal
    - Phase 2a: Simon's two-stage, Bryant & Day designs
    - Phase 2b: MCP-Mod dose-response modeling
    - Futility analysis, interim decisions, go/no-go criteria
  - phase3-pivotal.md - Enhanced from placeholder to comprehensive skill
    - Superiority, non-inferiority, equivalence designs
    - Multi-regional trial considerations, ICH E5/E17
    - DSMB oversight, interim analyses, regulatory endpoints
  - All skills include: YAML frontmatter, 3+ examples, validation rules, business rules

- **[TrialSim]** SDTM Domain Skills - Batch 2 (Expanded Domains)
  - EX (Exposure) domain - study drug exposure, dose modifications, infusion cycles
  - DS (Disposition) domain - subject disposition, discontinuation reasons, CONSORT
  - MH (Medical History) domain - pre-existing conditions, MedDRA coding, comorbidities
  - All skills include: YAML frontmatter, 3 examples, validation rules, business rules
  - Updated domains/README.md with implementation status (all 8 domains complete)
  - Updated SKILL.md quick links with new domain references
  - All SDTM domain skills now complete (DM, AE, VS, LB, CM, EX, DS, MH)

- **[TrialSim]** SDTM Domain Skills (Phase 2 Implementation - Batch 1)
  - `skills/trialsim/domains/` directory with README.md overview
  - DM (Demographics) domain - subject identifiers, demographics, treatment arms
  - AE (Adverse Events) domain - MedDRA coding hierarchy, SAE flags, outcomes
  - VS (Vital Signs) domain - BP, HR, temp, weight with visit scheduling
  - LB (Laboratory) domain - LOINC coding, reference ranges, chemistry/hematology
  - CM (Concomitant Medications) domain - ATC classification, polypharmacy patterns
  - All skills include: YAML frontmatter, 2+ examples, validation rules, business rules
  - Cross-product integration with PatientSim documented
- **[TrialSim]** Updated SKILL.md with domain skill references in Quick Links
- **[TrialSim]** Updated README.md with implementation status for all domain skills

- **[Docs]** CLAUDE-CODE-CONTEXT.md for Claude Code session context
  - Essential patterns and rules for implementation sessions
  - Quality patterns (frontmatter, validation tables, related skills)
  - Skill file template with complete structure
  - Cross-product integration overview
  - Common pitfalls and verification checklist
  - Ensures consistency when using Claude Code without Project Files

- **[Skills Quality]** YAML frontmatter added to all scenario skills
  - 10 files updated: state-management.md, value-based-care.md, all RxMemberSim skills
  - Frontmatter includes `name` and `description` with trigger phrases
  - Enables better skill discovery and routing
- **[Skills Quality]** Validation Rules sections added to 25+ scenario skills
  - Field-level validation tables (format, requirements, examples)
  - Business rules for realistic data generation
  - Covers all PatientSim, MemberSim, and RxMemberSim scenario skills
- **[TrialSim]** Usage examples added to SKILL.md
  - 4 comprehensive examples: Phase 3 trial, adverse events, screening, SDTM output
  - Follows pattern established by PatientSim and MemberSim

- **[Cross-Product]** Cross-Product Identity Correlation section in data-models.md
  - Entity inheritance diagram (Person → Patient/Member/RxMember)
  - Identity linking keys table (SSN as universal correlator)
  - Cross-product identity pattern with JSON example
  - Event correlation timing across products (encounters → claims → fills)
  - TrialSim identity considerations for trial subjects
- **[Cross-Product]** Integration patterns added to all scenario skills
  - PatientSim: 9 skills updated with MemberSim/RxMemberSim references
  - MemberSim: 7 skills updated with PatientSim/RxMemberSim references
  - RxMemberSim: 8 skills updated with PatientSim/MemberSim references
  - Each section includes contextual integration pattern guidance
- **[Docs]** Cross-product integration as standard development practice
  - HEALTHSIM-DEVELOPMENT-PROCESS.md updated with integration checklist
  - HEALTHSIM-PROJECT-INSTRUCTIONS.md updated with integration reminders
  - New skill and product checklists include cross-product verification
- **[Docs]** CROSS-PRODUCT-INTEGRATION-GAPS.md gap analysis
  - 7 structural gaps identified with severity ratings
  - Implementation roadmap with 4 phases
  - Status tracking for gap resolution
- **[Docs]** Architecture Guide expanded (Section 8.3)
  - Comprehensive cross-product mapping table (all 4 products)
  - Integration pattern examples with timing
  - Reference to identity correlation in data-models.md
- **[Docs]** Product SKILL.md files enhanced with cross-product sections
  - PatientSim SKILL.md: Added MemberSim, RxMemberSim, TrialSim integration tables
  - MemberSim SKILL.md: Expanded beyond oncology to all scenarios
  - RxMemberSim SKILL.md: Added full cross-product integration section
  - TrialSim SKILL.md: Enhanced therapeutic area mapping
- **[Docs]** README.md cross-product integration section
  - Visual diagram showing product relationships
  - Example patient journey table (HF admission flow)
  - Links to architecture guide and gap analysis
- **[TrialSim]** Comprehensive development plan (docs/TRIALSIM-DEVELOPMENT-PLAN.md)
  - 6-phase development roadmap covering 16 weeks
  - Architecture for skills, therapeutic areas, CDISC compliance
  - Detailed SDTM/ADaM domain coverage planning
  - Priority therapeutic areas: Oncology, CNS, CV, Immunology, Metabolic
  - Reference data requirements (MedDRA, WHO Drug, country codes)
  - Integration patterns with PatientSim and NetworkSim
- **[Workspace]** Consolidated to single unified repository (healthsim-workspace)
- **[Workspace]** Product Python packages merged into packages/ folder
  - packages/patientsim/ - PatientSim MCP server and utilities
  - packages/membersim/ - MemberSim MCP server and utilities
  - packages/rxmembersim/ - RxMemberSim MCP server and utilities
- **[TrialSim]** Folder structure for clinical trials (skills/trialsim/)
- **[TrialSim]** CDISC format files (formats/cdisc-sdtm.md, formats/cdisc-adam.md)
- **[PopulationSim]** Placeholder structure (skills/populationsim/)
- **[NetworkSim]** Placeholder structure (skills/networksim/)
- **[Docs]** HEALTHSIM-PROJECT-INSTRUCTIONS.md - condensed Claude project instructions
- Comprehensive documentation hub (docs/README.md)
- Link audit and fixes across all documentation
- Skills common/ directory for shared skills
- State management skill moved to skills/common/

### Changed

- **[Workspace]** Repository renamed from healthsim-common to healthsim-workspace
- **[Workspace]** VS Code workspace updated with all product packages
- **[Workspace]** GitHub remote updated to healthsim-workspace

### Fixed

- Linting and formatting issues across Python codebase
- RxMemberSim SKILL.md missing YAML frontmatter

## [1.2.0] - 2024-12-14

### Changed

- Renamed repository from healthsim-skills to healthsim-common
- Updated all internal references to new repository name
- Updated README title to "HealthSim Workspace"

### Fixed

- Broken documentation links in architecture docs
- Example code in skills.md now references actual files

## [1.1.0] - 2024-12-13

### Added

- Oncology scenarios (breast, lung, colorectal cancer)
- Oncology reference data (ICD-10 codes, medications, regimens)
- Pediatric scenarios (otitis media, childhood asthma)
- FHIR NDJSON documentation
- Dimensional analytics format documentation

### Changed

- Enhanced FHIR R4 format documentation
- Improved cross-domain examples

## [1.0.0] - 2024-12-09

### Added

- Initial release
- Master SKILL.md file
- PatientSim scenarios (diabetes, heart failure, CKD, maternal health, behavioral health, ED, sepsis, elective joint, ADT)
- MemberSim scenarios (professional claims, facility claims, behavioral health, prior auth, enrollment, value-based care)
- RxMemberSim scenarios (retail, specialty, DUR, formulary, rx prior auth, accumulators, manufacturer programs)
- Output formats (FHIR R4, HL7v2 ADT/ORM/ORU, X12 837/835/834/270-271, NCPDP D.0, C-CDA, CSV, SQL)
- Reference data (data models, code systems, clinical rules)
- hello-healthsim getting started guide
- MCP integration documentation
- State management documentation
- Skills format specification (v1.0 and v2.0)
- Extension framework documentation

[Unreleased]: https://github.com/mark64oswald/healthsim-workspace/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/mark64oswald/healthsim-workspace/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/mark64oswald/healthsim-workspace/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/mark64oswald/healthsim-workspace/releases/tag/v1.0.0
