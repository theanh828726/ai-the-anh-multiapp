import streamlit as st
from pathlib import Path
from openai import OpenAI

def run():
        # ====== Load nội dung từ file txt ======
    def rfile(name_file):
        with open(name_file, "r", encoding="utf-8") as file:
            return file.read()

    # Tiêu đề chào
    try:
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            st.image("logo.png", use_container_width=True)
    except:
        pass

    title_content = rfile("00.xinchao.txt")
    st.markdown(f"""<h1 style="text-align: center; font-size: 24px;">{title_content}</h1>""", unsafe_allow_html=True)

    # ====== API key ======
    openai_api_key = st.secrets.get("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    # ====== Tin nhắn hệ thống & ban đầu ======
    INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": rfile("01.system_trainning.txt")}
    INITIAL_ASSISTANT_MESSAGE = {"role": "assistant", "content": rfile("02.assistant.txt")}

    if "messages" not in st.session_state:
        st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

    # ====== CSS giao diện chat ======
    st.markdown(
        """
        <style>
            .assistant {
                padding: 10px;
                border-radius: 10px;
                max-width: 75%;
                background: none;
                text-align: left;
            }
            .user {
                padding: 10px;
                border-radius: 10px;
                max-width: 75%;
                background: none;
                text-align: right;
                margin-left: auto;
            }
            .assistant::before { content: "🤖 "; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ====== Hiển thị lịch sử chat ======
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f'<div class="assistant">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "user":
            st.markdown(f'<div class="user">{message["content"]}</div>', unsafe_allow_html=True)

    # ====== Nhập nội dung ======
    if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f'<div class="user">{prompt}</div>', unsafe_allow_html=True)

        response = ""
        model = rfile("module_chatgpt.txt").strip()
        messages = st.session_state.messages
        st.write("✅ Model đang dùng:", model)

        # ====== Gọi OpenAI stream ======
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            if chunk.choices:
                response += chunk.choices[0].delta.content or ""

        st.markdown(f'<div class="assistant">{response}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
