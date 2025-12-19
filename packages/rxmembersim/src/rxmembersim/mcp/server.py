"""RxMemberSim MCP Server."""

from datetime import date
from decimal import Decimal

try:
    from mcp.server import Server

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    Server = None  # type: ignore[misc,assignment]

from healthsim.state import Provenance

from ..authorization.prior_auth import PriorAuthWorkflow
from ..claims.adjudication import AdjudicationEngine
from ..core.member import RxMemberFactory
from ..dur.validator import DURValidator
from ..formulary.formulary import FormularyGenerator
from ..scenarios.engine import RxScenarioEngine
from .session import session_manager

# Initialize components
member_generator = RxMemberFactory()
formulary = FormularyGenerator().generate_standard_commercial()
adjudication_engine = AdjudicationEngine(formulary=formulary)
dur_validator = DURValidator()
pa_workflow = PriorAuthWorkflow()
scenario_engine = RxScenarioEngine()

if MCP_AVAILABLE:
    server = Server("rxmembersim")

    @server.tool()
    async def generate_rx_member(
        bin: str = "610014",
        pcn: str = "RXTEST",
        group_number: str = "GRP001",
    ) -> dict:
        """Generate a pharmacy benefit member.

        Args:
            bin: BIN number (identifies PBM)
            pcn: Processor Control Number
            group_number: Group identifier

        Returns:
            Generated RxMember as dictionary
        """
        member = member_generator.generate(
            bin=bin, pcn=pcn, group_number=group_number
        )
        # Add to session manager instead of local cache
        session_manager.add_rx_member(
            rx_member=member,
            provenance=Provenance.generated(skill="generate_rx_member"),
        )
        return member.model_dump()

    @server.tool()
    async def check_formulary(
        ndc: str,
    ) -> dict:
        """Check formulary status for a drug.

        Args:
            ndc: Drug NDC to check

        Returns:
            FormularyStatus with coverage details
        """
        status = formulary.check_coverage(ndc)
        return status.model_dump()

    @server.tool()
    async def check_dur(
        gpi: str,
        current_medications: list[str] | None = None,
    ) -> dict:
        """Run DUR checks for a drug.

        Args:
            gpi: Drug GPI
            current_medications: List of current medication GPIs

        Returns:
            DUR validation result with alerts
        """
        result = dur_validator.validate(
            ndc="",
            gpi=gpi,
            member_id="",
            service_date=date.today(),
            current_medications=current_medications or [],
        )
        return result.model_dump()

    @server.tool()
    async def submit_prior_auth(
        member_id: str,
        ndc: str,
        drug_name: str,
        prescriber_npi: str,
        prescriber_name: str,
        quantity: float = 1,
        days_supply: int = 30,
        urgency: str = "routine",
    ) -> dict:
        """Submit a prior authorization request.

        Args:
            member_id: Member identifier
            ndc: Drug NDC
            drug_name: Drug name
            prescriber_npi: Prescriber NPI
            prescriber_name: Prescriber name
            quantity: Quantity requested
            days_supply: Days supply
            urgency: "routine", "urgent", or "emergency"

        Returns:
            PA request and any auto-approval
        """
        request = pa_workflow.create_request(
            member_id=member_id,
            cardholder_id=member_id,
            ndc=ndc,
            drug_name=drug_name,
            quantity=Decimal(str(quantity)),
            days_supply=days_supply,
            prescriber_npi=prescriber_npi,
            prescriber_name=prescriber_name,
            urgency=urgency,
        )

        auto_response = pa_workflow.check_auto_approval(request)

        return {
            "request": request.model_dump(),
            "auto_approved": auto_response is not None,
            "response": auto_response.model_dump() if auto_response else None,
        }

    @server.tool()
    async def run_rx_scenario(
        scenario_id: str,
        member_id: str | None = None,
    ) -> dict:
        """Execute a pharmacy scenario.

        Args:
            scenario_id: Scenario identifier (e.g., "NEW_THERAPY_01")
            member_id: Optional member (generates if not provided)

        Returns:
            Timeline of events
        """
        scenarios = {s.scenario_id: s for s in scenario_engine.list_scenarios()}

        if scenario_id not in scenarios:
            return {
                "error": f"Unknown scenario: {scenario_id}",
                "available": list(scenarios.keys()),
            }

        if not member_id:
            member = member_generator.generate()
            member_id = member.member_id

        timeline = scenario_engine.execute_scenario(
            scenario=scenarios[scenario_id],
            member_id=member_id,
        )

        return {
            "scenario": scenarios[scenario_id].model_dump(),
            "member_id": member_id,
            "events": [e.model_dump() for e in timeline.events],
        }

    @server.tool()
    async def list_scenarios() -> list[dict]:
        """List available pharmacy scenarios.

        Returns:
            List of scenario definitions
        """
        return [s.model_dump() for s in scenario_engine.list_scenarios()]

else:
    server = None


def main() -> None:
    """Run the MCP server."""
    if not MCP_AVAILABLE:
        print("MCP package not installed. Install with: pip install mcp")
        return

    import asyncio

    asyncio.run(server.run())  # type: ignore[union-attr]


if __name__ == "__main__":
    main()
