"""State management for HealthSim products.

This module provides the foundational classes for workspace persistence
and entity provenance tracking across all HealthSim products:

- PatientSim: Clinical patient data
- MemberSim: Health plan member and claims data
- RxMemberSim: Pharmacy benefit and prescription data

Core Classes:
    Provenance: Tracks entity lineage (loaded, generated, derived)
    ProvenanceSummary: Aggregate statistics for workspace provenance
    SourceType: Enum of provenance source types
    EntityWithProvenance: Generic entity wrapper with provenance
    Workspace: Saved collection of entities
    WorkspaceMetadata: Workspace descriptive information
    Session: Abstract base for product-specific sessions
    SessionManager: Abstract base for workspace operations

Auto-Persist Classes (Structured RAG Pattern):
    AutoPersistService: Main service for auto-persistence
    PersistResult: Result of entity persistence
    QueryResult: Paginated query results
    ScenarioSummary: Token-efficient scenario summary
    ScenarioBrief: Brief scenario info for listing

Usage:
    Products extend Session and SessionManager with their entity types:

    ```python
    from healthsim.state import Session, SessionManager, Provenance

    class PatientSession(Session[Patient]):
        # PatientSim-specific implementation
        ...

    class PatientSessionManager(SessionManager[Patient]):
        @property
        def product_name(self) -> str:
            return "patientsim"
        ...
    ```

    For auto-persist:

    ```python
    from healthsim.state import get_auto_persist_service

    service = get_auto_persist_service()
    result = service.persist_entities(entities, 'patient')
    summary = service.get_scenario_summary(scenario_id=result.scenario_id)
    ```
"""

from .entity import EntityWithProvenance
from .provenance import Provenance, ProvenanceSummary, SourceType
from .session import Session, SessionManager
from .workspace import WORKSPACES_DIR, Workspace, WorkspaceMetadata
from .manager import (
    StateManager,
    get_manager,
    save_scenario,
    load_scenario,
    list_scenarios,
    delete_scenario,
    scenario_exists,
    export_scenario_to_json,
    import_scenario_from_json,
)
from .legacy import (
    export_to_json,
    import_from_json,
    list_legacy_scenarios,
    migrate_legacy_scenario,
    migrate_all_legacy_scenarios,
    LEGACY_SCENARIOS_PATH,
)

# Auto-persist (Structured RAG Pattern)
from .auto_naming import (
    generate_scenario_name,
    extract_keywords,
    ensure_unique_name,
    sanitize_name,
    parse_scenario_name,
)
from .summary import (
    ScenarioSummary,
    generate_summary,
    get_scenario_by_name,
)
from .auto_persist import (
    AutoPersistService,
    PersistResult,
    QueryResult,
    ScenarioBrief,
    get_auto_persist_service,
    reset_service,
)

__all__ = [
    # Provenance
    "Provenance",
    "ProvenanceSummary",
    "SourceType",
    # Entity
    "EntityWithProvenance",
    # Workspace (file-based)
    "Workspace",
    "WorkspaceMetadata",
    "WORKSPACES_DIR",
    # Session (abstract)
    "Session",
    "SessionManager",
    # State Manager (DuckDB-backed)
    "StateManager",
    "get_manager",
    "save_scenario",
    "load_scenario",
    "list_scenarios",
    "delete_scenario",
    "scenario_exists",
    "export_scenario_to_json",
    "import_scenario_from_json",
    # Legacy JSON support
    "export_to_json",
    "import_from_json",
    "list_legacy_scenarios",
    "migrate_legacy_scenario",
    "migrate_all_legacy_scenarios",
    "LEGACY_SCENARIOS_PATH",
    # Auto-Naming
    "generate_scenario_name",
    "extract_keywords",
    "ensure_unique_name",
    "sanitize_name",
    "parse_scenario_name",
    # Summary
    "ScenarioSummary",
    "generate_summary",
    "get_scenario_by_name",
    # Auto-Persist Service
    "AutoPersistService",
    "PersistResult",
    "QueryResult",
    "ScenarioBrief",
    "get_auto_persist_service",
    "reset_service",
]
