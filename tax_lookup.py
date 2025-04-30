import streamlit as st

# ✅ Hiển thị logo dùng chung
from pathlib import Path
logo_path = Path("logo.png")
if logo_path.exists():
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image(str(logo_path), use_container_width=True)

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
api_key = '5a5b4ea97e3349f4610adfe3bd489b7a'
captcha_type = "imagetotext"
excel_path = 'File ket qua tra cuu.xlsx'
pause_flag = False

# Hàm mở file Excel
def open_file_excel(file_path):
    try:
        os.startfile(file_path)
    except Exception as e:
        st.error("Vui lòng chạy chương trình trước!")

# Hàm giải Captcha
def solve_captcha(api_key, img_path, captcha_type):
    with open(img_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    data = {'key': api_key, 'type': captcha_type, 'img': img_base64, "module": "common", "casesensitive": False}
    try:
        r = requests.post(browser_API, data=data).json()
        return r.get('captcha')
    except Exception as e:
        return None

# Tải hình captcha
def download_image(element, path):
    try:
        element.screenshot(path)
    except Exception as e:
        st.error("Lỗi tải ảnh captcha")

# Mở trình duyệt Chrome
def launch_browser(url):
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get(url)
    return browser

# Đọc file Excel đầu vào
def read_data_from_file(filename):
    data = []
    try:
        df = pd.read_excel(filename)
        for idx, row in enumerate(df.itertuples(index=False), start=1):
            mst = str(row[0]).strip()
            data.append([idx, mst])
    except Exception as e:
        st.error("Lỗi đọc file Excel")
    return data

# Lưu kết quả ra file Excel
def save_to_excel(header, data, filename):
    df = pd.DataFrame(data, columns=header)
    df.to_excel(filename, index=False)

# Xử lý tự động với selenium
def selenium_task(data, browser_path, api_key, captcha_type, img_path, header_list, excel_path):
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
                if captcha_attempts >= max_captcha_attempts:
                    st.warning("Hết số lần giải captcha!")
                    break
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

    st.success("Hoàn thành!")

# Các hành động trong giao diện Streamlit
st.title("TRA CỨU MST TỰ ĐỘNG - AI Thế Anh | Humanized AI for Business")

uploaded_file = st.file_uploader("Chọn File MST (Excel)", type=["xlsx"])

if uploaded_file:
    with open("temp_uploaded.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    data = read_data_from_file("temp_uploaded.xlsx")
    st.dataframe(pd.DataFrame(data, columns=['STT', 'Mã số thuế']))

if st.button("▶️ Chạy"):
    if os.path.exists(excel_path):
        st.warning("File Excel đã tồn tại, không thể chạy.")
    else:
        if data:
            threading.Thread(target=selenium_task, args=(data, browser_path, api_key, captcha_type, img_path, header_list, excel_path), daemon=True).start()
        else:
            st.error("Vui lòng nhập file Excel.")

if st.button("📄 Mở File Excel Kết quả"):
    open_file_excel(excel_path)

if st.button("⏸ Tạm Dừng / Tiếp tục"):
    pause_flag = not pause_flag
    st.info("Đã đổi trạng thái Tạm dừng / Tiếp tục")