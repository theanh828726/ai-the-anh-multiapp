import streamlit as st
from openai import OpenAI

def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        return file.read()

# Hiển thị logo giữa
try:
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image("logo.png", use_container_width=True)
except:
    pass

# Tiêu đề
st.markdown(f"<h1 style='text-align: center; font-size: 24px;'>{rfile('00.xinchao.txt')}</h1>", unsafe_allow_html=True)

# API Key từ secrets
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# Khởi tạo prompt hệ thống
INITIAL_SYSTEM_MESSAGE = {"role": "system", "content": rfile("01.system_trainning.txt")}
INITIAL_ASSISTANT_MESSAGE = {"role": "assistant", "content": rfile("02.assistant.txt")}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

# Style hội thoại
st.markdown("""
<style>
.assistant {
    padding: 10px; border-radius: 10px; max-width: 75%;
    text-align: left; background-color: #f1f1f1;
}
.user {
    padding: 10px; border-radius: 10px; max-width: 75%;
    text-align: right; margin-left: auto;
    background-color: #dcf3ff;
}
.assistant::before {
    content: "🤖 Thế Anh - ";
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Hiển thị hội thoại trước
for msg in st.session_state.messages:
    role_class = "assistant" if msg["role"] == "assistant" else "user"
    st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# Nhận prompt người dùng
if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user">{prompt}</div>', unsafe_allow_html=True)

    model = rfile("module_chatgpt.txt").strip()
    st.success(f"✅ Model đang dùng: {model}")

    response = ""
    response_box = st.empty()

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            stream=True
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                response_box.markdown(f'<div class="assistant">{response}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Lỗi khi gọi OpenAI: {e}")

    st.session_state.messages.append({"role": "assistant", "content": response})
