"""
HealthSim State Manager - DuckDB Backend.

Provides save/load/list/delete operations for scenarios using DuckDB
as the storage backend instead of JSON files.
"""

from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime
from pathlib import Path
import json

import duckdb

from ..db import get_connection
from .serializers import (
    get_serializer,
    get_table_info,
    ENTITY_TABLE_MAP,
)


class StateManager:
    """
    Manages scenario persistence in DuckDB.
    
    Scenarios are collections of entities (patients, encounters, claims, etc.)
    that can be saved, loaded, listed, and deleted. Entity data is stored both:
    1. In typed canonical tables (patients, encounters, etc.) for SQL queries
    2. In scenario_entities.entity_data as JSON for round-trip compatibility
    
    Usage:
        manager = StateManager()
        
        # Save a scenario
        scenario_id = manager.save_scenario(
            name='diabetes-cohort',
            entities={'patients': [...], 'encounters': [...]},
            description='Type 2 diabetes patient cohort',
            tags=['diabetes', 'chronic']
        )
        
        # Load a scenario
        scenario = manager.load_scenario('diabetes-cohort')
        
        # List scenarios
        scenarios = manager.list_scenarios(tag='diabetes')
        
        # Delete a scenario
        manager.delete_scenario('diabetes-cohort')
    """
    
    def __init__(self, connection: Optional[duckdb.DuckDBPyConnection] = None):
        """
        Initialize state manager.
        
        Args:
            connection: Optional database connection (uses default if not provided)
        """
        self._conn = connection
    
    @property
    def conn(self) -> duckdb.DuckDBPyConnection:
        """Get database connection (lazy initialization)."""
        if self._conn is None:
            self._conn = get_connection()
        return self._conn
    
    def save_scenario(
        self,
        name: str,
        entities: Dict[str, List[Dict]],
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        overwrite: bool = False,
        product: str = 'healthsim',
    ) -> str:
        """
        Save a scenario to the database.
        
        Args:
            name: Unique scenario name
            entities: Dict mapping entity type to list of entities
            description: Optional description
            tags: Optional list of tags for filtering
            overwrite: If True, replace existing scenario with same name
            product: Product identifier (patientsim, membersim, etc.)
            
        Returns:
            Scenario ID (UUID string)
            
        Raises:
            ValueError: If scenario exists and overwrite=False
        """
        # Check for existing scenario
        existing = self._get_scenario_by_name(name)
        if existing and not overwrite:
            raise ValueError(f"Scenario '{name}' already exists. Use overwrite=True to replace.")
        
        scenario_id = existing['scenario_id'] if existing else str(uuid4())
        now = datetime.utcnow()
        
        # If overwriting, clear existing entity links
        if existing and overwrite:
            self._delete_scenario_entities(scenario_id)
            self.conn.execute("DELETE FROM scenario_tags WHERE scenario_id = ?", [scenario_id])
        
        # Build metadata JSON
        metadata = {
            'product': product,
            'entity_types': list(entities.keys()),
            'entity_counts': {k: len(v) for k, v in entities.items()},
        }
        
        # Create or update scenario record
        if existing:
            self.conn.execute("""
                UPDATE scenarios SET
                    description = ?,
                    updated_at = ?,
                    metadata = ?
                WHERE scenario_id = ?
            """, [description, now, json.dumps(metadata), scenario_id])
        else:
            self.conn.execute("""
                INSERT INTO scenarios (scenario_id, name, description, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [scenario_id, name, description, now, now, json.dumps(metadata)])
        
        # Insert entities
        entity_count = 0
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                self._save_entity(scenario_id, entity_type, entity)
                entity_count += 1
        
        # Save tags
        if tags:
            for tag in tags:
                # Check if tag already exists
                existing = self.conn.execute("""
                    SELECT id FROM scenario_tags WHERE scenario_id = ? AND tag = ?
                """, [scenario_id, tag]).fetchone()
                
                if not existing:
                    self.conn.execute("""
                        INSERT INTO scenario_tags (id, scenario_id, tag)
                        VALUES (nextval('scenario_tags_seq'), ?, ?)
                    """, [scenario_id, tag])
        
        return scenario_id
    
    def load_scenario(self, name_or_id: str) -> Dict[str, Any]:
        """
        Load a scenario from the database.
        
        Args:
            name_or_id: Scenario name or UUID
            
        Returns:
            Dict with scenario metadata and entities
            
        Raises:
            ValueError: If scenario not found
        """
        # Try as name first, then as UUID
        scenario = self._get_scenario_by_name(name_or_id)
        if not scenario:
            scenario = self._get_scenario_by_id(name_or_id)
        if not scenario:
            raise ValueError(f"Scenario '{name_or_id}' not found")
        
        scenario_id = scenario['scenario_id']
        
        # Load all entities for this scenario from scenario_entities
        entities = self._load_scenario_entities(scenario_id)
        
        # Load tags
        tags_result = self.conn.execute("""
            SELECT tag FROM scenario_tags WHERE scenario_id = ?
        """, [scenario_id]).fetchall()
        tags = [t[0] for t in tags_result]
        
        # Parse metadata
        metadata = {}
        if scenario.get('metadata'):
            try:
                metadata = json.loads(scenario['metadata']) if isinstance(scenario['metadata'], str) else scenario['metadata']
            except (json.JSONDecodeError, TypeError):
                pass
        
        return {
            'scenario_id': scenario_id,
            'name': scenario['name'],
            'description': scenario['description'],
            'created_at': scenario['created_at'],
            'updated_at': scenario['updated_at'],
            'tags': tags,
            'metadata': metadata,
            'entities': entities,
            'entity_count': sum(len(v) for v in entities.values()),
        }
    
    def list_scenarios(
        self,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        product: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List available scenarios.
        
        Args:
            tag: Filter by tag
            search: Search in name/description
            product: Filter by product (from metadata)
            limit: Max results (default 100)
            
        Returns:
            List of scenario summaries (without full entity data)
        """
        query = """
            SELECT DISTINCT s.scenario_id, s.name, s.description, 
                   s.created_at, s.updated_at, s.metadata
            FROM scenarios s
        """
        params = []
        conditions = []
        
        if tag:
            query += " JOIN scenario_tags t ON s.scenario_id = t.scenario_id"
            conditions.append("t.tag = ?")
            params.append(tag)
        
        if search:
            conditions.append("(s.name LIKE ? OR s.description LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY s.updated_at DESC LIMIT ?"
        params.append(limit)
        
        results = self.conn.execute(query, params).fetchall()
        
        scenarios = []
        for row in results:
            metadata = {}
            if row[5]:
                try:
                    metadata = json.loads(row[5]) if isinstance(row[5], str) else row[5]
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # Filter by product if specified
            if product and metadata.get('product') != product:
                continue
            
            # Get entity count
            count_result = self.conn.execute("""
                SELECT COUNT(*) FROM scenario_entities WHERE scenario_id = ?
            """, [row[0]]).fetchone()
            
            # Get tags
            tags_result = self.conn.execute("""
                SELECT tag FROM scenario_tags WHERE scenario_id = ?
            """, [row[0]]).fetchall()
            
            scenarios.append({
                'scenario_id': row[0],
                'name': row[1],
                'description': row[2],
                'created_at': row[3],
                'updated_at': row[4],
                'entity_count': count_result[0] if count_result else 0,
                'tags': [t[0] for t in tags_result],
                'metadata': metadata,
            })
        
        return scenarios
    
    def delete_scenario(self, name_or_id: str) -> bool:
        """
        Delete a scenario.
        
        Note: This removes the scenario metadata, entity links, and tags.
        Entity data in canonical tables is NOT deleted (for cross-scenario sharing).
        
        Args:
            name_or_id: Scenario name or UUID
            
        Returns:
            True if deleted, False if not found
        """
        scenario = self._get_scenario_by_name(name_or_id) or self._get_scenario_by_id(name_or_id)
        if not scenario:
            return False
        
        scenario_id = scenario['scenario_id']
        
        # Delete in order: tags, entity links, scenario
        self.conn.execute("DELETE FROM scenario_tags WHERE scenario_id = ?", [scenario_id])
        self.conn.execute("DELETE FROM scenario_entities WHERE scenario_id = ?", [scenario_id])
        self.conn.execute("DELETE FROM scenarios WHERE scenario_id = ?", [scenario_id])
        
        return True
    
    def scenario_exists(self, name_or_id: str) -> bool:
        """Check if a scenario exists."""
        return (
            self._get_scenario_by_name(name_or_id) is not None or
            self._get_scenario_by_id(name_or_id) is not None
        )
    
    def get_scenario_tags(self, name_or_id: str) -> List[str]:
        """Get tags for a scenario."""
        scenario = self._get_scenario_by_name(name_or_id) or self._get_scenario_by_id(name_or_id)
        if not scenario:
            return []
        
        result = self.conn.execute("""
            SELECT tag FROM scenario_tags WHERE scenario_id = ?
        """, [scenario['scenario_id']]).fetchall()
        return [t[0] for t in result]
    
    def add_scenario_tags(self, name_or_id: str, tags: List[str]) -> bool:
        """Add tags to a scenario."""
        scenario = self._get_scenario_by_name(name_or_id) or self._get_scenario_by_id(name_or_id)
        if not scenario:
            return False
        
        for tag in tags:
            # Check if tag already exists
            existing = self.conn.execute("""
                SELECT id FROM scenario_tags WHERE scenario_id = ? AND tag = ?
            """, [scenario['scenario_id'], tag]).fetchone()
            
            if not existing:
                self.conn.execute("""
                    INSERT INTO scenario_tags (id, scenario_id, tag)
                    VALUES (nextval('scenario_tags_seq'), ?, ?)
                """, [scenario['scenario_id'], tag])
        return True
    
    # =========================================================================
    # Private helper methods
    # =========================================================================
    
    def _get_scenario_by_name(self, name: str) -> Optional[Dict]:
        """Get scenario by name."""
        result = self.conn.execute(
            "SELECT scenario_id, name, description, created_at, updated_at, metadata FROM scenarios WHERE name = ?",
            [name]
        ).fetchone()
        if result:
            return {
                'scenario_id': result[0],
                'name': result[1],
                'description': result[2],
                'created_at': result[3],
                'updated_at': result[4],
                'metadata': result[5],
            }
        return None
    
    def _get_scenario_by_id(self, scenario_id: str) -> Optional[Dict]:
        """Get scenario by ID."""
        try:
            result = self.conn.execute(
                "SELECT scenario_id, name, description, created_at, updated_at, metadata FROM scenarios WHERE scenario_id = ?",
                [scenario_id]
            ).fetchone()
            if result:
                return {
                    'scenario_id': result[0],
                    'name': result[1],
                    'description': result[2],
                    'created_at': result[3],
                    'updated_at': result[4],
                    'metadata': result[5],
                }
        except Exception:
            pass
        return None
    
    def _save_entity(self, scenario_id: str, entity_type: str, entity: Dict) -> str:
        """
        Save entity to scenario_entities table (and optionally to canonical table).
        
        Returns entity_id.
        """
        # Determine entity ID
        table_name, id_column = get_table_info(entity_type)
        entity_id = entity.get(id_column) or entity.get('id') or entity.get(f'{entity_type}_id') or str(uuid4())
        
        # Store full entity as JSON in scenario_entities
        entity_json = json.dumps(entity, default=str)
        
        # Check if entity already exists for this scenario
        existing = self.conn.execute("""
            SELECT id FROM scenario_entities 
            WHERE scenario_id = ? AND entity_type = ? AND entity_id = ?
        """, [scenario_id, entity_type, entity_id]).fetchone()
        
        if existing:
            # Update existing
            self.conn.execute("""
                UPDATE scenario_entities 
                SET entity_data = ?
                WHERE scenario_id = ? AND entity_type = ? AND entity_id = ?
            """, [entity_json, scenario_id, entity_type, entity_id])
        else:
            # Insert new (explicitly use sequence for id)
            self.conn.execute("""
                INSERT INTO scenario_entities (id, scenario_id, entity_type, entity_id, entity_data, created_at)
                VALUES (nextval('scenario_entities_seq'), ?, ?, ?, ?, ?)
            """, [scenario_id, entity_type, entity_id, entity_json, datetime.utcnow()])
        
        # Also try to insert into canonical table if serializer exists
        serializer = get_serializer(entity_type)
        if serializer:
            try:
                self._insert_canonical_entity(entity_type, entity, serializer)
            except Exception:
                # Canonical insert is optional - JSON storage is the primary
                pass
        
        return entity_id
    
    def _insert_canonical_entity(self, entity_type: str, entity: Dict, serializer) -> None:
        """Insert entity into canonical table using serializer."""
        table_name, id_column = get_table_info(entity_type)
        
        # Get provenance from entity
        provenance = entity.get('_provenance', {})
        if 'provenance' in entity:
            prov_data = entity['provenance']
            if isinstance(prov_data, dict):
                provenance = prov_data
        
        # Serialize entity
        data = serializer(entity, provenance)
        
        # Build INSERT statement
        columns = list(data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        
        # For conflict handling, update all columns except the primary key
        non_pk_columns = [c for c in columns if c != id_column]
        updates = ', '.join([f"{col} = excluded.{col}" for col in non_pk_columns])
        
        try:
            self.conn.execute(f"""
                INSERT INTO {table_name} ({', '.join(columns)})
                VALUES ({placeholders})
                ON CONFLICT ({id_column}) DO UPDATE SET {updates}
            """, list(data.values()))
        except Exception:
            # Table might not exist or columns might not match - this is OK
            pass
    
    def _load_scenario_entities(self, scenario_id: str) -> Dict[str, List[Dict]]:
        """Load all entities for a scenario from scenario_entities table."""
        results = self.conn.execute("""
            SELECT entity_type, entity_id, entity_data
            FROM scenario_entities
            WHERE scenario_id = ?
            ORDER BY entity_type, created_at
        """, [scenario_id]).fetchall()
        
        entities: Dict[str, List[Dict]] = {}
        for row in results:
            entity_type = row[0]
            entity_data = row[2]
            
            # Parse JSON
            if isinstance(entity_data, str):
                try:
                    entity = json.loads(entity_data)
                except json.JSONDecodeError:
                    entity = {'id': row[1], '_raw': entity_data}
            else:
                entity = entity_data if entity_data else {'id': row[1]}
            
            if entity_type not in entities:
                entities[entity_type] = []
            entities[entity_type].append(entity)
        
        return entities
    
    def _delete_scenario_entities(self, scenario_id: str) -> None:
        """Remove all entity links for a scenario."""
        self.conn.execute(
            "DELETE FROM scenario_entities WHERE scenario_id = ?",
            [scenario_id]
        )
    
    # =========================================================================
    # JSON Export/Import Methods
    # =========================================================================
    
    def export_to_json(
        self,
        name_or_id: str,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        Export a scenario to JSON file for sharing.
        
        Args:
            name_or_id: Scenario name or UUID
            output_path: Where to save (default: ~/Downloads/{name}.json)
            
        Returns:
            Path to exported file
        """
        from .legacy import export_to_json as _export, export_scenario_for_sharing
        
        scenario = self.load_scenario(name_or_id)
        
        # Use default path if not specified
        if output_path is None:
            downloads = Path.home() / "Downloads"
            downloads.mkdir(exist_ok=True)
            # Clean name for filename
            safe_name = scenario['name'].replace(' ', '_').replace('/', '-')
            output_path = downloads / f"{safe_name}.json"
        
        # Prepare for export (remove internal fields)
        export_data = export_scenario_for_sharing(scenario)
        
        return _export(export_data, Path(output_path))
    
    def import_from_json(
        self,
        json_path: Path,
        name: Optional[str] = None,
        overwrite: bool = False,
    ) -> str:
        """
        Import a scenario from JSON file.
        
        Args:
            json_path: Path to JSON file
            name: Override scenario name (default: use filename or embedded name)
            overwrite: Replace existing scenario with same name
            
        Returns:
            Scenario ID
        """
        from .legacy import import_from_json as _import
        
        data = _import(Path(json_path))
        
        # Determine name (priority: argument > embedded > filename)
        scenario_name = name or data.get('name') or Path(json_path).stem
        
        # Get description and tags
        description = data.get('description')
        tags = data.get('tags', [])
        
        # Extract entities
        entities = data.get('entities', {})
        
        # Handle legacy format where entities are at top level
        if not entities:
            legacy_types = [
                'patients', 'patient',
                'encounters', 'encounter', 
                'diagnoses', 'diagnosis',
                'medications', 'medication',
                'members', 'member',
                'claims', 'claim',
                'prescriptions', 'prescription',
                'subjects', 'subject',
            ]
            for key in legacy_types:
                if key in data and isinstance(data[key], list):
                    # Normalize to plural form
                    normalized_key = key if key.endswith('s') else key + 's'
                    entities[normalized_key] = data[key]
        
        # Handle EntityWithProvenance wrapper format
        for entity_type in list(entities.keys()):
            entity_list = entities[entity_type]
            if entity_list and isinstance(entity_list[0], dict):
                if 'data' in entity_list[0] and 'provenance' in entity_list[0]:
                    # Unwrap EntityWithProvenance
                    entities[entity_type] = [
                        {**e['data'], '_provenance': e.get('provenance', {})}
                        for e in entity_list
                    ]
        
        return self.save_scenario(
            name=scenario_name,
            entities=entities,
            description=description,
            tags=tags,
            overwrite=overwrite,
        )


# =============================================================================
# Module-level convenience functions (for backward compatibility)
# =============================================================================

_manager: Optional[StateManager] = None


def get_manager() -> StateManager:
    """Get singleton state manager instance."""
    global _manager
    if _manager is None:
        _manager = StateManager()
    return _manager


def reset_manager() -> None:
    """Reset the singleton manager (for testing)."""
    global _manager
    _manager = None


def save_scenario(name: str, entities: Dict, **kwargs) -> str:
    """Convenience function for save_scenario."""
    return get_manager().save_scenario(name, entities, **kwargs)


def load_scenario(name_or_id: str) -> Dict:
    """Convenience function for load_scenario."""
    return get_manager().load_scenario(name_or_id)


def list_scenarios(**kwargs) -> List[Dict]:
    """Convenience function for list_scenarios."""
    return get_manager().list_scenarios(**kwargs)


def delete_scenario(name_or_id: str) -> bool:
    """Convenience function for delete_scenario."""
    return get_manager().delete_scenario(name_or_id)


def scenario_exists(name_or_id: str) -> bool:
    """Convenience function for scenario_exists."""
    return get_manager().scenario_exists(name_or_id)


def export_scenario_to_json(name_or_id: str, output_path: Optional[Path] = None) -> Path:
    """Convenience function for export_to_json."""
    return get_manager().export_to_json(name_or_id, output_path)


def import_scenario_from_json(json_path: Path, name: Optional[str] = None, overwrite: bool = False) -> str:
    """Convenience function for import_from_json."""
    return get_manager().import_from_json(json_path, name, overwrite)
