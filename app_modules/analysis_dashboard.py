import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

def run():
st.title('Dashboard Phân tích dữ liệu - AI Thế Anh ')

uploaded_file = st.file_uploader("Chọn file Excel cần phân tích", type=["xlsx"])

if uploaded_file is not None:
    st.subheader("📄 Xem trước 5 dòng đầu để xác định dòng tiêu đề")
    preview_df = pd.read_excel(uploaded_file, header=None, nrows=5)
    st.dataframe(preview_df)

    header_row = st.number_input("🔢 Chọn số dòng chứa tiêu đề (tính từ 0)", min_value=0, max_value=20, value=3)

    df = pd.read_excel(uploaded_file, header=header_row)
    st.success(f"✅ Đã đọc dữ liệu với dòng tiêu đề là dòng số {header_row + 1}")

    st.subheader('Chọn hạng mục cần phân tích')
    selected_columns = st.multiselect('Chọn một hoặc nhiều cột:', df.columns)

    if selected_columns:
        for selected_column in selected_columns:
            st.subheader(f'Bảng phân tích theo: {selected_column}')
            analysis = df[selected_column].value_counts(dropna=False).reset_index()
            analysis.columns = [selected_column, 'Số lượng']
            st.dataframe(analysis)

            fig1, ax1 = plt.subplots()
            ax1.pie(analysis['Số lượng'], labels=analysis[selected_column], autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            ax2.bar(analysis[selected_column].astype(str), analysis['Số lượng'])
            ax2.set_xlabel(selected_column)
            ax2.set_ylabel('Số lượng')
            ax2.set_title(f'Số lượng theo {selected_column}')
            plt.xticks(rotation=45)
            st.pyplot(fig2)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for selected_column in selected_columns:
                temp_df = df[selected_column].value_counts(dropna=False).reset_index()
                temp_df.columns = [selected_column, 'Số lượng']
                temp_df.to_excel(writer, sheet_name=selected_column[:31], index=False)
        output.seek(0)

        st.download_button(
            label="📥 Tải báo cáo Excel",
            data=output,
            file_name="bao_cao_phan_tich.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info('📂 Vui lòng upload file Excel để bắt đầu phân tích.')

st.caption('Created by Aivio – AI Thế Anh')
