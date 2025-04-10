from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

EMBEDDING_TABLE = "resume_embeddings"
RESUME_DOC_TABLE = "resume_docs"
EMBEDDING_MODEL_NAME = "thenlper/gte-base"
EMBEDDING_LENGTH = 768
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')


class Shared():
    embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )

    # singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Shared, cls).__new__(cls)
        return cls.instance

    def chunk(self, text: str):
        docs = self.splitter.create_documents(texts=[text])
        return [doc.page_content for doc in docs]
    
    def embed_documents(self, chunks: List[str]):
        return self.embedder.embed_documents(chunks)
    
    def embed_query(self, prompt: str):
        return self.embedder.embed_query(prompt)

