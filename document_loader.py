from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import Chroma

import os

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        # Using Bedrock embeddings
        self.embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1"
        )

    def load_documents(self, file_path):
        """Load documents based on file extension"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file type")

        return loader.load()

    def process_documents(self, documents):
        """Split documents and create vector store"""
        texts = self.text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
        return vectorstore
