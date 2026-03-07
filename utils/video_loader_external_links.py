"""
External Video Link Generator
外部视频链接生成器

Generates clickable links to view videos externally (Google Drive, OneDrive, etc.)
生成可点击的外部视频查看链接（Google Drive、OneDrive等）
"""

import streamlit as st
import json
from pathlib import Path


class VideoLoaderExternalLinks:
    """Generate external links for videos"""

    def __init__(self, mapping_file="data/video_mapping.json"):
        """
        Initialize external link generator

        Args:
            mapping_file: Path to JSON file with clip_id -> video URL/ID mapping
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

    def get_video_link(self, clip_id):
        """
        Get video viewing link

        Args:
            clip_id: Video clip ID

        Returns:
            str: Video viewing URL or None if not found
        """
        video_ref = self.video_mapping.get(clip_id)

        if not video_ref:
            return None

        # If it's already a full URL, return as is
        if video_ref.startswith('http'):
            return video_ref

        # If it's a Google Drive file ID, generate view URL
        if len(video_ref) == 33 and not '/' in video_ref:  # Google Drive file ID
            return f"https://drive.google.com/file/d/{video_ref}/view"

        return None

    def get_video_url(self, clip_id):
        """
        Get embeddable video URL for st.video()

        Args:
            clip_id: Video clip ID

        Returns:
            str: Video URL suitable for embedding or None if not found
        """
        video_ref = self.video_mapping.get(clip_id)

        if not video_ref:
            return None

        # If it's already a full URL, check if it needs conversion
        if video_ref.startswith('http'):
            # Convert Google Drive view links to embed/preview format
            if 'drive.google.com/file/d/' in video_ref:
                # Extract file ID from URL
                import re
                match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', video_ref)
                if match:
                    file_id = match.group(1)
                    # Return preview URL for embedding
                    return f"https://drive.google.com/file/d/{file_id}/preview"
            return video_ref

        # If it's a Google Drive file ID, generate preview URL
        if len(video_ref) == 33 and not '/' in video_ref:
            return f"https://drive.google.com/file/d/{video_ref}/preview"

        return None

    def display_video_link(self, clip_id):
        """
        Display clickable button to view video externally

        Args:
            clip_id: Video clip ID
        """
        video_link = self.get_video_link(clip_id)

        if not video_link:
            st.info(f"Video not configured: {clip_id}")
            return

        # Determine platform from URL
        if 'drive.google.com' in video_link:
            platform = "Google Drive"
            icon = "🎬"
            color = "#4285F4"  # Google blue
        elif 'sharepoint.com' in video_link or 'onedrive' in video_link.lower():
            platform = "OneDrive"
            icon = "📹"
            color = "#0078D4"  # Microsoft blue
        else:
            platform = "External Link"
            icon = "🔗"
            color = "#0066cc"

        # Display clickable button
        st.markdown(f"""
        <div style="padding: 12px; background-color: #f8f9fa; border-radius: 6px; margin: 8px 0; border-left: 4px solid {color};">
            <p style="margin: 0 0 8px 0; font-size: 13px; color: #666; font-weight: 500;">
                {icon} <strong>Video:</strong> {clip_id}
            </p>
            <a href="{video_link}" target="_blank" style="
                display: inline-block;
                padding: 10px 20px;
                background-color: {color};
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: 600;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.2s;
            " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)';"
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                {icon} Watch on {platform}
            </a>
        </div>
        """, unsafe_allow_html=True)

    def video_exists(self, clip_id):
        """Check if video exists in mapping"""
        return clip_id in self.video_mapping


# For backward compatibility
class VideoLoader(VideoLoaderExternalLinks):
    """Alias for backward compatibility"""
    pass
