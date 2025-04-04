import streamlit as st
import requests
import json
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Your Gemini API Key
API_KEY = "AIzaSyAXhxiP4JKjNOMWrJf9bUm0-lLlyAuN3Y8"  # Replace with your API key
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Function to get chatbot response from Gemini API
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

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input from the microphone
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for your message...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            st.write("Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "I couldn't understand. Please repeat."
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except Exception as e:
            return f"Error: {e}"

# Streamlit Layout
st.title("Voice-based Chatbot")
st.write("You can either type or speak your message to interact with the chatbot.")

# Text Input Box for typing messages
user_input_text = st.text_input("Type your message:")

# If the user typed a message
if user_input_text:
    bot_response = chatbot(user_input_text)
    st.write(f"**You**: {user_input_text}")
    st.write(f"**Bot**: {bot_response}")
    speak(bot_response)

# Button for voice input
if st.button("Start Listening"):
    user_input_voice = listen()
    st.write(f"**You (Voice)**: {user_input_voice}")

    if user_input_voice.lower() == "exit":
        st.write("Goodbye!")
    else:
        bot_response = chatbot(user_input_voice)
        st.write(f"**Bot**: {bot_response}")
        speak(bot_response)

