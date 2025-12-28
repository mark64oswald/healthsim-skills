# HealthSim MCP Server

MCP (Model Context Protocol) server for the HealthSim healthcare data simulation platform.

## Purpose

This server provides a **single connection holder** to the HealthSim DuckDB database, solving the file locking issue that prevents multiple processes from accessing the database simultaneously.

## Installation

```bash
cd /Users/markoswald/Developer/projects/healthsim-workspace/packages/mcp-server
pip install -e .
```

Or install dependencies directly:

```bash
pip install mcp pydantic duckdb
```

## Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "healthsim-mcp": {
      "command": "/Users/markoswald/anaconda3/bin/python",
      "args": [
        "/Users/markoswald/Developer/projects/healthsim-workspace/packages/mcp-server/healthsim_mcp.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/markoswald/Developer/projects/healthsim-workspace/packages/core/src:/Users/markoswald/Developer/projects/healthsim-workspace/packages/mcp-server"
      }
    }
  }
}
```

**Important**: 
1. Remove the old `healthsim-duckdb` entry to avoid conflicts
2. Adjust the Python path to match your environment (`which python3`)

## Available Tools

### Scenario Management

| Tool | Description |
|------|-------------|
| `healthsim_list_scenarios` | List all saved scenarios |
| `healthsim_load_scenario` | Load a scenario by name/ID |
| `healthsim_save_scenario` | Save entities as a scenario |
| `healthsim_delete_scenario` | Delete a scenario (requires confirm=True) |
| `healthsim_get_summary` | Get token-efficient scenario summary |

### Database Queries

| Tool | Description |
|------|-------------|
| `healthsim_query` | Execute read-only SQL queries |
| `healthsim_query_reference` | Query PopulationSim reference data |
| `healthsim_tables` | List all database tables |

## Reference Data Tables

| Table | Rows | Description |
|-------|------|-------------|
| `population.places_county` | 3,143 | CDC PLACES county-level health indicators |
| `population.places_tract` | 83,522 | CDC PLACES tract-level health indicators |
| `population.svi_county` | 3,144 | Social Vulnerability Index by county |
| `population.svi_tract` | 84,120 | Social Vulnerability Index by tract |
| `population.adi_blockgroup` | 242,336 | Area Deprivation Index by block group |

## Usage Examples

### List scenarios
```
Use healthsim_list_scenarios to see what's saved
```

### Query reference data
```
Use healthsim_query_reference with table="places_county" and state="CA"
```

### Save a scenario
```
Use healthsim_save_scenario with:
- name: "my-scenario"
- entities: {"patients": [...], "encounters": [...]}
- description: "Test scenario"
- tags: ["test", "demo"]
```

### Run custom SQL
```
Use healthsim_query with:
- sql: "SELECT countyname, obesity_crudeprev FROM ref_places_county WHERE stateabbr = 'TX' ORDER BY obesity_crudeprev DESC LIMIT 10"
```

## Database Location

The HealthSim database is stored at: `~/.healthsim/healthsim.duckdb`

## Troubleshooting

### Lock conflict error
If you see "Could not set lock on file", ensure:
1. The old `healthsim-duckdb` MCP server is removed from config
2. No Python processes are holding the database connection
3. Restart Claude Desktop after config changes

### Module not found
Ensure the healthsim core package is importable:
```bash
cd /Users/markoswald/Developer/projects/healthsim-workspace
source .venv/bin/activate
python -c "from healthsim.state import StateManager; print('OK')"
```
