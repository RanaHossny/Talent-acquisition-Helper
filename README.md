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
![System Architecture Diagram](https://github.com/RanaHossny/rag_chat/blob/main/Screenshot%202025-01-15%20201435.png)

# Offline App Process

1. Receive the PDFs from the backend server.
2. Use Marker OCR to extract the contents from the PDFs.
3. Perform semantic chunking using MiniLM-L6-v2 text embedding.
4. Store the chunks in Milvus Cloud and use stella_en_400M_v5 for vector representation.
![Offline App Process](https://github.com/RanaHossny/rag_chat/blob/main/Screenshot%202025-01-15%20202419.png)


# Online App Process

1. Implement RAG (Retrieval-Augmented Generation) with memory integration.
2. The user asks a query.
3. Chain the query with memory and previous retrieved documents.
4. Insert the chained query into LLM (Llama 3.2 Instruct) to generate a standalone question.
5. Use the standalone question to retrieve documents from the Milvus database.
6. Update the previous retrieved documents.
7. Use the updated retrieved documents, query, and memory to generate the response.
![Online App Process](https://github.com/RanaHossny/rag_chat/blob/main/Screenshot%202025-01-15%20202206.png)

# The sequence Diagrams:
![User login and data processing](https://github.com/RanaHossny/rag_chat/blob/main/image.png)
![AI query](https://github.com/RanaHossny/rag_chat/blob/main/Screenshot%202025-01-15%20132316.png)
![chat history](https://github.com/RanaHossny/rag_chat/blob/main/Screenshot%202025-01-15%20204112.png)(not total implemented)
