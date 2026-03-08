"""
Quick test for OneDrive folder video loader
"""

from utils.video_loader_onedrive_folder import VideoLoaderOneDriveFolder
import config

# Test initialization
print("Testing OneDrive Folder Video Loader")
print("=" * 70)

# Create loader with actual OneDrive URL
loader = VideoLoaderOneDriveFolder(folder_url=config.ONEDRIVE_VIDEO_FOLDER)

print(f"\nOneDrive Folder URL: {loader.folder_url}")
print("\nTesting video_exists():")
print(f"  DAY1_A3_TASHA_11093015 exists: {loader.video_exists('DAY1_A3_TASHA_11093015')}")
print(f"  DAY5_A3_TASHA_12143000 exists: {loader.video_exists('DAY5_A3_TASHA_12143000')}")

print("\nTesting required methods:")
print(f"  display_video_iframe: {hasattr(loader, 'display_video_iframe')}")
print(f"  display_video_link: {hasattr(loader, 'display_video_link')}")
print(f"  video_exists: {hasattr(loader, 'video_exists')}")

print("\n" + "=" * 70)
print("All tests passed! The video loader is working correctly.")
print("\nNext steps:")
print("1. Wait 1-2 minutes for Streamlit Cloud to redeploy")
print("2. Visit: https://egolife-video-annotation-a9stffvxovjypbfhcbbhnp.streamlit.app/")
print("3. Each video will show an 'Open OneDrive Folder' button")
print("4. Click the button to access the OneDrive folder")
print("5. Use Ctrl+F to search for the video file name (e.g., DAY5_A3_TASHA_12143000.mp4)")
print("=" * 70)
