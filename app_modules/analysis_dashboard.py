
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

def run():
    st.title("📊 Dashboard Phân tích dữ liệu - AI Thế Anh")
    uploaded_file = st.file_uploader("📂 Chọn file Excel cần phân tích", type=["xlsx"])

    if uploaded_file is not None:
        st.subheader("📄 Xem trước 5 dòng đầu để xác định dòng tiêu đề")
        preview_df = pd.read_excel(uploaded_file, header=None, nrows=5)
        st.dataframe(preview_df)

        header_row = st.number_input("🔢 Chọn dòng tiêu đề (tính từ 0)", min_value=0, max_value=20, value=3)

        df = pd.read_excel(uploaded_file, header=header_row)
        st.success(f"✅ Đã đọc dữ liệu với dòng tiêu đề ở dòng số {header_row + 1}")

        st.subheader('📌 Chọn cột cần phân tích')
        selected_columns = st.multiselect('📊 Chọn một hoặc nhiều cột:', df.columns)

        if selected_columns:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for col in selected_columns:
                    st.markdown(f"### 📈 Phân tích theo: `{col}`")
                    analysis = df[col].value_counts(dropna=False).reset_index()
                    analysis.columns = [col, 'Số lượng']
                    st.dataframe(analysis)

                    fig, ax = plt.subplots()
                    ax.bar(analysis[col].astype(str), analysis['Số lượng'])
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                    analysis.to_excel(writer, sheet_name=col[:31], index=False)
            output.seek(0)

            st.download_button("📥 Tải báo cáo Excel", data=output, file_name="bao_cao.xlsx")
