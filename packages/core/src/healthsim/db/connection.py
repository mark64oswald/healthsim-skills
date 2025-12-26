"""
Database connection management for HealthSim.

Provides:
- Automatic database creation on first access
- Connection pooling (via DuckDB's built-in)
- Path configuration (local vs cloud future)
"""

import os
from pathlib import Path
from typing import Optional
import duckdb

# Default database location
DEFAULT_DB_PATH = Path.home() / ".healthsim" / "healthsim.duckdb"


class DatabaseConnection:
    """Manages DuckDB connections for HealthSim."""
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[duckdb.DuckDBPyConnection] = None
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to database file. Uses DEFAULT_DB_PATH if not specified.
        """
        self.db_path = db_path or DEFAULT_DB_PATH
        self._ensure_directory()
    
    def _ensure_directory(self) -> None:
        """Create database directory if it doesn't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def connect(self) -> duckdb.DuckDBPyConnection:
        """
        Get or create database connection.
        
        Returns:
            Active DuckDB connection.
        """
        if self._connection is None:
            self._connection = duckdb.connect(str(self.db_path))
            self._initialize_if_needed()
        return self._connection
    
    def _initialize_if_needed(self) -> None:
        """Apply schema if this is a new database."""
        from .schema import apply_schema
        from .migrations import run_migrations
        
        # Check if schema_migrations table exists
        result = self._connection.execute("""
            SELECT count(*) FROM information_schema.tables 
            WHERE table_name = 'schema_migrations'
        """).fetchone()
        
        if result[0] == 0:
            # New database - apply full schema
            apply_schema(self._connection)
        else:
            # Existing database - run any pending migrations
            run_migrations(self._connection)
    
    def close(self) -> None:
        """Close the database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    @classmethod
    def get_instance(cls, db_path: Optional[Path] = None) -> 'DatabaseConnection':
        """
        Get singleton database connection instance.
        
        Args:
            db_path: Override default path (only used on first call).
            
        Returns:
            DatabaseConnection singleton.
        """
        if cls._instance is None:
            cls._instance = cls(db_path)
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (for testing)."""
        if cls._instance:
            cls._instance.close()
        cls._instance = None


def get_connection(db_path: Optional[Path] = None) -> duckdb.DuckDBPyConnection:
    """
    Convenience function to get database connection.
    
    Args:
        db_path: Optional path override (only used on first call).
    
    Returns:
        Active DuckDB connection.
    """
    return DatabaseConnection.get_instance(db_path).connect()
