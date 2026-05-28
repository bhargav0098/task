import streamlit as st
import requests

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

BACKEND_URL = "http://localhost:3000/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = requests.post(BACKEND_URL, json={"message": user_input})
            if response.status_code == 200:
                reply = response.json().get("reply", "No response received.")
                message_placeholder.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                error_msg = f"Error: Backend returned status code {response.status_code}"
                message_placeholder.markdown(error_msg)
        except requests.exceptions.ConnectionError:
            message_placeholder.markdown("Error: Could not connect to the backend server. Is it running on port 3000?")