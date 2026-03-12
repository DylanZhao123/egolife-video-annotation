"""
OneDrive Folder Link Video Loader
显示 OneDrive 文件夹链接的视频加载器

Simple approach: Show OneDrive folder link for each video
简单方法：为每个视频显示 OneDrive 文件夹链接
"""

import streamlit as st


class VideoLoaderOneDriveFolder:
    """Display OneDrive folder links for videos"""

    def __init__(self, folder_url=None):
        """
        Initialize OneDrive folder link loader

        Args:
            folder_url: OneDrive folder URL containing all videos
        """
        # Default OneDrive folder URL
        self.folder_url = folder_url or "https://1drv.ms/f/c/1f7d8c8e8c8e8c8e/your-folder-link"

    def display_video_iframe(self, clip_id):
        """
        Display OneDrive folder link for video

        Args:
            clip_id: Video clip ID
        """
        self._display_folder_link(clip_id)

    def display_video_link(self, clip_id):
        """
        Display OneDrive folder link for video

        Args:
            clip_id: Video clip ID
        """
        self._display_folder_link(clip_id)

    def render_video(self, clip_id):
        """
        Render video (alias for display_video_link)

        Args:
            clip_id: Video clip ID
        """
        self._display_folder_link(clip_id)

    def get_video_url(self, clip_id):
        """
        Get video URL (returns folder URL for OneDrive)

        Args:
            clip_id: Video clip ID

        Returns:
            Folder URL
        """
        return self.folder_url

    def is_video_available(self, clip_id):
        """Check if video is available (always True for folder-based)"""
        return True

    def _display_folder_link(self, clip_id):
        """Display folder link with clip information"""
        st.markdown(f"""
        <div style="padding: 16px; background-color: #f8f9fa; border-radius: 8px; margin: 12px 0; border-left: 4px solid #0078D4;">
            <p style="margin: 0 0 8px 0; font-size: 14px; color: #666; font-weight: 500;">
                📹 <strong>Video:</strong> {clip_id}
            </p>
            <p style="margin: 0 0 12px 0; font-size: 13px; color: #888;">
                Please find this video in the OneDrive folder below:
            </p>
            <a href="{self.folder_url}" target="_blank" style="
                display: inline-block;
                padding: 12px 24px;
                background-color: #0078D4;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: all 0.2s;
            " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)';"
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                📂 Open OneDrive Folder
            </a>
            <p style="margin: 12px 0 0 0; font-size: 12px; color: #999;">
                Tip: Use Ctrl+F to search for "<strong>{clip_id}.mp4</strong>" in the folder
            </p>
        </div>
        """, unsafe_allow_html=True)

    def video_exists(self, clip_id):
        """All videos are assumed to exist in the folder"""
        return True


# For backward compatibility
class VideoLoader(VideoLoaderOneDriveFolder):
    """Alias for backward compatibility"""
    pass
