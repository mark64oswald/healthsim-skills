"""
Phase 5: Integration and Performance Tests for Auto-Persist.

Tests full workflows across multiple operations:
- End-to-end persist → query → clone → merge → export workflows
- Performance testing with large batches (100-1000 entities)
- Edge cases and error handling
- Cross-product data integration

These tests validate the complete auto-persist feature set working together.
"""

import pytest
import json
import csv
import tempfile
import time
from pathlib import Path
from datetime import datetime, timedelta
from uuid import uuid4
import random

from healthsim.db import DatabaseConnection
from healthsim.state.auto_persist import (
    AutoPersistService,
    get_auto_persist_service,
    reset_service,
    PersistResult,
    CloneResult,
    MergeResult,
    ExportResult,
    CANONICAL_TABLES,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def test_db():
    """Create a temporary test database with schema applied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_integration.duckdb"
        db_conn = DatabaseConnection(db_path)
        conn = db_conn.connect()
        yield conn
        db_conn.close()


@pytest.fixture
def service(test_db):
    """Create a fresh AutoPersistService for each test."""
    reset_service()
    return AutoPersistService(test_db)


@pytest.fixture
def export_dir():
    """Create a temporary directory for exports."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def generate_patients(count: int) -> list:
    """Generate a batch of patient entities."""
    first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Martinez', 'Wilson']
    genders = ['male', 'female']
    
    patients = []
    for i in range(count):
        birth_year = random.randint(1940, 2005)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        
        patients.append({
            'patient_id': str(uuid4()),
            'given_name': random.choice(first_names),
            'family_name': random.choice(last_names),
            'gender': random.choice(genders),
            'birth_date': f'{birth_year}-{birth_month:02d}-{birth_day:02d}',
        })
    return patients


def generate_members(count: int) -> list:
    """Generate a batch of member entities."""
    first_names = ['Maria', 'James', 'Patricia', 'Robert', 'Linda', 'Michael', 'Barbara', 'William']
    last_names = ['Anderson', 'Taylor', 'Thomas', 'Moore', 'Jackson', 'White', 'Harris', 'Martin']
    
    members = []
    for i in range(count):
        birth_year = random.randint(1935, 1959)  # Medicare-age
        members.append({
            'member_id': str(uuid4()),
            'given_name': random.choice(first_names),
            'family_name': random.choice(last_names),
            'birth_date': f'{birth_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}',
            'plan_type': random.choice(['HMO', 'PPO', 'PFFS']),
            'group_id': f'GRP{random.randint(1000, 9999)}',  # Use correct column name
        })
    return members


# ============================================================================
# Integration Tests - Full Workflows
# ============================================================================

class TestEndToEndWorkflows:
    """Test complete workflows from persist through export."""
    
    def test_persist_query_export_workflow(self, service, export_dir):
        """Test: persist → query → export to all formats."""
        # Step 1: Persist patients
        patients = generate_patients(50)
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='workflow-test-1',
            tags=['integration', 'workflow'],
        )
        
        assert result.entities_persisted == 50
        scenario_id = result.scenario_id
        
        # Step 2: Query to verify (use results, not rows)
        query_result = service.query_scenario(
            scenario_id,
            "SELECT COUNT(*) as cnt FROM patients",
        )
        assert query_result.results[0]['cnt'] == 50
        
        # Step 3: Export to JSON (provide full file path, not directory)
        json_path = export_dir / "workflow-test-1.json"
        json_export = service.export_to_json(scenario_id, str(json_path))
        assert json_export.entities_exported.get('patients', 0) == 50
        assert Path(json_export.file_path).exists()
        
        # Verify JSON content (check for scenario info, not metadata)
        with open(json_export.file_path, 'r') as f:
            json_data = json.load(f)
        # Check the scenario exists in the data
        assert 'patients' in json_data.get('entities', json_data)
        
        # Step 4: Export to CSV (provide directory path)
        csv_dir = export_dir / "csv-export"
        csv_export = service.export_to_csv(scenario_id, str(csv_dir))
        assert csv_export.entities_exported.get('patients', 0) == 50
        
        csv_path = Path(csv_export.file_path) / 'patients.csv'
        assert csv_path.exists()
        
        # Verify CSV content
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 50
    
    def test_persist_clone_modify_merge_workflow(self, service):
        """Test: persist → clone → add data → merge back."""
        # Step 1: Create base scenario
        patients_a = generate_patients(20)
        result_a = service.persist_entities(
            entities=patients_a,
            entity_type='patient',
            scenario_name='base-cohort',
            tags=['base'],
        )
        base_id = result_a.scenario_id
        
        # Step 2: Clone for variant (use new_scenario_id, not target_scenario_id)
        clone = service.clone_scenario(
            base_id,
            new_name='variant-cohort',
            tags=['variant'],
        )
        variant_id = clone.new_scenario_id
        assert clone.entities_cloned.get('patients', 0) == 20
        
        # Step 3: Add more patients to variant
        patients_b = generate_patients(10)
        service.persist_entities(
            entities=patients_b,
            entity_type='patient',
            scenario_id=variant_id,
        )
        
        # Verify variant has 30 patients
        query_variant = service.query_scenario(
            variant_id,
            "SELECT COUNT(*) as cnt FROM patients",
        )
        assert query_variant.results[0]['cnt'] == 30
        
        # Step 4: Merge base and variant
        merged = service.merge_scenarios(
            source_scenario_ids=[base_id, variant_id],
            target_name='merged-cohort',
            conflict_strategy='skip',
        )
        
        # Should have combined unique patients
        total = merged.entities_merged.get('patients', 0)
        assert total >= 30  # At least the 30 from variant
    
    def test_tag_filter_clone_workflow(self, service):
        """Test: create tagged scenarios → filter by tag → clone filtered."""
        # Create several scenarios with different tags
        for i in range(5):
            patients = generate_patients(10)
            tags = ['batch']
            if i % 2 == 0:
                tags.append('even')
            else:
                tags.append('odd')
            
            service.persist_entities(
                entities=patients,
                entity_type='patient',
                scenario_name=f'tagged-scenario-{i}',
                tags=tags,
            )
        
        # Filter by 'even' tag
        even_scenarios = service.scenarios_by_tag('even')
        assert len(even_scenarios) == 3  # 0, 2, 4
        
        # Clone one of the filtered scenarios (ScenarioBrief is an object)
        clone = service.clone_scenario(
            even_scenarios[0].scenario_id,  # Use attribute access
            new_name='cloned-even',
            tags=['cloned', 'even'],
        )
        assert clone.total_entities == 10
        
        # Verify clone has correct tags
        clone_tags = service.get_tags(clone.new_scenario_id)
        assert 'cloned' in clone_tags
        assert 'even' in clone_tags


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Performance tests with large batches."""
    
    def test_persist_100_patients(self, service):
        """Test persisting 100 patients - baseline performance."""
        patients = generate_patients(100)
        
        start = time.time()
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='perf-100',
        )
        elapsed = time.time() - start
        
        assert result.entities_persisted == 100
        assert elapsed < 5.0, f"100 patients took {elapsed:.2f}s (should be < 5s)"
        print(f"\n  100 patients: {elapsed:.3f}s ({100/elapsed:.0f} entities/sec)")
    
    def test_persist_500_patients(self, service):
        """Test persisting 500 patients - medium batch."""
        patients = generate_patients(500)
        
        start = time.time()
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='perf-500',
        )
        elapsed = time.time() - start
        
        assert result.entities_persisted == 500
        assert elapsed < 15.0, f"500 patients took {elapsed:.2f}s (should be < 15s)"
        print(f"\n  500 patients: {elapsed:.3f}s ({500/elapsed:.0f} entities/sec)")
    
    def test_persist_1000_patients(self, service):
        """Test persisting 1000 patients - large batch."""
        patients = generate_patients(1000)
        
        start = time.time()
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='perf-1000',
        )
        elapsed = time.time() - start
        
        assert result.entities_persisted == 1000
        assert elapsed < 30.0, f"1000 patients took {elapsed:.2f}s (should be < 30s)"
        print(f"\n  1000 patients: {elapsed:.3f}s ({1000/elapsed:.0f} entities/sec)")
    
    def test_clone_large_scenario(self, service):
        """Test cloning a large scenario (patients only)."""
        # Create large scenario with patients only
        patients = generate_patients(500)
        
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='large-for-clone',
        )
        scenario_id = result.scenario_id
        
        # Clone
        start = time.time()
        clone = service.clone_scenario(scenario_id, new_name='large-clone')
        elapsed = time.time() - start
        
        assert clone.entities_cloned.get('patients', 0) == 500
        assert elapsed < 10.0, f"Cloning 500 entities took {elapsed:.2f}s"
        print(f"\n  Clone 500 entities: {elapsed:.3f}s")
    
    def test_merge_multiple_scenarios(self, service):
        """Test merging multiple scenarios."""
        # Create 5 scenarios
        scenario_ids = []
        for i in range(5):
            patients = generate_patients(50)
            result = service.persist_entities(
                entities=patients,
                entity_type='patient',
                scenario_name=f'merge-source-{i}',
            )
            scenario_ids.append(result.scenario_id)
        
        # Merge all
        start = time.time()
        merged = service.merge_scenarios(
            source_scenario_ids=scenario_ids,
            target_name='merged-5-sources',
            conflict_strategy='skip',
        )
        elapsed = time.time() - start
        
        total_merged = sum(merged.entities_merged.values())
        assert total_merged == 250  # 5 × 50 patients
        assert elapsed < 10.0, f"Merging 5 scenarios took {elapsed:.2f}s"
        print(f"\n  Merge 5 scenarios (250 entities): {elapsed:.3f}s")
    
    def test_export_large_scenario(self, service, export_dir):
        """Test exporting a large scenario."""
        # Create large scenario
        patients = generate_patients(500)
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='large-for-export',
        )
        
        # Export to JSON
        start = time.time()
        json_path = export_dir / "large-export.json"
        json_export = service.export_scenario(
            result.scenario_id,
            format='json',
            output_path=str(json_path),
        )
        json_elapsed = time.time() - start
        
        assert json_export.entities_exported.get('patients', 0) == 500
        assert json_elapsed < 10.0, f"Export to JSON took {json_elapsed:.2f}s"
        print(f"\n  Export 500 to JSON: {json_elapsed:.3f}s ({json_export.file_size_bytes/1024:.1f} KB)")
        
        # Export to CSV
        start = time.time()
        csv_dir = export_dir / "csv-large"
        csv_export = service.export_scenario(
            result.scenario_id,
            format='csv',
            output_path=str(csv_dir),
        )
        csv_elapsed = time.time() - start
        
        assert csv_export.entities_exported.get('patients', 0) == 500
        assert csv_elapsed < 10.0, f"Export to CSV took {csv_elapsed:.2f}s"
        print(f"  Export 500 to CSV: {csv_elapsed:.3f}s ({csv_export.file_size_bytes/1024:.1f} KB)")
    
    def test_query_large_dataset(self, service):
        """Test querying a large dataset."""
        # Create large scenario
        patients = generate_patients(1000)
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='large-for-query',
        )
        
        # Simple count query
        start = time.time()
        count_result = service.query_scenario(
            result.scenario_id,
            "SELECT COUNT(*) as cnt FROM patients",
        )
        count_elapsed = time.time() - start
        assert count_result.results[0]['cnt'] == 1000
        print(f"\n  COUNT query on 1000: {count_elapsed:.4f}s")
        
        # Filtered query
        start = time.time()
        filter_result = service.query_scenario(
            result.scenario_id,
            "SELECT * FROM patients WHERE gender = 'female' LIMIT 100",
        )
        filter_elapsed = time.time() - start
        assert len(filter_result.results) <= 100
        print(f"  Filtered query: {filter_elapsed:.4f}s")
        
        # Aggregation query
        start = time.time()
        agg_result = service.query_scenario(
            result.scenario_id,
            """SELECT gender, COUNT(*) as cnt 
               FROM patients 
               GROUP BY gender""",
        )
        agg_elapsed = time.time() - start
        assert len(agg_result.results) == 2  # male, female
        print(f"  Aggregation query: {agg_elapsed:.4f}s")


# ============================================================================
# Edge Case Tests
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_merge_single_scenario_error(self, service):
        """Test that merging a single scenario raises error."""
        patients = generate_patients(10)
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='single-scenario',
        )
        
        # Match the actual error message (case-sensitive)
        with pytest.raises(ValueError, match="At least 2 source scenarios"):
            service.merge_scenarios(
                source_scenario_ids=[result.scenario_id],
                target_name='should-fail',
            )
    
    def test_export_nonexistent_scenario(self, service, export_dir):
        """Test exporting a scenario that doesn't exist."""
        fake_id = str(uuid4())
        json_path = export_dir / "fake.json"
        
        with pytest.raises(ValueError, match="not found"):
            service.export_to_json(fake_id, str(json_path))
    
    def test_clone_nonexistent_scenario(self, service):
        """Test cloning a scenario that doesn't exist."""
        fake_id = str(uuid4())
        
        with pytest.raises(ValueError, match="not found"):
            service.clone_scenario(fake_id)
    
    def test_tag_case_insensitivity(self, service):
        """Test that tags are case-insensitive."""
        patients = generate_patients(5)
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='case-test',
            tags=['TestTag'],
        )
        
        # Add mixed case tags
        service.add_tag(result.scenario_id, 'UPPERCASE')
        service.add_tag(result.scenario_id, 'lowercase')
        service.add_tag(result.scenario_id, 'MixedCase')
        
        tags = service.get_tags(result.scenario_id)
        # All should be lowercase
        assert all(t == t.lower() for t in tags)
        assert 'testtag' in tags
        assert 'uppercase' in tags
        assert 'mixedcase' in tags
    
    def test_duplicate_tag_ignored(self, service):
        """Test that adding the same tag twice is idempotent."""
        patients = generate_patients(5)
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name='dup-tag-test',
        )
        
        service.add_tag(result.scenario_id, 'duplicate')
        service.add_tag(result.scenario_id, 'duplicate')
        service.add_tag(result.scenario_id, 'DUPLICATE')  # Case variation
        
        tags = service.get_tags(result.scenario_id)
        assert tags.count('duplicate') == 1
    
    def test_special_characters_in_scenario_name(self, service):
        """Test scenario names with special characters."""
        patients = generate_patients(5)
        
        # Names with various special characters
        # Note: sanitize_name has specific character handling rules
        special_names = [
            ('test-with-dashes', 'test-with-dashes'),
            ('test_with_underscores', 'test-with-underscores'),  # Underscores → dashes
            ('test.with.dots', 'testwithdots'),  # Dots removed
            ('test with spaces', 'test-with-spaces'),  # Spaces → dashes
        ]
        
        for input_name, expected_name in special_names:
            result = service.persist_entities(
                entities=patients.copy(),
                entity_type='patient',
                scenario_name=input_name,
            )
            assert result.scenario_name == expected_name
            
            # Should be able to find by filter_pattern
            scenarios = service.list_scenarios(filter_pattern=expected_name[:10])
            assert len(scenarios) >= 1
    
    def test_very_long_scenario_name(self, service):
        """Test handling of very long scenario names."""
        patients = generate_patients(5)
        long_name = 'a' * 500  # Very long name
        
        result = service.persist_entities(
            entities=patients,
            entity_type='patient',
            scenario_name=long_name,
        )
        
        # Should truncate or handle gracefully
        assert result.scenario_id is not None


# ============================================================================
# Cross-Product Tests
# ============================================================================

class TestCrossProduct:
    """Test scenarios with multiple product domains."""
    
    def test_multi_scenario_tagging_and_filtering(self, service):
        """Test tagging and filtering across multiple scenarios."""
        # Create scenarios from different products
        patients_1 = generate_patients(20)
        patients_2 = generate_patients(15)
        
        # PatientSim scenario
        result1 = service.persist_entities(
            entities=patients_1,
            entity_type='patient',
            scenario_name='patientsim-cohort',
            tags=['patientsim', 'training'],
        )
        
        # Another PatientSim scenario
        result2 = service.persist_entities(
            entities=patients_2,
            entity_type='patient',
            scenario_name='patientsim-test',
            tags=['patientsim', 'testing'],
        )
        
        # Query by product tag
        patientsim_scenarios = service.scenarios_by_tag('patientsim')
        assert len(patientsim_scenarios) == 2
        
        # Query by purpose tag
        training_scenarios = service.scenarios_by_tag('training')
        assert len(training_scenarios) == 1
        assert training_scenarios[0].name == 'patientsim-cohort'
        
        # Merge both into combined dataset
        merged = service.merge_scenarios(
            source_scenario_ids=[result1.scenario_id, result2.scenario_id],
            target_name='combined-patientsim',
            tags=['patientsim', 'merged'],
        )
        assert merged.entities_merged.get('patients', 0) == 35
    
    def test_all_canonical_tables_defined(self, service):
        """Verify CANONICAL_TABLES constant is defined with expected tables."""
        # CANONICAL_TABLES is a list of (table_name, id_column) tuples
        table_names = [t[0] for t in CANONICAL_TABLES]
        
        assert len(CANONICAL_TABLES) >= 17  # At least the original 17
        
        # Check key tables from each product
        assert 'patients' in table_names
        assert 'encounters' in table_names
        assert 'members' in table_names
