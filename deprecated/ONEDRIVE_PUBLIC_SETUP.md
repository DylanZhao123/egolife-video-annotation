# Creating Public OneDrive Links (No Login Required)
# 创建公开的OneDrive链接（无需登录）

---

## Problem | 问题

OneDrive for Business links often require Microsoft login, which blocks anonymous viewers.
OneDrive for Business链接通常需要Microsoft登录，这会阻止匿名访问者。

---

## Solution 1: Check Anonymous Link Settings | 检查匿名链接设置

### Step 1: Open OneDrive Settings | 打开OneDrive设置

1. Go to your OneDrive: https://onedrive.live.com
2. Or use your UNC OneDrive directly

### Step 2: Try Different Share Options | 尝试不同的分享选项

When sharing the `Egolife_videos` folder:

**Option A: "People with existing access" vs "Anyone"**
- Look for **"Anyone"** option (allows anonymous access)
- 查找**"任何人"**选项（允许匿名访问）
- vs **"People in University of North Carolina"** (requires UNC login)
- vs **"需要UNC登录"**

**Option B: "Specific people" with public setting**
- Try selecting "Anyone with the link"
- Uncheck "Allow editing"
- Make sure it says "No sign-in required" / "无需登录"

### Step 3: Test the Link | 测试链接

Open the share link in:
- Incognito/Private browser window (Chrome: Ctrl+Shift+N)
- 隐私浏览窗口测试
- If it prompts for login → Not public yet
- 如果提示登录 → 还不是公开的

---

## Solution 2: Use Embed Links (Works Without Login)
## 方案2：使用嵌入链接（无需登录即可使用）

OneDrive has a special "embed" URL format that works without login.
OneDrive有特殊的"嵌入"URL格式，无需登录即可使用。

### Format | 格式

**From:**
```
https://adminliveunc-my.sharepoint.com/:v:/g/personal/ziyangw_ad_unc_edu/XXXXXXXXXX
```

**To:**
```
https://adminliveunc-my.sharepoint.com/:v:/s/personal/ziyangw_ad_unc_edu/XXXXXXXXXX?download=1
```

Or use the embed URL:
```
https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/_layouts/15/embed.aspx?UniqueId=XXXXXXXXXX
```

### How to Get Embed Link | 如何获取嵌入链接

1. Right-click video in OneDrive
2. Select "Embed" / "嵌入"
3. Copy the iframe src URL
4. Modify to add `?download=1` at the end

---

## Solution 3: Use OneDrive Direct Download Links
## 方案3：使用OneDrive直接下载链接

### Step 1: Get Share Link | 获取分享链接

For each video:
1. Right-click → Share
2. Copy link (even if it requires login)

Example:
```
https://adminliveunc-my.sharepoint.com/:v:/g/personal/ziyangw_ad_unc_edu/EbcR5T...
```

### Step 2: Convert to Direct Download | 转换为直接下载

Replace:
- `:v:/g/` with `:v:/r/`
- Add `?download=1` at the end

**Script to do this automatically:**

```python
def convert_to_direct_link(share_link):
    """Convert OneDrive share link to direct download"""
    # Method 1: Replace /g/ with /r/
    direct_link = share_link.replace(':v:/g/', ':v:/r/')

    # Add download parameter
    if '?' in direct_link:
        direct_link += '&download=1'
    else:
        direct_link += '?download=1'

    return direct_link
```

---

## Solution 4: If OneDrive Doesn't Allow Public Access
## 方案4：如果OneDrive不允许公开访问

Your organization might have disabled anonymous sharing.
你的组织可能禁用了匿名分享。

### Alternative Hosting Options | 替代托管选项

#### Option A: GitHub Releases (Free, Unlimited Bandwidth)

**Pros:**
- Completely public
- No login required
- Great for project assets

**Cons:**
- Max file size: 2GB per file
- Manual upload process

**Setup:**
```bash
# 1. Create a release on GitHub
gh release create videos-v1.0 --title "Video Assets"

# 2. Upload videos
gh release upload videos-v1.0 *.mp4
```

**URL Format:**
```
https://github.com/DylanZhao123/egolife-video-annotation/releases/download/videos-v1.0/DAY1_A3_TASHA_11253000.mp4
```

#### Option B: Google Drive (Easier than OneDrive for public sharing)

**Setup:**
1. Upload videos to Google Drive folder
2. Right-click → Share → Anyone with the link
3. Use this URL format:
```
https://drive.google.com/uc?export=download&id=FILE_ID
```

#### Option C: Streamlit Cloud + GitHub Large Files

- Store smaller videos in GitHub repo
- Use Git LFS for large files
- Pros: Simple deployment
- Cons: Limited storage

#### Option D: Azure Blob Storage (If you have access)

**Pros:**
- Made by Microsoft, integrates with UNC systems
- Completely public URLs
- Scalable

**Cons:**
- Requires Azure account
- May need admin approval

---

## Solution 5: Hybrid Approach (Recommended)
## 方案5：混合方案（推荐）

### For Development/Testing (Local)
Use local video cache:
```
VidsAnnotaionWebsite/cache/videos/
  DAY1_A3_TASHA_11253000.mp4
  DAY2_A3_TASHA_21000000.mp4
  ...
```

### For Production (Streamlit Cloud)

**Option 1:** If videos are small (< 1GB total)
- Upload to GitHub repository
- Commit videos directly

**Option 2:** If videos are large
- Use GitHub Releases (2GB per file)
- Or external hosting (Google Drive, etc.)

**Option 3:** Accept login requirement
- Keep OneDrive links as-is
- Add authentication flow in app
- Users log in once, get session cookie

---

## Testing Current OneDrive Links
## 测试当前的OneDrive链接

Let's test if your current OneDrive links work:

### Test Script | 测试脚本

```python
import requests

def test_onedrive_link(url):
    """Test if OneDrive link is publicly accessible"""

    response = requests.head(url, allow_redirects=True)

    if response.status_code == 200:
        print(f"✅ Link works! Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print(f"   Content-Length: {response.headers.get('Content-Length')} bytes")
        return True
    elif response.status_code == 401:
        print(f"❌ Authentication required (401)")
        return False
    elif response.status_code == 403:
        print(f"❌ Access forbidden (403)")
        return False
    else:
        print(f"⚠️  Status: {response.status_code}")
        return False

# Test your link
test_link = "YOUR_ONEDRIVE_LINK_HERE"
test_onedrive_link(test_link)
```

---

## Recommended Next Steps
## 推荐的下一步

### Immediate (测试阶段)

1. **Try embed links** - Convert share links to embed format
2. **Test in incognito** - Verify no login required
3. **Generate mapping** - Use converted links

### Short-term (如果OneDrive受限)

1. **Use Google Drive** - Easier public sharing
2. **Or GitHub Releases** - For smaller videos

### Long-term (生产环境)

1. **Contact UNC IT** - Ask about public OneDrive sharing
2. **Or use Azure Storage** - Enterprise solution
3. **Or CDN service** - For better performance

---

## Quick Fix Script
## 快速修复脚本

I can create a script that:
1. Tests your current OneDrive links
2. Tries different URL formats
3. Finds which format works without login
4. Generates the correct mapping

Would you like me to create this?

---

