
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
import streamlit as st
from openai import OpenAI
import pandas as pd
from PIL import Image
import pytesseract
import tempfile
from datetime import datetime

# ----------------- CONFIG -----------------
st.set_page_config(page_title="AI Toán 5.0", layout="wide")
st.title("🧠 AI LỚP HỌC TOÁN 5.0 — V2")

api_key = st.sidebar.text_input("🔑 Nhập OpenAI API Key:", type="password")
if not api_key:
    st.warning("⚠️ Nhập API Key để sử dụng.")
    st.stop()

client = OpenAI(api_key=api_key)

menu = st.sidebar.radio("📌 Chọn chức năng:", [
    "✍️ Chấm tự luận",
    "🧮 Chấm trắc nghiệm",
    "🖼️ Chấm bài từ ảnh",
    "📝 Tạo đề kiểm tra",
    "📚 Tạo bài giảng",
    "📊 Bảng điểm",
    "🎒 Nộp bài học sinh",
    "ℹ️ Giới thiệu"
])

# ----------------- FUNCTIONS -----------------
def ai_grade(problem, answer):
    prompt = f"""
Bạn là giáo viên Toán THPT. Hãy:
- Chấm bài theo thang 10
- Chấm từng ý
- Nêu lỗi
- Cho lời khuyên cải thiện

Đề: {problem}
Bài làm: {answer}
"""
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return res.choices[0].message.content


def ai_generate_exam(topic, level, num_q):
    prompt = f"""
Tạo đề kiểm tra Toán {topic}, mức {level}, gồm {num_q} câu.
Xuất dạng:

Câu 1: ...
A. ...
B. ...
C. ...
D. ...
Đáp án: B
Lời giải: ...
"""
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return res.choices[0].message.content


def ai_lecture(topic):
    prompt = f"""
Soạn bài giảng Toán chủ đề {topic} gồm:
- Mục tiêu
- Kiến thức trọng tâm
- Ví dụ minh họa
- Bài tập + lời giải
- Tóm tắt ghi nhớ
"""
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return res.choices[0].message.content

# ----------------- CHẤM TỰ LUẬN -----------------
if menu == "✍️ Chấm tự luận":
    st.subheader("Chấm bài tự luận")
    p = st.text_area("📌 Đề bài")
    a = st.text_area("📝 Bài làm học sinh")
    if st.button("✅ Chấm"):
        st.write(ai_grade(p,a))

# ----------------- CHẤM TRẮC NGHIỆM -----------------
elif menu == "🧮 Chấm trắc nghiệm":
    st.subheader("🧮 Chấm trắc nghiệm")

    correct = st.text_input("🔑 Đáp án đúng (VD: A,B,C,B,D...)")
    student = st.text_input("🎓 Đáp án học sinh")

    if st.button("✅ Chấm điểm"):
        correct_list = correct.split(",")
        stu_list = student.split(",")
        score = sum([1 for i,j in zip(correct_list,stu_list) if i==j])
        st.success(f"🎯 Điểm: {score}/{len(correct_list)}")

# ----------------- OCR ẢNH -----------------
elif menu == "🖼️ Chấm bài từ ảnh":
    st.subheader("📸 Nhận diện bài làm từ ảnh")
    img = st.file_uploader("Upload ảnh", type=["png","jpg","jpeg"])
    if img:
        im = Image.open(img)
        st.image(im)
        text = pytesseract.image_to_string(im,lang="eng+vie")
        st.text_area("📄 OCR Text:", text)
        if st.button("✅ Chấm từ ảnh"):
            st.write(ai_grade("Bài trong ảnh", text))

# ----------------- TẠO ĐỀ -----------------
elif menu == "📝 Tạo đề kiểm tra":
    t = st.text_input("Chủ đề")
    l = st.selectbox("Mức độ",["Nhận biết","Thông hiểu","Vận dụng","Vận dụng cao"])
    n = st.slider("Số câu",5,30,10)
    if st.button("🎯 Tạo đề"):
        st.write(ai_generate_exam(t,l,n))

# ----------------- BÀI GIẢNG -----------------
elif menu == "📚 Tạo bài giảng":
    topic = st.text_input("Chủ đề bài giảng")
    if st.button("📘 Sinh bài giảng"):
        st.write(ai_lecture(topic))

# ----------------- BẢNG ĐIỂM -----------------
elif menu == "📊 Bảng điểm":
    st.write("📊 Chức năng nâng cấp — phiên bản V3 sẽ lưu Cloud + download Excel")

# ----------------- FORM NỘP BÀI -----------------
elif menu == "🎒 Nộp bài học sinh":
    name = st.text_input("Tên học sinh")
    ans = st.text_area("Bài làm")
    if st.button("📩 Nộp bài"):
        st.success("✅ Đã nộp bài — GV sẽ chấm trên bản chính")

# ----------------- INTRO -----------------
else:
    st.write("🧠 Hệ thống AI dạy học 5.0 — Bản nâng cấp V2")
