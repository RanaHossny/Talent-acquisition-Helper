class QueryMaker:
    def __init__(self, memory, retriever_manager, model_loader, end_token="</end>"):
        """
        Initialize the QueryMaker class.

        :param memory: Memory object for managing chat history.
        :param retriever_manager: Instance of the RetrieverManager for querying the vector store.
        :param model_loader: Instance of the ModelLoader for generating text responses.
        :param end_token: The token that marks the end of the response.
        """
        self.memory = memory
        self.retriever_manager = retriever_manager
        self.model_loader = model_loader
        self.end_token = end_token

    def ask_query(self, query_user, collection_name):
        """
        Process the query and generate a response based on the specified collection.

        :param query_user: The user's query string.
        :param collection_name: The name of the collection to query from the vector store.
        :return: The generated response.
        """
        # Retrieve relevant context snippets from the specified collection
        retriever = self.retriever_manager.get_retriever(collection_name)
        retrieved_texts = retriever.get_relevant_documents(query_user) if retriever else []

        # Prepare the messages for the text generation pipeline
        messages = [
            {
                "role": "system",
                "content": (
                    "This bot helps Talent Acquisition professionals find the best candidates for the required job. "
                    "Provide answer only to the following query based on the context provided below. "
                    "Do not generate or answer any other questions. "
                    "Do not make up or infer any information that is not directly stated in the context. "
                    f"This is the previous question and answer history if needed: {self.memory.load_memory_variables({})}. "
                    "Provide a concise answer. "
                    f"Context: {retrieved_texts} "
                    f"{self.end_token}"
                )
            },
            {"role": "user", "content": query_user}
        ]

        # Print the prepared messages for debugging purposes
        print("Prepared Messages:\n", messages)

        # Generate a response using the text generation pipeline
        response = self.model_loader.generator(messages, max_new_tokens=128)[-1]["generated_text"][-1]["content"]

        # Save the query and response in memory
        self.memory.save_context({"input": query_user}, {"output": response})

        # Output the query, context, and response
        print(f"Query: \n\t{query_user}")
        print(f"Context: \n\t{retrieved_texts}")
        print(f"Answer: \n\t{response}")

        return response
