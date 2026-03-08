# Video Annotation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://egolife-video-annotation-a9stffvxovjypbfhcbbhnp.streamlit.app/)

A web-based video annotation platform for multiple-choice questionnaire (MCQ) evaluation, built with Streamlit.

## Brief Introduction

This application enables annotators to review video evidence and answer multiple-choice questions. It features:

- **Question Navigation**: Browse through 120 questions with progress tracking
- **Video Evidence Display**: View query context and evidence clips via OneDrive
- **Response Recording**: Save answers with timestamps to JSONL format
- **Session Management**: Auto-save progress and resume from last position
- **Export Capability**: Download responses in multiple formats

**Live Demo**: [https://egolife-video-annotation-a9stffvxovjypbfhcbbhnp.streamlit.app/](https://egolife-video-annotation-a9stffvxovjypbfhcbbhnp.streamlit.app/)

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/DylanZhao123/egolife-video-annotation.git
cd egolife-video-annotation

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit `config.py` to set your OneDrive video folder URL:

```python
ONEDRIVE_VIDEO_FOLDER = "your-onedrive-shared-folder-url"
```

### 3. Run Locally

```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

### 4. Deploy to Streamlit Cloud

1. Push to GitHub
2. Visit [Streamlit Cloud](https://share.streamlit.io/)
3. Connect repository and deploy
4. App auto-updates on git push

## User Guidelines

### Annotation Workflow

1. **Enter Annotator ID**: Provide your unique identifier (e.g., `annotator_001`)

2. **Review Question**: Read the question and view available choices

3. **Watch Videos**:
   - Click "Open OneDrive Folder" button
   - Search for video file using Ctrl+F (e.g., `DAY5_A3_TASHA_12143000.mp4`)
   - Watch relevant clips

4. **Select Answer**: Choose the correct option from A/B/C/D

5. **Submit**: Click "Submit Answer" to save and proceed

6. **Navigate**: Use "Previous", "Skip", or jump to specific questions

### Video Access

Videos are hosted on OneDrive. For each video clip:
- Video ID is displayed (e.g., `DAY5_A3_TASHA_12143000`)
- Click "Open OneDrive Folder" to access the shared folder
- Use browser search (Ctrl+F) to find the video by filename
- Videos are organized by person (A3_TASHA, A2_ALICE, A1_JAKE) and day (DAY1-DAY7)

### Progress Tracking

- Progress saves automatically every 5 questions
- View completion status in sidebar
- Jump to any question number
- Session state persists across browser refreshes

### Response Export

- Click "Export Responses" in sidebar
- Download as JSONL (recommended), JSON, or CSV
- Each response includes: question ID, choice, timestamp, annotator ID

## Project Structure

```
egolife-video-annotation/
├── app.py                          # Main application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── data/
│   ├── A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json  # Questions
│   └── video_mapping.json          # Video ID to file mapping (for Google Drive version)
├── utils/
│   ├── data_parser.py              # Question data parsing
│   ├── session_manager.py          # Session state management
│   ├── response_recorder.py        # Answer recording
│   ├── video_loader_onedrive_folder.py    # OneDrive folder links (current)
│   └── video_loader_external_links.py     # Google Drive iframe (alternative)
├── deprecated/                     # Legacy files and old versions
├── switch_version.py               # Version switching utility
└── VERSION_SWITCHING_GUIDE.md      # How to switch between versions
```

## Version Information

**Current Version**: OneDrive Folder Links
- Simple and reliable
- Shows folder link for each video
- Users manually search for video files

**Alternative Version**: Google Drive Iframe Embedding
- Embeds videos directly in page
- Requires video mapping configuration
- Switch using: `python switch_version.py googledrive`

See `VERSION_SWITCHING_GUIDE.md` for details.

## Technical Details

- **Framework**: Streamlit 1.30+
- **Language**: Python 3.8+
- **Data Format**: JSONL for responses, JSON for questions
- **Video Storage**: OneDrive / Google Drive
- **Session State**: In-memory with file persistence

## Configuration Options

Key settings in `config.py`:

```python
# OneDrive folder URL
ONEDRIVE_VIDEO_FOLDER = "https://..."

# Auto-save frequency
AUTO_SAVE_INTERVAL = 5  # questions

# Data files
DATA_FILE = "data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json"
RESPONSES_FILE = "data/responses.jsonl"
```

## Data Format

### Input (Questions)

Questions are loaded from JSON file:

```json
{
  "sample_id": "altmulti_124",
  "query": "Before the last time you saw the bowl...",
  "choices": [
    {"label": "A", "text": "...", "support_clip_id": "..."},
    {"label": "B", "text": "...", "support_clip_id": "..."}
  ],
  "correct_choice": "D",
  "evidence_times": [
    {"clip_id": "DAY1_A3_TASHA_11253000", ...}
  ]
}
```

### Output (Responses)

Responses are saved to `data/responses.jsonl`:

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

## Support

For issues or questions:
- Check `VERSION_SWITCHING_GUIDE.md` for version switching
- See `ONEDRIVE_FOLDER_SETUP.md` for OneDrive configuration
- Review `deprecated/` folder for old documentation and tools

## License

MIT License

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Designed for video annotation research project
