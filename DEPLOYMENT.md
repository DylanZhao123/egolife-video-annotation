# Streamlit Cloud 部署指南 / Deployment Guide

## 🚀 快速部署 Quick Deploy

### 1. 准备工作 Prerequisites

- ✅ GitHub 账号
- ✅ Streamlit Cloud 账号（可以用GitHub登录）
- ✅ 本项目已推送到 GitHub

### 2. 部署步骤 Deployment Steps

#### 方式一：使用 Streamlit Cloud 界面部署（推荐）

1. **访问 Streamlit Cloud**
   - 打开：https://share.streamlit.io/
   - 使用 GitHub 账号登录

2. **创建新应用 New App**
   - 点击 "New app" 按钮
   - 选择你的 GitHub 仓库：`DylanZhao123/egolife-video-annotation`
   - Branch: `main`
   - Main file path: `app.py`
   - 点击 "Deploy"

3. **等待部署完成**
   - 首次部署需要 2-5 分钟
   - Streamlit 会自动安装 requirements.txt 中的依赖

4. **获取应用URL**
   - 部署成功后会自动分配一个URL
   - 格式：`https://[your-app-name].streamlit.app`

### 3. 配置说明 Configuration

#### 必需文件 Required Files

- ✅ `app.py` - 主应用文件
- ✅ `requirements.txt` - Python 依赖
- ✅ `config.py` - 应用配置
- ✅ `.streamlit/config.toml` - Streamlit 配置
- ✅ `utils/` - 工具模块目录

#### 数据文件 Data Files

默认数据文件路径：
- `data/A3_TASHA_human_adaptive_mcq_candidates_v1_low_risk.json`
- `data/video_mapping.json`

你可以在部署后通过应用界面上传新的JSON文件。

### 4. Google Drive 视频配置

视频通过 Google Drive 分享链接访问，已在 `config.py` 中配置：

```python
GDRIVE_BASE_FOLDER = "https://drive.google.com/drive/folders/1DoVComPUp4juZ9tNFF7EhYYEXlkkBI6K?usp=sharing"
```

确保：
1. ✅ Google Drive 文件夹设置为"任何人可查看"
2. ✅ `data/video_mapping.json` 已正确配置视频ID映射
3. ✅ 视频文件命名格式：`DAYx_A3_TASHA_xxxxxxxx.mp4`

### 5. 验证部署 Verify Deployment

部署成功后，访问你的应用URL，检查：

1. ✅ 页面正常加载
2. ✅ 侧边栏显示问题列表
3. ✅ 可以选择视频源（Google Drive / OneDrive）
4. ✅ 可以上传JSON文件
5. ✅ 视频可以正常播放

### 6. 常见问题 Troubleshooting

#### 问题：视频无法播放
**解决方案：**
- 检查 Google Drive 分享权限
- 确认 `video_mapping.json` 中的视频ID正确
- 检查视频文件格式是否支持

#### 问题：应用启动失败
**解决方案：**
- 检查 `requirements.txt` 依赖是否完整
- 查看 Streamlit Cloud 的日志输出
- 确认所有必需文件都已推送到 GitHub

#### 问题：JSON文件解析失败
**解决方案：**
- 使用 `test_json_compatibility.py` 测试JSON文件
- 确认JSON格式符合要求（见数据格式说明）

### 7. 更新应用 Update App

每次推送代码到 GitHub 后，Streamlit Cloud 会自动重新部署：

```bash
git add .
git commit -m "Update annotation system"
git push origin main
```

等待 2-3 分钟，应用会自动更新。

## 📝 数据格式说明 Data Format

### JSON 文件格式

支持的JSON格式示例：

```json
[
  {
    "sample_id": "A3_TASHA_q_00027",
    "query": "Earlier, I noticed a case in this scene...",
    "query_time": "DAY1_A3_TASHA_14143000",
    "query_type": "object_reidentification",
    "difficulty_tier": "hard",
    "correct_choice": "E",
    "choices": [
      {"label": "A", "text": "Day 2 morning: case was visible..."}
    ],
    "evidence_times": [
      {
        "clip_id": "DAY1_A3_TASHA_11103500",
        "timestamp_sec": 40235.0,
        "source_role": "distractor_evidence"
      }
    ]
  }
]
```

## 🔗 相关链接 Links

- **GitHub 仓库**: https://github.com/DylanZhao123/egolife-video-annotation
- **Streamlit Cloud**: https://share.streamlit.io/
