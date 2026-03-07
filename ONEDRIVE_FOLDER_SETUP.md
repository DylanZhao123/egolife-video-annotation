# OneDrive 文件夹链接设置

## 新版本说明

这个版本使用更简单、更可靠的方式访问视频：
- **不再使用复杂的视频嵌入**
- **每个视频显示 OneDrive 文件夹链接**
- **用户可以在 OneDrive 中搜索和观看视频**

## 配置步骤

### 1. 获取你的 OneDrive 文件夹链接

1. 打开 OneDrive，进入包含所有视频的文件夹
2. 点击右上角的"分享"按钮
3. 设置为"任何拥有链接的人都可以查看"
4. 复制链接

### 2. 更新配置文件

编辑 `config.py` 文件，找到这一行：

```python
ONEDRIVE_VIDEO_FOLDER = "https://adminliveunc-my.sharepoint.com/personal/ziyangw_ad_unc_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fziyangw%5Fad%5Func%5Fedu%2FDocuments%2FVideoAnnotationProject"
```

将引号中的 URL 替换为你的 OneDrive 文件夹链接。

### 3. 推送到 GitHub

```bash
git add config.py
git commit -m "Update OneDrive folder URL"
git push origin main
```

Streamlit Cloud 会自动重新部署。

## 用户使用流程

1. 查看问题和视频 ID（例如：`DAY5_A3_TASHA_12143000`）
2. 点击"Open OneDrive Folder"按钮
3. 在 OneDrive 中按 Ctrl+F 搜索视频文件名（例如：`DAY5_A3_TASHA_12143000.mp4`）
4. 找到视频并观看
5. 返回标注系统回答问题

## 优点

- **简单可靠**：不依赖复杂的嵌入技术
- **无兼容性问题**：所有浏览器都支持
- **易于维护**：只需要一个文件夹链接
- **灵活**：用户可以自由浏览所有视频

## 视频文件组织建议

建议在 OneDrive 中按以下结构组织视频：

```
VideoAnnotationProject/
├── A3_TASHA/
│   ├── DAY1/
│   │   ├── DAY1_A3_TASHA_11093015_12440000.mp4
│   │   └── ...
│   ├── DAY2/
│   └── ...
├── A2_ALICE/
└── A1_JAKE/
```

用户可以使用文件夹导航或搜索功能快速找到需要的视频。
