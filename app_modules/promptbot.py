import streamlit as st
from openai import OpenAI

def run():
    st.title("🤖 PromptBot - AI hỗ trợ tạo Prompt")
    api_key = st.secrets["OPENAI_API_KEY"]
    prompt = st.text_area("Nhập prompt bạn muốn cải tiến:")
    if st.button("Tạo Prompt"):
        if prompt:
            st.success(f"✅ Prompt được xử lý: {prompt} 🔁")
        else:
            st.warning("Vui lòng nhập prompt trước khi tạo.")
