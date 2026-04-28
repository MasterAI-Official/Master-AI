import streamlit as st
import google.generativeai as genai
import time

# --- 1. SETTINGS & PAGE CONFIG ---
st.set_page_config(
    page_title="Master.ai Premium",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM CSS (Grok/ChatGPT Style) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0b0e11; color: #e9eaeb; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #15191d !important;
        border-right: 1px solid #30363d;
        width: 300px !important;
    }
    
    /* Chat Message Bubbles */
    .stChatMessage {
        background-color: #1c2128;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #30363d;
    }
    
    /* Input Box Styling */
    .stChatInputContainer {
        padding-bottom: 20px;
        background-color: transparent !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00f2ff;
        color: black;
    }

    /* Custom Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00f2ff, #bc13fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (History & Tools) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00f2ff;'>Master.ai</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=80)
    st.markdown("---")
    
    st.subheader("📝 Recent Chats")
    # یہاں چیٹس کی لسٹ (بناوٹی طور پر) دکھائی دے گی
    st.button("📄 New Chat")
    st.button("📄 Python Expert Bot")
    st.button("📄 Game Logic Fix")
    
    st.markdown("---")
    st.info("👤 **Developer:** Virat Vasu")
    if st.button("🗑️ Clear All Conversations"):
        st.session_state.messages = []
        st.rerun()

# --- 4. ENGINE SETUP ---
SYSTEM_INSTRUCTION = "Your name is Master.ai. You are a premium AI teacher. Be firm, professional, and correct user mistakes immediately."

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=SYSTEM_INSTRUCTION
    )
except Exception as e:
    st.error("API Error! Please check Secrets.")

# --- 5. MAIN CHAT INTERFACE ---
st.markdown("<div class='main-header'>Master.ai Human-Core</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Container for messages to look clean
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input at the bottom
if prompt := st.chat_input("Message Master.ai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            response = model.generate_content(prompt)
            for word in response.text.split():
                full_response += word + " "
                time.sleep(0.04)
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
            
    
