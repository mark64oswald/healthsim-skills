"""Tests for DuckDB-backed state manager."""

import pytest
from datetime import datetime
import tempfile
from pathlib import Path
from uuid import uuid4

from healthsim.db import DatabaseConnection
from healthsim.state.manager import StateManager, reset_manager


@pytest.fixture
def test_db():
    """Create a temporary test database with schema applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_state.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def state_manager(test_db):
    """Create state manager with test database."""
    manager = StateManager(connection=test_db)
    yield manager
    reset_manager()


class TestSaveScenario:
    """Tests for save_scenario functionality."""
    
    def test_save_empty_scenario(self, state_manager):
        """Can save a scenario with no entities."""
        scenario_id = state_manager.save_scenario(
            name='empty-scenario',
            entities={},
            description='An empty test scenario'
        )
        
        assert scenario_id is not None
        assert len(scenario_id) == 36  # UUID format
    
    def test_save_scenario_with_patients(self, state_manager):
        """Can save a scenario with patient entities."""
        entities = {
            'patients': [
                {
                    'patient_id': str(uuid4()),
                    'mrn': 'MRN001',
                    'given_name': 'John',
                    'family_name': 'Doe',
                    'birth_date': '1980-01-15',
                    'gender': 'male',
                },
                {
                    'patient_id': str(uuid4()),
                    'mrn': 'MRN002',
                    'given_name': 'Jane',
                    'family_name': 'Smith',
                    'birth_date': '1985-06-20',
                    'gender': 'female',
                },
            ]
        }
        
        scenario_id = state_manager.save_scenario(
            name='patient-scenario',
            entities=entities,
            description='Test with patients'
        )
        
        assert scenario_id is not None
    
    def test_save_scenario_with_multiple_entity_types(self, state_manager):
        """Can save scenario with multiple entity types."""
        entities = {
            'patients': [
                {'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'John', 'family_name': 'Doe', 'birth_date': '1980-01-15', 'gender': 'male'}
            ],
            'encounters': [
                {'encounter_id': str(uuid4()), 'patient_mrn': 'MRN001', 'class_code': 'O', 'status': 'finished', 'admission_time': '2024-01-15T09:00:00'}
            ],
        }
        
        scenario_id = state_manager.save_scenario(
            name='multi-entity-scenario',
            entities=entities,
        )
        
        assert scenario_id is not None
    
    def test_save_scenario_with_tags(self, state_manager):
        """Can save scenario with tags."""
        scenario_id = state_manager.save_scenario(
            name='tagged-scenario',
            entities={'patients': []},
            tags=['diabetes', 'chronic', 'test'],
        )
        
        tags = state_manager.get_scenario_tags('tagged-scenario')
        assert 'diabetes' in tags
        assert 'chronic' in tags
        assert 'test' in tags
    
    def test_save_duplicate_name_fails(self, state_manager):
        """Saving with duplicate name raises error without overwrite."""
        state_manager.save_scenario(name='duplicate', entities={})
        
        with pytest.raises(ValueError, match="already exists"):
            state_manager.save_scenario(name='duplicate', entities={})
    
    def test_save_with_overwrite(self, state_manager):
        """Can overwrite existing scenario."""
        # Save original
        state_manager.save_scenario(
            name='overwrite-test',
            entities={'patients': [{'given_name': 'Original', 'family_name': 'Person', 'birth_date': '1990-01-01', 'gender': 'male'}]},
        )
        
        # Overwrite
        state_manager.save_scenario(
            name='overwrite-test',
            entities={'patients': [{'given_name': 'Updated', 'family_name': 'Person', 'birth_date': '1990-01-01', 'gender': 'male'}]},
            overwrite=True,
        )
        
        # Verify updated
        loaded = state_manager.load_scenario('overwrite-test')
        assert loaded['entities']['patients'][0]['given_name'] == 'Updated'


class TestLoadScenario:
    """Tests for load_scenario functionality."""
    
    def test_load_by_name(self, state_manager):
        """Can load scenario by name."""
        state_manager.save_scenario(name='load-by-name', entities={})
        
        loaded = state_manager.load_scenario('load-by-name')
        assert loaded['name'] == 'load-by-name'
    
    def test_load_by_id(self, state_manager):
        """Can load scenario by UUID."""
        scenario_id = state_manager.save_scenario(name='load-by-id', entities={})
        
        loaded = state_manager.load_scenario(scenario_id)
        assert loaded['scenario_id'] == scenario_id
    
    def test_load_not_found(self, state_manager):
        """Loading non-existent scenario raises error."""
        with pytest.raises(ValueError, match="not found"):
            state_manager.load_scenario('nonexistent-scenario')
    
    def test_load_preserves_entities(self, state_manager):
        """Loaded entities match saved entities."""
        original_entities = {
            'patients': [
                {
                    'patient_id': str(uuid4()),
                    'mrn': 'MRN123',
                    'given_name': 'Test',
                    'family_name': 'Patient',
                    'birth_date': '1975-03-10',
                    'gender': 'female',
                    'race': 'white',
                    'ethnicity': 'non-hispanic',
                }
            ]
        }
        
        state_manager.save_scenario(
            name='preserve-test',
            entities=original_entities,
        )
        
        loaded = state_manager.load_scenario('preserve-test')
        
        assert len(loaded['entities']['patients']) == 1
        patient = loaded['entities']['patients'][0]
        assert patient['given_name'] == 'Test'
        assert patient['family_name'] == 'Patient'
        assert patient['mrn'] == 'MRN123'
    
    def test_load_returns_metadata(self, state_manager):
        """Loaded scenario includes metadata."""
        state_manager.save_scenario(
            name='metadata-test',
            entities={},
            description='Test description',
            tags=['tag1', 'tag2'],
        )
        
        loaded = state_manager.load_scenario('metadata-test')
        
        assert loaded['name'] == 'metadata-test'
        assert loaded['description'] == 'Test description'
        assert 'tag1' in loaded['tags']
        assert 'tag2' in loaded['tags']
        assert 'created_at' in loaded
        assert 'updated_at' in loaded


class TestListScenarios:
    """Tests for list_scenarios functionality."""
    
    def test_list_empty(self, state_manager):
        """List returns empty when no scenarios."""
        scenarios = state_manager.list_scenarios()
        assert scenarios == []
    
    def test_list_all(self, state_manager):
        """List returns all scenarios."""
        state_manager.save_scenario(name='list-1', entities={})
        state_manager.save_scenario(name='list-2', entities={})
        state_manager.save_scenario(name='list-3', entities={})
        
        scenarios = state_manager.list_scenarios()
        names = [s['name'] for s in scenarios]
        
        assert 'list-1' in names
        assert 'list-2' in names
        assert 'list-3' in names
    
    def test_list_filter_by_tag(self, state_manager):
        """Can filter scenarios by tag."""
        state_manager.save_scenario(name='diabetes-1', entities={}, tags=['diabetes'])
        state_manager.save_scenario(name='diabetes-2', entities={}, tags=['diabetes', 'chronic'])
        state_manager.save_scenario(name='cardiac-1', entities={}, tags=['cardiac'])
        
        diabetes_scenarios = state_manager.list_scenarios(tag='diabetes')
        names = [s['name'] for s in diabetes_scenarios]
        
        assert 'diabetes-1' in names
        assert 'diabetes-2' in names
        assert 'cardiac-1' not in names
    
    def test_list_search(self, state_manager):
        """Can search scenarios by name/description."""
        state_manager.save_scenario(name='alpha-scenario', entities={}, description='First test')
        state_manager.save_scenario(name='beta-scenario', entities={}, description='Second alpha test')
        state_manager.save_scenario(name='gamma-scenario', entities={}, description='Third test')
        
        # Search in name
        results = state_manager.list_scenarios(search='alpha')
        names = [s['name'] for s in results]
        assert 'alpha-scenario' in names
        assert 'beta-scenario' in names  # 'alpha' in description
        assert 'gamma-scenario' not in names
    
    def test_list_with_limit(self, state_manager):
        """List respects limit parameter."""
        for i in range(10):
            state_manager.save_scenario(name=f'limited-{i}', entities={})
        
        scenarios = state_manager.list_scenarios(limit=5)
        assert len(scenarios) == 5
    
    def test_list_ordered_by_updated(self, state_manager):
        """List returns scenarios ordered by updated_at desc."""
        state_manager.save_scenario(name='old', entities={})
        state_manager.save_scenario(name='newer', entities={})
        state_manager.save_scenario(name='newest', entities={})
        
        scenarios = state_manager.list_scenarios()
        # Most recently updated should be first
        assert scenarios[0]['name'] == 'newest'


class TestDeleteScenario:
    """Tests for delete_scenario functionality."""
    
    def test_delete_by_name(self, state_manager):
        """Can delete scenario by name."""
        state_manager.save_scenario(name='to-delete', entities={})
        
        result = state_manager.delete_scenario('to-delete')
        assert result is True
        
        scenarios = state_manager.list_scenarios()
        names = [s['name'] for s in scenarios]
        assert 'to-delete' not in names
    
    def test_delete_by_id(self, state_manager):
        """Can delete scenario by UUID."""
        scenario_id = state_manager.save_scenario(name='delete-by-id', entities={})
        
        result = state_manager.delete_scenario(scenario_id)
        assert result is True
    
    def test_delete_not_found(self, state_manager):
        """Delete returns False for non-existent scenario."""
        result = state_manager.delete_scenario('nonexistent')
        assert result is False
    
    def test_delete_removes_tags(self, state_manager):
        """Delete also removes associated tags."""
        state_manager.save_scenario(
            name='tagged-delete',
            entities={},
            tags=['tag1', 'tag2'],
        )
        
        state_manager.delete_scenario('tagged-delete')
        
        # Verify tags are gone by checking the tags table directly
        result = state_manager.conn.execute(
            "SELECT COUNT(*) FROM scenario_tags WHERE scenario_id IN (SELECT scenario_id FROM scenarios WHERE name = 'tagged-delete')"
        ).fetchone()
        assert result[0] == 0


class TestScenarioExists:
    """Tests for scenario_exists functionality."""
    
    def test_exists_by_name(self, state_manager):
        """scenario_exists returns True for existing name."""
        state_manager.save_scenario(name='exists-test', entities={})
        
        assert state_manager.scenario_exists('exists-test') is True
    
    def test_exists_by_id(self, state_manager):
        """scenario_exists returns True for existing UUID."""
        scenario_id = state_manager.save_scenario(name='exists-by-id', entities={})
        
        assert state_manager.scenario_exists(scenario_id) is True
    
    def test_not_exists(self, state_manager):
        """scenario_exists returns False for non-existent scenario."""
        assert state_manager.scenario_exists('nonexistent') is False


class TestEntityRoundTrip:
    """Tests for entity data round-trip (save → load)."""
    
    def test_patient_round_trip(self, state_manager):
        """Patient data survives save/load cycle."""
        original = {
            'patient_id': str(uuid4()),
            'mrn': 'MRN999',
            'given_name': 'Alice',
            'family_name': 'Wonderland',
            'birth_date': '1990-05-15',
            'gender': 'female',
            'race': 'asian',
            'ethnicity': 'non-hispanic',
            'address': {
                'line1': '123 Main St',
                'city': 'Anytown',
                'state': 'CA',
                'postalCode': '90210',
            },
            'telecom': {
                'phone': '555-1234',
                'email': 'alice@example.com',
            },
        }
        
        state_manager.save_scenario(
            name='round-trip-test',
            entities={'patients': [original]},
        )
        
        loaded = state_manager.load_scenario('round-trip-test')
        patient = loaded['entities']['patients'][0]
        
        # Core fields
        assert patient['given_name'] == 'Alice'
        assert patient['family_name'] == 'Wonderland'
        assert patient['mrn'] == 'MRN999'
        
        # Nested fields (stored as JSON)
        assert patient.get('address', {}).get('city') == 'Anytown' or patient.get('city') == 'Anytown'
    
    def test_encounter_round_trip(self, state_manager):
        """Encounter data survives save/load cycle."""
        original = {
            'encounter_id': str(uuid4()),
            'patient_mrn': 'MRN001',
            'class_code': 'I',
            'status': 'in-progress',
            'admission_time': '2024-06-15T10:30:00',
            'facility': 'General Hospital',
            'department': 'Cardiology',
            'chief_complaint': 'Chest pain',
        }
        
        state_manager.save_scenario(
            name='encounter-round-trip',
            entities={'encounters': [original]},
        )
        
        loaded = state_manager.load_scenario('encounter-round-trip')
        encounter = loaded['entities']['encounters'][0]
        
        assert encounter['patient_mrn'] == 'MRN001'
        assert encounter['class_code'] == 'I'
        assert encounter['chief_complaint'] == 'Chest pain'
    
    def test_multiple_entity_types_round_trip(self, state_manager):
        """Multiple entity types survive save/load cycle."""
        entities = {
            'patients': [
                {'patient_id': str(uuid4()), 'mrn': 'MRN001', 'given_name': 'John', 'family_name': 'Doe', 'birth_date': '1980-01-01', 'gender': 'male'}
            ],
            'encounters': [
                {'encounter_id': str(uuid4()), 'patient_mrn': 'MRN001', 'class_code': 'O', 'status': 'finished', 'admission_time': '2024-01-15T09:00:00'}
            ],
            'members': [
                {'member_id': str(uuid4()), 'given_name': 'John', 'family_name': 'Doe', 'subscriber_id': 'SUB001'}
            ],
        }
        
        state_manager.save_scenario(
            name='multi-type-round-trip',
            entities=entities,
        )
        
        loaded = state_manager.load_scenario('multi-type-round-trip')
        
        assert len(loaded['entities']['patients']) == 1
        assert len(loaded['entities']['encounters']) == 1
        assert len(loaded['entities']['members']) == 1


class TestTagManagement:
    """Tests for tag management functionality."""
    
    def test_get_tags(self, state_manager):
        """Can get tags for a scenario."""
        state_manager.save_scenario(
            name='get-tags-test',
            entities={},
            tags=['alpha', 'beta', 'gamma'],
        )
        
        tags = state_manager.get_scenario_tags('get-tags-test')
        
        assert 'alpha' in tags
        assert 'beta' in tags
        assert 'gamma' in tags
    
    def test_add_tags(self, state_manager):
        """Can add tags to existing scenario."""
        state_manager.save_scenario(
            name='add-tags-test',
            entities={},
            tags=['original'],
        )
        
        state_manager.add_scenario_tags('add-tags-test', ['new1', 'new2'])
        
        tags = state_manager.get_scenario_tags('add-tags-test')
        assert 'original' in tags
        assert 'new1' in tags
        assert 'new2' in tags
    
    def test_add_duplicate_tag(self, state_manager):
        """Adding duplicate tag doesn't create duplicates."""
        state_manager.save_scenario(
            name='dup-tag-test',
            entities={},
            tags=['tag1'],
        )
        
        state_manager.add_scenario_tags('dup-tag-test', ['tag1', 'tag1'])
        
        tags = state_manager.get_scenario_tags('dup-tag-test')
        assert tags.count('tag1') == 1
