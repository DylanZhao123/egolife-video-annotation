"""
Test OneDrive Links and Find Public URL Format
测试OneDrive链接并找到公开URL格式
"""

import requests
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent))

def test_url(url, description):
    """Test if URL is publicly accessible (no login required)"""
    print(f"\nTesting: {description}")
    print(f"URL: {url[:80]}...")

    try:
        # Test without authentication
        response = requests.head(url, allow_redirects=True, timeout=10)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✅ SUCCESS - Link works without login!")
            content_type = response.headers.get('Content-Type', 'unknown')
            content_length = response.headers.get('Content-Length', 'unknown')
            print(f"   Content-Type: {content_type}")
            print(f"   Content-Length: {content_length} bytes")
            return True
        elif response.status_code == 401:
            print("❌ FAILED - Authentication required (401)")
            return False
        elif response.status_code == 403:
            print("❌ FAILED - Access forbidden (403)")
            return False
        elif response.status_code == 404:
            print("❌ FAILED - Not found (404)")
            return False
        else:
            print(f"⚠️  UNKNOWN - Status {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def convert_onedrive_formats(base_url):
    """Generate different OneDrive URL formats to try"""

    formats = []

    # Original
    formats.append(("Original", base_url))

    # Add download parameter
    if '?' in base_url:
        formats.append(("With &download=1", base_url + "&download=1"))
    else:
        formats.append(("With ?download=1", base_url + "?download=1"))

    # Replace /g/ with /r/ (sometimes works for public access)
    if ':v:/g/' in base_url:
        r_format = base_url.replace(':v:/g/', ':v:/r/')
        formats.append(("Replace /g/ with /r/", r_format))
        formats.append(("Replace /g/ with /r/ + download", r_format + "?download=1"))

    # Try embed format
    if 'sharepoint.com' in base_url:
        # This is a guess - actual embed URLs need the file ID
        formats.append(("Note: Embed format", "Need to get from OneDrive Embed option"))

    return formats

def main():
    print("\n" + "="*70)
    print("  ONEDRIVE PUBLIC LINK TESTER")
    print("  OneDrive公开链接测试器")
    print("="*70 + "\n")

    print("This tool tests if OneDrive links work without login.")
    print("此工具测试OneDrive链接是否无需登录即可访问。\n")

    print("Paste one of your OneDrive video share links:")
    print("粘贴一个你的OneDrive视频分享链接：")
    print("(Example: https://adminliveunc-my.sharepoint.com/:v:/g/...)")
    print()

    test_url_input = input("> ").strip()

    if not test_url_input:
        print("\n❌ No URL provided!")
        return

    print("\n" + "="*70)
    print("Testing different URL formats...")
    print("测试不同的URL格式...")
    print("="*70)

    # Test different formats
    formats = convert_onedrive_formats(test_url_input)

    working_format = None

    for description, url in formats:
        if url.startswith("Need to"):
            print(f"\n{description}: {url}")
            continue

        if test_url(url, description):
            working_format = (description, url)
            break

    print("\n" + "="*70)
    print("RESULTS / 结果")
    print("="*70 + "\n")

    if working_format:
        print(f"✅ FOUND WORKING FORMAT: {working_format[0]}")
        print(f"✅ 找到有效格式：{working_format[0]}\n")
        print(f"URL: {working_format[1]}\n")

        print("You can use this URL format for all videos!")
        print("你可以对所有视频使用这种URL格式！")

    else:
        print("❌ None of the formats work without login.")
        print("❌ 没有找到无需登录的格式。\n")

        print("="*70)
        print("SOLUTIONS / 解决方案")
        print("="*70 + "\n")

        print("Your OneDrive might require login for all links.")
        print("你的OneDrive可能要求所有链接都需要登录。\n")

        print("Option 1: Use Google Drive (Easier for public sharing)")
        print("方案1：使用Google Drive（更容易公开分享）")
        print("  - Upload videos to Google Drive")
        print("  - Share folder as 'Anyone with link'")
        print("  - Use format: https://drive.google.com/uc?export=download&id=FILE_ID\n")

        print("Option 2: Use GitHub Releases (Free, unlimited bandwidth)")
        print("方案2：使用GitHub Releases（免费，无限带宽）")
        print("  - Max 2GB per file")
        print("  - Run: gh release create videos-v1")
        print("  - Run: gh release upload videos-v1 *.mp4\n")

        print("Option 3: Contact UNC IT")
        print("方案3：联系UNC IT")
        print("  - Ask about enabling anonymous OneDrive sharing")
        print("  - Or request Azure Blob Storage access\n")

        print("Option 4: Accept login requirement (Temporary solution)")
        print("方案4：接受需要登录（临时方案）")
        print("  - Users must have Microsoft/UNC accounts")
        print("  - They log in once, then links work")
        print("  - Not ideal for public annotation system\n")

    print("="*70 + "\n")

if __name__ == "__main__":
    main()
    input("Press ENTER to exit / 按回车退出...")
