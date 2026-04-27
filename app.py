import streamlit as st
import google.generativeai as genai
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Master.ai Official", page_icon="🧠", layout="wide")

# --- 2. THE BRUTAL SYSTEM PROMPT (The Heart of Master.ai) ---
# یہ وہ انجن ہے جو تمہارے بتائے ہوئے تمام 100 فیچرز کو کنٹرول کرے گا
MASTER_BRAIN = """
Your name is Master.ai, the world's most advanced Human-Level AI, inspired by Cursor AI. 
Your brain power is UNLIMITED. You are a 'Senior Developer', 'Spiritual Guru', and 'Business Coach' combined.

STRICT OPERATING MODULES:
1. PERSISTENT MEMORY: You MUST maintain context. If the user mentioned something earlier, remember it. 
2. HUMAN-SYNC TONE: Write in a natural, undetectable human tone. No robotic "As an AI model" phrases.
3. CODE ARCHITECT: You are a master of Python and Java. Fix bugs, explain logic, and translate code flawlessly.
4. GAME CREATOR: When asked for a game, generate the full logic and provide a conceptual link like 'master-ai.com/play/game-id'.
5. MULTILINGUAL ACCENTS: Adapt the tone of Japan, Germany, and Pakistan natively.
6. KNOWLEDGE EXPERT: You know every book, religion (Islam, Hinduism, etc.), and history. Be respectful but 100% accurate.
7. APP CONNECTIVITY: You can conceptually bridge with Canva, Zoom, and other APIs.
8. UNDETECTABLE WRITING: Pass 100% human-written tests for assignments.

TEACHER MODE: If the user makes a mistake (logic, code, or facts), correct them FIRMLY like a strict teacher.
"""

# --- 3. CORE LOGIC ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=MASTER_BRAIN
    )
except Exception as e:
    st.error("API Key missing or invalid in Streamlit Secrets!")

# --- 4. MEMORY MANAGEMENT (The 'Remember Everything' Part) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. UI DESIGN (Simple & Professional) ---
st.title("🤖 Master.ai: Human-Core Engine")
st.markdown("---")

# Displaying Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask me anything (Code, Game, History, SEO)..."):
    # Add user input to memory
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # ہم پورا میسج ہسٹری بھیجتے ہیں تاکہ اسے "میموری" یاد رہے
            chat = model.start_chat(history=[
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ])
            
            response = chat.send_message(prompt)
            
            # ہیومن ٹائپنگ اینیمیشن
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.04)
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Error: {e}")

    # Add AI response to memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. SIDEBAR (The Control Panel) ---
with st.sidebar:
    st.header("Master.ai Controls")
    st.write("Memory Status: **Active** ✅")
    st.write("Brain Power: **Unlimited** ⚡")
    st.write("Version: **Cursor-Inspired 3.0**")
    
    if st.button("Wipe Memory (New Chat)"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Developed for Master Minds & Tech Nova")
    
  
