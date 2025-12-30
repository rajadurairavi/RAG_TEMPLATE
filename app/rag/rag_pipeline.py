import os
from typing import List

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.retrieval.retriever import semantic_search
from app.rag.prompts import RAG_PROMPT


# ============================================================
# Context Builder
# ============================================================

def build_context(documents) -> str:
    """
    Convert retrieved documents into a single context string.
    """
    return "\n\n".join(doc.page_content for doc in documents)


# ============================================================
# Intent-aware filtering (QUALITY IMPROVEMENT)
# ============================================================

def filter_documents_by_intent(documents, question: str):
    """
    Filter documents based on question intent.
    Prevents unrelated sections from entering context.
    """
    question_lower = question.lower()

    if "leave" in question_lower or "time off" in question_lower:
        keywords = ["leave", "pto", "sick", "time off", "absence"]

        filtered = [
            doc for doc in documents
            if any(k in doc.page_content.lower() for k in keywords)
        ]

        # Fallback if filter removes everything
        if filtered:
            return filtered

    return documents


# ============================================================
# RAG-facing Retriever (USED BY LCEL)
# ============================================================

def retriever(question: str) -> str:
    """
    RAG retriever:
    - Semantic search
    - Intent-aware filtering
    - Context construction
    """
    documents = semantic_search(question, k=8)
    documents = filter_documents_by_intent(documents, question)

    # Limit context size (VERY important)
    documents = documents[:4]

    return build_context(documents)


# ============================================================
# LLM
# ============================================================

def get_llm():
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",
        temperature=0
    )


# ============================================================
# LCEL RAG Chain
# ============================================================

def build_rag_chain():
    llm = get_llm()
    prompt = RAG_PROMPT

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# ============================================================
# Public API
# ============================================================

def answer_question(question: str) -> str:
    rag_chain = build_rag_chain()
    return rag_chain.invoke(question)


# ============================================================
# Manual Test
# ============================================================

if __name__ == "__main__":
    answer = answer_question(
        "What is the company's leave policy?"
    )

    print("\n🧠 Final Answer")
    print("=" * 60)
    print(answer)
