# AUTOMATED DEPLOYMENT GUIDE

## Current Status: App Running Locally

Your Streamlit app is already running at: **http://localhost:8501**

---

## OPTION 1: Quick Test (No Videos) - 30 seconds

You can test the basic functionality right now without videos:

1. Open: http://localhost:8501
2. See the question interface
3. Test navigation and UI

**Note**: Videos won't play yet (need OneDrive setup)

---

## OPTION 2: Full Setup with Videos - 10 minutes

### Auto-Open All Required Pages

Run this command to automatically open all needed pages:

```bash
python tools/quick_setup.py
```

This will:
1. Open Graph Explorer in your browser
2. Guide you through getting the access token
3. Automatically configure all 240 video links
4. Activate the configuration

---

## OPTION 3: Manual Video Setup - If Auto Fails

If the automated script doesn't work:

```bash
python tools/setup_onedrive_links.py
```

Then follow the on-screen instructions.

---

## After Video Setup is Complete

### Test Locally

Open: http://localhost:8501

Test that:
- [x] Questions load
- [x] Videos play
- [x] Can submit answers
- [x] Navigation works

---

### Deploy to GitHub

I've prepared all the commands for you. Just run these:

```bash
# 1. Create GitHub repo first (do this in browser):
# Go to: https://github.com/new
# Name: video-annotation-system
# Make it Public
# Don't initialize with README

# 2. Then run these commands:
cd "C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite"

# Add your GitHub remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/video-annotation-system.git

# Rename branch to main
git branch -M main

# Push everything
git push -u origin main
```

**After running these, your code will be on GitHub!**

---

### Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Click "Sign in with GitHub"
3. Click "New app"
4. Fill in:
   - Repository: `YOUR-USERNAME/video-annotation-system`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy"

Wait 2-3 minutes and you'll get your public URL!

---

## Quick Command Reference

```bash
# Test locally
python -m streamlit run app.py

# Run automated setup
python tools/quick_setup.py

# Check git status
git status

# Push new changes
git add .
git commit -m "Your message"
git push
```

---

## Need Help?

- Script not working? Check ONEDRIVE_SETUP.md
- GitHub issues? Check DEPLOYMENT.md
- General questions? Check README.md

---

## What's Already Done

[x] Project structure created
[x] All code written
[x] Git repository initialized
[x] App tested and running locally
[x] Documentation complete
[x] Automated scripts ready

## What You Need To Do

[ ] Run automated setup for videos (10 min)
[ ] Create GitHub repository (1 min)
[ ] Push code to GitHub (1 min)
[ ] Deploy to Streamlit Cloud (2 min)

**Total time: ~15 minutes**

---

## Pro Tip

You can skip the video setup initially and deploy without videos first,
then add videos later. The app will work, just videos won't play yet.

This way you can see your app live on Streamlit Cloud immediately!
