import re
import streamlit as st
from document_loader import DocumentProcessor
from qa_system import QASystem
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("Document Q&A System")

    # File upload
    uploaded_file = st.file_uploader("Upload a document", type=['pdf', 'txt'])

    if uploaded_file is not None:
        # Save uploaded file
        with open(f"./refdocs/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getvalue())

        # Process document
        processor = DocumentProcessor()
        documents = processor.load_documents(f"./refdocs/{uploaded_file.name}")
        vectorstore = processor.process_documents(documents)

        # Create QA system
        qa_system = QASystem(vectorstore)

        # Question input
        question = st.text_input("Ask a question about the document:")

        if question:
            with st.spinner("Searching for answer..."):
                result = qa_system.ask_question(question)
                st.write("**Your Question:**")
                st.write(result['query'])
                # print(result)
                st.write("**Answer:**")
                st.write(result['result'])

                st.write("**Sources:**")
                st.write(result["source_documents"])
                # for i, doc in enumerate(result["sources"]):
                #     st.write(f"Source {i+1}: {doc.page_content[:200]}...")

if __name__ == "__main__":
    main()
