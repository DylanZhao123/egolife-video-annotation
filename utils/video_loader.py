"""
Video Loader Module
Handles video URL mapping and loading from OneDrive or local cache
"""

import json
import streamlit as st
from pathlib import Path
import config

class VideoLoader:
    """Manages video loading from OneDrive URLs or local cache"""

    def __init__(self, mapping_file=None):
        """
        Initialize video loader

        Args:
            mapping_file: Path to video mapping JSON file
        """
        if mapping_file is None:
            mapping_file = config.VIDEO_MAPPING_FILE

        self.url_map = self._load_mapping(mapping_file)
        self.cache_dir = Path(config.CACHE_DIR)

    @st.cache_data
    def _load_mapping(_self, mapping_file):
        """
        Load video URL mapping from file

        Args:
            mapping_file: Path to mapping JSON file

        Returns:
            Dictionary mapping clip_id to video URL
        """
        try:
            if Path(mapping_file).exists():
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                st.warning(f"⚠️ Video mapping file not found: {mapping_file}")
                return {}
        except json.JSONDecodeError as e:
            st.error(f"❌ Error parsing video mapping: {e}")
            return {}

    def get_video_url(self, clip_id):
        """
        Get video URL for a clip ID

        Priority:
        1. OneDrive URL from mapping file
        2. Local cache file
        3. None (not found)

        Args:
            clip_id: Video clip ID (e.g., "DAY1_A3_TASHA_11253000")

        Returns:
            Video URL or local file path, or None if not found
        """
        if not clip_id:
            return None

        # Check URL mapping first
        if clip_id in self.url_map:
            return self.url_map[clip_id]

        # Check local cache
        cache_file = self.cache_dir / f"{clip_id}.mp4"
        if cache_file.exists():
            return str(cache_file)

        # Try other video formats
        for ext in ['.mov', '.avi', '.mkv', '.webm']:
            cache_file = self.cache_dir / f"{clip_id}{ext}"
            if cache_file.exists():
                return str(cache_file)

        # Not found
        return None

    def is_video_available(self, clip_id):
        """
        Check if video is available

        Args:
            clip_id: Video clip ID

        Returns:
            True if video is available, False otherwise
        """
        return self.get_video_url(clip_id) is not None

    def get_missing_videos(self, clip_ids):
        """
        Get list of missing videos

        Args:
            clip_ids: List or set of clip IDs

        Returns:
            List of clip IDs that are not available
        """
        return [clip_id for clip_id in clip_ids if not self.is_video_available(clip_id)]

    def add_video_mapping(self, clip_id, video_url):
        """
        Add a new video mapping

        Args:
            clip_id: Video clip ID
            video_url: OneDrive URL or local path
        """
        self.url_map[clip_id] = video_url

    def save_mapping(self, mapping_file=None):
        """
        Save current video mapping to file

        Args:
            mapping_file: Path to save mapping file (optional)
        """
        if mapping_file is None:
            mapping_file = config.VIDEO_MAPPING_FILE

        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(self.url_map, f, indent=2)

        st.success(f"✅ Video mapping saved to {mapping_file}")

def generate_onedrive_direct_link(share_url):
    """
    Convert OneDrive share URL to direct download link

    Args:
        share_url: OneDrive share URL

    Returns:
        Direct download URL
    """
    # OneDrive share URLs can be converted to direct links by adding ?download=1
    if '?' in share_url:
        return f"{share_url}&download=1"
    else:
        return f"{share_url}?download=1"

def extract_clip_id_from_filename(filename):
    """
    Extract clip ID from video filename

    Args:
        filename: Video filename (e.g., "DAY1_A3_TASHA_11253000.mp4")

    Returns:
        Clip ID without extension
    """
    return Path(filename).stem
