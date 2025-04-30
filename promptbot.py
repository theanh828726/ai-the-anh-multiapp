
import streamlit as st
from openai import OpenAI
import pandas as pd
from datetime import datetime
import random
from PIL import Image

# ✅ Cấu hình trang phải đặt đầu tiên
st.set_page_config(page_title="PromptBot All-in-One", layout="wide")

# ✅ Gắn logo MEGA
st.image("logo.png", use_container_width=True)

# ✅ Lấy API key từ secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Giao diện người dùng
st.title("🚀 PromptBot All-in-One: 3 Chế độ - Chat 💬 + Form 📝 + Công Thức 📋")
mode = st.selectbox("Chọn chế độ sử dụng:", ["Chat 💬", "Form 📝", "Công Thức 📋"])

# Khởi tạo session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chế độ Chat
if mode == "Chat 💬":
    st.subheader("💬 Trò chuyện với trợ lý AI")
    user_input = st.text_input("Nhập nội dung cần trao đổi ở đây nhé?")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("🤖 Đang trả lời..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            ).choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.success(response)

# Chế độ Form
elif mode == "Form 📝":
    st.subheader("📋 Nhập thông tin để tạo nội dung")
    name = st.text_input("Tên bạn là?")
    topic = st.text_input("Bạn muốn tạo nội dung về chủ đề gì?")
    tone = st.selectbox("Chọn giọng điệu:", ["Chuyên nghiệp", "Hài hước", "Truyền cảm hứng"])
    if st.button("Tạo nội dung"):
        prompt = f"Tạo nội dung về {topic} với giọng điệu {tone} dành cho người tên {name}."
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        st.info(response)

# Chế độ Công Thức
elif mode == "Công Thức 📋":
    st.subheader("📋 Nhập yêu cầu để sinh prompt công thức")
    goal = st.text_area("Mục tiêu bạn muốn đạt được?")
    if st.button("Sinh công thức"):
        prompt = f"Viết prompt công thức hiệu quả để đạt mục tiêu: {goal}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        st.info(response)
