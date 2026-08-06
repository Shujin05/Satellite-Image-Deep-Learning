"""Stub implementation for security screener using Google ADK."""

from typing import Any

from google.adk.tools import BaseTool


class SecurityScreenerStub(BaseTool):
    """Stub for selecting specific securities.

    Returns mock security selections for development.
    """

    def __init__(self):
        """Initialize security screener stub."""
        super().__init__(
            name="security_screener",
            description="Screen and select specific securities based on allocation strategy",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Apply factor-based screening to a list of tickers.

        Args:
            args: Tool arguments with 'tickers' (list of symbols to screen)
            tool_context: Google ADK tool context

        Returns:
            Screening results with approved and rejected tickers
        """
        tickers = args.get("tickers", [])

        # Mock: approve first N tickers, reject the rest with a reason
        approved = []
        rejected = {}
        factor_scores = {
            "NVDA": {"pe_rank": 0.55, "momentum_rank": 0.95, "quality_rank": 0.88, "composite": 0.79},
            "MSFT": {"pe_rank": 0.60, "momentum_rank": 0.72, "quality_rank": 0.94, "composite": 0.75},
            "GOOGL": {"pe_rank": 0.65, "momentum_rank": 0.68, "quality_rank": 0.90, "composite": 0.74},
            "AAPL": {"pe_rank": 0.58, "momentum_rank": 0.62, "quality_rank": 0.92, "composite": 0.71},
            "META": {"pe_rank": 0.72, "momentum_rank": 0.85, "quality_rank": 0.78, "composite": 0.78},
        }
        threshold = 0.60

        for ticker in tickers:
            scores = factor_scores.get(ticker, {"pe_rank": 0.45, "momentum_rank": 0.50, "quality_rank": 0.55, "composite": 0.50})
            if scores["composite"] >= threshold:
                approved.append({"symbol": ticker, "scores": scores})
            else:
                rejected[ticker] = f"composite factor score {scores['composite']:.2f} below threshold {threshold}"

        return {
            "approved": approved,
            "rejected": rejected,
            "screening_criteria": {
                "min_composite_score": threshold,
                "factors": ["pe_rank", "momentum_rank", "quality_rank"],
            },
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
                    "description": "List of ticker symbols to screen (e.g., ['NVDA', 'MSFT', 'GOOGL'])",
                }
            },
            "required": ["tickers"],
        }