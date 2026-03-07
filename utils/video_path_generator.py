"""
Video Path Generator
Automatically generates OneDrive paths based on video clip_id naming convention
"""

import re
import json
from pathlib import Path


class VideoPathGenerator:
    """Generate OneDrive paths for videos based on folder structure"""

    def __init__(self, base_url=None):
        """
        Initialize generator with base OneDrive URL

        Args:
            base_url: Base OneDrive URL (e.g., https://adminliveunc-my.sharepoint.com/...)
        """
        self.base_url = base_url or "https://adminliveunc-my.sharepoint.com/:f:/r/personal/ziyangw_ad_unc_edu/Documents/Egolife_videos"

    def parse_clip_id(self, clip_id):
        """
        Parse clip_id to extract day, person, and timestamp

        Format: DAY{day}_{person}_{timestamp}
        Example: DAY5_A3_TASHA_12143000

        Returns:
            dict with 'day', 'person', 'timestamp'
        """
        pattern = r'^DAY(\d+)_(A\d+_[A-Z]+)_(\d+)$'
        match = re.match(pattern, clip_id)

        if not match:
            raise ValueError(f"Invalid clip_id format: {clip_id}")

        return {
            'day': match.group(1),
            'person': match.group(2),
            'timestamp': match.group(3)
        }

    def generate_onedrive_path(self, clip_id):
        """
        Generate OneDrive path for a video clip

        Path structure: Egolife_videos/{person}/DAY{day}/{clip_id}.mp4
        Example: Egolife_videos/A3_TASHA/DAY5/DAY5_A3_TASHA_12143000.mp4

        Args:
            clip_id: Video clip ID (e.g., DAY5_A3_TASHA_12143000)

        Returns:
            str: Full OneDrive URL with download parameter
        """
        try:
            parsed = self.parse_clip_id(clip_id)

            # Build folder path: {person}/DAY{day}
            folder_path = f"{parsed['person']}/DAY{parsed['day']}"

            # Build full file path
            file_path = f"{folder_path}/{clip_id}.mp4"

            # Combine with base URL
            full_url = f"{self.base_url}/{file_path}?download=1"

            return full_url

        except ValueError as e:
            print(f"Warning: {e}")
            return None

    def generate_mapping_file(self, clip_ids, output_file="data/video_mapping.json"):
        """
        Generate video_mapping.json from list of clip IDs

        Args:
            clip_ids: List of video clip IDs
            output_file: Output JSON file path
        """
        mapping = {}

        for clip_id in clip_ids:
            url = self.generate_onedrive_path(clip_id)
            if url:
                mapping[clip_id] = url

        # Save to file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)

        print(f"Generated mapping for {len(mapping)} videos")
        print(f"Saved to: {output_file}")

        return mapping

    def update_existing_mapping(self, mapping_file="data/video_mapping.json"):
        """
        Update existing video_mapping.json with correct folder structure

        Args:
            mapping_file: Path to existing mapping file
        """
        mapping_path = Path(mapping_file)

        if not mapping_path.exists():
            print(f"Mapping file not found: {mapping_file}")
            return {}

        # Load existing mapping
        with open(mapping_path, 'r', encoding='utf-8') as f:
            existing_mapping = json.load(f)

        # Update each entry
        updated_mapping = {}
        for clip_id in existing_mapping.keys():
            new_url = self.generate_onedrive_path(clip_id)
            if new_url:
                updated_mapping[clip_id] = new_url
            else:
                # Keep original if generation fails
                updated_mapping[clip_id] = existing_mapping[clip_id]

        # Save updated mapping
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(updated_mapping, f, indent=2, ensure_ascii=False)

        print(f"Updated {len(updated_mapping)} video paths")
        print(f"Saved to: {mapping_file}")

        return updated_mapping


if __name__ == "__main__":
    # Example usage
    generator = VideoPathGenerator()

    # Test single clip
    test_clip = "DAY5_A3_TASHA_12143000"
    print(f"\nTest clip: {test_clip}")
    print(f"Generated path: {generator.generate_onedrive_path(test_clip)}")

    # Update existing mapping file
    print("\nUpdating video_mapping.json...")
    generator.update_existing_mapping()
