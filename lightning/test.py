import os
import shutil
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from langchain.schema import Document
from offline_app.embedding import StellaEmbedding
from offline_app.vectordb import RetrieverManager
from offline_app.parser import parse_pdf
from online_app.model import ModelManager
from online_app.QueryMake import QueryMaker
from langchain.memory import ConversationBufferWindowMemory



load_dotenv()

app = Flask(__name__)

# Set the base directory for temporary file storage
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


stella_embedding_model = StellaEmbedding()

retriever_manager = RetrieverManager(
    uri=os.getenv("MILVUS-URI"), 
    token=os.getenv("MILVUS-TOKEN"), 
    embedding_model=stella_embedding_model
)

retriever_manager.get_all_retrievers()

memory = ConversationBufferWindowMemory(k=2)
# Initialize model loader
checkpoint = "meta-llama/Llama-3.2-3B-Instruct"
model_loader = ModelManager(model_id=checkpoint)
model_loader.load_model()
model_loader.get_pipeline()
# Create an instance of QueryMaker
query_maker = QueryMaker(memory, retriever_manager, model_loader)

@app.route('/parse-pdfs', methods=['POST'])
def parse_pdfs():
    """
    Flask endpoint to handle batch PDF uploads, parse them, and return the output folder as a ZIP file.
    """
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files uploaded."}), 400

        files = request.files.getlist('files')  # Get all uploaded files

        # Define temporary input and output directories
        input_folder = os.path.join(MEDIA_ROOT, "input_docs")
        output_folder = os.path.join(MEDIA_ROOT, "output_docs")
        os.makedirs(input_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

        # Save uploaded files to the input folder
        for file in files:
            if not file.filename or not file.filename.endswith('.pdf'):
                return jsonify({"error": f"File '{file.filename}' is not a PDF. Skipping."}), 400

            file_path = os.path.join(input_folder, file.filename)
            file.save(file_path)

        # Call the parse_pdf function
        parse_pdf(input_folder, output_folder)

        # Create a ZIP file of the output folder
        output_zip_path = os.path.join(MEDIA_ROOT, "output_docs.zip")
        shutil.make_archive(output_zip_path.replace(".zip", ""), 'zip', output_folder)

        # Return the ZIP file as a response
        return send_file(output_zip_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up temporary folders
        for folder in [input_folder, output_folder]:
            if os.path.exists(folder):
                shutil.rmtree(folder)

        # Clean up the ZIP file
        if 'output_zip_path' in locals() and os.path.exists(output_zip_path):
            os.remove(output_zip_path)



@app.route('/add-collection', methods=['POST'])
def add_collection():
    try:
        data = request.get_json()

        collection_name = data.get('collection_name')
        documents_data = data.get('documents', [])

        if not collection_name or not documents_data:
            return jsonify({"error": "collection_name and documents are required"}), 400

        # Convert documents data to Document objects
        documents = [Document(**doc) for doc in documents_data]

        retriever_manager.add_collection(collection_name, documents)

        return jsonify({"message": f"Collection '{collection_name}' added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/query', methods=['POST'])
def query_endpoint():
    # Get JSON data from the request
    data = request.get_json()
    collection_name = data.get('collection_name')
    user_query = data.get("prompt")

    if not user_query:
        return jsonify({"error": " 'prompt' are required"}), 400
    
    # Call your query maker with the dynamic collection name and user query
    try:
        response = query_maker.ask_query(user_query, collection_name)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
    