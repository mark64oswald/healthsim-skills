# Oncology Scenarios

Comprehensive oncology patient generation skills for PatientSim.

## Skills

| Skill | Description | Key Features |
|-------|-------------|--------------|
| [oncology-domain.md](oncology-domain.md) | Foundational oncology knowledge | Staging, biomarkers, treatment modalities |
| [breast-cancer.md](breast-cancer.md) | Breast cancer scenarios | Molecular subtypes, hormonal/targeted therapy |
| [lung-cancer.md](lung-cancer.md) | Lung cancer scenarios | NSCLC/SCLC, biomarker-driven therapy |
| [colorectal-cancer.md](colorectal-cancer.md) | Colorectal cancer scenarios | Colon/rectal, MSI, hereditary syndromes |

## Quick Start

### Generate a Breast Cancer Patient
```
Generate a 55-year-old female with Stage IIA ER-positive, HER2-negative breast cancer
```

### Generate a Lung Cancer Patient
```
Generate a 68-year-old male with Stage IV NSCLC, EGFR exon 19 deletion positive
```

### Generate a Colorectal Cancer Patient
```
Generate a 58-year-old with Stage III colon cancer, MSI-high status
```

## Cross-Product Integration

### MemberSim (Claims)
- Facility claims for infusion center treatments
- Professional claims for oncology office visits
- Prior authorization for specialty oncology drugs

### RxMemberSim (Pharmacy)
- Specialty pharmacy for oral oncolytics (Ibrance, Tagrisso)
- Supportive care medications (antiemetics, G-CSF)
- Manufacturer copay assistance programs

## Reference Data

See [references/oncology/](../../../references/oncology/) for:
- ICD-10 diagnosis codes (115 codes)
- Oncology medications (90 drugs)
- Chemotherapy regimens (48 protocols)
- Tumor markers with LOINC codes
- Staging templates by cancer type
