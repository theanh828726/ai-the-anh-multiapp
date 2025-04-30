# 🚀 PromptBot All-in-One: 3 Chế độ - Chat 💬 + Form 📋 + Công Thức 📄

import streamlit as st
from openai import OpenAI
import pandas as pd
import random
from io import BytesIO
import requests
import os
from PIL import Image

# ✅ API Key GPT
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 💬 Basic Chat Example (rút gọn lại cho minh hoạ)
st.title("🤖 Thế Anh - Trợ lý AI đa năng")
st.write("Xin chào! Tôi là trợ lý AI Thế Anh. Bạn cần tôi giúp gì hôm nay?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Nhập nội dung cần trao đổi ở đây nhé?"):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI Thế Anh – phong cách truyền cảm hứng, cảm xúc, logic, danh dự."},
                *st.session_state.messages
            ],
            temperature=0.7,
            stream=False,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ Lỗi khi gọi OpenAI: {e}"

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})