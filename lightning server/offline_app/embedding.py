from sentence_transformers import SentenceTransformer

class StellaEmbedding:
    """
    This class is responsible for embedding text documents and queries using a pre-trained model.
    It uses the Sentence-BERT architecture to generate high-quality embeddings for text input.

    Attributes:
        model (SentenceTransformer): The Sentence-BERT model used to generate embeddings.
        query_prompt_name (str): The name of the prompt used when embedding queries.
    """
    def __init__(self, model_name="dunzhang/stella_en_400M_v5", device="cpu"):
        config_kwargs = {}
        if device == "cpu":
            config_kwargs = {
                "use_memory_efficient_attention": False,
                "unpad_inputs": False
            }

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