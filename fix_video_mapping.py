"""
Fix Video Mapping - Match short clip_ids to full filenames
"""

import json
from pathlib import Path

# Load existing mapping (from Google Drive scan)
with open('data/video_mapping copy.json', 'r', encoding='utf-8') as f:
    full_mapping = json.load(f)

# Load question data to get required clip_ids
with open('data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Extract all clip_ids from questions
required_clip_ids = set()

for q in questions:
    # Query time
    if 'query_time' in q and q['query_time']:
        required_clip_ids.add(q['query_time'])

    # Evidence clips
    if 'evidence_times' in q:
        for ev in q['evidence_times']:
            if 'clip_id' in ev and ev['clip_id']:
                required_clip_ids.add(ev['clip_id'])

    # Support clips in choices
    if 'choices' in q:
        for choice in q['choices']:
            if 'support_clip_id' in choice and choice['support_clip_id']:
                required_clip_ids.add(choice['support_clip_id'])

print(f"Found {len(required_clip_ids)} unique clip_ids in questions")

# Create new mapping
new_mapping = {}

def clip_id_matches(short_id, full_id):
    """Check if short clip_id matches full clip_id"""
    # Extract base parts (DAY, person, timestamp)
    # Short: DAY5_A3_TASHA_12143000
    # Full:  DAY5_A3_TASHA_11160008_12530000

    short_parts = short_id.split('_')
    full_parts = full_id.split('_')

    # Check day and person match
    if len(short_parts) < 4 or len(full_parts) < 5:
        return False

    day_match = short_parts[0] == full_parts[0]
    person_match = (short_parts[1] == full_parts[1] and
                   short_parts[2] == full_parts[2])

    if not (day_match and person_match):
        return False

    # Check if short timestamp falls within range or matches start
    short_time = short_parts[3]
    start_time = full_parts[3]

    # Try different matching strategies
    # 1. Exact match with start time
    if short_time == start_time:
        return True

    # 2. Check if in range (if we have end time)
    if len(full_parts) >= 5:
        end_time = full_parts[4]
        # Short time should be >= start and <= end
        if start_time <= short_time <= end_time:
            return True

    return False

# Match clip_ids
matched = 0
unmatched = []

for required_id in sorted(required_clip_ids):
    found = False

    # Try to find matching full clip_id
    for full_id, file_id in full_mapping.items():
        if clip_id_matches(required_id, full_id):
            new_mapping[required_id] = file_id
            matched += 1
            found = True
            print(f"OK Matched: {required_id} -> {full_id}")
            break

    if not found:
        unmatched.append(required_id)
        print(f"XX No match: {required_id}")

print(f"\n{'='*70}")
print(f"Matched: {matched}/{len(required_clip_ids)}")
print(f"Unmatched: {len(unmatched)}")

if unmatched:
    print(f"\nUnmatched clip_ids:")
    for clip_id in unmatched[:10]:
        print(f"  - {clip_id}")
    if len(unmatched) > 10:
        print(f"  ... and {len(unmatched) - 10} more")

# Save new mapping
output_file = Path('data/video_mapping.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_mapping, f, indent=2, ensure_ascii=False)

print(f"\nOK Saved {len(new_mapping)} mappings to {output_file}")
print(f"{'='*70}")
