"""Stub implementation for trade execution using Google ADK."""

from typing import Any

from google.adk.tools import BaseTool


class TradeExecutionStub(BaseTool):
    """Stub for executing trades via broker API."""

    def __init__(self):
        super().__init__(
            name="execute_trade",
            description="Execute buy/sell orders through broker API — takes symbol, quantity, action, type and returns order_id, status, filled_price",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        symbol = args.get("symbol", "UNKNOWN")
        quantity = args.get("quantity", 0)
        action = args.get("action", "BUY")
        execution_type = args.get("type", "MARKET")

        fill_prices = {
            "NVDA": 875.20, "MSFT": 415.60, "GOOGL": 175.40,
            "AAPL": 225.80, "META": 610.30,
        }
        filled_price = fill_prices.get(symbol, 150.0)

        return {
            "order_id": f"ORD-{symbol}-{quantity}",
            "status": "filled",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "execution_type": execution_type,
            "filled_price": filled_price,
            "filled_quantity": quantity,
            "execution_time": "2026-02-19T10:30:00Z",
            "commission": round(quantity * filled_price * 0.0001, 2),
            "slippage_bps": 2.1,
        }

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Stock ticker symbol (e.g., NVDA)"},
                "quantity": {"type": "integer", "description": "Number of shares to trade"},
                "action": {"type": "string", "enum": ["BUY", "SELL"], "description": "Trade direction"},
                "type": {"type": "string", "enum": ["MARKET", "LIMIT", "VWAP", "TWAP"], "description": "Execution strategy"},
            },
            "required": ["symbol", "quantity", "action", "type"],
        }