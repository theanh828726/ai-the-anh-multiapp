import streamlit as st
st.set_page_config(page_title="PromptBot All-in-One", layout="wide")

# ✅ Hiển thị logo dùng chung
from pathlib import Path
logo_path = Path("logo.png")
if logo_path.exists():
    col1, col2, col3 = st.columns([3, 4, 1])
    with col2:
        st.image(str(logo_path), use_column_width=True)

from openai import OpenAI
from datetime import datetime
import pandas as pd
import random
from io import BytesIO
import requests
import os
from PIL import Image

# Tiếp tục phần code của bạn ở đây...
