import streamlit as st
import google.generativeai as genai

# Page Settings
st.set_page_config(page_title="Master.ai", page_icon="🤖")

# API Configuration
try:
    # Secrets se key uthana
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Sab se stable model use karna
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Secrets configuration error!")

# UI
st.title("🤖 Master.ai: Human-Core")
st.write("Developed by Virat Vasu")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Master.ai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            
    
