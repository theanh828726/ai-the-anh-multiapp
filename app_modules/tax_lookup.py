
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time

def run():
# Set page config immediately
st.set_page_config(page_title="TRA CỨU MST TỰ ĐỘNG - AI Thế Anh", layout="wide")

# Logo
st.image("logo.png", use_container_width=True)

st.markdown("## TRA CỨU MST TỰ ĐỘNG - AI Thế Anh | Humanized AI for Business")

# API Key Input
st.markdown("### 🔐 Nhập API Key AutoCaptcha")
api_key = st.text_input("API Key", type="password")

# File uploader
st.markdown("📂 **Chọn File MST (Excel)**")
uploaded_file = st.file_uploader("Chọn file Excel chứa danh sách Mã số thuế", type=["xlsx"])

df_result = None

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)
    
    if st.button("▶️ Chạy"):
        if not api_key:
            st.warning("Vui lòng nhập API Key AutoCaptcha trước khi chạy.")
        else:
            df_result = df.copy()
            progress = st.progress(0, text="Đang xử lý...")

            session = requests.Session()
            results = []

            for idx, row in df.iterrows():
                try:
                    mst = str(row.iloc[1])
                    captcha_img = session.get("https://tracuunnt.gdt.gov.vn/tcnnt/captcha.jpg").content

                    # Gửi ảnh lên AutoCaptcha
                    response = requests.post(
                        "https://api.autocaptcha.ai/api/v1/solve",
                        headers={"x-api-key": api_key},
                        files={"file": ("captcha.jpg", BytesIO(captcha_img), "image/jpeg")},
                        timeout=30
                    )

                    captcha_text = response.json().get("captcha", "")

                    payload = {
                        "txtmst": mst,
                        "captcha": captcha_text,
                    }

                    headers = {
                        "Content-Type": "application/x-www-form-urlencoded"
                    }

                    response = session.post("https://tracuunnt.gdt.gov.vn/tcnnt/mstdn.jsp", data=payload, headers=headers)
                    soup = BeautifulSoup(response.text, "html.parser")
                    table = soup.find("table", class_="tblKetqua")
                    
                    if table:
                        cells = table.find_all("td")
                        result_text = cells[1].text.strip() if len(cells) > 1 else "Không tìm thấy"
                    else:
                        result_text = "Không tìm thấy"

                    results.append(result_text)

                except Exception as e:
                    results.append("Lỗi")

                progress.progress((idx + 1) / len(df), text=f"Đã xử lý {idx + 1}/{len(df)} dòng")

            df_result["Kết quả"] = results
            st.success("✅ Đã tra cứu xong.")
            st.dataframe(df_result)

            # Download
            from io import BytesIO
            towrite = BytesIO()
            df_result.to_excel(towrite, index=False)
            towrite.seek(0)
            st.download_button("📥 Mở File Excel Kết quả", towrite, "ket_qua_tra_cuu.xlsx")
