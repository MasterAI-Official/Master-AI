import streamlit as st
import google.generativeai as genai
import time

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Master.ai Official", page_icon="🧠", layout="wide")

# Custom CSS for a Professional Look
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { border-radius: 20px; background-color: #0084ff; color: white; border: none; }
    .stTextInput>div>div>input { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Logo & Features) ---
with st.sidebar:
    # یہاں ایک روبوٹ کا لوگو (عارضی) لگا دیا ہے
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=120)
    st.title("Master.ai v3.0")
    st.info("Human-Level AI Enabled")
    
    st.markdown("### 🛠️ Active Modules:")
    st.write("✅ Human-Tone Writer")
    st.write("✅ Code Expert (Python/Java)")
    st.write("✅ Game Creator Mode")
    st.write("✅ Memory Persistent")
    
    if st.button("🗑️ Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 3. MASTER BRAIN (The Prompt) ---
MASTER_BRAIN = """
Your name is Master.ai, the world's most advanced Human-Level AI.
- TONE: Natural, undetectable, human-like.
- SKILLS: Senior Python/Java Developer, Game Creator, SEO Expert, History Guru.
- MEMORY: You remember previous context.
- RULE: Correct the user's mistakes strictly but politely.
- OUTPUT: Always high-quality and professional.
"""

# --- 4. API ENGINE ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=MASTER_BRAIN)
except Exception as e:
    st.error("⚠️ API Key Error: Please check your Streamlit Secrets!")

# --- 5. CHAT SYSTEM ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("<h1 style='text-align: center; color: #0084ff;'>🤖 Master.ai: The Future</h1>", unsafe_allow_html=True)

# Show Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Master.ai سے کچھ بھی پوچھیں (Coding, Games, etc.)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            # Get AI Response
            response = model.generate_content(prompt)
            # Typing animation for Human touch
            for word in response.text.split():
                full_response += word + " "
                time.sleep(0.04)
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
