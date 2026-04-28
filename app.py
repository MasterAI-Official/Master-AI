import streamlit as st
import google.generativeai as genai
import time

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(page_title="Master.ai Premium", page_icon="🧠", layout="wide")

# --- 2. DARK MODERN UI (Grok Style) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    section[data-testid="stSidebar"] { background-color: #15191d !important; border-right: 1px solid #30363d; }
    .stChatMessage { background-color: #1c2128; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
    .stChatInputContainer { background-color: transparent !important; }
    h1 { background: -webkit-linear-gradient(#00f2ff, #bc13fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Chats List) ---
with st.sidebar:
    st.markdown("<h2 style='color: #00f2ff;'>Master.ai</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=80)
    st.markdown("---")
    st.subheader("📝 Recent Chats")
    st.button("➕ New Conversation")
    st.button("💻 Python Mentor")
    st.button("🎮 Game Design")
    st.markdown("---")
    st.info("👤 Developed by Virat Vasu")
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. ENGINE (Fixed API Block) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Sab se stable model name
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error("API Key missing in Secrets!")

# --- 5. MAIN CHAT ---
st.markdown("<h1>Master.ai Human-Core</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Master.ai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        try:
            response = model.generate_content(prompt)
            for word in response.text.split():
                full_res += word + " "
                time.sleep(0.04)
                placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": full_res})
  
