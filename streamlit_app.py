import streamlit as st
import hashlib
import gspread
import json
from datetime import datetime
import json
from google.oauth2.service_account import Credentials

# إعداد Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["gcp_service_account"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1eTeNcXALoIqqaKwEa4bmTd3RZLYpQisTyjNfQ89zroI/edit").sheet1

# إعداد Google Sheets
st.set_page_config(page_title="Interactive Wireless Lab", layout="centered")
st.title("🧪 Wireless Communication Interactive Lab")
st.subheader("🎓 Back-to-Back 16-QAM | Lab 1")

st.markdown("Please enter your full name or student ID to begin.")
student_name = st.text_input("🧑‍🎓 Your Name or Student ID")

# المهام والإجابات الصحيحة
tasks = [
    {"question": "What is the shape of the bit vector srcBits if it contains 20,000 bits as a column vector?", "answer": "(20000, 1)"},
    {"question": "What is the modulation order used for 16-QAM?", "answer": "16"},
    {"question": "How many modulated symbols are generated from 20,000 bits using 16-QAM (4 bits per symbol)?", "answer": "5000"},
    {"question": "How many distinct points are there in a 16-QAM constellation diagram?", "answer": "16"},
    {"question": "Describe the effect of adding AWGN noise to the constellation. Use one word: blurred, scattered, or unchanged.", "answer": "scattered"},
    {"question": "Write the first 5 bits received after demodulation (e.g., 1 0 1 1 0)", "answer": "1 0 1 1 0"},
    {"question": "If SNR = 20 dB, what is the expected BER? (Round to 3 decimal places)", "answer": "0.000"},
]

responses = []

if student_name:
    st.success(f"Welcome {student_name}, please answer the following tasks.")
    for idx, task in enumerate(tasks, 1):
        st.markdown(f"### Task {idx}")
        st.markdown(task["question"])
        answer = st.text_input(f"Your Answer for Task {idx}", key=f"answer_{idx}")
        correct = (answer.strip() == task["answer"])
        if answer:
            st.markdown("✅ Correct!" if correct else "❌ Try again.")
        responses.append((f"Task {idx}", answer, "✅" if correct else "❌"))

    if st.button("📤 Submit Lab"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for task_id, answer, result in responses:
            sheet.append_row([student_name, task_id, answer, result, timestamp])
        st.success("✅ Your responses have been submitted successfully!")
