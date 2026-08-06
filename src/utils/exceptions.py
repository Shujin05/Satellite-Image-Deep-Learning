"""Custom exceptions for the investment system."""


class InvestmentSystemError(Exception):
    """Base exception for all investment system errors."""
    pass


class AgentNotFoundError(InvestmentSystemError):
    """Raised when an agent is not found in the registry."""
    pass

