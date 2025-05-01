import streamlit as st

# Import từng module từ thư mục app_modules
from app_modules import (
    promptbot,
    tax_lookup,
    analysis_dashboard,
    chat_gpt_assistant,
    download_app
)

# Cấu hình trang
st.set_page_config(
    page_title="AI Thế Anh – Ứng dụng đa năng",
    page_icon="💡",
    layout="wide"
)

# Sidebar chọn chức năng
st.sidebar.title("💡 AI Thế Anh – Ứng dụng đa năng")
st.sidebar.markdown("### Chọn chức năng:")
option = st.sidebar.radio(
    "Chức năng:",
    (
        "📁 Tải file",
        "🤖 PromptBot",
        "📊 Phân tích dữ liệu",
        "🔍 Tra cứu mã số thuế",
        "💬 Trợ lý ChatGPT"
    ),
    label_visibility="collapsed"
)

# Điều hướng theo chức năng
if option == "📁 Tải file":
    download_app.run()

elif option == "🤖 PromptBot":
    promptbot.run()

elif option == "📊 Phân tích dữ liệu":
    analysis_dashboard.run()

elif option == "🔍 Tra cứu mã số thuế":
    tax_lookup.run()

elif option == "💬 Trợ lý ChatGPT":
    chat_gpt_assistant.run()

else:
    st.warning("Hãy chọn một chức năng từ thanh bên.")
