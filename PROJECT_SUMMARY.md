# Project Summary - Video Annotation System

## Overview

This is a clean, production-ready video annotation web application built with Streamlit. The project has been reorganized for clarity and maintainability.

## Current Status

✅ **Fully Functional**
- Main application: OneDrive folder links version
- Alternative version: Google Drive iframe embedding
- All legacy files archived in `deprecated/` folder
- Clean project structure with clear documentation

## Directory Structure

```
egolife-video-annotation/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies (streamlit, pandas, requests)
├── README.md                   # Main documentation (English)
│
├── data/
│   ├── A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json  # 120 questions
│   └── video_mapping.json      # Video ID to Google Drive file ID mapping
│
├── utils/
│   ├── __init__.py
│   ├── data_parser.py          # Question data parsing
│   ├── session_manager.py      # Session state and progress
│   ├── response_recorder.py    # Answer recording and export
│   ├── video_loader_onedrive_folder.py    # Current: OneDrive folder links
│   └── video_loader_external_links.py     # Alternative: Google Drive iframe
│
├── .streamlit/
│   ├── config.toml             # Streamlit UI configuration
│   └── secrets.toml            # Secrets (not in git)
│
├── switch_version.py           # Quick version switching utility
├── VERSION_SWITCHING_GUIDE.md  # How to switch versions
├── ONEDRIVE_FOLDER_SETUP.md    # OneDrive setup instructions
│
└── deprecated/                 # Archived legacy files
    ├── README.md               # Documentation of deprecated files
    ├── utils/                  # Old video loaders
    ├── tools/                  # Old setup tools
    ├── data/                   # Old data files
    └── *.py, *.md, *.bat       # All legacy scripts and docs
```

## Active Features

### Current Version: OneDrive Folder Links

**How it works:**
- For each video, display OneDrive folder link button
- Users click button to open OneDrive in new tab
- Users search for video file using Ctrl+F
- Simple, reliable, no embedding issues

**Files:**
- `utils/video_loader_onedrive_folder.py`
- `config.ONEDRIVE_VIDEO_FOLDER` (OneDrive shared folder URL)

### Alternative Version: Google Drive Iframe

**How it works:**
- Embeds videos directly in page using iframe
- Requires video mapping: clip_id → Google Drive file ID
- More seamless user experience
- May have browser compatibility issues

**Files:**
- `utils/video_loader_external_links.py`
- `data/video_mapping.json` (240 video mappings)

**Switch to this version:**
```bash
python switch_version.py googledrive
git add app.py
git commit -m "Switch to Google Drive version"
git push origin main
```

## Key Configuration

### config.py

```python
# OneDrive folder URL (current version)
ONEDRIVE_VIDEO_FOLDER = "https://adminliveunc-my.sharepoint.com/:f:/g/personal/..."

# Data files
DATA_FILE = "data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json"
RESPONSES_FILE = "data/responses.jsonl"
PROGRESS_FILE = "data/progress.json"

# Auto-save interval
AUTO_SAVE_INTERVAL = 5  # questions
```

## Deployment

### Live Application

**URL:** https://egolife-video-annotation-a9stffvxovjypbfhcbbhnp.streamlit.app/

**Auto-deployment:**
- Hosted on Streamlit Community Cloud
- Connected to GitHub repository
- Auto-updates on every `git push origin main`
- No manual deployment needed

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Access at http://localhost:8501
```

## Version History

### Recent Commits

1. **39c516b** - Reorganize project structure: move legacy files to deprecated/
2. **897b123** - Add automated version switching script
3. **971acb3** - Fix config cache issue and add version switching guide
4. **a5bea42** - Update OneDrive video folder URL
5. **d5d4d69** - Switch to OneDrive folder link approach
6. **f4f2a7f** - Fix video mapping to match question clip_ids

### Version Tags (Recommended)

Create tags for easy version management:

```bash
# Tag current OneDrive version
git tag -a v1.0-onedrive -m "OneDrive folder links version"
git push origin v1.0-onedrive

# Tag Google Drive version (after switching)
git tag -a v1.0-googledrive -m "Google Drive iframe version"
git push origin v1.0-googledrive
```

## Deprecated Files

All legacy files have been moved to `deprecated/` folder:

### Test Files
- test_*.py, demo_*.py

### Migration Tools
- migrate_videos_*.py
- OneDrive_to_GoogleDrive_*.ipynb
- setup_*.py, create_*.py

### Old Video Loaders
- utils/video_loader_auth.py
- utils/video_loader_google_drive.py
- utils/video_loader_onedrive_links.py
- utils/video_loader_simple.py

### Documentation
- All old .md setup guides
- System architecture docs
- Quick reference guides

See `deprecated/README.md` for complete list.

## Data Flow

```
Question Data (JSON)
    ↓
app.py loads questions
    ↓
Display question + video links
    ↓
User watches videos (OneDrive)
    ↓
User selects answer (A/B/C/D)
    ↓
Response saved (JSONL)
    ↓
Progress tracked
    ↓
Export responses
```

## Response Format

Each response in `data/responses.jsonl`:

```json
{
  "sample_id": "altmulti_124",
  "user_answer": "D",
  "correct_answer": "D",
  "is_correct": true,
  "time_spent_seconds": 155.23,
  "timestamp": "2026-03-06T10:30:25",
  "user_id": "annotator_001"
}
```

## Maintenance

### To Update OneDrive Folder

Edit `config.py`:
```python
ONEDRIVE_VIDEO_FOLDER = "your-new-onedrive-url"
```

Commit and push:
```bash
git add config.py
git commit -m "Update OneDrive folder URL"
git push origin main
```

### To Switch Versions

Use the automated script:
```bash
# Switch to OneDrive
python switch_version.py onedrive

# Switch to Google Drive
python switch_version.py googledrive

# Then commit and push
git add app.py
git commit -m "Switch version"
git push origin main
```

### To Add New Questions

1. Update `data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json`
2. Push to GitHub
3. Streamlit Cloud auto-updates

## Support & Documentation

- **Main README**: `README.md` - User guide and setup
- **Version Guide**: `VERSION_SWITCHING_GUIDE.md` - How to switch versions
- **OneDrive Setup**: `ONEDRIVE_FOLDER_SETUP.md` - OneDrive configuration
- **Deprecated Files**: `deprecated/README.md` - Legacy file documentation

## Future Enhancements (Optional)

- [ ] Multi-user authentication
- [ ] Admin dashboard for response monitoring
- [ ] Inter-annotator agreement calculation
- [ ] Video playback controls (speed, frame navigation)
- [ ] Side-by-side video comparison
- [ ] Database integration (Supabase/MongoDB)
- [ ] Google Sheets API for persistent storage

## License

MIT License

## Contact

GitHub: https://github.com/DylanZhao123/egolife-video-annotation
Live App: https://egolife-video-annotation-a9stffvxovjypbfhcbbhnp.streamlit.app/
