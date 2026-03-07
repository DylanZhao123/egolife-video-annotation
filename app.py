"""
Video Annotation System
A Streamlit application for annotating videos with multiple-choice questions
"""

import streamlit as st
import json
import time
from datetime import datetime
from pathlib import Path

# Import utility modules
from utils.data_parser import load_questions, format_choice_text
from utils.video_loader_external_links import VideoLoaderExternalLinks as VideoLoader
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

        # Load questions
        questions = load_questions(config.DATA_FILE)
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

    # Layout: Video on left, Question and choices on right
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("🎬 Video Evidence")

        # Video loader
        video_loader = VideoLoader()

        # Main query video (if different from evidence)
        query_time = current_question.get('query_time', '')
        if query_time:
            st.markdown("**Query Context Video:**")
            video_loader.display_video_link(query_time)

        # Evidence videos
        evidence_times = current_question.get('evidence_times', [])
        if evidence_times:
            st.markdown("**Evidence Clips:**")

            for idx, evidence in enumerate(evidence_times):
                clip_id = evidence.get('clip_id', '')
                with st.expander(f"📹 Evidence {idx + 1}", expanded=(idx == 0)):
                    video_loader.display_video_link(clip_id)

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

    with col_right:
        # Question
        st.markdown("<div class='question-box'>", unsafe_allow_html=True)
        st.markdown("### Question")
        st.markdown(f"**{current_question.get('query', 'No question text')}**")
        st.markdown("</div>", unsafe_allow_html=True)

        # Additional info
        with st.expander("Additional Information"):
            st.caption(f"**Sample ID:** {current_question.get('sample_id', 'N/A')}")
            st.caption(f"**Object:** {current_question.get('object_name', 'N/A')}")
            st.caption(f"**Query Type:** {current_question.get('query_type', 'N/A')}")
            st.caption(f"**Difficulty:** {current_question.get('difficulty_tier', 'N/A')} ({current_question.get('difficulty_score', 0):.2f})")

        # Choices
        st.markdown("### 📝 Select Your Answer")

        choices = current_question.get('choices', [])
        choice_labels = [choice['label'] for choice in choices]

        # Radio buttons for choices
        selected_choice = st.radio(
            "Options:",
            options=choice_labels,
            format_func=lambda x: format_choice_text(current_question, x),
            key=f"choice_{st.session_state.current_index}"
        )

        # Show support videos for choices
        if selected_choice:
            selected_choice_data = next((c for c in choices if c['label'] == selected_choice), None)
            if selected_choice_data:
                support_clip = selected_choice_data.get('support_clip_id')
                if support_clip:
                    with st.expander(f"🎥 View Support Video for Choice {selected_choice}"):
                        support_url = video_loader.get_video_link(support_clip)
                        if support_url:
                            st.video(support_url)
                        else:
                            st.info(f"Support video not configured: {support_clip}")

        st.markdown("---")

        # Submit button
        col_submit, col_skip = st.columns(2)
        with col_submit:
            if st.button("Submit Answer", type="primary", use_container_width=True):
                if selected_choice:
                    # Calculate time spent
                    time_spent = time.time() - st.session_state.question_start_time

                    # Check if correct
                    correct_answer = current_question.get('correct_choice', '')
                    is_correct = (selected_choice == correct_answer)

                    # Save response
                    response = {
                        'sample_id': current_question.get('sample_id', ''),
                        'user_answer': selected_choice,
                        'correct_answer': correct_answer,
                        'is_correct': is_correct,
                        'time_spent_seconds': round(time_spent, 2),
                        'timestamp': datetime.now().isoformat(),
                        'user_id': st.session_state.user_id
                    }

                    save_response(response)
                    st.session_state.responses.append(response)

                    # Show feedback
                    if is_correct:
                        st.success(f"Correct! The answer is {correct_answer}")
                    else:
                        st.error(f"Incorrect. The correct answer is {correct_answer}")

                    st.info(f"Time spent: {time_spent:.1f} seconds")

                    # Auto-advance after 2 seconds
                    time.sleep(2)
                    st.session_state.current_index += 1
                    st.session_state.question_start_time = time.time()
                    save_progress(st.session_state.current_index, st.session_state.responses)
                    st.rerun()
                else:
                    st.warning("Please select an answer before submitting.")

        with col_skip:
            if st.button("Skip Question", use_container_width=True):
                st.session_state.current_index += 1
                st.session_state.question_start_time = time.time()
                st.rerun()

if __name__ == "__main__":
    main()
