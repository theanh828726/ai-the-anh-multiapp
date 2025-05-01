import streamlit as st

def run():
    st.title("💬 Trợ lý ChatGPT")
    query = st.text_input("Nhập câu hỏi:")
    if st.button("Trả lời"):
        if query:
            st.success("✅ Trợ lý đang suy nghĩ... (giả lập)")
        else:
            st.warning("Hãy nhập câu hỏi để được trợ giúp.")
