"""
Test Google Drive video loading with a simple example
"""

import json
from pathlib import Path

# Test with a sample Google Drive file ID
# You can get this by:
# 1. Right-click any video in your Google Drive folder
# 2. Click "Get link"
# 3. Extract the ID from the URL

TEST_MAPPING = {
    "DAY1_A3_TASHA_11093015": "1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy",  # Example from before
    # Add more mappings here...
}


def create_test_mapping():
    """Create a test video_mapping.json with Google Drive file IDs"""

    output_file = Path("data/video_mapping_google_drive.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(TEST_MAPPING, f, indent=2, ensure_ascii=False)

    print(f"✓ Created test mapping: {output_file}")
    print(f"  Videos: {len(TEST_MAPPING)}")

    # Print test URLs
    print("\nGenerated URLs:")
    for clip_id, file_id in TEST_MAPPING.items():
        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
        view_url = f"https://drive.google.com/file/d/{file_id}/view"
        print(f"\n{clip_id}:")
        print(f"  Preview: {preview_url}")
        print(f"  View: {view_url}")


def print_instructions():
    """Print instructions for getting Google Drive file IDs"""
    print("\n" + "=" * 70)
    print("HOW TO GET GOOGLE DRIVE FILE IDs")
    print("=" * 70)
    print("""
1. Open your Google Drive folder:
   https://drive.google.com/drive/folders/1sF-zyyeaXBb68Ran3W-BWNPKv7gvaehQ

2. Navigate to a video file (e.g., A3_TASHA/DAY1/DAY1_A3_TASHA_xxxxx.mp4)

3. Right-click the video file → Click "Get link" or "Share"

4. The link will look like:
   https://drive.google.com/file/d/1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy/view?usp=sharing

5. The FILE ID is the part after "/d/" and before "/view":
   1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy

6. Add to TEST_MAPPING in this file:
   "DAY1_A3_TASHA_11093015": "1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy"

7. Run this script again to test

ALTERNATIVE - Use the automatic scanner (requires API key):
1. Get a Google API key from https://console.cloud.google.com/
2. Enable Google Drive API
3. Set environment variable: GOOGLE_API_KEY=your_key_here
4. Run: python scan_google_drive.py
""")
    print("=" * 70)


if __name__ == "__main__":
    print("Google Drive Video Test")
    print("=" * 70)

    if len(TEST_MAPPING) == 1:
        print("\n⚠ Only 1 test video configured")
        print_instructions()
    else:
        print(f"\n✓ {len(TEST_MAPPING)} videos configured")

    create_test_mapping()

    print("\n✓ Test mapping created!")
    print("\nNext steps:")
    print("1. Add more file IDs to TEST_MAPPING in this file")
    print("2. Or use utils/google_drive_mapper.py for interactive mapping")
    print("3. Or set up API key and run scan_google_drive.py")
