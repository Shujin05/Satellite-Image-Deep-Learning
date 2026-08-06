"""Stub implementation for Bloomberg market data."""

import random
from datetime import datetime


class BloombergStub:

    def __init__(self):
        """Initialize Bloomberg stub."""
        self.name = "market_data"

    async def get_market_data(self, symbols: list[str]) -> dict:
        """Get mock market data for symbols.

        Args:
            symbols: List of ticker symbols

        Returns:
            Market data for each symbol
        """
        data = {}
        for symbol in symbols:
            data[symbol] = {
                "price": round(random.uniform(50, 500), 2),
                "change": round(random.uniform(-5, 5), 2),
                "volume": random.randint(1000000, 10000000),
                "timestamp": datetime.now().isoformat(),
            }
        return data