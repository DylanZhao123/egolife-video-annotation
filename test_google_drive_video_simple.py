"""
Simple test to verify Google Drive video embedding works
"""

import streamlit as st

st.set_page_config(page_title="Google Drive Video Test", layout="wide")

st.title("Google Drive Video Embedding Test")

# Test file ID
FILE_ID = "1eMiFjV4WkhcvM8qm-s49gGP8vFyRKSoy"

st.write(f"**Testing Google Drive File ID:** `{FILE_ID}`")

# Different URL formats
preview_url = f"https://drive.google.com/file/d/{FILE_ID}/preview"
uc_url = f"https://drive.google.com/uc?id={FILE_ID}"
view_url = f"https://drive.google.com/file/d/{FILE_ID}/view"

st.markdown("---")

# Test 1: Preview URL
st.subheader("1. Preview URL (Recommended)")
st.write(f"`{preview_url}`")
try:
    st.video(preview_url)
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# Test 2: Direct download URL
st.subheader("2. Direct Download URL (uc?id=)")
st.write(f"`{uc_url}`")
try:
    st.video(uc_url)
except Exception as e:
    st.error(f"Error: {e}")

st.markdown("---")

# Test 3: iframe embed
st.subheader("3. iframe Embed")
iframe_html = f"""
<iframe src="{preview_url}"
        width="640"
        height="480"
        frameborder="0"
        allow="autoplay">
</iframe>
"""
st.markdown(iframe_html, unsafe_allow_html=True)

st.markdown("---")

# Test 4: External link
st.subheader("4. External Link Button")
st.link_button("Open in Google Drive", view_url)

st.markdown("---")

st.success("✓ Test complete! Check which format works best above.")
st.info("If videos don't load, ensure:\n1. Files are set to 'Anyone with the link can view'\n2. Files are actually video files (.mp4)")
