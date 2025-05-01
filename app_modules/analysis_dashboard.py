import streamlit as st
import pandas as pd

def run():
    st.title("📊 Dashboard Phân tích dữ liệu - AI Thế Anh")
    uploaded_file = st.file_uploader("Chọn file Excel cần phân tích", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.subheader("📄 Xem trước 5 dòng đầu:")
        st.dataframe(df.head())
