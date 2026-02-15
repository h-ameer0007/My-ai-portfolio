"""Analytics page - Video performance tracking."""

import streamlit as st
from services.data_service import DataService


def render():
    st.title("Analytics")
    st.markdown("Track video performance after publishing.")

    data_service = DataService()
    projects = data_service.get_all_projects()

    if not projects:
        st.info("No projects yet.")
        return

    # Project selector
    project_names = {p["id"]: p["name"] for p in projects}
    selected_id = st.selectbox(
        "Select Project",
        list(project_names.keys()),
        format_func=lambda x: project_names[x],
    )

    if not selected_id:
        return

    st.markdown("---")

    # Input analytics data
    st.subheader("Record Analytics")
    with st.form("add_analytics"):
        col1, col2, col3 = st.columns(3)
        with col1:
            views = st.number_input("Views", min_value=0, value=0)
            likes = st.number_input("Likes", min_value=0, value=0)
            comments = st.number_input("Comments", min_value=0, value=0)
        with col2:
            ctr = st.number_input("CTR (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
            avg_duration = st.number_input("Avg View Duration (min)", min_value=0.0, value=0.0, step=0.1)
            watch_hours = st.number_input("Watch Time (hours)", min_value=0.0, value=0.0, step=0.1)
        with col3:
            shares = st.number_input("Shares", min_value=0, value=0)
            revenue = st.number_input("Revenue ($)", min_value=0.0, value=0.0, step=0.01)
            date = st.date_input("Date")

        if st.form_submit_button("Record Analytics"):
            data_service.save_analytics(
                selected_id,
                views=views, likes=likes, comments=comments,
                ctr=ctr, avg_view_duration=avg_duration,
                watch_time_hours=watch_hours, shares=shares,
                revenue=revenue, date_recorded=str(date),
            )
            st.success("Analytics recorded!")
            st.rerun()

    # Display analytics
    st.markdown("---")
    st.subheader("Performance History")

    analytics = data_service.get_analytics(selected_id)
    if not analytics:
        st.info("No analytics recorded yet for this project.")
        return

    try:
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go

        df = pd.DataFrame(analytics)
        df["date_recorded"] = pd.to_datetime(df["date_recorded"])
        df = df.sort_values("date_recorded")

        # Key metrics
        latest = df.iloc[-1] if len(df) > 0 else None
        if latest is not None:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Views", f"{int(latest['views']):,}")
            with col2:
                st.metric("CTR", f"{latest['ctr']:.1f}%")
            with col3:
                st.metric("Avg Duration", f"{latest['avg_view_duration']:.1f} min")
            with col4:
                st.metric("Revenue", f"${latest['revenue']:.2f}")

        # Charts
        if len(df) > 1:
            fig_views = px.line(df, x="date_recorded", y="views", title="Views Over Time")
            st.plotly_chart(fig_views, use_container_width=True)

            fig_engagement = go.Figure()
            fig_engagement.add_trace(go.Scatter(x=df["date_recorded"], y=df["likes"], name="Likes"))
            fig_engagement.add_trace(go.Scatter(x=df["date_recorded"], y=df["comments"], name="Comments"))
            fig_engagement.add_trace(go.Scatter(x=df["date_recorded"], y=df["shares"], name="Shares"))
            fig_engagement.update_layout(title="Engagement Metrics")
            st.plotly_chart(fig_engagement, use_container_width=True)

        # Data table
        st.dataframe(df[["date_recorded", "views", "ctr", "avg_view_duration", "likes", "comments", "revenue"]])

    except ImportError:
        st.warning("Install pandas and plotly for charts.")
        for entry in analytics:
            st.text(f"{entry['date_recorded']}: {entry['views']} views, {entry['ctr']}% CTR, ${entry['revenue']}")
