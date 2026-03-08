# Video Annotation System - Architecture Overview
# 视频标注系统 - 架构概览

---

## System Overview | 系统概述

**English:** A web-based video annotation platform for collecting multiple-choice question responses about video content. Built with Streamlit for rapid deployment and ease of use.

**中文：** 基于Web的视频标注平台，用于收集视频内容的多选题回答。使用Streamlit构建，快速部署、易于使用。

---

## Core Logic | 核心逻辑

### Workflow | 工作流程

```
User Login → Load Questions → Display Video + Question → User Answers → Record Response → Next Question
用户登录 → 加载问题 → 显示视频+问题 → 用户作答 → 记录答案 → 下一题
```

### Data Flow | 数据流程

```
[JSON Question File] → [Data Parser] → [Session State] → [UI Display]
                                            ↓
[OneDrive Videos] → [Video Loader] → [Video Player]
                                            ↓
[User Input] → [Response Recorder] → [JSONL File]
```

**English:**
1. **Load**: System loads 120 questions from JSON file
2. **Display**: Shows video clips and multiple-choice question
3. **Interact**: User watches videos and selects an answer
4. **Record**: System saves user response with timestamp
5. **Progress**: Auto-saves progress, user can resume anytime

**中文：**
1. **加载**：系统从JSON文件加载120个问题
2. **显示**：展示视频片段和多选题
3. **交互**：用户观看视频并选择答案
4. **记录**：系统保存用户回答和时间戳
5. **进度**：自动保存进度，用户可随时恢复

---

## Technology Stack | 技术栈

### Frontend | 前端
- **Streamlit 1.30+**: Python web framework for data applications
- **Streamlit 1.30+**: Python的数据应用Web框架

### Backend | 后端
- **Python 3.8+**: Core programming language | 核心编程语言
- **Pandas 2.0+**: Data processing | 数据处理
- **Requests 2.28+**: HTTP library for API calls | HTTP库用于API调用

### Data Storage | 数据存储
- **JSON**: Question database (120 questions, 240 video clips)
- **JSON**: 问题数据库（120个问题，240个视频片段）
- **JSONL**: Response records (one JSON object per line)
- **JSONL**: 回答记录（每行一个JSON对象）

### Video Hosting | 视频托管
- **OneDrive**: Cloud video storage with direct links
- **OneDrive**: 云端视频存储，使用直链访问
- **Microsoft Graph API**: Automatic link generation
- **Microsoft Graph API**: 自动生成分享链接

### Deployment | 部署
- **GitHub**: Version control and code hosting
- **GitHub**: 版本控制和代码托管
- **Streamlit Cloud**: Free web hosting (1GB RAM, public apps)
- **Streamlit Cloud**: 免费Web托管（1GB内存，公开应用）

---

## File Structure | 文件结构

```
VidsAnnotaionWebsite/
│
├── app.py                      # Main application | 主应用程序
├── config.py                   # Configuration settings | 配置设置
├── requirements.txt            # Python dependencies | Python依赖
│
├── data/                       # Data files | 数据文件
│   ├── A3_TASHA_*.json        # Question database (120 questions)
│   │                          # 问题数据库（120个问题）
│   ├── video_mapping.json     # Video URL mapping (240 clips)
│   │                          # 视频URL映射（240个片段）
│   ├── responses.jsonl        # User responses (auto-generated)
│   │                          # 用户回答（自动生成）
│   └── progress.json          # Session progress (auto-save)
│                              # 会话进度（自动保存）
│
├── utils/                     # Utility modules | 工具模块
│   ├── data_parser.py        # Load and parse questions
│   │                         # 加载和解析问题
│   ├── video_loader.py       # Manage video URLs
│   │                         # 管理视频URL
│   ├── session_manager.py    # Handle user sessions
│   │                         # 处理用户会话
│   └── response_recorder.py  # Save user responses
│                             # 保存用户回答
│
└── tools/                    # Setup tools | 设置工具
    ├── quick_setup.py        # Auto-configure OneDrive links
    │                         # 自动配置OneDrive链接
    └── setup_onedrive_links.py  # Microsoft Graph API client
                              # Microsoft Graph API客户端
```

---

## Key Components | 核心组件

### 1. Data Parser | 数据解析器
**File:** `utils/data_parser.py`

**English:** Loads JSON question file, extracts video clip IDs, formats questions and choices.

**中文：** 加载JSON问题文件，提取视频片段ID，格式化问题和选项。

**Key Functions:**
- `load_questions()`: Load 120 questions from JSON
- `extract_clip_ids()`: Find all video references in questions
- `format_choice_text()`: Format A/B/C/D/E answer choices

---

### 2. Video Loader | 视频加载器
**File:** `utils/video_loader.py`

**English:** Maps video clip IDs to OneDrive URLs, handles missing videos gracefully.

**中文：** 将视频片段ID映射到OneDrive URL，妥善处理缺失的视频。

**Key Functions:**
- `get_video_url(clip_id)`: Get OneDrive URL for a video clip
- `load_mapping()`: Load video URL mapping from JSON
- Fallback to local cache if OneDrive link unavailable

---

### 3. Session Manager | 会话管理器
**File:** `utils/session_manager.py`

**English:** Manages user progress, auto-saves every 5 questions, enables session resumption.

**中文：** 管理用户进度，每5题自动保存，支持恢复会话。

**Key Functions:**
- `initialize_session()`: Create new user session
- `save_progress()`: Auto-save current position
- `load_progress()`: Resume from last session

**Session State:**
```python
{
    "current_index": 0,        # Current question number (0-119)
    "responses": [],           # List of submitted answers
    "user_id": "annotator_001", # Annotator identifier
    "start_time": "2026-03-06T10:00:00"  # Session start timestamp
}
```

---

### 4. Response Recorder | 回答记录器
**File:** `utils/response_recorder.py`

**English:** Saves each answer as a JSONL record with timestamp and correctness.

**中文：** 将每个答案保存为JSONL记录，包含时间戳和正确性。

**Record Format:**
```json
{
  "sample_id": "altmulti_124",
  "user_id": "annotator_001",
  "user_answer": "D",
  "correct_answer": "D",
  "is_correct": true,
  "time_spent_seconds": 155.23,
  "timestamp": "2026-03-06T15:30:25"
}
```

---

### 5. Main Application | 主应用
**File:** `app.py` (303 lines)

**English:** Streamlit web interface with video player, question display, answer submission, and navigation.

**中文：** Streamlit Web界面，包含视频播放器、问题显示、答案提交和导航。

**UI Layout:**
```
┌─────────────────────────────────────────────────┐
│  Sidebar                │  Main Content         │
│  - Progress metrics     │  ┌─────────────────┐  │
│  - User ID input        │  │ Video Player    │  │
│  - Navigation           │  └─────────────────┘  │
│  - Export button        │                       │
│                         │  Question Text        │
│                         │                       │
│                         │  [A] Choice A         │
│                         │  [B] Choice B         │
│                         │  [C] Choice C         │
│                         │  [D] Choice D         │
│                         │  [E] Choice E         │
│                         │                       │
│                         │  [Submit Answer]      │
└─────────────────────────────────────────────────┘
```

---

## Question Structure | 问题结构

**English:** Each question references multiple video clips for different purposes.

**中文：** 每个问题引用多个视频片段，用于不同目的。

```json
{
  "sample_id": "altmulti_124",
  "query": "Before the last time you saw the bowl...",

  "query_time": "DAY5_A3_TASHA_12143000",
  // Video shown when displaying the question
  // 显示问题时播放的视频

  "evidence_times": [
    {"clip_id": "DAY1_A3_TASHA_11253000", "start": 0, "end": 30},
    {"clip_id": "DAY5_A3_TASHA_12143000", "start": 0, "end": 30}
  ],
  // Background evidence clips for context
  // 提供上下文的背景证据片段

  "choices": [
    {
      "label": "A",
      "text": "In the living room on the table",
      "support_clip_id": "DAY2_A3_TASHA_21000000"
    },
    {
      "label": "B",
      "text": "In the kitchen on the counter",
      "support_clip_id": "DAY1_A3_TASHA_20383000"
    }
    // Each choice has a supporting video clip
    // 每个选项都有对应的支持视频片段
  ],

  "correct_choice": "D"
}
```

**Statistics | 统计数据:**
- Total Questions | 问题总数: **120**
- Total Video Clips | 视频片段总数: **240**
- Average Videos per Question | 平均每题视频数: **~6-8**
  - 1 query video | 1个查询视频
  - 1-2 evidence videos | 1-2个证据视频
  - 5 choice support videos | 5个选项支持视频

---

## Data Persistence | 数据持久化

### Local Deployment | 本地部署
**English:**
- Responses saved to `data/responses.jsonl`
- Progress saved to `data/progress.json`
- Persistent across restarts

**中文：**
- 回答保存到 `data/responses.jsonl`
- 进度保存到 `data/progress.json`
- 重启后持久保存

### Streamlit Cloud | 云端部署
**English:**
- File system is ephemeral (resets every 12 hours)
- Manual export via "Export Responses" button
- Optional: Integrate Google Sheets for auto-save

**中文：**
- 文件系统是临时的（每12小时重置）
- 通过"导出回答"按钮手动导出
- 可选：集成Google Sheets实现自动保存

---

## Deployment Options | 部署选项

### 1. Local Development | 本地开发
```bash
# Install dependencies | 安装依赖
pip install -r requirements.txt

# Run application | 运行应用
streamlit run app.py

# Access at | 访问地址
http://localhost:8501
```

### 2. Streamlit Cloud | 云端部署
**English:**
- Free hosting for public repositories
- Automatic deployment from GitHub
- URL format: `https://username-repo-app-xxx.streamlit.app`

**中文：**
- 公开仓库免费托管
- 从GitHub自动部署
- URL格式：`https://username-repo-app-xxx.streamlit.app`

**Limitations | 限制:**
- 1GB RAM
- Apps sleep after 7 days of inactivity
- No file persistence (use export or database)

---

## Configuration | 配置

### Video Links | 视频链接
**File:** `data/video_mapping.json`

**Format:**
```json
{
  "DAY1_A3_TASHA_11253000": "https://onedrive-share-link.com/video1.mp4?download=1",
  "DAY2_A3_TASHA_21000000": "https://onedrive-share-link.com/video2.mp4?download=1"
}
```

**Setup Methods | 配置方法:**
1. **Automatic | 自动**: Run `python tools/quick_setup.py` with Microsoft Graph API token
2. **Manual | 手动**: Generate OneDrive share links and paste into JSON file

---

## Security & Privacy | 安全与隐私

**English:**
- No personal data collection (only annotator ID)
- Videos hosted on institutional OneDrive (UNC)
- Responses stored locally or exported manually
- No third-party analytics or tracking

**中文：**
- 不收集个人数据（仅标注员ID）
- 视频托管在机构OneDrive（UNC）
- 回答本地存储或手动导出
- 无第三方分析或追踪

---

## Performance | 性能

**English:**
- Load Time: < 3 seconds (local) | < 5 seconds (cloud)
- Video Streaming: Depends on OneDrive bandwidth
- Response Time: Instant (session state)
- Supports: 10+ concurrent users (Streamlit Cloud)

**中文：**
- 加载时间：< 3秒（本地）| < 5秒（云端）
- 视频流：取决于OneDrive带宽
- 响应时间：即时（会话状态）
- 支持：10+并发用户（Streamlit Cloud）

---

## Future Enhancements | 未来改进

**Potential Features | 潜在功能:**
- [ ] Google Sheets integration for auto-save | Google Sheets集成自动保存
- [ ] Database backend (PostgreSQL/MongoDB) | 数据库后端
- [ ] Multi-user analytics dashboard | 多用户分析仪表板
- [ ] Video timestamp annotations | 视频时间戳标注
- [ ] Keyboard shortcuts for faster navigation | 键盘快捷键加快导航
- [ ] Dark mode support | 深色模式支持
- [ ] Mobile-responsive UI | 移动端响应式UI

---

## Troubleshooting | 故障排查

### Common Issues | 常见问题

**1. Videos not loading | 视频无法加载**
- Check `data/video_mapping.json` has real URLs | 检查是否有真实URL
- Verify OneDrive links are public | 验证OneDrive链接是公开的
- Ensure URLs end with `?download=1` | 确保URL以`?download=1`结尾

**2. Responses not saving | 回答未保存**
- Local: Check `data/responses.jsonl` exists | 本地：检查文件是否存在
- Cloud: Use "Export Responses" button | 云端：使用"导出回答"按钮

**3. Session lost | 会话丢失**
- Streamlit Cloud resets after inactivity | 云端闲置后重置
- Use "Resume Session" button if available | 使用"恢复会话"按钮

---

## Contact & Support | 联系与支持

**Repository | 仓库:**
https://github.com/DylanZhao123/egolife-video-annotation

**Documentation | 文档:**
- `README.md`: Project overview | 项目概览
- `DEPLOYMENT.md`: Deployment guide | 部署指南
- `ONEDRIVE_SETUP.md`: Video configuration | 视频配置
- `START_FROM_SCRATCH.md`: Complete setup tutorial | 完整设置教程

---

**Last Updated | 最后更新:** 2026-03-06
**Version | 版本:** 1.0.0
**License | 许可:** MIT
