import streamlit as st
import pandas as pd
import requests
import time
import os
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO
import threading

# Cấu hình các biến toàn cục
data = []
header_list = ['STT', 'Mã số thuế', 'Tên người nộp thuế', 'Cơ quan thuế', 'Số CMT/Thẻ căn cước', 'Ngày thay đổi thông tin gần nhất', 'Ghi chú']
img_path = 'captcha.png'
browser_path = 'https://tracuunnt.gdt.gov.vn/tcnnt/mstdn.jsp'
browser_API = "https://autocaptcha.pro/apiv3/process"
captcha_type = "imagetotext"
excel_path = 'File ket qua tra cuu.xlsx'
pause_flag = False

# ======= HÀM XỬ LÝ ===========
def open_file_excel(file_path):
    try:
        os.startfile(file_path)
    except Exception as e:
        st.error("Vui lòng chạy chương trình trước!")

def solve_captcha(api_key, img_path, captcha_type):
    with open(img_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    data = {'key': api_key, 'type': captcha_type, 'img': img_base64, "module": "common", "casesensitive": False}
    try:
        r = requests.post(browser_API, data=data, timeout=30).json()
        return r.get('captcha')
    except:
        return None

def download_image(element, path):
    try:
        element.screenshot(path)
    except Exception as e:
        st.error("Lỗi tải ảnh captcha")

def launch_browser(url):
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get(url)
    return browser

def read_data_from_file(filename):
    data = []
    try:
        df = pd.read_excel(filename)
        for idx, row in enumerate(df.itertuples(index=False), start=1):
            mst = str(row[0]).strip()
            data.append([idx, mst])
    except:
        st.error("Lỗi đọc file Excel")
    return data

def save_to_excel(header, data, filename):
    df = pd.DataFrame(data, columns=header)
    df.to_excel(filename, index=False)

def selenium_task(data, browser_path, api_key, img_path, header_list, excel_path, progress_placeholder):
    global pause_flag
    browser = launch_browser(browser_path)
    max_captcha_attempts = 5

    for idx, row in enumerate(data):
        while pause_flag:
            time.sleep(1)

        MST_ = row[1]
        browser.find_element(By.NAME, 'mst').send_keys(MST_)
        captcha_attempts = 0

        while captcha_attempts < max_captcha_attempts:
            captcha_element = browser.find_element(By.XPATH, '//td[@colspan="2"]//table//tbody//tr//td//div//img')
            download_image(captcha_element, img_path)
            captcha = solve_captcha(api_key, img_path, captcha_type)
            time.sleep(1)

            if not captcha:
                captcha_attempts += 1
                continue

            browser.find_element(By.NAME, 'captcha').send_keys(captcha)
            time.sleep(1)
            browser.find_element(By.XPATH, '//input[@type="button" and @value="" and contains(@class, "subBtn")]').click()
            time.sleep(1)

            try:
                table_element = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'ta_border')))
                break
            except:
                captcha_attempts += 1

        if captcha_attempts >= max_captcha_attempts:
            continue

        table_html = table_element.get_attribute('outerHTML')
        df_list = pd.read_html(StringIO(table_html))
        df = df_list[0]
        row_as_list = df.iloc[0, [1,2,3,4,5,6]].values.tolist()
        data[idx] = [idx+1] + row_as_list
        browser.find_element(By.NAME, 'mst').clear()

        save_to_excel(header_list, data, excel_path)
        progress_placeholder.progress((idx + 1) / len(data))

    browser.quit()
    st.success("Hoàn thành!")

# ======= GIAO DIỆN STREAMLIT ===========
st.set_page_config(page_title="Tra cứu MST", layout="wide")
st.image("https://i.imgur.com/LqREp9z.png", use_container_width=True)
st.title("TRA CỨU MST TỰ ĐỘNG - AI Thế Anh | Humanized AI for Business")

st.markdown("### 🔐 Nhập API Key AutoCaptcha")
api_key = st.text_input("API Key", type="password")

uploaded_file = st.file_uploader("📂 Chọn File MST (Excel)", type=["xlsx"])

if uploaded_file:
    with open("temp_uploaded.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    data = read_data_from_file("temp_uploaded.xlsx")
    st.dataframe(pd.DataFrame(data, columns=['STT', 'Mã số thuế']))

if st.button("▶️ Chạy"):
    if not api_key:
        st.warning("Vui lòng nhập API Key trước khi chạy.")
    elif os.path.exists(excel_path):
        st.warning("File Excel đã tồn tại, không thể chạy.")
    elif data:
        progress_placeholder = st.empty()
        threading.Thread(
            target=selenium_task,
            args=(data, browser_path, api_key, img_path, header_list, excel_path, progress_placeholder),
            daemon=True
        ).start()
    else:
        st.error("Vui lòng nhập file Excel.")

if st.button("📄 Mở File Excel Kết quả"):
    open_file_excel(excel_path)

if st.button("⏸ Tạm Dừng / Tiếp tục"):
    pause_flag = not pause_flag
    st.info("Đã đổi trạng thái Tạm dừng / Tiếp tục")