import streamlit as st
import google.generativeai as genai
import time

# --- 1. PAGE & UI CONFIG ---
st.set_page_config(page_title="Master.ai Premium", page_icon="🤖", layout="wide")

# Grok/ChatGPT Style CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    section[data-testid="stSidebar"] { background-color: #15191d !important; border-right: 1px solid #30363d; }
    .stChatMessage { background-color: #1c2128; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
    h1 { background: -webkit-linear-gradient(#00f2ff, #bc13fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #00f2ff;'>Master.ai v4.0</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=80)
    st.markdown("---")
    st.subheader("📝 Recent Chats")
    st.button("➕ New Chat", on_click=lambda: st.session_state.clear())
    st.info("👤 Developer: Virat Vasu")

# --- 3. CORE ENGINE (THE BUG FIXER) ---
# Yahan hum multiple models check karenge taake 404 na aaye
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Try Flash first, then Pro as backup
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        # Test connection
        test = model.generate_content("hi") 
    except:
        model = genai.GenerativeModel('gemini-pro')

    system_instruction = "Your name is Master.ai. You are an expert teacher. Correct user mistakes firmly and be human-like."
except Exception as e:
    st.error(f"Critical Setup Error: {e}")

# --- 4. CHAT INTERFACE ---
st.markdown("<h1>Master.ai: Human-Core</h1>", unsafe_allow_html=True)

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
        response_area = st.empty()
        full_res = ""
        try:
            # Combined prompt with system instruction
            response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
            
            # Streaming typing effect
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.04)
                response_area.markdown(full_res + "▌")
            response_area.markdown(full_res)
        except Exception as e:
            st.error(f"Logic Error: {e}. Please check your API Quota or Internet.")
            
    st.session_state.messages.append({"role": "assistant", "content": full_res})
            
