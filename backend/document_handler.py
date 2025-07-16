import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings

# Embedding model
embedding_model = OllamaEmbeddings(model="llama3")

# Document splitter
def split_document(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)

# Save or update vector store
def save_to_vectorstore(chunks):
    vector_dir = "vector_store"
    index_name = "index"

    if not os.path.exists(vector_dir):
        os.mkdir(vector_dir)

    index_path = os.path.join(vector_dir, f"{index_name}.faiss")

    if os.path.exists(index_path):
        # ✅ Append to existing FAISS store
        db = FAISS.load_local(
            vector_dir,
            embeddings=embedding_model,
            index_name=index_name,
            allow_dangerous_deserialization=True
        )
        db.add_documents(chunks)
    else:
        # 🆕 Create new FAISS index
        db = FAISS.from_documents(chunks, embedding_model)

    db.save_local(vector_dir, index_name=index_name)

# Main function to process uploaded file
def process_uploaded_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyMuPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    documents = loader.load()
    chunks = split_document(documents)
    save_to_vectorstore(chunks)
