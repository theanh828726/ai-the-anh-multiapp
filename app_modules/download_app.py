import streamlit as st

def run():
    st.title("📥 Tải file xuống")
    content = "Dữ liệu mẫu để tải về"
    st.download_button("Tải xuống nội dung", content, file_name="sample.txt")
