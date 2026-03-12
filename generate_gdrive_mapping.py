"""
Generate video_mapping.json from Google Drive folder

This script scans your Google Drive folder and creates a mapping file
that allows direct video embedding in the annotation app.

Prerequisites:
1. Install: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
2. Set up Google Cloud project and enable Drive API
3. Download OAuth2 credentials.json

Usage:
    python generate_gdrive_mapping.py
"""

import os
import json
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Your Google Drive folder ID (from the URL)
FOLDER_ID = '1DoVComPUp4juZ9tNFF7EhYYEXlkkBI6K'

def get_credentials():
    """Get valid user credentials from storage or run OAuth flow."""
    creds = None
    token_file = 'token.pickle'

    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("❌ credentials.json not found!")
                print("Please download OAuth2 credentials from Google Cloud Console")
                print("https://console.cloud.google.com/apis/credentials")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def list_files_in_folder(service, folder_id, folder_path=""):
    """Recursively list all video files in a folder."""
    video_map = {}

    try:
        # List all items in the folder
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            pageSize=1000,
            fields="files(id, name, mimeType)"
        ).execute()

        items = results.get('files', [])

        for item in items:
            item_name = item['name']
            item_id = item['id']
            mime_type = item['mimeType']

            current_path = f"{folder_path}/{item_name}" if folder_path else item_name

            if mime_type == 'application/vnd.google-apps.folder':
                # Recursively process subfolders
                print(f"📂 Scanning: {current_path}")
                subfolder_videos = list_files_in_folder(service, item_id, current_path)
                video_map.update(subfolder_videos)
            elif mime_type.startswith('video/') or item_name.endswith('.mp4'):
                # Video file found
                # Extract clip_id from filename (remove .mp4 extension)
                clip_id = Path(item_name).stem
                video_url = f"https://drive.google.com/file/d/{item_id}/view"
                video_map[clip_id] = video_url
                print(f"  🎬 Found: {clip_id}")

    except Exception as e:
        print(f"❌ Error scanning folder {folder_path}: {e}")

    return video_map

def main():
    """Main function to generate video mapping."""
    print("=" * 60)
    print("Google Drive Video Mapping Generator")
    print("=" * 60)
    print()

    # Get credentials
    print("🔐 Authenticating with Google Drive...")
    creds = get_credentials()
    if not creds:
        return

    # Build the Drive API service
    service = build('drive', 'v3', credentials=creds)

    print("✓ Authentication successful!")
    print()
    print(f"📂 Scanning folder ID: {FOLDER_ID}")
    print("This may take a few minutes for large folders...")
    print()

    # List all video files
    video_map = list_files_in_folder(service, FOLDER_ID)

    print()
    print("=" * 60)
    print(f"✓ Found {len(video_map)} video files")
    print("=" * 60)
    print()

    # Save to JSON file
    output_file = Path('data') / 'video_mapping.json'
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(video_map, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved mapping to: {output_file}")
    print()

    # Show sample mappings
    print("Sample mappings (first 5):")
    for i, (clip_id, url) in enumerate(list(video_map.items())[:5]):
        print(f"  {clip_id}")
        print(f"    → {url}")

    if len(video_map) > 5:
        print(f"  ... and {len(video_map) - 5} more")

    print()
    print("=" * 60)
    print("✓ Done! You can now deploy this mapping to Streamlit.")
    print("=" * 60)

if __name__ == '__main__':
    main()
