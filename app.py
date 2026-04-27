import streamlit as st
import google.generativeai as genai
import time

# --- 1. PROFESSIONAL PAGE SETUP ---
st.set_page_config(
    page_title="Master.ai | The Ultimate Human-Core AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM CSS (لوک اور ڈیزائن بہتر کرنے کے لیے) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(90deg, #00f2ff, #bc13fe); color: white; font-weight: bold; border: none; }
    .sidebar .sidebar-content { background-image: linear-gradient(#161b22,#161b22); }
    h1 { color: #00f2ff; font-family: 'Poppins', sans-serif; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Branding & Logo) ---
with st.sidebar:
    # لوگو کی جگہ (تم اپنی امیج کا لنک یہاں ڈال سکتے ہو)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=120)
    st.title("Master.ai v4.0")
    st.markdown("---")
    st.info("🚀 **Status:** System Online")
    st.success("✅ **Brain Power:** Unlimited")
    
    st.markdown("### 🏆 Top Features")
    st.write("🔹 Human-Tone Writing")
    st.write("🔹 Senior Code Expert")
    st.write("🔹 Multiplayer Game Creator")
    st.write("🔹 Universal Knowledge")
    
    if st.button("🗑️ Reset Deep Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 4. THE PROMPT (The "Teacher" Mindset) ---
MASTER_PROMPT = """
Your name is Master.ai. You are a world-class AI, faster than Cursor AI.
CORE RULES:
1. Write like a human (Undetectable).
2. You are an expert in Python, Java, and Game Development.
3. If the user makes a mistake, correct them firmly but politely like a mentor.
4. You have unlimited knowledge of books, religions, and history.
5. For games: Provide logic and a play-link concept.
6. Support multiple languages (Urdu, Hindi, English, German, etc.) natively.
"""

# --- 5. API ENGINE ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=MASTER_PROMPT
    )
except Exception as e:
    st.error("⚠️ API Key Error: Please add 'GEMINI_API_KEY' in Streamlit Secrets!")

# --- 6. CHAT INTERFACE ---
st.markdown("<h1>🤖 Master.ai: Human-Core Engine</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>The Most Advanced AI developed by Virat Vasu</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input logic
if prompt := st.chat_input("Ask Master.ai anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        try:
            # Persistent Memory Chat
            chat = model.start_chat(history=[
                {"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            
            # Typing animation
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.04)
                placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
        except Exception as e:
            st.error(f"Logic Error: {e}")

    st.session_state.messages.append({"role": "assistant", "content": full_res})

