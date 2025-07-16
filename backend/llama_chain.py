from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Load the LLaMA model via Ollama
llm = Ollama(model="llama3")  # Make sure 'ollama run llama3' works on your machine

# Load embeddings using Ollama
embedding_model = OllamaEmbeddings(model="llama3")

# Load vector DB from local FAISS index
def load_vectorstore():
    if os.path.exists("vector_store/index.faiss"):
        return FAISS.load_local(
            "vector_store",
            embeddings=embedding_model,
            index_name="index",
            allow_dangerous_deserialization=True  # ✅ Fix error with FAISS loading
        )
    else:
        return None

# Create a QA chain using LangChain’s RAG pattern
def get_qa_chain():
    vectorstore = load_vectorstore()
    if vectorstore:
        retriever = vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        return qa_chain
    else:
        return None

# Handle both document-based and general questions
def answer_question(question: str):
    qa_chain = get_qa_chain()

    if qa_chain:
        try:
            result = qa_chain.run(question)

            # 🔁 Fallback to LLM if the answer seems generic
            if not result or "I don't know" in result or "no information" in result.lower():
                return llm.invoke(question)

            return result
        except Exception as e:
            print("RAG failed:", e)

    # 🔁 If no vectorstore or any other error, use general LLM
    return llm.invoke(question)
