"""Stub implementation for risk calculator using Google ADK."""

from typing import Any

from google.adk.tools import BaseTool


class RiskCalculatorStub(BaseTool):
    """Stub for calculating portfolio risk metrics.

    Returns mock risk calculations for development.
    """

    def __init__(self):
        """Initialize risk calculator stub."""
        super().__init__(
            name="risk_calculator",
            description="Calculate portfolio risk metrics including VaR, CVaR, and drawdown",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Calculate mock risk metrics.

        Args:
            args: Tool arguments with 'portfolio' (portfolio holdings)
            tool_context: Google ADK tool context

        Returns:
            Mock risk metrics
        """
        portfolio = args.get("portfolio", {})

        return {
            "var_95": 85000.0,
            "var_99": 120000.0,
            "cvar_95": 95000.0,
            "max_drawdown": 0.12,
            "sharpe_ratio": 1.5,
            "risk_level": "medium",
            "volatility": 0.15,
            "beta": 1.1,
            "concentration_risk": "low",
        }

    @property
    def input_schema(self) -> dict:
        """Define input schema for the tool."""
        return {
            "type": "object",
            "properties": {
                "portfolio": {
                    "type": "object",
                    "description": "Portfolio holdings and positions",
                }
            },
            "required": ["portfolio"],
        }