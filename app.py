import streamlit.components.v1 as componentsimport 
streamlit as st
import os
import requests
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from pypdf import PdfReader
import time

# ----------------------------
# Load API Key (OpenRouter)
# ----------------------------
load_dotenv()

OPENROUTER_API_KEY = None

if "OPENROUTER_API_KEY" in st.secrets:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("OPENROUTER_API_KEY not found. Add it in Streamlit Secrets or .env file.")
    st.stop()

# ----------------------------
# Premium System Prompt
# ----------------------------
SYSTEM_PROMPT = """
You are a world-class senior software engineer, architect, and debugging specialist.

Rules:
- Never mention AI, model, GPT, OpenAI, or internal identity.
- Behave like a premium professional technical consultant.
- Always respond in the same language as the user.
- Match the user's tone automatically.

Core Skills:
- Full-stack development
- Mobile app development guidance
- Web development
- API design
- Database design
- Debugging and repair
- Security and optimization

Repair Mode Rules:
When user asks to fix/repair/debug:
- Provide structured output:
  1) PROBLEM SUMMARY
  2) ROOT CAUSE
  3) FIXED FULL CODE
  4) IMPROVEMENTS
  5) SECURITY FIXES
  6) PERFORMANCE OPTIMIZATION
  7) HOW TO RUN / TEST

Always provide production-ready answers.
"""

# ----------------------------
# OpenRouter Chat Function
# ----------------------------
def openrouter_chat(messages, model="deepseek/deepseek-chat", temperature=0.6):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Premium Assistant"
    }

    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "temperature": temperature
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()
    return data["choices"][0]["message"]["content"]

# ----------------------------
# Website Extractor
# ----------------------------
def get_website_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())[:7000]

# ----------------------------
# PDF Extractor
# ----------------------------
def get_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text[:9000]

# ----------------------------
# Page UI Config
# ----------------------------
st.set_page_config(page_title="Premium Assistant", layout="wide")

# ----------------------------
# Premium Styling (ChatGPT-like)
# ----------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    .stChatMessage {
        border-radius: 16px;
        padding: 8px;
    }
    .stTextArea textarea {
        border-radius: 12px;
    }
    .stButton button {
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 600;
    }
    .sidebar-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .section-title {
        font-size: 16px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Session State Init
# ----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "web_text" not in st.session_state:
    st.session_state.web_text = ""

if "last_request" not in st.session_state:
    st.session_state.last_request = 0

# ----------------------------
# Sidebar (ChatGPT Style)
# ----------------------------
st.sidebar.markdown("<div class='sidebar-title'>⚙️ Settings</div>", unsafe_allow_html=True)

model = st.sidebar.selectbox("Model", [
    "deepseek/deepseek-chat",
    "deepseek/deepseek-coder",
    "meta-llama/llama-3.1-70b-instruct",
    "mistralai/mistral-large"
])

tone = st.sidebar.selectbox("Tone Style", [
    "Auto",
    "Professional",
    "Friendly",
    "Strict Developer",
    "News Style"
])

temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 0.6, 0.1)

st.sidebar.markdown("<div class='section-title'>Tools</div>", unsafe_allow_html=True)

enable_pdf = st.sidebar.toggle("Enable PDF Mode", value=True)
enable_web = st.sidebar.toggle("Enable Website Mode", value=True)

st.sidebar.markdown("<div class='section-title'>Uploads</div>", unsafe_allow_html=True)

if enable_pdf:
    pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
    if pdf_file:
        st.session_state.pdf_text = get_pdf_text(pdf_file)
        st.sidebar.success("PDF Loaded")

if enable_web:
    url = st.sidebar.text_input("Website URL")
    if url:
        try:
            st.session_state.web_text = get_website_text(url)
            st.sidebar.success("Website Loaded")
        except:
            st.sidebar.error("Website Load Failed")

st.sidebar.markdown("<div class='section-title'>Chat Controls</div>", unsafe_allow_html=True)

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat = []
    st.success("Chat Cleared")
    st.rerun()

# ----------------------------
# Main Layout
# ----------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## 💬 Premium Chat")

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

with col2:
    st.markdown("## 🛠 Repair Tools")

    repair_mode = st.radio("Select Mode", [
        "Normal Chat",
        "Repair Code",
        "Explain Code",
        "Optimize Code",
        "Security Audit",
        "Build Project"
    ])

    st.markdown("### Quick Actions")

    if st.button("📌 Make Answer Short"):
        st.session_state.chat.append({"role": "user", "content": "From now on, keep answers short and direct."})
        st.rerun()

    if st.button("📌 Make Answer Detailed"):
        st.session_state.chat.append({"role": "user", "content": "From now on, provide detailed step-by-step answers."})
        st.rerun()

# ----------------------------
# Chat Input (Bottom Like ChatGPT)
# ----------------------------
user_input = st.chat_input("Message... (Type here)")

if user_input:
    # Rate limit control
    if time.time() - st.session_state.last_request < 2:
        st.warning("Please wait 2 seconds before sending another message.")
        st.stop()

    st.session_state.last_request = time.time()

    st.session_state.chat.append({"role": "user", "content": user_input})

    # Context Builder
    context = f"User selected tone: {tone}\n"
    context += f"Mode: {repair_mode}\n"

    if enable_pdf and st.session_state.pdf_text:
        context += f"\nPDF CONTENT:\n{st.session_state.pdf_text}\n"

    if enable_web and st.session_state.web_text:
        context += f"\nWEBSITE CONTENT:\n{st.session_state.web_text}\n"

    # Mode-based prompt
    if repair_mode == "Repair Code":
        context += "\nUser wants full code repair with best practices.\n"
    elif repair_mode == "Explain Code":
        context += "\nUser wants clear explanation step-by-step.\n"
    elif repair_mode == "Optimize Code":
        context += "\nUser wants performance optimization.\n"
    elif repair_mode == "Security Audit":
        context += "\nUser wants security vulnerability audit and fixes.\n"
    elif repair_mode == "Build Project":
        context += "\nUser wants a full project structure with files and commands.\n"

    messages = st.session_state.chat.copy()
    messages.append({"role": "system", "content": context})

    try:
        reply = openrouter_chat(messages, model=model, temperature=temperature)
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()
    except Exception as e:
        st.error(f"API Error: {e}")
SYSTEM_PROMPT = """
...your existing prompt...

Voice Interaction Mode:
- If the user requests voice conversation, respond in short spoken-style sentences.
- Use simple everyday language like a human.
- If the user cannot read, explain slowly using easy words.
- Ask confirmation questions like: Did you understand? Should I repeat?
- Keep answers short, clear, and friendly.
"""
VOICE_PROMPT = """
Voice Mode:
- Speak like a real human.
- Use short sentences.
- Use simple words.
- Explain slowly and clearly.
- If the user cannot read, explain everything in very easy language.
- Ask: "Did you understand?" and "Should I repeat?"
- Keep answers friendly and conversational.
"""
def speak(text, lang="en-US"):
    text = text.replace("\n", " ").replace('"', "'")
    js = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text}");
    msg.lang = "{lang}";
    msg.rate = 1;
    msg.pitch = 1;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0)
    speak(response)
