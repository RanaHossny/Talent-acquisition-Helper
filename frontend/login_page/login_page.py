import streamlit as st
from login_page.api import APIClient

def login():
    """
    Displays the login form and interacts with the APIClient to handle login logic.
    """
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Use APIClient to handle login
        response = APIClient.login(username, password)

        if response.status_code == 200:
            st.success("Login successful!")
            token = response.json().get("access_token")

            # Store the token in session state
            st.session_state["access_token"] = token
            st.write("Your access token has been saved to the session.")

            # Rerun the app to avoid showing login page content again
            st.rerun()
        else:
            st.error(response.json().get("detail", "Login failed."))
