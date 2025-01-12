from langchain_core.prompts import PromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface.llms import HuggingFacePipeline
import torch

class ModelManager:
    def __init__(self, model_id: str, torch_dtype=torch.bfloat16, device_map="auto"):
        """
        Initialize the ModelManager with a specified model ID.

        Args:
            model_id (str): Hugging Face model ID.
            torch_dtype: Torch data type for the model (default: torch.bfloat16).
            device_map: Device map for model loading (default: "auto").
        """
        self.model_id = model_id
        self.torch_dtype = torch_dtype
        self.device_map = device_map
        self.tokenizer = None
        self.model = None
        self.pipeline = None

    def load_model(self):
        """
        Load the tokenizer and model for the specified model ID.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, 
            torch_dtype=self.torch_dtype, 
            device_map=self.device_map
        )

    def get_pipeline(self, max_new_tokens=2024):
        """
        Create a Hugging Face pipeline for text generation using the loaded model and tokenizer.

        Args:
            max_new_tokens (int): Maximum number of tokens for generation (default: 2024).
        
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model and tokenizer must be loaded before creating a pipeline.")
        
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            torch_dtype=self.torch_dtype,
            device_map=self.device_map,
            max_new_tokens=max_new_tokens
        )
        self.generator = pipe

