import streamlit as st
from app_modules import promptbot, tax_lookup, analysis_dashboard, chat_gpt_assistant, download_app

st.set_page_config(page_title="AI Thế Anh – MultiApp", layout="wide")

# Sidebar menu
st.sidebar.title("🧠 AI Thế Anh – Ứng dụng đa năng")
app_mode = st.sidebar.radio(
    "Chọn chức năng:",
    (
        "📤 Tải file", 
        "🤖 PromptBot", 
        "📊 Phân tích dữ liệu", 
        "🔍 Tra cứu mã số thuế", 
        "💬 Trợ lý ChatGPT"
    )
)

# Gọi module tương ứng
if app_mode == "📤 Tải file":
    download_app.run()
elif app_mode == "🤖 PromptBot":
    promptbot.run()
elif app_mode == "📊 Phân tích dữ liệu":
    analysis_dashboard.run()
elif app_mode == "🔍 Tra cứu mã số thuế":
    tax_lookup.run()
elif app_mode == "💬 Trợ lý ChatGPT":
    chat_gpt_assistant.run()