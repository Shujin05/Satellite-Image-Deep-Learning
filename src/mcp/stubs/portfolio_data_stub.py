"""Stub implementation for market data using Google ADK."""

from typing import Any

from google.adk.tools import BaseTool


class MarketDataStub(BaseTool):
    """Stub for fetching market data.

    Returns mock market data for development.
    """

    def __init__(self):
        """Initialize market data stub."""
        super().__init__(
            name="market_data",
            description="Get real-time market data, prices, volume, and metrics for stock symbols",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Fetch mock market data.

        Args:
            args: Tool arguments with 'symbol' (ticker symbol)
            tool_context: Google ADK tool context

        Returns:
            Mock market data
        """
        symbol = args.get("symbol", "UNKNOWN")

        return {
            "symbol": symbol,
            "price": 150.0,
            "open": 148.20,
            "high": 151.80,
            "low": 147.50,
            "close": 150.0,
            "volume": 52_000_000,
            "avg_volume_30d": 48_000_000,
            "pe_ratio": 25.5,
            "eps_ttm": 5.88,
            "revenue_ttm": "391B",
            "market_cap": "2.5T",
            "52w_high": 199.62,
            "52w_low": 124.17,
            "beta": 1.24,
            "dividend_yield": 0.0044,
            "analyst_rating": "buy",
            "analyst_target_price": 175.0,
            "momentum_3m": 0.08,
            "momentum_12m": 0.22,
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