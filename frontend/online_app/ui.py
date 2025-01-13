import streamlit as st
import base64

class UI:
    def __init__(self, header_title="Talent Acquisition Helper", header_logo=None):
        """
        Initialize the UI class with a header title and an optional header logo in base64 format.
        """
        self.header_title = header_title
        self.header_logo = header_logo

    @staticmethod
    def get_button_label(conversation_id, conversations):
        """
        Find the conversation by its ID and return a button label
        with the first 5 words of the first user message.
        """
        # Find the conversation by its ID
        conversation = next((conv for conv in conversations if conv["id"] == conversation_id), None)

        if conversation is None:
            return f"Chat {conversation_id}: No conversation found"

        # Extract the first message from the 'user'
        first_message = next(
            (msg['content'] for msg in conversation['messages'] if msg['sender'] == 'user'), 
            "No user message"
        )

        # Return the button label with the first 5 words of the message
        return f"Chat {conversation_id}: {' '.join(first_message.split()[:5])}..."




