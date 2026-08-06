"""Component registry for centralized agent management."""

from typing import Any

from utils.exceptions import AgentNotFoundError
from utils.logging_config import get_logger


class ComponentRegistry:
    def __init__(self):
        """Initialize empty registry."""
        self._agents: dict[str, Any] = {}
        self.logger = get_logger(component="registry")

    def register_agent(self, name: str, agent: Any) -> None:
        """Register an agent by name.

        Args:
            name: Agent key used for lookup (e.g., "research", "trade_execution")
            agent: Google ADK LlmAgent instance

        Raises:
            ValueError: If agent name already registered
        """
        if name in self._agents:
            raise ValueError(f"Agent '{name}' is already registered")

        self._agents[name] = agent
        self.logger.info("Agent registered", name=name)

    def get_agent(self, name: str) -> Any:
        """Get agent by name.

        Raises:
            AgentNotFoundError: If agent doesn't exist
        """
        agent = self._agents.get(name)
        if agent is None:
            raise AgentNotFoundError(
                f"Agent '{name}' not found. Available: {list(self._agents.keys())}"
            )
        return agent

    def list_agents(self) -> list[str]:
        """List all registered agent names."""
        return list(self._agents.keys())

    def clear(self) -> None:
        """Clear all registered agents (useful for testing)."""
        self._agents.clear()
        self.logger.info("Registry cleared")


def register_all(registry: ComponentRegistry) -> None:
    from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams

    from agents import AGENT_SPECS
    from core.agent_factory import create_investment_agent
    from mcp.stubs.compliance_checker_stub import ComplianceCheckerStub
    from mcp.stubs.market_data_stub import MarketDataStub
    from mcp.stubs.news_sentiment_stub import NewsSentimentStub
    from mcp.stubs.portfolio_data_stub import PortfolioDataStub
    from mcp.stubs.portfolio_optimizer_stub import PortfolioOptimizerStub
    from mcp.stubs.risk_calculator_stub import RiskCalculatorStub
    from mcp.stubs.security_screener_stub import SecurityScreenerStub
    from mcp.stubs.trade_execution_stub import TradeExecutionStub
    from mcp.stubs.sec_fillings_stub import SecFilingsStub

    logger = get_logger(component="registry")
    logger.info("Registering all agents")

    market_data = MarketDataStub()
    sec_filings = SecFilingsStub()
    news_sentiment = NewsSentimentStub()
    portfolio_data = PortfolioDataStub()
    security_screener = SecurityScreenerStub()
    portfolio_optimizer = PortfolioOptimizerStub()
    risk_calculator = RiskCalculatorStub()
    compliance_checker = ComplianceCheckerStub()
    trade_execution = TradeExecutionStub()

    yfinance_docs = McpToolset(
        connection_params=SseConnectionParams(
            url="insert-mcp-sse-url-here",
        ),
    )

    registry.register_agent(
        "research",
        create_investment_agent(
            spec=AGENT_SPECS["research"],
            tools=[market_data, sec_filings, news_sentiment, yfinance_docs],
        ),
    )

    registry.register_agent(
        "security_selection",
        create_investment_agent(
            spec=AGENT_SPECS["security_selection"],
            tools=[security_screener, market_data],
        ),
    )

    registry.register_agent(
        "portfolio_strategy",
        create_investment_agent(
            spec=AGENT_SPECS["portfolio_strategy"],
            tools=[portfolio_optimizer, risk_calculator, portfolio_data],
        ),
    )

    registry.register_agent(
        "risk_monitoring",
        create_investment_agent(
            spec=AGENT_SPECS["risk_monitoring"],
            tools=[risk_calculator, compliance_checker, portfolio_data],
        ),
    )

    registry.register_agent(
        "trade_execution",
        create_investment_agent(
            spec=AGENT_SPECS["trade_execution"],
            tools=[trade_execution, compliance_checker],
        ),
    )

    logger.info("Registration complete", agents=registry.list_agents())