"""
Video Annotation System
A Streamlit application for annotating videos with multiple-choice questions
Version: 2.0.0 - Human verification with OneDrive folder links
"""

import streamlit as st
import json
import time
from datetime import datetime
from pathlib import Path

# Import utility modules
from utils.data_parser import load_questions, parse_questions_data
from utils.video_loader_onedrive_folder import VideoLoaderOneDriveFolder as VideoLoader
from utils.session_manager import initialize_session, save_progress, load_progress
from utils.response_recorder import save_response, export_responses
import config

# Page configuration
st.set_page_config(
    page_title="Video Annotation System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .choice-box {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
        border: 2px solid #e0e0e0;
    }
    .correct-answer {
        background-color: #d4edda;
        border-color: #28a745;
    }
    .video-container {
        margin: 1rem 0;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .annotation-guide {
        background-color: #eef6ff;
        border-left: 4px solid #2563eb;
        padding: 0.75rem 1rem;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
    }
    .right-panel p, .right-panel li, .right-panel label, .right-panel .stMarkdown {
        font-size: 1.15rem;
    }
    .right-panel h3 {
        font-size: 1.45rem;
    }
    .option-item {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.6rem 0.75rem;
        margin: 0.35rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session()

    # Load progress if exists
    if 'initialized' not in st.session_state:
        progress_data = load_progress()
        if progress_data:
            if st.sidebar.button("Resume Previous Session"):
                st.session_state.current_index = progress_data.get('current_index', 0)
                st.session_state.responses = progress_data.get('responses', [])
                st.rerun()
        st.session_state.initialized = True

    # Sidebar
    with st.sidebar:
        st.title("Video Annotation")
        st.markdown("---")

        # Data source selector
        default_data_path = st.session_state.get('data_file_path', str(config.DATA_FILE))
        data_file_path = st.text_input(
            "Annotation JSON path",
            value=default_data_path,
            help="Path to a local annotation JSON file."
        ).strip()
        st.session_state.data_file_path = data_file_path

        uploaded_json = st.file_uploader(
            "Or upload updated annotation JSON",
            type=['json'],
            accept_multiple_files=False
        )

        if uploaded_json is not None:
            try:
                uploaded_data = json.load(uploaded_json)
                questions = parse_questions_data(uploaded_data)
                current_source_key = f"upload::{uploaded_json.name}::{uploaded_json.size}"
                source_caption = f"Loaded from upload: {uploaded_json.name}"
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse uploaded JSON: {e}")
                questions = []
                current_source_key = "upload::invalid"
                source_caption = "Upload parse failed"
        else:
            questions = load_questions(data_file_path)
            current_source_key = f"path::{data_file_path}"
            source_caption = f"Loaded from path: {data_file_path}"

        st.caption(source_caption)

        # Reset position when dataset source changes
        if st.session_state.get('questions_source_key') != current_source_key:
            st.session_state.questions_source_key = current_source_key
            st.session_state.current_index = 0
            st.session_state.responses = []
            st.session_state.question_start_time = time.time()

        total_questions = len(questions)

        # Progress info
        st.metric("Total Questions", total_questions)
        st.metric("Current Question", st.session_state.current_index + 1)
        st.metric("Completed", len(st.session_state.responses))
        st.metric("Remaining", total_questions - st.session_state.current_index)

        # Progress bar
        progress = st.session_state.current_index / total_questions if total_questions > 0 else 0
        st.progress(progress)
        st.caption(f"Progress: {progress*100:.1f}%")

        st.markdown("---")

        # User ID input
        if 'user_id' not in st.session_state or not st.session_state.user_id:
            st.session_state.user_id = st.text_input(
                "Enter your Annotator ID:",
                value="annotator_001",
                key="user_id_input"
            )
        else:
            st.info(f"Annotator: {st.session_state.user_id}")

        st.markdown("---")

        # Navigation
        st.subheader("Navigation")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous", disabled=st.session_state.current_index == 0):
                st.session_state.current_index -= 1
                st.session_state.question_start_time = time.time()
                st.rerun()
        with col2:
            if st.button("Skip", disabled=st.session_state.current_index >= total_questions - 1):
                st.session_state.current_index += 1
                st.session_state.question_start_time = time.time()
                st.rerun()

        # Jump to question
        jump_to = st.number_input(
            "Jump to question:",
            min_value=1,
            max_value=total_questions,
            value=st.session_state.current_index + 1,
            key="jump_input"
        )
        if st.button("Go"):
            st.session_state.current_index = jump_to - 1
            st.session_state.question_start_time = time.time()
            st.rerun()

        st.markdown("---")

        # Save and export
        if st.button("💾 Save Progress"):
            save_progress(st.session_state.current_index, st.session_state.responses)
            st.success("Progress saved!")

        if st.button("📥 Export Responses"):
            export_file = export_responses(st.session_state.responses)
            st.success(f"Exported to {export_file}")

    # Main content
    if st.session_state.current_index >= total_questions:
        st.balloons()
        st.success("🎉 You have completed all questions!")
        st.metric("Total Time Spent", f"{sum([r.get('time_spent_seconds', 0) for r in st.session_state.responses]):.0f} seconds")
        st.metric("Accuracy", f"{sum([1 for r in st.session_state.responses if r.get('is_correct', False)]) / len(st.session_state.responses) * 100:.1f}%" if st.session_state.responses else "N/A")

        if st.button("🔄 Start Over"):
            st.session_state.current_index = 0
            st.session_state.responses = []
            st.session_state.question_start_time = time.time()
            st.rerun()
        return

    # Get current question
    current_question = questions[st.session_state.current_index]

    # Header
    st.markdown(f"<div class='main-header'>Question {st.session_state.current_index + 1} of {total_questions}</div>", unsafe_allow_html=True)

    # Video loader with OneDrive folder
    onedrive_url = getattr(config, 'ONEDRIVE_VIDEO_FOLDER',
                           "https://adminliveunc-my.sharepoint.com/:f:/g/personal/ziyangw_ad_unc_edu/IgA_aigeKcG-QKDy08QVHEiEARIVaWMqy6UH-1eFP7TijWA?e=aNCstX")
    video_loader = VideoLoader(folder_url=onedrive_url)

    # Layout: Video on left, Question and choices on right
    col_left, col_right = st.columns([2.2, 2.8])

    with col_left:
        st.subheader("🎬 Video Evidence")

        # Main query video
        query_time = current_question.get('query_time', '')
        if query_time:
            st.markdown(f"**Query Context Video:** `{query_time}`")
            video_loader.display_video_iframe(query_time)

        # Evidence videos
        evidence_times = current_question.get('evidence_times', [])
        if evidence_times:
            st.markdown("**Evidence Clips:**")

            for idx, evidence in enumerate(evidence_times):
                clip_id = evidence.get('clip_id', '')
                with st.expander(f"📹 Evidence {idx + 1}: {clip_id}", expanded=False):
                    video_loader.display_video_iframe(clip_id)

                    # Show object snapshot info
                    obj_snapshot = evidence.get('object_snapshot', {})
                    if obj_snapshot:
                        st.caption(f"**Object:** {obj_snapshot.get('object_name', 'N/A')}")
                        st.caption(f"**Location:** {obj_snapshot.get('location', 'N/A')}")
                        st.caption(f"**Status:** {', '.join(obj_snapshot.get('status', []))}")

                    # Dense caption
                    captions = evidence.get('dense_caption_context', [])
                    if captions:
                        st.caption(f"**Context:** {captions[0]}")

        # Choice support videos
        st.markdown("**Choice Support Videos:**")
        choices = current_question.get('choices', [])
        for choice in choices:
            label = choice.get('label', '')
            support_clip = choice.get('support_clip_id', '')
            if support_clip:
                with st.expander(f"Choice {label}: {support_clip}", expanded=False):
                    video_loader.display_video_iframe(support_clip)

    with col_right:
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        # Question
        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        st.markdown("### Question")
        st.markdown(f"**{current_question.get('query', 'No question text')}**")
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("📘 Annotation Guidelines", expanded=True):
            st.markdown("<div class='annotation-guide'>", unsafe_allow_html=True)
            st.markdown(
                "1. Watch query context video and at least one relevant support clip.\n"
                "2. Select the best answer based on visual evidence, not metadata.\n"
                "3. Rate query quality. If unclear or awkward, revise it in the box below.\n"
                "4. Mark option-set issues if distractors are weak, duplicated, or ambiguous.\n"
                "5. Use overall decision to indicate whether this MCQ can be kept as-is."
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Additional info
        with st.expander("Additional Information"):
            st.caption(f"**Sample ID:** {current_question.get('sample_id', 'N/A')}")
            st.caption(f"**Object:** {current_question.get('object_name', 'N/A')}")
            st.caption(f"**Query Type:** {current_question.get('query_type', 'N/A')}")
            st.caption(f"**Difficulty:** {current_question.get('difficulty_tier', 'N/A')} ({current_question.get('difficulty_score', 0):.2f})")

        # Choices
        st.markdown("### 📝 Options and Ground Truth")
        correct_answer = current_question.get('correct_choice', '')
        gt_text = ""
        for choice in choices:
            label = choice.get('label', '')
            text = choice.get('text', '')
            is_gt = (label == correct_answer)
            if is_gt:
                gt_text = text
            suffix = " ✅ Ground Truth" if is_gt else ""
            st.markdown(
                f"<div class='option-item'><b>{label}.</b> {text}{suffix}</div>",
                unsafe_allow_html=True
            )

        if correct_answer:
            st.info(f"Ground-truth label: {correct_answer}")
        if gt_text:
            st.caption(f"Ground-truth text: {gt_text}")

        st.markdown("### ✅ Human Verification")

        query_quality = st.radio(
            "Query quality",
            [
                "Good query (clear and answerable)",
                "Needs minor revision (wording/style)",
                "Needs major revision (logic/temporal ambiguity)",
                "Bad query (not answerable or invalid)",
            ],
            key=f"query_quality_{st.session_state.current_index}"
        )

        query_action = st.radio(
            "Query action",
            [
                "Keep original query",
                "Revise query text",
                "Reject this sample",
            ],
            key=f"query_action_{st.session_state.current_index}"
        )

        revised_query = st.text_area(
            "Updated query text (edit when needed)",
            value=current_question.get('query', ''),
            height=120,
            key=f"revised_query_{st.session_state.current_index}"
        )

        generated_answer_check = st.radio(
            "Generated correct choice quality",
            [
                "Correct",
                "Incorrect",
                "Unsure",
            ],
            horizontal=True,
            key=f"answer_quality_{st.session_state.current_index}"
        )

        options_quality = st.radio(
            "Options quality",
            [
                "Good options",
                "Usable but needs edits",
                "Bad options (regenerate)",
            ],
            horizontal=True,
            key=f"options_quality_{st.session_state.current_index}"
        )

        observed_issues = st.multiselect(
            "Observed issues",
            [
                "Ambiguous query",
                "Temporal inconsistency",
                "Multiple plausible correct options",
                "No correct option",
                "Distractors too easy",
                "Distractors unrealistic",
                "Option wording unclear",
                "Other",
            ],
            key=f"issues_{st.session_state.current_index}"
        )

        overall_decision = st.radio(
            "Overall decision",
            [
                "Accept",
                "Revise",
                "Reject",
            ],
            horizontal=True,
            key=f"overall_{st.session_state.current_index}"
        )

        verification_notes = st.text_area(
            "Verification notes",
            value="",
            height=90,
            key=f"notes_{st.session_state.current_index}"
        )

        st.markdown("---")

        # Submit button
        col_submit, col_skip = st.columns(2)
        with col_submit:
            if st.button("Submit Verification", type="primary", use_container_width=True):
                if query_action == "Revise query text" and not revised_query.strip():
                    st.warning("Please provide revised query text or choose another query action.")
                    st.stop()

                # Calculate time spent
                time_spent = time.time() - st.session_state.question_start_time

                # Save response
                response = {
                    'sample_id': current_question.get('sample_id', ''),
                    'user_answer': None,
                    'correct_answer': correct_answer,
                    'is_correct': None,
                    'time_spent_seconds': round(time_spent, 2),
                    'timestamp': datetime.now().isoformat(),
                    'user_id': st.session_state.user_id,
                    'human_verification': {
                        'query_quality': query_quality,
                        'query_action': query_action,
                        'original_query': current_question.get('query', ''),
                        'revised_query': revised_query.strip(),
                        'generated_answer_check': generated_answer_check,
                        'options_quality': options_quality,
                        'observed_issues': observed_issues,
                        'overall_decision': overall_decision,
                        'notes': verification_notes.strip(),
                        'ground_truth_label': correct_answer,
                        'ground_truth_text': gt_text
                    }
                }

                save_response(response)
                st.session_state.responses.append(response)
                st.success("Verification saved.")
                st.info(f"Time spent: {time_spent:.1f} seconds")

                # Auto-advance after 2 seconds
                time.sleep(2)
                st.session_state.current_index += 1
                st.session_state.question_start_time = time.time()
                save_progress(st.session_state.current_index, st.session_state.responses)
                st.rerun()

        with col_skip:
            if st.button("Skip Question", use_container_width=True):
                st.session_state.current_index += 1
                st.session_state.question_start_time = time.time()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
