"""
GitHub Releases Video Setup
使用GitHub Releases托管视频
"""

import json
import sys
import subprocess
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils.data_parser import load_questions, extract_clip_ids

def main():
    print("\n" + "="*70)
    print("  GITHUB RELEASES SETUP")
    print("  GitHub Releases配置")
    print("="*70 + "\n")

    # Load required videos
    base_dir = Path(__file__).parent
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'

    questions = load_questions(str(data_file))
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f"✅ Need {len(required_clip_ids)} video clips\n")

    print("="*70)
    print("REQUIREMENTS / 要求")
    print("="*70 + "\n")

    print("⚠️  Each video file must be < 2GB")
    print("⚠️  每个视频文件必须 < 2GB\n")

    print("Do your videos meet this requirement? (y/n)")
    print("你的视频符合这个要求吗？(y/n)")
    meets_req = input("> ").strip().lower()

    if meets_req != 'y':
        print("\n❌ GitHub Releases requires files < 2GB")
        print("❌ GitHub Releases要求文件 < 2GB")
        print("\n→ Use Google Drive instead (no size limit)")
        print("→ 改用Google Drive（无大小限制）")
        print("   Run: python setup_google_drive.py\n")
        return

    print("\n" + "="*70)
    print("STEP 1: Prepare Videos")
    print("步骤1：准备视频")
    print("="*70 + "\n")

    print("Where are your video files located?")
    print("你的视频文件在哪里？")
    print("(Enter the full path to the folder)")
    print("（输入文件夹的完整路径）\n")

    video_folder = input("Path: ").strip().strip('"')

    if not video_folder or not Path(video_folder).exists():
        print(f"\n❌ Folder not found: {video_folder}")
        return

    video_path = Path(video_folder)
    print(f"\n✅ Found folder: {video_path}\n")

    # List videos
    video_files = list(video_path.glob("*.mp4")) + list(video_path.glob("*.mov"))
    print(f"Found {len(video_files)} video files in folder\n")

    if len(video_files) < len(required_clip_ids):
        print(f"⚠️  Warning: Need {len(required_clip_ids)} videos, found {len(video_files)}")
        print(f"⚠️  警告：需要{len(required_clip_ids)}个视频，找到{len(video_files)}个\n")

    print("="*70)
    print("STEP 2: Create GitHub Release")
    print("步骤2：创建GitHub Release")
    print("="*70 + "\n")

    print("Creating release: 'video-assets-v1'")
    print("创建release：'video-assets-v1'\n")

    # Check if gh CLI is available
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ GitHub CLI not found")
            print("   Install from: https://cli.github.com")
            return
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) not installed")
        print("❌ 未安装GitHub CLI (gh)")
        print("\nInstall from: https://cli.github.com")
        return

    print("✅ GitHub CLI found\n")

    # Create release
    print("Creating release...")
    print("创建release...")

    cmd = [
        'gh', 'release', 'create', 'video-assets-v1',
        '--title', 'Video Assets for Annotation System',
        '--notes', 'Video clips for the EgoLife annotation system (240 clips)',
        '--repo', 'DylanZhao123/egolife-video-annotation'
    ]

    try:
        result = subprocess.run(cmd, cwd=str(base_dir), capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Release created!\n")
        elif 'already exists' in result.stderr:
            print("✅ Release already exists (will upload to existing)\n")
        else:
            print(f"❌ Error: {result.stderr}")
            return

    except Exception as e:
        print(f"❌ Error creating release: {e}")
        return

    print("="*70)
    print("STEP 3: Upload Videos")
    print("步骤3：上传视频")
    print("="*70 + "\n")

    print(f"⏱️  Uploading {len(video_files)} videos...")
    print(f"⏱️  上传{len(video_files)}个视频...")
    print("This may take 10-30 minutes depending on file sizes and internet speed")
    print("根据文件大小和网速，可能需要10-30分钟\n")

    print("Do you want to proceed? (y/n)")
    print("是否继续？(y/n)")
    proceed = input("> ").strip().lower()

    if proceed != 'y':
        print("\nCanceled. You can upload manually with:")
        print("已取消。你可以手动上传，使用：")
        print(f'cd "{video_path}"')
        print('gh release upload video-assets-v1 *.mp4 --repo DylanZhao123/egolife-video-annotation')
        return

    # Upload videos
    uploaded_count = 0
    failed_count = 0

    for video_file in video_files:
        print(f"\nUploading: {video_file.name}...")

        cmd = [
            'gh', 'release', 'upload', 'video-assets-v1',
            str(video_file),
            '--repo', 'DylanZhao123/egolife-video-annotation',
            '--clobber'  # Overwrite if exists
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                print(f"  ✅ Uploaded: {video_file.name}")
                uploaded_count += 1
            else:
                print(f"  ❌ Failed: {result.stderr[:100]}")
                failed_count += 1

        except subprocess.TimeoutExpired:
            print(f"  ⏱️ Timeout - file too large or slow connection")
            failed_count += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed_count += 1

    print("\n" + "="*70)
    print("UPLOAD SUMMARY / 上传总结")
    print("="*70)
    print(f"\n✅ Uploaded: {uploaded_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total: {len(video_files)}\n")

    if uploaded_count > 0:
        print("="*70)
        print("STEP 4: Generate Video Mapping")
        print("步骤4：生成视频映射")
        print("="*70 + "\n")

        # Generate mapping
        video_mapping = {}

        for clip_id in sorted(required_clip_ids):
            filename = f"{clip_id}.mp4"
            url = f"https://github.com/DylanZhao123/egolife-video-annotation/releases/download/video-assets-v1/{filename}"
            video_mapping[clip_id] = url

        # Save mapping
        output_file = base_dir / 'data' / 'video_mapping.json'

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(video_mapping, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved mapping to: {output_file}\n")

        # Show samples
        print("-"*70)
        print("Sample URLs / 示例URL:")
        print("-"*70)
        for i, (clip_id, url) in enumerate(list(video_mapping.items())[:3]):
            print(f"\n{clip_id}")
            print(f"  {url}")

        print("\n" + "="*70)
        print("NEXT STEPS / 下一步")
        print("="*70 + "\n")

        print("1. Test one URL in browser")
        print("   在浏览器中测试一个URL")
        print("   → Should download the video")
        print("   → 应该下载视频\n")

        print("2. Push to GitHub")
        print("   推送到GitHub")
        print("   git add data/video_mapping.json")
        print('   git commit -m "Add video URLs from GitHub Releases"')
        print("   git push\n")

        print("3. Streamlit Cloud will auto-redeploy")
        print("   Streamlit Cloud会自动重新部署\n")

        print("="*70 + "\n")

if __name__ == "__main__":
    main()
    input("Press ENTER to exit / 按回车退出...")
