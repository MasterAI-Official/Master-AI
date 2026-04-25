import streamlit as st
import google.generativeai as genai
import time

# --- 1. SETTING THE VIBE (UI CONFIG) ---
st.set_page_config(page_title="Master.ai Pro", page_icon="⚡", layout="wide")

# --- 2. THE ULTIMATE CSS (Hacker Style) ---
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stTextInput>div>div>input { border: 2px solid #00ffcc; border-radius: 20px; background-color: #1a1a1a; color: #00ffcc; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0099ff); color: black; font-weight: bold; border-radius: 25px; transition: 0.3s; border: none; }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0px 0px 20px #00ffcc; }
    .chat-card { background: #111; border-radius: 15px; padding: 20px; border-left: 5px solid #00ffcc; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE BRAIN (API KEY) ---
genai.configure(api_key="AIzaSyA9Vs7JK0nXUmZHcJVv0sofdC_Ujuvx-es")

# --- 4. SIDEBAR - THE COMMAND CENTER ---
with st.sidebar:
    st.markdown("<h1 style='color: #00ffcc;'>⚡ MASTER.AI PRO</h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.write("---")
    
    # Advanced Settings
    ai_power = st.select_slider("Select Intelligence Level:", options=["Base", "Smart", "Ultra"])
    feature_mode = st.selectbox("Switch Tool:", ["General Chat", "Expert Coder 💻", "Creative Writer ✍️", "Future Predictor 🔮"])
    
    st.write("---")
    if st.button("🔥 Reset System"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<p style='color: gray;'>Version 3.0 | Developed by Master</p>", unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.title("⚡ Master.ai - The Next Frontier")
st.write(f"Status: **{feature_mode} Mode Online**")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying chat with a custom "Card" look
for message in st.session_state.messages:
    with st.container():
        role_label = "👤 You" if message["role"] == "user" else "🤖 Master"
        st.markdown(f"<div class='chat-card'><b>{role_label}:</b><br>{message['content']}</div>", unsafe_allow_html=True)

# User Input
if prompt := st.chat_input("Connect with the future..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Custom instructions based on mode
    system_instruction = ""
    if feature_mode == "Expert Coder 💻":
        system_instruction = "Give advanced code and explain it in Roman Urdu. Be a pro developer."
    elif feature_mode == "Creative Writer ✍️":
        system_instruction = "Write amazing stories or scripts in a very professional way."
    
    full_query = f"{system_instruction} {prompt}"

    with st.chat_message("assistant"):
        with st.spinner("Decoding from the Matrix..."):
            try:
                # Using Gemini 1.5 Flash for speed
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(full_query)
                
                # Typing effect simulation
                placeholder = st.empty()
                full_res = ""
                for chunk in response.text.split():
                    full_res += chunk + " "
                    time.sleep(0.05)
                    placeholder.markdown(full_res + "▌")
                placeholder.markdown(full_res)
                
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Error connecting to the AI core. Check your API key.")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("Master.ai - Powering the Tech Revolution in Karachi 🇵🇰")
