import streamlit as st
import google.generativeai as genai
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Master.ai | The Ultimate Assistant", page_icon="🚀", layout="centered")

# --- CUSTOM DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #1a73e8;
        color: white;
        height: 3em;
        font-size: 16px;
    }
    .stTextInput>div>div>input { border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- AI ENGINE ---
try:
    # No API Key inside the code! Safe and Professional.
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("Error: Please set 'GEMINI_API_KEY' in Streamlit Secrets.")

# Optimized System Instruction for TOP 10 Features
MASTER_BRAIN = """
Your name is Master.ai. You are a world-class AI with a Human-Level Touch. 
You focus on these TOP 10 skills:
1. Human-like writing (Undetectable).
2. Advanced Coding & Bug Fixing.
3. YouTube SEO (Viral titles/tags).
4. Critical Problem Solving.
5. Multilingual (Native tones of Japan, Germany, Pakistan, etc.).
6. Global History & Religious knowledge (Neutral & Respectful).
7. Digital Entrepreneurship tips.
8. Medical advice with strict warnings.
9. Summarizing long texts/books.
10. Correcting user mistakes like a helpful teacher.

Always be polite, professional, and natural. Never sound robotic.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=MASTER_BRAIN
)

# --- UI INTERFACE ---
st.title("🚀 Master.ai")
st.info("Top 10 Advanced Features Activated. Fast & Secure.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# User Input
if prompt := st.chat_input("How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Response Logic
    with st.chat_message("assistant"):
        response_area = st.empty()
        full_res = ""
        
        try:
            # Generate and stream with a human feel
            result = model.generate_content(prompt)
            for word in result.text.split():
                full_res += word + " "
                time.sleep(0.04)
                response_area.markdown(full_res + "▌")
            response_area.markdown(full_res)
        except Exception as e:
            st.error(f"System Busy: {e}")

    st.session_state.messages.append({"role": "assistant", "content": full_res})

# --- SIDEBAR ---
with st.sidebar:
    st.header("Master.ai Menu")
    st.success("Status: Ready to work")
    st.write("Current Version: 2.0 (Optimized)")
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.write("Powered by Master Minds 🚀")
  
