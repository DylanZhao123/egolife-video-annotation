"""
ONE-CLICK DEPLOYMENT
Automatically opens all required pages and guides you through deployment
"""

import webbrowser
import time
import subprocess
import sys
from pathlib import Path

def print_step(step_num, title):
    print("\n" + "="*70)
    print(f"STEP {step_num}: {title}")
    print("="*70)

def open_url(url, delay=2):
    """Open URL and wait"""
    print(f"Opening: {url}")
    webbrowser.open(url)
    time.sleep(delay)

def main():
    print("\n" + "="*70)
    print("     VIDEO ANNOTATION SYSTEM - ONE-CLICK DEPLOYMENT")
    print("="*70)
    print("\nThis script will:")
    print("1. Open your local app (test basic functionality)")
    print("2. Guide you through OneDrive video setup")
    print("3. Help you push to GitHub")
    print("4. Open Streamlit Cloud for deployment")
    print("\nTotal time: ~15 minutes")
    print("="*70 + "\n")

    input("Press ENTER to begin...")

    # Step 1: Open local app
    print_step(1, "Test Local App (Without Videos)")
    print("\n>> Opening local app in your browser...")
    print(">> You can test the UI, navigation, and question loading")
    print(">> Videos won't play yet (we'll set that up next)")

    open_url("http://localhost:8501", delay=3)

    print("\n>> Take a moment to explore the app interface")
    input("Press ENTER when ready to continue...")

    # Step 2: OneDrive setup
    print_step(2, "Setup OneDrive Video Links (Optional but Recommended)")
    print("\n>> This will automatically configure all 240 video links")
    print(">> It takes 5-10 minutes but is MUCH faster than manual setup")

    choice = input("\nDo you want to setup videos now? (y/n): ").strip().lower()

    if choice == 'y':
        print("\n>> Opening Graph Explorer...")
        print("\nFollow these steps:")
        print("  1. Sign in with your UNC email")
        print("  2. Click 'Modify permissions'")
        print("  3. Enable: Files.Read.All and Files.ReadWrite.All")
        print("  4. Click 'Consent' button then 'Accept'")
        print("  5. Click 'Access token' tab")
        print("  6. Copy the token (starts with 'eyJ...')")

        open_url("https://developer.microsoft.com/en-us/graph/graph-explorer", delay=2)

        input("\nPress ENTER after you have the token ready...")

        print("\n>> Running automated setup script...")
        subprocess.run([sys.executable, "tools/quick_setup.py"], cwd=Path(__file__).parent)

        print("\n>> Video setup complete!")
        print(">> Refresh your browser at http://localhost:8501 to see videos playing")

        input("Press ENTER to continue...")
    else:
        print("\n>> Skipping video setup. You can run it later with:")
        print("   python tools/quick_setup.py")

    # Step 3: GitHub
    print_step(3, "Push to GitHub")
    print("\n>> Opening GitHub to create new repository...")
    print("\nIn GitHub:")
    print("  1. Repository name: video-annotation-system")
    print("  2. Make it PUBLIC (required for free Streamlit Cloud)")
    print("  3. Don't initialize with README")
    print("  4. Click 'Create repository'")

    open_url("https://github.com/new", delay=2)

    input("\nPress ENTER after creating the repository...")

    username = input("\nEnter your GitHub username: ").strip()

    if username:
        print("\n>> Run these commands in your terminal:\n")
        print(f"git remote add origin https://github.com/{username}/video-annotation-system.git")
        print("git branch -M main")
        print("git push -u origin main")
        print("\n>> After running these commands, come back here and press ENTER")

        input("\nPress ENTER after pushing to GitHub...")

        print("\n>> Great! Your code is now on GitHub")
    else:
        print("\n>> You can push to GitHub manually later")

    # Step 4: Streamlit Cloud
    print_step(4, "Deploy to Streamlit Cloud")
    print("\n>> Opening Streamlit Cloud...")
    print("\nIn Streamlit Cloud:")
    print("  1. Sign in with your GitHub account")
    print("  2. Click 'New app'")
    print("  3. Repository: your-username/video-annotation-system")
    print("  4. Branch: main")
    print("  5. Main file path: app.py")
    print("  6. Click 'Deploy!'")
    print("\n>> Wait 2-3 minutes for deployment to complete")
    print(">> You'll get a public URL like:")
    print(f"   https://{username}-video-annotation-system.streamlit.app")

    open_url("https://share.streamlit.io", delay=2)

    input("\nPress ENTER after deployment starts...")

    # Summary
    print("\n" + "="*70)
    print("     DEPLOYMENT COMPLETE!")
    print("="*70)
    print("\n Success Checklist:")
    print("  [x] Local app tested")
    if choice == 'y':
        print("  [x] Videos configured")
    else:
        print("  [ ] Videos not configured (you can do this later)")
    if username:
        print("  [x] Code pushed to GitHub")
        print("  [x] Deployment started on Streamlit Cloud")
    else:
        print("  [ ] GitHub push pending")
        print("  [ ] Streamlit Cloud deployment pending")

    print("\n Your app will be live in 2-3 minutes!")
    print(f"\n Public URL: https://{username}-video-annotation-system.streamlit.app")
    print("\n" + "="*70)

    print("\nNext Steps:")
    print("1. Wait for Streamlit Cloud deployment to complete")
    print("2. Share the URL with your annotators")
    print("3. Monitor responses in the Streamlit dashboard")

    if choice != 'y':
        print("\nTo add videos later:")
        print("  python tools/quick_setup.py")
        print("  git add data/video_mapping.json")
        print("  git commit -m 'Add video links'")
        print("  git push")

    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDeployment cancelled.")
        sys.exit(0)
