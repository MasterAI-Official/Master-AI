import streamlit as st
import google.generativeai as genai
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Master.ai | Human-Core AI",
    page_icon="🤖",
    layout="wide"
)

# --- 2. PREMIUM DESIGN (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; }
    .stButton>button { border-radius: 20px; background: linear-gradient(90deg, #00f2ff, #bc13fe); color: white; border: none; width: 100%; }
    h1 { color: #00f2ff; text-align: center; font-family: 'Poppins', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR BRANDING ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)
    st.title("Master.ai v4.0")
    st.markdown("---")
    st.info("🚀 System: Online")
    st.success("🧠 Brain: Unlimited")
    if st.button("🗑️ Clear Deep Memory"):
        st.session_state.messages = []
        st.rerun()

# --- 4. THE MASTER PROMPT (Teacher Mode) ---
MASTER_PROMPT = "Your name is Master.ai. You are a world-class AI mentor. Correct user mistakes firmly, speak like a human, and provide expert code/logic."

# --- 5. API ENGINE (FIXED) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Yahan model name bilkul sahi format mein hai
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=MASTER_PROMPT
    )
except Exception as e:
    st.error("API Key Error in Secrets!")

# --- 6. CHAT INTERFACE ---
st.markdown("<h1>🤖 Master.ai: Human-Core Engine</h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Developed by Virat Vasu</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Master.ai anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        try:
            # Memory handling
            response = model.generate_content(prompt)
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.04)
                placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_res})
    
