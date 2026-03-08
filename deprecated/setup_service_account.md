# Service Account Setup for OneDrive Videos
# 使用服务账户访问OneDrive视频

---

## Overview | 概述

**Concept:** Create a dedicated Microsoft account, share your videos with it, and let the server use this account's credentials to access videos.

**概念：** 创建一个专用的Microsoft账户，将视频分享给它，让服务器使用这个账户的凭证来访问视频。

**User Experience:** Anonymous users can watch videos without logging in - the server handles authentication behind the scenes.

**用户体验：** 匿名用户可以观看视频无需登录 - 服务器在后台处理认证。

---

## Method 1: OAuth Refresh Token (Recommended)
## 方法1：OAuth刷新令牌（推荐）

### Step 1: Create Service Account | 创建服务账户

1. **Create a new Microsoft account**
   创建新的Microsoft账户
   - Go to: https://outlook.com
   - Click "Create account"
   - Email: `egolife-videos@outlook.com` (or any name you prefer)
   - Password: Choose a strong password
   - This will also create a OneDrive account (15GB free)

2. **Share your videos with this account**
   将视频分享给这个账户
   - In your UNC OneDrive, right-click `Egolife_videos` folder
   - Click "Share"
   - Enter: `egolife-videos@outlook.com`
   - Set permission: "Can view" (read-only)
   - Click "Share"

### Step 2: Register Azure Application | 注册Azure应用

1. **Go to Azure Portal**
   访问Azure Portal
   - URL: https://portal.azure.com
   - Sign in with YOUR UNC account (or the service account)

2. **Create App Registration**
   创建应用注册
   - Search for "App registrations"
   - Click "New registration"
   - Name: `EgoLife Video Server`
   - Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
   - Redirect URI: `http://localhost:8501` (for getting initial token)
   - Click "Register"

3. **Note the Application (client) ID**
   记下应用程序（客户端）ID
   - Copy this ID, you'll need it

4. **Create Client Secret**
   创建客户端密钥
   - Go to "Certificates & secrets"
   - Click "New client secret"
   - Description: "Server access token"
   - Expires: 24 months (maximum)
   - Click "Add"
   - **Copy the secret VALUE immediately** (you can't see it again)

5. **Configure API Permissions**
   配置API权限
   - Go to "API permissions"
   - Click "Add a permission"
   - Select "Microsoft Graph"
   - Select "Delegated permissions"
   - Add these permissions:
     - `Files.Read.All` (Read all files user can access)
     - `offline_access` (Maintain access to data)
   - Click "Add permissions"
   - Click "Grant admin consent" (if available)

### Step 3: Get Refresh Token | 获取刷新令牌

**This is the most important step - getting a refresh token that never expires**
**这是最重要的步骤 - 获取永不过期的刷新令牌**

I'll create a script to help you get the refresh token:

```python
# This script will:
# 1. Open browser for you to log in as the service account
# 2. Get the authorization code
# 3. Exchange it for a refresh token
# 4. Save the refresh token to Streamlit secrets format
```

### Step 4: Store in Streamlit Secrets | 存储到Streamlit Secrets

In Streamlit Cloud (or local `.streamlit/secrets.toml`):

```toml
[onedrive]
client_id = "your-client-id-here"
client_secret = "your-client-secret-here"
refresh_token = "your-refresh-token-here"
tenant_id = "common"  # or your specific tenant ID
```

### Step 5: Update Video Loader | 更新视频加载器

The app will:
1. On startup, use refresh token to get access token
2. Use access token to get video download URLs
3. Cache URLs for 50 minutes (tokens valid for 1 hour)
4. Auto-refresh when expired

---

## Method 2: Shared Links + Backend Proxy (Simpler)
## 方法2：共享链接 + 后端代理（更简单）

### Alternative Approach:

1. **Create service account and share folder** (same as above)
   创建服务账户并分享文件夹（同上）

2. **Get a long-lived access token for the service account**
   为服务账户获取长期访问令牌

3. **Server acts as proxy:**
   服务器充当代理：
   - User requests video
   - Server uses service account token to get video from OneDrive
   - Server streams video to user
   - User never sees OneDrive URL

**Pros:** Simpler setup
**Cons:** Server uses more bandwidth (proxying videos)

---

## Method 3: Pre-signed URLs (Easiest)
## 方法3：预签名URL（最简单）

### How it works:

1. **One-time setup:**
   一次性设置：
   - Service account logs in
   - Gets share links for all 240 videos
   - Share links are valid for a long time (optional expiration)

2. **Store share links:**
   存储分享链接：
   - Save to `video_mapping.json`
   - These links work for anyone (no login needed)
   - But require the service account's permission

**Limitation:** OneDrive business links might still require login even when shared

---

## Implementation Plan
## 实施计划

### Which method should we use?

**Recommendation:** Method 1 (OAuth Refresh Token)

**Why:**
- Most secure
- Most reliable
- No bandwidth overhead
- Tokens auto-refresh

### I can create:

1. **Script to get refresh token:**
   获取刷新令牌的脚本
   - `get_refresh_token.py`
   - Interactive OAuth flow
   - Saves to secrets.toml format

2. **Updated video loader:**
   更新的视频加载器
   - `utils/video_loader_auth.py`
   - Auto-authenticates on startup
   - Caches access tokens
   - Generates temporary download URLs

3. **Streamlit secrets template:**
   Streamlit secrets模板
   - `.streamlit/secrets.toml.example`
   - Shows what credentials are needed

---

## Security Considerations
## 安全考虑

### ✅ Good practices:

- Service account has read-only access
- Credentials stored in Streamlit Secrets (encrypted)
- Access tokens expire after 1 hour
- Refresh tokens allow automatic renewal

### ⚠️ Important:

- Never commit secrets to GitHub
- Use separate service account (not your personal account)
- Regularly rotate client secrets
- Monitor service account access logs

---

## Cost Analysis
## 成本分析

**Option 1: Use existing UNC OneDrive**
- Cost: $0 (free)
- Requires: Service account setup (15 minutes)

**Option 2: Personal OneDrive with more space**
- Cost: $1.99/month for 100GB
- Easier public sharing

**Recommended:** Start with Option 1 (free), switch to Option 2 if needed.

---

## Testing Plan
## 测试计划

### Local testing:

1. Set up service account
2. Get refresh token
3. Test with `streamlit run app.py`
4. Verify videos load without user login

### Production deployment:

1. Add secrets to Streamlit Cloud
2. Deploy app
3. Test in incognito browser
4. Verify no login prompt

---

## Next Steps
## 下一步

Let me know if you want to proceed with this approach, and I'll create:

1. ✅ Script to get refresh token (`get_refresh_token.py`)
2. ✅ Updated video loader with OAuth (`utils/video_loader_auth.py`)
3. ✅ Secrets template (`.streamlit/secrets.toml.example`)
4. ✅ Setup guide (`SERVICE_ACCOUNT_SETUP.md`)

This is definitely the cleanest solution - no video migration needed!

---

**Ready to start? Let me create the automation scripts!**
**准备好开始了吗？我来创建自动化脚本！**
