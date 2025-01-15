from flask import Flask, request, jsonify
import os
import zipfile
import io
from offline_app.parser import parse_pdf
from offline_app.embedding import StellaEmbedding
from offline_app.MarkdownProcessor import MarkdownProcessor
from offline_app.Milvus_Manager import MilvusManager
from offline_app.utils import UtilsClass
from online_app.model import ModelLoader
from online_app.QueryMake import QueryMaker
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

UPLOAD_FOLDER = "Input"
OUTPUT_FOLDER="Output"
base_url = "https://in03-9d99fc6222710f5.serverless.gcp-us-west1.cloud.zilliz.com"
token = "e132ff5705634714bf719ecd8d0a68ebe7e2fd33c072c98555e9320925becb7cdc0aa14b2dc9b549f7df3da716b3c268651021b2"
memory = ConversationBufferWindowMemory(k=2)
# Initialize model loader
checkpoint = "meta-llama/Llama-3.2-3B-Instruct"
model_loader = ModelLoader(model_id=checkpoint)
model_loader.load_model()
model_loader.get_pipeline()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

stella_embedding_model = StellaEmbedding(device="cuda")
milvus_manager = MilvusManager(base_url, token)
util_manager=UtilsClass()
vectorstore=None
query_maker=QueryMaker(memory, vectorstore, model_loader)


@app.route('/')
def hello():
    return "Hello"
    
collection_name=None
@app.route('/send_collection_name/', methods=['POST'])
def receive_collection_name():
    global collection_name
    global vectorstore
    global query_maker
    collection_name=None

    # Get the collection_name from the request
    collection_name = request.form.get('name')
    print(collection_name)

    # Check if the collection_name was provided
    if not collection_name:
        return jsonify({"success": False, "error": "No collection name provided"}), 400
    if(milvus_manager.check_collection_exists(collection_name)):
        vectorstore=milvus_manager.get_collection(stella_embedding_model,collection_name)
        query_maker.retriever=vectorstore


    # Respond back with the collection_name
    return jsonify({
        "success": True,
        "message": f"Collection name '{collection_name}' received successfully"
    }), 200

@app.route('/upload_pdfs', methods=['POST'])
def upload_pdfs():
    global collection_name
    global milvus_manager
    global vectorstore
    global query_maker

    
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400
    
    # Check if the file is a ZIP
    if file and file.filename.endswith('.zip'):
        zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(zip_path)
        
        # Extract ZIP file
        try:
            print(collection_name)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(UPLOAD_FOLDER)
                
            parse_pdf(UPLOAD_FOLDER, OUTPUT_FOLDER, workers=4, max_files=30)
            processor = MarkdownProcessor(extracted_folder_path=OUTPUT_FOLDER)
            processor.process_files()
            processor.display_splits()
            vectorstore = milvus_manager.check_and_create_collection(collection_name, processor.all_splits, stella_embedding_model)
            query_maker.retriever=vectorstore
            # Clean up by deleting all files and folders inside UPLOAD_FOLDER and OUTPUT_FOLDER
            util_manager.clean_up_folder(UPLOAD_FOLDER)
            util_manager.clean_up_folder(OUTPUT_FOLDER)
            
            return jsonify({"success": True, "message": "Files extracted successfully"}), 200

        except zipfile.BadZipFile:
            return jsonify({"success": False, "error": "Invalid ZIP file"}), 400
        
    else:
        return jsonify({"success": False, "error": "File is not a valid ZIP"}), 400



@app.route('/query', methods=['POST'])
def query_endpoint():
    # Get JSON data from the request
    global query_maker
    data = request.get_json()
    user_query = data.get("user_input")

    if not user_query:
        return jsonify({"error": "'user_input' is required"}), 400

    # Call your query maker with the dynamic collection name and user query
    try:
        response = query_maker.ask_query(user_query)

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"An error occurred while processing the query: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True, port=8001,use_reloader=False)



