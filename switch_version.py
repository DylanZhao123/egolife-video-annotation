"""
Quick Version Switcher
快速版本切换工具

Usage:
    python switch_version.py onedrive    # 切换到 OneDrive 文件夹版本
    python switch_version.py googledrive # 切换到 Google Drive 嵌入版本
"""

import sys
import re
from pathlib import Path

def switch_to_onedrive():
    """Switch to OneDrive folder version"""
    app_file = Path('app.py')

    # Read current content
    content = app_file.read_text(encoding='utf-8')

    # Replace import statement
    content = re.sub(
        r'from utils\.video_loader_\w+ import \w+ as VideoLoader',
        'from utils.video_loader_onedrive_folder import VideoLoaderOneDriveFolder as VideoLoader',
        content
    )

    # Replace video loader initialization
    # Look for the pattern and replace it
    content = re.sub(
        r'video_loader = VideoLoader\(\)',
        '''onedrive_url = getattr(config, 'ONEDRIVE_VIDEO_FOLDER',
                               "https://adminliveunc-my.sharepoint.com/:f:/g/personal/ziyangw_ad_unc_edu/IgA_aigeKcG-QKDy08QVHEiEARIVaWMqy6UH-1eFP7TijWA?e=aNCstX")
        video_loader = VideoLoader(folder_url=onedrive_url)''',
        content
    )

    # Write back
    app_file.write_text(content, encoding='utf-8')

    print("✓ Switched to OneDrive folder version")
    print("\nChanges made:")
    print("  - Import: video_loader_onedrive_folder.VideoLoaderOneDriveFolder")
    print("  - Initialization: VideoLoader(folder_url=onedrive_url)")
    print("\nNext steps:")
    print("  1. Review changes: git diff app.py")
    print("  2. Commit: git add app.py && git commit -m 'Switch to OneDrive version'")
    print("  3. Push: git push origin main")

def switch_to_googledrive():
    """Switch to Google Drive iframe version"""
    app_file = Path('app.py')

    # Read current content
    content = app_file.read_text(encoding='utf-8')

    # Replace import statement
    content = re.sub(
        r'from utils\.video_loader_\w+ import \w+ as VideoLoader',
        'from utils.video_loader_external_links import VideoLoaderExternalLinks as VideoLoader',
        content
    )

    # Replace video loader initialization
    # Look for multi-line pattern and replace with simple one
    pattern = r"onedrive_url = getattr\(config, 'ONEDRIVE_VIDEO_FOLDER',\s*\"[^\"]+\"\)\s*video_loader = VideoLoader\(folder_url=onedrive_url\)"
    content = re.sub(pattern, 'video_loader = VideoLoader()', content, flags=re.DOTALL)

    # Also handle single line version
    content = re.sub(
        r'video_loader = VideoLoader\(folder_url=.*?\)',
        'video_loader = VideoLoader()',
        content
    )

    # Write back
    app_file.write_text(content, encoding='utf-8')

    print("✓ Switched to Google Drive iframe version")
    print("\nChanges made:")
    print("  - Import: video_loader_external_links.VideoLoaderExternalLinks")
    print("  - Initialization: VideoLoader()")
    print("\nNext steps:")
    print("  1. Review changes: git diff app.py")
    print("  2. Commit: git add app.py && git commit -m 'Switch to Google Drive version'")
    print("  3. Push: git push origin main")
    print("\nNote: Make sure data/video_mapping.json has all video mappings!")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python switch_version.py onedrive    # 切换到 OneDrive 版本")
        print("  python switch_version.py googledrive # 切换到 Google Drive 版本")
        sys.exit(1)

    version = sys.argv[1].lower()

    if version in ('onedrive', 'od'):
        switch_to_onedrive()
    elif version in ('googledrive', 'gd', 'google'):
        switch_to_googledrive()
    else:
        print(f"Unknown version: {version}")
        print("Valid options: onedrive, googledrive")
        sys.exit(1)

if __name__ == '__main__':
    main()
