
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
