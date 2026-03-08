"""
Google Drive Video Setup Helper
Google Drive视频配置助手

Manual steps - this script helps you organize the process
手动步骤 - 此脚本帮你整理流程
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils.data_parser import load_questions, extract_clip_ids

def main():
    print("\n" + "="*70)
    print("  GOOGLE DRIVE SETUP HELPER")
    print("  Google Drive配置助手")
    print("="*70 + "\n")

    # Load required videos
    base_dir = Path(__file__).parent
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'

    questions = load_questions(str(data_file))
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f"✅ Found {len(required_clip_ids)} video clips needed\n")

    # Save list for reference
    clips_list = base_dir / 'data' / 'required_videos.txt'
    with open(clips_list, 'w', encoding='utf-8') as f:
        for clip_id in sorted(required_clip_ids):
            f.write(f"{clip_id}.mp4\n")

    print(f"✅ Saved list to: {clips_list}\n")

    print("="*70)
    print("STEP 1: Upload Videos to Google Drive")
    print("步骤1：上传视频到Google Drive")
    print("="*70 + "\n")

    print("1. Go to: https://drive.google.com")
    print("   访问：https://drive.google.com\n")

    print("2. Create a new folder: 'Egolife_Videos'")
    print("   创建新文件夹：'Egolife_Videos'\n")

    print("3. Upload all 240 videos to this folder")
    print("   上传所有240个视频到此文件夹")
    print("   (You can drag & drop multiple files)")
    print("   （可以拖拽多个文件）\n")

    print("4. Wait for upload to complete")
    print("   等待上传完成\n")

    print("="*70)
    print("STEP 2: Make Folder Public")
    print("步骤2：设置文件夹为公开")
    print("="*70 + "\n")

    print("1. Right-click 'Egolife_Videos' folder")
    print("   右键点击'Egolife_Videos'文件夹\n")

    print("2. Select 'Share' / '共享'")
    print("   选择'Share' / '共享'\n")

    print("3. Click 'Change to anyone with the link'")
    print("   点击'更改为任何拥有链接的人都可以'\n")

    print("4. Set permission to 'Viewer' / '查看者'")
    print("   设置权限为'Viewer' / '查看者'\n")

    print("5. Click 'Done'")
    print("   点击'完成'\n")

    print("="*70)
    print("STEP 3: Get Folder ID")
    print("步骤3：获取文件夹ID")
    print("="*70 + "\n")

    print("1. Open the 'Egolife_Videos' folder")
    print("   打开'Egolife_Videos'文件夹\n")

    print("2. Look at the URL in browser:")
    print("   查看浏览器中的URL：")
    print("   https://drive.google.com/drive/folders/FOLDER_ID_HERE")
    print("   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^")
    print("   Copy this part / 复制这部分\n")

    print("3. Paste the folder ID below:")
    print("   在下方粘贴文件夹ID：\n")

    folder_id = input("Folder ID: ").strip()

    if not folder_id:
        print("\n❌ No folder ID provided. Run this script again when ready.")
        print("❌ 未提供文件夹ID。准备好后重新运行此脚本。")
        return

    print(f"\n✅ Folder ID: {folder_id}\n")

    # Generate mapping using Google Drive direct link format
    print("="*70)
    print("STEP 4: Generating Video Mapping")
    print("步骤4：生成视频映射")
    print("="*70 + "\n")

    print("Google Drive direct link format:")
    print("Google Drive直接链接格式：")
    print("https://drive.google.com/uc?export=download&id=FILE_ID\n")

    print("⚠️  IMPORTANT: We need each video's FILE ID, not folder ID")
    print("⚠️  重要：我们需要每个视频的文件ID，不是文件夹ID\n")

    print("To get FILE IDs:")
    print("获取文件ID的方法：\n")

    print("Option A: Manual (for small number of files)")
    print("方案A：手动（适合少量文件）")
    print("  1. Right-click each video → Get link")
    print("     右键每个视频 → 获取链接")
    print("  2. Copy the FILE_ID from URL")
    print("     从URL中复制FILE_ID\n")

    print("Option B: Use Google Drive API (automatic)")
    print("方案B：使用Google Drive API（自动）")
    print("  1. Enable Google Drive API")
    print("     启用Google Drive API")
    print("  2. Get credentials.json")
    print("     获取credentials.json")
    print("  3. Run automated script (I can help with this)")
    print("     运行自动化脚本（我可以帮你）\n")

    print("="*70)
    print("Which option do you prefer?")
    print("你想选择哪个方案？")
    print("="*70 + "\n")

    print("1. Manual - I'll create share links myself (good for testing)")
    print("   手动 - 我自己创建分享链接（适合测试）\n")

    print("2. Automatic - Use Google Drive API (faster for 240 videos)")
    print("   自动 - 使用Google Drive API（处理240个视频更快）\n")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "2":
        print("\n" + "="*70)
        print("Setting up Google Drive API automation...")
        print("设置Google Drive API自动化...")
        print("="*70 + "\n")

        print("I'll create the automation script for you.")
        print("我会为你创建自动化脚本。\n")

        print("You'll need to:")
        print("你需要：")
        print("1. Enable Google Drive API in Google Cloud Console")
        print("   在Google Cloud Console中启用Google Drive API")
        print("2. Download credentials.json")
        print("   下载credentials.json")
        print("3. Run the script")
        print("   运行脚本\n")

        print("This will save you from manually getting 240 file IDs!")
        print("这可以避免手动获取240个文件ID！\n")

    else:
        print("\n" + "="*70)
        print("Manual Setup Template")
        print("手动设置模板")
        print("="*70 + "\n")

        print("Edit data/video_mapping.json with this format:")
        print("用以下格式编辑 data/video_mapping.json：\n")

        print("{")
        sample_clips = sorted(list(required_clip_ids))[:3]
        for i, clip_id in enumerate(sample_clips):
            comma = "," if i < len(sample_clips) - 1 else ""
            print(f'  "{clip_id}": "https://drive.google.com/uc?export=download&id=FILE_ID_HERE"{comma}')
        print("  ...")
        print("}\n")

        print("Replace FILE_ID_HERE with actual Google Drive file IDs")
        print("将FILE_ID_HERE替换为实际的Google Drive文件ID\n")

    print("="*70 + "\n")

if __name__ == "__main__":
    main()
    input("Press ENTER to exit / 按回车退出...")
