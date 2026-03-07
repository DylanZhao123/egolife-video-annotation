"""
Configuration file for Video Annotation System
"""

from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
CACHE_DIR = BASE_DIR / 'cache'
UTILS_DIR = BASE_DIR / 'utils'

# Data files
DATA_FILE = DATA_DIR / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'
VIDEO_MAPPING_FILE = DATA_DIR / 'video_mapping.json'
RESPONSES_FILE = DATA_DIR / 'responses.jsonl'
PROGRESS_FILE = DATA_DIR / 'progress.json'

# Application settings
APP_TITLE = "Video Annotation System"
APP_ICON = "🎬"
PAGE_LAYOUT = "wide"

# Video settings
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']

# Session settings
AUTO_SAVE_INTERVAL = 5  # Auto-save progress every N questions
SHOW_FEEDBACK_DELAY = 2  # Seconds to show feedback before advancing

# OneDrive settings (optional)
ONEDRIVE_BASE_URL = "https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu"
# OneDrive folder containing all videos
ONEDRIVE_VIDEO_FOLDER = "https://adminliveunc-my.sharepoint.com/:f:/g/personal/ziyangw_ad_unc_edu/IgA_aigeKcG-QKDy08QVHEiEARIVaWMqy6UH-1eFP7TijWA?e=aNCstX"

# UI customization
THEME_PRIMARY_COLOR = "#4CAF50"
THEME_BACKGROUND_COLOR = "#FFFFFF"
THEME_SECONDARY_BACKGROUND_COLOR = "#F0F2F6"

# Export settings
EXPORT_FORMATS = ['jsonl', 'json', 'csv']
DEFAULT_EXPORT_FORMAT = 'jsonl'

# Development settings
DEBUG_MODE = False
SHOW_SAMPLE_IDS = True
SHOW_CORRECT_ANSWERS = False  # Set to True for testing
