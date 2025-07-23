import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import threading

engine = pyttsx3.init()
voices = engine.getProperty('voices')
female_voice = next((v for v in voices if "female" in v.name.lower() or "zira" in v.name.lower()), voices[0])
engine.setProperty('voice', female_voice.id)
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass

template = """
You are Nexa, a helpful, friendly AI assistant.

{context}

User: {question}
Nexa:
"""
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

st.set_page_config(page_title="Nexa AI", layout="centered")
st.title("💬 Nexa - Your AI Assistant")

if "context" not in st.session_state:
    st.session_state.context = ""
if "chat" not in st.session_state:
    st.session_state.chat = []
if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False
if "input" not in st.session_state:
    st.session_state.input = ""

col1, col2 = st.columns([3, 1])
with col1:
    st.caption("Switch between voice and text mode anytime:")
with col2:
    if st.button("🎙️ Toggle Mode"):
        st.session_state.voice_mode = not st.session_state.voice_mode
        st.success(f"Switched to {'Voice' if st.session_state.voice_mode else 'Text'} mode")

for speaker, msg, timestamp in st.session_state.chat:
    with st.chat_message(speaker):
        st.markdown(f"*{timestamp}*")
        st.markdown(msg)

def get_text_input():
    return st.chat_input("Type your message here...")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, phrase_time_limit=8)
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn’t catch that."
        except sr.RequestError:
            return "Speech recognition service error."

def respond(user_input):
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat.append(("user", user_input, timestamp))

    with st.chat_message("assistant"):
        with st.spinner("Nexa is thinking..."):
            try:
                result = chain.invoke({"context": st.session_state.context, "question": user_input})
                response = result.content if hasattr(result, "content") else str(result)
            except Exception as e:
                response = "Oops! Something went wrong."
                print("Error:", e)

        st.session_state.chat.append(("assistant", response, timestamp))
        st.markdown(f"*{timestamp}*")
        st.markdown(response)

        threading.Thread(target=speak, args=(response,), daemon=True).start()

        st.session_state.context += f"\nUser: {user_input}\nNexa: {response}"

if st.session_state.voice_mode:
    if st.button("🎧 Speak"):
        query = recognize_speech()
        if query:
            respond(query)
else:
    user_text = get_text_input()
    if user_text:
        respond(user_text)
