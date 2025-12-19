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
"""

from .entity import EntityWithProvenance
from .provenance import Provenance, ProvenanceSummary, SourceType
from .session import Session, SessionManager
from .workspace import WORKSPACES_DIR, Workspace, WorkspaceMetadata

__all__ = [
    # Provenance
    "Provenance",
    "ProvenanceSummary",
    "SourceType",
    # Entity
    "EntityWithProvenance",
    # Workspace
    "Workspace",
    "WorkspaceMetadata",
    "WORKSPACES_DIR",
    # Session (abstract)
    "Session",
    "SessionManager",
]
