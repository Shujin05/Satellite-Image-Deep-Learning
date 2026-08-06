from dataclasses import dataclass

@dataclass
class AgentSpec:
    name: str
    prompt_file: str
    model: str = "openai/gpt-4o-mini"

AGENT_SPECS = {
    "research": AgentSpec(
        name="research_agent",
        prompt_file="research_agent.yaml",
    ),
    "portfolio_strategy": AgentSpec(
        name="portfolio_strategy_agent",
        prompt_file="portfolio_strategy_agent.yaml",
    ),
    "security_selection": AgentSpec(
        name="security_selection_agent",
        prompt_file="security_selection_agent.yaml",
    ),
    "trade_execution": AgentSpec(
        name="trade_execution_agent",
        prompt_file="trade_execution_agent.yaml",
    ),
    "risk_monitoring": AgentSpec(
        name="risk_monitoring_agent",
        prompt_file="risk_monitoring_agent.yaml",
    ),
}


__all__ = ["AgentSpec", "AGENT_SPECS"]