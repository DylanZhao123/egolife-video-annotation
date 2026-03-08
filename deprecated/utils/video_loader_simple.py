"""
Simple Video Loader with Direct Access Token
使用直接访问令牌的简单视频加载器

For testing purposes - uses access token directly
用于测试目的 - 直接使用访问令牌
"""

import requests
from pathlib import Path
from datetime import datetime, timedelta
import streamlit as st

class VideoLoaderSimple:
    """Load videos from OneDrive using direct access token"""

    def __init__(self):
        self.cache_dir = Path('cache')
        self.cache_dir.mkdir(exist_ok=True)

        # Get access token from secrets
        self.access_token = None

        if hasattr(st, 'secrets') and 'onedrive' in st.secrets:
            self.access_token = st.secrets['onedrive'].get('access_token')

        # Cache for video URLs (valid for 50 minutes)
        self.url_cache = {}
        self.url_cache_expires = {}

        # Folder path in OneDrive
        self.folder_path = "Egolife_videos"

    def get_video_url(self, clip_id):
        """Get streaming URL for a video clip"""

        # Check cache first
        if clip_id in self.url_cache:
            if datetime.now() < self.url_cache_expires.get(clip_id, datetime.now()):
                return self.url_cache[clip_id]

        # Check local cache
        cache_file = self.cache_dir / f"{clip_id}.mp4"
        if cache_file.exists():
            return str(cache_file)

        # Get URL from OneDrive
        if self.access_token:
            try:
                url = self._get_onedrive_url(clip_id)

                if url:
                    # Cache URL for 50 minutes
                    self.url_cache[clip_id] = url
                    self.url_cache_expires[clip_id] = datetime.now() + timedelta(minutes=50)
                    return url

            except Exception as e:
                print(f"Error getting OneDrive URL for {clip_id}: {e}")

        # Fallback: video not configured
        return None

    def _get_onedrive_url(self, clip_id):
        """Get video download URL from OneDrive using Graph API"""

        # Video filename
        filename = f"{clip_id}.mp4"

        # Build Graph API URL
        url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{self.folder_path}/{filename}"

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                file_data = response.json()

                # Get download URL
                download_url = file_data.get('@microsoft.graph.downloadUrl')

                if download_url:
                    return download_url

                # Alternative: use content URL
                if 'id' in file_data:
                    file_id = file_data['id']
                    content_url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"

                    # Need to add authorization header
                    return content_url

            elif response.status_code == 404:
                # File not found
                print(f"Video not found in OneDrive: {filename}")
                return None

            elif response.status_code == 401:
                # Unauthorized - token expired
                print(f"⚠️ Access token expired! Please refresh.")
                return None

            else:
                print(f"Error accessing file: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None

        except Exception as e:
            print(f"Exception getting OneDrive URL: {e}")
            return None
