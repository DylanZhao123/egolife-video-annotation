# 从零开始配置指南

## 前提条件

确保已安装：
- Python 3.8+
- Git

---

## 步骤 1：启动本地应用（2分钟）

### 1.1 打开终端

在项目目录打开命令行：
```bash
cd C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite
```

### 1.2 安装依赖（首次运行）

```bash
pip install streamlit pandas requests
```

### 1.3 启动应用

```bash
streamlit run app.py
```

应用会自动在浏览器打开：`http://localhost:8501`

### 1.4 测试基本功能

在浏览器中：
- 查看问题界面
- 测试上一题/下一题按钮
- 尝试选择答案

**注意**：此时视频不会播放（需要配置OneDrive链接）

---

## 步骤 2：配置视频链接（10-15分钟）

### 选项A：自动配置（推荐）

#### 2.1 获取Microsoft Graph API访问令牌

1. 打开浏览器访问：
   ```
   https://developer.microsoft.com/en-us/graph/graph-explorer
   ```

2. 使用UNC邮箱登录：`ziyangw@ad.unc.edu`

3. 在左侧边栏点击 **"Modify permissions"**

4. 找到并勾选以下权限：
   - `Files.Read.All`
   - `Files.ReadWrite.All`

5. 点击底部的 **"Consent"** 按钮

6. 弹出窗口中点击 **"Accept"**

7. 点击页面顶部的 **"Access token"** 标签

8. 复制显示的访问令牌（以 "eyJ..." 开头的长字符串）

#### 2.2 运行自动配置脚本

保持Streamlit应用运行，新开一个终端窗口：

```bash
cd C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite
python tools/quick_setup.py
```

按提示操作：
- 选择 `y` 打开Graph Explorer（如已打开可跳过）
- 粘贴刚才复制的访问令牌
- 等待5-10分钟（脚本会处理240个视频）

#### 2.3 查看结果

脚本完成后会显示：
```
SUCCESS! Video links configured!
Mapped 240 videos successfully!
```

视频链接已保存到 `data/video_mapping.json`

#### 2.4 刷新应用

回到浏览器，刷新页面（F5），视频现在应该可以播放了。

---

### 选项B：手动配置（不推荐，耗时2-3小时）

如果自动配置失败，可以手动为每个视频创建分享链接：

1. 登录OneDrive
2. 进入 `Egolife_videos` 文件夹
3. 对每个视频：
   - 右键 → 共享
   - 选择"任何拥有链接的人都可查看"
   - 复制链接
   - 在链接末尾添加 `?download=1`
   - 添加到 `data/video_mapping.json`

---

## 步骤 3：推送到GitHub（3分钟）

### 3.1 创建GitHub仓库

1. 访问：`https://github.com/new`

2. 填写信息：
   - Repository name: `video-annotation-system`
   - Visibility: **Public**（免费Streamlit Cloud需要）
   - 不要勾选 "Initialize this repository with a README"

3. 点击 **"Create repository"**

### 3.2 连接本地仓库到GitHub

在项目目录终端中运行（替换YOUR-USERNAME为你的GitHub用户名）：

```bash
git remote add origin https://github.com/YOUR-USERNAME/video-annotation-system.git
```

### 3.3 推送代码

```bash
git branch -M main
git push -u origin main
```

### 3.4 验证

刷新GitHub仓库页面，应该能看到所有文件已上传。

---

## 步骤 4：部署到Streamlit Cloud（5分钟）

### 4.1 访问Streamlit Cloud

打开：`https://share.streamlit.io`

### 4.2 登录

点击 **"Sign in with GitHub"**，授权Streamlit访问你的GitHub账号

### 4.3 创建新应用

1. 点击右上角 **"New app"**

2. 填写部署信息：
   - **Repository**: 选择 `YOUR-USERNAME/video-annotation-system`
   - **Branch**: `main`
   - **Main file path**: `app.py`

3. 点击 **"Deploy!"**

### 4.4 等待部署

- 部署过程需要2-3分钟
- 可以查看实时日志了解进度
- 部署完成后会显示公开URL

### 4.5 获取公开URL

部署成功后，你的应用URL格式为：
```
https://YOUR-USERNAME-video-annotation-system.streamlit.app
```

复制此URL分享给标注人员。

---

## 步骤 5：测试线上应用（2分钟）

### 5.1 访问公开URL

在浏览器中打开刚才获得的URL

### 5.2 测试功能

- 问题加载正常
- 视频可以播放
- 可以选择答案并提交
- 导航功能正常

### 5.3 检查数据记录

答案会保存到 `data/responses.jsonl`，但Streamlit Cloud不支持文件持久化。

**解决方案**：
- 使用侧边栏的"Export Responses"按钮定期导出
- 或者集成Google Sheets（参考高级配置）

---

## 常见问题

### Q1: 本地应用启动失败

**错误**：`streamlit: command not found`

**解决**：
```bash
pip install streamlit
```

---

### Q2: 视频配置脚本报错

**错误**：`Token has expired`

**解决**：Graph Explorer的令牌1小时后过期。重新获取令牌：
1. 刷新Graph Explorer页面
2. 点击"Access token"
3. 复制新令牌
4. 重新运行脚本

---

### Q3: 视频不播放

**可能原因**：
1. OneDrive链接未配置
2. 链接格式错误（需要 `?download=1` 后缀）
3. 视频权限设置为私有

**检查**：
```bash
# 查看映射文件
cat data/video_mapping.json

# 测试一个链接（在浏览器中打开，应该下载视频）
```

---

### Q4: GitHub推送失败

**错误**：`remote origin already exists`

**解决**：
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/video-annotation-system.git
```

---

### Q5: Streamlit部署失败

**常见原因**：
- 仓库不是public
- `requirements.txt` 缺少依赖
- `app.py` 路径错误

**检查部署日志**：
在Streamlit Cloud点击应用 → "Manage app" → "Logs"

---

## 更新代码

### 本地修改后推送更新

```bash
# 修改代码后
git add .
git commit -m "描述你的修改"
git push
```

Streamlit Cloud会自动检测更新并重新部署（约1-2分钟）。

---

## 完整命令清单

### 启动本地应用
```bash
cd C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite
streamlit run app.py
```

### 配置视频
```bash
python tools/quick_setup.py
```

### 推送到GitHub
```bash
git remote add origin https://github.com/YOUR-USERNAME/video-annotation-system.git
git branch -M main
git push -u origin main
```

### 更新代码
```bash
git add .
git commit -m "更新说明"
git push
```

---

## 时间估算

| 步骤 | 时间 |
|------|------|
| 启动本地应用 | 2分钟 |
| 配置视频（自动）| 10分钟 |
| 推送到GitHub | 3分钟 |
| 部署到Streamlit Cloud | 5分钟 |
| 测试验证 | 2分钟 |
| **总计** | **约22分钟** |

---

## 下一步

部署完成后：

1. **分享URL**：把Streamlit Cloud的URL发给标注人员

2. **监控使用**：在Streamlit Cloud dashboard查看访问统计

3. **导出数据**：定期从应用侧边栏导出答案

4. **更新视频**：如需添加更多视频，重新运行配置脚本，然后推送更新

---

## 获取帮助

- **配置问题**：查看 `ONEDRIVE_SETUP.md`
- **部署问题**：查看 `DEPLOYMENT.md`
- **功能问题**：查看 `README.md`

---

## 快速恢复

如果浏览器关闭或终端断开：

### 重启本地应用
```bash
cd C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite
streamlit run app.py
```

### 查看已部署的应用
访问：`https://YOUR-USERNAME-video-annotation-system.streamlit.app`

### 查看本地应用
访问：`http://localhost:8501`
