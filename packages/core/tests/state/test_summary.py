"""Tests for scenario summary generation."""

import pytest
from datetime import datetime
import tempfile
from pathlib import Path
from uuid import uuid4

from healthsim.db import DatabaseConnection
from healthsim.state.summary import (
    ScenarioSummary,
    generate_summary,
    get_scenario_by_name,
)


@pytest.fixture
def test_db():
    """Create a temporary test database with schema applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_summary.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def scenario_with_data(test_db):
    """Create a scenario with sample data."""
    scenario_id = str(uuid4())
    now = datetime.utcnow()
    
    # Create scenario
    test_db.execute("""
        INSERT INTO scenarios (scenario_id, name, description, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, [scenario_id, 'test-scenario', 'A test scenario', now, now])
    
    # Add tags
    test_db.execute("""
        INSERT INTO scenario_tags (scenario_id, tag) VALUES (?, ?)
    """, [scenario_id, 'diabetes'])
    test_db.execute("""
        INSERT INTO scenario_tags (scenario_id, tag) VALUES (?, ?)
    """, [scenario_id, 'test'])
    
    # Add patients (using correct column names from schema)
    for i in range(5):
        test_db.execute("""
            INSERT INTO patients (id, scenario_id, mrn, given_name, family_name, 
                                  birth_date, gender, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            str(uuid4()), scenario_id, f'MRN{i:03d}', f'Patient{i}', 'Test',
            f'19{50 + i * 5}-01-01', 'male' if i % 2 == 0 else 'female', now
        ])
    
    return scenario_id


class TestScenarioSummary:
    """Tests for ScenarioSummary dataclass."""
    
    def test_to_dict(self):
        """Can convert summary to dict."""
        summary = ScenarioSummary(
            scenario_id='abc123',
            name='test-scenario',
            entity_counts={'patients': 10, 'encounters': 25},
            tags=['diabetes'],
        )
        
        d = summary.to_dict()
        
        assert d['scenario_id'] == 'abc123'
        assert d['name'] == 'test-scenario'
        assert d['entity_counts']['patients'] == 10
        assert 'diabetes' in d['tags']
    
    def test_to_json(self):
        """Can convert summary to JSON string."""
        summary = ScenarioSummary(
            scenario_id='abc123',
            name='test-scenario',
        )
        
        json_str = summary.to_json()
        
        assert 'abc123' in json_str
        assert 'test-scenario' in json_str
    
    def test_from_dict(self):
        """Can create summary from dict."""
        data = {
            'scenario_id': 'abc123',
            'name': 'test-scenario',
            'entity_counts': {'patients': 5},
            'tags': ['test'],
        }
        
        summary = ScenarioSummary.from_dict(data)
        
        assert summary.scenario_id == 'abc123'
        assert summary.name == 'test-scenario'
        assert summary.entity_counts['patients'] == 5
    
    def test_total_entities(self):
        """Can calculate total entity count."""
        summary = ScenarioSummary(
            scenario_id='abc123',
            name='test',
            entity_counts={'patients': 10, 'encounters': 20, 'claims': 15},
        )
        
        assert summary.total_entities() == 45
    
    def test_token_estimate(self):
        """Can estimate token count."""
        summary = ScenarioSummary(
            scenario_id='abc123',
            name='test-scenario',
            entity_counts={'patients': 10},
        )
        
        tokens = summary.token_estimate()
        
        # Should be a reasonable positive number
        assert tokens > 0
        assert tokens < 1000  # Simple summary should be small


class TestGenerateSummary:
    """Tests for generate_summary function."""
    
    def test_generate_basic_summary(self, test_db, scenario_with_data):
        """Can generate summary for scenario with data."""
        summary = generate_summary(
            scenario_id=scenario_with_data,
            include_samples=False,
            connection=test_db
        )
        
        assert summary.scenario_id == scenario_with_data
        assert summary.name == 'test-scenario'
        assert summary.entity_counts.get('patients', 0) == 5
    
    def test_generate_with_samples(self, test_db, scenario_with_data):
        """Summary includes samples when requested."""
        summary = generate_summary(
            scenario_id=scenario_with_data,
            include_samples=True,
            samples_per_type=3,
            connection=test_db
        )
        
        assert 'patients' in summary.samples
        assert len(summary.samples['patients']) <= 3
    
    def test_generate_includes_tags(self, test_db, scenario_with_data):
        """Summary includes scenario tags."""
        summary = generate_summary(
            scenario_id=scenario_with_data,
            connection=test_db
        )
        
        assert 'diabetes' in summary.tags
        assert 'test' in summary.tags
    
    def test_generate_not_found(self, test_db):
        """Raises error for non-existent scenario."""
        with pytest.raises(ValueError, match="not found"):
            generate_summary(
                scenario_id=str(uuid4()),
                connection=test_db
            )


class TestGetScenarioByName:
    """Tests for get_scenario_by_name function."""
    
    def test_exact_match(self, test_db, scenario_with_data):
        """Can find scenario by exact name."""
        result = get_scenario_by_name('test-scenario', test_db)
        
        assert result == scenario_with_data
    
    def test_case_insensitive(self, test_db, scenario_with_data):
        """Can find scenario with case-insensitive match."""
        result = get_scenario_by_name('TEST-SCENARIO', test_db)
        
        assert result == scenario_with_data
    
    def test_partial_match(self, test_db, scenario_with_data):
        """Can find scenario by partial name."""
        result = get_scenario_by_name('test', test_db)
        
        assert result == scenario_with_data
    
    def test_not_found(self, test_db):
        """Returns None for non-existent scenario."""
        result = get_scenario_by_name('nonexistent', test_db)
        
        assert result is None
