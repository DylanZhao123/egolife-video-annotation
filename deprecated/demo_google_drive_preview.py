"""
Google Drive Video Preview Demo
演示Google Drive视频预览功能
"""

import streamlit as st

st.set_page_config(page_title="Google Drive Video Preview Test", layout="wide")

st.title("Google Drive Video Preview Demo")
st.title("Google Drive视频预览演示")

st.write("---")

# Your test video
file_id = "1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy"

st.write("## Method 1: Preview URL (No Download Button)")
st.write("## 方法1：预览URL（无下载按钮）")

preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
st.write(f"**Preview URL:** `{preview_url}`")

st.markdown(f"""
<iframe
    src="{preview_url}"
    width="800"
    height="600"
    allow="autoplay"
    frameborder="0"
    allowfullscreen>
</iframe>
""", unsafe_allow_html=True)

st.write("---")

st.write("## Method 2: Direct Download URL with st.video()")
st.write("## 方法2：直接下载URL配合st.video()")

download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
st.write(f"**Download URL:** `{download_url}`")

try:
    st.video(download_url)
except Exception as e:
    st.error(f"Failed to load: {e}")

st.write("---")

st.info("""
### Summary / 总结

**Method 1 (iframe preview):**
- Pros: Embeds Google Drive's video player, looks professional
- Cons: May show Google Drive controls, users can still download via right-click

**方法1（iframe预览）：**
- 优点：嵌入Google Drive视频播放器，看起来专业
- 缺点：可能显示Google Drive控件，用户仍可通过右键下载

---

**Method 2 (st.video with download URL):**
- Pros: Uses Streamlit's native video player, clean interface
- Cons: Video is downloadable via browser

**方法2（st.video配合下载URL）：**
- 优点：使用Streamlit原生视频播放器，界面简洁
- 缺点：视频可通过浏览器下载

---

**Recommendation / 建议:**
- For maximum protection: Use Method 1
- For better user experience: Use Method 2
- Note: 100% download prevention is impossible, but Method 1 makes it harder

**推荐：**
- 最大保护：使用方法1
- 更好体验：使用方法2
- 注意：100%防止下载是不可能的，但方法1会增加难度
""")
