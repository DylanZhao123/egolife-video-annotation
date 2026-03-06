"""
Quick Setup Script - Automated OneDrive Configuration
Run this to automatically set up all video links
"""

import webbrowser
import time
import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from setup_onedrive_links import OneDriveVideoSetup, get_access_token_interactive
from utils.data_parser import load_questions, extract_clip_ids

def print_banner():
    print("\n" + "="*70)
    print("  VIDEO ANNOTATION SYSTEM - AUTOMATIC SETUP")
    print("="*70 + "\n")

def open_graph_explorer():
    """Open Graph Explorer in browser"""
    print("Opening Microsoft Graph Explorer in your browser...\n")
    time.sleep(1)

    url = "https://developer.microsoft.com/en-us/graph/graph-explorer"

    try:
        webbrowser.open(url)
        print(f">> Opened: {url}\n")
    except:
        print(f">> Please manually open: {url}\n")

    print("=" * 70)
    print("INSTRUCTIONS:")
    print("=" * 70)
    print("1. Sign in with your UNC email (if not already signed in)")
    print("2. Click 'Modify permissions' in the left sidebar")
    print("3. Find and enable these permissions:")
    print("   [ ] Files.Read.All")
    print("   [ ] Files.ReadWrite.All")
    print("4. Click 'Consent' button")
    print("5. Click 'Accept' in the popup")
    print("6. Click 'Access token' tab at the top")
    print("7. Copy the entire token (starts with 'eyJ...')")
    print("=" * 70 + "\n")

def main():
    print_banner()

    base_dir = Path(__file__).parent.parent

    print(">> Loading question data...")
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'
    questions = load_questions(str(data_file))

    if not questions:
        print("ERROR: Could not load questions!")
        return

    # Extract clip IDs
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f">> Loaded {len(questions)} questions")
    print(f">> Found {len(required_clip_ids)} unique video clips needed\n")

    # Open Graph Explorer
    print("STEP 1: Get Access Token")
    print("-" * 70)

    choice = input("Open Graph Explorer now? (y/n): ").strip().lower()

    if choice == 'y':
        open_graph_explorer()
        input("\nPress ENTER after you've completed the steps above...")

    print("\nSTEP 2: Paste Access Token")
    print("-" * 70)
    access_token = input("Paste your access token here: ").strip()

    if not access_token:
        print("\nERROR: No token provided. Exiting.")
        return

    print("\n>> Token received!")

    # Setup client
    print("\nSTEP 3: Generate Video Links")
    print("-" * 70)
    print("This will take 5-10 minutes for 240 videos...")
    print("Please wait...\n")

    client = OneDriveVideoSetup(access_token)
    folder_path = "Egolife_videos"
    output_file = base_dir / 'data' / 'video_mapping_generated.json'

    try:
        mapping = client.setup_video_mapping(folder_path, required_clip_ids, output_file)

        if mapping:
            # Automatically copy to main file
            import shutil
            main_file = base_dir / 'data' / 'video_mapping.json'
            shutil.copy(output_file, main_file)

            print("\n" + "="*70)
            print("SUCCESS! Video links configured!")
            print("="*70)
            print(f"\nGenerated: {output_file}")
            print(f"Activated: {main_file}")
            print(f"\nMapped {len(mapping)} videos successfully!")

            # Test the app
            print("\n" + "="*70)
            print("Next: Test the Application")
            print("="*70)
            print("\nThe app is already running at: http://localhost:8501")
            print("\nOpen this URL in your browser to test the system!")

            return True

    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("- Make sure your token is fresh (less than 1 hour old)")
        print("- Check that you granted the required permissions")
        print("- Verify the folder name is correct: 'Egolife_videos'")
        return False

if __name__ == "__main__":
    success = main()

    if success:
        print("\n" + "="*70)
        print("SETUP COMPLETE!")
        print("="*70)
        print("\nYour video annotation system is ready!")
        print("\nNext Steps:")
        print("  1. Test at: http://localhost:8501")
        print("  2. Push to GitHub (see DEPLOYMENT.md)")
        print("  3. Deploy to Streamlit Cloud")
        print("\n" + "="*70)
