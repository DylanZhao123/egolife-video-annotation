"""
Test Google Drive Public Video Access in Streamlit
测试Google Drive公开视频在Streamlit中的访问
"""

import streamlit as st
import requests

st.title("Google Drive Video Access Test")
st.title("Google Drive视频访问测试")

# Original share link
share_url = "https://drive.google.com/file/d/1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy/view?usp=sharing"
file_id = "1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy"

st.write("## Testing Different URL Formats")
st.write("## 测试不同的URL格式")

# Format 1: Direct download
direct_download = f"https://drive.google.com/uc?export=download&id={file_id}"
st.write("### Format 1: Direct Download URL")
st.write(direct_download)

# Test if accessible
try:
    response = requests.head(direct_download, allow_redirects=True, timeout=5)
    st.write(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        st.success("✅ Accessible without login!")
        st.write(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
        st.write(f"Content-Length: {response.headers.get('Content-Length', 'Unknown')} bytes")
    else:
        st.error(f"❌ Not accessible (Status: {response.status_code})")
except Exception as e:
    st.error(f"❌ Error: {e}")

st.write("---")

# Format 2: Preview/embed URL
preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
st.write("### Format 2: Preview/Embed URL")
st.write(preview_url)

# Try embedding with iframe
st.write("#### Attempting to embed video:")
st.markdown(f"""
<iframe src="{preview_url}"
        width="640"
        height="480"
        allow="autoplay"
        frameborder="0">
</iframe>
""", unsafe_allow_html=True)

st.write("---")

# Format 3: Using st.video with direct download
st.write("### Format 3: Streamlit st.video() with Direct URL")
try:
    st.video(direct_download)
    st.success("✅ Video loaded in st.video()")
except Exception as e:
    st.error(f"❌ Failed to load in st.video(): {e}")

st.write("---")

# Format 4: Check if authentication needed
st.write("### Format 4: Test Public Access")
try:
    response = requests.get(direct_download, stream=True, timeout=10)

    if response.status_code == 200:
        # Check if we got actual video data or a login redirect
        content_type = response.headers.get('Content-Type', '')

        if 'video' in content_type:
            st.success(f"✅ SUCCESS! Got video data directly!")
            st.write(f"Content-Type: {content_type}")

            # Show first few bytes
            first_bytes = next(response.iter_content(1024))
            st.write(f"First 20 bytes: {first_bytes[:20]}")

        elif 'text/html' in content_type:
            st.error("❌ Got HTML (likely login page or redirect)")
            st.write("This means the video is NOT publicly accessible")
        else:
            st.warning(f"⚠️ Unexpected content type: {content_type}")
    else:
        st.error(f"❌ HTTP {response.status_code}")

except Exception as e:
    st.error(f"❌ Request failed: {e}")

st.write("---")

st.write("## Summary / 总结")
st.info("""
**If Format 1 or 3 works**: Google Drive public sharing is working ✅

**If all formats fail**: Need to change sharing settings or use different hosting

**如果格式1或3有效**：Google Drive公开分享正常工作 ✅

**如果所有格式都失败**：需要更改分享设置或使用其他托管方式
""")
