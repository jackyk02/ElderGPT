import streamlit as st
from streamlit_chat import message
from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Pinecone
import pinecone

from langchain.llms import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE


# Pinecone config
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT_REGION"),
)

# OpenAI config
OPENAI_API= os.getenv('OPENAI_API_KEY')
template = """You are a chatbot having a conversation with a human.
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
     input_variables= ["human_input"], template=template
)

MODEL= 'gpt-3.5-turbo'
embeddings = OpenAIEmbeddings()
docsearch = Pinecone.from_existing_index(
    embedding=embeddings,
    index_name="langchain-doc-helper",
)
llm = ChatOpenAI(
     temperature=0,
     model_name=MODEL
)



if __name__ == "__main__":
    docs = docsearch.similarity_search("who created langchain")
    print("printing response:")
    print(docs[0].page_content)