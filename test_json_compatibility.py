"""
Test script to verify JSON compatibility with the annotation system
"""

import json
import sys
from pathlib import Path

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import os
    os.system('chcp 65001 > nul')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.data_parser import parse_questions_data, normalize_question_item

def test_json_file(json_path):
    """Test if a JSON file is compatible with the annotation system"""

    print(f"Testing JSON file: {json_path}")
    print("=" * 80)

    # 1. Load the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("[OK] JSON file loaded successfully")
    except Exception as e:
        print(f"[ERROR] Failed to load JSON: {e}")
        return False

    # 2. Check if it's a list
    if not isinstance(data, list):
        print(f"[ERROR] Data is not a list, it's a {type(data)}")
        return False
    print(f"[OK] Data is a list with {len(data)} items")

    # 3. Parse the data using the parser
    try:
        questions = parse_questions_data(data)
        print(f"[OK] Successfully parsed {len(questions)} questions")
    except Exception as e:
        print(f"[ERROR] Failed to parse questions: {e}")
        return False

    # 4. Check the structure of the first few questions
    print("\n" + "=" * 80)
    print("Checking question structure...")
    print("=" * 80)

    for i, q in enumerate(questions[:3]):  # Check first 3 questions
        print(f"\nQuestion {i+1}:")
        print("-" * 40)

        # Required fields
        required_fields = ['sample_id', 'query', 'choices', 'correct_choice']
        missing_fields = []

        for field in required_fields:
            if field in q:
                if field == 'choices':
                    print(f"  [OK] {field}: {len(q[field])} choices")
                elif field == 'query':
                    print(f"  [OK] {field}: '{q[field][:60]}...'")
                else:
                    print(f"  [OK] {field}: {q[field]}")
            else:
                missing_fields.append(field)
                print(f"  [MISSING] {field}")

        # Optional but important fields
        optional_fields = ['query_time', 'evidence_times', 'difficulty_tier', 'query_type']
        for field in optional_fields:
            if field in q:
                if field == 'evidence_times':
                    print(f"  [INFO] {field}: {len(q[field])} evidence clips")
                else:
                    print(f"  [INFO] {field}: {q[field]}")

        # Check choices structure
        if 'choices' in q and q['choices']:
            print(f"\n  Choices structure:")
            for j, choice in enumerate(q['choices'][:2]):  # Show first 2 choices
                print(f"    Choice {j+1}:")
                print(f"      - label: {choice.get('label', 'MISSING')}")
                print(f"      - text: '{choice.get('text', 'MISSING')[:50]}...'")
                if 'event_id' in choice:
                    print(f"      - event_id: {choice['event_id']}")
                if 'support_clip_id' in choice:
                    print(f"      - support_clip_id: {choice['support_clip_id']}")

        # Check evidence_times structure
        if 'evidence_times' in q and q['evidence_times']:
            print(f"\n  Evidence structure (first item):")
            ev = q['evidence_times'][0]
            print(f"    - clip_id: {ev.get('clip_id', 'MISSING')}")
            if 'object_snapshot' in ev:
                print(f"    - object_snapshot:")
                print(f"        object_name: {ev['object_snapshot'].get('object_name', 'N/A')}")
                print(f"        location: {ev['object_snapshot'].get('location', 'N/A')}")
                print(f"        status: {ev['object_snapshot'].get('status', 'N/A')}")
            if 'timestamp_sec' in ev:
                print(f"    - timestamp_sec: {ev['timestamp_sec']}")
            if 'source_role' in ev:
                print(f"    - source_role: {ev['source_role']}")

        if missing_fields:
            print(f"\n  [WARNING] Missing required fields: {missing_fields}")

    # 5. Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    # Count different question types
    type_counts = {}
    for q in questions:
        qtype = q.get('query_type', 'unknown')
        type_counts[qtype] = type_counts.get(qtype, 0) + 1

    print(f"\nTotal questions: {len(questions)}")
    print(f"\nQuestion types:")
    for qtype, count in sorted(type_counts.items()):
        print(f"  - {qtype}: {count}")

    # Count questions with evidence
    with_evidence = sum(1 for q in questions if q.get('evidence_times'))
    print(f"\nQuestions with evidence_times: {with_evidence}/{len(questions)}")

    # Count questions with query_time
    with_query_time = sum(1 for q in questions if q.get('query_time'))
    print(f"Questions with query_time: {with_query_time}/{len(questions)}")

    # Check if all questions have required fields
    all_valid = True
    for i, q in enumerate(questions):
        if not all(field in q for field in required_fields):
            print(f"\n[ERROR] Question {i+1} is missing required fields")
            all_valid = False

    if all_valid:
        print("\n[OK] All questions have required fields")
        print("\n[SUCCESS] JSON file is COMPATIBLE with the annotation system!")
        return True
    else:
        print("\n[ERROR] Some questions are missing required fields")
        print("\n[WARNING] JSON file may have compatibility issues")
        return False

if __name__ == "__main__":
    json_path = r"C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite\new_question_examples\A3_TASHA_entity_mem_annotation_input_diverse25.json"

    success = test_json_file(json_path)

    if success:
        print("\n" + "=" * 80)
        print("RECOMMENDATION: You can use this JSON file with the annotation system")
        print("=" * 80)
        sys.exit(0)
    else:
        print("\n" + "=" * 80)
        print("RECOMMENDATION: Fix the issues before using this file")
        print("=" * 80)
        sys.exit(1)
