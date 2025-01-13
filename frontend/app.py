import streamlit as st
import os
from login_page.login_page import login
from sign_up_page.sign_up_page import signup
from main_page.main_page import main_page
from general_ui import UI

# Initialize session state for token and files parsed flag
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "files_parsed" not in st.session_state:
    st.session_state.files_parsed = False

# Main app - handles login and signup navigation
def main():
    UI.apply_all_styles()

    # Sidebar navigation for logo and styling
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_base64 = UI.image_to_base64("R.png")
    my_ui = UI(header_logo=image_base64)

    # Render custom styles and header
    my_ui.render_custom_styles_and_header()

    st.sidebar.image("OIP.jpeg", use_container_width=True)

    # If the user is logged in, directly show the main page
    if st.session_state.access_token:
        main_page()
    
    else:
        # Navigation for Login and Sign Up
        page = st.sidebar.selectbox("Choose an option", ["Login", "Sign Up"])

        if page == "Sign Up":
            signup()
        elif page == "Login":
            login()

if __name__ == "__main__":
    main()
