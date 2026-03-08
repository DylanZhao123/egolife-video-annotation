"""
Video Loader with OAuth Authentication
带OAuth认证的视频加载器

Uses service account credentials to access OneDrive videos without user login
使用服务账户凭证访问OneDrive视频，用户无需登录
"""

import requests
import json
from pathlib import Path
from datetime import datetime, timedelta
import streamlit as st

class OneDriveAuthenticator:
    """Handle OneDrive OAuth authentication"""

    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

        self.access_token = None
        self.token_expires_at = None

        self.token_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    def get_access_token(self):
        """Get valid access token (refresh if expired)"""

        # Check if we have a valid token
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token

        # Token expired or doesn't exist, refresh it
        return self._refresh_access_token()

    def _refresh_access_token(self):
        """Use refresh token to get new access token"""

        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
            'scope': 'Files.Read.All offline_access'
        }

        try:
            response = requests.post(self.token_endpoint, data=data)

            if response.status_code == 200:
                token_data = response.json()

                self.access_token = token_data['access_token']

                # Set expiration (with 5-minute buffer)
                expires_in = token_data.get('expires_in', 3600)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)

                return self.access_token
            else:
                raise Exception(f"Failed to refresh token: {response.status_code} - {response.text}")

        except Exception as e:
            raise Exception(f"Error refreshing access token: {e}")

class VideoLoaderAuth:
    """Load videos from OneDrive using service account authentication"""

    def __init__(self):
        self.cache_dir = Path('cache')
        self.cache_dir.mkdir(exist_ok=True)

        # Initialize authenticator from secrets
        self.authenticator = None

        if hasattr(st, 'secrets') and 'onedrive' in st.secrets:
            self.authenticator = OneDriveAuthenticator(
                client_id=st.secrets['onedrive']['client_id'],
                client_secret=st.secrets['onedrive']['client_secret'],
                refresh_token=st.secrets['onedrive']['refresh_token']
            )

        # Cache for video URLs (valid for 50 minutes)
        self.url_cache = {}
        self.url_cache_expires = {}

        # Folder information
        self.folder_id = None
        self.folder_path = "Egolife_videos"  # Folder name in OneDrive

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
        if self.authenticator:
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

        # Get access token
        access_token = self.authenticator.get_access_token()

        if not access_token:
            return None

        # Video filename
        filename = f"{clip_id}.mp4"

        # Build Graph API URL
        # First, we need to find the file in the shared folder
        # For simplicity, we'll search for it

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Search for the file
        search_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{self.folder_path}/{filename}"

        try:
            response = requests.get(search_url, headers=headers)

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
                    return content_url

            elif response.status_code == 404:
                # File not found
                print(f"Video not found in OneDrive: {filename}")
                return None

            else:
                print(f"Error accessing file: {response.status_code}")
                return None

        except Exception as e:
            print(f"Exception getting OneDrive URL: {e}")
            return None

    def get_folder_files(self):
        """List all files in the OneDrive folder (for bulk operations)"""

        if not self.authenticator:
            return []

        access_token = self.authenticator.get_access_token()

        if not access_token:
            return []

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        folder_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{self.folder_path}:/children"

        try:
            response = requests.get(folder_url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                files = data.get('value', [])

                return [
                    {
                        'name': f['name'],
                        'id': f['id'],
                        'size': f.get('size', 0),
                        'download_url': f.get('@microsoft.graph.downloadUrl')
                    }
                    for f in files
                    if f.get('file')  # Only files, not folders
                ]

            else:
                print(f"Error listing folder: {response.status_code}")
                return []

        except Exception as e:
            print(f"Exception listing folder: {e}")
            return []

    @staticmethod
    @st.cache_data(ttl=3000)  # Cache for 50 minutes
    def _cached_get_url(clip_id, access_token, folder_path):
        """Cached version of URL retrieval"""

        filename = f"{clip_id}.mp4"

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        search_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{folder_path}/{filename}"

        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            file_data = response.json()
            return file_data.get('@microsoft.graph.downloadUrl')

        return None
