"""
Google Drive Manual Mapper
Helper tool to create video_mapping.json from Google Drive file links
"""

import json
import re
from pathlib import Path


class GoogleDriveMapper:
    """Helper to map video clip IDs to Google Drive file IDs"""

    def __init__(self):
        self.mapping = {}

    def extract_file_id(self, url_or_id):
        """
        Extract Google Drive file ID from URL or return ID if already extracted

        Args:
            url_or_id: Google Drive URL or file ID

        Returns:
            str: File ID or None
        """
        # If it's already a file ID (33 chars, alphanumeric + - _)
        if re.match(r'^[a-zA-Z0-9_-]{33}$', url_or_id):
            return url_or_id

        # Try to extract from URL
        # Format: https://drive.google.com/file/d/{FILE_ID}/view
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url_or_id)
        if match:
            return match.group(1)

        # Format: https://drive.google.com/open?id={FILE_ID}
        match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url_or_id)
        if match:
            return match.group(1)

        return None

    def add_video(self, clip_id, url_or_id):
        """
        Add a video mapping

        Args:
            clip_id: Video clip ID (e.g., DAY5_A3_TASHA_12143000)
            url_or_id: Google Drive URL or file ID
        """
        file_id = self.extract_file_id(url_or_id)

        if file_id:
            self.mapping[clip_id] = file_id
            print(f"✓ Added: {clip_id} -> {file_id}")
        else:
            print(f"✗ Failed to extract ID from: {url_or_id}")

    def add_from_text(self, text):
        """
        Parse text containing file names and URLs/IDs

        Format:
            DAY5_A3_TASHA_12143000.mp4: https://drive.google.com/file/d/xxx/view
            or
            DAY5_A3_TASHA_12143000.mp4, xxx-file-id-xxx

        Args:
            text: Multi-line text with file mappings
        """
        lines = text.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try to parse: filename: url or filename, id
            parts = re.split(r'[:\t,]', line, maxsplit=1)

            if len(parts) == 2:
                filename = parts[0].strip()
                url_or_id = parts[1].strip()

                # Extract clip_id from filename
                clip_id = filename.replace('.mp4', '').strip()

                self.add_video(clip_id, url_or_id)

    def save_mapping(self, output_file='data/video_mapping.json'):
        """
        Save mapping to JSON file

        Args:
            output_file: Output file path
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.mapping, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Saved {len(self.mapping)} videos to {output_file}")

    def load_existing(self, input_file='data/video_mapping.json'):
        """
        Load existing mapping file

        Args:
            input_file: Existing mapping file
        """
        input_path = Path(input_file)

        if input_path.exists():
            with open(input_path, 'r', encoding='utf-8') as f:
                self.mapping = json.load(f)
            print(f"✓ Loaded {len(self.mapping)} existing mappings")
        else:
            print(f"No existing mapping found at {input_file}")


def interactive_mode():
    """Interactive mode to manually add mappings"""
    print("=" * 60)
    print("Google Drive Manual Mapper - Interactive Mode")
    print("=" * 60)
    print("\nInstructions:")
    print("1. Open your Google Drive folder")
    print("2. For each video file, right-click -> Get link")
    print("3. Paste the link along with the filename below")
    print("\nFormat: filename: link")
    print("Example: DAY5_A3_TASHA_12143000.mp4: https://drive.google.com/file/d/xxx/view")
    print("\nType 'done' when finished, 'save' to save progress")
    print("=" * 60 + "\n")

    mapper = GoogleDriveMapper()

    # Try to load existing mapping
    mapper.load_existing()

    while True:
        user_input = input("\nEnter mapping (or 'done'/'save'): ").strip()

        if user_input.lower() == 'done':
            mapper.save_mapping()
            break
        elif user_input.lower() == 'save':
            mapper.save_mapping()
            continue
        elif not user_input:
            continue

        # Try to parse the input
        parts = re.split(r'[:\t,]', user_input, maxsplit=1)

        if len(parts) == 2:
            filename = parts[0].strip()
            url_or_id = parts[1].strip()

            clip_id = filename.replace('.mp4', '').strip()
            mapper.add_video(clip_id, url_or_id)
        else:
            print("Invalid format. Use: filename: url")

    print(f"\n✓ Complete! {len(mapper.mapping)} videos mapped")


def batch_mode_from_file(input_file):
    """
    Batch mode: read mappings from a text file

    Args:
        input_file: Text file with mappings
    """
    print(f"Reading mappings from: {input_file}")

    mapper = GoogleDriveMapper()

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    mapper.add_from_text(text)
    mapper.save_mapping()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Batch mode from file
        batch_mode_from_file(sys.argv[1])
    else:
        # Interactive mode
        interactive_mode()
