"""
OneDrive Video Link Generator
OneDrive视频链接生成器

Generates OneDrive viewing links for videos (requires UNC login)
为视频生成OneDrive查看链接（需要UNC登录）
"""

import streamlit as st


class VideoLoaderOneDriveLinks:
    """Generate OneDrive external links for videos"""

    def __init__(self, base_folder_url=None):
        """
        Initialize OneDrive link generator

        Args:
            base_folder_url: Base OneDrive folder URL
        """
        # UNC OneDrive base URL for video folder
        self.base_url = base_folder_url or "https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/Documents/Egolife_videos"

    def get_video_link(self, clip_id):
        """
        Get OneDrive link for a video

        Args:
            clip_id: Video clip ID (e.g., "DAY1_A3_TASHA_11093015")

        Returns:
            str: OneDrive viewing link
        """
        filename = f"{clip_id}.mp4"

        # Generate OneDrive viewing URL
        # Users will need to login with UNC account to view
        return f"{self.base_url}/{filename}"

    def display_video_link(self, clip_id):
        """
        Display clickable link to OneDrive video

        Args:
            clip_id: Video clip ID
        """
        video_link = self.get_video_link(clip_id)

        st.markdown(f"""
        <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin: 10px 0;">
            <p style="margin: 0 0 5px 0; font-size: 14px; color: #555;">
                🎬 <strong>Video:</strong> {clip_id}
            </p>
            <p style="margin: 0; font-size: 12px; color: #888;">
                ℹ️ Click below to watch video (UNC login required)
            </p>
            <a href="{video_link}" target="_blank" style="
                display: inline-block;
                margin-top: 8px;
                padding: 8px 16px;
                background-color: #0066cc;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            ">
                📹 Open Video in OneDrive
            </a>
        </div>
        """, unsafe_allow_html=True)

    def display_video_link_simple(self, clip_id):
        """
        Display simple text link

        Args:
            clip_id: Video clip ID
        """
        video_link = self.get_video_link(clip_id)

        st.markdown(f"**Video:** [{clip_id}]({video_link}) (Open in OneDrive - UNC login required)")


# For backward compatibility
class VideoLoader(VideoLoaderOneDriveLinks):
    """Alias for backward compatibility"""
    pass
