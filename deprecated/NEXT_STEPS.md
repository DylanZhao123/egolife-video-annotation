# 📋 Next Steps - Video Annotation System

## ✅ Completed Tasks

1. ✅ Git repository initialized
2. ✅ Project structure created
3. ✅ Main Streamlit application built (`app.py`)
4. ✅ Utility modules implemented
5. ✅ Configuration files created
6. ✅ Video mapping template generated (240 unique videos)
7. ✅ Initial commits created
8. ✅ Documentation written

## 🎯 What You Need to Do Next

### Priority 1: Get Video URLs from OneDrive (REQUIRED)

You have **240 video clips** that need OneDrive links. The system has generated a template file with all the clip IDs.

**File to edit**: `data/video_mapping.json`

**Your OneDrive folder**:
https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fziyangw%5Fad%5Func%5Fedu%2FDocuments%2FEgolife%5Fvideos

**Process for each video**:
1. Find the video file in OneDrive (e.g., `DAY1_A3_TASHA_11093015.mp4`)
2. Right-click → "Share"
3. Select "Anyone with the link can view"
4. Copy the share link
5. Add `?download=1` to the end
6. Update the URL in `data/video_mapping.json`

**Example**:
```json
{
  "DAY1_A3_TASHA_11093015": "https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/_layouts/15/download.aspx?share=EaBcDeFg123456&download=1"
}
```

**Tip**: You can start with just a few videos to test the system, then add the rest later.

---

### Priority 2: Push to GitHub

1. **Create a GitHub repository**:
   - Go to https://github.com/new
   - Name: `video-annotation-system` (or your choice)
   - Make it **Public** (required for free Streamlit Cloud)
   - Don't initialize with README

2. **Set remote and push**:
   ```bash
   cd "C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite"

   # Replace YOUR-USERNAME with your GitHub username
   git remote add origin https://github.com/YOUR-USERNAME/video-annotation-system.git

   git branch -M main
   git push -u origin main
   ```

3. **Add the data file** (if you want it in the repo):
   ```bash
   git add data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json
   git commit -m "Add question dataset"
   git push
   ```

---

### Priority 3: Test Locally

Before deploying to Streamlit Cloud, test the app locally:

```bash
cd "C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite"
streamlit run app.py
```

The app will open at `http://localhost:8501`

**What to test**:
- ✅ Questions load correctly
- ✅ Videos play (if you've added OneDrive URLs)
- ✅ Can select answers and submit
- ✅ Progress tracking works
- ✅ Navigation works (next, previous, jump to)
- ✅ Responses are saved to `data/responses.jsonl`

---

### Priority 4: Deploy to Streamlit Cloud

Once everything works locally:

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository**: `your-username/video-annotation-system`
   - **Branch**: `main`
   - **Main file**: `app.py`
5. Click "Deploy!"

Wait 2-3 minutes, then you'll get a public URL like:
`https://your-username-video-annotation-system.streamlit.app`

---

## 📊 Project Statistics

- **Questions**: 120
- **Unique video clips**: 240
- **Files created**: 14
- **Lines of code**: ~1,550
- **Dependencies**: 2 (streamlit, pandas)

---

## 🛠️ Optional Enhancements

After the basic system works, consider:

### Short-term:
- [ ] Add user authentication (simple password protection)
- [ ] Create an admin dashboard to view all responses
- [ ] Add keyboard shortcuts for faster annotation
- [ ] Export summary statistics

### Medium-term:
- [ ] Integrate Google Sheets for persistent storage
- [ ] Add video playback speed controls
- [ ] Implement inter-annotator agreement metrics
- [ ] Add batch import for multiple annotators

### Long-term:
- [ ] Multi-user task assignment system
- [ ] Quality control workflow
- [ ] Side-by-side video comparison
- [ ] Frame-by-frame navigation

---

## 🐛 Common Issues & Solutions

### Issue: "Data file not found"
**Solution**: Make sure `data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json` exists in the `data/` folder

### Issue: "Video not loading"
**Solution**:
1. Check `data/video_mapping.json` has correct URLs
2. Verify OneDrive links end with `?download=1`
3. Test a URL by pasting in browser - it should download the video

### Issue: "Module not found" error
**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: Responses not saving on Streamlit Cloud
**Solution**: Streamlit Cloud doesn't support file persistence. Options:
- Download responses regularly via the "Export" button
- Integrate Google Sheets API
- Use external database (Supabase, MongoDB Atlas)

---

## 📁 Project Structure Overview

```
VidsAnnotaionWebsite/
├── app.py                    # Main application - start here
├── config.py                 # Settings and configuration
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview
├── DEPLOYMENT.md             # Step-by-step deployment guide
├── NEXT_STEPS.md            # This file
│
├── data/
│   ├── A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json  # Questions (120)
│   ├── video_mapping.json                      # Video URLs (YOU NEED TO EDIT THIS)
│   ├── video_mapping_template.json             # Template with all 240 clip IDs
│   ├── responses.jsonl                         # User responses (generated)
│   └── progress.json                           # Session progress (generated)
│
├── utils/
│   ├── data_parser.py        # Load and parse questions
│   ├── video_loader.py       # Video URL management
│   ├── session_manager.py    # Progress tracking
│   └── response_recorder.py  # Save responses
│
└── tools/
    └── generate_video_mapping.py  # Helper to extract clip IDs
```

---

## 🎓 Quick Reference

### Start the app locally:
```bash
streamlit run app.py
```

### Git workflow:
```bash
# Make changes...
git add .
git commit -m "Your message"
git push
```

### Update video URLs:
Edit `data/video_mapping.json`

### View responses:
Open `data/responses.jsonl` in text editor or Excel

### Export responses:
Click "Export Responses" button in the app sidebar

---

## 📞 Getting Help

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Forum**: https://discuss.streamlit.io
- **This Project**: Check `README.md` and `DEPLOYMENT.md`

---

## 🎉 You're Ready!

Your video annotation system is fully built and ready to deploy. The only remaining step is to add your OneDrive video URLs, then push to GitHub and deploy!

Good luck with your annotation project! 🚀
