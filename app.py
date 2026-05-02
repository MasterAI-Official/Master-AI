import streamlit as st
import time

# --- 1. SYSTEM PROMPT & DOMAIN INTELLIGENCE ---
# This ensures the AI always acts within your specific parameters
SYSTEM_PROMPT = """
Role: Nova AI Premium Assistant.
Visual Context: Mobile-first OLED Black interface.
Personalization Memory: 
- User prefers Comma or Wolf cut hairstyles.
- User is an expert in Pigeon breeds (Lal Gandedar, Chitte White).
- Knowledge Focus: DJI Mini 3, Redmi Smartphones, YouTube SEO (Tech Nova, Master Minds).
- Local Intelligence: Karachi focus (Landmarks, Speed Kix motorcycle dealership).
Tone: Snappy, high-end, multi-part mystery narrative capability.
"""

# --- 2. PAGE CONFIG & UI THEME (OLED BLACK) ---
st.set_page_config(page_title="Nova AI", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for the "OLED Black" Standard and "Floating Capsule"
st.markdown(f"""
    <style>
    /* OLED Black Standard */
    .stApp {{
        background-color: #000000;
        color: #ECECEC;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: #171717;
        border-right: 1px solid #212121;
    }}

    /* Typography */
    h1, h2, h3, p, span, label {{
        color: #ECECEC !important;
        font-family: 'Inter', sans-serif;
    }}
    .secondary-label {{
        color: #B4B4B4 !important;
        font-size: 0.8rem;
    }}

    /* The Capsule Interface (Floating Pill Input) */
    .stChatInputContainer {{
        padding-bottom: 20px;
    }}
    .stChatInputContainer > div {{
        background-color: #171717 !important;
        border: 1px solid #212121 !important;
        border-radius: 30px !important; /* 30px Border Radius */
        padding: 8px 15px;
    }}

    /* Interactive Cards */
    .action-card {{
        background-color: #171717;
        border: 1px solid #212121;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        transition: 0.3s ease;
    }}
    .action-card:hover {{
        background-color: #212121;
        border-color: #ECECEC;
    }}

    /* Voice Mode Overlay */
    .voice-mode {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: #000000;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    
    /* Animation for Waveform */
    .waveform {{
        display: flex;
        align-items: center;
        gap: 5px;
    }}
    .bar {{
        width: 4px;
        height: 20px;
        background: #ECECEC;
        border-radius: 10px;
        animation: wave 1s infinite ease-in-out;
    }}
    @keyframes wave {{
        0%, 100% {{ height: 10px; }}
        50% {{ height: 50px; }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE (MEMORY) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "voice_active" not in st.session_state:
    st.session_state.voice_active = False

# --- 4. SIDEBAR (HIERARCHICAL SETTINGS) ---
with st.sidebar:
    st.title("Nova Settings")
    
    with st.expander("Personalization"):
        st.toggle("Memory Toggles", value=True)
        st.write("Current Style: Comma/Wolf Cut")
        st.write("Hobby: Pigeon Breeding")
        
    with st.expander("Data Controls"):
        st.button("Export Chat History")
        st.button("Archive Conversations")
        if st.button("Permanently Delete", type="primary"):
            st.session_state.messages = []
            
    with st.expander("Security"):
        st.toggle("Parental Controls", value=False)
        st.button("Account Linking")

# --- 5. VOICE MODE UI ---
if st.session_state.voice_active:
    st.markdown("""
        <div class="voice-mode">
            <div class="waveform">
                <div class="bar" style="animation-delay: 0.0s"></div>
                <div class="bar" style="animation-delay: 0.1s"></div>
                <div class="bar" style="animation-delay: 0.2s"></div>
                <div class="bar" style="animation-delay: 0.3s"></div>
                <div class="bar" style="animation-delay: 0.4s"></div>
            </div>
            <p style="margin-top:20px;">Listening to your request...</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Exit Voice Mode"):
        st.session_state.voice_active = False
        st.rerun()
    st.stop()

# --- 6. MAIN INTERFACE ---
st.markdown("### Nova AI")
st.markdown("<p class='secondary-label'>Premium Intelligence • Karachi Node</p>", unsafe_allow_html=True)

# Action Cards
cols = st.columns(3)
with cols[0]:
    st.markdown('<div class="action-card">🎨 <b>Create</b><br><span class="secondary-label">Visuals</span></div>', unsafe_allow_html=True)
with cols[1]:
    st.markdown('<div class="action-card">✍️ <b>Write</b><br><span class="secondary-label">Mystery Suite</span></div>', unsafe_allow_html=True)
with cols[2]:
    st.markdown('<div class="action-card">🔍 <b>Research</b><br><span class="secondary-label">Deep Dive</span></div>', unsafe_allow_html=True)

# Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. CHAT LOGIC (THE BRAIN) ---
if prompt := st.chat_input("Ask about DJI, Pigeons, or Tech Nova..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Simple Logic simulating the knowledge requested
        if "pigeon" in prompt.lower():
            ai_text = "I've logged your focus on Lal Gandedar and Chitte White breeds. Are we analyzing bloodlines or looking for market updates in Karachi?"
        elif "hair" in prompt.lower() or "style" in prompt.lower():
            ai_text = "Considering your preference for Comma and Wolf cuts, I recommend a high-hold matte pomade for the humid Karachi weather."
        elif "dji" in prompt.lower() or "mini 3" in prompt.lower():
            ai_text = "The DJI Mini 3 is perfect for Karachi's coastline. Remember to check local drone regulations and YouTube SEO keywords for 'Tech Nova'."
        elif "story" in prompt.lower():
            ai_text = "The shadows stretched across the Speed Kix showroom... (Part 1 of your Mystery Narrative is starting)."
        else:
            ai_text = "Processing your request through the Nova neural net. How can I assist with your YouTube SEO or Redmi smartphone specs today?"

        # Snappy typing animation
        for chunk in ai_text.split():
            full_response += chunk + " "
            time.sleep(0.05)
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Voice Mode Trigger (Fixed Floating)
st.sidebar.divider()
if st.sidebar.button("🎤 Open Voice Mode"):
    st.session_state.voice_active = True
    st.rerun()
