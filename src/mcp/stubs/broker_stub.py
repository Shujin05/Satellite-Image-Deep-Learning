"""Stub implementation for broker API."""

import random
from datetime import datetime


class BrokerStub:
    """Stub implementation of broker API.

    Returns mock data for development and testing.
    """

    def __init__(self):
        """Initialize broker stub."""
        self.name = "broker_api"

    async def execute_trade(self, symbol: str, quantity: int, side: str) -> dict:
        """Execute a mock trade.

        Args:
            symbol: Ticker symbol
            quantity: Number of shares
            side: 'BUY' or 'SELL'

        Returns:
            Trade execution result
        """
        return {
            "order_id": f"ORD{random.randint(10000, 99999)}",
            "symbol": symbol,
            "quantity": quantity,
            "side": side,
            "status": "FILLED",
            "fill_price": round(random.uniform(50, 500), 2),
            "timestamp": datetime.now().isoformat(),
        }