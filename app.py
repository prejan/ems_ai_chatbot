
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
