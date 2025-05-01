import streamlit as st
import importlib
import os

# ===============================
# Thiết lập cấu hình trang
# ===============================
st.set_page_config(
    page_title="AI Thế Anh – MultiApp Suite",
    layout="wide",
    page_icon="🤖"
)

st.image("logo.png", use_container_width=True)
st.markdown("## 💼 AI Thế Anh – Trợ lý AI đa nhiệm")

# ===============================
# Khởi tạo multi-app
# ===============================
APP_DIR = "app_modules"
app_files = [f for f in os.listdir(APP_DIR) if f.endswith(".py") and not f.startswith("__")]

# Tên hiển thị sidebar
app_display_names = {
    "promptbot.py": "🎨 PromptBot – Tạo hình ảnh",
    "tax_lookup.py": "🧾 Tra cứu mã số thuế",
    "analysis_dashboard.py": "📊 Dashboard phân tích dữ liệu",
    "chat_gpt_assistant.py": "🤖 Trợ lý ChatGPT",
    "download_app.py": "📁 Tải file từ Excel"
}

selected_file = st.sidebar.selectbox("🔍 Chọn chức năng", [app_display_names.get(f, f) for f in app_files])

# Mapping lại để lấy tên file từ tên hiển thị
selected_filename = [k for k, v in app_display_names.items() if v == selected_file][0]
module_path = f"{APP_DIR}.{selected_filename.replace('.py','')}"
module = importlib.import_module(module_path)
module.app()
