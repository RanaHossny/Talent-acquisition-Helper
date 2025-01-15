import requests
import streamlit as st
import os
backend_url = os.getenv("BACKEND_URL", "http://localhost:8001")
class APIClient:
    """
    A client for interacting with the local Django REST API.
    """
    BASE_URL = f"{backend_url}/chatbot"

    @staticmethod
    def get_headers():
        """
        Generates the headers for the API requests, including the Authorization token.
        """
        if "access_token" in st.session_state:
            return {
                "Authorization": f"Bearer {st.session_state['access_token']}",
                "Content-Type": "application/json",
            }
        else:
            raise ValueError("Access token not found in session state.")

    @staticmethod
    def post_conversation():
        """
        Creates a new conversation via the API.
        """
        url = f"{APIClient.BASE_URL}/conversations/"
        data = {}

        try:
            response = requests.post(url, json=data, headers=APIClient.get_headers())
            response.raise_for_status()
            return response.json().get("id")  
        except requests.exceptions.RequestException as e:
            print(f"Failed to create conversation: {e}")
            return None

    @staticmethod
    def post_message(sender, content, conversation_id):
        """
        Sends a message within a conversation via the API.
        """
        url = f"{APIClient.BASE_URL}/messages/"
        data = {
            "sender": sender,
            "content": content,
            "conversation_id": conversation_id,
        }

        try:
            response = requests.post(url, json=data, headers=APIClient.get_headers())
            response.raise_for_status()
            return response.json()  
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message: {e}")
            return None

    @staticmethod
    def fetch_conversations():
        """
        Fetches a list of all conversations from the API.
        """
        url = f"{APIClient.BASE_URL}/conversations/"

        try:
            response = requests.get(url, headers=APIClient.get_headers())
            response.raise_for_status()
            return response.json()  
        except requests.exceptions.RequestException as e:
            print(f"Error fetching conversations: {e}")
            return []

    @staticmethod
    def get_conversation_response(prompt):
        """
        Gets a conversation response from the API based on user input and context.
        """
        url = "https://8001-01jhhtwya97h5wp60v4q27p9xy.cloudspaces.litng.ai/query"
        payload = {
            "user_input": prompt,
        }
    
        try:
            response = requests.post(url, json=payload, headers=APIClient.get_headers())
            response.raise_for_status()
            return response.json().get("response", "No response found")
        except requests.exceptions.RequestException as e:
            print(f"Error getting conversation response: {e}")
            return None
    