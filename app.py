# Directory: ems_ai_chatbot

# ------------------- app.py -------------------
import streamlit as st
from utils.gemini_assistant import get_triage_assessment
from utils.voice_input import capture_vitals

st.set_page_config(page_title="EMS Triage AI", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    body { background-color: #0e1117; color: #ffffff; }
    .reportview-container { background: #0e1117; }
    .sidebar .sidebar-content { background: #0e1117; }
    .css-1d391kg, .css-1v0mbdj { color: #fff; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🚑 EMS AI Triage Chatbot")
st.markdown("""
### 🌙 Dark Themed Assistant for Emergency Medical Services
AI-powered triage assistance using symptoms, AVPU assessment, and vitals — powered by Google Gemini
---
""")

# Input Section
st.subheader("📝 Enter Patient Details")
symptoms = st.text_input("🧾 Symptoms (can be in local language):")
avpu_level = st.selectbox("🧠 AVPU Level:", ["Alert", "Verbal", "Pain", "Unresponsive"])
vitals = st.text_input("❤️ Vitals (Pulse, BP, etc.):")

# Voice Input
if st.button("🎙 Capture Vitals via Voice"):
    vitals = capture_vitals()
    st.success(f"Captured Vitals: {vitals}")

# Optional: Image Upload (placeholder for future visual triage)
st.file_uploader("📸 Upload patient image (optional)", type=["jpg", "png"], key="image")

# Generate Triage Report
if st.button("🩺 Get Triage Advice"):
    if not symptoms or not vitals:
        st.warning("Please enter both symptoms and vitals.")
    else:
        with st.spinner("Analyzing with Gemini AI..."):
            result = get_triage_assessment(symptoms, avpu_level, vitals)

        st.markdown("---")
        st.subheader("📋 Triage Report")
        triage_color = "🟨"
        if "red" in result.lower(): triage_color = "🟥"
        elif "green" in result.lower(): triage_color = "🟩"
        elif "black" in result.lower(): triage_color = "⬛"

        st.markdown(f"### {triage_color} **Triage Category Detected**")
        st.markdown("""
        <div style='background-color:#1e222d;padding:1.2rem;border-radius:10px;margin-top:1rem;'>
            <pre style='color:#ccc;font-size:0.95rem;'>
{}</pre>
        </div>
        """.format(result), unsafe_allow_html=True)

st.markdown("---")

# ------------------- requirements.txt -------------------
# streamlit
# google-generativeai
# speechrecognition
# pyaudio (only for local use)

# ------------------- utils/gemini_assistant.py -------------------
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def get_triage_assessment(symptoms, avpu_level, vitals):
    prompt = f'''
    Patient Report:
    - Symptoms: {symptoms}
    - AVPU Level: {avpu_level}
    - Vitals: {vitals}

    You are a medical triage assistant. Based on the AVPU scale, vitals, and symptoms, provide:
    1. Triage Category (Red / Yellow / Green / Black)
    2. Reason for classification
    3. Suggested immediate action
    '''
    response = model.generate_content(prompt)
    return response.text

# ------------------- utils/voice_input.py -------------------
import speech_recognition as sr

def capture_vitals():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for vitals...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"

# ----------------------------------------------------------
