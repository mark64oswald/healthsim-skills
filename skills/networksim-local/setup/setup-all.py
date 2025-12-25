#!/usr/bin/env python3
"""
NetworkSim-Local: Complete Setup Script

Runs all setup steps in sequence:
1. Download taxonomy codes
2. Download NPPES data
3. Build DuckDB database
4. Validate database

Usage:
    python setup-all.py [--skip-download] [--state STATE]
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_script(script_name: str, args: list = None) -> bool:
    """Run a Python script and return success status."""
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        return False
    
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(
        description='Complete NetworkSim-Local setup'
    )
    parser.add_argument(
        '--skip-download',
        action='store_true',
        help='Skip downloading (use existing files)'
    )
    parser.add_argument(
        '--skip-nppes',
        action='store_true',
        help='Skip NPPES download (taxonomy only)'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only run validation'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("NetworkSim-Local Complete Setup")
    print("="*60)
    
    success = True
    
    if args.validate_only:
        success = run_script('validate-db.py')
    else:
        # Step 1: Download taxonomy
        if not args.skip_download:
            if not run_script('download-taxonomy.py'):
                print("\nWARNING: Taxonomy download had issues (continuing)")
        
        # Step 2: Download NPPES
        if not args.skip_download and not args.skip_nppes:
            if not run_script('download-nppes.py'):
                print("\nERROR: NPPES download failed")
                success = False
        
        # Step 3: Build database
        if success:
            if not run_script('build-database.py'):
                print("\nERROR: Database build failed")
                success = False
        
        # Step 4: Validate
        if success:
            if not run_script('validate-db.py'):
                print("\nERROR: Validation failed")
                success = False
    
    print("\n" + "="*60)
    if success:
        print("SETUP COMPLETE ✓")
    else:
        print("SETUP FAILED ✗")
        sys.exit(1)


if __name__ == '__main__':
    main()
