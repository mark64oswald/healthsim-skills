#!/usr/bin/env python3
"""
NetworkSim-Local Database Builder

Builds a DuckDB database from NPPES NPI Registry data.

Usage:
    python build-database.py [--nppes-file PATH] [--output PATH]

Example:
    python build-database.py --nppes-file ../data/nppes/npidata_pfile_20050523-20251208.csv
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import duckdb
except ImportError:
    print("ERROR: duckdb not installed. Run: pip install duckdb")
    sys.exit(1)

# Column mapping: CSV column name -> DB column name
COLUMN_MAPPING = {
    'NPI': 'npi',
    'Entity Type Code': 'entity_type_code',
    'Provider Organization Name (Legal Business Name)': 'organization_name',
    'Provider Last Name (Legal Name)': 'last_name',
    'Provider First Name': 'first_name',
    'Provider Middle Name': 'middle_name',
    'Provider Name Prefix Text': 'name_prefix',
    'Provider Name Suffix Text': 'name_suffix',
    'Provider Credential Text': 'credential',
    'Provider Sex Code': 'gender_code',
    'Provider First Line Business Practice Location Address': 'practice_address_1',
    'Provider Second Line Business Practice Location Address': 'practice_address_2',
    'Provider Business Practice Location Address City Name': 'practice_city',
    'Provider Business Practice Location Address State Name': 'practice_state',
    'Provider Business Practice Location Address Postal Code': 'practice_zip',
    'Provider Business Practice Location Address Country Code (If outside U.S.)': 'practice_country',
    'Provider Business Practice Location Address Telephone Number': 'practice_phone',
    'Provider Business Practice Location Address Fax Number': 'practice_fax',
    'Healthcare Provider Taxonomy Code_1': 'taxonomy_code',
    'Provider License Number_1': 'license_number',
    'Provider License Number State Code_1': 'license_state',
    'Healthcare Provider Primary Taxonomy Switch_1': 'is_primary_taxonomy',
    'Provider Enumeration Date': 'enumeration_date',
    'Last Update Date': 'last_update_date',
    'NPI Deactivation Date': 'deactivation_date',
    'NPI Reactivation Date': 'reactivation_date',
    'Is Sole Proprietor': 'is_sole_proprietor',
    'Is Organization Subpart': 'is_subpart',
    'Authorized Official Last Name': 'auth_official_last_name',
    'Authorized Official First Name': 'auth_official_first_name',
    'Authorized Official Telephone Number': 'auth_official_phone',
}

# US State codes (including territories)
US_STATES = {
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
    'DC', 'PR', 'VI', 'GU', 'AS', 'MP'  # DC + Territories
}

# Top 10 states for filtered builds
TOP_10_STATES = {'CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI'}


def find_nppes_file(data_dir: Path) -> Path:
    """Find the NPPES data file in possible directories."""
    
    # Check multiple possible locations
    search_dirs = [
        data_dir / 'nppes',          # New location
        data_dir / 'raw' / 'nppes',  # Old location
        data_dir,                     # Direct in data dir
    ]
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        
        # Look for npidata_pfile_*.csv (exclude header files)
        for f in search_dir.glob('npidata_pfile_*.csv'):
            if 'fileheader' not in f.name.lower():
                return f
    
    return None


def build_database(nppes_file: Path, output_file: Path, 
                   filter_states: set = None, verbose: bool = True):
    """Build DuckDB database from NPPES CSV."""
    
    if verbose:
        print(f"NetworkSim-Local Database Builder")
        print(f"=" * 60)
        print(f"Input:  {nppes_file}")
        print(f"Output: {output_file}")
        if filter_states:
            print(f"Filter: {len(filter_states)} states")
        print()
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing database
    if output_file.exists():
        os.remove(output_file)
    
    # Connect to DuckDB
    con = duckdb.connect(str(output_file))
    
    try:
        if verbose:
            print("Step 1: Reading NPPES CSV (this may take several minutes)...")
        
        # Escape path for SQL (handle backslashes on Windows)
        escaped_path = str(nppes_file).replace('\\', '/')
        
        # Determine state filter
        states_to_use = filter_states if filter_states else US_STATES
        states_sql = ','.join([f"'{s}'" for s in states_to_use])
        
        # Build column selection
        column_select = ', '.join([
            f'"{csv}" AS {db}' for csv, db in COLUMN_MAPPING.items()
        ])
        
        # Create the providers table with filtering
        # Use all_varchar=true to avoid date parsing issues (NPPES uses MM/DD/YYYY)
        query = f"""
        CREATE TABLE providers AS
        SELECT {column_select}
        FROM read_csv_auto(
            '{escaped_path}',
            header=true,
            ignore_errors=true,
            parallel=true,
            sample_size=-1,
            all_varchar=true
        )
        WHERE 
            -- Active providers only (no deactivation date, or has reactivation)
            ("NPI Deactivation Date" IS NULL 
             OR TRIM("NPI Deactivation Date") = ''
             OR ("NPI Reactivation Date" IS NOT NULL AND TRIM("NPI Reactivation Date") != ''))
            -- Selected states only
            AND "Provider Business Practice Location Address State Name" IN ({states_sql})
        """
        
        con.execute(query)
        
        # Get record count
        count = con.execute("SELECT COUNT(*) FROM providers").fetchone()[0]
        if verbose:
            print(f"   Loaded {count:,} active providers")
        
        # Step 2: Create indexes
        if verbose:
            print("\nStep 2: Creating indexes...")
        
        con.execute("CREATE INDEX idx_npi ON providers(npi)")
        con.execute("CREATE INDEX idx_state ON providers(practice_state)")
        con.execute("CREATE INDEX idx_zip ON providers(practice_zip)")
        con.execute("CREATE INDEX idx_taxonomy ON providers(taxonomy_code)")
        con.execute("CREATE INDEX idx_city_state ON providers(practice_city, practice_state)")
        con.execute("CREATE INDEX idx_entity_type ON providers(entity_type_code)")
        
        if verbose:
            print("   Created 6 indexes")
        
        # Step 3: Create provider categories view
        if verbose:
            print("\nStep 3: Creating views...")
        
        con.execute("""
        CREATE VIEW provider_categories AS
        SELECT 
            npi,
            entity_type_code,
            organization_name,
            last_name,
            first_name,
            practice_state,
            practice_city,
            taxonomy_code,
            CASE 
                WHEN taxonomy_code LIKE '207%' THEN 'Physician (Allopathic)'
                WHEN taxonomy_code LIKE '208%' THEN 'Physician (Allopathic)'
                WHEN taxonomy_code LIKE '204%' THEN 'Physician (Osteopathic)'
                WHEN taxonomy_code LIKE '363L%' THEN 'Nurse Practitioner'
                WHEN taxonomy_code LIKE '363A%' THEN 'Physician Assistant'
                WHEN taxonomy_code LIKE '3336%' THEN 'Pharmacy'
                WHEN taxonomy_code LIKE '282N%' THEN 'Hospital - General Acute Care'
                WHEN taxonomy_code LIKE '282%' THEN 'Hospital - Other'
                WHEN taxonomy_code LIKE '261Q%' THEN 'Clinic'
                WHEN taxonomy_code LIKE '332%' THEN 'DME Supplier'
                WHEN taxonomy_code LIKE '313%' THEN 'Nursing Facility'
                WHEN taxonomy_code LIKE '174%' THEN 'Dentist'
                WHEN taxonomy_code LIKE '152%' THEN 'Optometrist'
                WHEN taxonomy_code LIKE '133%' THEN 'Podiatrist'
                WHEN taxonomy_code LIKE '111%' THEN 'Chiropractor'
                WHEN taxonomy_code LIKE '225%' THEN 'Physical Therapist'
                WHEN taxonomy_code LIKE '1041%' THEN 'Psychologist'
                WHEN taxonomy_code LIKE '1835%' THEN 'Pharmacist'
                ELSE 'Other'
            END as provider_category
        FROM providers
        """)
        
        if verbose:
            print("   Created provider_categories view")
        
        # Step 4: Create summary statistics table
        if verbose:
            print("\nStep 4: Computing statistics...")
        
        con.execute("""
        CREATE TABLE load_metadata (
            key VARCHAR PRIMARY KEY,
            value VARCHAR
        )
        """)
        
        states_str = ','.join(sorted(states_to_use)) if filter_states else 'ALL'
        con.execute(f"""
        INSERT INTO load_metadata VALUES
            ('source_file', '{nppes_file.name}'),
            ('load_date', '{datetime.now().isoformat()}'),
            ('total_providers', '{count}'),
            ('states_included', '{states_str}'),
            ('version', '1.0.0')
        """)
        
        # Get distribution stats
        stats = con.execute("""
        SELECT 
            provider_category,
            COUNT(*) as count
        FROM provider_categories
        GROUP BY provider_category
        ORDER BY count DESC
        """).fetchall()
        
        if verbose:
            print("\n   Provider Distribution:")
            for cat, cnt in stats[:12]:
                print(f"     {cat}: {cnt:,}")
            if len(stats) > 12:
                print(f"     ... and {len(stats) - 12} more categories")
        
        # State distribution
        if verbose:
            print("\n   State Distribution (top 10):")
            state_stats = con.execute("""
            SELECT practice_state, COUNT(*) as cnt
            FROM providers
            GROUP BY practice_state
            ORDER BY cnt DESC
            LIMIT 10
            """).fetchall()
            for state, cnt in state_stats:
                print(f"     {state}: {cnt:,}")
        
        # Final stats
        db_size = output_file.stat().st_size / (1024 * 1024)
        
        if verbose:
            print(f"\n{'=' * 60}")
            print(f"Database built successfully!")
            print(f"  Records:  {count:,}")
            print(f"  Size:     {db_size:.1f} MB")
            print(f"  Location: {output_file}")
        
        return count
        
    finally:
        con.close()


def main():
    parser = argparse.ArgumentParser(
        description='Build NetworkSim-Local DuckDB database from NPPES data'
    )
    parser.add_argument(
        '--nppes-file',
        type=Path,
        help='Path to NPPES CSV file (npidata_pfile_*.csv)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Output database path (default: data/networksim-local.duckdb)'
    )
    parser.add_argument(
        '--top-10-states',
        action='store_true',
        help='Filter to top 10 states only (smaller database)'
    )
    parser.add_argument(
        '--all-states',
        action='store_true',
        help='Include all US states and territories'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    # Determine paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    
    # Find or use specified NPPES file
    if args.nppes_file:
        nppes_file = args.nppes_file
    else:
        nppes_file = find_nppes_file(data_dir)
        if not nppes_file:
            print("ERROR: No NPPES file found.")
            print(f"Please download from https://download.cms.gov/nppes/NPI_Files.html")
            print(f"and extract to: {data_dir / 'nppes'}/")
            sys.exit(1)
    
    if not nppes_file.exists():
        print(f"ERROR: NPPES file not found: {nppes_file}")
        sys.exit(1)
    
    # Determine output path
    output_file = args.output or (data_dir / 'networksim-local.duckdb')
    
    # Determine state filter
    if args.top_10_states:
        filter_states = TOP_10_STATES
    elif args.all_states:
        filter_states = US_STATES
    else:
        # Default: all US states
        filter_states = US_STATES
    
    # Build database
    try:
        build_database(
            nppes_file, 
            output_file, 
            filter_states=filter_states,
            verbose=not args.quiet
        )
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
