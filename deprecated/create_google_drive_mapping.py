"""
Simple Google Drive Mapping Generator
Helps create video_mapping.json from Google Drive folder
"""

import json
import os
from pathlib import Path

print("=" * 70)
print("Google Drive Video Mapping Generator")
print("=" * 70)
print("\nThis tool will help you create video_mapping.json for Google Drive")
print("\nYou have 2 options:")
print("  1. Automatic scan (requires Google API key)")
print("  2. Manual entry (no API key needed)")
print("=" * 70)

choice = input("\nChoose option (1 or 2): ").strip()

if choice == "1":
    print("\n" + "=" * 70)
    print("OPTION 1: Automatic Scan with Google Drive API")
    print("=" * 70)

    api_key = input("\nEnter your Google API Key (or press Enter to skip): ").strip()

    if not api_key:
        print("\nNo API key provided. Switching to manual mode...")
        choice = "2"
    else:
        # Use the API scanner
        print("\nScanning Google Drive folder...")
        print("Folder ID: 1sF-zyyeaXBb68Ran3W-BWNPKv7gvaehQ")

        try:
            import requests

            FOLDER_ID = '1sF-zyyeaXBb68Ran3W-BWNPKv7gvaehQ'

            def list_files_in_folder(folder_id, api_key, path=""):
                """Recursively list all files in folder"""
                url = "https://www.googleapis.com/drive/v3/files"
                params = {
                    'q': f"'{folder_id}' in parents",
                    'key': api_key,
                    'fields': 'files(id, name, mimeType)',
                    'pageSize': 1000
                }

                response = requests.get(url, params=params)
                response.raise_for_status()

                files = response.json().get('files', [])
                video_mapping = {}

                for file in files:
                    file_name = file['name']
                    file_id = file['id']
                    mime_type = file.get('mimeType', '')

                    if mime_type == 'application/vnd.google-apps.folder':
                        # Recursively scan subfolder
                        current_path = f"{path}/{file_name}" if path else file_name
                        print(f"  Scanning: {current_path}")
                        subfolder_mapping = list_files_in_folder(file_id, api_key, current_path)
                        video_mapping.update(subfolder_mapping)

                    elif file_name.endswith('.mp4'):
                        clip_id = file_name.replace('.mp4', '')
                        video_mapping[clip_id] = file_id
                        print(f"    ✓ {clip_id}")

                return video_mapping

            print("\nScanning folders...")
            mapping = list_files_in_folder(FOLDER_ID, api_key)

            print(f"\n✓ Found {len(mapping)} videos")

            # Save to file
            output_file = Path("data/video_mapping.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(mapping, f, indent=2, ensure_ascii=False)

            print(f"✓ Saved to: {output_file}")

            # Show sample
            print("\nSample entries:")
            for i, (clip_id, file_id) in enumerate(list(mapping.items())[:5]):
                print(f"  {clip_id}: {file_id}")

            print("\n✓ Complete! You can now run your app with Google Drive videos.")

        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("\nTroubleshooting:")
            print("1. Check that your API key is correct")
            print("2. Ensure Google Drive API is enabled in your project")
            print("3. Verify the folder is set to 'Anyone with the link can view'")

if choice == "2":
    print("\n" + "=" * 70)
    print("OPTION 2: Manual Entry")
    print("=" * 70)
    print("""
To get file IDs manually:

1. Open: https://drive.google.com/drive/folders/1sF-zyyeaXBb68Ran3W-BWNPKv7gvaehQ

2. Navigate to a video file (e.g., A3_TASHA/DAY1/DAY1_A3_TASHA_xxxxx.mp4)

3. Right-click the video → "Get link"

4. Copy the file ID from the URL:
   https://drive.google.com/file/d/FILE_ID_HERE/view

5. Example:
   Filename: DAY1_A3_TASHA_11093015.mp4
   File ID: 1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy

For faster manual mapping, use the interactive tool:
  python utils/google_drive_mapper.py

Or create a text file with mappings and run:
  python utils/google_drive_mapper.py file_list.txt
""")

    print("\nWould you like to:")
    print("  a) Start interactive mapping now")
    print("  b) Exit and map later")

    sub_choice = input("\nChoice (a/b): ").strip().lower()

    if sub_choice == 'a':
        print("\nStarting interactive mapper...")
        print("\nEnter mappings in format: filename.mp4: file_id")
        print("Type 'done' when finished\n")

        mapping = {}

        # Load existing if available
        existing_file = Path("data/video_mapping.json")
        if existing_file.exists():
            with open(existing_file, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            print(f"✓ Loaded {len(mapping)} existing mappings\n")

        while True:
            user_input = input("Enter mapping (or 'done'): ").strip()

            if user_input.lower() == 'done':
                break

            if ':' not in user_input:
                print("  Invalid format. Use: filename.mp4: file_id")
                continue

            parts = user_input.split(':', 1)
            filename = parts[0].strip()
            file_id = parts[1].strip()

            clip_id = filename.replace('.mp4', '')
            mapping[clip_id] = file_id

            print(f"  ✓ Added: {clip_id}")

        # Save
        output_file = Path("data/video_mapping.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Saved {len(mapping)} mappings to {output_file}")
    else:
        print("\nNo problem! You can map videos later using:")
        print("  python utils/google_drive_mapper.py")

print("\n" + "=" * 70)
print("Next Steps:")
print("=" * 70)
print("""
1. Verify video_mapping.json was created in data/ folder
2. Test locally: streamlit run app.py
3. Push to GitHub to deploy to Streamlit Cloud
4. Your app will automatically use Google Drive videos with iframe embeds!
""")
