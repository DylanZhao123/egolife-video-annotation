# 🚀 立即部署到 Streamlit Cloud

## 📍 当前状态

✅ **代码已推送到 GitHub**: https://github.com/DylanZhao123/egolife-video-annotation
✅ **所有配置文件已就绪**
✅ **测试工具已包含** (test_json_compatibility.py)
✅ **部署文档已完成** (DEPLOYMENT.md)

---

## 🎯 三步部署流程

### 步骤 1: 访问 Streamlit Cloud

打开浏览器，访问：
```
https://share.streamlit.io/
```

使用你的 **GitHub 账号登录** (DylanZhao123)

---

### 步骤 2: 创建新应用

1. 点击右上角的 **"New app"** 按钮

2. 填写部署信息：
   - **Repository**: `DylanZhao123/egolife-video-annotation`
   - **Branch**: `main`
   - **Main file path**: `app.py`

3. 点击 **"Deploy!"** 按钮

---

### 步骤 3: 等待部署完成

- 首次部署大约需要 **2-5 分钟**
- Streamlit 会自动：
  - 克隆你的 GitHub 仓库
  - 安装 `requirements.txt` 中的依赖
  - 启动应用

- 部署成功后，你会看到：
  ```
  ✅ Your app is live!
  ```

- 你的应用 URL 会是：
  ```
  https://egolife-video-annotation.streamlit.app
  ```
  或
  ```
  https://[app-name]-[random-id].streamlit.app
  ```

---

## 📱 访问你的应用

部署成功后，你可以通过以下方式访问：

### 方式 1: 直接访问
```
https://egolife-video-annotation.streamlit.app
```

### 方式 2: 从 Streamlit Cloud 控制台
1. 访问 https://share.streamlit.io/
2. 在 "Your apps" 列表中找到你的应用
3. 点击应用名称即可打开

---

## 🔄 如何更新应用

每次修改代码后，只需：

```bash
git add .
git commit -m "Your update message"
git push origin main
```

Streamlit Cloud 会**自动检测更新**并重新部署，大约 2-3 分钟后生效。

---

## ✅ 验证部署成功

访问你的应用后，检查以下功能：

1. ✅ **页面加载正常** - 显示标题和侧边栏
2. ✅ **视频源选择** - 可以切换 Google Drive / OneDrive
3. ✅ **JSON上传** - 可以上传自定义JSON文件
4. ✅ **问题显示** - 显示问题和选项
5. ✅ **证据播放** - 可以展开查看证据视频
6. ✅ **提交验证** - 可以提交人工验证结果

---

## 🎨 自定义应用 URL（可选）

默认 URL 格式：`https://[random-name].streamlit.app`

如果想要自定义 URL（例如：`https://egolife-annotation.streamlit.app`）：

1. 在 Streamlit Cloud 控制台进入你的应用设置
2. 找到 "General" 选项卡
3. 修改 "App URL" 字段
4. 保存更改

**注意**：自定义 URL 需要该名称未被其他用户使用。

---

## 📊 监控和管理

### 查看日志
1. 在 Streamlit Cloud 控制台打开你的应用
2. 点击 "Manage app" 按钮
3. 选择 "Logs" 选项卡查看运行日志

### 重启应用
如果应用出现问题：
1. 点击 "Manage app"
2. 点击 "Reboot app" 按钮
3. 等待应用重启（约30秒）

### 删除应用
1. 点击 "Manage app"
2. 选择 "Settings" 选项卡
3. 滚动到底部，点击 "Delete app"

---

## 🌐 分享你的应用

部署成功后，你可以直接分享 URL 给团队成员：

```
https://egolife-video-annotation.streamlit.app
```

**无需登录**，任何人都可以访问和使用！

---

## 📞 需要帮助？

- **部署文档**: 查看 `DEPLOYMENT.md`
- **使用文档**: 查看 `README.md`
- **测试工具**: 运行 `python test_json_compatibility.py`
- **GitHub 问题**: https://github.com/DylanZhao123/egolife-video-annotation/issues

---

## 🎉 快速链接

| 资源 | 链接 |
|------|------|
| **GitHub 仓库** | https://github.com/DylanZhao123/egolife-video-annotation |
| **Streamlit Cloud** | https://share.streamlit.io/ |
| **预计应用 URL** | https://egolife-video-annotation.streamlit.app |
| **Google Drive 视频** | https://drive.google.com/drive/folders/1DoVComPUp4juZ9tNFF7EhYYEXlkkBI6K |

---

**准备好了吗？** 👉 现在就访问 https://share.streamlit.io/ 开始部署！
