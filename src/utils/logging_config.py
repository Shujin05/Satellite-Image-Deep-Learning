"""Structured logging configuration using structlog.

This module sets up structured logging for the entire system,
providing consistent, contextual, and machine-readable logs.
"""

import logging
import sys
from typing import Any

import structlog


def configure_logging(log_level: str = "INFO", environment: str = "development") -> None:
    """Configure structured logging for the application.

    This function sets up structlog with appropriate processors for
    the given environment. In development, logs are human-readable
    console output. In production, logs are JSON-formatted for parsing
    by log aggregation systems.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        environment: Runtime environment (development, staging, production)

    Examples:
        >>> configure_logging("DEBUG", "development")
        >>> configure_logging("INFO", "production")
    """
    # Convert log level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Shared processors for all environments
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if environment == "production":
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            ),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=numeric_level,
    )

    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(*args: Any, **initial_values: Any) -> Any:
    """Get a logger instance with optional initial context.

    This is a convenience wrapper around structlog.get_logger() that
    allows binding initial context values.

    Args:
        *args: Positional arguments passed to structlog.get_logger()
        **initial_values: Initial context to bind to the logger

    Returns:
        A structured logger instance

    Examples:
        >>> logger = get_logger(component="research_agent")
        >>> logger.info("analysis_complete", symbols=["AAPL", "MSFT"])

        >>> logger = get_logger(agent_id="agent_123", agent_type="research")
        >>> logger.warning("retry_attempt", attempt=2, max_retries=3)
    """
    logger = structlog.get_logger(*args)
    if initial_values:
        logger = logger.bind(**initial_values)
    return logger