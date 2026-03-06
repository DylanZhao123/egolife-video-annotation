"""
Automatic OneDrive Video Link Setup
This script connects to OneDrive and automatically generates share links for all videos
"""

import json
import requests
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_parser import extract_clip_ids, load_questions

class OneDriveVideoSetup:
    """Automatically setup video links from OneDrive"""

    def __init__(self, access_token):
        """
        Initialize with OneDrive access token

        Args:
            access_token: Microsoft Graph API access token
        """
        self.access_token = access_token
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    def list_folder_contents(self, folder_path):
        """
        List all files in a OneDrive folder

        Args:
            folder_path: Path to folder (e.g., "/Egolife_videos")

        Returns:
            List of file items
        """
        # Encode folder path
        encoded_path = requests.utils.quote(folder_path)

        # Get folder contents
        url = f"{self.base_url}/me/drive/root:/{encoded_path}:/children"

        print(f"Fetching folder contents from: {folder_path}")
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.json())
            return []

        data = response.json()
        items = data.get('value', [])

        print(f"Found {len(items)} items in folder")
        return items

    def create_share_link(self, item_id, link_type='view'):
        """
        Create a sharing link for a file

        Args:
            item_id: OneDrive item ID
            link_type: 'view', 'edit', or 'embed'

        Returns:
            Sharing link URL
        """
        url = f"{self.base_url}/me/drive/items/{item_id}/createLink"

        payload = {
            "type": link_type,
            "scope": "anonymous"  # Anyone with the link
        }

        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code in [200, 201]:
            data = response.json()
            return data['link']['webUrl']
        else:
            print(f"Error creating share link: {response.status_code}")
            print(response.json())
            return None

    def get_direct_download_link(self, item_id):
        """
        Get direct download link for a file

        Args:
            item_id: OneDrive item ID

        Returns:
            Direct download URL
        """
        url = f"{self.base_url}/me/drive/items/{item_id}/content"

        # Get redirect URL (don't follow redirect)
        response = requests.get(url, headers=self.headers, allow_redirects=False)

        if response.status_code == 302:
            download_url = response.headers.get('Location')
            return download_url
        else:
            print(f"Error getting download link: {response.status_code}")
            return None

    def extract_clip_id_from_filename(self, filename):
        """Extract clip ID from filename (remove extension)"""
        return Path(filename).stem

    def setup_video_mapping(self, folder_path, required_clip_ids, output_file):
        """
        Automatically setup video mapping

        Args:
            folder_path: OneDrive folder path
            required_clip_ids: Set of required clip IDs
            output_file: Path to output JSON file
        """
        print(f"\n{'='*60}")
        print("OneDrive Video Link Setup")
        print(f"{'='*60}\n")

        # Get folder contents
        items = self.list_folder_contents(folder_path)

        if not items:
            print("No files found in folder!")
            return

        # Filter video files
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        video_files = [
            item for item in items
            if item.get('file') and any(item['name'].lower().endswith(ext) for ext in video_extensions)
        ]

        print(f"\nFound {len(video_files)} video files")
        print(f"Need links for {len(required_clip_ids)} clip IDs\n")

        # Create mapping
        mapping = {}
        found_count = 0
        missing_clips = set(required_clip_ids)

        for i, video in enumerate(video_files, 1):
            filename = video['name']
            item_id = video['id']
            clip_id = self.extract_clip_id_from_filename(filename)

            print(f"[{i}/{len(video_files)}] Processing: {filename}")

            # Check if this clip is needed
            if clip_id in required_clip_ids:
                print(f"  -> Found required clip: {clip_id}")

                # Get share link
                share_link = self.create_share_link(item_id)

                if share_link:
                    # Convert to direct download link
                    if '?' in share_link:
                        download_link = f"{share_link}&download=1"
                    else:
                        download_link = f"{share_link}?download=1"

                    mapping[clip_id] = download_link
                    found_count += 1
                    missing_clips.discard(clip_id)
                    print(f"  -> Link generated successfully")
                else:
                    print(f"  -> Failed to generate link")
            else:
                print(f"  -> Skipping (not in required list)")

        # Summary
        print(f"\n{'='*60}")
        print("Summary")
        print(f"{'='*60}")
        print(f"Total video files in OneDrive: {len(video_files)}")
        print(f"Required clip IDs: {len(required_clip_ids)}")
        print(f"Successfully mapped: {found_count}")
        print(f"Missing: {len(missing_clips)}")

        if missing_clips:
            print(f"\nMissing clip IDs:")
            for clip_id in sorted(list(missing_clips))[:10]:
                print(f"  - {clip_id}")
            if len(missing_clips) > 10:
                print(f"  ... and {len(missing_clips) - 10} more")

        # Save mapping
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2)

        print(f"\nVideo mapping saved to: {output_file}")
        print(f"\nNext step: Copy this file to data/video_mapping.json")

        return mapping

def get_access_token_interactive():
    """
    Guide user to get access token
    """
    print("\n" + "="*60)
    print("Get Microsoft Graph API Access Token")
    print("="*60)
    print("\nOption 1: Using Graph Explorer (Easiest)")
    print("1. Go to: https://developer.microsoft.com/en-us/graph/graph-explorer")
    print("2. Sign in with your UNC account")
    print("3. Click 'Consent to permissions' and allow:")
    print("   - Files.Read.All")
    print("   - Files.ReadWrite.All")
    print("4. In the top bar, click 'Access token'")
    print("5. Copy the token and paste it here")
    print("\nOption 2: Using Azure Portal (Advanced)")
    print("See ONEDRIVE_SETUP.md for detailed instructions")
    print("="*60 + "\n")

    token = input("Paste your access token here: ").strip()
    return token

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent

    # Load required clip IDs
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'
    print(f"Loading questions from: {data_file}")

    questions = load_questions(str(data_file))

    if not questions:
        print("Error: Could not load questions!")
        return

    # Extract all required clip IDs
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f"Found {len(required_clip_ids)} unique clip IDs needed")

    # Get access token
    print("\nYou need a Microsoft Graph API access token to proceed.")
    print("This token gives temporary access to your OneDrive files.")

    choice = input("\nDo you want to get the access token now? (y/n): ").strip().lower()

    if choice != 'y':
        print("\nTo run this script later:")
        print("python tools/setup_onedrive_links.py")
        return

    access_token = get_access_token_interactive()

    if not access_token:
        print("No access token provided. Exiting.")
        return

    # Setup OneDrive client
    client = OneDriveVideoSetup(access_token)

    # OneDrive folder path
    folder_path = "Egolife_videos"
    print(f"\nUsing OneDrive folder: {folder_path}")

    # Output file
    output_file = base_dir / 'data' / 'video_mapping_generated.json'

    # Run setup
    try:
        mapping = client.setup_video_mapping(folder_path, required_clip_ids, output_file)

        if mapping:
            print("\n" + "="*60)
            print("SUCCESS! Video mapping created")
            print("="*60)
            print(f"\nGenerated file: {output_file}")
            print(f"\nTo use it, run:")
            print(f"cp {output_file} {base_dir}/data/video_mapping.json")

    except Exception as e:
        print(f"\nError: {e}")
        print("\nIf you see authentication errors, your token may have expired.")
        print("Get a new token from Graph Explorer and try again.")

if __name__ == "__main__":
    main()
