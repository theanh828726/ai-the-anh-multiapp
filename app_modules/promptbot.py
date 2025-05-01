
import streamlit as st
from openai import OpenAI

def run():
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    st.title("🎨 PromptBot - Sinh ảnh với DALL·E 3")
    prompt = st.text_area("Mô tả ảnh bạn muốn tạo:", height=150)
    if st.button("Tạo ảnh"):
        try:
            res = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
            img_url = res.data[0].url
            st.image(img_url, caption="Ảnh do AI tạo", use_column_width=True)
        except Exception as e:
            st.error(f"Lỗi: {e}")
