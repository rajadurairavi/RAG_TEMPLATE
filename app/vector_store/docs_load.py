from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader

DATA_DIR = Path("data")

def load_documents():
    documents = []

    for file in DATA_DIR.iterdir():
        if file.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(file))
            documents.extend(loader.load())
        elif file.suffix.lower() == ".txt":
            loader = TextLoader(str(file), encoding="utf-8")
            documents.extend(loader.load())

    print(f"✓ Loaded {len(documents)} document(s)")
    return documents


if __name__ == "__main__":
    docs = load_documents()



