import streamlit as st
import importlib
import os

st.set_page_config(page_title="AI Thế Anh – MultiApp Suite", layout="wide")
st.image("logo.png", use_column_width=True)
st.title("🚀 AI Thế Anh – MultiApp Dashboard")
st.markdown("Hệ thống gồm nhiều công cụ hỗ trợ doanh nghiệp bằng trí tuệ nhân tạo.")

# ===========================
# KHAI BÁO DANH SÁCH APP
# ===========================
apps = {
    "🎨 PromptBot – Tạo hình ảnh": "promptbot",
    "🧾 Tra cứu mã số thuế": "tax_lookup",
    "📊 Phân tích dữ liệu": "analysis_dashboard",
    "🤖 Trợ lý ChatGPT": "chat_gpt_assistant",
    "📥 Tải file tự động": "download_app"
}

# ===========================
# SIDEBAR CHỌN APP
# ===========================
choice = st.sidebar.selectbox("📂 Chọn chức năng", list(apps.keys()))
module_name = apps[choice]

# ===========================
# IMPORT & CHẠY APP
# ===========================
module = importlib.import_module(module_name)
if hasattr(module, "app"):
    module.app()
else:
    st.error(f"❌ Ứng dụng '{choice}' chưa có hàm app(). Vui lòng kiểm tra lại.")