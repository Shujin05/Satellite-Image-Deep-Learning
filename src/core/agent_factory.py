from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool

from agents import AgentSpec
from prompts.prompt_loader import load_prompt
from utils.logging_config import get_logger


def create_investment_agent(
    spec: AgentSpec,
    tools: Optional[list[BaseTool]] = None,
) -> LlmAgent:
    """Create a Google ADK LlmAgent for investment analysis.

    Args:
        spec: Agent specification with name, prompt_file, and model
        tools: Tools this agent should have access to (caller is responsible
               for passing only the correct tools for this agent)

    Returns:
        Google ADK LlmAgent instance
    """
    logger = get_logger(component="agent_factory")

    instruction = None
    if spec.prompt_file:
        try:
            prompts = load_prompt(spec.prompt_file)
            instruction = prompts.get("system")
        except Exception as e:
            logger.warning(
                "Failed to load prompt file",
                prompt_file=spec.prompt_file,
                error=str(e),
            )

    agent_tools = tools or []

    logger.info(
        "Creating Google ADK agent",
        name=spec.name,
        model=spec.model,
        tools=[getattr(t, "name", str(t)) for t in agent_tools],
    )

    agent = LlmAgent(
        name=spec.name,
        model=spec.model,
        instruction=instruction,
        tools=agent_tools,
    )

    logger.info("Google ADK agent created", name=spec.name)

    return agent