"""
Schema migration framework for HealthSim.

Migrations are applied at connection time, ensuring the database
schema is always up-to-date.
"""

from typing import List, Tuple
import duckdb

# Migration definitions: (version, description, sql)
# Format: Each migration is a tuple of (version, description, sql_statement)
# Versions should be comparable strings (e.g., "1.1", "1.2", "2.0")
MIGRATIONS: List[Tuple[str, str, str]] = [
    # Initial schema is applied via schema.py, not migrations
    # Add sequences for auto-increment IDs (fixes databases created before sequences added)
    ("1.1", "Add sequences for scenario_entities and scenario_tags", """
        CREATE SEQUENCE IF NOT EXISTS scenario_entities_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS scenario_tags_seq START 1;
    """),
    
    # Add scenario_id columns to canonical tables for auto-persist feature
    # This enables direct SQL queries on canonical tables filtered by scenario
    ("1.2", "Add scenario_id columns to canonical tables for auto-persist", """
        -- PatientSim tables
        ALTER TABLE patients ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE encounters ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE diagnoses ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE medications ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE lab_results ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE vital_signs ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE orders ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE clinical_notes ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        
        -- MemberSim tables
        ALTER TABLE members ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE claims ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE claim_lines ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        
        -- RxMemberSim tables
        ALTER TABLE prescriptions ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE pharmacy_claims ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        
        -- TrialSim tables
        ALTER TABLE subjects ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE trial_visits ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE adverse_events ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        ALTER TABLE exposures ADD COLUMN IF NOT EXISTS scenario_id VARCHAR;
        
        -- Indexes for scenario filtering
        CREATE INDEX IF NOT EXISTS idx_patients_scenario ON patients(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_encounters_scenario ON encounters(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_diagnoses_scenario ON diagnoses(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_medications_scenario ON medications(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_lab_results_scenario ON lab_results(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_vital_signs_scenario ON vital_signs(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_orders_scenario ON orders(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_clinical_notes_scenario ON clinical_notes(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_members_scenario ON members(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_claims_scenario ON claims(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_claim_lines_scenario ON claim_lines(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_prescriptions_scenario ON prescriptions(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_pharmacy_claims_scenario ON pharmacy_claims(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_subjects_scenario ON subjects(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_trial_visits_scenario ON trial_visits(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_adverse_events_scenario ON adverse_events(scenario_id);
        CREATE INDEX IF NOT EXISTS idx_exposures_scenario ON exposures(scenario_id);
    """),
]


def get_current_version(conn: duckdb.DuckDBPyConnection) -> str:
    """
    Get the current schema version from the database.
    
    Args:
        conn: DuckDB connection to check.
        
    Returns:
        Current schema version string.
    """
    result = conn.execute("""
        SELECT version FROM schema_migrations 
        ORDER BY applied_at DESC LIMIT 1
    """).fetchone()
    return result[0] if result else "0.0"


def get_applied_migrations(conn: duckdb.DuckDBPyConnection) -> List[str]:
    """
    Get list of all applied migration versions.
    
    Args:
        conn: DuckDB connection to check.
        
    Returns:
        List of applied version strings.
    """
    result = conn.execute("""
        SELECT version FROM schema_migrations ORDER BY applied_at
    """).fetchall()
    return [row[0] for row in result]


def run_migrations(conn: duckdb.DuckDBPyConnection) -> List[str]:
    """
    Run any pending migrations.
    
    Args:
        conn: DuckDB connection to apply migrations to.
        
    Returns:
        List of applied migration versions.
    """
    current = get_current_version(conn)
    applied = []
    
    for version, description, sql in MIGRATIONS:
        if version > current:
            # Execute the migration
            conn.execute(sql)
            
            # Record the migration
            conn.execute("""
                INSERT INTO schema_migrations (version, description)
                VALUES (?, ?)
            """, [version, description])
            
            applied.append(version)
    
    return applied


def get_pending_migrations(conn: duckdb.DuckDBPyConnection) -> List[Tuple[str, str]]:
    """
    Get list of pending migrations (not yet applied).
    
    Args:
        conn: DuckDB connection to check.
        
    Returns:
        List of (version, description) tuples for pending migrations.
    """
    current = get_current_version(conn)
    return [(v, d) for v, d, _ in MIGRATIONS if v > current]
