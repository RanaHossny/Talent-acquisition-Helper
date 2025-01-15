from langchain_experimental.text_splitter import SemanticChunker
from sentence_transformers import SentenceTransformer


class TextEmbedding:
    """
    This class is responsible for embedding text documents and queries using a pre-trained Sentence-BERT model.
    It provides methods to generate embeddings for individual text queries, documents, and chunks of text.
    It will be used in SemanticChunker as the other StellaEmbedding is quite heavy competion.

    Attributes:
        model (SentenceTransformer): The Sentence-BERT model used for generating embeddings.
        query_prompt_name (str): The name of the prompt used when embedding queries.
    """
    def __init__(self, model_name="all-MiniLM-L6-v2", device="cpu"):
        config_kwargs = {}

        self.model = SentenceTransformer(
            model_name,
            trust_remote_code=True,
            device=device,
            config_kwargs=config_kwargs
        ).to(device)

        self.query_prompt_name = "s2p_query"

    def embed_documents(self, texts):
        """Embed multiple documents."""
        return self.model.encode(texts, show_progress_bar=False)

    def embed_query(self, query):
        """Embed a single query."""
        return self.model.encode([query], prompt_name=self.query_prompt_name, show_progress_bar=False)[0]

    def embed_text(self, text):
        """Generate embedding for a single text."""
        return self.model.encode(text, convert_to_tensor=True)
