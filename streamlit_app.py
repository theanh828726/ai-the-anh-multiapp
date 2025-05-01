from app_modules import promptbot, tax_lookup, analysis_dashboard, chat_gpt_assistant, download_app
import streamlit as st

st.set_page_config(page_title="AI Thế Anh - Ứng dụng đa năng", layout="wide")

st.sidebar.markdown("### 🧠 AI Thế Anh – Ứng dụng đa năng")
app_choice = st.sidebar.radio("Chọn chức năng:", (
    "📂 Tải file", "🤖 PromptBot", "📊 Phân tích dữ liệu", "🧾 Tra cứu mã số thuế", "💬 Trợ lý ChatGPT"))

if app_choice == "📂 Tải file":
    download_app.run()

elif app_choice == "🤖 PromptBot":
    promptbot.run()

elif app_choice == "📊 Phân tích dữ liệu":
    analysis_dashboard.run()

elif app_choice == "🧾 Tra cứu mã số thuế":
    tax_lookup.run()

elif app_choice == "💬 Trợ lý ChatGPT":
    chat_gpt_assistant.run()