
import streamlit as st

def run():
    st.title("🔍 Tra cứu mã số thuế (demo)")
    st.write("Chức năng tra cứu MST thực tế có captcha, sẽ được cập nhật.")
    mst = st.text_input("Nhập mã số thuế:")
    if st.button("Tra cứu"):
        if mst:
            st.success(f"✅ Đã tra cứu mã: {mst}")
        else:
            st.warning("Vui lòng nhập mã số thuế.")
