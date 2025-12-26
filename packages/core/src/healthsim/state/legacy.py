"""
Legacy JSON file support for backward compatibility.

Provides functions for:
- Exporting scenarios to JSON files for sharing
- Importing JSON scenarios from external sources
- Reading old JSON scenarios during migration
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


# Legacy scenarios directory (JSON files)
LEGACY_SCENARIOS_PATH = Path.home() / ".healthsim" / "scenarios"

# Legacy workspaces directory
LEGACY_WORKSPACES_PATH = Path.home() / ".healthsim" / "workspaces"


def export_to_json(scenario: Dict[str, Any], output_path: Path) -> Path:
    """
    Export a scenario to JSON file.
    
    Args:
        scenario: Scenario dict from load_scenario()
        output_path: Where to write the file
        
    Returns:
        Path to written file
    """
    # Convert datetime objects to ISO strings
    scenario_copy = _serialize_for_json(scenario)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use atomic write (temp file + rename)
    temp_path = output_path.with_suffix('.tmp')
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(scenario_copy, f, indent=2, default=str)
    temp_path.rename(output_path)
    
    return output_path


def import_from_json(json_path: Path) -> Dict[str, Any]:
    """
    Read a scenario from JSON file.
    
    Args:
        json_path: Path to JSON file
        
    Returns:
        Scenario dict ready for save_scenario()
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Normalize structure if needed
    if 'entities' not in data:
        # Old format might have entities at top level
        entities = {}
        for key in ['patients', 'encounters', 'diagnoses', 'medications', 
                    'members', 'claims', 'prescriptions', 'subjects']:
            if key in data:
                entities[key] = data.pop(key)
        data['entities'] = entities
    
    return data


def list_legacy_scenarios() -> List[Dict[str, Any]]:
    """
    List JSON scenarios in legacy location.
    
    Returns:
        List of {name, path, modified_at, size_bytes}
    """
    scenarios = []
    
    # Check both legacy locations
    for legacy_path in [LEGACY_SCENARIOS_PATH, LEGACY_WORKSPACES_PATH]:
        if not legacy_path.exists():
            continue
        
        for json_file in legacy_path.glob("*.json"):
            try:
                stat = json_file.stat()
                scenarios.append({
                    'name': json_file.stem,
                    'path': str(json_file),
                    'modified_at': datetime.fromtimestamp(stat.st_mtime),
                    'size_bytes': stat.st_size,
                })
            except Exception:
                continue
    
    return sorted(scenarios, key=lambda x: x['modified_at'], reverse=True)


def migrate_legacy_scenario(json_path: Path, manager: Any) -> str:
    """
    Migrate a single legacy JSON scenario to DuckDB.
    
    Args:
        json_path: Path to the JSON file
        manager: StateManager instance
        
    Returns:
        Scenario ID of migrated scenario
    """
    # Read the JSON file
    data = import_from_json(json_path)
    
    # Extract name and other metadata
    name = data.get('name') or data.get('metadata', {}).get('name') or json_path.stem
    description = data.get('description') or data.get('metadata', {}).get('description')
    tags = data.get('tags') or data.get('metadata', {}).get('tags', [])
    
    # Get entities
    entities = data.get('entities', {})
    
    # Handle workspace format (EntityWithProvenance wrapper)
    for entity_type in list(entities.keys()):
        entity_list = entities[entity_type]
        if entity_list and isinstance(entity_list[0], dict) and 'data' in entity_list[0]:
            # Unwrap EntityWithProvenance
            entities[entity_type] = [
                {**e['data'], '_provenance': e.get('provenance', {})}
                for e in entity_list
            ]
    
    # Save to DuckDB
    scenario_id = manager.save_scenario(
        name=name,
        entities=entities,
        description=description,
        tags=tags,
        overwrite=True,  # Allow re-migration
    )
    
    return scenario_id


def migrate_all_legacy_scenarios(manager: Any, verbose: bool = True) -> Dict[str, str]:
    """
    Migrate all legacy JSON scenarios to DuckDB.
    
    Args:
        manager: StateManager instance
        verbose: Print progress messages
        
    Returns:
        Dict mapping original file names to scenario IDs
    """
    results = {}
    legacy_files = list_legacy_scenarios()
    
    if verbose:
        print(f"Found {len(legacy_files)} legacy scenarios to migrate")
    
    for item in legacy_files:
        json_path = Path(item['path'])
        try:
            if verbose:
                print(f"  Migrating {item['name']}...", end=" ")
            
            scenario_id = migrate_legacy_scenario(json_path, manager)
            results[item['name']] = scenario_id
            
            if verbose:
                print(f"✓ ({scenario_id[:8]})")
        except Exception as e:
            results[item['name']] = f"ERROR: {e}"
            if verbose:
                print(f"✗ ({e})")
    
    return results


def _serialize_for_json(obj: Any) -> Any:
    """Recursively convert non-JSON-serializable objects."""
    if obj is None:
        return None
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _serialize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_serialize_for_json(item) for item in obj]
    if hasattr(obj, '__dict__'):
        return _serialize_for_json(obj.__dict__)
    return obj


def export_scenario_for_sharing(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare a scenario for sharing/export (removes internal fields).
    
    Args:
        scenario: Scenario dict from load_scenario()
        
    Returns:
        Cleaned scenario dict suitable for export
    """
    # Create a clean copy
    export = {
        'name': scenario.get('name'),
        'description': scenario.get('description'),
        'tags': scenario.get('tags', []),
        'created_at': scenario.get('created_at'),
        'entities': {},
    }
    
    # Copy entities without internal provenance details
    for entity_type, entity_list in scenario.get('entities', {}).items():
        export['entities'][entity_type] = []
        for entity in entity_list:
            # Remove internal fields but keep the data
            clean_entity = {k: v for k, v in entity.items() if not k.startswith('_')}
            export['entities'][entity_type].append(clean_entity)
    
    return _serialize_for_json(export)
