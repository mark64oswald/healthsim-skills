"""
HealthSim MCP Server.

Provides MCP tools for interacting with the HealthSim DuckDB database.
Uses dual-connection pattern for concurrent access:
- Persistent read-only connection for queries (shared lock)
- On-demand write connection for modifications (brief exclusive lock)

See docs/mcp/duckdb-connection-architecture.md for design details.

Tools provided:
- healthsim_list_scenarios: List all saved scenarios
- healthsim_load_scenario: Load a scenario by name/ID
- healthsim_save_scenario: Save a new scenario
- healthsim_delete_scenario: Delete a scenario
- healthsim_query: Execute read-only SQL queries
- healthsim_get_summary: Get token-efficient scenario summary
- healthsim_query_reference: Query PopulationSim reference data
- healthsim_tables: List all tables in the database

Usage:
    python healthsim_mcp.py
    
Configuration in claude_desktop_config.json:
    "healthsim-mcp": {
        "command": "python",
        "args": ["/path/to/healthsim_mcp.py"]
    }

Environment Variables:
    HEALTHSIM_DB_PATH: Override default database path
"""

import json
import os
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import duckdb
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

# Add healthsim to path
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))

from healthsim.db import DEFAULT_DB_PATH
from healthsim.state import StateManager


# =============================================================================
# Configuration from Environment
# =============================================================================

# Allow override via environment variable
DB_PATH = Path(os.environ.get("HEALTHSIM_DB_PATH", str(DEFAULT_DB_PATH)))

# Log startup configuration (to stderr so it doesn't interfere with MCP protocol)
print(f"HealthSim MCP Server starting...", file=sys.stderr)
print(f"  Database: {DB_PATH}", file=sys.stderr)
print(f"  Connection mode: dual (read-only persistent + on-demand write)", file=sys.stderr)
print(f"  DB exists: {DB_PATH.exists()}", file=sys.stderr)


# =============================================================================
# Connection Manager - Dual Connection Pattern
# =============================================================================

class ConnectionManager:
    """
    Manages DuckDB connections using dual-connection pattern.
    
    - Read operations: Use persistent read-only connection (shared lock)
    - Write operations: Use on-demand connection (brief exclusive lock)
    
    This allows external processes (pytest, CLI tools) to access the database
    concurrently while MCP server is running.
    """
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._read_conn: Optional[duckdb.DuckDBPyConnection] = None
        self._read_manager: Optional[StateManager] = None
    
    def get_read_connection(self) -> duckdb.DuckDBPyConnection:
        """
        Get persistent read-only connection.
        
        Uses shared lock - allows concurrent readers from other processes.
        Connection is reused across all read operations.
        """
        if self._read_conn is None:
            self._read_conn = duckdb.connect(str(self.db_path), read_only=True)
            print(f"  Opened read-only connection to {self.db_path}", file=sys.stderr)
        return self._read_conn
    
    def get_read_manager(self) -> StateManager:
        """Get StateManager backed by read-only connection."""
        if self._read_manager is None:
            self._read_manager = StateManager(connection=self.get_read_connection())
        return self._read_manager
    
    @contextmanager
    def write_connection(self):
        """
        Context manager for write operations.
        
        Acquires exclusive lock, performs operation, releases immediately.
        Ensures write lock is held for minimum duration.
        
        Usage:
            with manager.write_connection() as conn:
                conn.execute("INSERT INTO ...")
        """
        conn = duckdb.connect(str(self.db_path))
        try:
            yield conn
        finally:
            conn.close()
    
    @contextmanager
    def write_manager(self):
        """
        Context manager for StateManager with write capability.
        
        Usage:
            with manager.write_manager() as state_mgr:
                state_mgr.save_scenario(...)
        """
        with self.write_connection() as conn:
            yield StateManager(connection=conn)
    
    def close(self):
        """Close all connections."""
        if self._read_conn:
            self._read_conn.close()
            self._read_conn = None
            self._read_manager = None
            print(f"  Closed read-only connection", file=sys.stderr)


# Global connection manager
_manager: Optional[ConnectionManager] = None


def _get_manager() -> ConnectionManager:
    """Get or create the connection manager."""
    global _manager
    if _manager is None:
        _manager = ConnectionManager(DB_PATH)
    return _manager


# Initialize the MCP server
mcp = FastMCP("healthsim_mcp")


# =============================================================================
# Pydantic Input Models
# =============================================================================

class ListScenariosInput(BaseModel):
    """Input for listing scenarios."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    tag: Optional[str] = Field(default=None, description="Filter by tag")
    search: Optional[str] = Field(default=None, description="Search in name/description")
    limit: int = Field(default=50, description="Maximum results", ge=1, le=200)


class LoadScenarioInput(BaseModel):
    """Input for loading a scenario."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name_or_id: str = Field(..., description="Scenario name or UUID", min_length=1)
    include_entities: bool = Field(default=True, description="Include full entity data")


class SaveScenarioInput(BaseModel):
    """Input for saving a scenario."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: str = Field(..., description="Unique scenario name", min_length=1, max_length=200)
    entities: Dict[str, List[Dict[str, Any]]] = Field(..., description="Entity dict: {type: [entities]}")
    description: Optional[str] = Field(default=None, description="Scenario description")
    tags: Optional[List[str]] = Field(default=None, description="Tags for filtering")
    overwrite: bool = Field(default=False, description="Overwrite if exists")


class DeleteScenarioInput(BaseModel):
    """Input for deleting a scenario."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name_or_id: str = Field(..., description="Scenario name or UUID", min_length=1)
    confirm: bool = Field(default=False, description="Must be True to delete")


class QueryInput(BaseModel):
    """Input for SQL queries."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    sql: str = Field(..., description="SQL query (SELECT only)", min_length=1)
    limit: int = Field(default=100, description="Max rows to return", ge=1, le=1000)


class GetSummaryInput(BaseModel):
    """Input for getting scenario summary."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    scenario_id_or_name: str = Field(..., description="Scenario name or UUID", min_length=1)
    include_samples: bool = Field(default=True, description="Include sample entities")
    samples_per_type: int = Field(default=3, description="Samples per entity type", ge=1, le=10)


class QueryReferenceInput(BaseModel):
    """Input for querying reference data."""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    table: str = Field(..., description="Reference table: places_county, places_tract, svi_county, svi_tract, adi_blockgroup")
    state: Optional[str] = Field(default=None, description="Filter by state abbreviation (e.g., 'CA')")
    county: Optional[str] = Field(default=None, description="Filter by county name")
    limit: int = Field(default=20, description="Max rows", ge=1, le=100)


# =============================================================================
# Tool Implementations - READ Operations (use persistent read connection)
# =============================================================================

@mcp.tool(
    name="healthsim_list_scenarios",
    annotations={
        "title": "List HealthSim Scenarios",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def list_scenarios(params: ListScenariosInput) -> str:
    """List all saved scenarios in the HealthSim database.
    
    Returns scenario names, descriptions, entity counts, and tags.
    Use this to discover available scenarios before loading them.
    
    Returns:
        JSON list of scenario summaries with: scenario_id, name, description,
        created_at, updated_at, entity_count, tags
    """
    manager = _get_manager().get_read_manager()
    
    scenarios = manager.list_scenarios(
        tag=params.tag,
        search=params.search,
        limit=params.limit,
    )
    
    # Format for readability
    result = []
    for s in scenarios:
        result.append({
            "scenario_id": s["scenario_id"],
            "name": s["name"],
            "description": s.get("description"),
            "entity_count": s.get("entity_count", 0),
            "tags": s.get("tags", []),
            "created_at": str(s.get("created_at", "")),
            "updated_at": str(s.get("updated_at", "")),
        })
    
    return json.dumps(result, indent=2, default=str)


@mcp.tool(
    name="healthsim_load_scenario",
    annotations={
        "title": "Load HealthSim Scenario",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def load_scenario(params: LoadScenarioInput) -> str:
    """Load a scenario by name or ID.
    
    Returns full scenario data including all entities. For large scenarios,
    consider using healthsim_get_summary instead for a token-efficient summary.
    
    Returns:
        JSON with scenario metadata and entities dict
    """
    manager = _get_manager().get_read_manager()
    
    try:
        scenario = manager.load_scenario(params.name_or_id)
        
        if not params.include_entities:
            # Return metadata only
            scenario.pop("entities", None)
        
        return json.dumps(scenario, indent=2, default=str)
    except ValueError as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_query",
    annotations={
        "title": "Query HealthSim Database",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def query(params: QueryInput) -> str:
    """Execute a SQL query against the HealthSim database.
    
    Only SELECT queries are allowed. Use this for:
    - Exploring reference data (ref_places_county, ref_svi_tract, etc.)
    - Querying entity tables (patients, members, encounters, claims)
    - Running analytics queries
    
    Available tables: SHOW TABLES for full list.
    
    Returns:
        JSON with columns and rows
    """
    conn = _get_manager().get_read_connection()
    
    # Basic SQL injection protection
    sql_lower = params.sql.lower().strip()
    if not sql_lower.startswith(("select", "show", "describe", "with")):
        return json.dumps({
            "error": "Only SELECT, SHOW, DESCRIBE, and WITH queries are allowed",
        })
    
    # Check for dangerous keywords
    dangerous = ["insert", "update", "delete", "drop", "alter", "create", "truncate"]
    for keyword in dangerous:
        if keyword in sql_lower.split():
            return json.dumps({
                "error": f"Query contains forbidden keyword: {keyword}",
            })
    
    try:
        # Add LIMIT if not present
        if "limit" not in sql_lower:
            sql = f"{params.sql.rstrip(';')} LIMIT {params.limit}"
        else:
            sql = params.sql
        
        result = conn.execute(sql).fetchall()
        columns = [desc[0] for desc in conn.description]
        
        # Convert to list of dicts
        rows = []
        for row in result:
            rows.append({col: val for col, val in zip(columns, row)})
        
        return json.dumps({
            "columns": columns,
            "row_count": len(rows),
            "rows": rows,
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_get_summary",
    annotations={
        "title": "Get Scenario Summary",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def get_summary(params: GetSummaryInput) -> str:
    """Get a token-efficient summary of a scenario.
    
    Use this instead of load_scenario when you need context about a scenario
    without loading all entities (~500 tokens vs potentially 10K+).
    
    Returns:
        JSON with entity counts, statistics, and optional samples
    """
    manager = _get_manager().get_read_manager()
    
    try:
        summary = manager.get_summary(
            params.scenario_id_or_name,
            include_samples=params.include_samples,
            samples_per_type=params.samples_per_type,
        )
        
        # Convert to dict for JSON serialization
        return json.dumps(summary.to_dict(), indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_query_reference",
    annotations={
        "title": "Query Reference Data",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def query_reference(params: QueryReferenceInput) -> str:
    """Query PopulationSim reference data tables.
    
    Available tables:
    - places_county: CDC PLACES county-level health indicators (3,143 rows)
    - places_tract: CDC PLACES tract-level health indicators (83,522 rows)
    - svi_county: Social Vulnerability Index by county (3,144 rows)
    - svi_tract: Social Vulnerability Index by tract (84,120 rows)
    - adi_blockgroup: Area Deprivation Index by block group (242,336 rows)
    
    Returns:
        JSON with columns and filtered rows
    """
    conn = _get_manager().get_read_connection()
    
    # Map short names to full table names
    table_map = {
        "places_county": "ref_places_county",
        "places_tract": "ref_places_tract",
        "svi_county": "ref_svi_county",
        "svi_tract": "ref_svi_tract",
        "adi_blockgroup": "ref_adi_blockgroup",
    }
    
    table = table_map.get(params.table)
    if not table:
        return json.dumps({
            "error": f"Unknown table: {params.table}",
            "available": list(table_map.keys()),
        })
    
    # Build query with filters
    conditions = []
    query_params = []
    
    if params.state:
        conditions.append("stateabbr = ?")
        query_params.append(params.state.upper())
    
    if params.county:
        conditions.append("countyname ILIKE ?")
        query_params.append(f"%{params.county}%")
    
    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    sql = f"SELECT * FROM {table}{where_clause} LIMIT {params.limit}"
    
    try:
        result = conn.execute(sql, query_params).fetchall()
        columns = [desc[0] for desc in conn.description]
        
        rows = []
        for row in result:
            rows.append({col: val for col, val in zip(columns, row)})
        
        return json.dumps({
            "table": table,
            "columns": columns,
            "row_count": len(rows),
            "rows": rows,
        }, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="healthsim_tables",
    annotations={
        "title": "List Database Tables",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    }
)
def list_tables() -> str:
    """List all tables in the HealthSim database.
    
    Returns table names grouped by category:
    - Reference tables (ref_*): PopulationSim demographic/health data
    - Entity tables: patients, members, encounters, claims, etc.
    - System tables: scenarios, scenario_entities, schema_migrations
    
    Returns:
        JSON with categorized table names
    """
    conn = _get_manager().get_read_connection()
    
    result = conn.execute("SHOW TABLES").fetchall()
    tables = [row[0] for row in result]
    
    # Categorize
    reference = [t for t in tables if t.startswith("ref_")]
    system = ["scenarios", "scenario_entities", "scenario_tags", "schema_migrations"]
    entity = [t for t in tables if t not in reference and t not in system]
    
    return json.dumps({
        "reference_tables": reference,
        "entity_tables": entity,
        "system_tables": [t for t in system if t in tables],
        "total": len(tables),
    }, indent=2)


# =============================================================================
# Tool Implementations - WRITE Operations (use on-demand write connection)
# =============================================================================

@mcp.tool(
    name="healthsim_save_scenario",
    annotations={
        "title": "Save HealthSim Scenario",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
    }
)
def save_scenario(params: SaveScenarioInput) -> str:
    """Save a scenario to the HealthSim database.
    
    Entities should be a dict mapping entity type to list of entities:
    {
        "patients": [{...}, {...}],
        "encounters": [{...}],
        "claims": [{...}]
    }
    
    Supported entity types: patients, members, encounters, claims, 
    claim_lines, prescriptions, subjects, etc.
    
    Returns:
        JSON with scenario_id and status
    """
    try:
        # Use write connection for the save operation
        with _get_manager().write_manager() as manager:
            scenario_id = manager.save_scenario(
                name=params.name,
                entities=params.entities,
                description=params.description,
                tags=params.tags,
                overwrite=params.overwrite,
            )
        
        # Get entity counts
        entity_counts = {k: len(v) for k, v in params.entities.items()}
        
        return json.dumps({
            "status": "saved",
            "scenario_id": scenario_id,
            "name": params.name,
            "entity_counts": entity_counts,
            "total_entities": sum(entity_counts.values()),
        }, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": f"Save failed: {str(e)}"})


@mcp.tool(
    name="healthsim_delete_scenario",
    annotations={
        "title": "Delete HealthSim Scenario",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": False,
    }
)
def delete_scenario(params: DeleteScenarioInput) -> str:
    """Delete a scenario from the database.
    
    CAUTION: This permanently removes the scenario and all linked entities.
    You must set confirm=True to actually delete.
    
    Returns:
        JSON with deletion status
    """
    if not params.confirm:
        return json.dumps({
            "error": "Must set confirm=True to delete. This action is permanent.",
            "scenario": params.name_or_id,
        })
    
    try:
        # Use write connection for the delete operation
        with _get_manager().write_manager() as manager:
            deleted = manager.delete_scenario(params.name_or_id, confirm=True)
        
        return json.dumps({
            "status": "deleted" if deleted else "not_found",
            "scenario": params.name_or_id,
        })
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": f"Delete failed: {str(e)}"})


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    mcp.run()
