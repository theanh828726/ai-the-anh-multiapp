import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import base64
import io

st.set_page_config(page_title="Tra cứu MST - AI Thế Anh", layout="wide")
st.image("logo.png", use_container_width=True)
st.title("📑 TRA CỨU MÃ SỐ THUẾ TỰ ĐỘNG")
st.caption("🤖 AI Thế Anh – Humanized AI for Business")

uploaded_file = st.file_uploader("📂 Tải file Excel chứa Mã số thuế", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if "Mã số thuế" not in df.columns:
        st.error("❌ File Excel phải có cột tên 'Mã số thuế'")
        st.stop()

    tax_codes = df["Mã số thuế"].dropna().astype(str).tolist()
    st.success(f"✅ Đã nạp {len(tax_codes)} mã số thuế.")
    
    api_key = st.secrets.get("AUTOCAPTCHA_API_KEY", "")
    if not api_key:
        api_key = st.text_input("🔑 Nhập AutoCaptcha API Key:", type="password")
    
    if st.button("🚀 Bắt đầu tra cứu"):
        session = requests.Session()
        results = []

        progress = st.progress(0)
        for idx, mst in enumerate(tax_codes):
            captcha_img = session.get("https://tracuunnt.gdt.gov.vn/tcnnt/captcha.jpg").content
            b64_img = base64.b64encode(captcha_img).decode("utf-8")

            payload = {
                "apikey": api_key,
                "base64": b64_img,
                "case": "0",
                "isPhrase": "0",
                "isMath": "0",
                "minLen": "4",
                "maxLen": "6"
            }
            r = requests.post("https://api.autocaptcha.top/funcaptcha/base64", json=payload)
            captcha = r.json().get("result")

            if captcha:
                data = {"mst": mst, "captcha": captcha, "search": "Tìm kiếm"}
                response = session.post("https://tracuunnt.gdt.gov.vn/tcnnt/mstdn.jsp", data=data)
                soup = BeautifulSoup(response.text, "html.parser")
                table = soup.find("table", {"class": "tableTK"})

                result = {"Mã số thuế": mst}
                if table:
                    for row in table.find_all("tr"):
                        cols = row.find_all("td")
                        if len(cols) >= 2:
                            k = cols[0].get_text(strip=True).replace(":", "")
                            v = cols[1].get_text(strip=True)
                            result[k] = v
                else:
                    result["Tên người nộp thuế"] = "Không tìm thấy"

                results.append(result)
            else:
                results.append({"Mã số thuế": mst, "Tên người nộp thuế": "Lỗi CAPTCHA"})

            progress.progress((idx + 1) / len(tax_codes))

        result_df = pd.DataFrame(results)
        st.success("🎉 Hoàn tất tra cứu!")
        st.dataframe(result_df)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False, sheet_name="Kết quả")
        st.download_button(
            label="📥 Tải file Excel kết quả",
            data=output.getvalue(),
            file_name="ket_qua_tra_cuu_mst.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )