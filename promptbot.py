
# 🚀 PromptBot All-in-One: 3 Chế độ - Chat 💬 + Form 🗘️ + Công Thức 📋

import streamlit as st
from openai import OpenAI
from datetime import datetime
import pandas as pd
import random
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from io import BytesIO
import requests
import os
from PIL import Image

# ✅ API Key GPT
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])