import streamlit as st

def run():
    st.title("🧾 Tra cứu mã số thuế")
    tax_code = st.text_input("Nhập mã số thuế:")
    if st.button("Tra cứu"):
        if tax_code:
            st.success(f"✅ Kết quả tra cứu MST: {tax_code}")
        else:
            st.warning("Vui lòng nhập mã số thuế.")
