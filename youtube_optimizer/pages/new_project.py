"""New Project page - Main 10-step optimization workflow."""

import streamlit as st
from services.data_service import DataService
from services.gemini_service import GeminiService
from services.claude_service import ClaudeService
from services.youtube_service import YouTubeService
from utils.validators import StepValidator, OutputExtractor
from utils.prompts import (
    get_step1_prompt, get_step2_prompt, get_step3_prompt,
    get_step4_prompt, get_step5_prompt, get_step6_prompt,
    get_step7_prompt, get_step8_prompt, get_step8_system_prompt,
    get_step9_prompt, get_step10_prompt,
)
from utils.exporters import export_step_output, export_full_report_docx, export_script_docx
from config.settings import (
    STEPS, STEP_API, SCRIPT_LENGTHS, SCRIPT_STYLES,
    VIDEO_LENGTHS,
)


def render():
    st.title("New Project - 10-Step Optimization")

    data_service = DataService()
    gemini_service = GeminiService()
    claude_service = ClaudeService()
    youtube_service = YouTubeService()

    # Project creation or selection
    if "current_project_id" not in st.session_state or st.session_state.current_project_id is None:
        _render_project_creation(data_service)
    else:
        project = data_service.get_project(st.session_state.current_project_id)
        if project:
            _render_workflow(project, data_service, gemini_service, claude_service, youtube_service)
        else:
            st.error("Project not found.")
            st.session_state.current_project_id = None
            st.rerun()


def _render_project_creation(data_service: DataService):
    """Render project creation form."""
    st.subheader("Create New Project")

    with st.form("create_project"):
        name = st.text_input("Project Name", placeholder="My Awesome Video")
        topic = st.text_area("Video Topic", placeholder="Describe your video topic in detail...")
        channel = st.text_input("Channel Name (optional)", placeholder="Your YouTube channel")
        audience = st.text_input("Target Audience (optional)", placeholder="e.g., Beginner programmers aged 18-35")

        submitted = st.form_submit_button("Create Project", type="primary")
        if submitted and name and topic:
            project_id = data_service.create_project(name, topic, channel, audience)
            st.session_state.current_project_id = project_id
            st.success(f"Project '{name}' created!")
            st.rerun()
        elif submitted:
            st.error("Please provide a project name and topic.")

    # Or select existing project
    st.markdown("---")
    st.subheader("Or Continue Existing Project")
    projects = data_service.get_all_projects()
    if projects:
        for p in projects[:5]:
            completed = data_service.get_completed_steps(p["id"])
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{p['name']}** - {p['topic'][:60]}... ({len(completed)}/10 steps)")
            with col2:
                if st.button("Continue", key=f"continue_{p['id']}"):
                    st.session_state.current_project_id = p["id"]
                    st.rerun()


def _render_workflow(project, data_service, gemini_service, claude_service, youtube_service):
    """Render the 10-step workflow for a project."""
    st.markdown(f"### Project: {project['name']}")
    st.caption(f"Topic: {project['topic']}")

    # Progress bar
    completed_steps = data_service.get_completed_steps(project["id"])
    progress = data_service.get_project_progress(project["id"])
    st.progress(progress, text=f"Progress: {len(completed_steps)}/10 steps ({int(progress * 100)}%)")

    # Back button
    if st.button("Back to Project List"):
        st.session_state.current_project_id = None
        st.rerun()

    st.markdown("---")

    # Step tabs
    step_tabs = st.tabs([f"Step {i}" for i in range(1, 11)])

    for step_num in range(1, 11):
        with step_tabs[step_num - 1]:
            _render_step(
                step_num, project, data_service,
                gemini_service, claude_service, youtube_service,
                completed_steps,
            )

    # Export section
    st.markdown("---")
    st.subheader("Export")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Export Full Report (DOCX)"):
            outputs = data_service.get_all_step_outputs(project["id"])
            if outputs:
                filepath = export_full_report_docx(project["name"], project, outputs)
                st.success(f"Exported to: {filepath}")
            else:
                st.warning("No step outputs to export.")
    with col2:
        if st.button("Export Script Only"):
            script = data_service.get_step_output(project["id"], 8)
            if script:
                filepath = export_script_docx(project["name"], script)
                st.success(f"Exported to: {filepath}")
            else:
                st.warning("No script to export. Complete Step 8 first.")
    with col3:
        step_to_export = st.selectbox("Export Step", range(1, 11), format_func=lambda x: f"Step {x}: {STEPS[x]}")
        if st.button("Export Step"):
            output = data_service.get_step_output(project["id"], step_to_export)
            if output:
                filepath = export_step_output(project["name"], step_to_export, output)
                st.success(f"Exported to: {filepath}")
            else:
                st.warning("No output for this step.")


def _render_step(step_num, project, data_service, gemini_service,
                 claude_service, youtube_service, completed_steps):
    """Render a single workflow step."""
    step_name = STEPS[step_num]
    api = STEP_API[step_num]
    is_completed = step_num in completed_steps

    # Status indicator
    status = "Completed" if is_completed else "Pending"
    st.markdown(f"**Step {step_num}: {step_name}** - _{status}_")

    # Check prerequisites
    if step_num > 1 and (step_num - 1) not in completed_steps:
        # Allow running step 3 without step 2 if needed, but generally enforce order
        if step_num not in [3]:  # Step 3 can run with just step 1
            st.warning(f"Complete Step {step_num - 1} first.")

    # Show existing output
    existing_output = data_service.get_step_output(project["id"], step_num)
    if existing_output:
        with st.expander("View Output", expanded=False):
            st.text(existing_output[:5000])
            if len(existing_output) > 5000:
                st.caption(f"... (truncated, {len(existing_output)} chars total)")

        # Validation
        validation = StepValidator.validate_step_output(step_num, existing_output)
        st.caption(f"Quality: {validation['message']}")

    # Step-specific inputs and run button
    if step_num == 8:
        _render_step8(project, data_service, claude_service, gemini_service, completed_steps)
    else:
        _render_generic_step(step_num, project, data_service, gemini_service,
                             youtube_service, completed_steps, existing_output)


def _render_generic_step(step_num, project, data_service, gemini_service,
                         youtube_service, completed_steps, existing_output):
    """Render a Gemini-powered step."""
    # Step-specific inputs
    user_angle = ""
    target_length = "Medium (10-15 min)"

    if step_num == 2:
        step1_output = data_service.get_step_output(project["id"], 1) or ""
        default_angle = OutputExtractor.extract_recommended_angle(step1_output)
        user_angle = st.text_input(
            "Selected Angle (from Step 1 or your own)",
            value=default_angle,
            key=f"angle_step2_{project['id']}",
        )

    if step_num == 5:
        target_length = st.selectbox(
            "Target Video Length",
            list(VIDEO_LENGTHS.keys()),
            key=f"length_step5_{project['id']}",
        )

    # Run button
    button_label = "Re-run Step" if existing_output else "Run Step"
    if st.button(button_label, key=f"run_step_{step_num}_{project['id']}", type="primary"):
        if not gemini_service.is_configured():
            st.error("Gemini API key not configured. Go to Settings.")
            return

        with st.spinner(f"Running Step {step_num}..."):
            try:
                prompt = _build_step_prompt(
                    step_num, project, data_service, youtube_service,
                    user_angle=user_angle, target_length=target_length,
                )
                response, tokens = gemini_service.generate(prompt)

                data_service.save_step_output(
                    project["id"], step_num, STEPS[step_num],
                    prompt[:500], response, gemini_tokens=tokens,
                )
                st.success(f"Step {step_num} complete! ({tokens} tokens)")
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")


def _render_step8(project, data_service, claude_service, gemini_service, completed_steps):
    """Render Step 8 - Script Writing with Claude."""
    # Always fetch fresh
    existing_step8 = data_service.get_step_output(project["id"], 8)

    # Script length selection
    script_length_option = st.selectbox(
        "Script Length",
        list(SCRIPT_LENGTHS.keys()),
        key=f"script_length_{project['id']}",
    )

    word_range = SCRIPT_LENGTHS.get(script_length_option)
    if word_range is None:
        col1, col2 = st.columns(2)
        with col1:
            min_words = st.number_input("Min Words", value=1500, min_value=200, key=f"min_words_{project['id']}")
        with col2:
            max_words = st.number_input("Max Words", value=2000, min_value=300, key=f"max_words_{project['id']}")
        word_range = (min_words, max_words)

    # Script style selection
    script_style = st.selectbox(
        "Script Style",
        SCRIPT_STYLES,
        key=f"script_style_{project['id']}",
    )
    st.caption(f"Style: {script_style} - Each style produces a unique voice and structure.")

    # Show existing output
    if existing_step8:
        with st.expander("View Current Script", expanded=False):
            st.text(existing_step8[:5000])
            word_count = len(existing_step8.split())
            st.caption(f"Word count: {word_count}")

        validation = StepValidator.validate_step_output(8, existing_step8)
        st.caption(f"Quality: {validation['message']}")

    # Run button
    button_label = "Re-write Script" if existing_step8 else "Write Script"
    if st.button(button_label, key=f"run_step_8_{project['id']}", type="primary"):
        if not claude_service.is_configured():
            st.error("Claude API key not configured. Go to Settings.")
            return

        # Check prerequisites
        required_steps = [1, 2, 4, 5, 6, 7]
        missing = [s for s in required_steps if s not in completed_steps]
        if missing:
            st.warning(f"Recommended: Complete steps {missing} first for best results.")

        with st.spinner("Claude is writing your script..."):
            try:
                previous_outputs = data_service.get_all_step_outputs(project["id"])

                user_inputs = {
                    "topic": project["topic"],
                    "script_length": script_length_option,
                    "script_style": script_style,
                    "word_range": word_range,
                }

                prompt = get_step8_prompt(user_inputs, previous_outputs)
                system_prompt = get_step8_system_prompt(script_style)

                response, tokens = claude_service.generate(
                    prompt, system_prompt=system_prompt,
                    temperature=0.8, max_tokens=8192,
                )

                data_service.save_step_output(
                    project["id"], 8, STEPS[8],
                    f"Style: {script_style}, Length: {script_length_option}",
                    response, claude_tokens=tokens,
                )
                st.success(f"Script written! ({tokens} tokens, {len(response.split())} words)")
                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")


def _build_step_prompt(step_num, project, data_service, youtube_service,
                       user_angle="", target_length="Medium (10-15 min)"):
    """Build the prompt for a given step."""
    topic = project["topic"]
    audience = project.get("target_audience", "")

    # Fetch YouTube data for steps that need it
    youtube_data = ""
    if step_num in [1, 3] and youtube_service.is_configured():
        try:
            videos = youtube_service.search_videos(topic)
            youtube_data = youtube_service.format_for_analysis(videos)
        except Exception:
            youtube_data = ""

    # Get previous step outputs
    get_output = lambda s: data_service.get_step_output(project["id"], s) or ""

    if step_num == 1:
        return get_step1_prompt(topic, audience, youtube_data)
    elif step_num == 2:
        return get_step2_prompt(topic, user_angle, get_output(1))
    elif step_num == 3:
        return get_step3_prompt(topic, youtube_data, get_output(1))
    elif step_num == 4:
        return get_step4_prompt(topic, get_output(1), get_output(2), get_output(3))
    elif step_num == 5:
        return get_step5_prompt(topic, target_length, get_output(1), get_output(2), get_output(4))
    elif step_num == 6:
        return get_step6_prompt(get_output(2), get_output(5))
    elif step_num == 7:
        return get_step7_prompt(topic, get_output(1), get_output(5))
    elif step_num == 9:
        return get_step9_prompt(get_output(2), get_output(7), get_output(8))
    elif step_num == 10:
        return get_step10_prompt(topic, get_output(4), get_output(2), get_output(8), get_output(3))
    else:
        return f"Analyze the topic: {topic}"
