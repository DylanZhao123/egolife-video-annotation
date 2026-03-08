"""
Batch Import Google Drive Videos
Quick tool to import multiple video links at once
"""

import json
import re
from pathlib import Path

print("=" * 70)
print("Batch Import Google Drive Videos")
print("=" * 70)
print("""
INSTRUCTIONS:

Method 1 - Paste Multiple Links at Once:
------------------------------------------
1. In Google Drive, select multiple video files (Ctrl+Click or Shift+Click)
2. Right-click → "Get link" → Copy links
3. Paste all links below (one per line or all at once)

Method 2 - Auto-detect from Browser:
-------------------------------------
1. Navigate through your Google Drive folders in browser
2. Copy the file list text from the page
3. Paste below - the tool will extract file IDs automatically

The tool will automatically extract file IDs from any Google Drive URLs!
""")
print("=" * 70)
print("\nPaste your Google Drive links below.")
print("When done, press Enter on a blank line, then type 'done' and press Enter again:\n")

# Collect input
lines = []
while True:
    line = input()
    if line.strip().lower() == 'done':
        break
    if line.strip():
        lines.append(line)

print(f"\nProcessing {len(lines)} lines...")

# Extract file IDs and filenames
mapping = {}
pattern_url = r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
pattern_id = r'\b([a-zA-Z0-9_-]{33})\b'  # Google Drive file IDs are 33 chars

for line in lines:
    # Try to extract URL
    url_match = re.search(pattern_url, line)
    if url_match:
        file_id = url_match.group(1)

        # Try to find filename in the same line
        # Look for pattern like "DAY1_A3_TASHA_12345678"
        filename_match = re.search(r'(DAY\d+_[A-Z0-9]+_[A-Z]+_\d+)', line)
        if filename_match:
            clip_id = filename_match.group(1)
        else:
            # Ask for filename
            print(f"\nFound file ID: {file_id}")
            clip_id = input("  Enter clip_id (e.g., DAY1_A3_TASHA_12345678): ").strip()
            if not clip_id:
                continue

        mapping[clip_id] = file_id
        print(f"  ✓ {clip_id} -> {file_id}")
    else:
        # Try to extract standalone file ID
        id_match = re.search(pattern_id, line)
        if id_match:
            file_id = id_match.group(1)
            filename_match = re.search(r'(DAY\d+_[A-Z0-9]+_[A-Z]+_\d+)', line)
            if filename_match:
                clip_id = filename_match.group(1)
                mapping[clip_id] = file_id
                print(f"  ✓ {clip_id} -> {file_id}")

# Load existing mapping
existing_file = Path("data/video_mapping.json")
if existing_file.exists():
    with open(existing_file, 'r', encoding='utf-8') as f:
        existing_mapping = json.load(f)
    print(f"\n✓ Loaded {len(existing_mapping)} existing mappings")
    existing_mapping.update(mapping)
    mapping = existing_mapping

# Save
output_file = Path("data/video_mapping.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print(f"\n{'=' * 70}")
print(f"✓ SUCCESS! Saved {len(mapping)} videos to {output_file}")
print(f"{'=' * 70}")

# Show sample
print("\nSample entries:")
for i, (clip_id, file_id) in enumerate(list(mapping.items())[:10]):
    preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
    print(f"  {clip_id}:")
    print(f"    {preview_url}")

print(f"\n{'=' * 70}")
print("Next Steps:")
print("  1. Test locally: streamlit run app.py")
print("  2. Push to GitHub: git add . && git commit -m 'Add videos' && git push")
print("  3. Your Streamlit Cloud app will auto-update!")
print(f"{'=' * 70}")
