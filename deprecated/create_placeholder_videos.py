"""
Create placeholder video mapping for testing
创建占位符视频映射用于测试
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils.data_parser import load_questions, extract_clip_ids

def main():
    print("\n" + "="*70)
    print("  CREATE PLACEHOLDER VIDEO MAPPING")
    print("  创建占位符视频映射")
    print("="*70 + "\n")

    print("This will create a placeholder mapping that shows:")
    print("这将创建一个占位符映射，显示：")
    print('- Message: "Video configuration pending"')
    print('- 消息："视频配置待完成"\n')

    base_dir = Path(__file__).parent
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'

    # Load questions
    questions = load_questions(str(data_file))
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f"Found {len(required_clip_ids)} video clips needed\n")

    # Create placeholder mapping
    # Option 1: Use a sample video URL (public domain)
    sample_video = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

    # Option 2: Use placeholder
    video_mapping = {}
    for clip_id in sorted(required_clip_ids):
        # You can either use:
        # 1. A sample video URL for all (for testing UI)
        # 2. Empty string (will show "Video not configured")

        video_mapping[clip_id] = ""  # Empty = show configuration message

    # Save
    output_file = base_dir / 'data' / 'video_mapping.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(video_mapping, f, indent=2, ensure_ascii=False)

    print(f"✅ Created: {output_file}")
    print(f"✅ Created {len(video_mapping)} placeholder entries\n")

    print("="*70)
    print("NOW YOU CAN:")
    print("现在你可以：")
    print("="*70)
    print("\n1. Test the UI and question flow without videos")
    print("   测试UI和问题流程（无视频）")
    print("\n2. Add real OneDrive URLs later when ready")
    print("   准备好后再添加真实的OneDrive URL")
    print("\n3. Run: streamlit run app.py")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
    input("Press ENTER to exit...")
