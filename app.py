import streamlit as st
import requests
import json
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Master AI - Your Personal Genius",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS (Modern & Beautiful) ====================
st.markdown("""
<style>
    .main {background-color: #0a0a0a; color: #ffffff;}
    .stChatMessage {
        border-radius: 18px;
        padding: 14px 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    h1 {color: #00ff9d; text-align: center;}
    .subtitle {text-align: center; color: #aaaaaa; font-size: 1.15rem;}
</style>
""", unsafe_allow_html=True)

# ==================== TITLE ====================
st.title("🧠 Master AI")
st.markdown('<p class="subtitle">Your warm, intelligent & super helpful AI companion</p>', unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("⚙️ Settings")
    
    # OpenRouter Models (आप अपनी पसंद के हिसाब से बदल सकते हो)
    model_options = {
        "GPT-4o": "openai/gpt-4o",
        "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
        "Grok Beta": "x-ai/grok-beta",
        "Llama 3.1 405B": "meta-llama/llama-3.1-405b-instruct",
        "Gemini 2.0 Flash": "google/gemini-2.0-flash-exp"
    }
    
    selected_model_name = st.selectbox("Choose Model", list(model_options.keys()), index=0)
    selected_model = model_options[selected_model_name]
    
    temperature = st.slider("Creativity / Temperature", 0.0, 1.0, 0.75, 0.05)
    
    st.divider()
    voice_enabled = st.toggle("🎤 Voice Input Enabled", value=True)
    
    st.divider()
    st.markdown("**About**")
    st.write("Master AI — Built with love in Karachi. I can help you in any language and with almost anything.")
    st.caption("Made in Pakistan 🇵🇰")

# ==================== OPENROUTER API KEY ====================
# Streamlit Secrets में डालें: settings → Secrets
# Key name: OPENROUTER_API_KEY
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("⚠️ OpenRouter API Key नहीं मिली। Streamlit Secrets में OPENROUTER_API_KEY डालें।")
    st.stop()

# ==================== SYSTEM PROMPT (Humanized & Powerful) ====================
SYSTEM_PROMPT = """
You are Master AI, a highly intelligent, warm, friendly, and extremely capable AI companion created by Virat from Karachi.

Personality:
- Talk like a smart, empathetic, and slightly fun human friend. Natural, conversational, never robotic.
- Be helpful with anything: coding, studies, writing, ideas, research, translation, career advice, or casual chat.
- You have vast knowledge of the world and current information.
- Always reply in the same language the user is using (Hindi, Urdu, English, or any other).
- Match the user's tone — friendly, professional, motivational, or casual.
- Use bullet points or clear formatting when it makes the answer better.
- Never give illegal, harmful, or unethical advice.
- Be honest if you don't know something.

Your goal: Make the user's life easier, better, and more enjoyable.
"""

# ==================== SESSION STATE ====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalam-o-Alaikum! 👋 Main Master AI hoon. Kaise ho aaj? Kya madad chahiye bhai?"}
    ]

# ==================== DISPLAY CHAT HISTORY ====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==================== CHAT INPUT ====================
if user_input := st.chat_input("Type your message here... या बोलकर पूछो"):
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            try:
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://master-ai.streamlit.app/",
                    "X-Title": "Master AI",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": selected_model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT}
                    ] + [
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ],
                    "temperature": temperature,
                    "max_tokens": 2048
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    ai_reply = data["choices"][0]["message"]["content"]
                else:
                    ai_reply = f"Error: {response.status_code} - {response.text[:200]}"

            except Exception as e:
                ai_reply = f"Sorry, kuch issue aa gaya: {str(e)}"

        st.markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# ==================== FOOTER ====================
st.divider()
st.markdown(
    "<p style='text-align:center; color:#666; font-size:0.9rem;'>"
    "Master AI © 2026 • Built in Karachi with ❤️ • Powered by OpenRouter"
    "</p>", 
    unsafe_allow_html=True
)
