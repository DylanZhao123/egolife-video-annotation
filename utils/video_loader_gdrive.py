"""
Google Drive Video Loader Module
Handles video loading from Google Drive with embedded playback and fallback links
"""

import re
import streamlit as st
from pathlib import Path
import json

class VideoLoaderGDrive:
    """Manages video loading from Google Drive folders."""

    CLIP_PATTERN = re.compile(r'^(DAY\d+_A\d+_[A-Za-z0-9]+)_(\d{8})$', re.IGNORECASE)
    SEGMENT_PATTERN = re.compile(
        r'^(DAY\d+_A\d+_[A-Za-z0-9]+)_(\d{8})_(\d{8})$',
        re.IGNORECASE
    )

    def __init__(self, base_folder_url=None, mapping_file=None):
        """
        Initialize Google Drive video loader

        Args:
            base_folder_url: Base Google Drive folder URL
            mapping_file: Optional JSON file mapping clip_id to specific URLs
        """
        self.base_folder_url = base_folder_url or ""
        self.mapping_file = mapping_file
        self.url_map = self._load_mapping()

        # Build mock local_index for compatibility with new zip logic
        self.local_index = {'direct': {}, 'segments': {}}

    def _load_mapping(self):
        """Load video URL mapping from file if exists"""
        if not self.mapping_file:
            return {}

        try:
            mapping_path = Path(self.mapping_file)
            if mapping_path.exists():
                with open(mapping_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def get_video_url(self, clip_id):
        """
        Get video URL for a clip ID

        Priority:
        1. Specific mapping from mapping file
        2. Base folder URL (fallback)

        Args:
            clip_id: Video clip ID (e.g., "DAY1_A3_TASHA_11253000")

        Returns:
            Video URL or folder URL
        """
        if not clip_id:
            return None

        # Check if we have specific URL mapping
        if clip_id in self.url_map:
            return self.url_map[clip_id]

        # Fallback to base folder
        return self.base_folder_url if self.base_folder_url else None

    def is_video_available(self, clip_id):
        """Check if video is available (always True for folder-based)"""
        return True

    def extract_gdrive_file_id(self, url):
        """
        Extract Google Drive file ID from URL

        Supports formats:
        - https://drive.google.com/file/d/FILE_ID/view
        - https://drive.google.com/open?id=FILE_ID
        """
        if not url:
            return None

        # Pattern 1: /file/d/FILE_ID/
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)

        # Pattern 2: ?id=FILE_ID
        match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)

        return None

    def get_embed_url(self, url):
        """
        Convert Google Drive URL to embeddable format

        Args:
            url: Google Drive URL

        Returns:
            Embeddable URL or None
        """
        file_id = self.extract_gdrive_file_id(url)
        if file_id:
            return f"https://drive.google.com/file/d/{file_id}/preview"
        return None

    def render_video(self, clip_id):
        """
        Render video with Google Drive embed or fallback link

        Args:
            clip_id: Video clip ID
        """
        url = self.get_video_url(clip_id)

        if not url:
            st.warning(f"No video configured for: {clip_id}")
            return

        # Check if this is a specific file URL (has file ID)
        file_id = self.extract_gdrive_file_id(url)

        if file_id:
            # Try to embed the video
            embed_url = self.get_embed_url(url)
            st.markdown(
                f'<iframe src="{embed_url}" width="100%" height="400" frameborder="0" allowfullscreen></iframe>',
                unsafe_allow_html=True
            )
            st.caption(f"📹 {clip_id}")
        else:
            # Folder URL - show link with search instruction
            self._render_folder_link(clip_id, url)

    def _render_folder_link(self, clip_id, folder_url):
        """Render folder link with search instructions"""
        st.markdown(f"""
        <div style="padding: 16px; background-color: #f8f9fa; border-radius: 8px; margin: 12px 0; border-left: 4px solid #4285f4;">
            <p style="margin: 0 0 8px 0; font-size: 14px; color: #666; font-weight: 500;">
                📹 <strong>Video:</strong> {clip_id}
            </p>
            <p style="margin: 0 0 12px 0; font-size: 13px; color: #888;">
                Please find this video in the Google Drive folder below:
            </p>
            <a href="{folder_url}" target="_blank" style="
                display: inline-block;
                padding: 12px 24px;
                background-color: #4285f4;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.2s;
            " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)';"
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                📂 Open Google Drive Folder
            </a>
            <p style="margin: 12px 0 0 0; font-size: 12px; color: #999;">
                Tip: Use Ctrl+F to search for "<strong>{clip_id}.mp4</strong>" in the folder
            </p>
        </div>
        """, unsafe_allow_html=True)

    def add_video_mapping(self, clip_id, video_url):
        """
        Add a new video mapping

        Args:
            clip_id: Video clip ID
            video_url: Google Drive file URL
        """
        self.url_map[clip_id] = video_url

    def save_mapping(self, mapping_file=None):
        """
        Save current video mapping to file

        Args:
            mapping_file: Path to save mapping file (optional)
        """
        if mapping_file is None:
            mapping_file = self.mapping_file

        if mapping_file:
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(self.url_map, f, indent=2, ensure_ascii=False)

# Alias for compatibility
VideoLoader = VideoLoaderGDrive
