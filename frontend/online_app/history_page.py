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



# -------------------------------
# Chat Interface: Display Messages and Input
# -------------------------------

def chat_interface():
    # Middle Layout: Chat Interface
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        # Display the current conversation's messages
        for message in st.session_state.get("messages", []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        st.markdown("</div>", unsafe_allow_html=True)

    # Chat Input and Response Handling
    if prompt := st.chat_input("What is up?"):
        # Initialize a conversation ID if not already set
        if "conversation_id" not in st.session_state:
            st.session_state["conversation_id"] = APIClient.post_conversation()

        # Display and save the user's message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state["context"] += f"User: {prompt}\n"
        APIClient.post_message("user", prompt, st.session_state["conversation_id"])

        # Simulate response (replace this with actual API call)
        response = "still need to integrate with lightning"

        if response.strip():
            st.chat_message("assistant").markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state["context"] += f"Assistant: {response}\n"
            APIClient.post_message("assistant", response, st.session_state["conversation_id"])
        else:
            st.chat_message("assistant").markdown("Sorry, I didn't get that. Could you try again?")
