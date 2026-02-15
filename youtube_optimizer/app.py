"""Main Streamlit app for YouTube Semantic Optimizer."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

st.set_page_config(
    page_title="YouTube Semantic Optimizer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.current_project_id = None


def main():
    st.sidebar.title("YouTube Semantic Optimizer")
    st.sidebar.markdown("---")

    # Navigation
    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "New Project", "Projects", "Analytics", "Settings"],
        index=0,
    )

    st.sidebar.markdown("---")

    # API status indicators
    from config.settings import GEMINI_API_KEY, CLAUDE_API_KEY, YOUTUBE_API_KEY

    st.sidebar.markdown("**API Status**")
    st.sidebar.markdown(
        f"- Gemini: {'Connected' if GEMINI_API_KEY else 'Not configured'}"
    )
    st.sidebar.markdown(
        f"- Claude: {'Connected' if CLAUDE_API_KEY else 'Not configured'}"
    )
    st.sidebar.markdown(
        f"- YouTube: {'Connected' if YOUTUBE_API_KEY else 'Not configured'}"
    )

    # Current model
    if "selected_gemini_model" in st.session_state:
        st.sidebar.markdown(f"**Model:** {st.session_state['selected_gemini_model']}")

    # Route to pages
    if page == "Dashboard":
        from pages import dashboard
        dashboard.render()
    elif page == "New Project":
        from pages import new_project
        new_project.render()
    elif page == "Projects":
        from pages import projects
        projects.render()
    elif page == "Analytics":
        from pages import analytics
        analytics.render()
    elif page == "Settings":
        from pages import settings
        settings.render()


if __name__ == "__main__":
    main()
