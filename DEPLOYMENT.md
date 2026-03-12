# Deployment Guide for Video Annotation System

## ✅ Deployment Status

**GitHub Repository**: https://github.com/DylanZhao123/egolife-video-annotation
**Streamlit Cloud**: https://egolife-video-annotation-a9stffvxovjypbfhcbbhnp.streamlit.app/
**Latest Commit**: d849ccf - Smart video path resolution with auto-matching

---

## 🎯 New Features

### 1. **Smart Video Path Resolution** ⭐ NEW
- Automatic parsing of clip_id format (e.g., `DAY1_A3_TASHA_14143000`)
- Displays precise navigation path: `A3_TASHA → DAY1 → DAY1_A3_TASHA_14143000.mp4`
- No manual URL mapping required for basic navigation
- Works with Google Drive folder structure automatically

### 2. Video Source Toggle
- **Toggle Button** in sidebar to switch between:
  - **Google Drive**: 30-second clips with smart path hints
  - **OneDrive**: Full videos (folder link for searching)

### 2. Advanced Evidence System
- **Three Evidence Groups**:
  - Query Evidence (find anchor moment)
  - Correct Option Evidence (verify ground truth)
  - Distractor Evidence (check incorrect options)
- Each with annotation guidance

### 3. Download Functionality
- Export responses to server
- Download button appears after export
- JSONL format with timestamp

### 4. Multi-Dataset Support
- Dynamic dataset detection from JSON
- Per-dataset response files
- User and dataset filtering

---

## 🚀 Streamlit Cloud Deployment

### Auto-Deployment
Streamlit Cloud is configured to auto-deploy from the `main` branch. The latest push will trigger automatic redeployment.

### Manual Trigger (if needed)
1. Go to https://share.streamlit.io/
2. Login with your account
3. Find "egolife-video-annotation" app
4. Click "Reboot" if auto-deploy doesn't trigger

### Expected Deployment Time
- Usually 2-5 minutes after push
- Check deployment logs in Streamlit Cloud dashboard

---

## 📋 Configuration

### Video Sources
Both sources are pre-configured in `config.py`:

```python
# Google Drive (30s clips)
GDRIVE_BASE_FOLDER = "https://drive.google.com/drive/folders/1DoVComPUp4juZ9tNFF7EhYYEXlkkBI6K?usp=sharing"

# OneDrive (Full videos)
ONEDRIVE_VIDEO_FOLDER = "https://adminliveunc-my.sharepoint.com/:f:/g/personal/ziyangw_ad_unc_edu/IgA_aigeKcG-QKDy08QVHEiEARIVaWMqy6UH-1eFP7TijWA?e=aNCstX"
```

### Video Mapping (Optional)
To enable embedded Google Drive videos, create `data/video_mapping.json`:

```json
{
  "DAY1_A3_TASHA_11103500": "https://drive.google.com/file/d/YOUR_FILE_ID/view",
  "DAY1_A1_JAKE_10203000": "https://drive.google.com/file/d/ANOTHER_FILE_ID/view"
}
```

Videos with mappings will be embedded; others show folder links.

---

## 🧪 Testing Checklist

After deployment, verify:

- [ ] Video source toggle works (sidebar)
- [ ] Google Drive shows folder links
- [ ] OneDrive shows folder links
- [ ] Evidence groups display correctly (3 sections)
- [ ] Upload JSON file works
- [ ] Export responses button works
- [ ] Download responses button appears and downloads JSONL
- [ ] Navigation (Previous/Next/Skip) works
- [ ] Progress saving works
- [ ] Annotation guidelines display

---

## 📊 Usage Instructions for Annotators

### 1. Select Video Source
- In sidebar, choose between:
  - **Google Drive** (recommended for 30s clips)
  - **OneDrive** (for full videos)

### 2. Load Data
- Use default JSON path, or
- Upload custom JSON file

### 3. Annotate
- Review **Query Evidence** first
- Check **Correct Option Evidence**
- Verify **Distractor Evidence**
- Fill in verification form
- Submit

### 4. Export Results
- Click **📥 Export Responses**
- Click **⬇️ Download Responses**
- Save JSONL file to your computer

---

## 🔧 Troubleshooting

### Videos Not Loading
- Check video source toggle matches your data
- For Google Drive: verify folder URL is accessible
- For OneDrive: verify folder URL is accessible

### Download Not Working
- Must click Export first, then Download appears
- Download button has timestamp key to prevent duplicates

### Deployment Failed
- Check Streamlit Cloud logs for errors
- Verify all dependencies in `requirements.txt`
- Check file permissions in repository

---

## 📝 Future Enhancements

### When Video Upload Completes
1. Create `data/video_mapping.json` with file IDs
2. Videos will auto-embed instead of showing folder links
3. Better user experience with inline playback

### Potential Features
- Bulk upload multiple JSON files
- Export to CSV format
- Progress visualization dashboard
- Annotation statistics per user

---

## 🆘 Support

**Issues**: https://github.com/DylanZhao123/egolife-video-annotation/issues
**Contact**: Check repository for maintainer info

---

Last Updated: 2026-03-12
Version: 2.0.0 - Advanced Annotation UI
