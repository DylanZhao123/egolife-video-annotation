# Complete Guide: Service Account for OneDrive Videos
# 完整指南：使用服务账户访问OneDrive视频

**Goal:** Allow users to watch videos without logging in, while videos stay in your UNC OneDrive.

**目标：** 允许用户观看视频无需登录，同时视频保留在你的UNC OneDrive中。

---

## Overview | 概述

**How it works:**
1. Create a dedicated Microsoft account (service account)
2. Share your UNC OneDrive folder with this account
3. Get OAuth credentials for this account
4. Server uses these credentials to access videos
5. Users watch videos without any login

**工作原理：**
1. 创建一个专用的Microsoft账户（服务账户）
2. 将你的UNC OneDrive文件夹分享给此账户
3. 获取此账户的OAuth凭证
4. 服务器使用这些凭证访问视频
5. 用户观看视频无需任何登录

---

## Part 1: Create Service Account (5 minutes)
## 第一部分：创建服务账户（5分钟）

### Step 1.1: Create Microsoft Account

1. Go to: https://outlook.com
2. Click **"Create account"** / **"创建账户"**
3. Choose an email address:
   - Example: `egolife-videos@outlook.com`
   - Or: `unc-video-annotation@outlook.com`
   - Any name you prefer
4. Set a strong password
5. Complete the registration

**Result:** You now have a Microsoft account with 15GB free OneDrive storage.

### Step 1.2: Share Videos with Service Account

1. Go to your UNC OneDrive:
   https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu

2. Navigate to `Documents/Egolife_videos` folder

3. Right-click the folder → **"Share"**

4. Enter the service account email:
   `egolife-videos@outlook.com` (or whatever you chose)

5. Set permission to **"Can view"** (read-only)

6. Click **"Share"**

**Result:** Service account can now access your videos.

---

## Part 2: Create Azure App Registration (10 minutes)
## 第二部分：创建Azure应用注册（10分钟）

### Step 2.1: Go to Azure Portal

1. Visit: https://portal.azure.com

2. Sign in with **YOUR UNC account** (ziyangw@ad.unc.edu)
   - Or sign in with the service account (either works)

### Step 2.2: Create App Registration

1. In Azure Portal, search for: **"App registrations"**

2. Click **"New registration"**

3. Fill in details:
   - **Name:** `EgoLife Video Annotation Server`
   - **Supported account types:**
     Select **"Accounts in any organizational directory and personal Microsoft accounts"**
     (This allows both UNC and Outlook accounts)
   - **Redirect URI:**
     - Platform: **Web**
     - URI: `http://localhost:8501`

4. Click **"Register"**

**Result:** You'll see the app overview page.

### Step 2.3: Save Application (Client) ID

On the app overview page, you'll see:

```
Application (client) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Copy this ID** - you'll need it later.

### Step 2.4: Create Client Secret

1. In the left menu, click **"Certificates & secrets"**

2. Click **"New client secret"**

3. Description: `Server access key`

4. Expires: **24 months** (maximum available)

5. Click **"Add"**

6. **⚠️ IMPORTANT:** Copy the **Value** immediately!
   - You can only see it once
   - It looks like: `xxx~xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Result:** You now have a client secret.

### Step 2.5: Configure API Permissions

1. In the left menu, click **"API permissions"**

2. Click **"Add a permission"**

3. Select **"Microsoft Graph"**

4. Select **"Delegated permissions"**

5. Search and add these permissions:
   - ✅ `Files.Read` (Read user files)
   - ✅ `Files.Read.All` (Read all files that user can access)
   - ✅ `offline_access` (Maintain access to data you have given it access to)

6. Click **"Add permissions"**

7. Click **"Grant admin consent for [your organization]"**
   - If you don't see this button, it's OK - we'll consent during OAuth flow

**Result:** App has permission to read files.

---

## Part 3: Get Refresh Token (5 minutes)
## 第三部分：获取刷新令牌（5分钟）

### Step 3.1: Run the Script

In your terminal:

```bash
cd C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite
python get_refresh_token.py
```

### Step 3.2: Enter Credentials

The script will ask for:

1. **Client ID** - paste the Application ID from Step 2.3
2. **Client Secret** - paste the secret value from Step 2.4

### Step 3.3: Authorize

1. Browser will open automatically

2. **⚠️ IMPORTANT:** Log in with your **SERVICE ACCOUNT**
   - Email: `egolife-videos@outlook.com`
   - NOT your UNC account!

3. You'll see permission request:
   - "EgoLife Video Annotation Server wants to:"
   - "Read your files"
   - "Maintain access to data"

4. Click **"Accept"** / **"接受"**

5. Browser will redirect to localhost:8501 with success message

6. Return to terminal

### Step 3.4: Save Secrets

The script will automatically:
1. Save credentials to `.streamlit/secrets.toml`
2. Show you the content to copy for Streamlit Cloud

**Result:** You now have a refresh token!

---

## Part 4: Update Application Code (2 minutes)
## 第四部分：更新应用代码（2分钟）

### Step 4.1: Update Video Loader

Replace the video loader in `app.py`:

```python
# OLD:
from utils.video_loader import VideoLoader

# NEW:
from utils.video_loader_auth import VideoLoaderAuth as VideoLoader
```

That's it! The new loader will automatically use OAuth authentication.

### Step 4.2: Test Locally

```bash
streamlit run app.py
```

1. Open http://localhost:8501
2. Navigate to a question
3. Video should load automatically (no login prompt)

**If video doesn't load:**
- Check `.streamlit/secrets.toml` exists and has correct credentials
- Check service account has access to the folder
- Check console for error messages

---

## Part 5: Deploy to Streamlit Cloud (3 minutes)
## 第五部分：部署到Streamlit Cloud（3分钟）

### Step 5.1: Add Secrets to Streamlit Cloud

1. Go to: https://share.streamlit.io

2. Find your app: `egolife-video-annotation`

3. Click ⚙️ **Settings**

4. Click **"Secrets"** in left menu

5. Paste the content from `.streamlit/secrets.toml`:

```toml
[onedrive]
client_id = "your-client-id-here"
client_secret = "your-client-secret-here"
refresh_token = "your-very-long-refresh-token-here"
tenant_id = "common"
```

6. Click **"Save"**

### Step 5.2: Update Code in GitHub

```bash
# Update video loader import in app.py
git add app.py utils/video_loader_auth.py
git commit -m "Add OAuth authentication for OneDrive videos"
git push
```

### Step 5.3: Wait for Redeployment

- Streamlit Cloud detects the push
- Automatically redeploys (1-2 minutes)
- App restarts with new code

### Step 5.4: Test Production

1. Open your Streamlit Cloud URL
2. Open in **incognito/private window** (to ensure you're not logged in)
3. Navigate to a question
4. Video should load without any login!

**Result:** Users can watch videos without logging in! 🎉

---

## Security Notes | 安全说明

### ✅ Good Practices:

- Service account has **read-only** access to videos
- Credentials stored in Streamlit Secrets (encrypted at rest)
- Access tokens expire after 1 hour (auto-refreshed)
- Refresh token allows automatic renewal
- No user passwords or personal data stored

### 🔒 What's Protected:

- Your UNC OneDrive remains private
- Only the shared folder is accessible
- Service account can only READ files
- Original videos never leave your OneDrive
- Users never see the service account credentials

### ⚠️ Important:

- **Never** commit `.streamlit/secrets.toml` to GitHub
- Add to `.gitignore`:
  ```
  .streamlit/secrets.toml
  ```
- Rotate client secrets periodically (every 6-12 months)
- Monitor service account access in Azure AD logs

---

## Troubleshooting | 故障排查

### Issue 1: "Failed to refresh token"

**Cause:** Refresh token expired or revoked

**Solution:**
1. Re-run `get_refresh_token.py`
2. Update secrets in Streamlit Cloud

### Issue 2: "File not found"

**Cause:** Service account doesn't have access to folder

**Solution:**
1. Check folder is shared with service account
2. Verify permission is "Can view"
3. Check folder name is correct: `Egolife_videos`

### Issue 3: "Access token expired"

**Cause:** Token not refreshing automatically

**Solution:**
- This should auto-refresh
- Check `video_loader_auth.py` is being used
- Check logs for errors

### Issue 4: Videos load slowly

**Cause:** OneDrive API rate limiting

**Solution:**
- URLs are cached for 50 minutes
- First load may be slow, subsequent loads are faster
- Consider pre-generating URLs during app startup

---

## Cost Analysis | 成本分析

**Option 1: Free (Recommended)**
- Use existing UNC OneDrive (free)
- Service account: Free Outlook account (15GB storage)
- Azure App Registration: Free
- Total: **$0/month**

**Option 2: More Storage**
- If you need more than 15GB for service account
- OneDrive 100GB: $1.99/month
- OneDrive 1TB: $6.99/month (includes Office 365)

**Recommendation:** Start with free option, upgrade only if needed.

---

## Performance | 性能

**Expected Performance:**

- First video load: 2-5 seconds (getting URL from OneDrive)
- Subsequent loads: < 1 second (cached URLs)
- Token refresh: 1-2 seconds (every 50 minutes)
- Concurrent users: 100+ (Graph API limit: 10,000 requests/10 minutes)

**Optimization Tips:**

- URLs cached for 50 minutes
- Use Streamlit's @st.cache_data for additional caching
- Pre-fetch URLs for all videos on app startup
- Monitor API usage in Azure portal

---

## Maintenance | 维护

**Regular Tasks:**

- **Every 6 months:** Rotate client secret in Azure
- **Monthly:** Check Azure AD logs for unusual activity
- **As needed:** Re-run get_refresh_token.py if token expires

**Monitoring:**

- Azure Portal → App Registrations → Your App → Usage
- Check API call volume
- Monitor error rates

---

## Summary | 总结

**What you did:**

1. ✅ Created service account (egolife-videos@outlook.com)
2. ✅ Shared UNC OneDrive folder with service account
3. ✅ Created Azure app registration
4. ✅ Got OAuth refresh token
5. ✅ Updated app code to use OAuth
6. ✅ Deployed to Streamlit Cloud

**What users get:**

- 🎥 Watch videos without logging in
- 🚀 Fast video loading
- 🔒 Secure (no access to your personal OneDrive)
- 📱 Works on any device

**Benefits for you:**

- 💰 Free (no migration costs)
- 🏠 Videos stay in your UNC OneDrive
- 🔧 Easy to maintain
- 📊 Full control and monitoring

---

## Next Steps | 下一步

1. **Test thoroughly:**
   - Try all 120 questions
   - Verify all videos load
   - Test in different browsers

2. **Monitor usage:**
   - Check Azure portal for API usage
   - Monitor Streamlit Cloud logs

3. **Optional enhancements:**
   - Add video preloading for faster UX
   - Add offline caching
   - Add video quality selection

---

**Questions or issues? Check the troubleshooting section or ask for help!**

**有问题吗？查看故障排查部分或寻求帮助！**

---

**Total Setup Time:** ~25 minutes
**Cost:** $0
**Difficulty:** Medium
**Maintenance:** Low

**🎉 You're all set! Users can now watch videos without logging in!**
