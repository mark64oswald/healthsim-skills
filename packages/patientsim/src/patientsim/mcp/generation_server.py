"""MCP Server for PatientSim generation capabilities.

This module implements a Model Context Protocol (MCP) server that exposes
patient generation tools for use with Claude Code and other MCP clients.

Enhanced to support conversational interactions with session state management.
"""

import json
import logging
import random
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from patientsim.core.generator import PatientGenerator
from patientsim.core.models import Gender
from patientsim.mcp.formatters import (
    format_cohort_summary,
    format_error,
    format_patient_summary,
    format_scenario_details,
    format_scenario_list,
    format_success,
)
from patientsim.mcp.session import SessionManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("patientsim.mcp")

# Initialize MCP server
app = Server("patientsim-generation")

# Initialize session manager
session_manager = SessionManager()


# Note: Serialization helpers removed - now using human-readable formatters
# For exporting data, use separate export tools with FHIR/HL7v2/MIMIC transformers


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="generate_patient",
            description="Generate a single synthetic patient. Returns human-readable summary and stores in session.",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario": {
                        "type": "string",
                        "description": "Optional scenario skill to use for generation",
                    },
                    "age_range": {
                        "type": "array",
                        "description": "Age range as [min, max] (default: [18, 85])",
                        "items": {"type": "integer", "minimum": 0, "maximum": 120},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                    "gender": {
                        "type": "string",
                        "description": "Gender: M, F, or 'any' for random",
                        "enum": ["M", "F", "any"],
                    },
                    "conditions": {
                        "type": "array",
                        "description": "List of conditions to include",
                        "items": {"type": "string"},
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                    },
                },
            },
        ),
        Tool(
            name="generate_cohort",
            description="Generate a cohort of patients. Returns summary with statistics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "count": {
                        "type": "integer",
                        "description": "Number of patients to generate",
                        "minimum": 1,
                        "maximum": 1000,
                    },
                    "scenario": {
                        "type": "string",
                        "description": "Optional scenario skill to use",
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Generation parameters (age_range, gender, etc.)",
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility",
                    },
                },
                "required": ["count"],
            },
        ),
        Tool(
            name="list_scenarios",
            description="List available scenario templates with descriptions",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="describe_scenario",
            description="Get detailed information about a specific scenario",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario_name": {
                        "type": "string",
                        "description": "Name of the scenario to describe",
                    },
                },
                "required": ["scenario_name"],
            },
        ),
        Tool(
            name="modify_patient",
            description="Modify an existing patient in the session",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "Patient session ID to modify",
                    },
                    "modifications": {
                        "type": "object",
                        "description": "Fields to modify (e.g., age, gender, diagnoses)",
                    },
                },
                "required": ["patient_id", "modifications"],
            },
        ),
        Tool(
            name="get_patient_details",
            description="Get detailed information about a patient in the session",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "Patient session ID or position (e.g., '1' for first patient)",
                    },
                    "section": {
                        "type": "string",
                        "description": "Specific section: demographics, encounter, diagnoses, labs, vitals",
                        "enum": ["demographics", "encounter", "diagnoses", "labs", "vitals"],
                    },
                },
                "required": ["patient_id"],
            },
        ),
        # State Management Tools
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
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "generate_patient":
            return await _generate_patient_tool(arguments)
        elif name == "generate_cohort":
            return await _generate_cohort_tool(arguments)
        elif name == "list_scenarios":
            return await _list_scenarios_tool(arguments)
        elif name == "describe_scenario":
            return await _describe_scenario_tool(arguments)
        elif name == "modify_patient":
            return await _modify_patient_tool(arguments)
        elif name == "get_patient_details":
            return await _get_patient_details_tool(arguments)
        # State Management Tools
        elif name == "save_scenario":
            return await _save_scenario_tool(arguments)
        elif name == "load_scenario":
            return await _load_scenario_tool(arguments)
        elif name == "list_saved_scenarios":
            return await _list_saved_scenarios_tool(arguments)
        elif name == "delete_scenario":
            return await _delete_scenario_tool(arguments)
        elif name == "workspace_summary":
            return await _workspace_summary_tool(arguments)
        else:
            error_msg = format_error(
                f"Unknown tool: {name}",
                "Available tools: generate_patient, generate_cohort, list_scenarios, describe_scenario, modify_patient, get_patient_details, save_scenario, load_scenario, list_saved_scenarios, delete_scenario, workspace_summary",
            )
            return [TextContent(type="text", text=error_msg)]
    except Exception as e:
        logger.exception(f"Error in tool {name}")
        error_msg = format_error(
            f"{type(e).__name__}: {str(e)}", "Please check the tool parameters and try again."
        )
        return [TextContent(type="text", text=error_msg)]


async def _generate_patient_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Generate a single patient with enhanced conversational output."""
    # Extract arguments
    _scenario = arguments.get("scenario")  # TODO: implement scenario-based generation
    age_range = arguments.get("age_range", [18, 85])
    gender_str = arguments.get("gender")
    conditions = arguments.get("conditions", [])
    seed = arguments.get("seed")

    # Validate age range
    if len(age_range) == 2 and age_range[0] > age_range[1]:
        error_msg = format_error(
            "Invalid age range: minimum age must be <= maximum age",
            f"You provided [{age_range[0]}, {age_range[1]}]. Try [{age_range[1]}, {age_range[0]}] instead.",
        )
        return [TextContent(type="text", text=error_msg)]

    # Convert gender
    gender = None
    if gender_str and gender_str != "any":
        try:
            gender = Gender(gender_str)
        except ValueError:
            error_msg = format_error(
                f"Invalid gender: {gender_str}", "Valid values are: M, F, or 'any'"
            )
            return [TextContent(type="text", text=error_msg)]

    # Generate patient
    generator = PatientGenerator(seed=seed)
    patient = generator.generate_patient(
        age_range=tuple(age_range) if age_range else (18, 85), gender=gender
    )

    # Generate encounter and clinical data
    encounter = generator.generate_encounter(patient)

    # Generate diagnoses (use conditions if specified, otherwise random)
    num_diagnoses = len(conditions) if conditions else random.randint(1, 3)
    diagnoses = [generator.generate_diagnosis(patient, encounter) for _ in range(num_diagnoses)]

    # Generate labs and vitals
    labs = [generator.generate_lab_result(patient, encounter) for _ in range(random.randint(3, 8))]
    vitals = generator.generate_vital_signs(patient, encounter)

    # Add to session
    session = session_manager.add_patient(
        patient=patient, encounter=encounter, diagnoses=diagnoses, labs=labs, vitals=vitals
    )

    # Format human-readable response
    response = format_patient_summary(session)

    # Add helpful next steps
    next_steps = [
        f"View full details: get_patient_details(patient_id='{session.id}')",
        "Export to FHIR, HL7v2, or MIMIC format",
        "Generate more patients to build a cohort",
    ]

    response += "\n\n" + format_success(
        f"Patient added to session (Total: {session_manager.count()})", next_steps
    )

    return [TextContent(type="text", text=response)]


async def _generate_cohort_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Generate a cohort of patients with enhanced output."""
    count = arguments["count"]
    _scenario = arguments.get("scenario")  # TODO: implement scenario-based generation
    parameters = arguments.get("parameters", {})
    seed = arguments.get("seed")

    # Extract parameters
    age_range = parameters.get("age_range", [18, 85])
    gender_str = parameters.get("gender")

    # Generate patients
    generator = PatientGenerator(seed=seed)
    sessions = []

    for _ in range(count):
        # Convert gender
        gender = None
        if gender_str and gender_str != "any":
            try:
                gender = Gender(gender_str)
            except ValueError:
                gender = None  # Invalid gender string, use random

        # Generate patient and encounter
        patient = generator.generate_patient(
            age_range=tuple(age_range) if age_range else (18, 85), gender=gender
        )
        encounter = generator.generate_encounter(patient)

        # Generate clinical data
        num_diagnoses = random.randint(1, 3)
        diagnoses = [generator.generate_diagnosis(patient, encounter) for _ in range(num_diagnoses)]

        num_labs = random.randint(3, 8)
        labs = [generator.generate_lab_result(patient, encounter) for _ in range(num_labs)]

        vitals = generator.generate_vital_signs(patient, encounter)

        # Add to session
        session = session_manager.add_patient(
            patient=patient, encounter=encounter, diagnoses=diagnoses, labs=labs, vitals=vitals
        )
        sessions.append(session)

    # Format human-readable response
    response = format_cohort_summary(sessions, _scenario)

    # Add helpful next steps
    next_steps = [
        "View details of a specific patient: get_patient_details(patient_id='<id>')",
        "Export cohort to FHIR, HL7v2, or MIMIC format",
        "Generate additional patients to expand the cohort",
    ]

    response += "\n\n" + format_success(f"Generated {count} patients successfully", next_steps)

    return [TextContent(type="text", text=response)]


async def _list_scenarios_tool(_arguments: dict[str, Any]) -> list[TextContent]:
    """List available scenario templates with human-readable format."""
    # Look for skills in the skills directory
    skills_dir = Path(__file__).parent.parent.parent / "skills" / "library"

    scenarios = {}
    if skills_dir.exists():
        for skill_file in skills_dir.glob("*.yaml"):
            try:
                import yaml

                with open(skill_file) as f:
                    skill_data = yaml.safe_load(f)

                scenarios[skill_file.stem] = {
                    "description": skill_data.get("description", "No description"),
                    "category": skill_data.get("category", "general"),
                    "file": str(skill_file),
                }
            except Exception as e:
                logger.warning(f"Error loading skill {skill_file}: {e}")

    if not scenarios:
        response = format_error(
            "No scenarios found", f"Check that scenario files exist in: {skills_dir}"
        )
    else:
        response = format_scenario_list(scenarios)
        response += "\n\n" + format_success(
            f"Found {len(scenarios)} available scenarios",
            ["Use describe_scenario(scenario_name='<name>') for details"],
        )

    return [TextContent(type="text", text=response)]


async def _describe_scenario_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Get detailed information about a specific scenario."""
    scenario_name = arguments["scenario_name"]

    # Look for the scenario file
    skills_dir = Path(__file__).parent.parent.parent / "skills" / "library"
    scenario_file = skills_dir / f"{scenario_name}.yaml"

    if not scenario_file.exists():
        error_msg = format_error(
            f"Scenario '{scenario_name}' not found",
            "Use list_scenarios() to see available scenarios",
        )
        return [TextContent(type="text", text=error_msg)]

    try:
        import yaml

        with open(scenario_file) as f:
            skill_data = yaml.safe_load(f)

        metadata = {
            "description": skill_data.get("description", "No description"),
            "parameters": skill_data.get("parameters", {}),
            "example": skill_data.get("example", ""),
            "category": skill_data.get("category", "general"),
        }

        response = format_scenario_details(scenario_name, metadata)
        return [TextContent(type="text", text=response)]

    except Exception as e:
        logger.exception(f"Error loading scenario {scenario_name}")
        error_msg = format_error(
            f"Failed to load scenario: {str(e)}", "Check that the scenario file is valid YAML"
        )
        return [TextContent(type="text", text=error_msg)]


async def _modify_patient_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Modify an existing patient in the session."""
    patient_id = arguments["patient_id"]
    modifications = arguments["modifications"]

    # Get the patient session
    session = session_manager.get_by_id(patient_id)

    if not session:
        # Try interpreting as position
        try:
            position = int(patient_id)
            session = session_manager.get_by_position(position)
        except (ValueError, TypeError):
            pass

    if not session:
        error_msg = format_error(
            f"Patient '{patient_id}' not found in session",
            f"Current session has {session_manager.count()} patients. Use get_patient_details() to view them.",
        )
        return [TextContent(type="text", text=error_msg)]

    # Update the patient
    try:
        updated_session = session_manager.update_patient(session.id, modifications)
        if updated_session:
            response = format_patient_summary(updated_session)
            response += "\n\n" + format_success(
                "Patient updated successfully",
                [f"View full details: get_patient_details(patient_id='{session.id}')"],
            )
        else:
            response = format_error(
                "Failed to update patient", "Check that the modification fields are valid"
            )
    except Exception as e:
        logger.exception(f"Error modifying patient {patient_id}")
        response = format_error(
            f"Failed to modify patient: {str(e)}",
            "Ensure modifications are compatible with the Patient model",
        )

    return [TextContent(type="text", text=response)]


async def _get_patient_details_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Get detailed information about a patient in the session."""
    patient_id = arguments["patient_id"]
    section = arguments.get("section")

    # Get the patient session
    session = session_manager.get_by_id(patient_id)

    if not session:
        # Try interpreting as position
        try:
            position = int(patient_id)
            session = session_manager.get_by_position(position)
        except (ValueError, TypeError):
            pass

    if not session:
        error_msg = format_error(
            f"Patient '{patient_id}' not found in session",
            f"Current session has {session_manager.count()} patients. Generate patients first with generate_patient() or generate_cohort().",
        )
        return [TextContent(type="text", text=error_msg)]

    # Format the response based on requested section
    if section:
        # Return specific section
        summary = session.to_summary()
        if section in summary:
            response = f"## {section.title()} for {session.patient.full_name}\n\n"
            response += json.dumps(summary[section], indent=2)
        else:
            response = format_error(
                f"Section '{section}' not found",
                "Available sections: demographics, encounter, diagnoses, labs, vitals",
            )
    else:
        # Return full patient summary
        response = format_patient_summary(session)

    return [TextContent(type="text", text=response)]


# === State Management Tool Handlers ===


def _format_scenario_saved(scenario: Any) -> str:
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
    lines.append(
        f'You can load this anytime with: `load_scenario(name="{scenario.metadata.name}")`'
    )

    return "\n".join(lines)


def _format_scenario_loaded(scenario: Any, summary: dict) -> str:
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


def _format_saved_scenario_list(scenarios: list[dict]) -> str:
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


async def _save_scenario_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle save_scenario tool call."""
    name = arguments.get("name")
    if not name:
        return [TextContent(type="text", text=format_error("Scenario name is required", ""))]

    # Check if workspace has content
    if session_manager.count() == 0:
        return [
            TextContent(
                type="text",
                text=format_error(
                    "Nothing to save",
                    "Generate some patients first with `generate_patient` or `generate_cohort`.",
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
        return [TextContent(type="text", text=_format_scenario_saved(scenario))]

    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Failed to save scenario: {e}", ""))]


async def _load_scenario_tool(arguments: dict[str, Any]) -> list[TextContent]:
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

        scenario, summary = session_manager.load_scenario(
            scenario_id=scenario_id,
            name=name,
            mode=mode,
            patient_ids=patient_ids,
        )

        result = _format_scenario_loaded(scenario, summary)

        if mode == "replace" and current_count > 0:
            result = f"_Replaced {current_count} existing patients._\n\n" + result

        return [TextContent(type="text", text=result)]

    except FileNotFoundError:
        return [
            TextContent(
                type="text",
                text=format_error(f"Scenario not found: {scenario_id or name}", ""),
            )
        ]
    except ValueError as e:
        return [TextContent(type="text", text=format_error(str(e), ""))]
    except Exception as e:
        return [TextContent(type="text", text=format_error(f"Failed to load scenario: {e}", ""))]


async def _list_saved_scenarios_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle list_saved_scenarios tool call."""
    search = arguments.get("search")
    tags = arguments.get("tags")
    limit = arguments.get("limit", 20)

    scenarios = session_manager.list_scenarios(
        search=search,
        tags=tags,
        limit=limit,
    )

    return [TextContent(type="text", text=_format_saved_scenario_list(scenarios))]


async def _delete_scenario_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle delete_scenario tool call."""
    scenario_id = arguments.get("scenario_id")
    confirm = arguments.get("confirm", False)

    if not scenario_id:
        return [
            TextContent(
                type="text",
                text=format_error("scenario_id is required", ""),
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
        return [
            TextContent(
                type="text",
                text=f"**Deleted:** \"{info['name']}\"\n- {info['patient_count']} patients removed",
            )
        ]
    else:
        return [
            TextContent(
                type="text",
                text=format_error(f"Scenario not found: {scenario_id}", ""),
            )
        ]


async def _workspace_summary_tool(_arguments: dict[str, Any]) -> list[TextContent]:
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


async def main() -> None:
    """Run the MCP server."""
    logger.info("Starting PatientSim MCP Generation Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
