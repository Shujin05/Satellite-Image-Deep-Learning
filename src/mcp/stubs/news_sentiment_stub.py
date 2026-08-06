"""Stub implementation for news sentiment using Google ADK."""

from typing import Any

from google.adk.tools import BaseTool


class NewsSentimentStub(BaseTool):
    """Stub for fetching news feeds and earnings call sentiment.

    Returns mock news sentiment data for development.
    """

    def __init__(self):
        """Initialize news sentiment stub."""
        super().__init__(
            name="news_sentiment",
            description="Get news feeds and earnings call sentiment for a stock symbol",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Fetch mock news sentiment.

        Args:
            args: Tool arguments with 'symbol' (ticker symbol)
            tool_context: Google ADK tool context

        Returns:
            Mock news sentiment data
        """
        symbol = args.get("symbol", "UNKNOWN")

        return {
            "symbol": symbol,
            "overall_sentiment": "positive",
            "sentiment_score": 0.72,
            "news_headlines": [
                {"headline": f"{symbol} beats earnings estimates for Q4", "sentiment": "positive", "date": "2026-02-10"},
                {"headline": f"{symbol} announces expanded AI initiatives", "sentiment": "positive", "date": "2026-02-08"},
                {"headline": f"{symbol} faces mild headwinds from macro uncertainty", "sentiment": "negative", "date": "2026-02-05"},
            ],
            "earnings_call_sentiment": {
                "tone": "confident",
                "management_guidance": "raised",
                "key_themes": ["AI growth", "margin expansion", "international demand"],
                "analyst_questions_tone": "constructive",
            },
            "social_momentum": "rising",
            "institutional_flow": "net_buying",
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