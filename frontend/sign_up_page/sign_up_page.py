import streamlit as st
from sign_up_page.api import APIClient

def signup():
    """
    Displays the signup form and interacts with the APIClient to handle signup logic.
    """
    st.title("Sign Up")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != password_confirm:
            st.error("Passwords do not match.")
        else:
            # Use APIClient to handle signup
            response = APIClient.signup(username, email, password, password_confirm)

            if response.status_code == 201:
                st.success("Signup successful! You are now logged in.")
                token = response.json().get("access_token")

                # Store the token in session state
                st.session_state["access_token"] = token
                st.write("Your access token has been saved to the session.")

                # Rerun the app to avoid showing signup page content again
                st.rerun()
            else:
                st.error(response.json().get("detail", "Signup failed."))
