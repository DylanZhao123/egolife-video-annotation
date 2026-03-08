"""
Google Drive Folder Scanner
Scans a public Google Drive folder and generates video_mapping.json
"""

import os
import json
import requests
from pathlib import Path

# Google Drive API settings
API_KEY = os.getenv('GOOGLE_API_KEY', '')  # Optional: set via environment variable
FOLDER_ID = '1sF-zyyeaXBb68Ran3W-BWNPKv7gvaehQ'


def list_files_in_folder(folder_id, api_key=None):
    """
    List all files in a Google Drive folder using the API

    Args:
        folder_id: Google Drive folder ID
        api_key: Google API key (optional for public folders)

    Returns:
        List of file metadata
    """
    if not api_key:
        print("Warning: No API key provided. This may fail for private folders.")
        print("Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        return []

    url = "https://www.googleapis.com/drive/v3/files"

    params = {
        'q': f"'{folder_id}' in parents",
        'key': api_key,
        'fields': 'files(id, name, mimeType)',
        'pageSize': 1000
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        return data.get('files', [])

    except requests.exceptions.RequestException as e:
        print(f"Error accessing Google Drive API: {e}")
        return []


def scan_folder_structure(folder_id, api_key=None, path=""):
    """
    Recursively scan Google Drive folder structure

    Args:
        folder_id: Google Drive folder ID to scan
        api_key: Google API key
        path: Current path (for tracking hierarchy)

    Returns:
        Dict mapping clip_id to Google Drive file ID
    """
    files = list_files_in_folder(folder_id, api_key)

    video_mapping = {}

    for file in files:
        file_name = file['name']
        file_id = file['id']
        mime_type = file.get('mimeType', '')

        # If it's a folder, recurse into it
        if mime_type == 'application/vnd.google-apps.folder':
            current_path = f"{path}/{file_name}" if path else file_name
            print(f"Scanning folder: {current_path}")

            # Recursively scan subfolder
            subfolder_mapping = scan_folder_structure(file_id, api_key, current_path)
            video_mapping.update(subfolder_mapping)

        # If it's a video file, add to mapping
        elif file_name.endswith('.mp4'):
            # Extract clip_id from filename (remove .mp4 extension)
            clip_id = file_name.replace('.mp4', '')
            video_mapping[clip_id] = file_id

            print(f"  Found video: {clip_id} -> {file_id}")

    return video_mapping


def generate_mapping_file(output_file='data/video_mapping.json'):
    """
    Generate video_mapping.json from Google Drive folder scan
    """
    api_key = API_KEY

    if not api_key:
        print("\n" + "="*60)
        print("MANUAL MODE: Google API Key not found")
        print("="*60)
        print("\nTo use automatic scanning, set up Google API key:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project and enable Google Drive API")
        print("3. Create an API key")
        print("4. Set environment variable: GOOGLE_API_KEY=your_key")
        print("\nFor now, you'll need to manually create video_mapping.json")
        print("="*60 + "\n")
        return

    print(f"Scanning Google Drive folder: {FOLDER_ID}")
    print("-" * 60)

    video_mapping = scan_folder_structure(FOLDER_ID, api_key)

    print("-" * 60)
    print(f"\nFound {len(video_mapping)} videos")

    # Save to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(video_mapping, f, indent=2, ensure_ascii=False)

    print(f"Saved mapping to: {output_file}")

    # Show sample
    print("\nSample entries:")
    for i, (clip_id, file_id) in enumerate(list(video_mapping.items())[:5]):
        print(f"  {clip_id}: {file_id}")

    return video_mapping


if __name__ == "__main__":
    print("Google Drive Video Mapper")
    print("=" * 60)

    # Check if API key is available
    if API_KEY:
        generate_mapping_file()
    else:
        print("\nNo API key found. Starting manual mapping helper...")
        print("\nPlease share the file list from Google Drive,")
        print("or set up the API key to scan automatically.")
        print("\nFolder structure should be:")
        print("  Egolife_videos/")
        print("    A3_TASHA/")
        print("      DAY1/")
        print("        DAY1_A3_TASHA_xxxxx.mp4")
        print("      DAY2/")
        print("        ...")
