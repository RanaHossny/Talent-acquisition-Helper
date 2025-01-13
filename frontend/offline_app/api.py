import requests
import streamlit as st
class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def upload_pdfs(self, zip_buffer):
            endpoint = f"{self.base_url}/retriever/upload-pdf/"

            # Retrieve the access token from session state
            access_token = st.session_state.get("access_token", None)

            if not access_token:
                return {"success": False, "error": "Access token not found."}

            # Set up headers with the token for authentication
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            # Prepare files for the POST request
            files = {
                'file': ('uploaded_pdfs.zip', zip_buffer, 'application/zip')
            }

            try:
                # Send the POST request with the access token in headers
                response = requests.post(endpoint, headers=headers, files=files)
                print(f"Response Status Code: {response.status_code}")
                print(f"Response Content: {response.content}")  # Log the raw response content

                if response.status_code == 201:
                    return response.json()
                return {"success": False, "error": response.json()}
            except Exception as e:
                return {"success": False, "error": str(e)}




    def get_user_collection(self):
        # Define the endpoint for getting the user's collection name
        endpoint = f"{self.base_url}/api/collection/"

        # Retrieve the access token from session state
        access_token = st.session_state.get("access_token", None)

        if not access_token:
            return {"success": False, "error": "Access token not found."}

        # Set up headers with the token for authentication
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            # Send the GET request with the access token in headers
            response = requests.get(endpoint, headers=headers)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.content}")  # Log the raw response content

            if response.status_code == 200:
                # Assuming the response contains the collection name as part of the JSON response
                return response.json()  # or response.json()['name'] if only the name is needed
            return {"success": False, "error": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_collection_name(self, collection_name):
        endpoint = "https://8001-01jhd73nrtd9bf4m8n8d9ctmj5.cloudspaces.litng.ai/send_collection_name/"

    

        try:
            # Send the POST request
            response = requests.post(endpoint,data=collection_name)

            # Log the response for debugging
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")

            # Return the JSON response or an error
            if response.status_code == 200:
                return response.json()
            return {"success": False, "error": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}