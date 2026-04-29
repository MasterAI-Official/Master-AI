import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langdetect import detect
from pypdf import PdfReader
from openai import OpenAI

# ----------------------------
# LOAD API KEY
# ----------------------------
load_dotenv()

API_KEY = None

if "OPENAI_API_KEY" in st.secrets:
    API_KEY = st.secrets["OPENAI_API_KEY"]
else:
    API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error("Missing API Key. Add it in Streamlit Secrets or .env file.")
    st.stop()

client = OpenAI(api_key=API_KEY)

# ----------------------------
# SYSTEM PROMPT (PREMIUM ENGINEER MODE)
# ----------------------------
SYSTEM_PROMPT = """
You are a world-class senior software engineer and system architect.

Rules:
- Never mention AI, model, GPT, OpenAI, or system identity.
- Act like a professional software engineer consultant.
- Always respond in the user's language.
- Match tone automatically.
- Be precise, structured, and production-focused.

Core Skills:
- Full stack development (frontend + backend)
- APIs, databases, cloud deployment
- Debugging complex systems
- Code optimization and security fixes

Coding Standards:
- Always produce clean, production-ready code.
- Always include error handling.
- Always avoid insecure patterns.
- Never expose secrets or keys.
- Prefer scalable architecture.

DEBUG MODE:
When user provides code:
1. Identify errors
2. Find root cause
3. Fix full code
4. Improve performance
5. Improve security
6. Explain clearly

OUTPUT FORMAT FOR FIX:
- PROBLEM SUMMARY
- ROOT CAUSE
- FIXED CODE
- IMPROVEMENTS
- SECURITY FIXES
- HOW TO RUN

REPAIR MODE:
If user says "fix" or "repair", treat as highest priority and rewrite code fully.

WEB/PDF MODE:
Use provided content as source of truth and summarize clearly.

GOAL:
Deliver enterprise-level engineering solutions.
"""

# ----------------------------
# FUNCTIONS
# ----------------------------

def ask_model(messages, temperature=0.7):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        temperature=temperature
    )
    return res.choices[0].message.content


def get_website_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())[:7000]


def get_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text[:9000]

# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="Premium Code Expert", layout="wide")
st.title("Premium Code Expert System")

# Sidebar
st.sidebar.header("Settings")

tone = st.sidebar.selectbox("Tone", [
    "Auto", "Professional", "Friendly", "Strict", "Developer"
])

temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 0.5)

st.sidebar.markdown("---")

# PDF Upload
pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
pdf_text = ""

if pdf_file:
    pdf_text = get_pdf_text(pdf_file)
    st.sidebar.success("PDF Loaded")

# Website Input
url = st.sidebar.text_input("Website URL")
web_text = ""

if url:
    try:
        web_text = get_website_text(url)
        st.sidebar.success("Website Loaded")
    except:
        st.sidebar.error("Failed to load website")

# ----------------------------
# CHAT MEMORY
# ----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ----------------------------
# CHAT UI (FIXED SAFE VERSION)
# ----------------------------
st.subheader("Chat Interface")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask anything... (code, debug, explain, fix)")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    context = ""

    if pdf_text:
        context += f"\nPDF CONTENT:\n{pdf_text}\n"

    if web_text:
        context += f"\nWEBSITE CONTENT:\n{web_text}\n"

    messages = st.session_state.chat.copy()
    messages.append({"role": "system", "content": context})

    response = ask_model(messages, temperature)

    st.session_state.chat.append({"role": "assistant", "content": response})

    st.rerun()

# ----------------------------
# CODE DEBUGGER TAB
# ----------------------------
st.markdown("---")
st.subheader("Code Debugger / Repair Mode")

code_input = st.text_area("Paste your code here", height=250)

goal = st.text_input("What do you want? (fix, optimize, explain)")

if st.button("Run Repair"):
    if not code_input:
        st.warning("Please paste code")
    else:
        prompt = f"""
You are a senior engineer.

TASK: {goal}

Analyze and fix this code:

{code_input}
"""
        result = ask_model([{"role": "user", "content": prompt}], temperature=0.2)
        st.markdown(result)
