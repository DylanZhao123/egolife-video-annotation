# 🔧 OneDrive Automatic Setup Guide

This guide will help you automatically generate share links for all 240 videos.

## Quick Start (5 minutes)

### Step 1: Install Required Package

```bash
pip install requests
```

### Step 2: Get Access Token

**Easiest Method: Graph Explorer**

1. Go to: https://developer.microsoft.com/en-us/graph/graph-explorer

2. Click "Sign in with Microsoft" (top right)
   - Use your UNC email: `ziyangw@ad.unc.edu`

3. After signing in, you'll see the Graph Explorer interface

4. Click "Modify permissions" (left sidebar)
   - Find and enable: `Files.Read.All`
   - Find and enable: `Files.ReadWrite.All`
   - Click "Consent" button

5. You may see a popup asking for permissions - Click "Accept"

6. Click "Access token" tab (top of page)

7. Copy the entire token (it's very long, starts with "eyJ...")

### Step 3: Run the Automatic Setup Script

```bash
cd "C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite"
python tools/setup_onedrive_links.py
```

The script will:
1. Ask you to paste the access token
2. Connect to your OneDrive
3. Find all videos in the `Egolife_videos` folder
4. Generate share links for each video
5. Create `data/video_mapping_generated.json`

### Step 4: Use the Generated File

```bash
# Copy the generated file to the main mapping file
cp data/video_mapping_generated.json data/video_mapping.json

# Or on Windows:
copy data\video_mapping_generated.json data\video_mapping.json
```

Done! All 240 video links are now configured.

---

## Alternative Method: Azure App Registration (Advanced)

If you need a long-term solution or the token keeps expiring, you can create an Azure app:

### Step 1: Create Azure App

1. Go to: https://portal.azure.com
2. Search for "App registrations"
3. Click "New registration"
4. Fill in:
   - Name: "Video Annotation System"
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: Leave blank for now
5. Click "Register"

### Step 2: Configure Permissions

1. In your app, go to "API permissions"
2. Click "Add a permission"
3. Select "Microsoft Graph"
4. Select "Delegated permissions"
5. Search and add:
   - `Files.Read.All`
   - `Files.ReadWrite.All`
6. Click "Add permissions"
7. Click "Grant admin consent" (if you have admin rights)

### Step 3: Get Client ID and Secret

1. Go to "Overview" - copy the "Application (client) ID"
2. Go to "Certificates & secrets"
3. Click "New client secret"
4. Description: "Video setup script"
5. Expires: 3 months
6. Click "Add"
7. Copy the secret VALUE immediately (you can't see it again)

### Step 4: Create Config File

Create `tools/onedrive_config.json`:

```json
{
  "client_id": "your-client-id-here",
  "client_secret": "your-client-secret-here",
  "tenant_id": "your-tenant-id-here"
}
```

### Step 5: Use the Enhanced Script

I can create an enhanced script that uses this app registration if you prefer this method.

---

## Troubleshooting

### Error: "Token has expired"

Access tokens from Graph Explorer expire after 1 hour. Solutions:
1. Get a new token (takes 30 seconds)
2. Run the script in chunks
3. Use Azure App Registration method instead

### Error: "Insufficient privileges"

Make sure you've consented to these permissions:
- `Files.Read.All`
- `Files.ReadWrite.All`

### Error: "Folder not found"

Check the folder name in the script. If your folder is named differently:

Edit `tools/setup_onedrive_links.py`, line 246:
```python
folder_path = "Egolife_videos"  # Change this to your folder name
```

### Script is too slow

The script processes one video at a time. For 240 videos, expect:
- 5-10 minutes total
- ~1-2 seconds per video

You can run it in the background and let it complete.

### Some videos are missing

The script will report missing videos at the end. Reasons:
1. Video file not in OneDrive folder
2. Filename doesn't match clip_id
3. Wrong folder path

Check the "Missing clip IDs" list in the output.

---

## Manual Verification

After running the script, verify a few links:

```bash
# View the generated mapping
cat data/video_mapping.json | head -20

# Test a link (copy one URL and paste in browser)
# It should download the video
```

---

## Security Notes

### Access Token Safety

- ✅ Access tokens expire after 1 hour (safe)
- ✅ Tokens are not stored anywhere
- ✅ Token only gives access to your files
- ⚠️ Don't share the token with others
- ⚠️ Don't commit it to GitHub

### Permissions Explanation

- `Files.Read.All`: Needed to list videos in your folder
- `Files.ReadWrite.All`: Needed to create share links

These permissions only affect YOUR OneDrive files, not others.

### Revoking Access

To revoke access after setup:
1. Go to: https://myaccount.microsoft.com/privacy/app-permissions
2. Find "Graph Explorer" or your app
3. Click "Remove these permissions"

---

## Batch Processing (for very large folders)

If you have thousands of videos, you can process in batches:

```python
# Edit tools/setup_onedrive_links.py
# Add this parameter to limit processing:
def setup_video_mapping(self, folder_path, required_clip_ids, output_file, max_files=100):
    # Only process first 100 videos
```

Run multiple times with different offsets.

---

## FAQ

**Q: Will this script modify my OneDrive files?**
A: No, it only reads files and creates share links. No files are modified or deleted.

**Q: Are the share links permanent?**
A: Yes, the links remain valid until you manually delete them from OneDrive.

**Q: Can I use this for other folders?**
A: Yes, just change the `folder_path` variable in the script.

**Q: What if I have videos in subfolders?**
A: The script needs to be modified to search recursively. Let me know if you need this.

**Q: Can I run this script multiple times?**
A: Yes, it's safe to run multiple times. It will regenerate all links.

---

## Getting Help

If you encounter issues:

1. Check the error message carefully
2. Verify your access token is fresh (< 1 hour old)
3. Make sure the OneDrive folder path is correct
4. Check that you have the required permissions

Need more help? Just ask!
