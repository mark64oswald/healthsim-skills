# Changelog

All notable changes to healthsim-workspace (Skills repository) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation hub (docs/README.md)
- Link audit and fixes across all documentation

## [1.2.0] - 2024-12-14

### Changed
- Renamed repository from healthsim-skills to healthsim-workspace
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
