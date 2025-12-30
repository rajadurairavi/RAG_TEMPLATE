from app.vector_store.vectorstore import load_vector_store


def semantic_search(query: str, k: int = 8, debug: bool = False):
    """
    Perform semantic search over the FAISS vector store.

    Retriever responsibility:
    - Take a query
    - Return relevant documents

    It does NOT:
    - Know about prompts
    - Talk to LLMs
    - Decide answers
    """

    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(query, k=k)

    # Debug / visibility output (optional)
    if debug:
        for idx, doc in enumerate(results, start=1):
            print(f"\nResult {idx}")
            print("-" * 40)
            print(doc.page_content[:500])
            print("\nMetadata:", doc.metadata)

    return results


# Manual retriever test (ONLY runs when this file is executed directly)
if __name__ == "__main__":
    semantic_search(
        query="What is the company's leave policy?",
        k=8,
        debug=True
    )
