"""
Helper script to generate video_mapping.json from your data file
This extracts all unique clip_ids from the question data
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_parser import load_questions, extract_clip_ids

def generate_video_mapping(data_file, output_file):
    """
    Generate video mapping template from question data

    Args:
        data_file: Path to question JSON file
        output_file: Path to output video_mapping.json
    """
    print(f"Loading questions from {data_file}...")
    questions = load_questions(data_file)

    if not questions:
        print("No questions found!")
        return

    print(f"Loaded {len(questions)} questions")

    # Extract all clip IDs
    all_clip_ids = set()
    for question in questions:
        clip_ids = extract_clip_ids(question)
        all_clip_ids.update(clip_ids)

    print(f"Found {len(all_clip_ids)} unique video clips")

    # Create mapping template
    mapping = {}
    for clip_id in sorted(all_clip_ids):
        mapping[clip_id] = f"https://your-onedrive-link.com/{clip_id}.mp4?download=1"

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)

    print(f"Video mapping template saved to {output_file}")
    print(f"\nNext steps:")
    print(f"1. Go to your OneDrive folder")
    print(f"2. For each video, right-click -> Share -> Get link")
    print(f"3. Make sure 'Anyone with the link can view' is selected")
    print(f"4. Copy the share link and add ?download=1 at the end")
    print(f"5. Update the URLs in {output_file}")
    print(f"\nExample OneDrive link format:")
    print(f"https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/_layouts/15/download.aspx?...")

if __name__ == "__main__":
    # Paths
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'
    output_file = base_dir / 'data' / 'video_mapping_template.json'

    generate_video_mapping(data_file, output_file)
