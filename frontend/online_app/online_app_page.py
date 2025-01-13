# import os
# import streamlit as st
# from online_app.api import  APIClient
# from online_app.ui import UI
# # Page 2 (Chatbot)
# def page_2():
#     # -------------------------------
#     # Configuration and Initialization
#     # -------------------------------
#     # Initialize session state for chat history and context
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     if "context" not in st.session_state:
#         st.session_state["context"] = ""
    
#     # Sidebar content
#     st.sidebar.write("""
#         About:\n
#         This bot helps Talent Acquisition professionals find the best candidates for the required job.
#         Users can ask for more information about the chosen candidates.
#         """)

#     # Fetch conversations and create buttons for each chat ID
#     selected_conversation_id = None
#     conversations = APIClient.fetch_conversations()
#     for conversation in conversations:
#         chat_id = conversation["id"]
#         button_label = UI.get_button_label(chat_id, conversations)
#         if st.sidebar.button(button_label):
#             selected_conversation_id = chat_id
#             st.session_state["selected_chat"] = chat_id


#     # If a conversation is selected, display its messages
#     if selected_conversation_id or "selected_chat" in st.session_state:
#         selected_conversation_id = selected_conversation_id or st.session_state["selected_chat"]
#         st.session_state["conversation_id"] = selected_conversation_id



 

#     # -------------------------------
#     # Middle Layout: Chat Interface
#     # -------------------------------

#     # Chat container for displaying messages
#     with st.container():
#         st.markdown('<div class="chat-container">', unsafe_allow_html=True)

#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         st.markdown("</div>", unsafe_allow_html=True)

#     # -------------------------------
#     # Chat Input and Response Handling
#     # -------------------------------

#     if prompt := st.chat_input("What is up?"):
#         # Initialize a conversation ID if not already set
#         if "conversation_id" not in st.session_state:
#             st.session_state["conversation_id"] = APIClient.post_conversation()

#         # Display and save the user's message
#         st.chat_message("user").markdown(prompt)
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         st.session_state["context"] += f"User: {prompt}\n"
#         APIClient.post_message("user", prompt, st.session_state["conversation_id"])

#         # response = APIClient.get_conversation_response(prompt, st.session_state["context"])
#         response = "still need to integrate with lightning"

#         if response.strip():
#             st.chat_message("assistant").markdown(response)
#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.session_state["context"] += f"Assistant: {response}\n"
#             APIClient.post_message("assistant", response, st.session_state["conversation_id"])
#         else:
#             st.chat_message("assistant").markdown("Sorry, I didn't get that. Could you try again?")



import os
import streamlit as st
from online_app.api import APIClient
from online_app.ui import UI
from online_app.history_page import show_conversation_history  # Import the history page function

# Page 2 (Chatbot)
def page_2():
    # -------------------------------
    # Configuration and Initialization
    # -------------------------------
    # Initialize session state for chat history and context
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "context" not in st.session_state:
        st.session_state["context"] = ""
    
    # Sidebar content
    st.sidebar.write("""
        About:\n
        This bot helps Talent Acquisition professionals find the best candidates for the required job.
        Users can ask for more information about the chosen candidates.
        """)

    # Fetch conversations and create buttons for each chat ID
    selected_conversation_id = None
    conversations = APIClient.fetch_conversations()
    for conversation in conversations:
        chat_id = conversation["id"]
        button_label = UI.get_button_label(chat_id, conversations)
        if st.sidebar.button(button_label):
            selected_conversation_id = chat_id
            st.session_state["selected_chat"] = chat_id

    # If a conversation is selected, display its messages
    if selected_conversation_id or "selected_chat" in st.session_state:
        selected_conversation_id = selected_conversation_id or st.session_state["selected_chat"]
        st.session_state["conversation_id"] = selected_conversation_id
        
        # Call the function from history_page to show conversation history
        show_conversation_history(conversations, selected_conversation_id)

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

    if prompt := st.chat_input("What is up?"):
        # Initialize a conversation ID if not already set
        # if "conversation_id" not in st.session_state:
        #     st.session_state["conversation_id"] = APIClient.post_conversation()

        # Display and save the user's message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state["context"] += f"User: {prompt}\n"
        # APIClient.post_message("user", prompt, st.session_state["conversation_id"])

        response = APIClient.get_conversation_response(prompt)

        if response.strip():
            st.chat_message("assistant").markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state["context"] += f"Assistant: {response}\n"
            # APIClient.post_message("assistant", response, st.session_state["conversation_id"])
        else:
            st.chat_message("assistant").markdown("Sorry, I didn't get that. Could you try again?")
