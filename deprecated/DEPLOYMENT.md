# 🚀 Deployment Guide

## Quick Start: Push to GitHub and Deploy

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the "+" icon in the top right → "New repository"
3. Fill in:
   - **Repository name**: `video-annotation-system` (or your preferred name)
   - **Description**: Video annotation system for EgoLife dataset
   - **Visibility**: Public (required for free Streamlit Cloud)
4. **DO NOT** initialize with README (we already have one)
5. Click "Create repository"

### Step 2: Push Code to GitHub

GitHub will show you commands. Run these in your project directory:

```bash
# Set remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/video-annotation-system.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

Example:
```bash
cd "C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite"
git remote add origin https://github.com/your-username/video-annotation-system.git
git branch -M main
git push -u origin main
```

### Step 3: Add Your Data File (Optional)

If you want to include the question data in the repository:

```bash
git add data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json
git commit -m "Add question dataset"
git push
```

**Note**: The data file is 630KB, which is acceptable for GitHub. However, if you have concerns about making it public, you can:
- Keep it out of the repo
- Upload directly to Streamlit Cloud secrets
- Use a private repository (requires Streamlit paid plan)

### Step 4: Configure Video URLs

You need to get OneDrive direct download links for your videos:

#### Option A: Manual Configuration

1. Go to your OneDrive folder: https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fziyangw%5Fad%5Func%5Fedu%2FDocuments%2FEgolife%5Fvideos

2. For each video:
   - Right-click → "Share"
   - Select "Anyone with the link can view"
   - Copy the share link
   - Add `?download=1` to the end

3. Edit `data/video_mapping.json` with the URLs

Example:
```json
{
  "DAY1_A3_TASHA_11093015": "https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/_layouts/15/download.aspx?share=XXXXX&download=1",
  "DAY1_A3_TASHA_11113000": "https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/_layouts/15/download.aspx?share=YYYYY&download=1"
}
```

#### Option B: Batch Script (Advanced)

You can create a script to batch-generate share links using Microsoft Graph API.

### Step 5: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in:
   - **Repository**: `your-username/video-annotation-system`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy!"

Wait 2-3 minutes for deployment to complete.

### Step 6: Access Your App

Once deployed, you'll get a URL like:
```
https://your-username-video-annotation-system.streamlit.app
```

Share this URL with your annotators!

## Keeping GitHub in Sync

### After Making Changes

```bash
# Check what files changed
git status

# Add changed files
git add <file1> <file2>

# Or add all changes
git add .

# Commit with a message
git commit -m "Description of changes"

# Push to GitHub
git push
```

Streamlit Cloud will automatically redeploy when you push changes.

## Troubleshooting

### Videos Not Loading

1. Check that video URLs in `data/video_mapping.json` are correct
2. Verify URLs end with `?download=1`
3. Test a video URL by pasting it in your browser - it should download
4. Make sure OneDrive links are set to "Anyone with link can view"

### App Crashes on Startup

1. Check the Streamlit Cloud logs (click "Manage app" → "Logs")
2. Common issues:
   - Missing data file: Add it to the repo or upload via secrets
   - Import errors: Check `requirements.txt` includes all dependencies
   - File path issues: Use relative paths, not absolute

### Data Not Persisting

Streamlit Cloud doesn't support file persistence. Solutions:
1. Use Google Sheets API (recommended)
2. Use a database (Supabase, MongoDB Atlas)
3. Download responses regularly from the app

## Advanced: Using Secrets

If you need to store sensitive data (API keys, credentials):

1. In Streamlit Cloud, go to "Manage app" → "Settings" → "Secrets"
2. Add secrets in TOML format:

```toml
# .streamlit/secrets.toml
ONEDRIVE_API_KEY = "your-api-key"
DATABASE_URL = "your-database-url"
```

3. Access in code:
```python
import streamlit as st
api_key = st.secrets["ONEDRIVE_API_KEY"]
```

## Monitoring Usage

Streamlit Cloud provides:
- Real-time viewer count
- App activity logs
- Resource usage metrics

Access via "Manage app" in the Streamlit Cloud dashboard.

## Updating the App

To update your app:

```bash
# Make changes to your code
# ...

# Commit and push
git add .
git commit -m "Update: describe your changes"
git push
```

Streamlit Cloud will automatically detect the push and redeploy within 1-2 minutes.

## Getting Help

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Forum: https://discuss.streamlit.io
- GitHub Issues: Create an issue in your repository
