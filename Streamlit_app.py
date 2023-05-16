
import snowflake.connector
import streamlit as st



# Load Snowflake secrets
snowflake_secrets = st.secrets["snowflake"]



# Create Snowflake connection configuration
config = {
 "account": snowflake_secrets["account"],
 "user": snowflake_secrets["user"],
 "password": snowflake_secrets["password"],
 "role": snowflake_secrets["role"],
 "database": snowflake_secrets["database"],
 "schema": snowflake_secrets["schema"],
 "warehouse": snowflake_secrets["warehouse"]
}


# Print out Snowflake configuration
# print(config)

# # Connect to Snowflake
# conn = snowflake.connector.connect(**config)


from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.vectorstores import FAISS
# import streamlit as st

loader = UnstructuredMarkdownLoader('schema.md')
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
texts = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings(openai_api_key = st.secrets["openai_api_key"])
docsearch = FAISS.from_documents(texts, embeddings)

docsearch.save_local("faiss_index")

# with open("vectors.pkl", "wb") as f:
#     pickle.dump(docsearch, f)





