"""
Quick Test: Create a small video mapping for testing embedded playback

This script helps you quickly test video embedding without setting up Google API.
Just provide a few video file links from Google Drive.
"""

import json
from pathlib import Path

def main():
    print("=" * 60)
    print("Quick Video Mapping Generator")
    print("=" * 60)
    print()
    print("This tool helps you create a test mapping file.")
    print("You'll need to get Google Drive links for a few videos first.")
    print()
    print("How to get a video link:")
    print("1. Open Google Drive")
    print("2. Navigate to your video file")
    print("3. Right-click the file > 'Get link'")
    print("4. Copy the link (looks like: https://drive.google.com/file/d/FILE_ID/view)")
    print()
    print("=" * 60)
    print()

    mapping = {}

    print("Enter your test videos (or type 'done' to finish):")
    print()

    while True:
        print("-" * 60)
        clip_id = input("Clip ID (e.g., DAY1_A3_TASHA_14143000): ").strip()

        if clip_id.lower() == 'done':
            break

        if not clip_id:
            continue

        # Remove .mp4 extension if user included it
        if clip_id.endswith('.mp4'):
            clip_id = clip_id[:-4]

        google_link = input("Google Drive link: ").strip()

        if not google_link:
            continue

        # Extract file ID from link if it's a full URL
        if 'drive.google.com/file/d/' in google_link:
            # Already in correct format
            mapping[clip_id] = google_link
            print(f"✓ Added: {clip_id}")
        elif len(google_link) > 20:  # Probably a file ID
            mapping[clip_id] = f"https://drive.google.com/file/d/{google_link}/view"
            print(f"✓ Added: {clip_id}")
        else:
            print("❌ Invalid link format. Please try again.")
            continue

        print()

    if not mapping:
        print("\nNo videos added. Exiting.")
        return

    print()
    print("=" * 60)
    print(f"✓ Created mapping for {len(mapping)} videos")
    print("=" * 60)
    print()

    # Save to file
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'video_mapping.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to: {output_file}")
    print()
    print("Mappings created:")
    for clip_id, url in mapping.items():
        print(f"  {clip_id}")
        print(f"    → {url}")
    print()
    print("=" * 60)
    print("Next steps:")
    print("1. Run: streamlit run app.py")
    print("2. Upload a JSON file containing these clip_ids")
    print("3. Switch to Google Drive mode")
    print("4. Videos should now embed directly!")
    print("=" * 60)

if __name__ == '__main__':
    main()
