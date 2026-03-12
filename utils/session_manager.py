"""
Session Manager Module
Handles session state initialization, progress saving, and recovery
"""

import streamlit as st
import json
import time
import re
from pathlib import Path
from datetime import datetime
import config

def _sanitize_key(text):
    text = str(text)
    text = re.sub(r'[^a-zA-Z0-9._-]+', '_', text)
    return text[:180] if len(text) > 180 else text

def _progress_file(progress_key=None):
    if not progress_key:
        return Path(config.DATA_DIR) / 'progress.json'
    safe_key = _sanitize_key(progress_key)
    return Path(config.DATA_DIR) / f'progress_{safe_key}.json'

def initialize_session():
    """Initialize Streamlit session state variables"""

    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    if 'responses' not in st.session_state:
        st.session_state.responses = []

    if 'question_start_time' not in st.session_state:
        st.session_state.question_start_time = time.time()

    if 'session_start_time' not in st.session_state:
        st.session_state.session_start_time = datetime.now()

    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""

def save_progress(current_index, responses, progress_key=None, extra_state=None):
    """
    Save current progress to file

    Args:
        current_index: Current question index
        responses: List of response dictionaries
    """
    progress_file = _progress_file(progress_key)

    progress_data = {
        'current_index': current_index,
        'responses': responses,
        'last_saved': datetime.now().isoformat(),
        'user_id': st.session_state.get('user_id', ''),
        'session_start': st.session_state.get('session_start_time', datetime.now()).isoformat()
    }
    if extra_state and isinstance(extra_state, dict):
        progress_data.update(extra_state)

    try:
        # Create data directory if it doesn't exist
        Path(config.DATA_DIR).mkdir(parents=True, exist_ok=True)

        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2)

        return True
    except Exception as e:
        st.error(f"❌ Error saving progress: {e}")
        return False

def load_progress(progress_key=None):
    """
    Load progress from file

    Returns:
        Progress dictionary or None if not found
    """
    progress_file = _progress_file(progress_key)

    try:
        if progress_file.exists():
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return None
    except Exception as e:
        st.warning(f"⚠️ Error loading progress: {e}")
        return None

def clear_progress(progress_key=None):
    """Delete progress file"""
    progress_file = _progress_file(progress_key)

    try:
        if progress_file.exists():
            progress_file.unlink()
            return True
    except Exception as e:
        st.error(f"❌ Error clearing progress: {e}")
        return False

def get_session_duration():
    """
    Get current session duration in seconds

    Returns:
        Duration in seconds
    """
    if 'session_start_time' in st.session_state:
        return (datetime.now() - st.session_state.session_start_time).total_seconds()
    return 0

def format_duration(seconds):
    """
    Format duration in human-readable format

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "1h 23m 45s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)
