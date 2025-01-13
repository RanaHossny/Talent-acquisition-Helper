import streamlit as st
from offline_app.offline_app_page import page_1
from online_app.online_app_page import page_2

# Initialize flag in session state
if "files_parsed" not in st.session_state:
    st.session_state.files_parsed = False


# Main app
def main_page():
     
    # Only show these two options in the sidebar
    page = st.sidebar.selectbox("Select Page", ["Setup Database", "Chatbot"],)

    if page == "Setup Database":
        page_1()
    elif page == "Chatbot":
        page_2()



