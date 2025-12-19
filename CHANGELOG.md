# Changelog

All notable changes to healthsim-common (Skills repository) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
