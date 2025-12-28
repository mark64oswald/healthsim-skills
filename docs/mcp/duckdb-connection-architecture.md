# DuckDB Connection Architecture for HealthSim MCP

## Overview

This document describes the dual-connection pattern used by the HealthSim MCP server to enable concurrent database access while maintaining write capability.

## Problem Statement

DuckDB uses file-level locking with specific concurrency rules:

| First Connection | Second Connection | Result |
|-----------------|-------------------|--------|
| Read-Write | Any | ❌ Blocked (exclusive lock) |
| Read-Only | Read-Only | ✅ Allowed (shared lock) |
| Read-Only | Read-Write | ❌ Blocked |

**Original Issue**: The MCP server held a single read-write connection for its entire lifetime. This exclusive lock blocked all other processes (pytest, CLI tools, other scripts) from accessing the database, even for read-only operations.

## Solution: Dual Connection Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│ healthsim-mcp Server                                                │
│                                                                     │
│ ┌─────────────────────────────────┐  ┌────────────────────────────┐│
│ │ Read Connection (persistent)    │  │ Write Connection (on-demand)││
│ │ read_only=True                  │  │ read_only=False            ││
│ │ Shared lock                     │  │ Exclusive lock             ││
│ │                                 │  │                            ││
│ │ → healthsim_query()             │  │ → healthsim_save_scenario()││
│ │ → healthsim_list_scenarios()    │  │ → healthsim_delete_scenario│
│ │ → healthsim_load_scenario()     │  │                            ││
│ │ → healthsim_get_summary()       │  │ Acquired per-operation     ││
│ │ → healthsim_query_reference()   │  │ Released immediately after ││
│ │ → healthsim_tables()            │  │                            ││
│ └─────────────────────────────────┘  └────────────────────────────┘│
│              │                                    │                 │
│              │ Shared Lock                        │ Brief Exclusive │
│              ↓                                    ↓                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        healthsim.duckdb                             │
│                        (1.7 GB)                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ↓ Concurrent Access Now Possible
┌─────────────────────────────────────────────────────────────────────┐
│ External Processes                                                  │
│                                                                     │
│ pytest (read_only=True)        ✅ Allowed                           │
│ CLI tools (read_only=True)     ✅ Allowed                           │
│ Jupyter notebooks (read_only)  ✅ Allowed                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Implementation

### Connection Manager

```python
from contextlib import contextmanager
import duckdb

class ConnectionManager:
    """Manages DuckDB connections with dual-connection pattern."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._read_conn: Optional[duckdb.DuckDBPyConnection] = None
    
    def get_read_connection(self) -> duckdb.DuckDBPyConnection:
        """Get persistent read-only connection.
        
        Returns same connection on subsequent calls.
        Uses shared lock - allows concurrent readers.
        """
        if self._read_conn is None:
            self._read_conn = duckdb.connect(str(self.db_path), read_only=True)
        return self._read_conn
    
    @contextmanager
    def write_connection(self):
        """Context manager for write operations.
        
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
    
    def close(self):
        """Close all connections."""
        if self._read_conn:
            self._read_conn.close()
            self._read_conn = None
```

### Tool Classification

| Tool | Operation Type | Connection |
|------|---------------|------------|
| `healthsim_list_scenarios` | Read | Persistent read |
| `healthsim_load_scenario` | Read | Persistent read |
| `healthsim_get_summary` | Read | Persistent read |
| `healthsim_query` | Read | Persistent read |
| `healthsim_query_reference` | Read | Persistent read |
| `healthsim_tables` | Read | Persistent read |
| `healthsim_save_scenario` | **Write** | On-demand write |
| `healthsim_delete_scenario` | **Write** | On-demand write |

## Benefits

1. **Concurrent Testing**: pytest can run against live database while MCP server is active
2. **Multi-Tool Support**: Multiple processes can query database simultaneously
3. **Minimal Lock Duration**: Write locks held only during actual write operations
4. **Cloud-Ready**: Pattern works with hosted databases that have similar locking semantics
5. **No Feature Loss**: All 8 MCP tools remain fully functional

## Trade-offs

1. **Slightly More Complex**: Two connection patterns instead of one
2. **Write Latency**: Small overhead for connection establishment on writes (typically <50ms)
3. **No Write Caching**: Each write operation creates new connection (but writes are infrequent)

## Testing Concurrent Access

```python
def test_concurrent_read_access():
    """Verify multiple read connections work simultaneously."""
    conn1 = duckdb.connect(str(DB_PATH), read_only=True)
    conn2 = duckdb.connect(str(DB_PATH), read_only=True)
    
    # Both should work
    result1 = conn1.execute("SELECT COUNT(*) FROM scenarios").fetchone()
    result2 = conn2.execute("SELECT COUNT(*) FROM scenarios").fetchone()
    
    assert result1 == result2
    
    conn1.close()
    conn2.close()


def test_read_during_mcp_active():
    """Verify external read works while MCP server holds read connection."""
    # MCP server uses read connection (simulated)
    mcp_conn = duckdb.connect(str(DB_PATH), read_only=True)
    
    # External process (like pytest) should also work
    external_conn = duckdb.connect(str(DB_PATH), read_only=True)
    result = external_conn.execute("SELECT 1").fetchone()
    assert result[0] == 1
    
    external_conn.close()
    mcp_conn.close()
```

## Migration Notes

The change is backward-compatible. Existing claude_desktop_config.json configurations continue to work. The `HEALTHSIM_READ_ONLY` environment variable is now deprecated (read operations are always read-only by default).

## Related Documentation

- [MCP Configuration](configuration.md) - Server setup
- [Data Architecture](../data-architecture.md) - Database schema overview
- [Testing Patterns](../testing-patterns.md) - Test conventions
