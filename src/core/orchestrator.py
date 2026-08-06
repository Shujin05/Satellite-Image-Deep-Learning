import json

from google.adk.agents import SequentialAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

from core.registry import ComponentRegistry
from utils.logging_config import get_logger


class InvestmentOrchestrator:
    """Orchestrates the multi-agent investment workflow."""

    def __init__(self, registry: ComponentRegistry):
        """Initialize orchestrator with a populated registry.

        Args:
            registry: ComponentRegistry containing all registered agents
        """
        self.registry = registry
        self.logger = get_logger(component="orchestrator")

    def _build_workflow(self) -> SequentialAgent:
        """Build the sequential workflow from registered agents."""
        return SequentialAgent(
            name="investment_workflow",
            description="Complete investment decision workflow",
            sub_agents=[
                self.registry.get_agent("research"),
                self.registry.get_agent("security_selection"),
                self.registry.get_agent("portfolio_strategy"),
                self.registry.get_agent("risk_monitoring"),
                self.registry.get_agent("trade_execution"),
            ],
        )

    async def run_workflow(self, mandate: dict) -> dict:
        """Run the complete investment workflow.

        Args:
            mandate: Investment mandate with keys:
                - mandate: str — natural language instruction
                - portfolio_size: float — total capital in USD
                - risk_tolerance: str — conservative / moderate / aggressive
                - constraints: list[str] — position/mandate constraints

        Returns:
            Dict with "results" (per-agent outputs), "status", and "mandate"
        """
        self.logger.info("Starting investment workflow", mandate=mandate.get("mandate"))

        user_message = (
            f"Investment mandate: {mandate.get('mandate')}\n"
            f"Portfolio size: ${mandate.get('portfolio_size', 1_000_000):,.0f}\n"
            f"Risk tolerance: {mandate.get('risk_tolerance', 'moderate')}\n"
            f"Constraints: {', '.join(mandate.get('constraints', []))}\n\n"
            "Execute the full investment workflow: research → security selection → "
            "portfolio strategy → risk monitoring → trade execution."
        )

        workflow = self._build_workflow()
        runner = InMemoryRunner(agent=workflow)
        await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id="investment_system",
            session_id="session_1",
        )
        results = []

        async for event in runner.run_async(
            user_id="investment_system",
            session_id="session_1",
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=user_message)],
            ),
        ):
            if event.content and event.content.parts:
                text = "".join(
                    part.text for part in event.content.parts if hasattr(part, "text") and part.text
                )
                if text:
                    entry = {"agent": event.author, "output": text}
                    results.append(entry)
                    self.logger.debug("workflow_event", agent=event.author, content=text[:200])

        self.logger.info("Investment workflow completed", results_count=len(results))
        return {"results": results, "status": "success", "mandate": mandate}


async def run_investment_analysis(registry: ComponentRegistry, mandate: dict) -> dict:
    """Entry point for running investment analysis.

    Args:
        registry: Populated ComponentRegistry
        mandate: Investment mandate dict

    Returns:
        Analysis results
    """
    orchestrator = InvestmentOrchestrator(registry)
    return await orchestrator.run_workflow(mandate)