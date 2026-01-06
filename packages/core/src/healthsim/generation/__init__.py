"""Data generation framework.

This module provides base classes and utilities for generating
synthetic data with reproducibility support.

The two-phase architecture:
  Phase 1 (Building): Conversational → ProfileSpecification JSON
  Phase 2 (Execution): ProfileSpecification → Generated Data
"""

from healthsim.generation.base import BaseGenerator, PersonGenerator
from healthsim.generation.cohort import (
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
)
from healthsim.generation.distributions import (
    AgeDistribution,
    AgeBandDistribution,
    CategoricalDistribution,
    ConditionalDistribution,
    ExplicitDistribution,
    LogNormalDistribution,
    NormalDistribution,
    UniformDistribution,
    WeightedChoice,
    create_distribution,
)
from healthsim.generation.profile_schema import (
    ClinicalSpec,
    ConditionSpec,
    CoverageSpec,
    DemographicsSpec,
    DistributionSpec,
    DistributionType,
    GenerationSpec,
    GeographyReference,
    OutputSpec,
    ProfileSpecification,
    PROFILE_TEMPLATES,
)
from healthsim.generation.profile_executor import (
    ExecutionResult,
    GeneratedEntity,
    HierarchicalSeedManager,
    ProfileExecutor,
    ValidationMetric,
    ValidationReport,
    execute_profile,
)
from healthsim.generation.reproducibility import SeedManager
from healthsim.generation.reference_profiles import (
    DemographicProfile,
    GeographyLevel,
    GeographyReference as GeoReference,
    ReferenceProfileResolver,
    create_hybrid_profile,
    list_counties,
    list_states,
    merge_profile_with_reference,
    resolve_geography,
)
from healthsim.generation.journey_engine import (
    BaseEventType,
    DelaySpec,
    EventCondition,
    EventDefinition,
    JourneyEngine,
    JourneySpecification,
    MemberEventType,
    PatientEventType,
    RxEventType,
    Timeline,
    TimelineEvent,
    TrialEventType,
    create_journey_engine,
    create_simple_journey,
    get_journey_template,
    JOURNEY_TEMPLATES,
)
from healthsim.generation.triggers import (
    CrossProductCoordinator,
    LinkedEntity,
    RegisteredTrigger,
    TriggerPriority,
    TriggerRegistry,
    create_coordinator,
)
from healthsim.generation.handlers import (
    PatientSimHandlers,
    MemberSimHandlers,
    RxMemberSimHandlers,
    TrialSimHandlers,
    create_patientsim_handlers,
    create_membersim_handlers,
    create_rxmembersim_handlers,
    create_trialsim_handlers,
    register_all_handlers,
)
from healthsim.generation.cross_domain_sync import (
    CrossDomainSync,
    SyncConfig,
    SyncReport,
    ProductType,
    TriggerType,
    TriggerSpec,
    TriggerResult,
    PersonIdentity,
    IdentityRegistry,
    CorrelatorType,
    create_cross_domain_sync,
    hash_ssn,
)
from healthsim.generation.journey_validation import (
    ValidationSeverity,
    ValidationCategory,
    ValidationIssue,
    ValidationResult,
    JourneySpecValidator,
    TimelineValidator,
    CrossEventValidator,
    JourneyValidator,
    validate_journey_spec,
    validate_timeline,
    validate_events,
    create_journey_validator,
)
from healthsim.generation.orchestrator import (
    ProfileJourneyOrchestrator,
    EntityWithTimeline,
    OrchestratorResult,
    orchestrate,
)
from healthsim.generation.skill_reference import (
    SkillReference,
    ResolvedParameters,
    SkillResolver,
    ParameterResolver,
    get_skill_resolver,
    get_parameter_resolver,
    resolve_skill_ref,
)
from healthsim.generation.skill_journeys import (
    SKILL_AWARE_TEMPLATES,
    list_skill_aware_templates,
    get_skill_aware_template,
)

__all__ = [
    # Generators
    "BaseGenerator",
    "PersonGenerator",
    "CohortGenerator",
    "CohortConstraints",
    "CohortProgress",
    # Distributions
    "WeightedChoice",
    "NormalDistribution",
    "UniformDistribution",
    "AgeDistribution",
    "LogNormalDistribution",
    "CategoricalDistribution",
    "AgeBandDistribution",
    "ExplicitDistribution",
    "ConditionalDistribution",
    "create_distribution",
    # Profile Schema
    "ProfileSpecification",
    "GenerationSpec",
    "DemographicsSpec",
    "ClinicalSpec",
    "CoverageSpec",
    "ConditionSpec",
    "DistributionSpec",
    "DistributionType",
    "GeographyReference",
    "OutputSpec",
    "PROFILE_TEMPLATES",
    # Profile Executor
    "ProfileExecutor",
    "ExecutionResult",
    "GeneratedEntity",
    "HierarchicalSeedManager",
    "ValidationReport",
    "ValidationMetric",
    "execute_profile",
    # Reproducibility
    "SeedManager",
    # Reference Profiles
    "ReferenceProfileResolver",
    "DemographicProfile",
    "GeographyLevel",
    "GeoReference",
    "resolve_geography",
    "list_counties",
    "list_states",
    "create_hybrid_profile",
    "merge_profile_with_reference",
    # Journey Engine
    "JourneyEngine",
    "JourneySpecification",
    "Timeline",
    "TimelineEvent",
    "EventDefinition",
    "EventCondition",
    "DelaySpec",
    "BaseEventType",
    "PatientEventType",
    "MemberEventType",
    "RxEventType",
    "TrialEventType",
    "create_journey_engine",
    "create_simple_journey",
    "get_journey_template",
    "JOURNEY_TEMPLATES",
    # Cross-Product Triggers
    "TriggerRegistry",
    "RegisteredTrigger",
    "TriggerPriority",
    "CrossProductCoordinator",
    "LinkedEntity",
    "create_coordinator",
    # Product Handlers
    "PatientSimHandlers",
    "MemberSimHandlers",
    "RxMemberSimHandlers",
    "TrialSimHandlers",
    "create_patientsim_handlers",
    "create_membersim_handlers",
    "create_rxmembersim_handlers",
    "create_trialsim_handlers",
    "register_all_handlers",
    # Cross-Domain Sync
    "CrossDomainSync",
    "SyncConfig",
    "SyncReport",
    "ProductType",
    "TriggerType",
    "TriggerSpec",
    "TriggerResult",
    "PersonIdentity",
    "IdentityRegistry",
    "CorrelatorType",
    "create_cross_domain_sync",
    "hash_ssn",
    # Journey Validation
    "ValidationSeverity",
    "ValidationCategory",
    "ValidationIssue",
    "ValidationResult",
    "JourneySpecValidator",
    "TimelineValidator",
    "CrossEventValidator",
    "JourneyValidator",
    "validate_journey_spec",
    "validate_timeline",
    "validate_events",
    "create_journey_validator",
    # Orchestrator
    "ProfileJourneyOrchestrator",
    "EntityWithTimeline",
    "OrchestratorResult",
    "orchestrate",
    # Skill Reference
    "SkillReference",
    "ResolvedParameters",
    "SkillResolver",
    "ParameterResolver",
    "get_skill_resolver",
    "get_parameter_resolver",
    "resolve_skill_ref",
    # Skill-Aware Journeys
    "SKILL_AWARE_TEMPLATES",
    "list_skill_aware_templates",
    "get_skill_aware_template",
]
