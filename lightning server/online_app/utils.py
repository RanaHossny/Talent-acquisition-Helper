import os
import uuid
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from typing import List


class UtilsClass:
    
    def format_docs(self, docs) -> str:
        """
        Formats a list of documents by including metadata information (candidate's name)
        and the document content. If the candidate's name is not available, it defaults
        to 'Unknown Candidate'.

        Args:
            docs (list): A list of document objects, where each document has metadata
                         (a dictionary) and page_content (the document's text).

        Returns:
            str: A single string where each document is formatted with the candidate's
                 name followed by the document content, separated by double newlines.
        """
        formatted_docs = []
        for doc in docs:
            candidate_name = doc.metadata.get('name', 'Unknown Candidate')
            page_content = doc.page_content if hasattr(doc, 'page_content') else ''
            formatted_doc = f"Candidate Name: {candidate_name}\n{page_content}"
            formatted_docs.append(formatted_doc)
        return "\n\n".join(formatted_docs)

