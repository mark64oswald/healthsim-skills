"""Tests for SDTM export functionality."""

import csv
import json
import tempfile
from datetime import date
from pathlib import Path

import pytest

from trialsim.core.models import (
    AdverseEvent,
    AECausality,
    AEOutcome,
    AESeverity,
    ArmType,
    Exposure,
    Subject,
    SubjectStatus,
    Visit,
    VisitType,
)
from trialsim.formats.sdtm import (
    SDTMDomain,
    SDTMVariable,
    ExportFormat,
    ExportConfig,
    ExportResult,
    SDTMExporter,
    export_to_sdtm,
    create_sdtm_exporter,
    get_domain_variables,
    get_required_variables,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_subjects():
    """Create sample subjects for testing."""
    return [
        Subject(
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            site_id="SITE01",
            age=45,
            sex="M",
            race="WHITE",
            ethnicity="NOT HISPANIC OR LATINO",
            screening_date=date(2025, 1, 1),
            randomization_date=date(2025, 1, 8),
            arm=ArmType.TREATMENT,
            status=SubjectStatus.ON_TREATMENT,
        ),
        Subject(
            subject_id="SUBJ-002",
            protocol_id="PROTO-001",
            site_id="SITE01",
            age=52,
            sex="F",
            race="BLACK OR AFRICAN AMERICAN",
            ethnicity="NOT HISPANIC OR LATINO",
            screening_date=date(2025, 1, 3),
            randomization_date=date(2025, 1, 10),
            arm=ArmType.PLACEBO,
            status=SubjectStatus.ON_TREATMENT,
        ),
    ]


@pytest.fixture
def sample_visits(sample_subjects):
    """Create sample visits for testing."""
    return [
        Visit(
            visit_id="VST-001",
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            site_id="SITE01",
            visit_number=1,
            visit_name="Screening",
            visit_type=VisitType.SCREENING,
            planned_date=date(2025, 1, 1),
            actual_date=date(2025, 1, 1),
            visit_status="completed",
        ),
        Visit(
            visit_id="VST-002",
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            site_id="SITE01",
            visit_number=2,
            visit_name="Week 4",
            visit_type=VisitType.SCHEDULED,
            planned_date=date(2025, 2, 5),
            actual_date=date(2025, 2, 6),
            visit_status="completed",
        ),
    ]


@pytest.fixture
def sample_adverse_events():
    """Create sample adverse events for testing."""
    return [
        AdverseEvent(
            ae_id="AE-001",
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            ae_term="Headache",
            system_organ_class="Nervous system disorders",
            onset_date=date(2025, 1, 15),
            resolution_date=date(2025, 1, 17),
            severity=AESeverity.GRADE_1,
            is_serious=False,
            causality=AECausality.POSSIBLY,
            outcome=AEOutcome.RECOVERED,
        ),
        AdverseEvent(
            ae_id="AE-002",
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            ae_term="Nausea",
            system_organ_class="Gastrointestinal disorders",
            onset_date=date(2025, 1, 20),
            severity=AESeverity.GRADE_2,
            is_serious=False,
            causality=AECausality.PROBABLY,
            outcome=AEOutcome.RECOVERING,
        ),
    ]


@pytest.fixture
def sample_exposures():
    """Create sample exposures for testing."""
    return [
        Exposure(
            exposure_id="EXP-001",
            subject_id="SUBJ-001",
            protocol_id="PROTO-001",
            drug_name="Study Drug A",
            dose=100.0,
            dose_unit="mg",
            route="oral",
            start_date=date(2025, 1, 8),
            end_date=date(2025, 2, 8),
        ),
        Exposure(
            exposure_id="EXP-002",
            subject_id="SUBJ-002",
            protocol_id="PROTO-001",
            drug_name="Placebo",
            dose=0.0,
            dose_unit="mg",
            route="oral",
            start_date=date(2025, 1, 10),
        ),
    ]


# =============================================================================
# Domain Definition Tests
# =============================================================================

class TestDomainDefinitions:
    """Tests for SDTM domain definitions."""

    def test_get_dm_variables(self):
        """Test getting DM domain variables."""
        variables = get_domain_variables(SDTMDomain.DM)
        
        assert len(variables) > 0
        var_names = [v.name for v in variables]
        assert "STUDYID" in var_names
        assert "USUBJID" in var_names
        assert "AGE" in var_names
        assert "SEX" in var_names

    def test_get_ae_variables(self):
        """Test getting AE domain variables."""
        variables = get_domain_variables(SDTMDomain.AE)
        
        var_names = [v.name for v in variables]
        assert "AETERM" in var_names
        assert "AESEV" in var_names
        assert "AESER" in var_names

    def test_get_required_variables(self):
        """Test getting required variables."""
        required = get_required_variables(SDTMDomain.DM)
        
        assert "STUDYID" in required
        assert "USUBJID" in required
        assert "SEX" in required

    def test_sdtm_variable_structure(self):
        """Test SDTMVariable dataclass."""
        variables = get_domain_variables(SDTMDomain.DM)
        studyid = next(v for v in variables if v.name == "STUDYID")
        
        assert studyid.label == "Study Identifier"
        assert studyid.data_type == "Char"
        assert studyid.required is True


# =============================================================================
# Export Config Tests
# =============================================================================

class TestExportConfig:
    """Tests for ExportConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = ExportConfig()
        
        assert config.study_id == "STUDY01"
        assert config.sponsor == "SPONSOR"
        assert config.include_empty is False

    def test_custom_config(self):
        """Test custom configuration."""
        config = ExportConfig(
            study_id="MYTEST01",
            sponsor="ACME",
            domains=[SDTMDomain.DM, SDTMDomain.AE],
        )
        
        assert config.study_id == "MYTEST01"
        assert config.sponsor == "ACME"
        assert len(config.domains) == 2


# =============================================================================
# SDTM Exporter Tests
# =============================================================================

class TestSDTMExporter:
    """Tests for SDTMExporter."""

    def test_basic_creation(self):
        """Test creating exporter."""
        exporter = SDTMExporter()
        
        assert exporter.config is not None
        assert exporter.config.study_id == "STUDY01"

    def test_creation_with_config(self):
        """Test creating exporter with config."""
        config = ExportConfig(study_id="TEST01")
        exporter = SDTMExporter(config)
        
        assert exporter.config.study_id == "TEST01"

    def test_export_dm_domain(self, sample_subjects):
        """Test exporting DM domain."""
        exporter = SDTMExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export(
                subjects=sample_subjects,
                output_dir=tmpdir,
                format=ExportFormat.CSV,
            )
            
            assert result.success is True
            assert SDTMDomain.DM in result.domains_exported
            assert result.record_counts["DM"] == 2
            
            # Check file was created
            dm_file = Path(tmpdir) / "dm.csv"
            assert dm_file.exists()
            
            # Verify content
            with open(dm_file) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
            assert len(rows) == 2
            assert rows[0]["STUDYID"] == "STUDY01"
            assert rows[0]["SEX"] == "M"
            assert rows[1]["SEX"] == "F"

    def test_export_ae_domain(self, sample_subjects, sample_adverse_events):
        """Test exporting AE domain."""
        exporter = SDTMExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export(
                subjects=sample_subjects,
                adverse_events=sample_adverse_events,
                output_dir=tmpdir,
                format=ExportFormat.CSV,
            )
            
            assert result.success is True
            assert SDTMDomain.AE in result.domains_exported
            assert result.record_counts["AE"] == 2
            
            # Check file content
            ae_file = Path(tmpdir) / "ae.csv"
            with open(ae_file) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
            assert rows[0]["AETERM"] == "Headache"
            assert rows[0]["AESEV"] == "MILD"
            assert rows[1]["AETERM"] == "Nausea"
            assert rows[1]["AESEV"] == "MODERATE"

    def test_export_ex_domain(self, sample_subjects, sample_exposures):
        """Test exporting EX domain."""
        exporter = SDTMExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export(
                subjects=sample_subjects,
                exposures=sample_exposures,
                output_dir=tmpdir,
                format=ExportFormat.CSV,
            )
            
            assert result.success is True
            assert SDTMDomain.EX in result.domains_exported
            assert result.record_counts["EX"] == 2
            
            # Check file content
            ex_file = Path(tmpdir) / "ex.csv"
            with open(ex_file) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
            assert rows[0]["EXTRT"] == "Study Drug A"
            assert float(rows[0]["EXDOSE"]) == 100.0

    def test_export_sv_domain(self, sample_subjects, sample_visits):
        """Test exporting SV domain."""
        exporter = SDTMExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export(
                subjects=sample_subjects,
                visits=sample_visits,
                output_dir=tmpdir,
                format=ExportFormat.CSV,
            )
            
            assert result.success is True
            assert SDTMDomain.SV in result.domains_exported
            assert result.record_counts["SV"] == 2

    def test_export_json_format(self, sample_subjects):
        """Test exporting to JSON format."""
        exporter = SDTMExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export(
                subjects=sample_subjects,
                output_dir=tmpdir,
                format=ExportFormat.JSON,
            )
            
            assert result.success is True
            
            # Check JSON file
            dm_file = Path(tmpdir) / "dm.json"
            assert dm_file.exists()
            
            with open(dm_file) as f:
                data = json.load(f)
                
            assert len(data) == 2
            assert data[0]["STUDYID"] == "STUDY01"

    def test_export_all_domains(
        self,
        sample_subjects,
        sample_visits,
        sample_adverse_events,
        sample_exposures,
    ):
        """Test exporting all domains together."""
        exporter = SDTMExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export(
                subjects=sample_subjects,
                visits=sample_visits,
                adverse_events=sample_adverse_events,
                exposures=sample_exposures,
                output_dir=tmpdir,
                format=ExportFormat.CSV,
            )
            
            assert result.success is True
            assert len(result.domains_exported) == 4
            assert len(result.files_created) == 4

    def test_export_result_summary(self, sample_subjects):
        """Test ExportResult summary generation."""
        exporter = SDTMExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = exporter.export(
                subjects=sample_subjects,
                output_dir=tmpdir,
            )
            
            summary = result.to_summary()
            
            assert "SDTM Export Summary" in summary
            assert "Success" in summary
            assert "DM:" in summary

    def test_usubjid_format(self, sample_subjects):
        """Test USUBJID format is correct."""
        config = ExportConfig(study_id="MYTEST")
        exporter = SDTMExporter(config)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter.export(
                subjects=sample_subjects,
                output_dir=tmpdir,
            )
            
            dm_file = Path(tmpdir) / "dm.csv"
            with open(dm_file) as f:
                reader = csv.DictReader(f)
                row = next(reader)
                
            # Format should be STUDYID-SITEID-SUBJID
            assert row["USUBJID"] == "MYTEST-SITE01-SUBJ-001"

    def test_study_day_calculation(self, sample_subjects, sample_adverse_events):
        """Test study day calculation."""
        exporter = SDTMExporter()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter.export(
                subjects=sample_subjects,
                adverse_events=sample_adverse_events,
                output_dir=tmpdir,
            )
            
            ae_file = Path(tmpdir) / "ae.csv"
            with open(ae_file) as f:
                reader = csv.DictReader(f)
                row = next(reader)
                
            # AE onset 2025-01-15, randomization 2025-01-08
            # Day = 15 - 8 + 1 = 8
            assert int(row["AESTDY"]) == 8


# =============================================================================
# Convenience Function Tests
# =============================================================================

class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_export_to_sdtm(self, sample_subjects):
        """Test export_to_sdtm function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = export_to_sdtm(
                subjects=sample_subjects,
                output_dir=tmpdir,
                study_id="FUNCTEST",
            )
            
            assert result.success is True
            
            dm_file = Path(tmpdir) / "dm.csv"
            with open(dm_file) as f:
                reader = csv.DictReader(f)
                row = next(reader)
                
            assert "FUNCTEST" in row["USUBJID"]

    def test_create_sdtm_exporter(self):
        """Test create_sdtm_exporter function."""
        exporter = create_sdtm_exporter(
            study_id="FACTORY01",
            sponsor="TESTCO",
        )
        
        assert isinstance(exporter, SDTMExporter)
        assert exporter.config.study_id == "FACTORY01"
        assert exporter.config.sponsor == "TESTCO"


# =============================================================================
# Mapping Tests
# =============================================================================

class TestMappings:
    """Tests for SDTM code mappings."""

    def test_sex_mapping(self, sample_subjects):
        """Test sex code mapping."""
        exporter = SDTMExporter()
        
        assert exporter._map_sex("M") == "M"
        assert exporter._map_sex("F") == "F"
        assert exporter._map_sex("MALE") == "M"
        assert exporter._map_sex("FEMALE") == "F"
        assert exporter._map_sex("unknown") == "U"

    def test_severity_mapping(self):
        """Test severity code mapping."""
        exporter = SDTMExporter()
        
        assert exporter._map_severity(AESeverity.GRADE_1) == "MILD"
        assert exporter._map_severity(AESeverity.GRADE_2) == "MODERATE"
        assert exporter._map_severity(AESeverity.GRADE_3) == "SEVERE"

    def test_causality_mapping(self):
        """Test causality code mapping."""
        exporter = SDTMExporter()
        
        assert exporter._map_causality(AECausality.NOT_RELATED) == "NOT RELATED"
        assert exporter._map_causality(AECausality.POSSIBLY) == "POSSIBLE"
        assert exporter._map_causality(AECausality.PROBABLY) == "PROBABLE"

    def test_route_mapping(self):
        """Test route code mapping."""
        exporter = SDTMExporter()
        
        assert exporter._map_route("oral") == "ORAL"
        assert exporter._map_route("iv") == "INTRAVENOUS"
        assert exporter._map_route("sc") == "SUBCUTANEOUS"
