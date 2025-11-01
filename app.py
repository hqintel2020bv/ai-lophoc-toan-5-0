
import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI
from PIL import Image
import pytesseract
import tempfile

# ---------------- CẤU HÌNH ----------------
st.set_page_config(page_title="AI LỚP HỌC TOÁN 5.0", layout="wide")
st.title("🧠 AI LỚP HỌC TOÁN 5.0 - STREAMLIT")

openai_api_key = st.text_input("🔑 Nhập OpenAI API Key:", type="password")

menu = st.sidebar.radio("📌 Chọn chức năng:", [
    "✍️ Chấm bài tự luận",
    "📷 Chấm bài từ ảnh",
    "📊 Bảng điểm",
    "ℹ️ Giới thiệu"
])

# ✅ Function chuyển giọng nói sang văn bản
def voice_to_text():
    st.subheader("🎤 Nhập bằng giọng nói")
    audio = st.audio_input("Giữ nút micro để đọc bài làm:")
    
    if audio:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.write(audio.read())
        temp_file.seek(0)

        if st.button("✅ Chuyển giọng nói sang văn bản"):
            client = OpenAI(api_key=openai_api_key)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=open(temp_file.name, "rb")
            )
            st.success("✅ Đã nhận dạng xong")
            return transcript.text

    return ""

# ✅ OCR từ ảnh
def ocr_image(img):
    return pytesseract.image_to_string(img, lang="eng+vie")

# ---------------- CHỨC NĂNG CHÍNH ----------------

# ✍️ Chấm bài tự luận
if menu == "✍️ Chấm bài tự luận":
    st.header("📑 Chấm bài tự luận bằng GPT")
    
    de_bai = st.text_area("📌 Đề bài:")
    bai_lam = st.text_area("🧠 Bài làm của học sinh:")

    if st.button("🚀 Chấm bài"):
        client = OpenAI(api_key=openai_api_key)
        prompt = f"Hãy chấm bài Toán 10 theo thang 10 điểm và nhận xét:\nĐề bài: {de_bai}\nBài làm: {bai_lam}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        st.write("✅ Kết quả:")
        st.write(response.choices[0].message.content)

# 📷 Chấm bài từ ảnh
elif menu == "📷 Chấm bài từ ảnh":
    st.header("📎 Chấm bài từ ảnh")
    uploaded = st.file_uploader("Tải ảnh bài làm", type=["png","jpg","jpeg"])

    if uploaded:
        img = Image.open(uploaded)
        st.image(img, caption="Ảnh bài làm", use_column_width=True)

        with st.spinner("🔍 Đang nhận dạng chữ..."):
            text = ocr_image(img)

        st.write("📄 Văn bản OCR:")
        st.text_area("", text, height=150)

# 📊 Bảng điểm
elif menu == "📊 Bảng điểm":
    st.header("📊 Bảng điểm sắp ra mắt...")

# ℹ️ Giới thiệu
else:
    st.header("ℹ️ Giới thiệu")
    st.write("✅ Ứng dụng AI Lớp học Toán 5.0 phiên bản Streamlit")
