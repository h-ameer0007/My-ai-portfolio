"""Settings page - API configuration & model selection."""

import streamlit as st
from services.gemini_service import GeminiService
from services.claude_service import ClaudeService
from services.youtube_service import YouTubeService
from config.settings import GEMINI_API_KEY, CLAUDE_API_KEY, YOUTUBE_API_KEY


def render():
    st.title("Settings")
    st.markdown("Configure API keys and model selection.")

    # API Key Status
    st.subheader("API Keys")
    st.markdown("""
    API keys are configured via the `.env` file in the project root.
    Create a `.env` file with:
    ```
    GEMINI_API_KEY=your_key_here
    CLAUDE_API_KEY=your_key_here
    YOUTUBE_API_KEY=your_key_here
    ```
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Gemini API**")
        if GEMINI_API_KEY:
            st.success(f"Configured ({GEMINI_API_KEY[:8]}...)")
        else:
            st.error("Not configured")
    with col2:
        st.markdown("**Claude API**")
        if CLAUDE_API_KEY:
            st.success(f"Configured ({CLAUDE_API_KEY[:8]}...)")
        else:
            st.error("Not configured")
    with col3:
        st.markdown("**YouTube API**")
        if YOUTUBE_API_KEY:
            st.success(f"Configured ({YOUTUBE_API_KEY[:8]}...)")
        else:
            st.warning("Optional - not configured")

    # Test connections
    st.markdown("---")
    st.subheader("Test Connections")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Test Gemini"):
            gemini = GeminiService()
            success, msg = gemini.test_connection()
            if success:
                st.success(msg)
            else:
                st.error(msg)
    with col2:
        if st.button("Test Claude"):
            claude = ClaudeService()
            success, msg = claude.test_connection()
            if success:
                st.success(msg)
            else:
                st.error(msg)
    with col3:
        if st.button("Test YouTube"):
            yt = YouTubeService()
            success, msg = yt.test_connection()
            if success:
                st.success(msg)
            else:
                st.error(msg)

    # Model Selection
    st.markdown("---")
    st.subheader("Gemini Model Selection")

    gemini = GeminiService()
    if not gemini.is_configured():
        st.warning("Configure Gemini API key first.")
        return

    current_model = st.session_state.get("selected_gemini_model", gemini.current_model_name)
    st.markdown(f"**Current Model:** {current_model}")

    # List available models
    if st.button("Refresh Available Models"):
        st.session_state["available_models"] = gemini.list_available_models()

    models = st.session_state.get("available_models", [])

    if not models:
        st.info("Click 'Refresh Available Models' to see available options.")
        models = gemini.list_available_models()
        if models:
            st.session_state["available_models"] = models

    if models:
        # Categorize models
        pro_models = [m for m in models if m["category"] == "PRO"]
        flash_models = [m for m in models if m["category"] == "Flash"]
        other_models = [m for m in models if m["category"] == "Other"]

        st.markdown("### Available Models")

        if pro_models:
            st.markdown("**PRO Models**")
            for m in pro_models:
                col1, col2 = st.columns([3, 1])
                with col1:
                    selected = " (current)" if m["name"] == current_model else ""
                    st.markdown(f"- {m['display_name']} (`{m['name']}`){selected}")
                with col2:
                    if st.button("Select", key=f"select_{m['name']}"):
                        gemini.set_model(m["name"])
                        st.success(f"Switched to {m['name']}")
                        st.rerun()

        if flash_models:
            st.markdown("**Flash Models**")
            for m in flash_models:
                col1, col2 = st.columns([3, 1])
                with col1:
                    selected = " (current)" if m["name"] == current_model else ""
                    st.markdown(f"- {m['display_name']} (`{m['name']}`){selected}")
                with col2:
                    if st.button("Select", key=f"select_{m['name']}"):
                        gemini.set_model(m["name"])
                        st.success(f"Switched to {m['name']}")
                        st.rerun()

        if other_models:
            with st.expander("Other Models"):
                for m in other_models:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        selected = " (current)" if m["name"] == current_model else ""
                        st.markdown(f"- {m['display_name']} (`{m['name']}`){selected}")
                    with col2:
                        if st.button("Select", key=f"select_{m['name']}"):
                            gemini.set_model(m["name"])
                            st.success(f"Switched to {m['name']}")
                            st.rerun()

    # Test selected model
    st.markdown("---")
    if st.button("Test Current Model"):
        success, msg = gemini.test_connection()
        if success:
            st.success(msg)
        else:
            st.error(msg)
