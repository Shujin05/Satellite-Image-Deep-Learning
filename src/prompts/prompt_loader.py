"""Utility for loading prompt templates from files."""

from pathlib import Path
from typing import Dict, Optional
import yaml


class PromptLoader:
    """Loads and manages prompt templates.

    Prompts are stored as YAML files in the prompts directory.
    This allows easy editing, versioning, and A/B testing of prompts.
    """

    def __init__(self, prompts_dir: Optional[Path] = None):
        """Initialize prompt loader.

        Args:
            prompts_dir: Directory containing prompt files.
                        Defaults to this package's prompts directory.
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent
        self.prompts_dir = Path(prompts_dir)
        self._cache: Dict[str, Dict] = {}

    def load_prompt(self, filename: str) -> Dict[str, str]:
        """Load prompt from YAML file.

        Args:
            filename: Name of prompt file (e.g., 'research_agent.yaml')

        Returns:
            Dictionary with 'system' and 'user_template' keys

        Example:
            loader = PromptLoader()
            prompts = loader.load_prompt('research_agent.yaml')
            system_prompt = prompts['system']
            user_prompt = prompts['user_template'].format(symbols=["AAPL"])
        """
        # Check cache first
        if filename in self._cache:
            return self._cache[filename]

        # Load from file
        filepath = self.prompts_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Prompt file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)

        # Validate structure
        if 'system' not in prompts:
            raise ValueError(f"Prompt file {filename} missing 'system' key")

        # Cache for future use
        self._cache[filename] = prompts

        return prompts

    def format_user_prompt(self, template: str, **kwargs) -> str:
        """Format user prompt template with variables.

        Args:
            template: Prompt template string with {variable} placeholders
            **kwargs: Variables to substitute into template

        Returns:
            Formatted prompt string
        """
        return template.format(**kwargs)

    def clear_cache(self) -> None:
        """Clear the prompt cache (useful for hot-reloading in development)."""
        self._cache.clear()


# Global instance for convenience
_loader = PromptLoader()


def load_prompt(filename: str) -> Dict[str, str]:
    """Convenience function to load prompt using global loader.

    Args:
        filename: Name of prompt file

    Returns:
        Dictionary with prompt templates
    """
    return _loader.load_prompt(filename)


def get_system_prompt(filename: str) -> str:
    """Get system prompt from file.

    Args:
        filename: Name of prompt file

    Returns:
        System prompt string
    """
    prompts = load_prompt(filename)
    return prompts['system']


def format_user_prompt(filename: str, **kwargs) -> str:
    """Load and format user prompt in one step.

    Args:
        filename: Name of prompt file
        **kwargs: Variables to substitute

    Returns:
        Formatted user prompt
    """
    prompts = load_prompt(filename)
    template = prompts.get('user_template', '')
    return template.format(**kwargs)