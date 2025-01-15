import streamlit as st
from online_app.api import APIClient  

# -------------------------------
# History Page: Display Selected Conversation
# -------------------------------

import streamlit as st

def show_conversation_history(conversations, selected_conversation_id):
    # Clear the chat history to avoid showing previous messages
    st.session_state.messages = []  
    
    # Fetch messages for the selected conversation
    messages = [
        msg for conv in conversations if conv["id"] == selected_conversation_id
        for msg in conv.get("messages", [])
    ]
    
    st.title(f"Conversation {selected_conversation_id}")
    
    # Iterate through each message in the selected conversation
    for message in sorted(messages, key=lambda x: x["timestamp"]):
        sender = "User" if message["sender"] == "user" else "Assistant"
        content = message["content"]
    
        # Display each message using `st.chat_message`
        with st.chat_message(sender.lower()):
            st.markdown(f"**{sender}**: {content}")
    
    # Reset the selected_conversation_id to avoid displaying the same chat again
    selected_conversation_id = None
    st.session_state["selected_chat"] = None  # Reset session state for selected chat




