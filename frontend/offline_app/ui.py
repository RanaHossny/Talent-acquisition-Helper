import streamlit as st
import base64

class PDFUploaderUI:
    """
    Handles the user interface for uploading and interacting with PDFs.
    """

    @staticmethod
    def display_upload_ui():
        """
        Display the upload section in the Streamlit app.

        Returns:
        - List of uploaded files (if any).
        """
        st.title("PDF Uploader and Parser")
        st.write("Upload multiple PDF files to parse them using the backend parser.")
        uploaded_files = st.file_uploader(
            "Choose PDF files (you can upload multiple files)", 
            type=["pdf"], 
            accept_multiple_files=True
        )

        # Provide feedback if no files were uploaded
        if uploaded_files is not None:
            st.write(f"{len(uploaded_files)} file(s) selected.")
        else:
            st.write("No files uploaded yet.")

        return uploaded_files

    @staticmethod
    def display_response(response):
        """
        Display the response from the API.

        Args:
        - response: Response object or dictionary from the API client.
        """
        if response.get("success"):  
            st.success("PDFs uploaded and parsed successfully!")
            st.json(response["data"])  
        else:  
            st.error(f"Error: {response.get('error')}")
            if "details" in response:
                st.text(response["details"])

    @staticmethod
    def display_download_link(file_data, filename):
        """
        Provide a download link for processed PDF data.

        Args:
        - file_data: The content or data to be downloaded.
        - filename: The name for the downloadable file.
        """
        b64 = base64.b64encode(file_data).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download the processed file</a>'
        st.markdown(href, unsafe_allow_html=True)
