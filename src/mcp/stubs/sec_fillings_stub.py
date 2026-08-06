"""Stub implementation for SEC filings using Google ADK."""

from typing import Any

from google.adk.tools import BaseTool


class SecFilingsStub(BaseTool):
    """Stub for fetching SEC filings (10-K, 10-Q).

    Returns mock SEC filing data for development.
    """

    def __init__(self):
        """Initialize SEC filings stub."""
        super().__init__(
            name="sec_filings",
            description="Get SEC filings (10-K, 10-Q) and financial reports for a stock symbol",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Fetch mock SEC filings.

        Args:
            args: Tool arguments with 'symbol' (ticker symbol)
            tool_context: Google ADK tool context

        Returns:
            Mock SEC filings data
        """
        symbol = args.get("symbol", "UNKNOWN")

        return {
            "symbol": symbol,
            "last_10k": "Strong earnings growth, improving margins, solid free cash flow generation",
            "last_10q": "Positive outlook, beating analyst estimates by 8%, expanding market share in cloud segment",
            "filing_date": "2026-02-01",
            "fiscal_year": 2025,
            "key_metrics": {
                "revenue_growth_yoy": "14.7%",
                "gross_margin": "46.2%",
                "operating_margin": "30.1%",
                "net_margin": "26.4%",
                "eps_growth_yoy": "18.3%",
                "free_cash_flow": "112B",
                "debt_to_equity": 0.52,
                "return_on_equity": 0.34,
                "current_ratio": 1.07,
            },
            "earnings_transcript_summary": (
                "Management highlighted strong demand across all segments. CEO noted "
                "accelerating AI-driven revenue with 40% growth in services. CFO raised "
                "full-year guidance citing better-than-expected gross margins."
            ),
            "earnings_surprises": [
                {"quarter": "Q4 2025", "actual_eps": 2.40, "consensus_eps": 2.22, "surprise_pct": 8.1},
                {"quarter": "Q3 2025", "actual_eps": 2.18, "consensus_eps": 2.09, "surprise_pct": 4.3},
            ],
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