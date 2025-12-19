"""Tests for scenario skill files."""

from pathlib import Path

import pytest

from patientsim.skills.loader import SkillLoader
from patientsim.skills.schema import SkillType


class TestScenarioSkills:
    """Tests for scenario template skills."""

    @pytest.fixture
    def skills_dir(self) -> Path:
        """Get the skills directory path."""
        return Path(__file__).parent.parent.parent / "skills"

    @pytest.fixture
    def loader(self) -> SkillLoader:
        """Create a skill loader."""
        return SkillLoader()

    def test_load_diabetes_management(self, skills_dir: Path, loader: SkillLoader) -> None:
        """Test loading diabetes management scenario."""
        skill_path = skills_dir / "scenarios" / "diabetes-management.md"
        if not skill_path.exists():
            pytest.skip(f"Skill file not found: {skill_path}")

        skill = loader.load_file(skill_path)

        # Verify basic metadata
        assert "Diabetes" in skill.name
        assert skill.metadata.type == SkillType.SCENARIO_TEMPLATE
        assert skill.metadata.version == "2.0"
        assert "diabetes" in skill.metadata.tags

        # Verify v2.0-specific sections
        assert skill.is_v2_format()
        assert skill.for_claude is not None
        assert skill.purpose is not None

        # Verify parameters exist
        assert len(skill.parameters) > 0
        param_names = {p.name for p in skill.parameters}
        assert "age_range" in param_names

        # Verify generation rules present
        assert skill.generation_rules is not None

    def test_load_ed_chest_pain(self, skills_dir: Path, loader: SkillLoader) -> None:
        """Test loading ED chest pain scenario."""
        skill_path = skills_dir / "scenarios" / "ed-chest-pain.md"
        if not skill_path.exists():
            pytest.skip(f"Skill file not found: {skill_path}")

        skill = loader.load_file(skill_path)

        # Verify basic metadata
        assert "Chest Pain" in skill.name
        assert skill.metadata.type == SkillType.SCENARIO_TEMPLATE
        assert "emergency" in skill.metadata.tags or "cardiac" in skill.metadata.tags

        # Verify v2.0-specific sections
        assert skill.is_v2_format()
        assert skill.for_claude is not None

        # Verify parameters
        assert len(skill.parameters) > 0

        # Verify generation rules
        assert skill.generation_rules is not None

    def test_load_elective_joint(self, skills_dir: Path, loader: SkillLoader) -> None:
        """Test loading elective joint replacement scenario."""
        skill_path = skills_dir / "scenarios" / "elective-joint.md"
        if not skill_path.exists():
            pytest.skip(f"Skill file not found: {skill_path}")

        skill = loader.load_file(skill_path)

        # Verify basic metadata
        assert "Joint" in skill.name
        assert skill.metadata.type == SkillType.SCENARIO_TEMPLATE
        assert "orthopedics" in skill.metadata.tags or "surgery" in skill.metadata.tags

        # Verify parameters
        assert len(skill.parameters) > 0
        param_names = {p.name for p in skill.parameters}
        assert "joint_type" in param_names

        # Verify generation rules
        assert skill.generation_rules is not None

    def test_all_scenarios_loadable(self, skills_dir: Path, loader: SkillLoader) -> None:
        """Test that v2.0 scenario skills can be loaded."""
        scenarios_dir = skills_dir / "scenarios"
        if not scenarios_dir.exists():
            pytest.skip("Scenarios directory not found")

        scenario_files = list(scenarios_dir.glob("*.md"))
        if not scenario_files:
            pytest.skip("No scenario files found")

        v2_files = ["diabetes-management.md", "ed-chest-pain.md", "elective-joint.md"]
        loaded_count = 0

        for scenario_file in scenario_files:
            if scenario_file.name not in v2_files:
                continue  # Skip non-v2 files

            skill = loader.load_file(scenario_file)

            # Basic validation
            assert skill.name, f"No name in {scenario_file}"
            assert skill.metadata, f"No metadata in {scenario_file}"
            loaded_count += 1

        assert loaded_count > 0, "No v2 scenario files were loaded"

    def test_scenario_parameters_valid(self, skills_dir: Path, loader: SkillLoader) -> None:
        """Test that scenario parameters are valid."""
        scenarios_dir = skills_dir / "scenarios"
        if not scenarios_dir.exists():
            pytest.skip("Scenarios directory not found")

        v2_files = ["diabetes-management.md", "ed-chest-pain.md", "elective-joint.md"]

        for filename in v2_files:
            scenario_file = scenarios_dir / filename
            if not scenario_file.exists():
                continue

            skill = loader.load_file(scenario_file)

            for param in skill.parameters:
                # All parameters should have a name
                assert param.name, f"Parameter without name in {scenario_file}"
