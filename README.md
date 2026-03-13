# Video Annotation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://egolife-video-annotation.streamlit.app/)

A web-based video annotation platform for multiple-choice questionnaire (MCQ) evaluation and human verification, built with Streamlit.

## 🚀 Live Demo

**Access the app here**: [https://egolife-video-annotation.streamlit.app/](https://egolife-video-annotation.streamlit.app/)

## 📋 Latest Updates (March 2026)

- ✅ Google Drive 30s video clips support (primary source)
- ✅ OneDrive full-length video support (alternative)
- ✅ JSON file upload for custom annotation tasks
- ✅ Human verification workflow with quality checks
- ✅ Enhanced evidence display with temporal metadata
- ✅ Auto-resume from last annotated question
- ✅ Comprehensive deployment documentation

## Brief Introduction

This application enables annotators to review video evidence and perform human verification of machine-generated questions. It features:

- **Dual Video Sources**: Google Drive (30s clips) or OneDrive (full videos)
- **Evidence Organization**: Structured display of Query/Correct/Distractor evidence
- **Human Verification**: Quality assessment with detailed feedback options
- **Flexible JSON Upload**: Support multiple annotation task formats
- **Session Management**: Auto-save progress and exact resume from last question
- **Export & Download**: Save responses in JSONL format with download button
- **Temporal Metadata**: Display timestamps, day/time info, and clip positions

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

The app supports two video sources (configurable in the sidebar):

#### Google Drive (Default - Recommended)
- 30-second video clips
- Faster loading
- Pre-configured in `config.py`:

```python
GDRIVE_BASE_FOLDER = "https://drive.google.com/drive/folders/..."
VIDEO_MAPPING_FILE = DATA_DIR / 'video_mapping.json'
```

#### OneDrive (Alternative)
- Full-length videos (2-hour segments)
- Edit `config.py`:

```python
ONEDRIVE_VIDEO_FOLDER = "your-onedrive-shared-folder-url"
```

### 3. Run Locally

```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

### 4. Test JSON Compatibility

Before using a new JSON file, test its compatibility:

```bash
python test_json_compatibility.py
```

This validates:
- Required fields (sample_id, query, choices, correct_choice)
- Evidence structure (evidence_times, query_time)
- Choice format (labels, text, support_clip_id)
- Overall data format

### 5. Deploy to Streamlit Cloud

See detailed instructions in `DEPLOYMENT.md`:

1. Push code to GitHub
2. Visit [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your repository: `DylanZhao123/egolife-video-annotation`
4. Set main file: `app.py`
5. Deploy and get your URL

App auto-updates on every git push.

## User Guidelines

### Human Verification Workflow

1. **Setup**:
   - Enter Annotator ID (e.g., `annotator_001`)
   - Select video source (Google Drive or OneDrive)
   - Upload JSON file or use default dataset

2. **Review Evidence**:
   - **Query Evidence**: View the anchor moment/scene
   - **Correct Option Evidence**: Check ground truth support
   - **Distractor Evidence**: Verify why distractors are incorrect

3. **Evaluate Question**:
   - **Query Quality**: Rate clarity and answerability
   - **Query Action**: Keep original / Revise / Reject
   - **Generated Answer**: Verify correctness
   - **Options Quality**: Assess distractor quality
   - **Observed Issues**: Flag specific problems
   - **Overall Decision**: Accept / Revise / Reject

4. **Submit Verification**: Click "Submit Verification" to save and advance

5. **Navigate**: Use "Previous", "Skip", or jump to specific questions

### Video Access

#### Google Drive (Primary)
- Videos embedded directly in the app
- 30-second clips for each evidence item
- Automatic video loading from mapping file
- Format: `DAYx_IDENTITY_HHMMSSFF.mp4`

#### OneDrive (Alternative)
- Full-length videos (2-hour segments)
- Click "Open OneDrive Folder" to access
- Use browser search (Ctrl+F) to find clips
- Videos organized by person and day

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

Questions are loaded from JSON file. Supported formats:

#### Format 1: Entity Memory Annotation (Current)
```json
{
  "sample_id": "A3_TASHA_q_00027",
  "query": "Earlier, I noticed a case in this scene: 'I reached out toward...'",
  "query_time": "DAY1_A3_TASHA_14143000",
  "raw_query_time": "Day1_14:14:30",
  "query_type": "object_reidentification",
  "difficulty_tier": "hard",
  "difficulty_score": 20.0,
  "correct_choice": "E",
  "choices": [
    {
      "label": "A",
      "text": "Day 2 morning: case was visible. Scene cue: ...",
      "event_id": "obj_00010"
    }
  ],
  "evidence_times": [
    {
      "clip_id": "DAY1_A3_TASHA_11103500",
      "object_snapshot": {
        "object_name": "case",
        "location": "",
        "status": ["closed"]
      },
      "dense_caption_context": ["i reached out toward..."],
      "timestamp_sec": 40235.0,
      "start_sec": 40220.0,
      "end_sec": 40250.0,
      "source_role": "distractor_evidence"
    }
  ]
}
```

#### Format 2: Legacy MCQ Format
```json
{
  "sample_id": "altmulti_124",
  "query": "Before the last time you saw the bowl...",
  "choices": [
    {"label": "A", "text": "...", "support_clip_id": "..."}
  ],
  "correct_choice": "D"
}
```

See `test_json_compatibility.py` for format validation.

### Output (Responses)

Responses are saved to `data/responses_{user_id}.jsonl` with human verification data:

```json
{
  "sample_id": "A3_TASHA_q_00027",
  "question_uid": "A3_TASHA_q_00027",
  "question_index": 0,
  "dataset_id": "abc123def456",
  "user_answer": null,
  "correct_answer": "E",
  "is_correct": null,
  "time_spent_seconds": 145.67,
  "timestamp": "2026-03-13T10:30:25",
  "user_id": "annotator_001",
  "human_verification": {
    "query_quality": "Good query (clear and answerable)",
    "query_action": "Keep original query",
    "original_query": "Earlier, I noticed a case...",
    "revised_query": "",
    "generated_answer_check": "Correct",
    "options_quality": "Good options",
    "observed_issues": ["Distractors too easy"],
    "overall_decision": "Accept",
    "notes": "Clear evidence, good distractors",
    "ground_truth_label": "E",
    "ground_truth_text": "Day 1 afternoon: case was open..."
  }
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
