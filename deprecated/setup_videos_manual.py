"""
Manual Video Setup - Using public folder URL
手动视频配置 - 使用公开文件夹URL
"""

import json
import sys
from pathlib import Path
from urllib.parse import quote

# Add parent to path
sys.path.append(str(Path(__file__).parent))

from utils.data_parser import load_questions, extract_clip_ids

def construct_onedrive_url(folder_share_url, filename):
    """
    Construct direct download URL from folder share URL
    从文件夹分享URL构造直接下载URL
    """
    # Method 1: Using folder URL pattern
    # 方法1：使用文件夹URL模式

    # If folder_share_url is like: https://...sharepoint.com/.../Egolife_videos
    # We can construct: https://...sharepoint.com/.../Egolife_videos/filename.mp4

    base_url = folder_share_url.rstrip('/')
    encoded_filename = quote(filename)
    direct_url = f"{base_url}/{encoded_filename}?download=1"

    return direct_url

def main():
    print("\n" + "="*70)
    print("  MANUAL VIDEO SETUP - Using Public Folder")
    print("  手动视频配置 - 使用公开文件夹")
    print("="*70 + "\n")

    # Step 1: Get folder share URL
    print("STEP 1: Get your OneDrive folder share URL")
    print("步骤1：获取你的OneDrive文件夹分享URL")
    print("-" * 70)
    print("\nIn OneDrive web:")
    print("在OneDrive网页中：")
    print("1. Right-click on 'Egolife_videos' folder")
    print("   右键点击'Egolife_videos'文件夹")
    print("2. Select 'Share' / '共享'")
    print("3. Set to 'Anyone with the link can view'")
    print("   设置为'任何拥有链接的人都可以查看'")
    print("4. Click 'Copy link' / '复制链接'")
    print("-" * 70 + "\n")

    print("Paste the folder share URL here:")
    print("在此粘贴文件夹分享URL：")
    folder_url = input("> ").strip()

    if not folder_url:
        print("\n❌ ERROR: No URL provided!")
        return False

    print(f"\n✅ URL received!")
    print(f"✅ URL已接收！\n")

    # Step 2: Load questions
    print("STEP 2: Loading question data...")
    print("步骤2：加载问题数据...")
    print("-" * 70)

    base_dir = Path(__file__).parent
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'

    questions = load_questions(str(data_file))

    if not questions:
        print("❌ ERROR: Could not load questions!")
        return False

    # Extract clip IDs
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f"✅ Loaded {len(questions)} questions")
    print(f"✅ Found {len(required_clip_ids)} unique video clips\n")

    # Step 3: Generate mapping
    print("STEP 3: Generating video URLs...")
    print("步骤3：生成视频URL...")
    print("-" * 70 + "\n")

    video_mapping = {}

    for clip_id in sorted(required_clip_ids):
        # Assume video filename is: clip_id.mp4
        # 假设视频文件名是：clip_id.mp4
        filename = f"{clip_id}.mp4"
        url = construct_onedrive_url(folder_url, filename)
        video_mapping[clip_id] = url

    print(f"✅ Generated {len(video_mapping)} video URLs\n")

    # Step 4: Save to file
    output_file = base_dir / 'data' / 'video_mapping.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(video_mapping, f, indent=2, ensure_ascii=False)

    print("="*70)
    print("✅ SUCCESS!")
    print("="*70)
    print(f"\n📁 Saved to: {output_file}")
    print(f"📁 已保存到: {output_file}\n")

    # Show samples
    print("-"*70)
    print("Sample URLs / 示例URL:")
    print("-"*70)
    for i, (clip_id, url) in enumerate(list(video_mapping.items())[:3]):
        print(f"\n{clip_id}")
        print(f"  → {url}")

    print("\n" + "="*70)
    print("NEXT STEPS / 下一步:")
    print("="*70)
    print("\n1. Test one URL in browser / 在浏览器中测试一个URL:")
    print("   Copy any URL above and paste in browser")
    print("   复制上面任意一个URL并在浏览器中打开")
    print("   → Should download the video file")
    print("   → 应该会下载视频文件")
    print("\n2. If URLs work, push to GitHub / 如果URL有效，推送到GitHub:")
    print("   git add data/video_mapping.json")
    print('   git commit -m "Add video URLs"')
    print("   git push")
    print("\n3. If URLs don't work, try Method 3 (see below)")
    print("   如果URL无效，尝试方法3（见下文）")
    print("\n" + "="*70 + "\n")

    return True

if __name__ == "__main__":
    success = main()

    if not success:
        print("\n" + "="*70)
        print("ALTERNATIVE METHOD 3: Manual Entry")
        print("备选方法3：手动输入")
        print("="*70)
        print("\nIf automatic URL construction doesn't work:")
        print("如果自动构造URL不起作用：")
        print("\n1. Manually create share links for each video in OneDrive")
        print("   在OneDrive中为每个视频手动创建分享链接")
        print("\n2. Use this template to fill in video_mapping.json:")
        print("   使用此模板填写 video_mapping.json：")
        print("\n{")
        print('  "DAY1_A3_TASHA_11253000": "https://your-link.com/video1.mp4?download=1",')
        print('  "DAY2_A3_TASHA_21000000": "https://your-link.com/video2.mp4?download=1"')
        print("}")
        print("\n" + "="*70 + "\n")

    input("Press ENTER to exit / 按回车键退出...")
