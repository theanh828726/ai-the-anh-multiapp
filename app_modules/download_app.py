
import streamlit as st
import pandas as pd
import requests

def run():
    st.title("📥 Tải file từ danh sách Excel")
    uploaded_file = st.file_uploader("Chọn file Excel có cột URL", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        url_column = st.selectbox("Chọn cột chứa URL:", df.columns)
        if st.button("Bắt đầu tải"):
            for idx, row in df.iterrows():
                url = row[url_column]
                try:
                    r = requests.get(url)
                    filename = url.split("/")[-1]
                    with open(f"downloads/{filename}", "wb") as f:
                        f.write(r.content)
                    st.success(f"Đã tải: {filename}")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
