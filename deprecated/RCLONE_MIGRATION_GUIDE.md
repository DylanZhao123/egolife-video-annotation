# Rclone Video Migration Guide
# Rclone视频迁移指南

快速将481GB视频从UNC OneDrive迁移到Google Drive
Fast migration of 481GB videos from UNC OneDrive to Google Drive

---

## Option 1: Google Colab (Recommended - FREE & FAST)
## 方案1：Google Colab（推荐 - 免费且快速）

**Speed:** 2-4 hours for 481GB
**Cost:** FREE
**Difficulty:** ⭐⭐ Medium

### Why Google Colab?
为什么选择Google Colab？

- ✅ Free cloud server (免费云服务器)
- ✅ Fast connection to Google Drive (快速连接Google Drive)
- ✅ No local bandwidth/storage needed (不占用本地带宽/存储)
- ✅ Can run in background (可后台运行)

### Step-by-Step Instructions
分步指南

#### Step 1: Open Google Colab

1. Go to: https://colab.research.google.com
2. Sign in with your Google account (aaa26723178391@gmail.com)
3. Click "New Notebook"

#### Step 2: Install Rclone in Colab

Paste this code in the first cell:

```python
# Install rclone
!curl https://rclone.org/install.sh | sudo bash

# Check installation
!rclone version
```

Click the play button to run.

#### Step 3: Configure OneDrive

Paste this code in a new cell:

```python
# Configure OneDrive for Business (UNC)
!rclone config create unc_onedrive onedrive \
  --onedrive-chunk-size 100M \
  --onedrive-upload-cutoff 100M \
  --auto-confirm

# This will prompt you to authenticate
# Follow the OAuth flow to login with your UNC account
```

**Important:** You'll see a URL - click it, login with UNC account, authorize, then paste the code back.

#### Step 4: Configure Google Drive

```python
# Mount Google Drive in Colab
from google.colab import drive
drive.mount('/content/drive')

# This will prompt you to authenticate
# Click the link and authorize with aaa26723178391@gmail.com
```

#### Step 5: Start Transfer

```python
# Create destination folder
!mkdir -p "/content/drive/MyDrive/Egolife_videos"

# Start transfer with progress
!rclone copy \
  unc_onedrive:Egolife_videos \
  "/content/drive/MyDrive/Egolife_videos" \
  --progress \
  --transfers 8 \
  --checkers 8 \
  --buffer-size 64M \
  --drive-chunk-size 64M \
  --stats 10s \
  --stats-one-line \
  -v

print("✅ Transfer complete!")
```

**This will take 2-4 hours for 481GB**

#### Step 6: Keep Session Alive

Colab may disconnect after 90 minutes of inactivity. Use this code to keep it alive:

```python
# Keep alive script
import time
from IPython.display import clear_output

while True:
    print("⏳ Transfer running... Check progress above ⬆️")
    print(f"Time: {time.strftime('%H:%M:%S')}")
    time.sleep(300)  # Print every 5 minutes
    clear_output(wait=True)
```

#### Step 7: Verify Transfer

```python
# List files in Google Drive
!ls -lh "/content/drive/MyDrive/Egolife_videos"

# Count files
!ls "/content/drive/MyDrive/Egolife_videos" | wc -l
# Should show 240 files
```

---

## Option 2: Local Rclone (Slower but More Control)
## 方案2：本地Rclone（较慢但更可控）

**Speed:** 8-24 hours (depending on your internet)
**Cost:** FREE
**Difficulty:** ⭐⭐⭐ Medium

### Installation

#### Windows:

1. Download: https://rclone.org/downloads/
2. Extract to `C:\rclone`
3. Add to PATH or use full path

Or use Chocolatey:
```powershell
choco install rclone
```

### Configuration

#### Step 1: Configure OneDrive

```bash
rclone config
# Choose: n (new remote)
# Name: unc_onedrive
# Type: onedrive
# Client ID/Secret: leave blank
# Edit advanced config: No
# Use auto config: Yes
# Choose: OneDrive for Business
# Login with UNC account
# Choose your organization
```

#### Step 2: Configure Google Drive

```bash
rclone config
# Choose: n (new remote)
# Name: google_drive
# Type: drive
# Client ID/Secret: leave blank
# Scope: 1 (Full access)
# Use auto config: Yes
# Login with aaa26723178391@gmail.com
# Choose: This computer only
# Configure as team drive: No
```

#### Step 3: Test Connection

```bash
# List OneDrive files
rclone ls unc_onedrive:Egolife_videos --max-depth 1

# List Google Drive
rclone ls google_drive:
```

#### Step 4: Start Transfer

```bash
# Create destination folder
rclone mkdir google_drive:Egolife_videos

# Start transfer with optimizations
rclone copy \
  unc_onedrive:Egolife_videos \
  google_drive:Egolife_videos \
  --progress \
  --transfers 8 \
  --checkers 8 \
  --buffer-size 128M \
  --drive-chunk-size 64M \
  --onedrive-chunk-size 100M \
  --stats 30s \
  --stats-one-line \
  --log-file rclone_transfer.log \
  -v
```

**Performance Flags Explained:**
- `--transfers 8`: Transfer 8 files in parallel
- `--checkers 8`: Check 8 files in parallel
- `--buffer-size 128M`: Memory buffer for each transfer
- `--drive-chunk-size 64M`: Upload chunk size to Google Drive
- `--stats 30s`: Show progress every 30 seconds

---

## Option 3: Cloud Server Rclone (FASTEST but costs money)
## 方案3：云服务器Rclone（最快但需付费）

**Speed:** 1-3 hours for 481GB
**Cost:** $0.50-$2 (one-time)
**Difficulty:** ⭐⭐⭐⭐ Advanced

### Recommended Providers:

1. **DigitalOcean Droplet** ($0.007/hour = ~$0.50 total)
2. **AWS EC2 t3.medium** (~$1 for 4 hours)
3. **Google Cloud Compute Engine** (~$1 for 4 hours)

### Quick Setup (DigitalOcean Example):

#### Step 1: Create Droplet

1. Go to: https://cloud.digitalocean.com
2. Create Droplet
3. Choose: Ubuntu 22.04
4. Size: Basic $6/month (will only run for hours)
5. Region: Choose closest to you
6. Click "Create"

#### Step 2: SSH Into Server

```bash
ssh root@your_droplet_ip
```

#### Step 3: Install Rclone

```bash
curl https://rclone.org/install.sh | sudo bash
rclone version
```

#### Step 4: Configure Remotes

Since server has no browser, use remote config:

**On your local computer:**
```bash
rclone authorize "onedrive"
# Login and copy the token

rclone authorize "drive"
# Login and copy the token
```

**On the server:**
```bash
rclone config
# Add unc_onedrive: paste OneDrive token
# Add google_drive: paste Google Drive token
```

#### Step 5: Start Transfer

```bash
# Use screen to keep running if you disconnect
screen -S rclone_transfer

rclone copy \
  unc_onedrive:Egolife_videos \
  google_drive:Egolife_videos \
  --progress \
  --transfers 16 \
  --checkers 16 \
  --buffer-size 256M \
  --drive-chunk-size 128M \
  --onedrive-chunk-size 100M \
  --stats 10s \
  --stats-one-line \
  --log-file rclone.log \
  -vv

# Detach: Ctrl+A, then D
# Reattach: screen -r rclone_transfer
```

#### Step 6: Monitor Progress

```bash
# Check log
tail -f rclone.log

# Check stats
watch -n 5 'rclone ls google_drive:Egolife_videos | wc -l'
```

#### Step 7: Cleanup

After transfer completes:
```bash
# Verify file count
rclone ls google_drive:Egolife_videos | wc -l

# Delete droplet to stop charges
```

---

## Performance Comparison
## 性能对比

| Method | Speed | Time (481GB) | Cost | Difficulty |
|--------|-------|--------------|------|------------|
| **Google Colab** | High | 2-4 hours | FREE | ⭐⭐ |
| **Local Rclone** | Medium | 8-24 hours | FREE | ⭐⭐⭐ |
| **Cloud Server** | Highest | 1-3 hours | $0.5-2 | ⭐⭐⭐⭐ |
| **MultCloud** | Low | 2-3 days | FREE | ⭐ |

---

## Troubleshooting
## 故障排查

### Issue: "OAuth token expired"

**Solution:**
```bash
rclone config reconnect unc_onedrive:
rclone config reconnect google_drive:
```

### Issue: "Rate limit exceeded"

**Solution:** Add retry flags:
```bash
--retries 10 \
--low-level-retries 10 \
--tpslimit 10
```

### Issue: Transfer interrupted

**Solution:** Resume with sync (won't re-upload existing files):
```bash
rclone sync \
  unc_onedrive:Egolife_videos \
  google_drive:Egolife_videos \
  [same flags as before]
```

### Issue: "Quota exceeded" on Google Drive

**Check your quota:**
```bash
rclone about google_drive:
```

Free Google account: 15GB
If you need more: Upgrade to Google One ($1.99/month for 100GB)

---

## After Transfer Complete
## 传输完成后

### Step 1: Verify Files

```bash
# Count files
rclone ls google_drive:Egolife_videos | wc -l
# Should be 240

# Check total size
rclone size google_drive:Egolife_videos
# Should be ~481GB
```

### Step 2: Make Files Public

I'll create a script to:
1. List all files in Google Drive
2. Set each to "Anyone with link can view"
3. Generate direct download URLs
4. Create video_mapping.json

---

## Next Steps
## 下一步

After files are in Google Drive, I'll help you:

1. ✅ Set folder to public
2. ✅ Get all file IDs
3. ✅ Generate direct download URLs
4. ✅ Create video_mapping.json
5. ✅ Deploy to Streamlit Cloud

---

**Estimated Total Time:**
- Colab: 2-4 hours transfer + 30 min setup = **3-5 hours total**
- Local: 8-24 hours transfer + 20 min setup = **8-24 hours total**
- Cloud Server: 1-3 hours transfer + 1 hour setup = **2-4 hours total**

---

**Recommended:** Start with Google Colab (FREE and fast!)
