"""Claude API client for YouTube Semantic Optimizer (Step 8 - Script Writing)."""

import anthropic
from typing import Tuple
from loguru import logger

from config.settings import CLAUDE_API_KEY, CLAUDE_MODEL


class ClaudeService:
    """Handles Claude API interactions for script writing."""

    def __init__(self):
        self.api_key = CLAUDE_API_KEY
        self.model = CLAUDE_MODEL
        self._client = None

    @property
    def client(self):
        if self._client is None and self.api_key:
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, system_prompt: str = "",
                 temperature: float = 0.7, max_tokens: int = 8192) -> Tuple[str, int]:
        """Generate content using Claude. Returns (response_text, token_count)."""
        if not self.is_configured():
            raise ValueError("Claude API key not configured. Set CLAUDE_API_KEY in .env")

        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages,
            }
            if system_prompt:
                kwargs["system"] = system_prompt

            response = self.client.messages.create(**kwargs)

            text = response.content[0].text
            tokens = response.usage.input_tokens + response.usage.output_tokens

            return text, tokens

        except Exception as e:
            logger.error(f"Claude generation error: {e}")
            raise

    def test_connection(self) -> Tuple[bool, str]:
        """Test the Claude API connection."""
        try:
            response, _ = self.generate(
                "Say 'OK' if you can read this.",
                temperature=0.1,
                max_tokens=50,
            )
            return True, f"Connected. Model: {self.model}. Response: {response[:100]}"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
