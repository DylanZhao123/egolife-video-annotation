"""
AUTO DEPLOYMENT - Opens all required pages
Run this and follow the pages that open
"""

import webbrowser
import time

print("\n" + "="*70)
print("  AUTO DEPLOYMENT - Opening all required pages...")
print("="*70 + "\n")

time.sleep(2)

# 1. Local app
print("[1/4] Opening local app...")
webbrowser.open("http://localhost:8501")
time.sleep(3)

# 2. Graph Explorer
print("[2/4] Opening Graph Explorer for OneDrive...")
webbrowser.open("https://developer.microsoft.com/en-us/graph/graph-explorer")
time.sleep(3)

# 3. GitHub new repo
print("[3/4] Opening GitHub to create repository...")
webbrowser.open("https://github.com/new")
time.sleep(3)

# 4. Streamlit Cloud
print("[4/4] Opening Streamlit Cloud...")
webbrowser.open("https://share.streamlit.io")
time.sleep(2)

print("\n" + "="*70)
print("  ALL PAGES OPENED!")
print("="*70)
print("\nFollow these tabs in your browser:\n")

print("TAB 1: Local App (http://localhost:8501)")
print("  >> Test the interface without videos\n")

print("TAB 2: Graph Explorer")
print("  >> Sign in with UNC email")
print("  >> Modify permissions: Files.Read.All, Files.ReadWrite.All")
print("  >> Click 'Consent' then 'Accept'")
print("  >> Click 'Access token' and copy it")
print("  >> Then run: python tools/quick_setup.py\n")

print("TAB 3: GitHub New Repository")
print("  >> Name: video-annotation-system")
print("  >> Public repository")
print("  >> Don't initialize with README")
print("  >> Create repository")
print("  >> Then run these commands:")
print("     git remote add origin https://github.com/YOUR-USERNAME/video-annotation-system.git")
print("     git branch -M main")
print("     git push -u origin main\n")

print("TAB 4: Streamlit Cloud")
print("  >> Sign in with GitHub")
print("  >> New app")
print("  >> Select your repository")
print("  >> Main file: app.py")
print("  >> Deploy!\n")

print("="*70)
print("\nEstimated time: 15 minutes")
print("="*70 + "\n")
