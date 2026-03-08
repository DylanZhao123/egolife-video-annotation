"""
Resumable Video Migration Script
可恢复的视频迁移脚本

Supports token refresh during long migration
支持长时间迁移中的token刷新

Features:
- Saves progress after each video
- Can resume from last successful upload
- Prompts for new token when expired
- Skip already migrated videos
"""

import os
import sys
import time
import requests
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent))

from utils.data_parser import load_questions, extract_clip_ids

class ResumableVideoMigrator:
    """Migrate videos with resume support and token refresh"""

    def __init__(self, temp_dir="temp_videos", progress_file="migration_progress.json"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)

        self.progress_file = Path(progress_file)

        # Load or create progress tracking
        self.progress = self._load_progress()

        # Statistics
        self.downloaded_count = 0
        self.uploaded_count = 0
        self.failed_count = 0
        self.skipped_count = 0

    def _load_progress(self):
        """Load migration progress from file"""

        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'completed': [],
                'failed': [],
                'last_updated': None
            }

    def _save_progress(self):
        """Save migration progress to file"""

        self.progress['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')

        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2, ensure_ascii=False)

    def is_completed(self, clip_id):
        """Check if video already migrated"""
        return clip_id in self.progress['completed']

    def mark_completed(self, clip_id):
        """Mark video as successfully migrated"""
        if clip_id not in self.progress['completed']:
            self.progress['completed'].append(clip_id)
        self._save_progress()

    def mark_failed(self, clip_id):
        """Mark video as failed"""
        if clip_id not in self.progress['failed']:
            self.progress['failed'].append(clip_id)
        self._save_progress()

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

                file_size = local_path.stat().st_size / (1024 * 1024)
                print(f"  ✅ Downloaded: {filename} ({file_size:.1f} MB)")
                self.downloaded_count += 1
                return local_path

            elif response.status_code == 401:
                print(f"  ⚠️  TOKEN EXPIRED! Need to refresh UNC token.")
                raise TokenExpiredError("UNC access token expired")

            elif response.status_code == 404:
                print(f"  ❌ Not found in UNC OneDrive: {filename}")
                self.failed_count += 1
                return None

            else:
                print(f"  ❌ Error downloading: {response.status_code}")
                self.failed_count += 1
                return None

        except TokenExpiredError:
            raise  # Re-raise token expiration
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            self.failed_count += 1
            return None

    def upload_to_personal(self, local_path, personal_access_token):
        """Upload one video to personal OneDrive"""

        filename = local_path.name

        print(f"  ⬆️  Uploading to personal OneDrive: {filename}")

        # For large files, use upload session
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
            elif response.status_code == 401:
                print(f"  ⚠️  TOKEN EXPIRED! Need to refresh personal token.")
                raise TokenExpiredError("Personal access token expired")
            else:
                print(f"  ❌ Upload failed: {response.status_code}")
                self.failed_count += 1
                return False

        except TokenExpiredError:
            raise
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

            if response.status_code == 401:
                raise TokenExpiredError("Personal access token expired")

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

        except TokenExpiredError:
            raise
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

class TokenExpiredError(Exception):
    """Raised when access token expires"""
    pass

def get_new_token(token_type):
    """Prompt user for new access token"""

    print("\n" + "="*70)
    print(f"⚠️  {token_type} TOKEN EXPIRED!")
    print(f"⚠️  {token_type} 令牌已过期！")
    print("="*70 + "\n")

    print("Please get a new access token:")
    print("请获取新的访问令牌：\n")

    print("1. Go to: https://developer.microsoft.com/en-us/graph/graph-explorer")

    if "UNC" in token_type:
        print("2. Sign in with your UNC account (ziyangw@ad.unc.edu)")
        print("3. Grant permission: Files.Read.All")
    else:
        print("2. Sign in with annotationTest138@outlook.com")
        print("3. Grant permission: Files.ReadWrite.All")

    print("4. Click 'Access token' tab")
    print("5. Copy the token\n")

    new_token = input(f"Paste new {token_type} token here: ").strip()

    if not new_token:
        print("❌ No token provided. Exiting.")
        sys.exit(1)

    print(f"✅ New token received!\n")
    return new_token

def main():
    print("\n" + "="*70)
    print("  RESUMABLE VIDEO MIGRATION")
    print("  可恢复的视频迁移")
    print("="*70 + "\n")

    print("Features / 功能:")
    print("✅ Resume from last position if interrupted")
    print("   如果中断可从上次位置恢复")
    print("✅ Automatic token refresh prompts")
    print("   令牌过期时自动提示更新")
    print("✅ Skip already migrated videos")
    print("   跳过已迁移的视频\n")

    # Load required videos
    base_dir = Path(__file__).parent
    data_file = base_dir / 'data' / 'A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json'

    questions = load_questions(str(data_file))
    required_clip_ids = set()
    for question in questions:
        required_clip_ids.update(extract_clip_ids(question))

    print(f"Total videos to migrate: {len(required_clip_ids)}\n")

    # Initialize migrator
    migrator = ResumableVideoMigrator()

    # Check resume status
    already_done = len(migrator.progress['completed'])

    if already_done > 0:
        print(f"✅ Found previous progress: {already_done} videos already migrated")
        print(f"✅ 找到之前的进度：{already_done} 个视频已迁移")
        print(f"⏭️  Will skip these and continue from #{already_done + 1}\n")

    remaining = len(required_clip_ids) - already_done
    print(f"📊 Remaining: {remaining} videos to migrate\n")

    # Get initial tokens
    print("="*70)
    print("STEP 1: Get Access Tokens")
    print("步骤1：获取访问令牌")
    print("="*70 + "\n")

    unc_token = get_new_token("UNC")
    personal_token = get_new_token("Personal")

    # Start migration
    print("\n" + "="*70)
    print("STARTING MIGRATION")
    print("开始迁移")
    print("="*70 + "\n")

    start_time = time.time()

    # Process each video
    for i, clip_id in enumerate(sorted(required_clip_ids), 1):
        # Skip if already completed
        if migrator.is_completed(clip_id):
            migrator.skipped_count += 1
            print(f"\n[{i}/{len(required_clip_ids)}] ⏭️  Skipped (already done): {clip_id}")
            continue

        print(f"\n[{i}/{len(required_clip_ids)}] Processing: {clip_id}")

        local_path = None
        success = False

        try:
            # Download
            local_path = migrator.download_from_unc(clip_id, unc_token)

            if not local_path:
                migrator.mark_failed(clip_id)
                continue

            # Upload
            success = migrator.upload_to_personal(local_path, personal_token)

            if success:
                # Delete local copy
                migrator.cleanup_local(local_path)
                # Mark as completed
                migrator.mark_completed(clip_id)
            else:
                migrator.mark_failed(clip_id)

        except TokenExpiredError as e:
            print(f"\n⚠️  Token expired: {e}")

            # Determine which token expired and get new one
            if "UNC" in str(e):
                unc_token = get_new_token("UNC")
            else:
                personal_token = get_new_token("Personal")

            # Retry current video
            print(f"\n🔄 Retrying: {clip_id}")

            try:
                if not local_path:
                    local_path = migrator.download_from_unc(clip_id, unc_token)

                if local_path:
                    success = migrator.upload_to_personal(local_path, personal_token)

                    if success:
                        migrator.cleanup_local(local_path)
                        migrator.mark_completed(clip_id)
                    else:
                        migrator.mark_failed(clip_id)

            except Exception as retry_error:
                print(f"❌ Retry failed: {retry_error}")
                migrator.mark_failed(clip_id)

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            migrator.mark_failed(clip_id)

        # Brief pause
        time.sleep(1)

    elapsed_time = time.time() - start_time

    # Summary
    print("\n" + "="*70)
    print("MIGRATION COMPLETE")
    print("迁移完成")
    print("="*70 + "\n")

    print(f"✅ Downloaded: {migrator.downloaded_count}")
    print(f"✅ Uploaded: {migrator.uploaded_count}")
    print(f"⏭️  Skipped (already done): {migrator.skipped_count}")
    print(f"❌ Failed: {migrator.failed_count}")
    print(f"⏱️  Time: {elapsed_time/60:.1f} minutes")
    print(f"\n📊 Progress saved to: {migrator.progress_file}")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration paused. Run again to resume from last position.")
        print("⚠️  迁移已暂停。再次运行可从上次位置继续。")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")

    input("\nPress ENTER to exit...")
