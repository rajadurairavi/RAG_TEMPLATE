from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a helpful assistant.
Answer the question strictly using the provided context.

Rules:
- Use ONLY the context.
- If the answer is not found, say:
  "I don't know based on the provided context."
- Do NOT use outside knowledge.
"""
    ),
    (
        "human",
        """
Context:
{context}

Question:
{question}
"""
    )
])
