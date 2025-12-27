"""
Auto-persist service for HealthSim.

Implements the Structured RAG pattern:
- Summary in context (~500 tokens)
- Samples for consistency (~3000 tokens)
- Data stays in DuckDB
- Paginated queries for retrieval

This service is the primary interface for the auto-persist feature,
coordinating between auto-naming, summary generation, and database operations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4
import re

from ..db import get_connection
from .serializers import get_serializer, get_table_info, ENTITY_TABLE_MAP
from .auto_naming import generate_scenario_name, ensure_unique_name, sanitize_name
from .summary import ScenarioSummary, generate_summary, get_scenario_by_name


@dataclass
class PersistResult:
    """Result of a persist operation."""
    
    scenario_id: str
    scenario_name: str
    entity_type: str
    entities_persisted: int
    entity_ids: List[str]
    summary: ScenarioSummary
    is_new_scenario: bool
    batch_number: Optional[int] = None
    total_batches: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'scenario_id': self.scenario_id,
            'scenario_name': self.scenario_name,
            'entity_type': self.entity_type,
            'entities_persisted': self.entities_persisted,
            'entity_ids': self.entity_ids,
            'is_new_scenario': self.is_new_scenario,
            'batch_number': self.batch_number,
            'total_batches': self.total_batches,
            'summary': self.summary.to_dict(),
        }


@dataclass
class QueryResult:
    """Result of a paginated query."""
    
    results: List[Dict]
    total_count: int
    page: int
    page_size: int
    has_more: bool
    query_executed: str
    
    @property
    def offset(self) -> int:
        """Get current offset."""
        return self.page * self.page_size
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'results': self.results,
            'total_count': self.total_count,
            'page': self.page,
            'page_size': self.page_size,
            'has_more': self.has_more,
            'query_executed': self.query_executed,
        }


@dataclass
class ScenarioBrief:
    """Brief scenario info for listing."""
    
    scenario_id: str
    name: str
    description: Optional[str]
    entity_count: int
    created_at: datetime
    updated_at: datetime
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'scenario_id': self.scenario_id,
            'name': self.name,
            'description': self.description,
            'entity_count': self.entity_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tags': self.tags,
        }


# SQL patterns that are NOT allowed in queries
DISALLOWED_SQL_PATTERNS = [
    r'\bINSERT\b',
    r'\bUPDATE\b',
    r'\bDELETE\b',
    r'\bDROP\b',
    r'\bCREATE\b',
    r'\bALTER\b',
    r'\bTRUNCATE\b',
    r'\bGRANT\b',
    r'\bREVOKE\b',
    r'\bEXEC\b',
    r'\bEXECUTE\b',
    r'--',  # SQL comments
    r';.*\S',  # Multiple statements
]


def _validate_query(query: str) -> bool:
    """
    Validate that a query is SELECT-only.
    
    Args:
        query: SQL query string
        
    Returns:
        True if query is safe, False otherwise
        
    Raises:
        ValueError: If query contains disallowed patterns
    """
    query_upper = query.upper().strip()
    
    # Must start with SELECT or WITH (for CTEs)
    if not (query_upper.startswith('SELECT') or query_upper.startswith('WITH')):
        raise ValueError("Query must be a SELECT statement")
    
    # Check for disallowed patterns
    for pattern in DISALLOWED_SQL_PATTERNS:
        if re.search(pattern, query, re.IGNORECASE):
            raise ValueError(f"Query contains disallowed pattern: {pattern}")
    
    return True


class AutoPersistService:
    """
    Service for auto-persisting generated entities.
    
    Implements the core Structured RAG pattern:
    1. Persist entities to DuckDB immediately after generation
    2. Return summary (not full data) to context
    3. Provide paginated queries for data retrieval
    
    Usage:
        service = get_auto_persist_service()
        
        # Persist entities
        result = service.persist_entities(
            entities=[...],
            entity_type='patient',
            context_keywords=['diabetes', 'elderly']
        )
        
        # Query data
        query_result = service.query_scenario(
            scenario_id=result.scenario_id,
            query="SELECT * FROM patients WHERE gender = 'F'"
        )
    """
    
    def __init__(self, connection=None):
        """
        Initialize the service.
        
        Args:
            connection: Optional DuckDB connection (uses default if not provided)
        """
        self._conn = connection
    
    @property
    def conn(self):
        """Get database connection."""
        if self._conn is None:
            self._conn = get_connection()
        return self._conn
    
    def _create_scenario(
        self,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """
        Create a new scenario.
        
        Args:
            name: Scenario name
            description: Optional description
            tags: Optional list of tags
            
        Returns:
            New scenario ID
        """
        scenario_id = str(uuid4())
        now = datetime.utcnow()
        
        self.conn.execute("""
            INSERT INTO scenarios (scenario_id, name, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, [scenario_id, name, description, now, now])
        
        # Add tags
        if tags:
            for tag in tags:
                self.conn.execute("""
                    INSERT INTO scenario_tags (scenario_id, tag)
                    VALUES (?, ?)
                """, [scenario_id, tag.lower()])
        
        return scenario_id
    
    def _update_scenario_timestamp(self, scenario_id: str):
        """Update scenario's updated_at timestamp."""
        self.conn.execute("""
            UPDATE scenarios SET updated_at = ? WHERE scenario_id = ?
        """, [datetime.utcnow(), scenario_id])
    
    def persist_entities(
        self,
        entities: List[Dict],
        entity_type: str,
        scenario_id: Optional[str] = None,
        scenario_name: Optional[str] = None,
        scenario_description: Optional[str] = None,
        context_keywords: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        batch_number: Optional[int] = None,
        total_batches: Optional[int] = None,
    ) -> PersistResult:
        """
        Persist entities to DuckDB and return summary.
        
        If no scenario_id provided:
        - Creates new scenario with auto-generated name
        - Uses context_keywords for naming if available
        
        Args:
            entities: List of entity dictionaries to persist
            entity_type: Type of entities (patient, claim, etc.)
            scenario_id: Existing scenario ID to add to (optional)
            scenario_name: Name for new scenario (optional, auto-generated if not provided)
            scenario_description: Description for new scenario (optional)
            context_keywords: Keywords from generation context for auto-naming
            tags: Tags for the scenario
            batch_number: Current batch number (for progress tracking)
            total_batches: Total number of batches (for progress tracking)
            
        Returns:
            PersistResult with summary (NOT full entity data)
        """
        if not entities:
            raise ValueError("No entities to persist")
        
        # Normalize entity type
        entity_type = entity_type.lower().rstrip('s') + 's'  # Ensure plural
        
        # Get table info
        table_info = get_table_info(entity_type)
        if not table_info:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        table_name, id_column = table_info
        
        # Get serializer
        serializer = get_serializer(entity_type)
        
        # Create or use existing scenario
        is_new_scenario = False
        if not scenario_id:
            is_new_scenario = True
            
            # Generate name if not provided
            if not scenario_name:
                scenario_name = generate_scenario_name(
                    keywords=context_keywords,
                    entity_type=entity_type,
                    connection=self.conn,
                )
            else:
                scenario_name = ensure_unique_name(
                    sanitize_name(scenario_name),
                    connection=self.conn,
                )
            
            scenario_id = self._create_scenario(
                name=scenario_name,
                description=scenario_description,
                tags=tags,
            )
        else:
            # Get existing scenario name
            result = self.conn.execute("""
                SELECT name FROM scenarios WHERE scenario_id = ?
            """, [scenario_id]).fetchone()
            
            if not result:
                raise ValueError(f"Scenario not found: {scenario_id}")
            
            scenario_name = result[0]
        
        # Persist entities
        entity_ids = []
        
        for entity in entities:
            # Serialize entity
            if serializer:
                serialized = serializer(entity)
            else:
                serialized = entity.copy()
            
            # Add scenario_id
            serialized['scenario_id'] = scenario_id
            
            # Get or generate entity ID
            entity_id = serialized.get(id_column) or str(uuid4())
            serialized[id_column] = entity_id
            entity_ids.append(entity_id)
            
            # Build insert statement
            columns = list(serialized.keys())
            placeholders = ', '.join(['?' for _ in columns])
            column_str = ', '.join(columns)
            
            try:
                self.conn.execute(f"""
                    INSERT INTO {table_name} ({column_str})
                    VALUES ({placeholders})
                """, list(serialized.values()))
            except Exception as e:
                # Handle duplicate key by updating
                if 'duplicate' in str(e).lower() or 'unique' in str(e).lower():
                    # Update existing record
                    set_clause = ', '.join([f"{col} = ?" for col in columns if col != id_column])
                    values = [v for k, v in serialized.items() if k != id_column]
                    values.append(entity_id)
                    
                    self.conn.execute(f"""
                        UPDATE {table_name}
                        SET {set_clause}
                        WHERE {id_column} = ?
                    """, values)
                else:
                    raise
        
        # Update scenario timestamp
        self._update_scenario_timestamp(scenario_id)
        
        # Generate summary
        summary = generate_summary(
            scenario_id=scenario_id,
            include_samples=True,
            samples_per_type=3,
            connection=self.conn,
        )
        
        return PersistResult(
            scenario_id=scenario_id,
            scenario_name=scenario_name,
            entity_type=entity_type,
            entities_persisted=len(entities),
            entity_ids=entity_ids,
            summary=summary,
            is_new_scenario=is_new_scenario,
            batch_number=batch_number,
            total_batches=total_batches,
        )
    
    def get_scenario_summary(
        self,
        scenario_id: Optional[str] = None,
        scenario_name: Optional[str] = None,
        include_samples: bool = True,
        samples_per_type: int = 3,
    ) -> ScenarioSummary:
        """
        Get scenario summary for loading into context.
        
        IMPORTANT: Never loads full entity data!
        Returns summary (~500 tokens) + samples (~3000 tokens)
        
        Args:
            scenario_id: Scenario UUID (optional if name provided)
            scenario_name: Scenario name for fuzzy lookup (optional if ID provided)
            include_samples: Whether to include sample entities
            samples_per_type: Number of samples per entity type
            
        Returns:
            ScenarioSummary with counts, statistics, and samples
        """
        # Resolve scenario ID
        if not scenario_id:
            if not scenario_name:
                raise ValueError("Either scenario_id or scenario_name required")
            
            scenario_id = get_scenario_by_name(scenario_name, self.conn)
            if not scenario_id:
                raise ValueError(f"Scenario not found: {scenario_name}")
        
        return generate_summary(
            scenario_id=scenario_id,
            include_samples=include_samples,
            samples_per_type=samples_per_type,
            connection=self.conn,
        )
    
    def query_scenario(
        self,
        scenario_id: str,
        query: str,
        limit: int = 20,
        offset: int = 0,
    ) -> QueryResult:
        """
        Execute paginated query against scenario data.
        
        Args:
            scenario_id: Scenario to query
            query: SQL SELECT query
            limit: Results per page (default 20, max 100)
            offset: Starting offset
            
        Returns:
            QueryResult with paginated results
            
        Raises:
            ValueError: If query is not SELECT-only
        """
        # Validate query
        _validate_query(query)
        
        # Enforce limits
        limit = min(limit, 100)
        
        # Modify query to add pagination and scenario filter
        # This is a simplified approach - assumes query doesn't already have LIMIT
        query_lower = query.lower().strip()
        
        # Add scenario_id filter if not already present
        if 'scenario_id' not in query_lower:
            # Find WHERE clause or add one
            if ' where ' in query_lower:
                # Add to existing WHERE
                where_idx = query_lower.index(' where ') + 7
                query = query[:where_idx] + f"scenario_id = '{scenario_id}' AND " + query[where_idx:]
            else:
                # Find FROM clause and add WHERE after table name
                # This is simplified - proper SQL parsing would be more robust
                from_match = re.search(r'\bFROM\s+(\w+)', query, re.IGNORECASE)
                if from_match:
                    table_end = from_match.end()
                    query = query[:table_end] + f" WHERE scenario_id = '{scenario_id}'" + query[table_end:]
        
        # Remove any existing LIMIT/OFFSET
        query = re.sub(r'\bLIMIT\s+\d+', '', query, flags=re.IGNORECASE)
        query = re.sub(r'\bOFFSET\s+\d+', '', query, flags=re.IGNORECASE)
        
        # Get total count first
        count_query = f"SELECT COUNT(*) FROM ({query}) AS subquery"
        try:
            total_count = self.conn.execute(count_query).fetchone()[0]
        except Exception:
            total_count = 0
        
        # Add pagination
        paginated_query = f"{query} LIMIT {limit} OFFSET {offset}"
        
        # Execute query
        try:
            result = self.conn.execute(paginated_query)
            columns = [desc[0] for desc in result.description]
            rows = result.fetchall()
            
            results = []
            for row in rows:
                row_dict = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    # Convert special types
                    if isinstance(value, (datetime,)):
                        value = value.isoformat()
                    row_dict[col] = value
                results.append(row_dict)
        except Exception as e:
            raise ValueError(f"Query error: {str(e)}")
        
        page = offset // limit if limit > 0 else 0
        has_more = (offset + len(results)) < total_count
        
        return QueryResult(
            results=results,
            total_count=total_count,
            page=page,
            page_size=limit,
            has_more=has_more,
            query_executed=paginated_query,
        )
    
    def list_scenarios(
        self,
        filter_pattern: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 20,
        sort_by: str = "updated_at",
    ) -> List[ScenarioBrief]:
        """
        List available scenarios with brief stats.
        
        Args:
            filter_pattern: Filter by name pattern (case-insensitive)
            tag: Filter by tag
            limit: Maximum results
            sort_by: Sort field (updated_at, created_at, name)
            
        Returns:
            List of ScenarioBrief objects
        """
        # Build query
        query = """
            SELECT 
                s.scenario_id,
                s.name,
                s.description,
                s.created_at,
                s.updated_at
            FROM scenarios s
        """
        
        params = []
        conditions = []
        
        if filter_pattern:
            conditions.append("LOWER(s.name) LIKE LOWER(?)")
            params.append(f"%{filter_pattern}%")
        
        if tag:
            query += " JOIN scenario_tags t ON s.scenario_id = t.scenario_id"
            conditions.append("LOWER(t.tag) = LOWER(?)")
            params.append(tag)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Sort
        sort_map = {
            'updated_at': 's.updated_at DESC',
            'created_at': 's.created_at DESC',
            'name': 's.name ASC',
        }
        query += f" ORDER BY {sort_map.get(sort_by, 's.updated_at DESC')}"
        query += f" LIMIT {limit}"
        
        result = self.conn.execute(query, params).fetchall()
        
        scenarios = []
        for row in result:
            scenario_id = str(row[0])
            
            # Get entity count
            count = 0
            for table in ['patients', 'members', 'subjects', 'claims', 'prescriptions']:
                try:
                    cnt_result = self.conn.execute(f"""
                        SELECT COUNT(*) FROM {table} WHERE scenario_id = ?
                    """, [scenario_id]).fetchone()
                    count += cnt_result[0] if cnt_result else 0
                except Exception:
                    pass
            
            # Get tags
            tags_result = self.conn.execute("""
                SELECT tag FROM scenario_tags WHERE scenario_id = ?
            """, [scenario_id]).fetchall()
            tags = [t[0] for t in tags_result]
            
            scenarios.append(ScenarioBrief(
                scenario_id=scenario_id,
                name=row[1],
                description=row[2],
                entity_count=count,
                created_at=row[3],
                updated_at=row[4],
                tags=tags,
            ))
        
        return scenarios
    
    def rename_scenario(
        self,
        scenario_id: str,
        new_name: str,
    ) -> Tuple[str, str]:
        """
        Rename a scenario.
        
        Args:
            scenario_id: Scenario to rename
            new_name: New name for the scenario
            
        Returns:
            Tuple of (old_name, new_name)
            
        Raises:
            ValueError: If scenario not found or name already exists
        """
        # Get current name
        result = self.conn.execute("""
            SELECT name FROM scenarios WHERE scenario_id = ?
        """, [scenario_id]).fetchone()
        
        if not result:
            raise ValueError(f"Scenario not found: {scenario_id}")
        
        old_name = result[0]
        
        # Sanitize and ensure unique
        new_name = sanitize_name(new_name)
        new_name = ensure_unique_name(new_name, self.conn)
        
        # Update
        self.conn.execute("""
            UPDATE scenarios SET name = ?, updated_at = ?
            WHERE scenario_id = ?
        """, [new_name, datetime.utcnow(), scenario_id])
        
        return (old_name, new_name)
    
    def delete_scenario(
        self,
        scenario_id: str,
        confirm: bool = False,
    ) -> Dict[str, Any]:
        """
        Delete scenario and all linked entities.
        
        Args:
            scenario_id: Scenario to delete
            confirm: Must be True to proceed with deletion
            
        Returns:
            Dict with deleted scenario info
            
        Raises:
            ValueError: If confirm is not True or scenario not found
        """
        if not confirm:
            raise ValueError("Deletion requires confirm=True")
        
        # Get scenario info
        result = self.conn.execute("""
            SELECT name, description FROM scenarios WHERE scenario_id = ?
        """, [scenario_id]).fetchone()
        
        if not result:
            raise ValueError(f"Scenario not found: {scenario_id}")
        
        name = result[0]
        description = result[1]
        
        # Count entities before deletion
        entity_count = 0
        for table in ENTITY_TABLE_MAP.values():
            table_name = table[0] if isinstance(table, tuple) else table
            try:
                cnt = self.conn.execute(f"""
                    SELECT COUNT(*) FROM {table_name} WHERE scenario_id = ?
                """, [scenario_id]).fetchone()
                entity_count += cnt[0] if cnt else 0
            except Exception:
                pass
        
        # Delete entities from all tables
        for table in ENTITY_TABLE_MAP.values():
            table_name = table[0] if isinstance(table, tuple) else table
            try:
                self.conn.execute(f"""
                    DELETE FROM {table_name} WHERE scenario_id = ?
                """, [scenario_id])
            except Exception:
                pass
        
        # Delete tags
        self.conn.execute("""
            DELETE FROM scenario_tags WHERE scenario_id = ?
        """, [scenario_id])
        
        # Delete scenario
        self.conn.execute("""
            DELETE FROM scenarios WHERE scenario_id = ?
        """, [scenario_id])
        
        return {
            'scenario_id': scenario_id,
            'name': name,
            'description': description,
            'entity_count': entity_count,
        }
    
    def get_entity_samples(
        self,
        scenario_id: str,
        entity_type: str,
        count: int = 3,
        strategy: str = "diverse",
    ) -> List[Dict]:
        """
        Get sample entities for pattern consistency.
        
        Args:
            scenario_id: Scenario to get samples from
            entity_type: Type of entities to sample
            count: Number of samples (default 3)
            strategy: Sampling strategy
                - "diverse": Maximize variety (default)
                - "random": Random selection
                - "recent": Most recently added
                
        Returns:
            List of sample entity dictionaries
        """
        # Normalize entity type
        entity_type = entity_type.lower()
        if not entity_type.endswith('s'):
            entity_type = entity_type + 's'
        
        # Get table info
        table_info = get_table_info(entity_type)
        if not table_info:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        table_name, id_column = table_info
        
        # Build query based on strategy
        if strategy == "random":
            order_clause = "ORDER BY RANDOM()"
        elif strategy == "recent":
            order_clause = "ORDER BY created_at DESC"
        else:  # diverse - sample evenly across the dataset
            order_clause = "ORDER BY created_at"
        
        # Get samples
        try:
            result = self.conn.execute(f"""
                SELECT * FROM {table_name}
                WHERE scenario_id = ?
                {order_clause}
            """, [scenario_id]).fetchall()
            
            columns = [desc[0] for desc in self.conn.execute(
                f"SELECT * FROM {table_name} LIMIT 1"
            ).description]
        except Exception as e:
            raise ValueError(f"Error fetching samples: {str(e)}")
        
        if not result:
            return []
        
        # For diverse sampling, take evenly spaced samples
        if strategy == "diverse" and len(result) > count:
            step = len(result) / count
            indices = [int(i * step) for i in range(count)]
            selected = [result[i] for i in indices]
        else:
            selected = result[:count]
        
        # Convert to dicts
        samples = []
        for row in selected:
            sample = {}
            for i, col in enumerate(columns):
                value = row[i]
                if isinstance(value, datetime):
                    value = value.isoformat()
                # Skip internal columns
                if col not in ('scenario_id', 'generation_seed'):
                    sample[col] = value
            samples.append(sample)
        
        return samples


# Module-level singleton
_service: Optional[AutoPersistService] = None


def get_auto_persist_service(connection=None) -> AutoPersistService:
    """
    Get singleton service instance.
    
    Args:
        connection: Optional DuckDB connection
        
    Returns:
        AutoPersistService instance
    """
    global _service
    if _service is None or connection is not None:
        _service = AutoPersistService(connection)
    return _service


def reset_service():
    """Reset the singleton service (for testing)."""
    global _service
    _service = None
