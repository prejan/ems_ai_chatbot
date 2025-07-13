# Directory: ems_ai_chatbot

# ------------------- app.py -------------------
import streamlit as st
from utils.gemini_assistant import get_triage_assessment
from utils.voice_input import capture_vitals

st.set_page_config(page_title="EMS Triage AI", layout="centered")
st.title("🚑 EMS Triage AI Chatbot")

st.markdown("""
This tool helps first responders make fast decisions in emergencies using AVPU assessment, vitals, and symptoms.
""")

symptoms = st.text_input("Enter patient symptoms (can be in local language):")
avpu_level = st.selectbox("AVPU Level:", ["Alert", "Verbal", "Pain", "Unresponsive"])

vitals = st.text_input("Enter patient vitals (BP, pulse, etc.):")
if st.button("🎙 Capture Vitals via Voice"):
    vitals = capture_vitals()
    st.success(f"Captured Vitals: {vitals}")

if st.button("🩺 Get Triage Advice"):
    if not symptoms or not vitals:
        st.warning("Please fill in both symptoms and vitals.")
    else:
        with st.spinner("Analyzing with AI..."):
            result = get_triage_assessment(symptoms, avpu_level, vitals)
            st.subheader("📋 Triage Report")
            st.write(result)

st.markdown("---")
st.markdown("Created using Gemini API, Streamlit & Speech Recognition")

# ------------------- requirements.txt -------------------
# streamlit
# google-generativeai
# speechrecognition
# pyaudio
# gspread
# oauth2client

# ------------------- utils/gemini_assistant.py -------------------
import google.generativeai as genai

# Replace with your actual Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")
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

# ------------------- (Optional) Google Sheets Integration -------------------
# You can add `utils/sheets_logger.py` later to log responses to Google Sheets using gspread and oauth2client.
