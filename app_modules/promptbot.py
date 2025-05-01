# 🚀 PromptBot All-in-One: Trợ lý tạo hình ảnh đa năng 📋
import streamlit as st
from openai import OpenAI
from datetime import datetime
import pandas as pd
import random
from io import BytesIO
import requests
import os
from PIL import Image

def run():
    # ✅ API Key GPT
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # ===========================
    # 📜 Danh sách style + tag
    # ===========================
    style_categories = {
        "🎨 Phong cách hội họa": [
            ("Oil Painting", "Tranh sơn dầu, nét dày, cổ điển"),
            ("Watercolor", "Tranh màu nước, nhẹ nhàng, trong trẻ"),
            #... (rút gọn cho ngắn gọn)
        ]
    }

    style_tags = {
        "Cinematic": "cinematic lighting, ultra detail, depth of field, 8k",
        "Portrait": "natural skin texture, soft lighting, shallow depth of field"
    }

    # ⚙️ UI Setup
    st.set_page_config(page_title="PromptBot All-in-One", layout="wide")
    st.title(":robot_face: All-in-One - Trợ lý tạo hình ảnh đa năng - AI Thế Anh 📋")

    mode = st.sidebar.selectbox("😊 Chế độ sử dụng", ["💬 Chatbot", "🗘️ Form truyền thống", "📋 Prompt công thức"])
    style_group = st.sidebar.selectbox("🎨 Nhóm phong cách:", list(style_categories.keys()))
    style = st.sidebar.selectbox("🌟 Phong cách cụ thể:", [s[0] for s in style_categories[style_group]])
    default_tag = style_tags.get(style, "ultra detail, high resolution")
    tags = st.sidebar.text_area("🌟 Từ khoá nâng cao:", value=default_tag)

    if mode == "📋 Prompt công thức":
        st.subheader("🔧 Nhập thông tin để tạo Prompt")
        col1, col2 = st.columns(2)
        with col1:
            subject = st.text_input("👤 Chủ thể:", placeholder="Ví dụ: Một cô gái mặc áo dài")
            action = st.text_input("🎨 Hành động:", placeholder="Ví dụ: Đang đi bên bờ hồ")
            scene = st.text_input("🌄 Bối cảnh:", placeholder="Ví dụ: Hồ Hoàn Kiếm lúc hoàng hôn")
            mood = st.text_input("🔦 Ánh sáng / Cảm xúc:", placeholder="Ví dụ: Ánh sáng vàng nhẹ, lung linh")
        if st.button("🚀 Tạo Prompt"):
            prompt_vn = f"{subject} {action}, {scene}, {mood}, {style}, {tags}"
            prompt_en = prompt_vn
            st.success(f"**🇻🇳 Prompt tiếng Việt:** {prompt_vn}")
            st.code(f"{prompt_en}", language="markdown")

    def generate_image(prompt, size="1024x1024"):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1
        )
        return response.data[0].url

    with st.expander("🖼️ Tạo ảnh với DALL·E"):
        with st.form("dalle_form"):
            prompt = st.text_input("Nhập mô tả để tạo ảnh bằng DALL·E")
            submitted = st.form_submit_button("Tạo ảnh 🎨")
            if submitted and prompt:
                with st.spinner("Đang tạo ảnh bằng DALL·E..."):
                    image_url = generate_image(prompt)
                    st.image(image_url, caption="Ảnh được tạo bởi DALL·E")