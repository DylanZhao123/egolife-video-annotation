"""
Get OAuth Refresh Token for Service Account
获取服务账户的OAuth刷新令牌

This script helps you get a refresh token that the server can use to access OneDrive videos.
此脚本帮助你获取服务器用于访问OneDrive视频的刷新令牌。
"""

import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
from pathlib import Path

# Configuration
CLIENT_ID = ""  # You'll enter this when running the script
CLIENT_SECRET = ""  # You'll enter this when running the script
REDIRECT_URI = "http://localhost:8501"
SCOPES = "Files.Read.All offline_access"

# OAuth endpoints
AUTHORIZATION_ENDPOINT = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
TOKEN_ENDPOINT = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

# Global variable to store authorization code
auth_code = None

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback"""

    def do_GET(self):
        global auth_code

        # Parse query parameters
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if 'code' in params:
            auth_code = params['code'][0]

            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            success_html = """
            <html>
            <head><title>Authorization Successful</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: green;">✅ Authorization Successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                <p>你可以关闭此窗口并返回终端。</p>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode())
        else:
            # Error response
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            error_html = """
            <html>
            <head><title>Authorization Failed</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: red;">❌ Authorization Failed</h1>
                <p>Please try again.</p>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode())

    def log_message(self, format, *args):
        # Suppress log messages
        pass

def get_authorization_code(client_id):
    """Open browser for user to authorize and get authorization code"""

    # Build authorization URL
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
        'response_mode': 'query'
    }

    auth_url = f"{AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"

    print("\n" + "="*70)
    print("STEP 1: Authorize the Application")
    print("步骤1：授权应用程序")
    print("="*70 + "\n")

    print("Opening browser for authorization...")
    print("正在打开浏览器进行授权...\n")

    print("⚠️  IMPORTANT: Log in with your SERVICE ACCOUNT")
    print("⚠️  重要：使用你的服务账户登录")
    print("   (e.g., egolife-videos@outlook.com)\n")

    print("NOT your personal UNC account!")
    print("不是你的个人UNC账户！\n")

    # Open browser
    webbrowser.open(auth_url)

    print("After you approve:")
    print("授权后：")
    print("- Browser will redirect to localhost:8501")
    print("- 浏览器会重定向到localhost:8501")
    print("- You'll see a success message")
    print("- 你会看到成功消息")
    print("- Return here to continue")
    print("- 返回这里继续\n")

    # Start local server to receive callback
    server = HTTPServer(('localhost', 8501), OAuthCallbackHandler)

    print("Waiting for authorization...")
    print("等待授权...\n")

    # Handle one request (the OAuth callback)
    server.handle_request()

    return auth_code

def exchange_code_for_token(client_id, client_secret, auth_code):
    """Exchange authorization code for access and refresh tokens"""

    print("\n" + "="*70)
    print("STEP 2: Exchange Code for Tokens")
    print("步骤2：用代码交换令牌")
    print("="*70 + "\n")

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    print("Requesting tokens from Microsoft...")
    print("从Microsoft请求令牌...\n")

    response = requests.post(TOKEN_ENDPOINT, data=data)

    if response.status_code == 200:
        token_data = response.json()

        print("✅ Success! Received tokens:")
        print("✅ 成功！收到令牌：\n")

        print(f"Access Token: {token_data['access_token'][:50]}...")
        print(f"Refresh Token: {token_data['refresh_token'][:50]}...")
        print(f"Expires in: {token_data['expires_in']} seconds")
        print(f"Token type: {token_data['token_type']}\n")

        return token_data
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"❌ 错误：{response.status_code}\n")
        print(f"Response: {response.text}\n")
        return None

def save_secrets(client_id, client_secret, refresh_token):
    """Save credentials to Streamlit secrets format"""

    print("\n" + "="*70)
    print("STEP 3: Save to Streamlit Secrets")
    print("步骤3：保存到Streamlit Secrets")
    print("="*70 + "\n")

    # Create .streamlit directory if it doesn't exist
    streamlit_dir = Path('.streamlit')
    streamlit_dir.mkdir(exist_ok=True)

    secrets_file = streamlit_dir / 'secrets.toml'

    secrets_content = f"""# OneDrive Service Account Credentials
# OneDrive服务账户凭证
# Generated by get_refresh_token.py

[onedrive]
client_id = "{client_id}"
client_secret = "{client_secret}"
refresh_token = "{refresh_token}"
tenant_id = "common"

# Usage in app:
# import streamlit as st
# client_id = st.secrets["onedrive"]["client_id"]
# client_secret = st.secrets["onedrive"]["client_secret"]
# refresh_token = st.secrets["onedrive"]["refresh_token"]
"""

    with open(secrets_file, 'w', encoding='utf-8') as f:
        f.write(secrets_content)

    print(f"✅ Saved to: {secrets_file}")
    print(f"✅ 已保存到：{secrets_file}\n")

    print("="*70)
    print("For Streamlit Cloud:")
    print("在Streamlit Cloud中：")
    print("="*70 + "\n")

    print("1. Go to your app settings")
    print("   进入应用设置\n")

    print("2. Find 'Secrets' section")
    print("   找到'Secrets'部分\n")

    print("3. Copy and paste this content:")
    print("   复制并粘贴以下内容：\n")

    print("-" * 70)
    print(secrets_content)
    print("-" * 70 + "\n")

def main():
    print("\n" + "="*70)
    print("  GET OAUTH REFRESH TOKEN")
    print("  获取OAuth刷新令牌")
    print("="*70 + "\n")

    print("This script will help you get a refresh token for your service account.")
    print("此脚本将帮助你获取服务账户的刷新令牌。\n")

    print("PREREQUISITES / 前提条件:")
    print("-" * 70)
    print("1. Created a Microsoft service account (e.g., egolife-videos@outlook.com)")
    print("   已创建Microsoft服务账户（如egolife-videos@outlook.com）\n")

    print("2. Shared your UNC OneDrive 'Egolife_videos' folder with this account")
    print("   已将UNC OneDrive的'Egolife_videos'文件夹分享给此账户\n")

    print("3. Created an Azure App Registration")
    print("   已创建Azure应用注册")
    print("   - Got Client ID")
    print("   - Got Client Secret")
    print("   - Added permissions: Files.Read.All, offline_access\n")

    print("4. Set redirect URI to: http://localhost:8501")
    print("   已设置重定向URI为：http://localhost:8501\n")

    print("-" * 70 + "\n")

    input("Press ENTER if you've completed all prerequisites... ")

    # Get client credentials
    print("\n" + "="*70)
    print("Enter Your Azure App Credentials")
    print("输入你的Azure应用凭证")
    print("="*70 + "\n")

    client_id = input("Client ID (Application ID): ").strip()

    if not client_id:
        print("❌ Client ID is required!")
        return

    client_secret = input("Client Secret (Value): ").strip()

    if not client_secret:
        print("❌ Client Secret is required!")
        return

    # Get authorization code
    auth_code = get_authorization_code(client_id)

    if not auth_code:
        print("❌ Failed to get authorization code")
        return

    print(f"✅ Received authorization code: {auth_code[:20]}...\n")

    # Exchange for tokens
    token_data = exchange_code_for_token(client_id, client_secret, auth_code)

    if not token_data:
        print("❌ Failed to get tokens")
        return

    # Save secrets
    save_secrets(client_id, client_secret, token_data['refresh_token'])

    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("✅ 设置完成！")
    print("="*70 + "\n")

    print("Next steps:")
    print("下一步：\n")

    print("1. Test locally:")
    print("   本地测试：")
    print("   streamlit run app.py\n")

    print("2. Deploy to Streamlit Cloud:")
    print("   部署到Streamlit Cloud：")
    print("   - Add secrets to Streamlit Cloud settings")
    print("   - 在Streamlit Cloud设置中添加secrets")
    print("   - App will automatically use service account")
    print("   - 应用会自动使用服务账户\n")

    print("3. Users can watch videos WITHOUT logging in!")
    print("   用户可以观看视频无需登录！\n")

    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Canceled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")

    input("\nPress ENTER to exit...")
