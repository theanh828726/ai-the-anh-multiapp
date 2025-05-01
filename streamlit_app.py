# streamlit_app.py
import streamlit as st
import importlib
import os

st.set_page_config(page_title="AI Thế Anh – MultiApp Suite", layout="wide")

st.sidebar.title("📌 Menu Tính năng")
st.title("🚀 AI Thế Anh – MultiApp Dashboard")
st.markdown("Hệ thống gồm nhiều công cụ tự động hóa và phân tích thông minh.")

# Tìm các app con
apps = {}
for file in os.listdir():
    if file.endswith(".py") and file not in ["streamlit_app.py", "__init__.py"]:
        try:
            mod = importlib.import_module(file.replace(".py", ""))
            if hasattr(mod, "app"):
                apps[file.replace(".py", "").replace("_", " ").title()] = mod
        except Exception as e:
            st.sidebar.warning(f"⚠️ Không thể import {file}: {e}")

# Chọn app
selection = st.sidebar.radio("🔽 Chọn ứng dụng", list(apps.keys()))

# Chạy app
if selection:
    apps[selection].app()