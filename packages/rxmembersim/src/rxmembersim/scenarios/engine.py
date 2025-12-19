"""Scenario execution engine."""

import random
import string
from collections.abc import Callable
from datetime import date, datetime, timedelta

from pydantic import BaseModel

from .events import RxEvent, RxEventType, RxTimeline


class RxScenarioDefinition(BaseModel):
    """Definition of a pharmacy scenario."""

    scenario_id: str
    scenario_name: str
    description: str
    duration_days: int
    event_sequence: list[dict]


class RxScenarioEngine:
    """Execute pharmacy scenarios."""

    def __init__(self) -> None:
        self.event_handlers: dict[RxEventType, Callable] = {}

    def execute_scenario(
        self,
        scenario: RxScenarioDefinition,
        member_id: str,
        start_date: date | None = None,
    ) -> RxTimeline:
        """Execute a scenario and generate timeline."""
        start_date = start_date or date.today()
        timeline = RxTimeline(member_id=member_id)

        for event_def in scenario.event_sequence:
            event_type = RxEventType(event_def["type"])
            day_offset = event_def.get("day_offset", 0)
            event_date = start_date + timedelta(days=day_offset)

            event = RxEvent(
                event_id=f"EVT{''.join(random.choices(string.digits, k=10))}",
                event_type=event_type,
                event_date=event_date,
                event_timestamp=datetime.combine(event_date, datetime.min.time()),
                member_id=member_id,
                ndc=event_def.get("data", {}).get("ndc"),
                data=event_def.get("data", {}),
                outcome=event_def.get("outcome"),
            )

            timeline.add_event(event)

        return timeline

    def list_scenarios(self) -> list[RxScenarioDefinition]:
        """List available scenarios."""
        return [
            self.new_therapy_approved(),
            self.new_therapy_pa_required(),
            self.new_therapy_step_therapy(),
            self.specialty_onboarding(),
            self.adherence_gap(),
            self.manufacturer_copay_card(),
        ]

    @staticmethod
    def new_therapy_approved() -> RxScenarioDefinition:
        """Scenario: New prescription fills successfully."""
        return RxScenarioDefinition(
            scenario_id="NEW_THERAPY_01",
            scenario_name="New Therapy - Approved",
            description="New prescription fills successfully",
            duration_days=30,
            event_sequence=[
                {"type": "new_prescription", "day_offset": 0},
                {"type": "claim_submitted", "day_offset": 0},
                {"type": "claim_approved", "day_offset": 0, "outcome": "approved"},
            ],
        )

    @staticmethod
    def new_therapy_pa_required() -> RxScenarioDefinition:
        """Scenario: Prescription requires prior authorization."""
        return RxScenarioDefinition(
            scenario_id="NEW_THERAPY_PA",
            scenario_name="New Therapy - PA Required",
            description="Prescription requires prior authorization",
            duration_days=14,
            event_sequence=[
                {"type": "new_prescription", "day_offset": 0},
                {"type": "claim_submitted", "day_offset": 0},
                {"type": "pa_required", "day_offset": 0, "data": {"reject_code": "75"}},
                {"type": "pa_submitted", "day_offset": 1},
                {"type": "pa_approved", "day_offset": 3},
                {"type": "claim_submitted", "day_offset": 3},
                {"type": "claim_approved", "day_offset": 3, "outcome": "approved"},
            ],
        )

    @staticmethod
    def new_therapy_step_therapy() -> RxScenarioDefinition:
        """Scenario: Must try preferred drug first."""
        return RxScenarioDefinition(
            scenario_id="NEW_THERAPY_ST",
            scenario_name="New Therapy - Step Therapy",
            description="Must try preferred drug first",
            duration_days=90,
            event_sequence=[
                {
                    "type": "new_prescription",
                    "day_offset": 0,
                    "data": {"drug": "target"},
                },
                {"type": "claim_submitted", "day_offset": 0},
                {
                    "type": "claim_rejected",
                    "day_offset": 0,
                    "data": {"reject_code": "76"},
                },
                {
                    "type": "new_prescription",
                    "day_offset": 1,
                    "data": {"drug": "step1"},
                },
                {"type": "claim_submitted", "day_offset": 1},
                {"type": "claim_approved", "day_offset": 1},
                {"type": "refill_due", "day_offset": 30},
                {"type": "claim_submitted", "day_offset": 30},
                {"type": "claim_approved", "day_offset": 30},
                {
                    "type": "claim_submitted",
                    "day_offset": 60,
                    "data": {"drug": "target"},
                },
                {
                    "type": "claim_approved",
                    "day_offset": 60,
                    "outcome": "step_therapy_satisfied",
                },
            ],
        )

    @staticmethod
    def specialty_onboarding() -> RxScenarioDefinition:
        """Scenario: Full specialty pharmacy workflow."""
        return RxScenarioDefinition(
            scenario_id="SPECIALTY_ONBOARD",
            scenario_name="Specialty Drug Onboarding",
            description="Full specialty pharmacy workflow",
            duration_days=21,
            event_sequence=[
                {
                    "type": "new_prescription",
                    "day_offset": 0,
                    "data": {"specialty": True},
                },
                {"type": "specialty_enrollment", "day_offset": 0},
                {"type": "hub_referral", "day_offset": 1},
                {"type": "pa_submitted", "day_offset": 2},
                {"type": "pa_approved", "day_offset": 5},
                {"type": "copay_card_applied", "day_offset": 5},
                {"type": "claim_submitted", "day_offset": 7},
                {
                    "type": "claim_approved",
                    "day_offset": 7,
                    "outcome": "specialty_dispensed",
                },
            ],
        )

    @staticmethod
    def adherence_gap() -> RxScenarioDefinition:
        """Scenario: Member misses refills then resumes."""
        return RxScenarioDefinition(
            scenario_id="ADHERENCE_GAP",
            scenario_name="Adherence Gap",
            description="Member misses refills then resumes",
            duration_days=120,
            event_sequence=[
                {"type": "claim_approved", "day_offset": 0},
                {"type": "refill_due", "day_offset": 30},
                {"type": "refill_reminder", "day_offset": 35},
                {"type": "refill_reminder", "day_offset": 45},
                {"type": "claim_submitted", "day_offset": 60},
                {
                    "type": "claim_approved",
                    "day_offset": 60,
                    "data": {"gap_days": 30},
                },
            ],
        )

    @staticmethod
    def manufacturer_copay_card() -> RxScenarioDefinition:
        """Scenario: Brand drug with manufacturer copay assistance.

        This scenario demonstrates a common pattern where patients use
        manufacturer copay cards to reduce out-of-pocket costs for
        expensive brand-name medications. The PBM coordinates the
        copay card accumulator separately from plan accumulators.
        """
        return RxScenarioDefinition(
            scenario_id="MANUFACTURER_COPAY_CARD",
            scenario_name="Manufacturer Copay Card Program",
            description=(
                "Brand drug fill with manufacturer copay assistance "
                "and accumulator coordination"
            ),
            duration_days=90,
            event_sequence=[
                # Initial prescription for expensive brand drug
                {
                    "type": "new_prescription",
                    "day_offset": 0,
                    "data": {
                        "drug": "brand_biologic",
                        "awp": 5000.00,
                        "therapeutic_class": "TNF Inhibitors",
                    },
                },
                # Claim submitted to PBM
                {"type": "claim_submitted", "day_offset": 0},
                # Initial adjudication - high copay without assistance
                {
                    "type": "claim_adjudicated",
                    "day_offset": 0,
                    "data": {
                        "patient_pay_before_card": 250.00,
                        "plan_paid": 4500.00,
                        "deductible_applied": 0,
                        "coinsurance_pct": 20,
                    },
                },
                # Copay card enrollment check
                {
                    "type": "copay_card_check",
                    "day_offset": 0,
                    "data": {
                        "manufacturer": "AbbVie",
                        "program": "Patient Assistance Program",
                        "card_id": "PAP123456",
                        "max_benefit": 15000.00,
                        "per_fill_max": 500.00,
                    },
                },
                # Copay card applied
                {
                    "type": "copay_card_applied",
                    "day_offset": 0,
                    "data": {
                        "card_payment": 225.00,
                        "patient_final_pay": 25.00,
                        "program_ytd_used": 225.00,
                        "note": "Copay reduced from $250 to $25",
                    },
                },
                # Final claim approval
                {
                    "type": "claim_approved",
                    "day_offset": 0,
                    "outcome": "approved_with_copay_card",
                    "data": {
                        "total_cost": 5000.00,
                        "plan_paid": 4500.00,
                        "copay_card_paid": 225.00,
                        "patient_paid": 25.00,
                    },
                },
                # Accumulator handling (copay accumulator vs deductible accumulator)
                {
                    "type": "accumulator_update",
                    "day_offset": 1,
                    "data": {
                        "plan_accumulator_credit": 250.00,  # Full copay counts toward OOP max
                        "copay_card_accumulator_credit": 225.00,  # Manufacturer portion tracked
                        "note": "Accumulator maximizer: copay card does NOT reduce OOP credit",
                    },
                },
                # Refill month 2
                {"type": "refill_due", "day_offset": 30},
                {
                    "type": "claim_submitted",
                    "day_offset": 30,
                    "data": {"fill_number": 1},
                },
                {
                    "type": "copay_card_applied",
                    "day_offset": 30,
                    "data": {
                        "card_payment": 225.00,
                        "patient_final_pay": 25.00,
                        "program_ytd_used": 450.00,
                    },
                },
                {
                    "type": "claim_approved",
                    "day_offset": 30,
                    "outcome": "approved_with_copay_card",
                },
                # Refill month 3
                {"type": "refill_due", "day_offset": 60},
                {
                    "type": "claim_submitted",
                    "day_offset": 60,
                    "data": {"fill_number": 2},
                },
                {
                    "type": "copay_card_applied",
                    "day_offset": 60,
                    "data": {
                        "card_payment": 225.00,
                        "patient_final_pay": 25.00,
                        "program_ytd_used": 675.00,
                    },
                },
                {
                    "type": "claim_approved",
                    "day_offset": 60,
                    "outcome": "approved_with_copay_card",
                },
            ],
        )
