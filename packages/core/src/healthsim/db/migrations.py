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
