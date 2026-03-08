"""
Google Drive Video Loader (Preview Mode)
Google Drive视频加载器（预览模式）

Uses preview URLs that don't allow direct download
使用不允许直接下载的预览URL
"""

import streamlit as st
import json
from pathlib import Path


class VideoLoaderGoogleDrive:
    """Load videos from Google Drive using public preview URLs"""

    def __init__(self, mapping_file="data/video_mapping.json"):
        """
        Initialize Google Drive video loader

        Args:
            mapping_file: Path to JSON file with clip_id -> Google Drive file_id mapping
        """
        self.mapping_file = Path(mapping_file)
        self.video_mapping = self._load_mapping()

    def _load_mapping(self):
        """Load video mapping from JSON file"""
        if not self.mapping_file.exists():
            st.error(f"Video mapping file not found: {self.mapping_file}")
            return {}

        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Failed to load video mapping: {e}")
            return {}

    def get_video_url(self, clip_id):
        """
        Get Google Drive direct download URL for a video

        Args:
            clip_id: Video clip ID (e.g., "P01_01_frame_0000081600")

        Returns:
            str: Google Drive direct download URL or None if not found
        """
        file_id = self.video_mapping.get(clip_id)

        if not file_id:
            return None

        # Use direct download URL (works with st.video())
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    def display_video(self, clip_id, width=640, height=480):
        """
        Display video using Google Drive preview (no download button)

        Args:
            clip_id: Video clip ID
            width: Video width in pixels
            height: Video height in pixels
        """
        video_url = self.get_video_url(clip_id)

        if not video_url:
            st.error(f"Cannot display video: {clip_id}")
            return

        # Method 1: Embedded iframe (NO download button)
        st.markdown(f"""
        <iframe
            src="{video_url}"
            width="{width}"
            height="{height}"
            allow="autoplay"
            frameborder="0"
            allowfullscreen>
        </iframe>
        """, unsafe_allow_html=True)

        # Display video info
        st.caption(f"Video: {clip_id}")

    def display_video_native(self, clip_id):
        """
        Display video using Streamlit's native video player
        NOTE: This method ALLOWS download via browser

        Args:
            clip_id: Video clip ID
        """
        file_id = self.video_mapping.get(clip_id)

        if not file_id:
            st.error(f"Video not found: {clip_id}")
            return

        # Use direct download URL for st.video()
        # WARNING: This allows users to download video via browser
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        try:
            st.video(download_url)
            st.caption(f"Video: {clip_id}")
        except Exception as e:
            st.error(f"Failed to load video: {e}")

    def get_all_clip_ids(self):
        """Get list of all available clip IDs"""
        return list(self.video_mapping.keys())

    def video_exists(self, clip_id):
        """Check if video exists in mapping"""
        return clip_id in self.video_mapping


# Example usage
if __name__ == "__main__":
    st.title("Google Drive Video Loader Test")

    loader = VideoLoaderGoogleDrive()

    st.write(f"Total videos in mapping: {len(loader.get_all_clip_ids())}")

    # Test with example clip
    test_clip = "test_video"  # Replace with actual clip_id

    if st.button("Test Video (Preview Mode - No Download)"):
        loader.display_video(test_clip, width=800, height=600)

    if st.button("Test Video (Native Player - Allows Download)"):
        loader.display_video_native(test_clip)
