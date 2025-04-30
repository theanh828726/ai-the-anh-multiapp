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

# ✅ API Key GPT
OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# ===========================
# 📜 Danh sách style + tag
# ===========================
style_categories = {
    "🎨 Phong cách hội họa": [
        ("Oil Painting", "Tranh sơn dầu, nét dày, cổ điển"),
        ("Watercolor", "Tranh màu nước, nhẹ nhàng, trong trẻ"),
        ("Ink Wash / Sumi-e", "Tranh thủy mặc, phong cách Á Đông"),
        ("Gouache", "Tranh bột màu, đậm nét, cổ tích"),
        ("Fresco", "Tranh tường, thời Phục Hưng"),
        ("Impressionism", "Tranh ấn tượng, nét vẻ mờ ảo như Monet"),
        ("Expressionism", "Biểu cảm mạnh mẽ, cảm xúc mãnh liệt"),
        ("Cubism", "Lập thể kiểu Picasso"),
        ("Surrealism", "Siêu thực kiểu Dali"),
        ("Pop Art", "Sặc sỡ, kiểu Andy Warhol")
    ],
    "📷 Phong cách nhiếp ảnh": [
        ("Portrait", "Ảnh chân dung"),
        ("Cinematic", "Ánh sáng điện ảnh, cực nghệ"),
        ("Black & White", "Đen trắng, sâu lắng"),
        ("HDR", "Rực rỡ, độ tương phản cao"),
        ("Vintage", "Cổ điển, hoài niệm"),
        ("Macro", "Cận cảnh chi tiết nhỏ"),
        ("Bokeh", "Phông nền mờ, điểm sáng lung linh"),
        ("Photojournalism", "Báo chí chân thực"),
        ("Fashion Editorial", "Tạp chí thời trang chuyên nghiệp")
    ],
    "🎨 Kỹ thuật số & Hiện Đại": [
        ("Digital Painting", "Vẽ kỹ thuật số"),
        ("Vector Art", "Nét gọn, đồ họa phẳng"),
        ("Low Poly", "Mô hình đa giác đơn giản"),
        ("Pixel Art", "Phong cách game 8-bit"),
        ("Glitch Art", "Lỗi kỹ thuật, hiệu ứng “điện giật”"),
        ("Synthwave / Vaporwave", "Neon tím, thập niên 80s"),
        ("Cyberpunk", "Tương lai tối tăm, công nghệ cao"),
        ("Futuristic", "Viễn tưởng, hiện đại hóa mạnh")
    ],
    "🙌 Truyện tranh & Hoạt hình": [
        ("Anime", "Hoạt hình Nhật Bản"),
        ("Manga Style", "Truyện tranh trắng đen Nhật Bản"),
        ("Disney / Pixar", "Dễ thương, hoạt hình 3D"),
        ("Cartoon", "Kiểu hoạt hình truyền thống"),
        ("Comic Book", "Truyện tranh Mỹ kiểu Marvel/DC"),
        ("Chibi", "Nhân vật đầu to, cực kỳ dễ thương")
    ],
    "💎 Nghệ thuật cao cấp / Phức tạp": [
        ("Concept Art", "Dành cho dựng cảnh, nhân vật fantasy"),
        ("Matte Painting", "Hậu cảnh điện ảnh hoành tráng"),
        ("Steampunk", "Cơ khí cổ điển, bánh răng kim loại"),
        ("Art Nouveau", "Hoa văn uốn lượn kiểu châu Âu thế kỷ 19"),
        ("Baroque", "Cầu kỳ, xa hoa kiểu châu Âu cổ"),
        ("Gothic", "U ám, cổ kính kiểu nhà thờ"),
        ("Fantasy", "Thế giới phép thuật, rồng, elf…"),
        ("Dark Art", "Kỳ bí, kinh dị, u tối")
    ],
    "🧘 Lối sống / Con người / Tình cảm": [
        ("Minimalist", "Tối giản, tinh tế"),
        ("Dreamcore / Liminal", "Ảo mộng, không gian lắng chừng ký ức"),
        ("Realistic / Hyper Realistic", "Siêu thực, như thật 100%"),
        ("Emotional Portrait", "Chân dung biểu cảm mạnh"),
        ("Fashion Lookbook", "Gợi cảm, thời trang ấn tượng"),
        ("Candid", "Khoảnh khắc đời thường không dàn dựng")
    ]
}

style_tags = {
    "Cinematic": "cinematic lighting, ultra detail, depth of field, 8k",
    "Portrait": "natural skin texture, soft lighting, shallow depth of field",
    "Fantasy": "epic composition, glowing effects, dynamic lighting",
    "Oil Painting": "oil painting style, thick brush strokes, classical look",
    "Watercolor": "watercolor texture, gentle color palette, artistic effect",
    "Surrealism": "dreamlike scene, floating objects, vivid colors"
}

# ===========================
# ⚙️ UI Setup
# ===========================
st.set_page_config(page_title="PromptBot All-in-One", layout="wide")
st.title(":robot_face: PromptBot: All-in-One: Trợ lý tạo hình ảnh đa năng 📋")

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

# =======================
# 🎨 Tạo ảnh từ DALL·E
# =======================

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