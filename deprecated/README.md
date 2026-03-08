# Deprecated Files

This directory contains files that are no longer used in the main application but are kept for reference and historical purposes.

## Contents

### Test Files
- `test_*.py` - Various testing scripts
- `demo_*.py` - Demo applications

### Migration Tools
- `migrate_videos_*.py` - Video migration scripts
- `OneDrive_*.ipynb` - OneDrive to Google Drive migration notebooks
- `setup_*.py` - Various setup scripts
- `create_*.py` - File creation utilities

### Old Video Loaders
- `utils/video_loader_*.py` - Alternative video loader implementations
  - `video_loader_auth.py` - Authentication-based loader
  - `video_loader_google_drive.py` - Google Drive loader
  - `video_loader_onedrive_links.py` - OneDrive individual links loader
  - `video_loader_simple.py` - Simple loader implementation
  - `google_drive_mapper.py` - Google Drive mapping utility

### Documentation
- Various `.md` files - Old setup guides, deployment docs, and system documentation
- `.txt` files - Quick reference guides and instructions

### Data Files
- `data/` - Temporary data files and old mapping versions

### Tools
- `tools/` - Old setup and generation tools

### Scripts
- `*.bat`, `*.ps1` - Windows batch and PowerShell scripts
- `auto_deploy.py` - Automated deployment script

## Active Files (Not Deprecated)

The main application uses:
- `app.py` - Main Streamlit application
- `config.py` - Configuration
- `requirements.txt` - Dependencies
- `utils/video_loader_onedrive_folder.py` - Current video loader (OneDrive folder links)
- `utils/video_loader_external_links.py` - Google Drive version (for switching)
- `data/video_mapping.json` - Video mapping for Google Drive version
- `data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json` - Question data

## Version Information

- **Current Version**: OneDrive Folder Links
- **Alternative Version**: Google Drive Iframe Embedding (use `switch_version.py` to switch)
