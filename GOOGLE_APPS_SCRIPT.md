# Google Apps Script - 自动生成视频映射

## 最简单的方法！在 Google Drive 中一键生成映射

### 步骤：

#### 1. 打开 Google Apps Script

访问: https://script.google.com/

#### 2. 创建新项目

点击 "新建项目"

#### 3. 粘贴以下代码

```javascript
function generateVideoMapping() {
  // 你的 Google Drive 文件夹 ID
  var FOLDER_ID = '1sF-zyyeaXBb68Ran3W-BWNPKv7gvaehQ';

  var mapping = {};

  // 扫描文件夹
  function scanFolder(folderId, path) {
    var folder = DriveApp.getFolderById(folderId);
    var folders = folder.getFolders();

    // 扫描子文件夹
    while (folders.hasNext()) {
      var subfolder = folders.next();
      var subfolderName = subfolder.getName();
      var currentPath = path ? path + '/' + subfolderName : subfolderName;

      Logger.log('Scanning: ' + currentPath);
      scanFolder(subfolder.getId(), currentPath);
    }

    // 扫描视频文件
    var files = folder.getFiles();
    while (files.hasNext()) {
      var file = files.next();
      var fileName = file.getName();

      if (fileName.endsWith('.mp4')) {
        var clipId = fileName.replace('.mp4', '');
        var fileId = file.getId();
        mapping[clipId] = fileId;
        Logger.log('  Found: ' + clipId + ' -> ' + fileId);
      }
    }
  }

  // 开始扫描
  Logger.log('Starting scan...');
  scanFolder(FOLDER_ID, '');

  // 输出结果
  Logger.log('');
  Logger.log('Total videos found: ' + Object.keys(mapping).length);
  Logger.log('');
  Logger.log('Copy the JSON below to data/video_mapping.json:');
  Logger.log('================================================================');
  Logger.log(JSON.stringify(mapping, null, 2));
  Logger.log('================================================================');

  // 也创建一个文本文件在 Drive 中
  var jsonContent = JSON.stringify(mapping, null, 2);
  var folder = DriveApp.getFolderById(FOLDER_ID);
  var file = folder.createFile('video_mapping.json', jsonContent, MimeType.PLAIN_TEXT);
  Logger.log('');
  Logger.log('Also saved to Google Drive: ' + file.getUrl());
}
```

#### 4. 运行脚本

1. 点击工具栏的 "运行" 按钮（播放图标）
2. 选择函数 `generateVideoMapping`
3. 首次运行会要求授权 - 点击"审核权限"并授权
4. 等待脚本运行完成（可能需要1-2分钟）

#### 5. 查看结果

1. 点击 "查看" → "日志" 或 "执行日志"
2. 复制 JSON 输出
3. 粘贴到 `data/video_mapping.json`

**或者**：脚本会在你的 Google Drive 根文件夹中创建 `video_mapping.json` 文件，直接下载即可！

---

## 备用方法：API Key 配置

如果 API Key 返回 403 错误，需要：

### 1. 启用 Google Drive API

1. 访问: https://console.cloud.google.com/apis/library/drive.googleapis.com
2. 确保选择了正确的项目
3. 点击 "启用"

### 2. 配置 API Key 权限

1. 访问: https://console.cloud.google.com/apis/credentials
2. 点击你的 API Key
3. 在 "API 限制" 部分：
   - 选择 "限制密钥"
   - 勾选 "Google Drive API"
   - 点击 "保存"

### 3. 重新运行扫描

```bash
python create_google_drive_mapping.py
```

选择选项 1，输入你的 API Key。

---

## 最快速的手动方法

如果你想快速开始：

1. 打开 Google Drive 文件夹
2. 进入一个 DAY 文件夹（如 A3_TASHA/DAY1）
3. 选择所有视频文件（Ctrl+A）
4. 右键 → "获取链接"
5. 运行我们的批量导入工具：

```bash
python batch_import_google_drive.py
```

6. 粘贴所有链接（一次性粘贴或逐个粘贴都可以）
7. 工具会自动提取文件 ID

重复步骤 2-6 for 每个文件夹（DAY1-DAY7, 不同人物）。

---

## 推荐方式

**Google Apps Script** 是最简单的方式 - 一次运行即可获取所有视频映射！
