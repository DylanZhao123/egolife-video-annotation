"""
Batch Video Migration Script
批量视频迁移脚本

Downloads from UNC OneDrive, uploads to personal OneDrive, then deletes local copy
从UNC OneDrive下载，上传到个人OneDrive，然后删除本地副本

One video at a time to save disk space
一次一个视频以节省磁盘空间
"""

import os
import sys
import time
import requests
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent))

from utils.data_parser import load_questions, extract_clip_ids

class VideoMigrator:
    """Migrate videos from UNC OneDrive to personal OneDrive"""

    def __init__(self, temp_dir="temp_videos"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)

        # Statistics
        self.downloaded_count = 0
        self.uploaded_count = 0
        self.failed_count = 0
        self.skipped_count = 0

    def download_from_unc(self, clip_id, unc_access_token):
        """Download one video from UNC OneDrive"""

        filename = f"{clip_id}.mp4"
        local_path = self.temp_dir / filename

        # Check if already exists
        if local_path.exists():
            print(f"  ✓ Already downloaded locally: {filename}")
            return local_path

        print(f"  ⬇️  Downloading from UNC OneDrive: {filename}")

        # Graph API URL
        url = f"https://graph.microsoft.com/v1.0/me/drive/root:/Egolife_videos/{filename}:/content"

        headers = {
            'Authorization': f'Bearer {unc_access_token}'
        }

        try:
            response = requests.get(url, headers=headers, stream=True)

            if response.status_code == 200:
                # Download with progress
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

                            # Show progress every 100MB
                            if downloaded % (100 * 1024 * 1024) == 0:
                                progress_mb = downloaded / (1024 * 1024)
                                print(f"    Downloaded: {progress_mb:.1f} MB")

                file_size = local_path.stat().st_size / (1024 * 1024)
                print(f"  ✅ Downloaded: {filename} ({file_size:.1f} MB)")
                self.downloaded_count += 1
                return local_path

            elif response.status_code == 404:
                print(f"  ❌ Not found in UNC OneDrive: {filename}")
                self.failed_count += 1
                return None

            else:
                print(f"  ❌ Error downloading: {response.status_code}")
                self.failed_count += 1
                return None

        except Exception as e:
            print(f"  ❌ Exception: {e}")
            self.failed_count += 1
            return None

    def upload_to_personal(self, local_path, personal_access_token):
        """Upload one video to personal OneDrive"""

        filename = local_path.name

        print(f"  ⬆️  Uploading to personal OneDrive: {filename}")

        # For files > 4MB, use upload session (recommended)
        file_size = local_path.stat().st_size

        if file_size > 4 * 1024 * 1024:  # > 4MB
            return self._upload_large_file(local_path, personal_access_token)
        else:
            return self._upload_small_file(local_path, personal_access_token)

    def _upload_small_file(self, local_path, access_token):
        """Upload file < 4MB"""

        filename = local_path.name
        url = f"https://graph.microsoft.com/v1.0/me/drive/root:/Egolife_videos/{filename}:/content"

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/octet-stream'
        }

        with open(local_path, 'rb') as f:
            data = f.read()

        try:
            response = requests.put(url, headers=headers, data=data)

            if response.status_code in [200, 201]:
                print(f"  ✅ Uploaded: {filename}")
                self.uploaded_count += 1
                return True
            else:
                print(f"  ❌ Upload failed: {response.status_code}")
                print(f"     {response.text[:200]}")
                self.failed_count += 1
                return False

        except Exception as e:
            print(f"  ❌ Exception: {e}")
            self.failed_count += 1
            return False

    def _upload_large_file(self, local_path, access_token):
        """Upload file > 4MB using upload session"""

        filename = local_path.name

        # Create upload session
        create_session_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/Egolife_videos/{filename}:/createUploadSession"

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        session_data = {
            "item": {
                "@microsoft.graph.conflictBehavior": "replace"
            }
        }

        try:
            response = requests.post(create_session_url, headers=headers, json=session_data)

            if response.status_code not in [200, 201]:
                print(f"  ❌ Failed to create upload session: {response.status_code}")
                self.failed_count += 1
                return False

            session_info = response.json()
            upload_url = session_info['uploadUrl']

            # Upload in chunks
            chunk_size = 10 * 1024 * 1024  # 10MB chunks
            file_size = local_path.stat().st_size

            with open(local_path, 'rb') as f:
                chunk_start = 0

                while chunk_start < file_size:
                    chunk_end = min(chunk_start + chunk_size, file_size)
                    chunk_data = f.read(chunk_size)

                    headers = {
                        'Content-Length': str(len(chunk_data)),
                        'Content-Range': f'bytes {chunk_start}-{chunk_end-1}/{file_size}'
                    }

                    chunk_response = requests.put(upload_url, headers=headers, data=chunk_data)

                    if chunk_response.status_code not in [200, 201, 202]:
                        print(f"  ❌ Chunk upload failed: {chunk_response.status_code}")
                        self.failed_count += 1
                        return False

                    progress = (chunk_end / file_size) * 100
                    print(f"    Progress: {progress:.1f}%")

                    chunk_start = chunk_end

            print(f"  ✅ Uploaded: {filename}")
            self.uploaded_count += 1
            return True

        except Exception as e:
            print(f"  ❌ Exception during upload: {e}")
            self.failed_count += 1
            return False

    def cleanup_local(self, local_path):
        """Delete local file after successful upload"""

        try:
            if local_path and local_path.exists():
                local_path.unlink()
                print(f"  🗑️  Deleted local copy: {local_path.name}")
                return True
        except Exception as e:
            print(f"  ⚠️  Failed to delete: {e}")
            return False

def main():
    print("\n" + "="*70)
    print("  VIDEO MIGRATION - BATCH PROCESSING")
    print("  视频迁移 - 批量处理")
    print("="*70 + "\n")

    print("This script will:")
    print("此脚本将：")
    print("1. Download one video from UNC OneDrive")
    print("   从UNC OneDrive下载一个视频")
    print("2. Upload it to annotationTest138@outlook.com")
    print("   上传到annotationTest138@outlook.com")
    print("3. Delete local copy")
    print("   删除本地副本")
    print("4. Repeat for all 240 videos")
    print("   重复处理全部240个视频\n")

    print("⚠️  You'll need access tokens for BOTH OneDrive accounts")
    print("⚠️  你需要两个OneDrive账户的访问令牌\n")

    # Load required videos
    base_dir = Path(__file__).parent
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'

    questions = load_questions(str(data_file))
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f"Found {len(required_clip_ids)} videos to migrate\n")

    # Get access tokens
    print("="*70)
    print("STEP 1: Get UNC OneDrive Access Token")
    print("步骤1：获取UNC OneDrive访问令牌")
    print("="*70 + "\n")

    print("Go to: https://developer.microsoft.com/en-us/graph/graph-explorer")
    print("1. Sign in with your UNC account (ziyangw@ad.unc.edu)")
    print("2. Grant permissions: Files.Read.All")
    print("3. Copy the access token\n")

    unc_token = input("Paste UNC access token: ").strip()

    if not unc_token:
        print("❌ Token required!")
        return

    print("\n" + "="*70)
    print("STEP 2: Get Personal OneDrive Access Token")
    print("步骤2：获取个人OneDrive访问令牌")
    print("="*70 + "\n")

    print("Go to: https://developer.microsoft.com/en-us/graph/graph-explorer")
    print("1. Sign OUT and sign in with annotationTest138@outlook.com")
    print("2. Grant permissions: Files.ReadWrite.All")
    print("3. Copy the access token\n")

    personal_token = input("Paste personal access token: ").strip()

    if not personal_token:
        print("❌ Token required!")
        return

    # Initialize migrator
    migrator = VideoMigrator()

    print("\n" + "="*70)
    print("STARTING MIGRATION")
    print("开始迁移")
    print("="*70 + "\n")

    start_time = time.time()

    # Process each video
    for i, clip_id in enumerate(sorted(required_clip_ids), 1):
        print(f"\n[{i}/{len(required_clip_ids)}] Processing: {clip_id}")

        # Download
        local_path = migrator.download_from_unc(clip_id, unc_token)

        if not local_path:
            continue

        # Upload
        success = migrator.upload_to_personal(local_path, personal_token)

        if success:
            # Delete local copy
            migrator.cleanup_local(local_path)
        else:
            print(f"  ⚠️  Keeping local copy due to upload failure")

        # Brief pause to avoid rate limiting
        time.sleep(1)

    elapsed_time = time.time() - start_time

    # Summary
    print("\n" + "="*70)
    print("MIGRATION COMPLETE")
    print("迁移完成")
    print("="*70 + "\n")

    print(f"✅ Downloaded: {migrator.downloaded_count}")
    print(f"✅ Uploaded: {migrator.uploaded_count}")
    print(f"❌ Failed: {migrator.failed_count}")
    print(f"⏱️  Time: {elapsed_time/60:.1f} minutes")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Canceled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")

    input("\nPress ENTER to exit...")
