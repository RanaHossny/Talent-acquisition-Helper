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
    def image_to_base64(image_path):
        """
        Convert an image file to a base64-encoded string for use in Markdown or other formats.
        """
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    def render_custom_styles_and_header(self):
        """
        Helper function to load the CSS styles and render the header with the title and logo.
        """
        st.markdown(
        """
        <style>
        /* Fix the header with logo and photo */
        .header-container {
            display: flex;
            align-items: center;
            position: fixed;
            top: 30px;  /* Adjust this value to move the header down */
            width: 100%;
            background-color: transparent;  /* Set background to transparent */
            padding: 12px 20px;
            z-index: 6000;
        }
        .header-container h1 {
            margin-right: 20px;
            color: #000;  
        }
        .header-container img {
            margin-left: 20px;
        }

        /* Style the chat container with scroll */
        .chat-container {
            max-height: 500px;  /* Adjust height for chat container */
            overflow-y: auto;   /* Enables vertical scrolling for chat */
            padding: 50px;
            margin-top: 200px;   /* Create space below the fixed header */
        }

        /* Style for sidebar */
        .sidebar {
            padding-top: 70px; /* Adjust space below header */
        }
        </style>
        """,
        unsafe_allow_html=True
        )

        if self.header_logo:
            st.markdown(
            f"""
            <div class="header-container">
                <h1>{self.header_title}</h1>
            <img src="data:image/jpeg;base64,{self.header_logo}" width="150">
            </div>
            """,
            unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"""
                <div class="header-container">
                    <h1>{self.header_title}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
    @staticmethod
    def set_main_app_background():
        """Set the background for the main app content."""
        st.markdown(
        f"""
        <style>
        /* Main app content background */
        .stApp {{
            background: url("https://img.freepik.com/free-vector/white-background-with-hexagonal-line-pattern-design_1017-28442.jpg?t=st=1736337365~exp=1736340965~hmac=9ba86eb549a87d06bfc5ac2b8676f7397b38a7dc862bc4af680160bc53898f60&w=1060") no-repeat center center fixed; 
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    @staticmethod
    def set_sidebar_background():
        """Set the background for the sidebar."""
        st.markdown(
        f"""
        <style>
        /* Sidebar background */
        .stSidebar {{
            background: rgba(255, 255, 255, 0.8);  /* Optional: Set a light translucent background for sidebar */
            background-image: url("https://img.freepik.com/free-vector/light-wave-border-background_53876-81563.jpg?t=st=1736345132~exp=1736348732~hmac=4af4723adb2edf1db4972da3ab38e53a84bd11c6a9b4ab6c300d41df5cd395b8&w=740");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
        )

    @staticmethod
    def set_sidebar_text_color():
        st.markdown("""
         <style>
        .stSidebar .stSelectbox label {
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
    <style>
    .stSidebar .stMarkdown p {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    @staticmethod
    def apply_all_styles():
        """Apply all styles for the background and sidebar."""
        UI.set_main_app_background()
        UI.set_sidebar_background()
        UI.set_sidebar_text_color()
