"""Stub implementation for compliance checker using Google ADK."""

from typing import Any

from google.adk.tools import BaseTool


class ComplianceCheckerStub(BaseTool):
    """Stub for checking regulatory compliance.

    Returns mock compliance check results for development.
    """

    def __init__(self):
        """Initialize compliance checker stub."""
        super().__init__(
            name="compliance_checker",
            description="Check trades and positions against regulatory compliance requirements",
        )

    async def run_async(self, *, args: dict, tool_context) -> dict[str, Any]:
        """Check mock compliance.

        Args:
            args: Tool arguments with 'trades' (proposed trades)
            tool_context: Google ADK tool context

        Returns:
            Mock compliance check results
        """
        trades = args.get("trades", [])

        return {
            "compliant": True,
            "checks_passed": [
                "Position limits",
                "Concentration limits",
                "Regulatory constraints",
                "Internal policies",
            ],
            "warnings": [],
            "violations": [],
            "approval_required": False,
        }

    @property
    def input_schema(self) -> dict:
        """Define input schema for the tool."""
        return {
            "type": "object",
            "properties": {
                "trades": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "List of proposed trades to check for compliance",
                }
            },
            "required": ["trades"],
        }