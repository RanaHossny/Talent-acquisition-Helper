from typing import Optional
from langchain.vectorstores import Milvus
from .utils import UtilsClass


class QueryMaker:
    def __init__(self, memory,  retriever: Optional[Milvus], model_loader, end_token="</end>"):
        """
        Initialize the QueryMaker class.

        :param memory: Memory object for managing chat history.
        :param retriever_manager: Instance of the RetrieverManager for querying the vector store.
        :param model_loader: Instance of the ModelLoader for generating text responses.
        :param end_token: The token that marks the end of the response.
        """

        self.memory = memory
        self.retriever = retriever
        self.model_loader = model_loader
        self.end_token = end_token
        self.util_manager=UtilsClass()

    def ask_query(self, query_user):
        """
        Process the query and generate a response based on the specified collection.

        :param query_user: The user's query string.
        :param collection_name: The name of the collection to query from the vector store.
        :return: The generated response.
        """
        memory_data=self.memory.load_memory_variables({})

        standalone_system_message = [
            {
                "role": "system",
                "content": (
                    "Given a chat history and a follow-up question, rephrase the follow-up question to be a standalone question. "
                    "Do NOT answer the question, just reformulate it if needed, otherwise return it as is. "
                    "Only return the final standalone question. "
                    f"This is the history: {memory_data} "
                    f"{self.end_token}"
                )
            },
            {"role": "user", "content": query_user}
        ]


        question_response = self.model_loader.generator(standalone_system_message, max_new_tokens=256)[-1]["generated_text"][-1]["content"]
        print(f"question:{question_response}")
        if self.retriever:
            retrieved_texts=self.retriever.as_retriever().invoke(question_response,k=2)
        else:
            retrieved_texts = []

        retrieved_texts=self.util_manager.format_docs(retrieved_texts)
        # Prepare the messages for the text generation pipeline
        messages = [
            {
                "role": "system",
                "content": (
                    "This bot helps Talent Acquisition professionals find the best candidates for the required job. "
                    "Provide answer only to the following query"
                    "Do not generate or answer any other questions. "
                    "Do not ask the user any question. "
                    f"Context: {retrieved_texts} donot use Context if not needed for user query" 
                    "Do not make up or infer any information that is not directly stated in the context. "
                    f"This is the previous question and answer history if needed: {self.memory.load_memory_variables({})}. "
                    "Provide a concise answer. "
                    f"{self.end_token}"
                )
            },
            {"role": "user", "content": query_user}
        ]


        # Generate a response using the text generation pipeline

        try:
            response = self.model_loader.generator(messages, max_new_tokens=512)[-1]["generated_text"][-1]["content"]
        except Exception as e:
            print(f"An error occurred: {e}")
            response = None
        # Save the query and response in memory
        self.memory.save_context({"input": query_user}, {"output": response})

        # # Output the query, context, and response
        # print(f"Query: \n\t{query_user}")
        print(f"Context: \n\t{retrieved_texts}")
        # print(f"Answer: \n\t{response}")

        return response

