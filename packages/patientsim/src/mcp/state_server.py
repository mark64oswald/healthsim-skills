"""MCP Server for PatientSim state management capabilities.

This module implements a Model Context Protocol (MCP) server that exposes
scenario save/load tools for workspace persistence.

Tools:
- save_scenario: Save workspace to a named scenario
- load_scenario: Load a scenario into workspace
- list_saved_scenarios: List saved scenarios with filtering
- delete_scenario: Delete a saved scenario
"""

import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from patientsim.mcp.session import SessionManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("patientsim.mcp.state")

# Initialize MCP server
app = Server("patientsim-state")

# Session manager - this would be shared with generation server in practice
# For standalone operation, we create our own instance
session_manager = SessionManager()


def format_scenario_saved(scenario: Any) -> str:
    """Format scenario save confirmation."""
    lines = [
        f'**Saved: "{scenario.metadata.name}"**',
        "",
        "**Scenario Summary:**",
        f"- Scenario ID: `{scenario.metadata.workspace_id}`",
        f"- Patients: {scenario.get_entity_count('patients')}",
        f"- Total entities: {scenario.get_entity_count()}",
    ]

    if scenario.metadata.description:
        lines.append(f"- Description: {scenario.metadata.description}")

    if scenario.metadata.tags:
        lines.append(f"- Tags: {', '.join(scenario.metadata.tags)}")

    # Provenance breakdown
    prov = scenario.provenance_summary
    if prov.by_source_type:
        lines.append("")
        lines.append("**Provenance:**")
        if prov.by_source_type.get("generated", 0) > 0:
            lines.append(f"- Generated: {prov.by_source_type['generated']} entities")
        if prov.by_source_type.get("loaded", 0) > 0:
            lines.append(f"- Loaded: {prov.by_source_type['loaded']} entities")
        if prov.by_source_type.get("derived", 0) > 0:
            lines.append(f"- Derived: {prov.by_source_type['derived']} entities")

    if prov.skills_used:
        lines.append(f"- Skills used: {', '.join(prov.skills_used)}")

    lines.append("")
    lines.append(f'You can load this anytime with: `load "{scenario.metadata.name}"`')

    return "\n".join(lines)


def format_scenario_loaded(scenario: Any, summary: dict) -> str:
    """Format scenario load confirmation."""
    lines = [
        f'**Loaded: "{scenario.metadata.name}"**',
        "",
        f"- Patients loaded: {summary['patients_loaded']}",
        f"- Total entities: {summary['total_entities']}",
    ]

    if summary.get("patients_skipped", 0) > 0:
        lines.append(f"- Patients skipped (conflicts): {summary['patients_skipped']}")

    if summary.get("conflicts"):
        lines.append("")
        lines.append("**Conflicts:**")
        for conflict in summary["conflicts"]:
            lines.append(f"- MRN {conflict['mrn']}: {conflict['resolution']}")

    lines.append("")
    lines.append("Ready to continue! What would you like to work on?")

    return "\n".join(lines)


def format_scenario_list(scenarios: list[dict]) -> str:
    """Format list of saved scenarios."""
    if not scenarios:
        return "No saved scenarios found.\n\nGenerate some patients and use `save_scenario` to save your work."

    lines = ["**Your Saved Scenarios:**", ""]

    for s in scenarios:
        name = s["name"]
        created = s["created_at"][:10]  # Just the date
        patient_count = s["patient_count"]
        tags = ", ".join(s.get("tags", [])) if s.get("tags") else ""

        line = f"- **{name}** ({created}) - {patient_count} patients"
        if tags:
            line += f" [tags: {tags}]"
        if s.get("description"):
            line += f"\n  _{s['description']}_"

        lines.append(line)

    lines.append("")
    lines.append("Use `load_scenario` with a name to restore a scenario.")

    return "\n".join(lines)


def format_scenario_deleted(info: dict) -> str:
    """Format scenario deletion confirmation."""
    return f"**Deleted:** \"{info['name']}\"\n- {info['patient_count']} patients removed"


def format_error(message: str) -> str:
    """Format error message."""
    return f"**Error:** {message}"


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available state management tools."""
    return [
        Tool(
            name="save_scenario",
            description="Save the current workspace as a named scenario. Captures all patients and clinical data with provenance tracking.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the scenario (e.g., 'diabetes-cohort', 'ed-testing')",
                        "minLength": 1,
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of what this scenario contains",
                    },
                    "tags": {
                        "type": "array",
                        "description": "Optional tags for organization (e.g., ['training', 'diabetes'])",
                        "items": {"type": "string"},
                    },
                    "patient_ids": {
                        "type": "array",
                        "description": "Specific patient IDs to save (default: all patients)",
                        "items": {"type": "string"},
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="load_scenario",
            description="Load a saved scenario into the workspace. Can replace or merge with existing patients.",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario_id": {
                        "type": "string",
                        "description": "UUID of scenario to load (if known)",
                    },
                    "name": {
                        "type": "string",
                        "description": "Name to search for (fuzzy match)",
                    },
                    "mode": {
                        "type": "string",
                        "description": "Load mode: 'replace' clears workspace first, 'merge' adds to existing",
                        "enum": ["replace", "merge"],
                        "default": "replace",
                    },
                    "patient_ids": {
                        "type": "array",
                        "description": "Specific patient IDs to load (default: all patients)",
                        "items": {"type": "string"},
                    },
                },
            },
        ),
        Tool(
            name="list_saved_scenarios",
            description="List saved scenarios with optional filtering by name, description, or tags.",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Search string for name or description",
                    },
                    "tags": {
                        "type": "array",
                        "description": "Filter by tags (scenarios must have ALL specified tags)",
                        "items": {"type": "string"},
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum scenarios to return",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100,
                    },
                },
            },
        ),
        Tool(
            name="delete_scenario",
            description="Delete a saved scenario. This action cannot be undone.",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario_id": {
                        "type": "string",
                        "description": "UUID of scenario to delete",
                    },
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be true to confirm deletion",
                    },
                },
                "required": ["scenario_id", "confirm"],
            },
        ),
        Tool(
            name="workspace_summary",
            description="Get a summary of the current workspace state including patient count and provenance breakdown.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls for state management."""

    try:
        if name == "save_scenario":
            return await handle_save_scenario(arguments)
        elif name == "load_scenario":
            return await handle_load_scenario(arguments)
        elif name == "list_saved_scenarios":
            return await handle_list_scenarios(arguments)
        elif name == "delete_scenario":
            return await handle_delete_scenario(arguments)
        elif name == "workspace_summary":
            return await handle_workspace_summary(arguments)
        else:
            return [TextContent(type="text", text=format_error(f"Unknown tool: {name}"))]

    except Exception as e:
        logger.exception(f"Error in tool {name}")
        return [TextContent(type="text", text=format_error(str(e)))]


async def handle_save_scenario(arguments: dict) -> list[TextContent]:
    """Handle save_scenario tool call."""
    name = arguments.get("name")
    if not name:
        return [TextContent(type="text", text=format_error("Scenario name is required"))]

    # Check if workspace has content
    if session_manager.count() == 0:
        return [
            TextContent(
                type="text",
                text=format_error(
                    "Nothing to save. Generate some patients first with `generate_patient` or `generate_cohort`."
                ),
            )
        ]

    description = arguments.get("description")
    tags = arguments.get("tags", [])
    patient_ids = arguments.get("patient_ids")

    try:
        scenario = session_manager.save_scenario(
            name=name,
            description=description,
            tags=tags,
            patient_ids=patient_ids,
        )
        return [TextContent(type="text", text=format_scenario_saved(scenario))]

    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Failed to save scenario: {e}"))]


async def handle_load_scenario(arguments: dict) -> list[TextContent]:
    """Handle load_scenario tool call."""
    scenario_id = arguments.get("scenario_id")
    name = arguments.get("name")
    mode = arguments.get("mode", "replace")
    patient_ids = arguments.get("patient_ids")

    if not scenario_id and not name:
        # List recent scenarios to help user choose
        scenarios = session_manager.list_scenarios(limit=5)
        if scenarios:
            lines = [
                "Please specify a scenario to load. Recent scenarios:",
                "",
            ]
            for s in scenarios:
                lines.append(f"- **{s['name']}** ({s['created_at'][:10]})")
            lines.append("")
            lines.append("Use `load_scenario` with `name` or `scenario_id`.")
            return [TextContent(type="text", text="\n".join(lines))]
        else:
            return [
                TextContent(
                    type="text",
                    text="No scenarios found. Save your work first with `save_scenario`.",
                )
            ]

    try:
        # Warn if replacing non-empty workspace
        current_count = session_manager.count()
        if mode == "replace" and current_count > 0:
            # Note: In a real interactive scenario, we might prompt for confirmation
            # For now, we proceed but include a note in the response
            pass

        scenario, summary = session_manager.load_scenario(
            scenario_id=scenario_id,
            name=name,
            mode=mode,
            patient_ids=patient_ids,
        )

        result = format_scenario_loaded(scenario, summary)

        if mode == "replace" and current_count > 0:
            result = f"_Replaced {current_count} existing patients._\n\n" + result

        return [TextContent(type="text", text=result)]

    except FileNotFoundError:
        return [
            TextContent(
                type="text",
                text=format_error(f"Scenario not found: {scenario_id or name}"),
            )
        ]
    except ValueError as e:
        return [TextContent(type="text", text=format_error(str(e)))]
    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Failed to load scenario: {e}"))]


async def handle_list_scenarios(arguments: dict) -> list[TextContent]:
    """Handle list_saved_scenarios tool call."""
    search = arguments.get("search")
    tags = arguments.get("tags")
    limit = arguments.get("limit", 20)

    scenarios = session_manager.list_scenarios(
        search=search,
        tags=tags,
        limit=limit,
    )

    return [TextContent(type="text", text=format_scenario_list(scenarios))]


async def handle_delete_scenario(arguments: dict) -> list[TextContent]:
    """Handle delete_scenario tool call."""
    scenario_id = arguments.get("scenario_id")
    confirm = arguments.get("confirm", False)

    if not scenario_id:
        return [
            TextContent(
                type="text",
                text=format_error("scenario_id is required"),
            )
        ]

    if not confirm:
        return [
            TextContent(
                type="text",
                text="Deletion requires confirmation. Set `confirm: true` to proceed.",
            )
        ]

    info = session_manager.delete_scenario(scenario_id)

    if info:
        return [TextContent(type="text", text=format_scenario_deleted(info))]
    else:
        return [
            TextContent(
                type="text",
                text=format_error(f"Scenario not found: {scenario_id}"),
            )
        ]


async def handle_workspace_summary(_arguments: dict) -> list[TextContent]:
    """Handle workspace_summary tool call."""
    summary = session_manager.get_workspace_summary()

    if summary["patient_count"] == 0:
        return [
            TextContent(
                type="text",
                text="**Workspace is empty.**\n\nGenerate patients with `generate_patient` or load a scenario with `load_scenario`.",
            )
        ]

    lines = [
        "**Current Workspace:**",
        "",
        f"- Patients: {summary['patient_count']}",
    ]

    if summary["encounter_count"] > 0:
        lines.append(f"- Encounters: {summary['encounter_count']}")
    if summary["diagnosis_count"] > 0:
        lines.append(f"- Diagnoses: {summary['diagnosis_count']}")
    if summary["medication_count"] > 0:
        lines.append(f"- Medications: {summary['medication_count']}")
    if summary["lab_count"] > 0:
        lines.append(f"- Lab results: {summary['lab_count']}")
    if summary["vital_count"] > 0:
        lines.append(f"- Vital signs: {summary['vital_count']}")
    if summary["procedure_count"] > 0:
        lines.append(f"- Procedures: {summary['procedure_count']}")
    if summary["note_count"] > 0:
        lines.append(f"- Clinical notes: {summary['note_count']}")

    # Provenance breakdown
    prov = summary.get("provenance_summary", {})
    if prov:
        lines.append("")
        lines.append("**Provenance:**")
        if prov.get("generated", 0) > 0:
            lines.append(f"- Generated: {prov['generated']} patients")
        if prov.get("loaded", 0) > 0:
            lines.append(f"- Loaded: {prov['loaded']} patients")
        if prov.get("derived", 0) > 0:
            lines.append(f"- Derived: {prov['derived']} patients")

    return [TextContent(type="text", text="\n".join(lines))]


def get_session_manager() -> SessionManager:
    """Get the session manager instance for external use."""
    return session_manager


def set_session_manager(manager: SessionManager) -> None:
    """Set the session manager instance for shared use with other servers."""
    global session_manager
    session_manager = manager


async def main():
    """Run the state management MCP server."""
    logger.info("Starting PatientSim State Management MCP Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
