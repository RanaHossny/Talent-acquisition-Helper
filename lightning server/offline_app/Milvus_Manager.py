import requests
from langchain.vectorstores import Milvus

class MilvusManager:
    def __init__(self, base_url, token):
        """Initialize the MilvusManager with base URL and token."""
        self.base_url = base_url
        self.token = token

    def check_collection_exists(self, collection_name):
        """Check if the collection exists in the Milvus database."""
        url = f"{self.base_url}/v2/vectordb/collections/has"
        data = {
            "collectionName": collection_name
        }

        try:
            response = requests.post(url, json=data, headers={"Authorization": f"Bearer {self.token}"})
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get("data", {}).get("has", False):
                    print(f"Collection '{collection_name}' exists.")
                    return True
                else:
                    print(f"Collection '{collection_name}' does not exist.")
                    return False
            else:
                print(f"Error: Received status code {response.status_code}")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


    def drop_collection(self, collection_name):
        """Drop the specified collection from the Milvus database."""
        url = f"{self.base_url}/v2/vectordb/collections/drop"
        data = {
            "collectionName": collection_name
        }
    
        try:
            response = requests.post(url, json=data, headers={"Authorization": f"Bearer {self.token}"})
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get("code") == 0:
                    print(f"Collection '{collection_name}' has been dropped successfully.")
                    return True
                else:
                    print(f"Failed to drop collection '{collection_name}'.")
                    return False
            else:
                print(f"Error: Received status code {response.status_code}")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    

    def create_collection(self, collection_name, all_splits, stella_embedding_model):
        """Create a new collection in the Milvus database."""
        try:
            vectorstore = Milvus.from_documents(
                all_splits,
                stella_embedding_model,
                collection_name=collection_name,
                connection_args={
                    "uri": self.base_url,
                    "token": self.token
                }
            )
            print(f"Collection '{collection_name}' created successfully.")
            return vectorstore
        except Exception as e:
            print(f"An error occurred while creating the collection: {e}")
            return None

    def check_and_create_collection(self, collection_name, all_splits, stella_embedding_model):
        """Check if the collection exists, drop it if it does, and create a new one."""
        if self.check_collection_exists(collection_name):
            self.drop_collection(collection_name)
        return self.create_collection(collection_name, all_splits, stella_embedding_model)

    def get_collection(self,embedding_function ,collection_name):
        """Get the specified collection from the Milvus database."""
        try:
            vectorstore = Milvus(
                embedding_function=embedding_function,
                collection_name=collection_name,
                connection_args={"uri": self.base_url, "token": self.token},
            )
            print(f"Collection '{collection_name}' retrieved successfully.")
            return vectorstore
        except Exception as e:
            print(f"An error occurred while retrieving the collection '{collection_name}': {e}")
            return None
