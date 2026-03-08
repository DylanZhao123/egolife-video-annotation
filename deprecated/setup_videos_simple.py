"""
Simple Video Setup - Just paste your token and run
简单视频配置 - 只需粘贴令牌并运行
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent))

from tools.setup_onedrive_links import OneDriveVideoSetup
from utils.data_parser import load_questions, extract_clip_ids

def main():
    print("\n" + "="*70)
    print("  VIDEO SETUP - SIMPLIFIED VERSION")
    print("  视频配置 - 简化版本")
    print("="*70 + "\n")

    # Step 1: Paste token
    print("STEP 1: Paste your Microsoft Graph API access token")
    print("步骤1：粘贴你的Microsoft Graph API访问令牌")
    print("-" * 70)
    print("\nGet your token from:")
    print("从这里获取令牌：")
    print("https://developer.microsoft.com/en-us/graph/graph-explorer")
    print("\n1. Sign in with UNC email | 用UNC邮箱登录")
    print("2. Click 'Modify Permissions' | 点击'Modify Permissions'")
    print("3. Enable: Files.Read.All + Files.ReadWrite.All | 启用这两个权限")
    print("4. Click 'Consent' | 点击'Consent'")
    print("5. Click 'Access token' tab | 点击'Access token'标签")
    print("6. Copy the token | 复制令牌")
    print("-" * 70 + "\n")

    access_token = input("Paste token here / 在此粘贴令牌: ").strip()

    if not access_token:
        print("\n❌ ERROR: No token provided! | 错误：未提供令牌！")
        return False

    print(f"\n✅ Token received! ({len(access_token)} characters)")
    print(f"✅ 令牌已接收！（{len(access_token)} 字符）\n")

    # Step 2: Load questions
    print("STEP 2: Loading question data...")
    print("步骤2：加载问题数据...")
    print("-" * 70)

    base_dir = Path(__file__).parent
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'

    questions = load_questions(str(data_file))

    if not questions:
        print("❌ ERROR: Could not load questions! | 错误：无法加载问题！")
        return False

    # Extract clip IDs
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f"✅ Loaded {len(questions)} questions | 已加载{len(questions)}个问题")
    print(f"✅ Found {len(required_clip_ids)} unique video clips | 找到{len(required_clip_ids)}个唯一视频片段\n")

    # Step 3: Generate video links
    print("STEP 3: Generating OneDrive share links...")
    print("步骤3：生成OneDrive分享链接...")
    print("-" * 70)
    print("⏱️  This will take 5-10 minutes for 240 videos...")
    print("⏱️  处理240个视频需要5-10分钟...")
    print("⏱️  Please wait... 请稍候...\n")

    client = OneDriveVideoSetup(access_token)
    folder_path = "Egolife_videos"
    output_file = base_dir / 'data' / 'video_mapping_generated.json'

    try:
        mapping = client.setup_video_mapping(folder_path, required_clip_ids, output_file)

        if mapping:
            # Copy to main file
            import shutil
            main_file = base_dir / 'data' / 'video_mapping.json'
            shutil.copy(output_file, main_file)

            print("\n" + "="*70)
            print("✅ SUCCESS! | 成功！")
            print("="*70)
            print(f"\n📁 Generated: {output_file}")
            print(f"📁 Activated: {main_file}")
            print(f"\n✅ Mapped {len(mapping)} videos successfully!")
            print(f"✅ 成功映射了 {len(mapping)} 个视频！")

            # Show sample
            print("\n" + "-"*70)
            print("Sample mappings / 示例映射:")
            print("-"*70)
            for i, (clip_id, url) in enumerate(list(mapping.items())[:3]):
                print(f"{clip_id}")
                print(f"  → {url[:80]}...")
                if i < 2:
                    print()

            print("\n" + "="*70)
            print("NEXT STEPS / 下一步:")
            print("="*70)
            print("\n1. Test locally / 本地测试:")
            print("   streamlit run app.py")
            print("   Open: http://localhost:8501")
            print("\n2. Push to GitHub / 推送到GitHub:")
            print("   git add data/video_mapping.json")
            print('   git commit -m "Add OneDrive video links"')
            print("   git push")
            print("\n3. Streamlit Cloud will auto-redeploy in 1-2 minutes")
            print("   Streamlit Cloud会在1-2分钟内自动重新部署")
            print("\n" + "="*70 + "\n")

            return True
        else:
            print("\n❌ ERROR: No mappings generated! | 错误：未生成映射！")
            return False

    except Exception as e:
        print(f"\n❌ ERROR / 错误: {e}\n")
        print("Troubleshooting / 故障排查:")
        print("-" * 70)
        print("1. Token expired? Get a fresh one (< 1 hour old)")
        print("   令牌过期？获取新的令牌（< 1小时）")
        print("\n2. Permissions granted? Check Files.Read.All + Files.ReadWrite.All")
        print("   权限已授予？检查 Files.Read.All + Files.ReadWrite.All")
        print("\n3. Folder name correct? Check 'Egolife_videos' exists in OneDrive")
        print("   文件夹名称正确？检查OneDrive中是否存在'Egolife_videos'")
        print("\n4. Signed in with correct account? Use UNC email")
        print("   使用正确的账户登录？使用UNC邮箱")
        print("-" * 70 + "\n")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  Starting video configuration...")
    print("  开始配置视频...")
    print("="*70)

    success = main()

    if success:
        print("🎉 Setup complete! All videos are ready!")
        print("🎉 配置完成！所有视频已就绪！\n")
    else:
        print("⚠️  Setup failed. Please check the errors above.")
        print("⚠️  配置失败。请检查上面的错误。\n")

    input("Press ENTER to exit / 按回车键退出...")
