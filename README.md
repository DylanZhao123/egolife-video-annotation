# 🎬 Video Annotation System

A Streamlit-based web application for annotating videos with multiple-choice questions, designed for the EgoLife video dataset.

## Features

- 📹 **Video Playback**: Seamless integration with OneDrive-hosted videos
- ❓ **Multiple Choice Questions**: Interactive question answering interface
- 💾 **Progress Tracking**: Automatic progress saving and recovery
- 📊 **Statistics**: Real-time accuracy and time tracking
- 🔄 **Session Management**: Resume where you left off
- 📥 **Export**: Export responses in JSONL, JSON, or CSV format

## Project Structure

```
VidsAnnotaionWebsite/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   ├── A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json  # Question data
│   ├── video_mapping.json         # Clip ID to video URL mapping
│   ├── responses.jsonl            # User responses (generated)
│   └── progress.json              # Session progress (generated)
├── utils/
│   ├── __init__.py
│   ├── data_parser.py             # Data loading and parsing
│   ├── video_loader.py            # Video URL management
│   ├── session_manager.py         # Session state management
│   └── response_recorder.py       # Response saving and export
└── cache/                          # Local video cache (optional)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone this repository:
```bash
git clone <your-repo-url>
cd VidsAnnotaionWebsite
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure video URLs:
   - Edit `data/video_mapping.json`
   - Add OneDrive direct download links for each clip_id
   - See [Video Setup Guide](#video-setup) below

## Usage

### Running Locally

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Deploying to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Click "Deploy"

## Video Setup

### Option 1: OneDrive Direct Links (Recommended)

1. Upload videos to OneDrive
2. Right-click each video → Share → "Anyone with the link can view"
3. Copy the share link
4. Add `?download=1` to the end of the URL
5. Add to `data/video_mapping.json`:

```json
{
  "DAY1_A3_TASHA_11253000": "https://adminliveunc-my.sharepoint.com/.../video1.mp4?download=1",
  "DAY2_A3_TASHA_10460000": "https://adminliveunc-my.sharepoint.com/.../video2.mp4?download=1"
}
```

### Option 2: Local Cache

Place video files in the `cache/` directory with filenames matching the clip IDs:

```
cache/
├── DAY1_A3_TASHA_11253000.mp4
├── DAY2_A3_TASHA_10460000.mp4
└── ...
```

## Configuration

Edit `config.py` to customize:

- Data file paths
- Video settings
- UI theme
- Auto-save intervals
- Export formats

## Data Format

### Input (Questions)

Questions are loaded from `data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json`:

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
{"sample_id": "altmulti_124", "user_answer": "D", "correct_answer": "D", "is_correct": true, "time_spent_seconds": 155.23, "timestamp": "2026-03-06T10:30:25", "user_id": "annotator_001"}
```

## Features

### Current Features

- ✅ Video playback with OneDrive integration
- ✅ Multiple-choice question interface
- ✅ Progress tracking and recovery
- ✅ Response recording (JSONL format)
- ✅ Real-time statistics
- ✅ Export to multiple formats

### Future Enhancements

- [ ] Multi-user authentication
- [ ] Admin dashboard
- [ ] Quality control (inter-annotator agreement)
- [ ] Video playback controls (speed, frame-by-frame)
- [ ] Side-by-side video comparison
- [ ] Google Sheets integration for data persistence

## Troubleshooting

### Videos not loading

1. Check that `data/video_mapping.json` has correct URLs
2. Verify OneDrive links end with `?download=1`
3. Check that videos are publicly accessible
4. Try using local cache instead

### Progress not saving on Streamlit Cloud

Streamlit Cloud doesn't support persistent file storage. Consider:
- Using Google Sheets API
- Using a database (e.g., Supabase, MongoDB Atlas)
- Downloading responses regularly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Contact

For questions or issues, please open an issue on GitHub.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Designed for the EgoLife video dataset
