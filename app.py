"""Streamlit web interface for Corkaz."""

import os
import streamlit as st
from corkaz.config import Config
from corkaz.ai import CorkAI

st.set_page_config(page_title="Corkaz AI", page_icon="🦘")

st.title("Corkaz AI")
st.subheader("Ngarrindjeri community-led on-Country game guide")

@st.cache_resource
def get_ai():
    config = Config()
    try:
        config.validate()
    except ValueError as exc:
        st.error(f"Configuration error: {exc}")
        st.stop()
    return CorkAI(config=config)

ai = get_ai()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("You:"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Sync AI history with session state if needed, or just let AI handle it
            # The CorkAI class maintains its own history. We just need to stream the response.
            for token in ai.stream_send(prompt):
                full_response += token
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as exc:
            st.error(f"Error: {exc}")

with st.sidebar:
    if st.button("Reset Conversation"):
        ai.reset()
        st.session_state.messages = []
        st.rerun()
