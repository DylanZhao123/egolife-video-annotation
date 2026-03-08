import json
import os
import time
from typing import Any, Dict, List, Optional

import streamlit as st


PAGE_TITLE = "EgoLife MCQ Verification Annotation"
LAYOUT = "wide"

DEFAULT_INPUT = (
    "/nas-ssd2/ziyang/Memory_project/openai/egolife/gpt5_caption/results/"
    "object_caption/tale_sofa_extract/"
    "A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json"
)
DEFAULT_VIDEO_ROOT = "/nas-ssd2/video_datasets/EgoLife"
DEFAULT_OUTPUT = "./annotations_mcq_verification.jsonl"


@st.cache_data(show_spinner=False)
def load_json_tasks(input_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(input_path):
        return []
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        st.error(f"Failed to load input JSON: {exc}")
        return []

    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "samples", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return []


def get_processed_count(output_path: str) -> int:
    if not os.path.exists(output_path):
        return 0
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    except Exception:
        return 0


def normalize_choices(entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw_choices = entry.get("choices", [])
    if not isinstance(raw_choices, list):
        return []

    choices: List[Dict[str, Any]] = []
    for idx, choice in enumerate(raw_choices):
        fallback_label = chr(ord("A") + idx)
        if isinstance(choice, dict):
            label = str(choice.get("label", fallback_label)).strip().upper()
            text = str(choice.get("text", "")).strip()
            support_clip_id = choice.get("support_clip_id")
            support_frame_path = choice.get("support_frame_path")
        else:
            label = fallback_label
            text = str(choice).strip()
            support_clip_id = None
            support_frame_path = None
        choices.append(
            {
                "label": label,
                "text": text,
                "support_clip_id": support_clip_id,
                "support_frame_path": support_frame_path,
            }
        )
    return choices


def resolve_clip_path(clip_id: Optional[str], video_root: str) -> Optional[str]:
    if not clip_id:
        return None
    clip_id = str(clip_id).strip()
    if not clip_id:
        return None

    parts = clip_id.split("_")
    if len(parts) < 3:
        return None

    day = parts[0]
    identity = "_".join(parts[1:3])
    candidate_paths = [
        os.path.join(video_root, identity, day, f"{clip_id}.mp4"),
        os.path.join(video_root, identity, day, f"{clip_id}.MP4"),
    ]

    for path in candidate_paths:
        if os.path.exists(path):
            return path
    return None


def render_video_with_meta(video_path: Optional[str], clip_id: Optional[str], title: str) -> None:
    st.markdown(f"**{title}**")
    st.caption(f"clip_id: {clip_id if clip_id else '(none)'}")
    if video_path and os.path.exists(video_path):
        st.video(video_path)
        st.caption(video_path)
    else:
        st.warning("Video not found.")


def render_frame(frame_path: Optional[str], title: str) -> None:
    if not frame_path:
        return
    st.markdown(f"**{title}**")
    if os.path.exists(frame_path):
        st.image(frame_path)
        st.caption(frame_path)
    else:
        st.warning(f"Frame not found: {frame_path}")


def save_annotation(
    output_path: str,
    source_entry: Dict[str, Any],
    payload: Dict[str, Any],
    duration_seconds: float,
) -> None:
    result = source_entry.copy()
    result["human_verification"] = payload
    result["annotation_time_seconds"] = round(duration_seconds, 2)
    result["annotated_at"] = time.time()

    with open(output_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)
    st.title(PAGE_TITLE)

    st.sidebar.title("Config")
    input_file = st.sidebar.text_input("Input JSON", value=DEFAULT_INPUT).strip()
    video_root = st.sidebar.text_input("Video Root", value=DEFAULT_VIDEO_ROOT).strip()
    output_file = st.sidebar.text_input("Output JSONL", value=DEFAULT_OUTPUT).strip()

    if not os.path.exists(input_file):
        st.warning(f"Input file not found: {input_file}")
        st.stop()

    if "loaded_input_file" not in st.session_state or st.session_state.loaded_input_file != input_file:
        st.session_state.loaded_input_file = input_file
        st.session_state.all_tasks = load_json_tasks(input_file)

    tasks = st.session_state.get("all_tasks", [])
    if not tasks:
        st.warning("No tasks loaded from input JSON.")
        st.stop()

    processed_count = get_processed_count(output_file)
    current_idx = processed_count

    if current_idx >= len(tasks):
        st.success("All tasks completed.")
        st.stop()

    task_key = f"{input_file}::{current_idx}"
    if "current_task_key" not in st.session_state or st.session_state.current_task_key != task_key:
        st.session_state.current_task_key = task_key
        st.session_state.task_start_time = time.time()

    st.sidebar.progress(current_idx / len(tasks))
    st.sidebar.markdown(f"Task: {current_idx + 1} / {len(tasks)}")
    st.sidebar.markdown(f"Processed (from output lines): {processed_count}")

    entry = tasks[current_idx]
    choices = normalize_choices(entry)
    label_to_choice = {c["label"]: c for c in choices}
    labels = [c["label"] for c in choices]

    provided_correct = str(entry.get("correct_choice", "")).strip().upper()
    if provided_correct not in label_to_choice and labels:
        provided_correct = labels[0]

    query_clip_id = entry.get("query_time")
    query_video_path = resolve_clip_path(query_clip_id, video_root)

    answer_clip_id = entry.get("answer_support_clip_id") or entry.get("support_clip_id")
    answer_video_path = resolve_clip_path(answer_clip_id, video_root)
    answer_frame_path = entry.get("answer_support_frame_path")

    st.markdown(
        f"**sample_id:** `{entry.get('sample_id', '(missing)')}` | "
        f"**combined_sample_id:** `{entry.get('combined_sample_id', '(missing)')}`"
    )

    left_col, right_col = st.columns([1.2, 1.2])

    with left_col:
        st.subheader("Evidence")
        tab_query, tab_answer, tab_choice = st.tabs(
            ["Query-Time Clip", "Answer Evidence", "Choice Evidence"]
        )

        with tab_query:
            render_video_with_meta(query_video_path, query_clip_id, "Query-time clip")

        with tab_answer:
            render_video_with_meta(answer_video_path, answer_clip_id, "Answer-support clip")
            render_frame(answer_frame_path, "Answer-support frame")

        with tab_choice:
            if not choices:
                st.warning("No choices found in this sample.")
            else:
                selected_label = st.selectbox(
                    "Preview option evidence",
                    labels,
                    format_func=lambda x: f"{x}: {label_to_choice[x]['text']}",
                )
                selected_choice = label_to_choice[selected_label]
                choice_clip_id = selected_choice.get("support_clip_id")
                choice_video_path = resolve_clip_path(choice_clip_id, video_root)
                render_video_with_meta(choice_video_path, choice_clip_id, "Option support clip")
                render_frame(selected_choice.get("support_frame_path"), "Option support frame")

    with right_col:
        st.subheader("MCQ and Annotation")
        st.markdown(f"**Object:** `{entry.get('object_name', '')}`")
        st.markdown(f"**Query Type:** `{entry.get('query_type', '')}`")
        st.markdown(f"**Difficulty:** `{entry.get('difficulty_tier', '')}`")
        st.markdown("**Query**")
        st.info(str(entry.get("query", "")))

        st.markdown("**Options**")
        for choice in choices:
            is_provided = choice["label"] == provided_correct
            suffix = " (provided correct)" if is_provided else ""
            st.markdown(f"- **{choice['label']}**: {choice['text']}{suffix}")

        if not choices:
            st.error("This sample has no options. It cannot be annotated with this UI.")
            st.stop()

        with st.form(f"annotation_form_{current_idx}"):
            query_clear = st.radio(
                "1) Is the query clear and answerable from evidence?",
                ["Yes", "Partly", "No"],
                horizontal=True,
            )

            annotator_choice = st.radio(
                "2) Which option is correct?",
                labels,
                format_func=lambda x: f"{x}: {label_to_choice[x]['text']}",
            )

            single_correct = st.radio(
                "3) Is there exactly one unambiguously correct option?",
                ["Yes", "No", "Unsure"],
                horizontal=True,
            )

            distractor_quality = st.radio(
                "4) Distractor quality",
                ["Good", "Mixed", "Poor"],
                horizontal=True,
            )

            option_issues = st.multiselect(
                "5) Option issues (if any)",
                [
                    "More than one correct option",
                    "No correct option",
                    "Distractors too easy",
                    "Distractors implausible",
                    "Temporal mismatch",
                    "Wording ambiguity",
                    "Duplicate or near-duplicate options",
                    "Other",
                ],
            )

            overall = st.radio(
                "6) Overall generated MCQ quality",
                ["Accept", "Needs revision", "Reject"],
                horizontal=True,
            )

            notes = st.text_area("Notes", value="")
            submitted = st.form_submit_button("Submit and Next", type="primary")

        if submitted:
            provided_text = label_to_choice.get(provided_correct, {}).get("text", "")
            annotator_text = label_to_choice.get(annotator_choice, {}).get("text", "")
            payload = {
                "query_clear": query_clear,
                "annotator_choice": annotator_choice,
                "annotator_choice_text": annotator_text,
                "provided_correct_choice": provided_correct,
                "provided_correct_text": provided_text,
                "provided_choice_is_correct": annotator_choice == provided_correct,
                "single_correct_option": single_correct,
                "distractor_quality": distractor_quality,
                "option_issues": option_issues,
                "overall_quality": overall,
                "notes": notes.strip(),
            }
            save_annotation(
                output_file,
                entry,
                payload,
                time.time() - st.session_state.task_start_time,
            )
            st.rerun()


if __name__ == "__main__":
    main()
