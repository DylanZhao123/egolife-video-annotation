# ⚡ Quick Start: Automatic OneDrive Setup

## 🎯 Goal
Automatically generate share links for all 240 videos in 5 minutes.

---

## 📋 Step-by-Step Instructions

### Step 1: Open Graph Explorer (1 minute)

1. Open this link in your browser:
   ```
   https://developer.microsoft.com/en-us/graph/graph-explorer
   ```

2. Click **"Sign in with Microsoft"** (top right corner)

3. Sign in with your UNC email: `ziyangw@ad.unc.edu`

### Step 2: Grant Permissions (1 minute)

1. After signing in, look at the left sidebar

2. Click **"Modify permissions"** (or "Consent to permissions")

3. Find these two permissions and enable them:
   - ✅ `Files.Read.All`
   - ✅ `Files.ReadWrite.All`

4. Click the **"Consent"** button at the bottom

5. A popup will appear asking for permissions - Click **"Accept"**

### Step 3: Copy Access Token (30 seconds)

1. At the top of the page, you'll see several tabs

2. Click the **"Access token"** tab

3. You'll see a very long string of text (starts with "eyJ...")

4. Click the **copy icon** or select all and copy

5. Keep this window open (we'll need it in a moment)

### Step 4: Run the Setup Script (2 minutes)

1. Open your terminal/command prompt

2. Navigate to your project:
   ```bash
   cd "C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite"
   ```

3. Run the setup script:
   ```bash
   python tools/setup_onedrive_links.py
   ```

4. When prompted, paste your access token and press Enter

5. The script will:
   - Connect to your OneDrive
   - Find all videos in `Egolife_videos` folder
   - Generate share links (takes 5-10 minutes for 240 videos)
   - Save to `data/video_mapping_generated.json`

### Step 5: Activate the Mapping (10 seconds)

Once the script finishes:

**Windows:**
```bash
copy data\video_mapping_generated.json data\video_mapping.json
```

**Mac/Linux:**
```bash
cp data/video_mapping_generated.json data/video_mapping.json
```

---

## ✅ You're Done!

All 240 video links are now configured. Next steps:

1. **Test locally:**
   ```bash
   streamlit run app.py
   ```

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add OneDrive video links"
   git push
   ```

3. **Deploy to Streamlit Cloud** (see DEPLOYMENT.md)

---

## 🔍 Visual Guide

### What Graph Explorer Looks Like:

```
┌─────────────────────────────────────────────────────────┐
│  Microsoft Graph Explorer                  [Sign in]    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Modify permissions         │  GET  v                   │
│  ├─ Files.Read.All    ☐    │  https://graph.microsoft │
│  ├─ Files.ReadWrite.All ☐  │                          │
│  └─ [Consent]              │                           │
│                            │                           │
│  [Response] [Access token] [Request headers]           │
│  ┌─────────────────────────────────────────┐          │
│  │ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... │  [Copy]  │
│  └─────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

### What the Script Output Looks Like:

```
============================================================
OneDrive Video Link Setup
============================================================

Fetching folder contents from: Egolife_videos
Found 240 items in folder

Found 240 video files
Need links for 240 clip IDs

[1/240] Processing: DAY1_A3_TASHA_11093015.mp4
  -> Found required clip: DAY1_A3_TASHA_11093015
  -> Link generated successfully

[2/240] Processing: DAY1_A3_TASHA_11113000.mp4
  -> Found required clip: DAY1_A3_TASHA_11113000
  -> Link generated successfully

...

============================================================
Summary
============================================================
Total video files in OneDrive: 240
Required clip IDs: 240
Successfully mapped: 240
Missing: 0

Video mapping saved to: data/video_mapping_generated.json
```

---

## ⚠️ Troubleshooting

### "Token has expired"
**Solution:** The token expires after 1 hour. Go back to Graph Explorer and get a new one.

### "Insufficient privileges"
**Solution:** Make sure you clicked "Consent" after enabling both `Files.Read.All` and `Files.ReadWrite.All`.

### "Folder not found"
**Solution:** Check your folder name. If it's not "Egolife_videos", edit `tools/setup_onedrive_links.py` line 246.

### Script running too long
**Normal!** Processing 240 videos takes 5-10 minutes. Each video takes 1-2 seconds.

### Python not found
**Solution:** Make sure Python is installed. Check with: `python --version`

---

## 💡 Pro Tips

1. **Keep Graph Explorer open** while the script runs in case you need a new token

2. **Run during low activity** - takes 5-10 minutes

3. **Check the summary** at the end to see if any videos are missing

4. **Verify** a few links by opening them in your browser - they should download videos

---

## 📞 Need Help?

If something goes wrong:

1. Read the error message carefully
2. Check the "Troubleshooting" section above
3. See `ONEDRIVE_SETUP.md` for detailed instructions
4. Ask for help with the specific error message

---

## 🎉 Success Checklist

- [ ] Graph Explorer opened and signed in
- [ ] Permissions granted (Files.Read.All, Files.ReadWrite.All)
- [ ] Access token copied
- [ ] Script ran successfully
- [ ] `video_mapping_generated.json` created
- [ ] File copied to `video_mapping.json`
- [ ] App tested locally
- [ ] Ready to deploy!

**Estimated Total Time: 5-15 minutes**
