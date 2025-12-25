#!/usr/bin/env python3
"""
NetworkSim-Local: NUCC Taxonomy Code Downloader

Downloads the Healthcare Provider Taxonomy Code Set from NUCC.

Note: NUCC requires accepting a license agreement for commercial use.
This script downloads the publicly available CSV version.

Usage:
    python download-taxonomy.py [--output-dir PATH]
"""

import argparse
import csv
import sys
from pathlib import Path
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error

# CMS provides a taxonomy crosswalk that's publicly downloadable
CMS_TAXONOMY_URL = "https://data.cms.gov/provider-data/api/1/datastore/query/hpt5-frrd/0?limit=2000&offset=0&format=csv"

# Alternative: Direct taxonomy data from NUCC (may require form)
# NUCC_TAXONOMY_URL = "https://www.nucc.org/images/stories/CSV/nucc_taxonomy_241.csv"


def download_cms_taxonomy(output_path: Path) -> bool:
    """Download taxonomy crosswalk from CMS data.gov."""
    print("Downloading taxonomy data from CMS...")
    
    try:
        if HAS_REQUESTS:
            response = requests.get(CMS_TAXONOMY_URL, timeout=60)
            response.raise_for_status()
            content = response.text
        else:
            with urllib.request.urlopen(CMS_TAXONOMY_URL, timeout=60) as response:
                content = response.read().decode('utf-8')
        
        # Save raw file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Count records
        lines = content.strip().split('\n')
        print(f"Downloaded {len(lines) - 1} taxonomy records")
        
        return True
        
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def create_taxonomy_reference(output_dir: Path) -> Path:
    """Create a comprehensive taxonomy reference file."""
    
    # Core taxonomy codes used in healthcare
    # Based on NUCC taxonomy code set structure
    taxonomy_data = [
        # Header
        ["code", "grouping", "classification", "specialization", "definition"],
        
        # Physicians - Allopathic (207*)
        ["207K00000X", "Allopathic & Osteopathic Physicians", "Allergy & Immunology", "", "Allergy and immunology physician"],
        ["207L00000X", "Allopathic & Osteopathic Physicians", "Anesthesiology", "", "Anesthesiology physician"],
        ["207N00000X", "Allopathic & Osteopathic Physicians", "Dermatology", "", "Dermatology physician"],
        ["207P00000X", "Allopathic & Osteopathic Physicians", "Emergency Medicine", "", "Emergency medicine physician"],
        ["207Q00000X", "Allopathic & Osteopathic Physicians", "Family Medicine", "", "Family medicine physician"],
        ["207R00000X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "", "Internal medicine physician"],
        ["207RC0000X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Cardiovascular Disease", "Cardiologist"],
        ["207RE0101X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Endocrinology", "Endocrinologist"],
        ["207RG0100X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Gastroenterology", "Gastroenterologist"],
        ["207RH0000X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Hematology", "Hematologist"],
        ["207RI0001X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Clinical & Laboratory Immunology", "Immunologist"],
        ["207RI0200X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Infectious Disease", "Infectious disease specialist"],
        ["207RN0300X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Nephrology", "Nephrologist"],
        ["207RP1001X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Pulmonary Disease", "Pulmonologist"],
        ["207RR0500X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Rheumatology", "Rheumatologist"],
        ["207T00000X", "Allopathic & Osteopathic Physicians", "Neurological Surgery", "", "Neurosurgeon"],
        ["207U00000X", "Allopathic & Osteopathic Physicians", "Nuclear Medicine", "", "Nuclear medicine physician"],
        ["207V00000X", "Allopathic & Osteopathic Physicians", "Obstetrics & Gynecology", "", "OB/GYN physician"],
        ["207VG0400X", "Allopathic & Osteopathic Physicians", "Obstetrics & Gynecology", "Gynecology", "Gynecologist"],
        ["207W00000X", "Allopathic & Osteopathic Physicians", "Ophthalmology", "", "Ophthalmologist"],
        ["207X00000X", "Allopathic & Osteopathic Physicians", "Orthopaedic Surgery", "", "Orthopedic surgeon"],
        ["207Y00000X", "Allopathic & Osteopathic Physicians", "Otolaryngology", "", "ENT physician"],
        ["208000000X", "Allopathic & Osteopathic Physicians", "Pediatrics", "", "Pediatrician"],
        ["2080P0006X", "Allopathic & Osteopathic Physicians", "Pediatrics", "Developmental-Behavioral Pediatrics", "Developmental pediatrician"],
        ["208100000X", "Allopathic & Osteopathic Physicians", "Physical Medicine & Rehabilitation", "", "Physiatrist"],
        ["208200000X", "Allopathic & Osteopathic Physicians", "Plastic Surgery", "", "Plastic surgeon"],
        ["208600000X", "Allopathic & Osteopathic Physicians", "Surgery", "", "General surgeon"],
        ["208800000X", "Allopathic & Osteopathic Physicians", "Urology", "", "Urologist"],
        ["208C00000X", "Allopathic & Osteopathic Physicians", "Colon & Rectal Surgery", "", "Colorectal surgeon"],
        ["208D00000X", "Allopathic & Osteopathic Physicians", "General Practice", "", "General practice physician"],
        ["208G00000X", "Allopathic & Osteopathic Physicians", "Thoracic Surgery", "", "Thoracic surgeon"],
        ["2084N0400X", "Allopathic & Osteopathic Physicians", "Psychiatry & Neurology", "Neurology", "Neurologist"],
        ["2084P0800X", "Allopathic & Osteopathic Physicians", "Psychiatry & Neurology", "Psychiatry", "Psychiatrist"],
        
        # Nurse Practitioners (363L*)
        ["363L00000X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "", "Nurse practitioner"],
        ["363LA2100X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "Acute Care", "Acute care NP"],
        ["363LA2200X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "Adult Health", "Adult health NP"],
        ["363LC0200X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "Critical Care Medicine", "Critical care NP"],
        ["363LF0000X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "Family", "Family NP"],
        ["363LG0600X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "Gerontology", "Gerontology NP"],
        ["363LP0200X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "Pediatrics", "Pediatric NP"],
        ["363LP0808X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "Psych/Mental Health", "Psychiatric NP"],
        ["363LW0102X", "Physician Assistants & Advanced Practice Nursing", "Nurse Practitioner", "Women's Health", "Women's health NP"],
        
        # Physician Assistants (363A*)
        ["363A00000X", "Physician Assistants & Advanced Practice Nursing", "Physician Assistant", "", "Physician assistant"],
        ["363AM0700X", "Physician Assistants & Advanced Practice Nursing", "Physician Assistant", "Medical", "Medical PA"],
        ["363AS0400X", "Physician Assistants & Advanced Practice Nursing", "Physician Assistant", "Surgical", "Surgical PA"],
        
        # Pharmacies (3336*)
        ["3336C0002X", "Suppliers", "Pharmacy", "Clinic Pharmacy", "Clinic pharmacy"],
        ["3336C0003X", "Suppliers", "Pharmacy", "Community/Retail Pharmacy", "Retail pharmacy"],
        ["3336C0004X", "Suppliers", "Pharmacy", "Compounding Pharmacy", "Compounding pharmacy"],
        ["3336H0001X", "Suppliers", "Pharmacy", "Home Infusion Therapy Pharmacy", "Home infusion pharmacy"],
        ["3336I0012X", "Suppliers", "Pharmacy", "Institutional Pharmacy", "Institutional pharmacy"],
        ["3336L0003X", "Suppliers", "Pharmacy", "Long Term Care Pharmacy", "Long term care pharmacy"],
        ["3336M0002X", "Suppliers", "Pharmacy", "Mail Order Pharmacy", "Mail order pharmacy"],
        ["3336N0007X", "Suppliers", "Pharmacy", "Nuclear Pharmacy", "Nuclear pharmacy"],
        ["3336S0011X", "Suppliers", "Pharmacy", "Specialty Pharmacy", "Specialty pharmacy"],
        
        # Hospitals (282*, 283*, 284*)
        ["282N00000X", "Hospitals", "General Acute Care Hospital", "", "General acute care hospital"],
        ["282NC0060X", "Hospitals", "General Acute Care Hospital", "Critical Access", "Critical access hospital"],
        ["282NC2000X", "Hospitals", "General Acute Care Hospital", "Children", "Children's hospital"],
        ["282NR1301X", "Hospitals", "General Acute Care Hospital", "Rural", "Rural hospital"],
        ["282NW0100X", "Hospitals", "General Acute Care Hospital", "Women", "Women's hospital"],
        ["283Q00000X", "Hospitals", "Psychiatric Hospital", "", "Psychiatric hospital"],
        ["283X00000X", "Hospitals", "Rehabilitation Hospital", "", "Rehabilitation hospital"],
        ["284300000X", "Hospitals", "Special Hospital", "", "Special hospital"],
        ["286500000X", "Hospitals", "Military Hospital", "", "Military hospital"],
        
        # Clinics (261Q*)
        ["261Q00000X", "Ambulatory Health Care Facilities", "Clinic/Center", "", "Clinic/center"],
        ["261QA0005X", "Ambulatory Health Care Facilities", "Clinic/Center", "Ambulatory Family Planning Facility", "Family planning clinic"],
        ["261QA0600X", "Ambulatory Health Care Facilities", "Clinic/Center", "Adult Day Care", "Adult day care"],
        ["261QA1903X", "Ambulatory Health Care Facilities", "Clinic/Center", "Ambulatory Surgical", "Ambulatory surgery center"],
        ["261QB0400X", "Ambulatory Health Care Facilities", "Clinic/Center", "Birthing", "Birthing center"],
        ["261QC0050X", "Ambulatory Health Care Facilities", "Clinic/Center", "Critical Access Hospital", "CAH clinic"],
        ["261QC1500X", "Ambulatory Health Care Facilities", "Clinic/Center", "Community Health", "Community health center"],
        ["261QC1800X", "Ambulatory Health Care Facilities", "Clinic/Center", "Corporate Health", "Corporate health clinic"],
        ["261QD0000X", "Ambulatory Health Care Facilities", "Clinic/Center", "Dental", "Dental clinic"],
        ["261QE0002X", "Ambulatory Health Care Facilities", "Clinic/Center", "Emergency Care", "Emergency clinic"],
        ["261QE0700X", "Ambulatory Health Care Facilities", "Clinic/Center", "End-Stage Renal Disease (ESRD) Treatment", "Dialysis center"],
        ["261QF0400X", "Ambulatory Health Care Facilities", "Clinic/Center", "Federally Qualified Health Center", "FQHC"],
        ["261QH0100X", "Ambulatory Health Care Facilities", "Clinic/Center", "Health Service", "Health service clinic"],
        ["261QM0801X", "Ambulatory Health Care Facilities", "Clinic/Center", "Mental Health", "Mental health clinic"],
        ["261QM1000X", "Ambulatory Health Care Facilities", "Clinic/Center", "Migrant Health", "Migrant health center"],
        ["261QP0904X", "Ambulatory Health Care Facilities", "Clinic/Center", "Public Health, Federal", "Federal public health clinic"],
        ["261QP0905X", "Ambulatory Health Care Facilities", "Clinic/Center", "Public Health, State or Local", "State/local public health clinic"],
        ["261QP2300X", "Ambulatory Health Care Facilities", "Clinic/Center", "Primary Care", "Primary care clinic"],
        ["261QR0200X", "Ambulatory Health Care Facilities", "Clinic/Center", "Radiology", "Radiology center"],
        ["261QR0400X", "Ambulatory Health Care Facilities", "Clinic/Center", "Rehabilitation", "Rehabilitation clinic"],
        ["261QR0401X", "Ambulatory Health Care Facilities", "Clinic/Center", "Rehabilitation, Comprehensive Outpatient", "CORF"],
        ["261QR0405X", "Ambulatory Health Care Facilities", "Clinic/Center", "Rehabilitation, Cardiac Facilities", "Cardiac rehab"],
        ["261QR0800X", "Ambulatory Health Care Facilities", "Clinic/Center", "Recovery Care", "Recovery care clinic"],
        ["261QR1100X", "Ambulatory Health Care Facilities", "Clinic/Center", "Research", "Research clinic"],
        ["261QR1300X", "Ambulatory Health Care Facilities", "Clinic/Center", "Rural Health", "Rural health clinic"],
        ["261QS0112X", "Ambulatory Health Care Facilities", "Clinic/Center", "Oral and Maxillofacial Surgery", "Oral surgery clinic"],
        ["261QS0132X", "Ambulatory Health Care Facilities", "Clinic/Center", "Ophthalmologic Surgery", "Eye surgery center"],
        ["261QS1000X", "Ambulatory Health Care Facilities", "Clinic/Center", "Student Health", "Student health clinic"],
        ["261QS1200X", "Ambulatory Health Care Facilities", "Clinic/Center", "Sleep Disorder Diagnostic", "Sleep clinic"],
        ["261QU0200X", "Ambulatory Health Care Facilities", "Clinic/Center", "Urgent Care", "Urgent care clinic"],
        ["261QV0200X", "Ambulatory Health Care Facilities", "Clinic/Center", "VA", "VA clinic"],
        
        # Skilled Nursing Facilities (314*)
        ["314000000X", "Nursing & Custodial Care Facilities", "Skilled Nursing Facility", "", "Skilled nursing facility"],
        ["3140N1450X", "Nursing & Custodial Care Facilities", "Skilled Nursing Facility", "Nursing Care, Pediatric", "Pediatric SNF"],
        
        # Home Health (251E*)
        ["251E00000X", "Agencies", "Home Health", "", "Home health agency"],
        
        # Laboratories (291U*)
        ["291U00000X", "Laboratories", "Clinical Medical Laboratory", "", "Clinical laboratory"],
        
        # Other common provider types
        ["111N00000X", "Chiropractic Providers", "Chiropractor", "", "Chiropractor"],
        ["122300000X", "Dental Providers", "Dentist", "", "Dentist"],
        ["1223G0001X", "Dental Providers", "Dentist", "General Practice", "General dentist"],
        ["152W00000X", "Eye and Vision Services Providers", "Optometrist", "", "Optometrist"],
        ["156FX1800X", "Eye and Vision Services Providers", "Technician/Technologist", "Optician", "Optician"],
        ["163W00000X", "Nursing Service Providers", "Registered Nurse", "", "Registered nurse"],
        ["174400000X", "Other Service Providers", "Specialist", "", "Specialist"],
        ["1835G0000X", "Pharmacy Service Providers", "Pharmacist", "", "Pharmacist"],
        ["225100000X", "Respiratory, Developmental, Rehabilitative", "Physical Therapist", "", "Physical therapist"],
        ["225500000X", "Respiratory, Developmental, Rehabilitative", "Respiratory Therapist", "", "Respiratory therapist"],
        ["2255A2300X", "Respiratory, Developmental, Rehabilitative", "Specialist/Technologist", "Athletic Trainer", "Athletic trainer"],
        ["2251S0007X", "Respiratory, Developmental, Rehabilitative", "Specialist/Technologist", "Speech-Language Pathologist", "Speech therapist"],
        ["225X00000X", "Respiratory, Developmental, Rehabilitative", "Occupational Therapist", "", "Occupational therapist"],
        ["231H00000X", "Speech, Language and Hearing Service Providers", "Audiologist", "", "Audiologist"],
        ["332B00000X", "Suppliers", "Durable Medical Equipment & Medical Supplies", "", "DME supplier"],
        ["335E00000X", "Suppliers", "Prosthetic/Orthotic Supplier", "", "Prosthetic/orthotic supplier"],
    ]
    
    output_path = output_dir / "taxonomy_codes.csv"
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(taxonomy_data)
    
    print(f"Created taxonomy reference: {output_path}")
    print(f"  Records: {len(taxonomy_data) - 1}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Download NUCC Healthcare Provider Taxonomy codes'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help='Output directory (default: ../data/taxonomy relative to script)'
    )
    
    args = parser.parse_args()
    
    # Determine output directory
    script_dir = Path(__file__).parent
    output_dir = args.output_dir or (script_dir.parent / 'data' / 'taxonomy')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("NetworkSim-Local: Taxonomy Code Downloader")
    print("=" * 60)
    
    # Try CMS download first
    cms_file = output_dir / "cms_taxonomy_crosswalk.csv"
    if download_cms_taxonomy(cms_file):
        print(f"\nCMS taxonomy crosswalk saved to: {cms_file}")
    else:
        print("\nNote: CMS download failed, will use built-in reference")
    
    # Create comprehensive reference file
    print("\nCreating taxonomy reference file...")
    ref_file = create_taxonomy_reference(output_dir)
    
    print("\n" + "=" * 60)
    print("Taxonomy download complete!")
    print(f"Output directory: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
