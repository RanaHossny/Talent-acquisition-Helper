import os
import uuid
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from typing import List


class UtilsClass:
    
    def extract_name_from_filename(self, filename: str) -> str:
        """
        Extract the name from the filename.
        """
        name_parts = filename.split('_')
        if len(name_parts) > 1:
            return ' '.join(name_parts).replace('.md', '').strip()
        return filename.replace('.md', '').strip()

    @staticmethod
    def generate_candidate_id() -> str:
        """
        Generate a unique candidate ID.
        """
        return str(uuid.uuid4())[:8]

    def process_markdown_files(self, extracted_folder_path: str, text_splitter) -> List:
        """
        Process markdown files in a folder and return split documents with metadata.

        Parameters:
            extracted_folder_path (str): Path to the folder containing markdown files.
            text_splitter: An instance of a text splitting class with a split_documents method.

        Returns:
            List: A list of split documents with metadata.
        """
        all_splits = []
        # Process each markdown file
        for root, dirs, files in os.walk(extracted_folder_path):
            for file in files:
                if file.endswith('.md'):  # Only process markdown files
                    file_path = os.path.join(root, file)

                    # Load markdown file using UnstructuredMarkdownLoader
                    loader = UnstructuredMarkdownLoader(file_path)
                    data = loader.load()

                    if data:  # Ensure there is at least one document
                        # Extract metadata
                        extracted_name = self.extract_name_from_filename(file)
                        candidate_id = self.generate_candidate_id()

                        # Attach metadata to the first document in data
                        data[0].metadata["name"] = extracted_name
                        data[0].metadata["candidate_id"] = candidate_id

                        # Use the text_splitter to split documents
                        splits = text_splitter.split_documents(data)
                        all_splits.extend(splits)

        return all_splits

    
    def clean_up_folder(self,folder_path):
        """Deletes all files and subdirectories inside the specified folder."""
        try:
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))  # Delete file
                for name in dirs:
                    os.rmdir(os.path.join(root, name))  # Delete empty directory
            print(f"Cleaned up folder: {folder_path}")
        except Exception as e:
            print(f"Error cleaning up folder {folder_path}: {e}")
