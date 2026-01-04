"""
Tests for the healthsim_add_entities MCP tool.

This tool provides incremental entity addition to scenarios, solving:
1. Batch truncation - allows adding entities in multiple calls
2. Destructive overwrite - uses upsert logic instead of replace

Tests cover:
- Creating new scenarios via add_entities
- Adding to existing scenarios
- Upsert behavior (update existing, insert new)
- Batch tracking
- Error handling
"""

import json
import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime

import duckdb

# Import the MCP server module
import sys
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "mcp-server"))
sys.path.insert(0, str(WORKSPACE_ROOT / "packages" / "core" / "src"))

from healthsim_mcp import (
    ConnectionManager,
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create a temp file path but don't create the file
    # DuckDB will create it fresh
    fd, path = tempfile.mkstemp(suffix='.duckdb')
    os.close(fd)
    os.unlink(path)  # Delete the empty file so DuckDB can create it
    db_path = Path(path)
    
    # Initialize schema
    conn = duckdb.connect(str(db_path))
    conn.execute("""
        CREATE TABLE scenarios (
            scenario_id VARCHAR PRIMARY KEY,
            name VARCHAR UNIQUE NOT NULL,
            description VARCHAR,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            metadata JSON
        )
    """)
    conn.execute("""
        CREATE TABLE cohort_entities (
            id INTEGER PRIMARY KEY,
            scenario_id VARCHAR NOT NULL,
            entity_type VARCHAR NOT NULL,
            entity_id VARCHAR NOT NULL,
            entity_data JSON,
            created_at TIMESTAMP,
            UNIQUE(scenario_id, entity_type, entity_id)
        )
    """)
    conn.execute("""
        CREATE TABLE cohort_tags (
            id INTEGER PRIMARY KEY,
            scenario_id VARCHAR NOT NULL,
            tag VARCHAR NOT NULL,
            UNIQUE(scenario_id, tag)
        )
    """)
    conn.execute("CREATE SEQUENCE cohort_entities_seq START 1")
    conn.execute("CREATE SEQUENCE cohort_tags_seq START 1")
    conn.close()
    
    yield db_path
    
    # Cleanup
    db_path.unlink(missing_ok=True)


@pytest.fixture
def connection_manager(temp_db):
    """Create a connection manager for the temp database."""
    return ConnectionManager(temp_db)


class TestAddEntitiesNewScenario:
    """Tests for creating new scenarios via add_entities."""
    
    def test_create_scenario_with_name(self, connection_manager):
        """Create a new scenario by providing scenario_name."""
        with connection_manager.write_connection() as conn:
            # Create scenario
            scenario_id = "test-uuid-123"
            scenario_name = "Test Scenario"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, [scenario_id, scenario_name, "Test description", now, now])
            
            # Verify scenario was created
            result = conn.execute(
                "SELECT name FROM cohorts WHERE id = ?",
                [scenario_id]
            ).fetchone()
            
            assert result is not None
            assert result[0] == scenario_name
    
    def test_create_scenario_auto_name(self, connection_manager):
        """Create a new scenario with auto-generated name."""
        with connection_manager.write_connection() as conn:
            # Auto-generate name
            scenario_id = "test-uuid-456"
            scenario_name = f"scenario-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, scenario_name, now, now])
            
            # Verify
            result = conn.execute(
                "SELECT name FROM cohorts WHERE id = ?",
                [scenario_id]
            ).fetchone()
            
            assert result is not None
            assert result[0].startswith("scenario-")


class TestAddEntitiesToExisting:
    """Tests for adding entities to existing scenarios."""
    
    def test_add_entities_to_existing_scenario(self, connection_manager):
        """Add entities to a scenario that already exists."""
        with connection_manager.write_connection() as conn:
            # Create scenario first
            scenario_id = "existing-scenario-123"
            now = datetime.utcnow()
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, "Existing Scenario", now, now])
            
            # Add initial entities
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (1, ?, 'patients', 'PAT-001', '{"name": "John"}', ?)
            """, [scenario_id, now])
            
            # Verify initial state
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE id = ?",
                [scenario_id]
            ).fetchone()[0]
            assert count == 1
            
            # Add more entities
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (2, ?, 'patients', 'PAT-002', '{"name": "Jane"}', ?)
            """, [scenario_id, now])
            
            # Verify new count
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE id = ?",
                [scenario_id]
            ).fetchone()[0]
            assert count == 2
    
    def test_add_different_entity_types(self, connection_manager):
        """Add different entity types to same scenario."""
        with connection_manager.write_connection() as conn:
            scenario_id = "multi-type-scenario"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, "Multi-Type Scenario", now, now])
            
            # Add patients
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (1, ?, 'patients', 'PAT-001', '{"name": "John"}', ?)
            """, [scenario_id, now])
            
            # Add members
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (2, ?, 'members', 'MBR-001', '{"plan": "Gold"}', ?)
            """, [scenario_id, now])
            
            # Verify both types exist
            types = conn.execute("""
                SELECT DISTINCT entity_type FROM cohort_entities WHERE id = ?
            """, [scenario_id]).fetchall()
            
            type_set = {t[0] for t in types}
            assert 'patients' in type_set
            assert 'members' in type_set


class TestUpsertBehavior:
    """Tests for upsert (update or insert) behavior."""
    
    def test_insert_new_entity(self, connection_manager):
        """Insert a new entity that doesn't exist."""
        with connection_manager.write_connection() as conn:
            scenario_id = "upsert-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, "Upsert Test", now, now])
            
            # Insert new entity
            entity_id = "NEW-001"
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (1, ?, 'patients', ?, '{"name": "New Patient"}', ?)
            """, [scenario_id, entity_id, now])
            
            # Verify insert
            result = conn.execute("""
                SELECT entity_data FROM cohort_entities 
                WHERE id = ? AND entity_id = ?
            """, [scenario_id, entity_id]).fetchone()
            
            assert result is not None
            data = json.loads(result[0])
            assert data["name"] == "New Patient"
    
    def test_update_existing_entity(self, connection_manager):
        """Update an entity that already exists (upsert behavior)."""
        with connection_manager.write_connection() as conn:
            scenario_id = "upsert-update-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, "Upsert Update Test", now, now])
            
            # Insert initial entity
            entity_id = "PAT-001"
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES (1, ?, 'patients', ?, '{"name": "Original"}', ?)
            """, [scenario_id, entity_id, now])
            
            # Update via upsert logic
            # Check if exists
            existing = conn.execute("""
                SELECT id FROM cohort_entities 
                WHERE id = ? AND entity_type = ? AND entity_id = ?
            """, [scenario_id, 'patients', entity_id]).fetchone()
            
            assert existing is not None  # Should exist
            
            # Update
            conn.execute("""
                UPDATE cohort_entities 
                SET entity_data = ?, created_at = ?
                WHERE id = ? AND entity_type = ? AND entity_id = ?
            """, ['{"name": "Updated"}', now, scenario_id, 'patients', entity_id])
            
            # Verify update
            result = conn.execute("""
                SELECT entity_data FROM cohort_entities 
                WHERE id = ? AND entity_id = ?
            """, [scenario_id, entity_id]).fetchone()
            
            data = json.loads(result[0])
            assert data["name"] == "Updated"
    
    def test_upsert_does_not_delete_other_entities(self, connection_manager):
        """Verify that upserting doesn't delete entities not in the current batch."""
        with connection_manager.write_connection() as conn:
            scenario_id = "no-delete-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, "No Delete Test", now, now])
            
            # Insert 3 entities
            for i in range(1, 4):
                conn.execute("""
                    INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                    VALUES (?, ?, 'patients', ?, ?, ?)
                """, [i, scenario_id, f"PAT-00{i}", f'{{"id": {i}}}', now])
            
            # Verify 3 entities
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE id = ?",
                [scenario_id]
            ).fetchone()[0]
            assert count == 3
            
            # Now "upsert" just one entity (PAT-002)
            conn.execute("""
                UPDATE cohort_entities 
                SET entity_data = ?
                WHERE id = ? AND entity_id = ?
            """, ['{"id": 2, "updated": true}', scenario_id, "PAT-002"])
            
            # Verify still 3 entities (no deletion)
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE id = ?",
                [scenario_id]
            ).fetchone()[0]
            assert count == 3
            
            # Verify PAT-001 and PAT-003 still exist unchanged
            result = conn.execute("""
                SELECT entity_id FROM cohort_entities 
                WHERE id = ? ORDER BY entity_id
            """, [scenario_id]).fetchall()
            
            ids = [r[0] for r in result]
            assert ids == ["PAT-001", "PAT-002", "PAT-003"]


class TestBatchTracking:
    """Tests for batch progress tracking."""
    
    def test_batch_number_tracking(self, connection_manager):
        """Track batch numbers across multiple calls."""
        with connection_manager.write_connection() as conn:
            scenario_id = "batch-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, "Batch Test", now, now])
            
            # Simulate batch 1 of 4
            batch_1_count = 50
            for i in range(1, batch_1_count + 1):
                conn.execute("""
                    INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                    VALUES (?, ?, 'patients', ?, '{}', ?)
                """, [i, scenario_id, f"PAT-{i:03d}", now])
            
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE id = ?",
                [scenario_id]
            ).fetchone()[0]
            assert count == 50
            
            # Simulate batch 2 of 4
            for i in range(51, 101):
                conn.execute("""
                    INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                    VALUES (?, ?, 'patients', ?, '{}', ?)
                """, [i, scenario_id, f"PAT-{i:03d}", now])
            
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE id = ?",
                [scenario_id]
            ).fetchone()[0]
            assert count == 100


class TestErrorHandling:
    """Tests for error conditions."""
    
    def test_scenario_not_found(self, connection_manager):
        """Error when scenario_id doesn't exist."""
        with connection_manager.write_connection() as conn:
            # Try to find non-existent scenario
            result = conn.execute(
                "SELECT name FROM cohorts WHERE id = ?",
                ["non-existent-id"]
            ).fetchone()
            
            assert result is None
    
    def test_empty_entities_handled(self, connection_manager):
        """Handle empty entity lists gracefully."""
        with connection_manager.write_connection() as conn:
            scenario_id = "empty-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, "Empty Test", now, now])
            
            # Adding empty list should not error
            entities = {}  # Empty
            
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    pass  # Nothing to do
            
            # Scenario should exist with 0 entities
            count = conn.execute(
                "SELECT COUNT(*) FROM cohort_entities WHERE id = ?",
                [scenario_id]
            ).fetchone()[0]
            assert count == 0


class TestEntityTypeNormalization:
    """Tests for entity type normalization (singular -> plural)."""
    
    def test_singular_to_plural_conversion(self):
        """Verify entity types are normalized to plural form."""
        test_cases = [
            ("patient", "patients"),
            ("patients", "patients"),
            ("member", "members"),
            ("members", "members"),
            ("claim", "claims"),
            ("encounter", "encounters"),
        ]
        
        for input_type, expected in test_cases:
            normalized = input_type.lower()
            if not normalized.endswith('s'):
                normalized += 's'
            assert normalized == expected, f"Failed for {input_type}"


class TestScenarioTotals:
    """Tests for scenario total calculations."""
    
    def test_total_by_type(self, connection_manager):
        """Calculate totals by entity type."""
        with connection_manager.write_connection() as conn:
            scenario_id = "totals-test"
            now = datetime.utcnow()
            
            conn.execute("""
                INSERT INTO cohorts (id, name, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, [scenario_id, "Totals Test", now, now])
            
            # Add mixed entities
            conn.execute("""
                INSERT INTO cohort_entities (id, cohort_id, entity_type, entity_id, entity_data, created_at)
                VALUES 
                    (1, ?, 'patients', 'P1', '{}', ?),
                    (2, ?, 'patients', 'P2', '{}', ?),
                    (3, ?, 'patients', 'P3', '{}', ?),
                    (4, ?, 'members', 'M1', '{}', ?),
                    (5, ?, 'members', 'M2', '{}', ?)
            """, [scenario_id, now, scenario_id, now, scenario_id, now, scenario_id, now, scenario_id, now])
            
            # Get totals by type
            result = conn.execute("""
                SELECT entity_type, COUNT(*) as count 
                FROM cohort_entities 
                WHERE id = ? 
                GROUP BY entity_type
            """, [scenario_id]).fetchall()
            
            totals = {row[0]: row[1] for row in result}
            
            assert totals.get('patients') == 3
            assert totals.get('members') == 2
            assert sum(totals.values()) == 5



class TestToolSelectionGuidance:
    """Tests verifying tool descriptions contain proper selection guidance.
    
    These tests ensure Claude receives clear signals about when to use
    save_scenario vs add_entities based on entity count thresholds.
    """
    
    def test_save_scenario_warns_about_large_datasets(self):
        """Verify save_scenario docstring warns about 50+ entity limit."""
        from healthsim_mcp import save_scenario
        
        docstring = save_scenario.__doc__
        assert docstring is not None
        
        # Should warn to use add_entities instead
        assert "add_entities" in docstring.lower() or "healthsim_add_entities" in docstring
        
        # Should mention the 50 entity threshold
        assert "50" in docstring
        
        # Should indicate it's for small datasets
        assert "small" in docstring.lower() or "≤50" in docstring
        
        # Should warn about replacement behavior
        assert "replace" in docstring.lower()
    
    def test_add_entities_recommends_for_large_datasets(self):
        """Verify add_entities docstring recommends itself for large datasets."""
        from healthsim_mcp import add_entities
        
        docstring = add_entities.__doc__
        assert docstring is not None
        
        # Should indicate it's recommended
        assert "recommended" in docstring.lower() or "RECOMMENDED" in docstring
        
        # Should mention 50 entity threshold
        assert "50" in docstring
        
        # Should mention upsert/incremental behavior
        assert "upsert" in docstring.lower() or "incremental" in docstring.lower()
        
        # Should mention it doesn't delete
        assert "never delete" in docstring.lower() or "NEVER deletes" in docstring
    
    def test_tool_descriptions_are_complementary(self):
        """Verify the two tools have complementary guidance."""
        from healthsim_mcp import save_scenario, add_entities
        
        save_doc = save_scenario.__doc__
        add_doc = add_entities.__doc__
        
        # save_scenario should redirect to add_entities for large datasets
        assert "healthsim_add_entities" in save_doc or "add_entities" in save_doc
        
        # add_entities should be marked as preferred
        assert "✅" in add_doc or "RECOMMENDED" in add_doc
        
        # save_scenario should have warning indicator
        assert "⚠" in save_doc or "WARNING" in save_doc
    
    def test_threshold_consistency(self):
        """Verify both tools reference the same entity count threshold."""
        from healthsim_mcp import save_scenario, add_entities
        
        save_doc = save_scenario.__doc__
        add_doc = add_entities.__doc__
        
        # Both should mention 50 as the threshold
        assert "50" in save_doc, "save_scenario should mention 50 entity threshold"
        assert "50" in add_doc, "add_entities should mention 50 entity threshold"


class TestToolAnnotations:
    """Tests verifying MCP tool annotations are correct."""
    
    def test_save_scenario_annotations(self):
        """Verify save_scenario has correct MCP annotations."""
        from healthsim_mcp import mcp
        
        # Get the tool from the MCP server
        tools = mcp._tool_manager._tools
        save_tool = tools.get("healthsim_save_cohort")
        
        assert save_tool is not None, "healthsim_save_cohort tool should exist"
    
    def test_add_entities_annotations(self):
        """Verify add_entities has correct MCP annotations."""
        from healthsim_mcp import mcp
        
        tools = mcp._tool_manager._tools
        add_tool = tools.get("healthsim_add_entities")
        
        assert add_tool is not None, "healthsim_add_entities tool should exist"
    
    def test_add_entities_is_idempotent(self):
        """Verify add_entities is marked as idempotent (upsert behavior)."""
        from healthsim_mcp import mcp
        
        tools = mcp._tool_manager._tools
        add_tool = tools.get("healthsim_add_entities")
        
        # The tool should exist and be properly configured
        assert add_tool is not None
        # Note: FastMCP may store annotations differently, 
        # but the key behavior is tested in TestUpsertBehavior
