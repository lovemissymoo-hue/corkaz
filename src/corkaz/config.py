"""Configuration management for Corkaz."""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    # AI provider settings
    api_key: str = field(default_factory=lambda: os.environ.get("OPENAI_API_KEY", ""))
    model: str = field(default_factory=lambda: os.environ.get("CORKAZ_MODEL", "gpt-4o-mini"))
    base_url: str = field(
        default_factory=lambda: os.environ.get(
            "CORKAZ_BASE_URL", "https://api.openai.com/v1"
        )
    )

    # Conversation settings
    max_history: int = field(
        default_factory=lambda: int(os.environ.get("CORKAZ_MAX_HISTORY", "20"))
    )
    temperature: float = field(
        default_factory=lambda: float(os.environ.get("CORKAZ_TEMPERATURE", "0.7"))
    )
    system_prompt: str = field(
        default_factory=lambda: os.environ.get(
            "CORKAZ_SYSTEM_PROMPT",
            "You are a helpful AI assistant created by Corkaz.",
        )
    )

    def validate(self) -> None:
        """Raise ValueError if required settings are missing."""
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it before running Corkaz."
            )
        if self.max_history < 1:
            raise ValueError("CORKAZ_MAX_HISTORY must be at least 1.")
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("CORKAZ_TEMPERATURE must be between 0.0 and 2.0.")
