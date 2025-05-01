
import streamlit as st
from openai import OpenAI

def run():
    st.title("💬 Trợ lý ChatGPT - AI Thế Anh")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "Bạn là trợ lý AI hữu ích"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                stream=True,
            ):
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
