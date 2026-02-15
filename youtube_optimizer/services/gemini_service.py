"""Google Gemini API client for YouTube Semantic Optimizer."""

import google.generativeai as genai
from typing import Optional, List, Dict, Tuple
from loguru import logger

from config.settings import GEMINI_API_KEY, DEFAULT_GEMINI_MODEL


class GeminiService:
    """Handles all Gemini API interactions."""

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.current_model_name = DEFAULT_GEMINI_MODEL
        self._model = None

        if self.api_key:
            genai.configure(api_key=self.api_key)

        # Check session state for user-selected model
        try:
            import streamlit as st
            if hasattr(st, "session_state") and "selected_gemini_model" in st.session_state:
                self.current_model_name = st.session_state["selected_gemini_model"]
        except Exception:
            pass

    @property
    def model(self):
        if self._model is None or getattr(self._model, "model_name", "") != f"models/{self.current_model_name}":
            self._model = genai.GenerativeModel(self.current_model_name)
        return self._model

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def set_model(self, model_name: str):
        """Switch to a different Gemini model."""
        self.current_model_name = model_name
        self._model = None
        try:
            import streamlit as st
            st.session_state["selected_gemini_model"] = model_name
        except Exception:
            pass
        logger.info(f"Switched Gemini model to: {model_name}")

    def list_available_models(self) -> List[Dict[str, str]]:
        """List available Gemini models, categorized."""
        if not self.api_key:
            return []

        try:
            models = []
            for m in genai.list_models():
                if "generateContent" in [s for s in m.supported_generation_methods]:
                    name = m.name.replace("models/", "")
                    display = m.display_name or name

                    if "pro" in name.lower():
                        category = "PRO"
                    elif "flash" in name.lower():
                        category = "Flash"
                    else:
                        category = "Other"

                    models.append({
                        "name": name,
                        "display_name": display,
                        "category": category,
                    })
            return models
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    def generate(self, prompt: str, temperature: float = 0.7,
                 max_tokens: int = 8192) -> Tuple[str, int]:
        """Generate content using Gemini. Returns (response_text, token_count)."""
        if not self.is_configured():
            raise ValueError("Gemini API key not configured. Set GEMINI_API_KEY in .env")

        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
            )

            text = response.text
            tokens = 0
            if hasattr(response, "usage_metadata"):
                tokens = getattr(response.usage_metadata, "total_token_count", 0)

            return text, tokens

        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise

    def test_connection(self) -> Tuple[bool, str]:
        """Test the Gemini API connection."""
        try:
            response, _ = self.generate("Say 'OK' if you can read this.", temperature=0.1, max_tokens=50)
            return True, f"Connected. Model: {self.current_model_name}. Response: {response[:100]}"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
