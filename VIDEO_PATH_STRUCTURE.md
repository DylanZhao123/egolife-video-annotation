# Video Path Structure

## Overview

Videos are automatically mapped based on their clip_id naming convention to the corresponding OneDrive folder structure.

## Folder Structure

```
Egolife_videos/
├── A1_JAKE/
│   ├── DAY1/
│   ├── DAY2/
│   ├── ...
│   └── DAY7/
├── A2_ALICE/
│   ├── DAY1/
│   ├── ...
├── A3_TASHA/
│   ├── DAY1/
│   │   └── DAY1_A3_TASHA_11093015.mp4
│   ├── DAY2/
│   ├── DAY3/
│   ├── DAY4/
│   ├── DAY5/
│   │   └── DAY5_A3_TASHA_12143000.mp4
│   ├── DAY6/
│   └── DAY7/
├── A4_LUCIA/
├── A5_KATRINA/
└── A6_SHURE/
```

## Naming Convention

Videos follow the pattern: `DAY{day}_{person}_{timestamp}.mp4`

**Examples:**
- `DAY5_A3_TASHA_12143000.mp4`
  - Day: 5
  - Person: A3_TASHA
  - Timestamp: 12143000

- `DAY1_A3_TASHA_11093015.mp4`
  - Day: 1
  - Person: A3_TASHA
  - Timestamp: 11093015

## Generated Path

The system automatically generates OneDrive paths:

```
https://adminliveunc-my.sharepoint.com/:f:/r/personal/ziyangw_ad_unc_edu/Documents/Egolife_videos/{person}/DAY{day}/{clip_id}.mp4?download=1
```

**Example:**
```
Clip ID: DAY5_A3_TASHA_12143000

Generated path:
https://adminliveunc-my.sharepoint.com/:f:/r/personal/ziyangw_ad_unc_edu/Documents/Egolife_videos/A3_TASHA/DAY5/DAY5_A3_TASHA_12143000.mp4?download=1
```

## How to Update Paths

If you add new videos or need to regenerate the mapping:

```bash
python utils/video_path_generator.py
```

This will:
1. Read all existing clip_ids from `data/video_mapping.json`
2. Parse each clip_id to extract person and day
3. Generate the correct OneDrive path
4. Update `data/video_mapping.json`

## Supported People

- A1_JAKE
- A2_ALICE
- A3_TASHA
- A4_LUCIA
- A5_KATRINA
- A6_SHURE

## Days

- DAY1 through DAY7

## Notes

- All videos must be in OneDrive with public sharing enabled
- Videos must end with `.mp4` extension
- The `?download=1` parameter enables direct download/streaming
- Path updates are automatically deployed to Streamlit Cloud when pushed to GitHub
