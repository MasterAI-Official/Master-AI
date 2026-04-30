import streamlit as st
import requests
import json
import time
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from bs4 import BeautifulSoup
from gtts import gTTS
import tempfile
import base64
import streamlit.components.v1 as components
from streamlit_mic_recorder import mic_recorder

# ----------------------------
# API KEY
# ----------------------------
load_dotenv()

API_KEY = None
if "OPENROUTER_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("Missing API Key")
    st.stop()

# ----------------------------
# SYSTEM PROMPT (MASTER BRAIN)
# ----------------------------
SYSTEM_PROMPT = """
You are a world-class AI assistant and senior software engineer.

Rules:
- Never mention AI or system identity.
- Respond naturally like a human expert.
- Be precise, helpful, and structured.
- If voice mode is enabled, respond in short spoken sentences.
- If user is confused, simplify explanation.

Capabilities:
- Coding expert
- Debugging and repair
- Web understanding
- PDF analysis
- Project building guidance
"""

# ----------------------------
# API CALL
# ----------------------------
def ask_ai(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "temperature": 0.6
    }

    res = requests.post(url, headers=headers, data=json.dumps(payload))
    return res.json()["choices"][0]["message"]["content"]

# ----------------------------
# TEXT TO SPEECH
# ----------------------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)

    audio = open(tmp.name, "rb").read()
    b64 = base64.b64encode(audio).decode()

    audio_html = f"""
    <audio autoplay controls>
    <source src="data:audio/mp3;base64,{b64}">
    </audio>
    """
    components.html(audio_html, height=100)

# ----------------------------
# WEBSITE SCRAPER
# ----------------------------
def get_web(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    for t in soup(["script", "style"]):
        t.extract()

    return " ".join(soup.get_text().split())[:6000]

# ----------------------------
# PDF READER
# ----------------------------
def get_pdf(file):
    reader = PdfReader(file)
    text = ""
    for p in reader.pages:
        t = p.extract_text()
        if t:
            text += t + "\n"
    return text[:8000]

# ----------------------------
# UI CONFIG
# ----------------------------
st.set_page_config(page_title="Master AI", layout="wide")

st.title("💎 Master AI - Ultimate Assistant")

# ----------------------------
# SESSION
# ----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "web" not in st.session_state:
    st.session_state.web = ""

if "pdf" not in st.session_state:
    st.session_state.pdf = ""

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("⚙️ Settings")

voice_output = st.sidebar.toggle("🔊 Voice Output", value=True)
voice_input = st.sidebar.toggle("🎤 Voice Input", value=True)

model = st.sidebar.selectbox("Model", ["deepseek/deepseek-chat"])

st.sidebar.markdown("---")

pdf_file = st.sidebar.file_uploader("Upload PDF")

if pdf_file:
    st.session_state.pdf = get_pdf(pdf_file)

url = st.sidebar.text_input("Website URL")

if url:
    try:
        st.session_state.web = get_web(url)
    except:
        st.error("Website load failed")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat = []
    st.rerun()

# ----------------------------
# CHAT UI
# ----------------------------
for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ----------------------------
# VOICE INPUT
# ----------------------------
voice_text = None

if voice_input:
    audio = mic_recorder(start_prompt="🎤 Speak", stop_prompt="⏹ Stop", just_once=True)
    if audio:
        voice_text = "User spoke something (voice input detected)"

# ----------------------------
# INPUT
# ----------------------------
user_input = st.chat_input("Type message...")

if user_input or voice_text:

    text = user_input if user_input else voice_text

    st.session_state.chat.append({"role": "user", "content": text})

    context = ""

    if st.session_state.pdf:
        context += f"PDF:\n{st.session_state.pdf}\n"

    if st.session_state.web:
        context += f"WEB:\n{st.session_state.web}\n"

    messages = st.session_state.chat.copy()
    messages.append({"role": "system", "content": context})

    response = ask_ai(messages)

    st.session_state.chat.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)

        if voice_output:
            speak(response)

# ----------------------------
# ACTION BUTTONS (3 DOT STYLE)
# ----------------------------
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 Copy Last"):
        st.toast("Copy manually (browser)")

with col2:
    if st.button("🔁 Regenerate"):
        if st.session_state.chat:
            last = st.session_state.chat[-1]["content"]
            st.session_state.chat.append({"role": "user", "content": last})
            st.rerun()

with col3:
    if st.button("📤 Share"):
        st.info("Use browser share / copy link")
