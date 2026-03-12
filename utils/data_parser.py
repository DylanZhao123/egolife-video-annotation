"""
Data Parser Module
Handles loading and parsing question data from JSON files
"""

import json
from pathlib import Path

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

def _extract_clip_id_from_frame_path(frame_path):
    """Extract clip ID from a frame path like .../DAY6_A1_JAKE_20503000/frame_0030.jpg."""
    if not frame_path:
        return None
    try:
        parent = Path(frame_path).parent.name
        return parent if parent else None
    except Exception:
        return None

def _normalize_hard_videoqa_item(item):
    """
    Normalize hierarchical_cap hard_videoqa_examples format into app schema.
    """
    options = item.get('options', []) or []
    choices = []
    for idx, opt in enumerate(options):
        if isinstance(opt, dict):
            label = str(opt.get('option', chr(ord('A') + idx))).strip().upper()
            text = str(opt.get('text', '')).strip()
            support_clip_id = _extract_clip_id_from_frame_path(opt.get('support_frame_path'))
            choices.append({
                'label': label,
                'text': text,
                'support_clip_id': support_clip_id,
                'event_id': opt.get('event_id')
            })
        else:
            label = chr(ord('A') + idx)
            choices.append({'label': label, 'text': str(opt), 'support_clip_id': None})

    query_frame_path = item.get('query_frame_path')
    query_clip_id = _extract_clip_id_from_frame_path(query_frame_path) or item.get('query_time')

    supporting_paths = item.get('supporting_evidence_frame_paths', []) or []
    evidence_times = []
    for fp in supporting_paths:
        clip_id = _extract_clip_id_from_frame_path(fp)
        if clip_id:
            evidence_times.append({
                'clip_id': clip_id,
                'dense_caption_context': [],
                'frame_path': fp
            })

    answer_label = str(item.get('answer', '')).strip().upper()
    answer_support_clip_id = None
    if evidence_times:
        answer_support_clip_id = evidence_times[0].get('clip_id')

    return {
        'sample_id': item.get('qa_id', ''),
        'query': item.get('question', ''),
        'choices': choices,
        'correct_choice': answer_label,
        'query_time': query_clip_id,
        'query_frame_path': query_frame_path,
        'answer_support_clip_id': answer_support_clip_id,
        'evidence_times': evidence_times,
        'difficulty_tier': item.get('difficulty', 'unknown'),
        'difficulty_score': item.get('difficulty_score', 0),
        'query_type': item.get('type', 'event_retrieval_mcq'),
        'reasoning_detailed': item.get('reasoning_detailed', {}),
        'constraints_satisfied': item.get('constraints_satisfied', {}),
        'raw_query_time': item.get('query_time', '')
    }

def _parse_day_time_to_clip_id(raw_time, identity):
    """
    Convert strings like 'Day1_20:46:30' or 'Day 6 19:16' to clip IDs:
      DAY1_A1_JAKE_20463000
    Returns None on parse failure.
    """
    if not raw_time or not identity:
        return None

    s = str(raw_time).strip()
    # Match: Day1_20:46:30 or Day 1 20:46:30 or Day 1 20:46
    import re
    m = re.search(r'Day\s*([0-9]+)[ _-]*([0-9]{1,2}):([0-9]{2})(?::([0-9]{2}))?', s, flags=re.IGNORECASE)
    if not m:
        return None

    day = int(m.group(1))
    hh = int(m.group(2))
    mm = int(m.group(3))
    ss = int(m.group(4)) if m.group(4) is not None else 0
    identity = str(identity).strip().upper()
    return f"DAY{day}_{identity}_{hh:02d}{mm:02d}{ss:02d}00"

def _normalize_rigorous_filtered_query_item(item):
    """
    Normalize rigorous verification filtered queries format into app schema.
    """
    options = item.get('options', []) or []
    choices = []
    for idx, opt in enumerate(options):
        label = chr(ord('A') + idx)
        choices.append({
            'label': label,
            'text': str(opt),
            'support_clip_id': None
        })

    answer_index = item.get('answer_index')
    correct_choice = ''
    if isinstance(answer_index, int) and 0 <= answer_index < len(choices):
        correct_choice = choices[answer_index]['label']

    identity = item.get('identity', '')
    raw_query_time = item.get('query_time', '')
    query_clip_id = _parse_day_time_to_clip_id(raw_query_time, identity)

    entity = item.get('entity')
    if isinstance(entity, dict):
        object_name = entity.get('canonical_object', '')
    else:
        object_name = str(entity) if entity is not None else ''

    return {
        'sample_id': item.get('query_id', ''),
        'query': item.get('question', ''),
        'choices': choices,
        'correct_choice': correct_choice,
        'query_time': query_clip_id or raw_query_time,
        'raw_query_time': raw_query_time,
        'answer_support_clip_id': None,
        'evidence_times': [],
        'difficulty_tier': item.get('difficulty', 'unknown'),
        'difficulty_score': item.get('difficulty_score', 0),
        'query_type': item.get('task_type', 'rigorous_query'),
        'object_name': object_name,
        'identity': identity,
        'answer_text': item.get('answer_text', ''),
        'reasoning': item.get('reasoning', ''),
        'evidence_clip_uids': item.get('evidence_clip_uids', [])
    }

def normalize_question_item(item):
    """
    Normalize multiple possible schemas into one app-friendly schema.
    """
    if not isinstance(item, dict):
        return {'sample_id': '', 'query': str(item), 'choices': [], 'correct_choice': ''}

    # Already in current app schema
    if 'choices' in item and 'query' in item:
        return item

    # New hard_videoqa_examples schema
    if 'question' in item and 'options' in item and 'answer' in item:
        return _normalize_hard_videoqa_item(item)

    # Rigorous verification filtered query schema
    if 'question' in item and 'options' in item and 'answer_index' in item:
        return _normalize_rigorous_filtered_query_item(item)

    return item

def parse_questions_data(data):
    """
    Parse and normalize loaded JSON object into a list of question dicts.
    Supports:
      - list[question]
      - {"qa_examples": [...]}
      - {"items"/"data"/"samples": [...]}
      - single question dict
    """
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        if isinstance(data.get('qa_examples'), list):
            items = data['qa_examples']
        elif isinstance(data.get('items'), list):
            items = data['items']
        elif isinstance(data.get('data'), list):
            items = data['data']
        elif isinstance(data.get('samples'), list):
            items = data['samples']
        else:
            items = [data]
    else:
        items = []

    return [normalize_question_item(x) for x in items]

def load_questions(file_path):
    """
    Load questions from JSON file

    Args:
        file_path: Path to JSON file containing questions

    Returns:
        List of question dictionaries
    """
    # Use caching if streamlit is available
    if HAS_STREAMLIT:
        return _load_questions_cached(file_path)
    else:
        return _load_questions_raw(file_path)

@st.cache_data if HAS_STREAMLIT else lambda func: func
def _load_questions_cached(file_path):
    """Cached version of load_questions"""
    return _load_questions_raw(file_path)

def _load_questions_raw(file_path):
    """Load questions without streamlit dependencies"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return parse_questions_data(data)
    except FileNotFoundError:
        if HAS_STREAMLIT:
            st.error(f"Data file not found: {file_path}")
        else:
            print(f"Error: Data file not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        if HAS_STREAMLIT:
            st.error(f"Error parsing JSON: {e}")
        else:
            print(f"Error: JSON parsing failed: {e}")
        return []

def format_choice_text(question, choice_label):
    """
    Format choice text for display

    Args:
        question: Question dictionary
        choice_label: Choice label (A, B, C, etc.)

    Returns:
        Formatted choice text
    """
    choices = question.get('choices', [])
    choice = next((c for c in choices if c['label'] == choice_label), None)

    if not choice:
        return f"{choice_label}. [Not found]"

    text = choice.get('text', 'No text')

    # Truncate long text
    max_length = 200
    if len(text) > max_length:
        text = text[:max_length] + "..."

    return f"{choice_label}. {text}"

def get_choice_full_text(question, choice_label):
    """
    Get full text of a choice (without truncation)

    Args:
        question: Question dictionary
        choice_label: Choice label (A, B, C, etc.)

    Returns:
        Full choice text
    """
    choices = question.get('choices', [])
    choice = next((c for c in choices if c['label'] == choice_label), None)

    if not choice:
        return "Choice not found"

    return choice.get('text', 'No text')

def extract_clip_ids(question):
    """
    Extract all clip IDs mentioned in the question

    Args:
        question: Question dictionary

    Returns:
        Set of clip IDs
    """
    clip_ids = set()

    # Query time
    query_time = question.get('query_time', '')
    if query_time:
        clip_ids.add(query_time)

    # Evidence times
    evidence_times = question.get('evidence_times', [])
    for evidence in evidence_times:
        clip_id = evidence.get('clip_id', '')
        if clip_id:
            clip_ids.add(clip_id)

    # Support clip IDs from choices
    choices = question.get('choices', [])
    for choice in choices:
        support_clip = choice.get('support_clip_id', '')
        if support_clip:
            clip_ids.add(support_clip)

    # Answer support clip
    answer_support = question.get('answer_support_clip_id', '')
    if answer_support:
        clip_ids.add(answer_support)

    return clip_ids

def get_question_stats(questions):
    """
    Get statistics about the question set

    Args:
        questions: List of question dictionaries

    Returns:
        Dictionary with statistics
    """
    if not questions:
        return {}

    total_clips = set()
    difficulty_counts = {}

    for q in questions:
        total_clips.update(extract_clip_ids(q))
        difficulty = q.get('difficulty_tier', 'unknown')
        difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1

    return {
        'total_questions': len(questions),
        'total_unique_clips': len(total_clips),
        'difficulty_distribution': difficulty_counts,
        'avg_choices_per_question': sum(len(q.get('choices', [])) for q in questions) / len(questions)
    }
