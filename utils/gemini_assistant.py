import google.generativeai as genai
import os

# ✅ Configure Gemini with environment variable (DO NOT hardcode your key)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use 'gemini-pro' for free-tier or paid-tier Gemini access
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
