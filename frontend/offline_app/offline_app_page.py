import streamlit as st
from offline_app.api import APIClient
import os
import zipfile
import io

# Page 1 (PDF Uploader and Parser)
def page_1():
    api_client = APIClient()
    collection_name=api_client.get_user_collection()
    api_client.send_collection_name(collection_name)
    st.subheader("Setup Database")
    st.write("Upload multiple PDF files to be used in the database.")

    # Initialize the session state flag if it doesn't exist
    if "files_uploaded" not in st.session_state:
        st.session_state.files_uploaded = False

    # File uploader
    uploaded_files = st.file_uploader(
        "Choose PDF files (you can upload multiple files)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    # Update the flag based on file upload status
    if uploaded_files:
        st.session_state.files_uploaded = True
    else:
        st.session_state.files_uploaded = False

    if st.session_state.files_uploaded:
        st.write(f"{len(uploaded_files)} file(s) selected for upload.")

        # Create a zip file from the uploaded PDFs
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file in uploaded_files:
                zip_file.writestr(file.name, file.getvalue())
        
        zip_buffer.seek(0)  # Rewind to the beginning of the buffer

        if st.button("Upload and Parse All Files"):
            with st.spinner("Uploading and parsing files..."):
                # Send the zip file to the Django API
                response = api_client.upload_pdfs(zip_buffer)

            if response["success"]:
                st.success("Files parsed successfully!")
            else:
                st.error(response["error"])

    else:
        st.session_state.files_parsed = False
        st.write("No files uploaded. Please upload at least one PDF file.")
