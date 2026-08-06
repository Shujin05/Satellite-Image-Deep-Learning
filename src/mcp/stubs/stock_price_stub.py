"""Stub implementation for stock prices using Google ADK."""

import random
from datetime import datetime
from typing import Any

from google.adk.tools import BaseTool


class StockPriceStub(BaseTool):
    """Stub for fetching real-time stock prices.

    Returns mock stock price data for development.
    """

    def __init__(self):
        """Initialize stock price stub."""
        super().__init__(
            name="stock_prices",
            description="Get real-time stock prices, metrics, and market data for given stock symbols",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Fetch mock stock price data.

        Args:
            args: Tool arguments with 'symbols' (list of ticker symbols)
            tool_context: Google ADK tool context

        Returns:
            Mock stock price data for each symbol
        """
        symbols = args.get("symbols", [])
        if isinstance(symbols, str):
            symbols = [symbols]

        prices = {}
        for symbol in symbols:
            prices[symbol] = {
                "price": round(random.uniform(50, 500), 2),
                "change": round(random.uniform(-10, 10), 2),
                "change_percent": round(random.uniform(-5, 5), 2),
                "volume": random.randint(1_000_000, 50_000_000),
                "market_cap": f"${random.randint(100, 3000)}B",
                "pe_ratio": round(random.uniform(15, 35), 1),
                "52_week_high": round(random.uniform(400, 600), 2),
                "52_week_low": round(random.uniform(50, 200), 2),
                "timestamp": datetime.now().isoformat(),
            }

        return {"prices": prices, "status": "success"}

    @property
    def input_schema(self) -> dict:
        """Define input schema for the tool."""
        return {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of stock ticker symbols (e.g., ['AAPL', 'MSFT'])",
                }
            },
            "required": ["symbols"],
        }