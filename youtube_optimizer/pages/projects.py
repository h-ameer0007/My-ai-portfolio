"""Projects page - Project management."""

import streamlit as st
from services.data_service import DataService
from config.settings import STEPS


def render():
    st.title("Projects")
    st.markdown("Manage your optimization projects.")

    data_service = DataService()
    projects = data_service.get_all_projects()

    if not projects:
        st.info("No projects yet. Go to **New Project** to create one.")
        return

    # Filter
    status_filter = st.selectbox("Filter by Status", ["All", "Active", "Completed", "Archived"])

    for project in projects:
        completed_steps = data_service.get_completed_steps(project["id"])
        progress = data_service.get_project_progress(project["id"])

        if status_filter == "Active" and len(completed_steps) == 10:
            continue
        if status_filter == "Completed" and len(completed_steps) < 10:
            continue
        if status_filter == "Archived" and project["status"] != "archived":
            continue

        with st.expander(f"**{project['name']}** ({len(completed_steps)}/10 steps)"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**Topic:** {project['topic']}")
                st.markdown(f"**Channel:** {project.get('channel', 'N/A')}")
                st.markdown(f"**Audience:** {project.get('target_audience', 'N/A')}")
                st.progress(progress, text=f"{int(progress * 100)}% complete")

                # Step status
                for step_num in range(1, 11):
                    icon = "Done" if step_num in completed_steps else "Pending"
                    st.caption(f"Step {step_num}: {STEPS[step_num]} - {icon}")

            with col2:
                tokens = data_service.get_token_usage(project["id"])
                st.markdown(f"**Tokens:** {tokens['total_tokens']:,}")
                st.caption(f"Created: {project['created_at']}")

                if st.button("Open Project", key=f"open_{project['id']}"):
                    st.session_state.current_project_id = project["id"]
                    st.rerun()

                if st.button("Delete", key=f"delete_{project['id']}", type="secondary"):
                    st.session_state[f"confirm_delete_{project['id']}"] = True

                if st.session_state.get(f"confirm_delete_{project['id']}"):
                    st.warning("Are you sure?")
                    col_y, col_n = st.columns(2)
                    with col_y:
                        if st.button("Yes, Delete", key=f"confirm_yes_{project['id']}"):
                            data_service.delete_project(project["id"])
                            del st.session_state[f"confirm_delete_{project['id']}"]
                            st.rerun()
                    with col_n:
                        if st.button("Cancel", key=f"confirm_no_{project['id']}"):
                            del st.session_state[f"confirm_delete_{project['id']}"]
                            st.rerun()
