"""
Tests for entity type taxonomy validation.

Ensures that reference data (providers, facilities, pharmacies) cannot be 
accidentally stored in scenarios, while scenario data and relationships are allowed.
"""

import pytest
import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from healthsim_mcp import (
    SCENARIO_ENTITY_TYPES,
    RELATIONSHIP_ENTITY_TYPES,
    REFERENCE_ENTITY_TYPES,
    ALLOWED_ENTITY_TYPES,
    validate_entity_types,
)


class TestEntityTypeTaxonomy:
    """Tests for the entity type taxonomy constants."""
    
    def test_scenario_entity_types_defined(self):
        """Scenario entity types should include PHI data types."""
        assert "patients" in SCENARIO_ENTITY_TYPES
        assert "members" in SCENARIO_ENTITY_TYPES
        assert "claims" in SCENARIO_ENTITY_TYPES
        assert "encounters" in SCENARIO_ENTITY_TYPES
    
    def test_relationship_entity_types_defined(self):
        """Relationship types should link scenario to reference data."""
        assert "pcp_assignments" in RELATIONSHIP_ENTITY_TYPES
        assert "network_contracts" in RELATIONSHIP_ENTITY_TYPES
    
    def test_reference_entity_types_defined(self):
        """Reference types should include real-world data that exists in shared tables."""
        assert "providers" in REFERENCE_ENTITY_TYPES
        assert "facilities" in REFERENCE_ENTITY_TYPES
        assert "pharmacies" in REFERENCE_ENTITY_TYPES
    
    def test_allowed_types_is_union(self):
        """Allowed types should be scenario data + relationships."""
        expected = SCENARIO_ENTITY_TYPES | RELATIONSHIP_ENTITY_TYPES
        assert ALLOWED_ENTITY_TYPES == expected
    
    def test_reference_types_not_in_allowed(self):
        """Reference types should NOT be in allowed types."""
        for ref_type in REFERENCE_ENTITY_TYPES:
            assert ref_type not in ALLOWED_ENTITY_TYPES


class TestValidateEntityTypes:
    """Tests for the validate_entity_types() function."""
    
    # === Tests for VALID entity types ===
    
    def test_patients_allowed(self):
        """Patients should be allowed (scenario data)."""
        entities = {"patients": [{"patient_id": "P001"}]}
        assert validate_entity_types(entities) is None
    
    def test_members_allowed(self):
        """Members should be allowed (scenario data)."""
        entities = {"members": [{"member_id": "M001"}]}
        assert validate_entity_types(entities) is None
    
    def test_claims_allowed(self):
        """Claims should be allowed (scenario data)."""
        entities = {"claims": [{"claim_id": "C001"}]}
        assert validate_entity_types(entities) is None
    
    def test_pcp_assignments_allowed(self):
        """PCP assignments should be allowed (relationship data)."""
        entities = {"pcp_assignments": [{"member_id": "M001", "provider_npi": "1234567890"}]}
        assert validate_entity_types(entities) is None
    
    def test_network_contracts_allowed(self):
        """Network contracts should be allowed (relationship data)."""
        entities = {"network_contracts": [{"plan_id": "PLAN001", "provider_npi": "1234567890"}]}
        assert validate_entity_types(entities) is None
    
    def test_multiple_allowed_types(self):
        """Multiple allowed types in one call should be valid."""
        entities = {
            "patients": [{"patient_id": "P001"}],
            "members": [{"member_id": "M001"}],
            "pcp_assignments": [{"member_id": "M001", "provider_npi": "123"}],
        }
        assert validate_entity_types(entities) is None
    
    # === Tests for REJECTED reference data types ===
    
    def test_providers_rejected(self):
        """Providers should be rejected (reference data)."""
        entities = {"providers": [{"npi": "1234567890", "name": "Dr. Test"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "REJECTED" in error
        assert "providers" in error.lower()
        assert "reference data" in error.lower()
    
    def test_facilities_rejected(self):
        """Facilities should be rejected (reference data)."""
        entities = {"facilities": [{"npi": "1234567890", "name": "Test Hospital"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "REJECTED" in error
    
    def test_pharmacies_rejected(self):
        """Pharmacies should be rejected (reference data)."""
        entities = {"pharmacies": [{"npi": "1234567890", "name": "Test Pharmacy"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "REJECTED" in error
    
    def test_hospitals_rejected(self):
        """Hospitals should be rejected (reference data)."""
        entities = {"hospitals": [{"npi": "1234567890", "name": "Test Hospital"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "REJECTED" in error
    
    def test_rejection_message_has_correct_approach(self):
        """Rejection message should explain the correct approach."""
        entities = {"providers": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        
        assert "healthsim_search_providers" in error
        assert "pcp_assignments" in error
        assert "network_contracts" in error
    
    def test_mixed_valid_and_reference_rejected(self):
        """If ANY type is reference data, the whole request should be rejected."""
        entities = {
            "patients": [{"patient_id": "P001"}],  # Valid
            "providers": [{"npi": "123"}],          # Invalid - reference data
        }
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "providers" in error.lower()
    
    # === Tests for singular/plural normalization ===
    
    def test_singular_patient_normalized(self):
        """Singular 'patient' should be normalized and allowed."""
        entities = {"patient": [{"patient_id": "P001"}]}
        assert validate_entity_types(entities) is None
    
    def test_singular_provider_rejected(self):
        """Singular 'provider' should be normalized and rejected."""
        entities = {"provider": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        assert error is not None
        assert "REJECTED" in error
    
    # === Tests for unknown types ===
    
    def test_unknown_type_returns_warning(self):
        """Unknown entity types should return a warning with allowed types."""
        entities = {"foobar": [{"id": "1"}]}
        error = validate_entity_types(entities)
        
        assert error is not None
        assert "Unknown entity type" in error
        assert "foobar" in error
        assert "patients" in error  # Should list allowed types


class TestValidationInTools:
    """Tests that validation is actually called in the MCP tools."""
    
    def test_add_entities_rejects_providers(self):
        """add_entities should reject providers with helpful error."""
        from healthsim_mcp import add_entities, AddEntitiesInput
        
        params = AddEntitiesInput(
            scenario_name="test-scenario",
            entities={"providers": [{"npi": "1234567890", "name": "Dr. Test"}]}
        )
        
        result = json.loads(add_entities(params))
        
        assert "error" in result
        assert "REJECTED" in result["error"]
        assert "providers" in result["error"].lower()
    
    def test_add_entities_allows_patients(self):
        """add_entities should allow patients (would need DB for full test)."""
        from healthsim_mcp import AddEntitiesInput
        
        # Just test the input validation passes (full test would need DB)
        params = AddEntitiesInput(
            scenario_name="test-scenario",
            entities={"patients": [{"patient_id": "P001", "name": "Test Patient"}]}
        )
        
        # Validation should pass - the function may fail later due to DB
        error = validate_entity_types(params.entities)
        assert error is None
    
    def test_save_scenario_rejects_facilities(self):
        """save_scenario should reject facilities with helpful error."""
        from healthsim_mcp import save_scenario, SaveScenarioInput
        
        params = SaveScenarioInput(
            name="test-scenario",
            entities={"facilities": [{"npi": "1234567890", "name": "Test Hospital"}]}
        )
        
        result = json.loads(save_scenario(params))
        
        assert "error" in result
        assert "REJECTED" in result["error"]


class TestRejectionMessageQuality:
    """Tests that rejection messages are helpful and educational."""
    
    def test_message_explains_why(self):
        """Rejection should explain WHY reference data shouldn't be stored."""
        entities = {"providers": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        
        assert "8.9M" in error or "millions" in error.lower() or "shared tables" in error.lower()
        assert "duplicates" in error.lower() or "copies" in error.lower()
    
    def test_message_shows_correct_pattern(self):
        """Rejection should show the correct relationship pattern."""
        entities = {"providers": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        
        # Should show an example of how to do it correctly
        assert "member_id" in error
        assert "provider_npi" in error
    
    def test_message_mentions_query_tools(self):
        """Rejection should point to query tools for accessing reference data."""
        entities = {"providers": [{"npi": "123"}]}
        error = validate_entity_types(entities)
        
        assert "healthsim_search_providers" in error or "healthsim_query" in error
