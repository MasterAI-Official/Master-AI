import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="AI Custom App", layout="wide", initial_sidebar_state="expanded")

# 2. Master CSS (The "Brutal" OLED Dark Mode based on your 30 Images)
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #000000;
        color: #ECECEC;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #2F2F2F;
    }
    
    /* Custom Menu Cards (Settings/Memories style) */
    .custom-card {
        background-color: #171717;
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #2F2F2F;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.3s;
        cursor: pointer;
    }
    .custom-card:hover {
        background-color: #212121;
        border-color: #444;
    }

    /* ChatGPT Style Chat Input Bar (Capsule Shape) */
    .stChatInputContainer {
        padding-bottom: 20px;
        background-color: transparent !important;
    }
    
    div[data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid #333 !important;
        background-color: #212121 !important;
        padding: 5px 15px;
    }

    /* Action Buttons (Create Image, Write/Edit) */
    .action-btn {
        background-color: #171717;
        border: 1px solid #2F2F2F;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        color: white;
        font-weight: 500;
    }

    /* iOS Style Toggle (Using CSS) */
    .switch {
        position: relative;
        display: inline-block;
        width: 40px;
        height: 22px;
    }
</style>
""", unsafe_allow_html=True)

# 3. JavaScript for Interactive Elements (Voice Pulse & Auto-Scroll)
components.html("""
<script>
    const scrollChat = () => {
        window.scrollTo(0, document.body.scrollHeight);
    }
    // Listen for changes and scroll
    const observer = new MutationObserver(scrollChat);
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", height=0)

# 4. App Logic & UI Structure
def main():
    # Sidebar Navigation (History)
    with st.sidebar:
        st.markdown("<h2 style='color:white;'>ChatGPT</h2>", unsafe_allow_html=True)
        if st.button("＋ New Chat", use_container_width=True):
            st.session_state.messages = []
        
        st.markdown("---")
        st.caption("Recent")
        st.markdown("📁 Project: Drone Tech Nova")
        st.markdown("📁 Mystery Script Part 1")
        st.markdown("📁 Karachi Speed Kix Research")

    # Main Interface
    tab1, tab2 = st.tabs(["💬 Chat", "⚙️ Settings"])

    with tab1:
        # Home Screen Action Cards (Based on your image 1000216467.jpg)
        if "messages" not in st.session_state or len(st.session_state.messages) == 0:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="custom-card">🎨 Create an image</div>', unsafe_allow_html=True)
                st.markdown('<div class="custom-card">💡 Brainstorm</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="custom-card">📝 Write or edit</div>', unsafe_allow_html=True)
                st.markdown('<div class="custom-card">🔍 Deep Research</div>', unsafe_allow_html=True)
        
        # Chat Input
        if prompt := st.chat_input("Message..."):
            with st.chat_message("user"):
                st.markdown(prompt)

    with tab2:
        # Settings & Memories (Based on your images 1000216469.jpg, 1000216474.jpg)
        st.markdown("### Personalization")
        st.markdown('<div class="custom-card">🧠 Memories <span>></span></div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-card">👤 Personal Profile <span>></span></div>', unsafe_allow_html=True)
        
        st.markdown("### Data Controls")
        st.markdown('<div class="custom-card">📤 Export Data <span>></span></div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-card" style="color:#FF4B4B;">🗑️ Delete Account <span>></span></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
            
