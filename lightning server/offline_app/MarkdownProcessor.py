from langchain_text_splitters import RecursiveCharacterTextSplitter
from  .utils import UtilsClass
from .text_embedding import TextEmbedding
from langchain_experimental.text_splitter import SemanticChunker

class MarkdownProcessor:
    def __init__(self, extracted_folder_path='/content/drive/MyDrive/output'):
        self.extracted_folder_path = extracted_folder_path
        TextEmbedding_model = TextEmbedding(device="cuda")
        self.text_splitter = SemanticChunker(TextEmbedding_model,breakpoint_threshold_type="gradient")
        self.my_utils=UtilsClass()


    def process_files(self):
        self.all_splits = self.my_utils.process_markdown_files(extracted_folder_path=self.extracted_folder_path,text_splitter=self.text_splitter)

    def display_splits(self, num_splits=6):
        print(f"Total splits processed: {len(self.all_splits)}")
        for split in self.all_splits[:num_splits]:
            print(f"Metadata: {split.metadata}")
            print(f"Content: {split.page_content[:1000]}")

