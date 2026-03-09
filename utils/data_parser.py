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

def parse_questions_data(data):
    """
    Parse questions data from already-loaded JSON

    Args:
        data: JSON data (dict or list)

    Returns:
        List of question dictionaries
    """
    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return [data]
    else:
        return []

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
            return data if isinstance(data, list) else [data]
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
