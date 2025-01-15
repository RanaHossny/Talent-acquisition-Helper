import os
import streamlit as st
from online_app.api import APIClient
from online_app.ui import UI
from online_app.history_page import show_conversation_history  

# Page 2 (Chatbot)
def page_2():
    # -------------------------------
    # Configuration and Initialization
    # -------------------------------
    # Initialize session state for chat history and context
    if "messages" not in st.session_state:
        st.session_state.messages = []


    if "conversation_id" not in st.session_state:
                st.session_state["conversation_id"] = None
    
    # Sidebar content
    st.sidebar.write("""
        About:\n
        This bot helps Talent Acquisition professionals find the best candidates for the required job.
        Users can ask for more information about the chosen candidates.
        """)

    # Fetch conversations and create buttons for each chat ID
    if "token_conversation" not in st.session_state:
        st.session_state["token_conversation"]=True

    conversations = APIClient.fetch_conversations()
    for conversation in conversations:

        button_label = UI.get_button_label(conversation["id"], conversations)
        if st.sidebar.button(button_label):
            st.session_state["selected_chat"] = conversation

    # If a conversation is selected, display its messages
    if  "selected_chat" in st.session_state and st.session_state["selected_chat"] and st.session_state["conversation_id"]!=st.session_state["selected_chat"]["id"]:
        st.session_state["conversation_id"] = st.session_state["selected_chat"]["id"]
        # Call the function from history_page to show conversation history
        st.session_state["token_conversation"]=st.session_state["selected_chat"]["token_valid"]
        show_conversation_history(conversations, st.session_state["selected_chat"]["id"])


    # -------------------------------
    # Middle Layout: Chat Interface
    # -------------------------------

    # Chat container for displaying messages
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------
    # Chat Input and Response Handling
    # -------------------------------
    if(st.session_state["token_conversation"]):
        if prompt := st.chat_input("What is up?"):
            # Initialize a conversation ID if not already set
            if not st.session_state["conversation_id"]:
                st.session_state["conversation_id"] = APIClient.post_conversation()

            # Display and save the user's message
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            APIClient.post_message("user", prompt, st.session_state["conversation_id"])

            response = APIClient.get_conversation_response(prompt)

            if response.strip():
                st.chat_message("assistant").markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                APIClient.post_message("assistant", response, st.session_state["conversation_id"])
            else:
                st.chat_message("assistant").markdown("Sorry, I didn't get that. Could you try again?")
    else:
        st.warning("The conversation cannot be completed because the database in use is unavailable.")
        st.session_state["token_conversation"]=True
