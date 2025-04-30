import streamlit as st
from openai import OpenAI

# ----- Hàm đọc nội dung từ file -----
def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()

# ----- Hiển thị logo -----
try:
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image("logo.png", use_container_width=True)
except:
    pass

# ----- Tiêu đề mở đầu -----
title_content = rfile("00.xinchao.txt")
st.markdown(f"""<h1 style="text-align: center; font-size: 24px;">{title_content}</h1>""", unsafe_allow_html=True)

# ----- API Key từ secrets -----
openai_api_key = st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# ----- Đọc nội dung huấn luyện từ các file .txt -----
INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": rfile("01.system_trainning.txt")}
INITIAL_ASSISTANT_MESSAGE = {"role": "assistant", "content": rfile("02.assistant.txt")}

# ----- Session khởi tạo lần đầu -----
if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

# ----- Style trái phải -----
st.markdown("""
    <style>
        .assistant {
            padding: 10px;
            border-radius: 10px;
            max-width: 75%;
            text-align: left;
        }
        .user {
            padding: 10px;
            border-radius: 10px;
            max-width: 75%;
            text-align: right;
            margin-left: auto;
        }
        .assistant::before { content: "🤖 Thế Anh - "; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ----- Hiển thị hội thoại cũ -----
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="assistant">{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "user":
        st.markdown(f'<div class="user">{message["content"]}</div>', unsafe_allow_html=True)

# ----- Nhập liệu người dùng -----
if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user">{prompt}</div>', unsafe_allow_html=True)

    # ----- Gọi OpenAI API -----
    response = ""
    model = rfile("module_chatgpt.txt").strip()
    st.success(f"✅ Model đang dùng: {model}")

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                st.markdown(f'<div class="assistant">{response}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Lỗi khi gọi OpenAI: {e}")

    st.session_state.messages.append({"role": "assistant", "content": response})
