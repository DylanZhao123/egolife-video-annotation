# Google Sheets 集成指南

## 为什么需要Google Sheets？

Streamlit Cloud不支持文件持久化，答案会在重启后丢失。
Google Sheets可以：
- ✅ 实时自动保存所有答案
- ✅ 多人同时标注
- ✅ 随时查看进度
- ✅ 导出为Excel/CSV

---

## 快速设置（15分钟）

### 步骤1：创建Google Sheets表格

1. 访问：https://sheets.google.com
2. 创建新表格，命名：`Video_Annotation_Responses`
3. 第一行设置表头：
   ```
   sample_id | user_id | user_answer | correct_answer | is_correct | time_spent_seconds | timestamp
   ```

### 步骤2：获取Google API凭证

1. 访问：https://console.cloud.google.com
2. 创建新项目："VideoAnnotation"
3. 启用API：Google Sheets API
4. 创建服务账号
5. 下载JSON密钥文件（重命名为 `credentials.json`）

### 步骤3：分享表格给服务账号

1. 打开 `credentials.json`，找到 `client_email`
2. 在Google Sheets中点击"共享"
3. 将服务账号邮箱添加为编辑者

### 步骤4：配置Streamlit Secrets

在Streamlit Cloud：
1. 进入你的应用设置
2. 找到 "Secrets" 部分
3. 添加：

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "your-private-key"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"

[sheets]
spreadsheet_id = "your-spreadsheet-id"
```

### 步骤5：安装依赖

在 `requirements.txt` 添加：
```
gspread==5.12.0
oauth2client==4.1.3
```

### 步骤6：修改代码（我会帮你做）

需要修改 `utils/response_recorder.py` 来支持Google Sheets。

---

## 简化方案：使用Streamlit提供的数据连接

Streamlit有内置的Google Sheets连接器：

### 更简单的方法（推荐）：

在 `requirements.txt` 添加：
```
streamlit-gsheets-connection
```

然后在代码中：
```python
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 连接到Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 读取数据
df = conn.read()

# 写入数据
conn.update(data=new_data)
```

---

## 快速启用（我可以帮你）

如果你想启用Google Sheets：

1. 告诉我你想使用哪种方案
2. 我会修改代码
3. 提交并推送更新
4. Streamlit自动重新部署

---

## 或者：使用现有的导出功能

如果觉得Google Sheets太复杂，可以：

**定期提醒标注人员**：
- 每完成10-20题点击"Export Responses"
- 下载文件发送给你
- 你合并所有文件

这样简单但需要手动操作。
