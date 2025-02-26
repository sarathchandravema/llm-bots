from dotenv import load_dotenv ## loads API keys
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from collections import OrderedDict

load_dotenv()

os.environ["HUGGINGFACEHUB_API_KEY"] = os.getenv("HUGGINGFACEHUB_API_KEY")

loader = PyPDFLoader("grades_trim.pdf")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
texts = text_splitter.split_documents(docs)

## Initialize embedding model
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

try:
    embeds = embed_model.embed_documents([doc.page_content for doc in texts])
    print("Vectors done!!!")
except Exception as e:
    print(f"Error in embed process: {e}")

## Vector store
vector_store = Chroma(embedding_function=embed_model, persist_directory="data")

vector_store.add_documents(documents=texts)

try:
    test_query = "what is the name of student with id, S1004?"
    results = vector_store.search(query=test_query, search_type='similarity')

    unique_results = OrderedDict()
    for doc in results:
        if doc.page_content not in unique_results:
            unique_results[doc.page_content] = doc
    
    final_results = list(unique_results.values())[:3]
    print(f"Unique query results:\n{final_results}")
except Exception as e:
    print(f"Error during test query: {e}")