
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
from PIL import Image
import io

# --- ULTIMATE CONFIGURATION ---
st.set_page_config(page_title="Master.ai God Mode", page_icon="🧠", layout="wide")

# API Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


# --- HACKER NEON THEME (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; }
    .stButton>button { 
        background: linear-gradient(45deg, #00ffcc, #0055ff); 
        color: white; border-radius: 12px; border: none;
        box-shadow: 0 4px 15px rgba(0, 255, 204, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 255, 204, 0.5); }
    .chat-bubble { background: #111; padding: 15px; border-radius: 15px; border-left: 5px solid #00ffcc; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: THE BRAIN CENTER ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Master.ai v4.0")
    st.subheader("Ultimate Features")
    
    app_mode = st.selectbox("Switch Dimension:", 
        ["Multi-Modal Chat 🤖", "Vision Solver (Image/Docs) 👁️", "Code Architect 💻", "Voice Master 🎙️"])
    
    st.write("---")
    voice_output = st.toggle("Voice Response 🔊", value=True)
    st.info("God Mode: Activated ⚡")

# --- FEATURE 1: MULTI-MODAL CHAT ---
if app_mode == "Multi-Modal Chat 🤖":
    st.title("🚀 Master AI - Universe Brain")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.container():
            st.markdown(f"<div class='chat-bubble'><b>{'You' if m['role']=='user' else 'Master'}:</b><br>{m['content']}</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask anything... I know everything."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Accessing Satellite Data..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            st.markdown(f"<div class='chat-bubble'><b>Master:</b><br>{response.text}</div>", unsafe_allow_html=True)
            
            if voice_output:
                tts = gTTS(text=response.text[:250], lang='en')
                tts.save("voice.mp3")
                st.audio("voice.mp3")
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- FEATURE 2: VISION SOLVER (Homework & Image AI) ---
elif app_mode == "Vision Solver (Image/Docs) 👁️":
    st.title("👁️ Image Intelligence & Solver")
    st.write("Upload any photo, document, or homework problem.")
    
    uploaded_file = st.file_uploader("Drop image here...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=400)
        task = st.text_input("What should I do with this? (e.g. 'Solve this', 'Explain', 'Describe')")
        
        if st.button("Execute Vision Task"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content([task if task else "Describe this image in detail", img])
            st.success("Analysis Complete:")
            st.write(res.text)

# --- FEATURE 3: CODE ARCHITECT ---
elif app_mode == "Code Architect 💻":
    st.title("💻 Master Coding Engine")
    lang = st.selectbox("Language:", ["Python", "HTML/CSS", "JavaScript", "C++"])
    code_req = st.text_area("Describe the app or script you want to build:")
    
    if st.button("Generate Pro Code"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_prompt = f"Act as a Senior Engineer. Write {lang} code for: {code_req}. Explain in Roman Urdu."
        res = model.generate_content(full_prompt)
        st.code(res.text, language=lang.lower())

# --- FEATURE 4: VOICE MASTER ---
elif app_mode == "Voice Master 🎙️":
    st.title("🎙️ Voice Intelligence")
    st.write("This mode focuses on audio interactions and translations.")
    voice_text = st.text_area("Enter text to convert to a professional AI voice:")
    if st.button("Generate AI Voice"):
        tts = gTTS(text=voice_text, lang='en', slow=False)
        tts.save("master_voice.mp3")
        st.audio("master_voice.mp3")

# --- FOOTER ---
st.write("---")
st.caption("Master.ai Pro Max | Powered by Karachi's Future Legend")
          
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="Master.ai Pro Max", layout="wide")


st.markdown("""
    <style>
    .stApp { background: #000000; color: #00ffcc; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(90deg, #00ffcc, #0099ff); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR MODES ---
with st.sidebar:
    st.title("⚡ Master Control")
    mode = st.radio("Select Tool:", ["Smart Chat 💬", "Vision Master (Photo/Docs) 📷", "Expert Coder 💻"])
    st.write("---")
    voice_on = st.checkbox("Enable Voice Response 🔊")

# --- VISION MODE (Photos & Homework Solver) ---
if mode == "Vision Master (Photo/Docs) 📷":
    st.header("📷 Vision Master - Photo & Document Solver")
    uploaded_file = st.file_uploader("Upload a photo or document screenshot...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        user_query = st.text_input("What should I do with this image? (e.g., 'Solve this math problem' or 'Explain this')")
        
        if st.button("Analyze Image"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([user_query if user_query else "Explain this image", image])
            st.markdown(f"### 🤖 Master's Analysis:\n{response.text}")

# --- CHAT MODE (With Voice Support) ---
elif mode == "Smart Chat 💬":
    st.header("💬 Smart Chat with Master.ai")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Ask Master.ai anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
            # VOICE FEATURE
            if voice_on:
                tts = gTTS(text=response.text[:200], lang='en') # پہلا تھوڑا حصہ بولے گا تاکہ لوڈنگ تیز ہو
                tts.save("resp.mp3")
                st.audio("resp.mp3")
                
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- CODER MODE ---
elif mode == "Expert Coder 💻":
    st.header("💻 Expert Coding Assistant")
    code_prompt = st.text_area("What code do you need?")
    if st.button("Generate & Explain"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Write code for: {code_prompt}. Then explain it in Roman Urdu.")
        st.markdown(res.text)
