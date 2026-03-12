# 视频自动匹配指南 (Video Auto-Matching Guide)

## 📹 功能概述

系统现在能够从问题的 `clip_id` 自动解析出视频的路径信息，帮助用户快速定位视频文件。

---

## 🎯 工作原理

### Clip ID 格式
```
DAY1_A3_TASHA_14143000
│   │   │      └─ 时间戳 (14:14:30.00)
│   │   └─ 身份标识 (A3_TASHA)
│   └─ 身份编号 (A3)
└─ 天数 (DAY1)
```

### Google Drive 文件夹结构
```
📂 主文件夹 (1DoVComPUp4juZ9tNFF7EhYYEXlkkBI6K)
├── 📂 A1_JAKE
│   ├── 📂 DAY1
│   │   └── 🎬 DAY1_A1_JAKE_10203000.mp4
│   ├── 📂 DAY2
│   └── 📂 DAY3
├── 📂 A2_ALICE
│   ├── 📂 DAY1
│   ├── 📂 DAY2
│   └── 📂 DAY3
├── 📂 A3_TASHA
│   ├── 📂 DAY1
│   │   └── 🎬 DAY1_A3_TASHA_14143000.mp4
│   ├── 📂 DAY2
│   ├── 📂 DAY3
│   └── 📂 DAY4
└── 📂 A4_LUCIA
    └── ...
```

---

## 🚀 自动解析功能

### 示例 1: 标准30秒片段
**Clip ID**: `DAY1_A3_TASHA_14143000`

**系统自动解析**:
- Identity: `A3_TASHA`
- Day: `DAY1`
- Filename: `DAY1_A3_TASHA_14143000.mp4`

**显示路径提示**:
```
📂 Path: A3_TASHA → DAY1 → DAY1_A3_TASHA_14143000.mp4
```

**用户操作**:
1. 点击 "📂 Open Google Drive Folder"
2. 导航到 `A3_TASHA` 文件夹
3. 进入 `DAY1` 子文件夹
4. 找到 `DAY1_A3_TASHA_14143000.mp4`

### 示例 2: 2小时片段
**Clip ID**: `DAY1_A3_TASHA_00000000_07200000`

**系统自动解析**:
- Identity: `A3_TASHA`
- Day: `DAY1`
- Filename: `DAY1_A3_TASHA_00000000_07200000.mp4`
- 时间范围: 00:00:00 - 02:00:00

---

## 📊 JSON 文件示例

### 问题结构
```json
{
  "sample_id": "A3_TASHA_q_00027",
  "query": "Earlier, I noticed a case...",
  "query_time": "DAY1_A3_TASHA_14143000",
  "answer_support_clip_id": "DAY1_A3_TASHA_14143000",
  "evidence_times": [
    {
      "clip_id": "DAY1_A3_TASHA_11103500",
      "source_role": "distractor_evidence"
    },
    {
      "clip_id": "DAY1_A3_TASHA_14143000",
      "source_role": "query_time"
    }
  ],
  "choices": [...]
}
```

### 自动提取的 Clip IDs
系统会从以下字段自动提取并显示视频：
- `query_time`
- `answer_support_clip_id`
- `evidence_times[].clip_id`
- `choices[].support_clip_id` (如果有)

---

## 🎨 用户界面

### Google Drive 模式显示

```
┌─────────────────────────────────────────────────┐
│ 📹 Video: DAY1_A3_TASHA_14143000               │
│                                                 │
│ 📂 Path: A3_TASHA → DAY1 →                     │
│         DAY1_A3_TASHA_14143000.mp4             │
│                                                 │
│ Navigate to: A3_TASHA folder → DAY1 subfolder  │
│                                                 │
│ [ 📂 Open Google Drive Folder ]                │
│                                                 │
│ Tip: Once in the folder, navigate to           │
│ A3_TASHA/DAY1/ and search for                  │
│ "DAY1_A3_TASHA_14143000.mp4"                   │
└─────────────────────────────────────────────────┘
```

### Evidence 分组
系统会在三个Evidence组中显示相关视频：

1. **Query Evidence** (查询证据)
   - 显示 `query_time` 对应的视频
   - 帮助定位问题提到的时刻

2. **Correct Option Evidence** (正确选项证据)
   - 显示 `answer_support_clip_id` 视频
   - 显示标记为 `query_time` 的 evidence clips

3. **Distractor Evidence** (干扰项证据)
   - 显示其他 evidence clips
   - 帮助验证干扰项为何不正确

---

## 🔧 高级功能：视频映射文件

如果你有每个视频的具体 Google Drive 文件链接，可以创建映射文件实现直接嵌入播放。

### 创建 `data/video_mapping.json`

```json
{
  "DAY1_A3_TASHA_14143000": "https://drive.google.com/file/d/1ABC...XYZ/view",
  "DAY1_A3_TASHA_11103500": "https://drive.google.com/file/d/1DEF...UVW/view",
  "DAY2_A1_JAKE_10203000": "https://drive.google.com/file/d/1GHI...RST/view"
}
```

### 效果
- **有映射**：视频直接嵌入播放（iframe）
- **无映射**：显示智能路径提示和文件夹链接

---

## 📝 测试步骤

### 1. 上传测试数据
上传 `new_question_examples/A3_TASHA_entity_mem_annotation_input_diverse25.json`

### 2. 切换到 Google Drive 模式
在 Sidebar 选择 "Google Drive (30s clips)"

### 3. 验证自动解析
检查 Evidence 组中的视频显示：
- [ ] 显示正确的 clip_id
- [ ] 显示路径提示 (Identity → Day → Filename)
- [ ] 文件夹链接可点击
- [ ] 导航说明清晰

### 4. 测试视频定位
点击文件夹链接后：
- [ ] 能找到对应的 Identity 文件夹 (如 A3_TASHA)
- [ ] 能找到对应的 Day 子文件夹 (如 DAY1)
- [ ] 能用 Ctrl+F 搜索到视频文件

---

## 🔄 OneDrive 模式

切换到 "OneDrive (Full videos)" 时：
- 显示 OneDrive 文件夹链接（长视频）
- 适用于查看完整的2小时视频片段
- 同样显示 clip_id 和搜索提示

---

## 💡 使用建议

### 对于标注者
1. **优先使用 Google Drive 模式** - 30秒片段更精确
2. **记住文件夹结构** - Identity/Day 两层结构
3. **使用浏览器搜索** - Ctrl+F 快速定位文件名
4. **切换模式查看** - 需要更多上下文时切换到 OneDrive

### 对于管理员
1. **保持命名一致性** - 确保所有视频文件遵循标准格式
2. **完善映射文件** - 逐步添加视频URL映射以支持嵌入播放
3. **监控部署** - 检查 Streamlit Cloud 日志

---

## 🎯 未来增强

### 计划中的功能
- [ ] 自动生成 video_mapping.json（通过 Google Drive API）
- [ ] 缓存视频文件ID以加快加载
- [ ] 支持视频预览缩略图
- [ ] 批量下载功能

### 需要的改进
- [ ] Google Drive API 集成（需要认证）
- [ ] 视频时间戳跳转（需要播放器控制）
- [ ] 离线模式支持

---

## 📞 支持

如果遇到问题：
1. 检查 clip_id 格式是否正确
2. 确认 Google Drive 文件夹权限
3. 验证文件夹结构匹配
4. 查看 Streamlit Cloud 错误日志

---

**最后更新**: 2026-03-12
**版本**: 3.0.0 - 智能视频匹配
