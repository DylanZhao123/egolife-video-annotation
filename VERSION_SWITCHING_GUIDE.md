# 版本切换指南 - Version Switching Guide

## 两个可用版本

### 版本 1: OneDrive 文件夹链接版本（当前版本）
- **特点**: 显示 OneDrive 文件夹链接，用户手动搜索视频
- **优点**: 简单、可靠、无嵌入问题
- **缺点**: 需要用户手动搜索视频文件

### 版本 2: Google Drive 嵌入版本
- **特点**: 尝试在页面中直接嵌入 Google Drive 视频
- **优点**: 视频直接显示在页面中
- **缺点**: 可能有兼容性问题，出现 AttributeError

---

## 如何切换版本

### 方法 1: 使用 Git 分支切换（推荐）

#### 创建分支保存当前版本

```bash
# 当前在 main 分支（OneDrive 文件夹版本）
cd C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite

# 创建 onedrive-folder 分支保存当前版本
git branch onedrive-folder

# 创建 google-drive-iframe 分支
git branch google-drive-iframe
```

#### 切换到 OneDrive 文件夹版本

```bash
git checkout onedrive-folder
# 或
git checkout main
```

在 `app.py` 中使用:
```python
from utils.video_loader_onedrive_folder import VideoLoaderOneDriveFolder as VideoLoader
```

然后推送:
```bash
git push origin onedrive-folder
# 或
git push origin main
```

#### 切换到 Google Drive 嵌入版本

```bash
git checkout google-drive-iframe
```

在 `app.py` 中修改:
```python
from utils.video_loader_external_links import VideoLoaderExternalLinks as VideoLoader
```

在视频加载部分修改:
```python
video_loader = VideoLoader()  # 不需要 folder_url 参数
```

然后推送:
```bash
git push origin google-drive-iframe
```

---

### 方法 2: 直接修改代码切换（快速方法）

#### 切换到 OneDrive 文件夹版本

**修改 `app.py` (第15行):**
```python
from utils.video_loader_onedrive_folder import VideoLoaderOneDriveFolder as VideoLoader
```

**修改 `app.py` (第173行):**
```python
onedrive_url = getattr(config, 'ONEDRIVE_VIDEO_FOLDER',
                       "https://adminliveunc-my.sharepoint.com/:f:/g/personal/ziyangw_ad_unc_edu/IgA_aigeKcG-QKDy08QVHEiEARIVaWMqy6UH-1eFP7TijWA?e=aNCstX")
video_loader = VideoLoader(folder_url=onedrive_url)
```

**推送:**
```bash
git add app.py
git commit -m "Switch to OneDrive folder version"
git push origin main
```

#### 切换到 Google Drive 嵌入版本

**修改 `app.py` (第15行):**
```python
from utils.video_loader_external_links import VideoLoaderExternalLinks as VideoLoader
```

**修改 `app.py` (第173行):**
```python
video_loader = VideoLoader()
```

**推送:**
```bash
git add app.py
git commit -m "Switch to Google Drive iframe version"
git push origin main
```

---

### 方法 3: 使用 Git Tags 标记版本

#### 为当前版本创建标签

```bash
# OneDrive 文件夹版本
git tag -a v1.0-onedrive-folder -m "OneDrive folder link version"
git push origin v1.0-onedrive-folder

# Google Drive 版本（需要先切换代码）
git tag -a v1.0-google-drive -m "Google Drive iframe version"
git push origin v1.0-google-drive
```

#### 切换到特定版本

```bash
# 查看所有标签
git tag

# 切换到 OneDrive 版本
git checkout v1.0-onedrive-folder

# 切换到 Google Drive 版本
git checkout v1.0-google-drive

# 推送到 main 分支触发部署
git checkout -b temp-deploy
git push origin temp-deploy:main --force
```

---

## 快速参考：关键文件差异

### OneDrive 文件夹版本
| 文件 | 内容 |
|------|------|
| `app.py` (line 15) | `from utils.video_loader_onedrive_folder import VideoLoaderOneDriveFolder as VideoLoader` |
| `app.py` (line 173) | `video_loader = VideoLoader(folder_url=onedrive_url)` |
| 所需文件 | `utils/video_loader_onedrive_folder.py` |
| 配置 | `config.ONEDRIVE_VIDEO_FOLDER` |

### Google Drive 嵌入版本
| 文件 | 内容 |
|------|------|
| `app.py` (line 15) | `from utils.video_loader_external_links import VideoLoaderExternalLinks as VideoLoader` |
| `app.py` (line 173) | `video_loader = VideoLoader()` |
| 所需文件 | `utils/video_loader_external_links.py`, `data/video_mapping.json` |
| 配置 | 需要 `data/video_mapping.json` 包含视频映射 |

---

## Streamlit Cloud 部署设置

如果想在 Streamlit Cloud 上切换版本，只需：

1. 在本地切换到想要的版本
2. 推送到 GitHub
3. Streamlit Cloud 会自动检测更新并重新部署（1-2分钟）

或者手动触发重启：
1. 访问 Streamlit Cloud 管理页面
2. 点击右下角 "Manage app"
3. 点击 "Reboot app"

---

## 推荐

**目前推荐使用 OneDrive 文件夹版本**，因为：
- 更稳定，无 AttributeError
- 不依赖复杂的嵌入技术
- 用户流程清晰

如果 Google Drive 嵌入版本能正常工作，可以切换回去获得更好的用户体验。
