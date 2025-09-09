import re
from langchain.chains import RetrievalQA
from langchain_aws import BedrockLLM
from langchain_aws import BedrockEmbeddings
from langchain_aws.chat_models.bedrock import ChatBedrock
from langchain_core.prompts import PromptTemplate
import boto3
from langchain.chains import RetrievalQA
from streamlit.elements.widgets.button_group import SelectionMode

bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)

prompt_template = """
Human: Use the following pieces of context to provide a
concise answer to the question at the end but use at least 250 words
to summarize with detailed explanations. If you don't know the answer,
just say that you don't know.
<context>
{context}
</context>

Question: {question}

Assistant:"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


class QASystem:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.llm = ChatBedrock(
            model="us.anthropic.claude-sonnet-4-20250514-v1:0",
            model_kwargs={
                "max_tokens": 512,
                "temperature": 0.1,
                "top_p": 0.9
            },
            region="us-east-1",
            streaming=False
        )


    def ask_question(self, query):
        qa_sys = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        return qa_sys({"query": query})
