@echo off
cd /d "C:\Users\Dylan\LabStuff\VidsAnnotaionWebsite"
echo Starting Streamlit application...
python -m streamlit run app.py --server.headless=true
