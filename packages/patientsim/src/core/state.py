"""State management models for PatientSim.

This module re-exports state management classes from healthsim-core,
providing backwards compatibility for PatientSim code.

The core classes (Provenance, EntityWithProvenance, etc.) are now
defined in healthsim.state and shared across all HealthSim products.

PatientSim-specific aliases:
- Cohort -> Workspace (cross-product term)
- CohortMetadata -> WorkspaceMetadata (cross-product term)
- COHORTS_DIR -> WORKSPACES_DIR (cross-product location)
"""

from pathlib import Path

# Re-export core classes from healthsim.state
from healthsim.state import (
    WORKSPACES_DIR,
    EntityWithProvenance,
    Provenance,
    ProvenanceSummary,
    Session,
    SessionManager,
    SourceType,
    Workspace,
    WorkspaceMetadata,
)

# Legacy aliases for backwards compatibility
Cohort = Workspace
CohortMetadata = WorkspaceMetadata

# Legacy location (deprecated, use WORKSPACES_DIR)
COHORTS_DIR = Path.home() / ".healthsim" / "cohorts"

__all__ = [
    # Core types (from healthsim.state)
    "SourceType",
    "Provenance",
    "ProvenanceSummary",
    "EntityWithProvenance",
    "Session",
    "SessionManager",
    # Cross-product names
    "Workspace",
    "WorkspaceMetadata",
    "WORKSPACES_DIR",
    # Legacy aliases (deprecated, use cross-product names)
    "Cohort",
    "CohortMetadata",
    "COHORTS_DIR",
]
