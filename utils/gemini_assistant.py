
import google.generativeai as genai

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyBSXTCcaqRrqR84EA5GrigxOtkzfJTgaz0")
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
