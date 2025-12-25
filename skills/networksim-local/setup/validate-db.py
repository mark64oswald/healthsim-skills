#!/usr/bin/env python3
"""
NetworkSim-Local: Database Validation

Validates the NetworkSim-Local DuckDB database after building.

Usage:
    python validate-db.py [--database PATH]
"""

import argparse
import sys
from pathlib import Path

try:
    import duckdb
except ImportError:
    print("ERROR: duckdb not installed. Run: pip install duckdb")
    sys.exit(1)


def validate_database(db_path: Path) -> bool:
    """Run validation checks on the database."""
    
    print(f"Validating: {db_path}")
    print("=" * 60)
    
    if not db_path.exists():
        print(f"ERROR: Database not found: {db_path}")
        return False
    
    try:
        con = duckdb.connect(str(db_path), read_only=True)
    except Exception as e:
        print(f"ERROR: Could not open database: {e}")
        return False
    
    errors = []
    
    # Check 1: Table exists
    print("\n[1] Checking tables...")
    tables = con.execute("SHOW TABLES").fetchall()
    table_names = [t[0] for t in tables]
    
    if 'providers' not in table_names:
        errors.append("Missing 'providers' table")
    else:
        print("  ✓ providers table exists")
    
    if 'load_metadata' not in table_names:
        errors.append("Missing 'load_metadata' table")
    else:
        print("  ✓ load_metadata table exists")
    
    # Check 2: Record count
    print("\n[2] Checking record counts...")
    try:
        count = con.execute("SELECT COUNT(*) FROM providers").fetchone()[0]
        if count < 1000000:
            errors.append(f"Low record count: {count:,} (expected 1M+)")
        else:
            print(f"  ✓ {count:,} providers loaded")
    except Exception as e:
        errors.append(f"Could not count providers: {e}")
    
    # Check 3: Data quality
    print("\n[3] Checking data quality...")
    
    # Check for NPIs
    npi_check = con.execute("""
        SELECT COUNT(*) FROM providers 
        WHERE npi IS NOT NULL AND LENGTH(npi) = 10
    """).fetchone()[0]
    
    if npi_check != count:
        errors.append(f"Invalid NPIs found: {count - npi_check} records")
    else:
        print(f"  ✓ All NPIs valid (10 digits)")
    
    # Check state distribution
    print("\n[4] State distribution...")
    states = con.execute("""
        SELECT practice_state, COUNT(*) as cnt 
        FROM providers 
        WHERE practice_state IS NOT NULL
        GROUP BY practice_state 
        ORDER BY cnt DESC 
        LIMIT 10
    """).fetchall()
    
    for state, cnt in states:
        print(f"  {state}: {cnt:,}")
    
    # Check 5: Entity type distribution
    print("\n[5] Entity type distribution...")
    entities = con.execute("""
        SELECT 
            CASE entity_type_code 
                WHEN '1' THEN 'Individual'
                WHEN '2' THEN 'Organization'
                ELSE 'Unknown'
            END as entity_type,
            COUNT(*) as cnt
        FROM providers
        GROUP BY entity_type_code
        ORDER BY cnt DESC
    """).fetchall()
    
    for entity, cnt in entities:
        print(f"  {entity}: {cnt:,}")
    
    # Check 6: Provider categories
    print("\n[6] Provider categories (top 15)...")
    try:
        categories = con.execute("""
            SELECT provider_category, COUNT(*) as cnt
            FROM provider_categories
            GROUP BY provider_category
            ORDER BY cnt DESC
            LIMIT 15
        """).fetchall()
        
        for cat, cnt in categories:
            print(f"  {cat}: {cnt:,}")
    except Exception as e:
        print(f"  Note: provider_categories view not available: {e}")
    
    # Check 7: Sample data
    print("\n[7] Sample provider lookup...")
    sample = con.execute("""
        SELECT npi, 
               COALESCE(organization_name, last_name || ', ' || first_name) as name,
               taxonomy_code,
               practice_city,
               practice_state
        FROM providers
        WHERE practice_state = 'CA'
        LIMIT 3
    """).fetchall()
    
    for row in sample:
        print(f"  NPI: {row[0]} | {row[1]} | {row[3]}, {row[4]}")
    
    # Check 8: Indexes
    print("\n[8] Checking indexes...")
    # DuckDB doesn't have a direct way to list indexes, but we can verify query performance
    
    # Test NPI lookup (should be fast with index)
    import time
    test_npi = sample[0][0] if sample else None
    if test_npi:
        start = time.time()
        con.execute(f"SELECT * FROM providers WHERE npi = '{test_npi}'").fetchone()
        elapsed = time.time() - start
        if elapsed < 0.1:
            print(f"  ✓ NPI lookup: {elapsed*1000:.1f}ms")
        else:
            print(f"  ⚠ NPI lookup slow: {elapsed*1000:.1f}ms")
    
    # Check 9: Metadata
    print("\n[9] Load metadata...")
    try:
        metadata = con.execute("SELECT * FROM load_metadata").fetchall()
        for key, value in metadata:
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"  Note: Could not read metadata: {e}")
    
    con.close()
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f"  ✗ {err}")
        return False
    else:
        print("VALIDATION PASSED ✓")
        print(f"\nDatabase ready: {db_path}")
        print(f"Size: {db_path.stat().st_size / (1024*1024):.1f} MB")
        return True


def interactive_query(db_path: Path):
    """Run interactive queries for testing."""
    
    print("\n" + "=" * 60)
    print("Interactive Query Mode")
    print("Type 'exit' to quit, or enter SQL queries")
    print("=" * 60)
    
    con = duckdb.connect(str(db_path), read_only=True)
    
    while True:
        try:
            query = input("\nSQL> ").strip()
            
            if query.lower() in ('exit', 'quit', 'q'):
                break
            
            if not query:
                continue
            
            result = con.execute(query).fetchall()
            
            if result:
                # Get column names
                desc = con.description
                if desc:
                    headers = [d[0] for d in desc]
                    print(" | ".join(headers))
                    print("-" * 60)
                
                for row in result[:20]:  # Limit output
                    print(" | ".join(str(v) for v in row))
                
                if len(result) > 20:
                    print(f"... ({len(result)} total rows)")
            else:
                print("(no results)")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    con.close()
    print("\nGoodbye!")


def main():
    parser = argparse.ArgumentParser(
        description='Validate NetworkSim-Local database'
    )
    parser.add_argument(
        '--database',
        type=Path,
        default=None,
        help='Path to DuckDB database'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Start interactive query mode after validation'
    )
    
    args = parser.parse_args()
    
    # Find database
    script_dir = Path(__file__).parent
    db_path = args.database or (script_dir.parent / 'data' / 'networksim-local.duckdb')
    
    # Also check alternate location
    if not db_path.exists():
        alt_path = script_dir.parent / 'data' / 'processed' / 'networksim.duckdb'
        if alt_path.exists():
            db_path = alt_path
    
    # Run validation
    valid = validate_database(db_path)
    
    if not valid:
        sys.exit(1)
    
    # Interactive mode
    if args.interactive:
        interactive_query(db_path)


if __name__ == '__main__':
    main()
