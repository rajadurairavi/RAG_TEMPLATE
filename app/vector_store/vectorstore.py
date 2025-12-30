from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.vector_store.docs_load import load_documents

# Single source of truth for FAISS index location
INDEX_DIR = Path("data/faiss_index")


def get_embeddings():
    """
    Returns the embedding model.
    Centralized to avoid duplication.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def chunk_documents(documents):
    """
    Chunk documents into smaller pieces suitable for embeddings.
    Chunking belongs to vector store preparation.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_documents(documents)


def create_vector_store():
    """
    ONE-TIME ingestion process:
    - Load documents
    - Chunk them
    - Create FAISS index
    - Save it to disk
    """

    print("📄 Loading documents...")
    documents = load_documents()

    print("✂️ Chunking documents...")
    chunks = chunk_documents(documents)

    print("🧠 Creating embeddings and FAISS index...")
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))

    print("✅ FAISS vector store created and saved")
    return vectorstore


def load_vector_store():
    """
    Runtime loading:
    - Loads FAISS index from disk
    - Used during retrieval / RAG
    """

    if not INDEX_DIR.exists():
        raise FileNotFoundError(
            "FAISS index not found. Run create_vector_store() first."
        )

    print("📦 Loading FAISS index from disk...")
    embeddings = get_embeddings()

    return FAISS.load_local(
        str(INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )


if __name__ == "__main__":
    # Run this ONCE to create the FAISS index
    create_vector_store()
