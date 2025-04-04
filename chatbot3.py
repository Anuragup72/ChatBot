import streamlit as st
import requests
import json
from gtts import gTTS
import speech_recognition as sr
import os
import tempfile

API_KEY = "AIzaSyAXhxiP4JKjNOMWrJf9bUm0-lLlyAuN3Y8"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def chatbot(message):
    payload = {
        "contents": [
            {
                "parts": [{"text": message}]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_data = response.json()
            bot_response = response_data["candidates"][0]["content"]["parts"][0]["text"]
            return bot_response.strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}"

def speak(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

def recognize_speech_from_file(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Error from Google API: {e}"

st.title("🗣️ Voice + Text Chatbot using Gemini API")

st.write("Type your message below or upload a voice message (WAV format).")

user_input = st.text_input("💬 Type your message:")
if user_input:
    st.write(f"**You:** {user_input}")
    response = chatbot(user_input)
    st.write(f"**Bot:** {response}")
    speak(response)

st.markdown("### 🎤 Upload your voice message")
audio_file = st.file_uploader("Upload a WAV audio file", type=["wav"])

if audio_file:
    st.audio(audio_file)
    text_from_audio = recognize_speech_from_file(audio_file)
    st.write(f"**You (from audio):** {text_from_audio}")
    response = chatbot(text_from_audio)
    st.write(f"**Bot:** {response}")
    speak(response)
