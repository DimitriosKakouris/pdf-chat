# 📚 LangChain Document Q&A System

> An intelligent document question-answering system powered by LangChain

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/langchain-latest-green.svg)](https://python.langchain.com/)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)

## 🌟 Overview

Transform your documents into an interactive knowledge base! This application allows you to upload PDF or text documents and ask intelligent questions about their content using state-of-the-art AI models.

## 🏗️ Architecture

```mermaid
graph TD
    A[Document Upload] --> B[Document Processor]
    B --> C[Text Splitting]
    C --> D[Bedrock Embeddings]
    D --> E[ChromaDB Vector Store]
    E --> F[Retrieval QA System]
    F --> G[Claude Sonnet Response]
    G --> H[Streamlit UI]
```

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DimitriosKakouris/pdf-chat.git
   cd langchain-qa
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser** 
   Navigate to `http://localhost:8501`

## 🔧 Configuration

### Model Configuration

The system uses:
- **LLM**: `us.anthropic.claude-sonnet-4-20250514-v1:0`
- **Embeddings**: `amazon.titan-embed-text-v1`
- **Vector Store**: ChromaDB with persistent storage

## 📖 Usage

### 1. Upload Document 📄
- Click "Upload a document" 
- Select your PDF or TXT file
- Wait for processing to complete

### 2. Ask Questions 💭
- Type your question in the text input
- Get comprehensive answers (250+ words)
- View source context and references

## 🏢 Project Structure

```
langchain-qa/
├── main.py                 # Streamlit application entry point
├── qa_system.py           # Q&A system implementation
├── document_loader.py     # Document processing utilities
├── requirements.txt       # Python dependencies
├── refdocs/              # Uploaded documents storage
├── chroma_db/            # Vector database storage
```

## 🛠️ Technical Details

### Document Processing Pipeline

1. **Loading**: PyPDFLoader for PDFs, TextLoader for text files
2. **Chunking**: RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
3. **Embedding**: AWS Bedrock Titan embeddings
4. **Storage**: ChromaDB vector database with persistence

### Q&A System

- **Retrieval**: Similarity search with top-k=3 results
- **Generation**: Claude Sonnet with custom prompt template
- **Output**: Detailed 250+ word responses with context

## 🎯 Customization

### Modify Chunk Size
```python
# In document_loader.py
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # Increase for larger chunks
    chunk_overlap=300
)
```

### Adjust Model Parameters
```python
# In qa_system.py
self.llm = ChatBedrock(
    model="us.anthropic.claude-sonnet-4-20250514-v1:0",
    model_kwargs={
        "max_tokens": 2000,    # Increase for longer responses
        "temperature": 0.3,    # Adjust creativity (0-1)
        "top_p": 0.9
    }
)
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments

- **LangChain** - For the amazing framework
- **AWS Bedrock** - For powerful AI models  
- **Streamlit** - For the UI framework
- **ChromaDB** - For efficient vector storage
