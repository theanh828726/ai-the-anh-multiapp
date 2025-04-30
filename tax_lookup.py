import streamlit as st
from pathlib import Path

logo_path = Path("logo.png")
if logo_path.exists():
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image(str(logo_path), use_container_width=True)

st.title('Tra cứu mã số thuế')
st.write('Tự động kiểm tra thông tin MST.')