import requests
import json
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Your Gemini API Key
API_KEY = "AIzaSyAXhxiP4JKjNOMWrJf9bUm0-lLlyAuN3Y8"# अपनी API Key डालें
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

# Function to take voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "I couldn't understand. Please repeat."
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except Exception as e:
            return f"Error: {e}"

# Voice-based chatbot interaction
while True:
    print("Say something (or say 'exit' to quit)...")
    user_input = listen()
    print(f"You: {user_input}")

    if user_input.lower() == "exit":
        speak("Goodbye!")
        break

    bot_response = chatbot(user_input)
    print(f"Bot: {bot_response}")
    speak(bot_response)
