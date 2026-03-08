# Google Drive Setup Guide

## Quick Test

A test app is running at: http://localhost:8504

This tests if Google Drive videos can be embedded in Streamlit.

## Current Status

✅ Video loader updated to support Google Drive
✅ Test app created
⏳ Need to map all video files to their Google Drive IDs

## Option 1: Quick Manual Test (Start Here)

1. **Get a few file IDs for testing:**
   - Open https://drive.google.com/drive/folders/1sF-zyyeaXBb68Ran3W-BWNPKv7gvaehQ
   - Navigate to `A3_TASHA/DAY1/`
   - Right-click any `.mp4` file → "Get link"
   - Extract the ID from the URL:
     ```
     https://drive.google.com/file/d/FILE_ID_HERE/view
     ```

2. **Update the test:**
   - Edit `test_google_drive_simple.py`
   - Add file IDs to `TEST_MAPPING`
   - Example:
     ```python
     TEST_MAPPING = {
         "DAY1_A3_TASHA_11093015": "1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy",
         "DAY1_A3_TASHA_11113000": "YOUR_FILE_ID_HERE",
     }
     ```

3. **Test the video:**
   - Visit http://localhost:8504
   - Check if videos load correctly

## Option 2: Interactive Mapping Tool

For mapping many videos manually:

```bash
python utils/google_drive_mapper.py
```

This will guide you through adding mappings one by one.

## Option 3: Automatic Scanning (Recommended for 240 videos)

### Setup Google API Key:

1. **Create a Google Cloud Project:**
   - Go to https://console.cloud.google.com/
   - Click "Select a project" → "New Project"
   - Name it (e.g., "EgoLife Video Mapper")

2. **Enable Google Drive API:**
   - In your project, go to "APIs & Services" → "Library"
   - Search for "Google Drive API"
   - Click "Enable"

3. **Create API Key:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the API key

4. **Make your folder accessible:**
   - Your folder is already public (Anyone with the link)
   - This allows the API to list files without OAuth

5. **Run the scanner:**
   ```bash
   # Set API key
   set GOOGLE_API_KEY=your_api_key_here

   # Run scanner
   python scan_google_drive.py
   ```

This will automatically:
- Scan all folders (A1_JAKE, A2_ALICE, A3_TASHA, etc.)
- Find all .mp4 files
- Extract file IDs
- Generate `data/video_mapping.json`

## Option 4: Batch Import from Text File

If you can export a list of files from Google Drive:

1. Create a text file `file_list.txt`:
   ```
   DAY1_A3_TASHA_11093015.mp4: 1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy
   DAY1_A3_TASHA_11113000.mp4: <another-file-id>
   ```

2. Run:
   ```bash
   python utils/google_drive_mapper.py file_list.txt
   ```

## Video URL Formats

Google Drive file IDs work with these URLs:

- **View:** `https://drive.google.com/file/d/{FILE_ID}/view`
- **Preview:** `https://drive.google.com/file/d/{FILE_ID}/preview` (best for embedding)
- **Direct:** `https://drive.google.com/uc?id={FILE_ID}`

## Update Main App

Once you have `data/video_mapping.json` with Google Drive IDs:

1. The app will automatically use the new IDs
2. No code changes needed - the video loader supports both OneDrive and Google Drive
3. Just commit and push to deploy

## Troubleshooting

### Videos don't load in test app

- Check that files are set to "Anyone with the link can view"
- Verify the file ID is correct
- Try different URL formats in the test app

### API scanner fails

- Verify API key is correct
- Check that Google Drive API is enabled
- Ensure the folder is set to public access

### Too many files to map manually

- Use Option 3 (API scanner) - it's the fastest
- Or contact me to help set it up

## Next Steps

1. ✅ Test with a few videos using the test app (http://localhost:8504)
2. Choose mapping method (API scanner recommended)
3. Generate complete `data/video_mapping.json`
4. Update main app and test locally
5. Push to GitHub to deploy to Streamlit Cloud
