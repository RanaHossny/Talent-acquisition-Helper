# System Overview

## Lightning AI Server
- **Online App**: Handles user queries and serves as the core processing unit for interactions.
- **Offline App**: Focuses on:
  - OCR (Optical Character Recognition) for PDFs.
  - Setting up a vector database for document retrieval.
  - Interacting with the Milvus database.
  - Managing cloud storage for storing and retrieving documents in the vector database.

## Frontend Server
A Streamlit app designed to provide a user-friendly GUI. It includes:
- **Login Page**: Secure user authentication.
- **Sign-In Page**: User registration.
- **Data Setup Page**: For uploading and configuring documents.
- **Chatbot Page**: Allows users to interact with the chatbot.

The frontend communicates with:
- Lightning AI Server for query handling.
- Django Server for backend operations.

## Backend Server
Key Applications:
- **Document Retriever App**: 
  - Handles PDF uploads.
  - Prepares documents for storage and retrieval.
- **Chatbot App**: 
  - Stores and retrieves chat history.
- **Accounts App**: 
  - Manages user authentication and account operations.

## System Architecture Diagram
