"""Stub implementation for portfolio optimizer using Google ADK."""

from typing import Any

from google.adk.tools import BaseTool


class PortfolioOptimizerStub(BaseTool):
    """Stub for optimizing portfolio allocation.

    Returns mock optimized portfolio allocation for development.
    """

    def __init__(self):
        """Initialize portfolio optimizer stub."""
        super().__init__(
            name="portfolio_optimizer",
            description="Run mean-variance optimization over approved tickers — returns per-ticker weights and portfolio statistics",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Run mean-variance optimization over a set of approved tickers.

        Args:
            args: Tool arguments with 'tickers' (list) and 'risk_tolerance'
            tool_context: Google ADK tool context

        Returns:
            Optimized per-ticker weights and portfolio statistics
        """
        tickers = args.get("tickers", [])
        risk_tolerance = args.get("risk_tolerance", "moderate")

        if not tickers:
            tickers = ["CASH"]

        n = len(tickers)
        base_weight = round(1.0 / n, 4)
        weights = {t: base_weight for t in tickers}

        # At aggressive tolerance, tilt toward top pick (up to 50%)
        if risk_tolerance == "aggressive" and n > 1:
            top = tickers[0]
            weights[top] = round(min(base_weight * 1.5, 0.50), 4)
            remainder = round(1.0 - weights[top], 4)
            per_other = round(remainder / (n - 1), 4)
            for t in tickers[1:]:
                weights[t] = per_other

        return {
            "allocations": weights,
            "expected_return": 0.14,
            "portfolio_volatility": 0.18,
            "sharpe_ratio": 0.72,
            "optimization_method": "mean-variance",
            "risk_tolerance_used": risk_tolerance,
        }

    @property
    def input_schema(self) -> dict:
        """Define input schema for the tool."""
        return {
            "type": "object",
            "properties": {
                "tickers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Approved ticker symbols to optimize over (e.g., ['NVDA', 'MSFT'])",
                },
                "risk_tolerance": {
                    "type": "string",
                    "enum": ["conservative", "moderate", "aggressive"],
                    "description": "Risk tolerance level driving concentration vs. diversification",
                },
            },
            "required": ["tickers", "risk_tolerance"],
        }