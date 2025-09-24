import re
import os
import streamlit as st
from document_loader import DocumentProcessor
from qa_system import QASystem
from dotenv import load_dotenv
import glob

load_dotenv()

def clear_document_pool():
    """Clear all documents from the pool and reset session state"""
    # Remove files from refdocs directory
    for file in glob.glob("./refdocs/*.pdf"):
        os.remove(file)

    for file in glob.glob("./refdocs/*.txt"):
        os.remove(file)

    # Clear session state
    if 'vectorstore' in st.session_state:
        del st.session_state.vectorstore
    if 'qa_system' in st.session_state:
        del st.session_state.qa_system
    if 'processed_files' in st.session_state:
        del st.session_state.processed_files

    # Increment uploader key to reset file uploader
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0
    st.session_state.uploader_key += 1

    st.success("Document pool cleared successfully!")


def process_all_documents():

    """Process all documents in refdocs directory into a single vector store"""
    all_documents=[]

    document_files = glob.glob("./refdocs/*.txt") + glob.glob("./refdocs/*.pdf")

    if not document_files:
        return None, []

    processor = DocumentProcessor()
    all_documents = []
    processed_files = []
    for file_path in document_files:
        try:
            st.warning(f"Processing {file_path}...")
            documents = processor.load_documents(file_path)
            all_documents.extend(documents)
            processed_files.append(os.path.basename(file_path))
        except Exception as e:
            st.error(f"Error processing {file_path}: {str(e)}")

    if all_documents:
        # Create single vector store from all documents
        vectorstore = processor.process_documents(all_documents)
        return vectorstore, processed_files

    return None, []


def main():
    st.title("pdf-chat")



    # Initialize session state
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0

    # File upload
    uploaded_file = st.file_uploader("Add document to pool", type=['pdf', 'txt'], key=f"uploader_{st.session_state.uploader_key}")

    # Clear button
    if st.button("Clear document pool"):
        clear_document_pool()
        st.rerun()  # Force a clean rerun after clearing


    if uploaded_file is not None:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"


        if file_id not in st.session_state.processed_files:
            # Save uploaded file
            file_path = f"./refdocs/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
                # # Store in session state
                # st.session_state.vectorstore = vectorstore
                # st.session_state.qa_system = QASystem(vectorstore)
                # st.session_state.processed_files.add(file_id)
        else:
            st.warning(f"Document '{uploaded_file.name}' already uploaded.")


    if st.button("Process Documents"):
        vectorstore, processed_files = process_all_documents()
        if vectorstore:
            st.session_state.vectorstore = vectorstore
            st.session_state.qa_system = QASystem(vectorstore)
            st.session_state.processed_files = processed_files

        st.success("Documents processed successfully!")

    # Show Q&A interface only if we have a processed document
    if 'qa_system' in st.session_state:
        st.write("---")
        st.subheader("Ask Questions")

        # Question input
        question = st.text_input("Ask a question about the document:")

        if question:
            with st.spinner("Searching for answer..."):


                result = st.session_state.qa_system.ask_question(question)

                st.write("**Your Question:**")
                st.write(result['query'])

                st.write("**Answer:**")
                st.write(result['result'])

                st.write("**Sources:**")

                for i, doc in enumerate(result["source_documents"]):
                    with st.expander(f"Source {i+1}"):
                        st.write(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)

    elif uploaded_file is None:
        st.info("Please upload a document to get started.")

if __name__ == "__main__":
    main()
