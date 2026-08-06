"""Stub implementation for 10K earnings calls using Google ADK."""

from datetime import datetime
from typing import Any

from google.adk.tools import BaseTool


class EarningsCallStub(BaseTool):
    """Stub for fetching 10K earnings call transcripts.

    Returns mock earnings call data for development.
    """

    def __init__(self):
        """Initialize earnings call stub."""
        super().__init__(
            name="earnings_calls",
            description="Fetch 10K earnings call transcripts and financial highlights for a given stock symbol",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Fetch mock 10K earnings call transcript.

        Args:
            args: Tool arguments with 'symbol' (ticker symbol)
            tool_context: Google ADK tool context

        Returns:
            Mock earnings call transcript
        """
        symbol = args.get("symbol", "UNKNOWN")

        # Mock earnings call data
        return {
            "symbol": symbol,
            "fiscal_year": 2024,
            "quarter": "Q4",
            "date": datetime.now().isoformat(),
            "key_highlights": [
                f"{symbol} reported strong revenue growth of 15% YoY",
                "Operating margins improved to 28%",
                "Management guidance for next quarter is positive",
                "New product launches expected in Q1 2025",
            ],
            "financial_metrics": {
                "revenue": "$25.4B",
                "eps": "$2.15",
                "operating_income": "$7.1B",
                "guidance_next_q": "$26.0B - $27.0B",
            },
            "management_commentary": (
                f"We're pleased with {symbol}'s performance this quarter. "
                "Our strategic initiatives are delivering results, and we see "
                "continued momentum in our core business segments."
            ),
        }

    @property
    def input_schema(self) -> dict:
        """Define input schema for the tool."""
        return {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL, MSFT)",
                }
            },
            "required": ["symbol"],
        }