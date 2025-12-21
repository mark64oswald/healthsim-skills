# Changelog

All notable changes to healthsim-common (Skills repository) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
