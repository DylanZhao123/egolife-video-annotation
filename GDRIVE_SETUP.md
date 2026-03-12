# Google Drive 视频嵌入设置指南

## 🎯 目标
让系统直接嵌入播放 Google Drive 中的视频，而不是显示文件夹链接。

---

## 📋 设置步骤

### 方法一：自动生成映射（推荐）⭐

#### 1. 安装依赖
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

#### 2. 设置 Google Cloud Project

1. **访问 Google Cloud Console**
   - 网址：https://console.cloud.google.com/

2. **创建新项目**
   - 点击顶部项目下拉菜单
   - 点击 "NEW PROJECT"
   - 项目名称：`video-annotation-app`
   - 点击 "CREATE"

3. **启用 Google Drive API**
   - 在左侧菜单选择 "APIs & Services" > "Library"
   - 搜索 "Google Drive API"
   - 点击 "ENABLE"

4. **创建 OAuth 2.0 凭据**
   - 转到 "APIs & Services" > "Credentials"
   - 点击 "CREATE CREDENTIALS" > "OAuth client ID"
   - 应用类型：选择 "Desktop app"
   - 名称：`Video Annotation Desktop`
   - 点击 "CREATE"

5. **下载凭据文件**
   - 点击下载图标（⬇️）
   - 将文件重命名为 `credentials.json`
   - 放到项目根目录：`C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite\credentials.json`

#### 3. 运行映射生成器
```bash
cd C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite
python generate_gdrive_mapping.py
```

**首次运行**：
- 浏览器会自动打开
- 选择你的 Google 账号
- 点击 "Allow" 授权访问
- 脚本会开始扫描文件夹

**输出**：
- 生成 `data/video_mapping.json`
- 包含所有视频的 clip_id → Google Drive URL 映射

#### 4. 部署映射文件
```bash
git add data/video_mapping.json
git commit -m "Add Google Drive video mapping for embedded playback"
git push origin main
```

---

### 方法二：手动创建映射（测试用）

如果你只想测试几个视频，可以手动创建映射文件：

#### 1. 获取视频文件的分享链接
在 Google Drive 中：
- 右键点击视频文件
- 选择 "Get link"
- 复制链接（格式：`https://drive.google.com/file/d/FILE_ID/view?usp=sharing`）

#### 2. 创建 `data/video_mapping.json`
```json
{
  "DAY1_A3_TASHA_14143000": "https://drive.google.com/file/d/1ABC...XYZ/view",
  "DAY1_A3_TASHA_11103500": "https://drive.google.com/file/d/1DEF...UVW/view",
  "DAY1_A3_TASHA_14133000": "https://drive.google.com/file/d/1GHI...RST/view"
}
```

#### 3. 测试
- 本地运行 `streamlit run app.py`
- 上传包含这些 clip_id 的 JSON
- 切换到 Google Drive 模式
- 应该看到视频直接嵌入播放

---

### 方法三：使用浏览器扩展（快速方案）

#### 1. 安装 Google Drive 文件列表导出扩展
- Chrome Web Store 搜索 "Drive File Export"
- 或使用：https://workspace.google.com/marketplace/app/export_sheet_data/

#### 2. 导出文件列表
- 在 Google Drive 中打开你的文件夹
- 使用扩展导出文件列表（包含文件名和ID）
- 保存为 CSV 或 JSON

#### 3. 转换为映射文件
我可以帮你写一个脚本来转换导出的文件列表。

---

## 🔍 验证映射文件

映射文件格式：
```json
{
  "clip_id_without_extension": "https://drive.google.com/file/d/FILE_ID/view",
  ...
}
```

示例：
```json
{
  "DAY1_A3_TASHA_14143000": "https://drive.google.com/file/d/1a2B3c4D5e6F7g8H9i0J/view",
  "DAY2_A1_JAKE_10203000": "https://drive.google.com/file/d/1k2L3m4N5o6P7q8R9s0T/view"
}
```

---

## 🎬 系统行为

### 有映射的视频
```html
<iframe src="https://drive.google.com/file/d/FILE_ID/preview"
        width="100%" height="400" frameborder="0" allowfullscreen>
</iframe>
```
- ✅ 直接嵌入播放
- ✅ 无需离开页面
- ✅ 播放控制（播放/暂停/跳转）

### 无映射的视频
- 显示智能路径提示
- 显示文件夹链接
- 需要手动导航到文件

---

## 📊 映射文件统计

生成映射后，你会看到：
```
✓ Found 1247 video files

Sample mappings (first 5):
  DAY1_A3_TASHA_14143000
    → https://drive.google.com/file/d/1a2B3c4D5e6F7g8H9i0J/view
  DAY1_A3_TASHA_11103500
    → https://drive.google.com/file/d/1k2L3m4N5o6P7q8R9s0T/view
  ...
```

---

## 🚀 快速开始（最简方案）

**如果你想立即测试**：

1. 在 Google Drive 中找到一个视频
2. 右键 > Get link
3. 复制链接中的 FILE_ID 部分
4. 创建临时映射文件：

```bash
cd C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite
mkdir -p data
echo '{
  "DAY1_A3_TASHA_14143000": "https://drive.google.com/file/d/YOUR_FILE_ID/view"
}' > data/video_mapping.json
```

5. 本地测试：`streamlit run app.py`

---

## ⚠️ 重要提示

### 文件权限
确保视频文件的分享权限设置为：
- "Anyone with the link can view"
- 或者至少包含你的 Streamlit Cloud 域名

### 文件大小
- Google Drive 嵌入播放器支持大多数视频格式
- 建议视频大小 < 500MB 以获得更好的加载速度

### API 配额
- Google Drive API 有每日配额限制
- 免费用户：10,000 requests/day
- 映射生成只需运行一次

---

## 🔧 故障排除

### 问题 1：视频无法播放
**可能原因**：文件权限不足
**解决方案**：
- 检查视频文件的分享设置
- 确保设置为 "Anyone with the link"

### 问题 2：映射文件未生效
**可能原因**：
- 文件路径错误
- JSON 格式错误

**检查**：
```python
import json
with open('data/video_mapping.json') as f:
    data = json.load(f)
    print(f"Loaded {len(data)} mappings")
```

### 问题 3：API 认证失败
**解决方案**：
- 删除 `token.pickle`
- 重新运行 `generate_gdrive_mapping.py`
- 重新授权

---

## 📝 下一步

1. **选择一个方法**：自动生成 vs 手动创建
2. **生成映射文件**
3. **本地测试**：确认视频能嵌入播放
4. **推送到 GitHub**：部署到 Streamlit Cloud
5. **验证线上环境**：确认所有视频正常播放

---

## 💡 建议

### 开发阶段
- 使用手动映射文件测试几个视频
- 确认功能正常后再生成完整映射

### 生产环境
- 使用自动生成的完整映射
- 定期更新映射（当添加新视频时）
- 保留映射文件的备份

---

## 🆘 需要帮助？

如果遇到问题，提供以下信息：
- 错误信息截图
- `data/video_mapping.json` 示例（脱敏处理）
- 视频文件的分享权限设置

---

**文档版本**: 1.0.0
**最后更新**: 2026-03-12
