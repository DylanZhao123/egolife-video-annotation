"""
Response Recorder Module
Handles saving and exporting user responses
"""

import json
from pathlib import Path
from datetime import datetime
import streamlit as st
import config

def save_response(response_data):
    """
    Save a single response to JSONL file

    Args:
        response_data: Dictionary containing response information

    Returns:
        True if successful, False otherwise
    """
    response_file = Path(config.DATA_DIR) / 'responses.jsonl'

    try:
        # Create data directory if it doesn't exist
        Path(config.DATA_DIR).mkdir(parents=True, exist_ok=True)

        # Append to JSONL file
        with open(response_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(response_data) + '\n')

        return True
    except Exception as e:
        st.error(f"❌ Error saving response: {e}")
        return False

def load_responses():
    """
    Load all responses from JSONL file

    Returns:
        List of response dictionaries
    """
    response_file = Path(config.DATA_DIR) / 'responses.jsonl'
    responses = []

    try:
        if response_file.exists():
            with open(response_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        responses.append(json.loads(line))
    except Exception as e:
        st.error(f"❌ Error loading responses: {e}")

    return responses

def export_responses(responses, format='jsonl'):
    """
    Export responses to file

    Args:
        responses: List of response dictionaries
        format: Export format ('jsonl', 'json', or 'csv')

    Returns:
        Path to exported file
    """
    export_dir = Path(config.DATA_DIR) / 'exports'
    export_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if format == 'jsonl':
        export_file = export_dir / f'responses_{timestamp}.jsonl'
        with open(export_file, 'w', encoding='utf-8') as f:
            for response in responses:
                f.write(json.dumps(response) + '\n')

    elif format == 'json':
        export_file = export_dir / f'responses_{timestamp}.json'
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(responses, f, indent=2)

    elif format == 'csv':
        export_file = export_dir / f'responses_{timestamp}.csv'
        import csv

        if responses:
            keys = responses[0].keys()
            with open(export_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(responses)

    return str(export_file)

def calculate_accuracy(responses):
    """
    Calculate accuracy from responses

    Args:
        responses: List of response dictionaries

    Returns:
        Accuracy percentage (0-100)
    """
    if not responses:
        return 0.0

    correct = sum(1 for r in responses if r.get('is_correct', False))
    return (correct / len(responses)) * 100

def calculate_stats(responses):
    """
    Calculate statistics from responses

    Args:
        responses: List of response dictionaries

    Returns:
        Dictionary with statistics
    """
    if not responses:
        return {
            'total_responses': 0,
            'accuracy': 0.0,
            'avg_time': 0.0,
            'total_time': 0.0
        }

    correct = sum(1 for r in responses if r.get('is_correct', False))
    times = [r.get('time_spent_seconds', 0) for r in responses]

    return {
        'total_responses': len(responses),
        'correct_responses': correct,
        'accuracy': (correct / len(responses)) * 100,
        'avg_time': sum(times) / len(times),
        'total_time': sum(times),
        'min_time': min(times) if times else 0,
        'max_time': max(times) if times else 0
    }

def get_response_summary(responses):
    """
    Generate a summary report of responses

    Args:
        responses: List of response dictionaries

    Returns:
        Formatted summary string
    """
    if not responses:
        return "No responses recorded yet."

    stats = calculate_stats(responses)

    summary = f"""
📊 Response Summary
==================
Total Questions Answered: {stats['total_responses']}
Correct Answers: {stats['correct_responses']}
Accuracy: {stats['accuracy']:.1f}%
Average Time per Question: {stats['avg_time']:.1f}s
Total Time Spent: {stats['total_time']:.1f}s
Fastest Response: {stats['min_time']:.1f}s
Slowest Response: {stats['max_time']:.1f}s
"""

    return summary
