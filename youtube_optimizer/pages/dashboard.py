"""Dashboard page - Analytics overview."""

import streamlit as st
from services.data_service import DataService
from config.settings import STEPS


def render():
    st.title("Dashboard")
    st.markdown("Overview of your YouTube optimization projects.")

    data_service = DataService()
    projects = data_service.get_all_projects()

    if not projects:
        st.info("No projects yet. Go to **New Project** to get started.")
        return

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Projects", len(projects))
    with col2:
        active = sum(1 for p in projects if p["status"] == "active")
        st.metric("Active Projects", active)
    with col3:
        completed = sum(
            1 for p in projects
            if len(data_service.get_completed_steps(p["id"])) == 10
        )
        st.metric("Completed", completed)
    with col4:
        summary = data_service.get_all_analytics_summary()
        total_tokens = sum(
            (s.get("total_gemini_tokens") or 0) + (s.get("total_claude_tokens") or 0)
            for s in summary
        )
        st.metric("Total Tokens Used", f"{total_tokens:,}")

    st.markdown("---")

    # Recent projects
    st.subheader("Recent Projects")
    for project in projects[:10]:
        progress = data_service.get_project_progress(project["id"])
        completed_steps = data_service.get_completed_steps(project["id"])

        with st.expander(
            f"**{project['name']}** - {project['topic'][:50]} "
            f"({len(completed_steps)}/10 steps)"
        ):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(progress, text=f"{int(progress * 100)}% complete")
                st.caption(f"Created: {project['created_at']}")
                st.caption(f"Last updated: {project['updated_at']}")

                if completed_steps:
                    step_names = [
                        f"Step {s}: {STEPS.get(s, '')}" for s in completed_steps
                    ]
                    st.markdown("**Completed:** " + " | ".join(step_names))

            with col2:
                tokens = data_service.get_token_usage(project["id"])
                st.markdown(f"**Gemini tokens:** {tokens['gemini_tokens']:,}")
                st.markdown(f"**Claude tokens:** {tokens['claude_tokens']:,}")

                if st.button("Open", key=f"open_{project['id']}"):
                    st.session_state.current_project_id = project["id"]
                    st.rerun()

    # Token usage chart
    if summary:
        st.markdown("---")
        st.subheader("Token Usage by Project")
        try:
            import pandas as pd
            import plotly.express as px

            df = pd.DataFrame(summary)
            if not df.empty and "name" in df.columns:
                df["total_tokens"] = (
                    df["total_gemini_tokens"].fillna(0)
                    + df["total_claude_tokens"].fillna(0)
                )
                if df["total_tokens"].sum() > 0:
                    fig = px.bar(
                        df,
                        x="name",
                        y=["total_gemini_tokens", "total_claude_tokens"],
                        title="Token Usage",
                        labels={"value": "Tokens", "name": "Project"},
                        barmode="stack",
                    )
                    st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.warning("Install pandas and plotly for charts: pip install pandas plotly")
