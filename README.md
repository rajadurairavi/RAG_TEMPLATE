
┌────────────────────────────┐
│      Employee Question     │
│  "What is the leave policy?"│
└─────────────┬──────────────┘
              ↓
┌────────────────────────────┐
│     Query Processing       │
│ - Clean question           │
│ - Pass as-is to pipeline   │
└─────────────┬──────────────┘
              ↓
┌──────────────────────────────────────────┐
│   Document Retrieval (RAG Retriever)     │
│                                          │
│  1️⃣ Semantic Search (FAISS)              │
│     → fetch top-k chunks                 │
│                                          │
│  2️⃣ Intent-aware Filtering               │
│     → keep only leave-related chunks     │
│                                          │
│  3️⃣ Context Limiting                     │
│     → top 3–4 chunks only                │
└─────────────┬────────────────────────────┘
              ↓
┌────────────────────────────┐
│      Context Injection     │
│                            │
│  Context string injected   │
│  into ChatPromptTemplate   │
│                            │
│  {context} + {question}    │
└─────────────┬──────────────┘
              ↓
┌────────────────────────────┐
│   LLM Answer Generation    │
│  (ChatGroq – LLaMA)        │
│                            │
│  • Reads ONLY context      │
│  • No guessing             │
│  • No hallucination        │
└─────────────┬──────────────┘
              ↓
┌────────────────────────────┐
│  Final Answer + Sources    │
│                            │
│  ✔ Grounded                │
│  ✔ Accurate                │
│  ✔ Explainable             │
└────────────────────────────┘


User Question
     ↓
answer_question(question)
     ↓
LCEL RAG Chain
     ↓
{
  "context": retriever(question),
  "question": question
}
     ↓
retriever()
  ├─ semantic_search()
  ├─ intent_filter()
  ├─ build_context()
     ↓
ChatPromptTemplate
     ↓
ChatGroq LLM
     ↓
StrOutputParser
     ↓
Final Answer

“RAG is retrieval first, reasoning later — the LLM never sees the database, only the curated context.”

🧠 YOUR RAG – FULL FLOW (Box-by-Box)
🟦 1️⃣ Knowledge Base (Static World)
data/
 ├── Company_Guidelines.txt
 ├── HR_Policies.txt


What it is

Raw business knowledge

PDFs / TXT / DOCs

Rule

LLM never sees these files directly ❌

🟦 2️⃣ Ingestion (ONE-TIME job)
docs_load.py

Files
  ↓
Text
  ↓
Chunks


What happens

Read files

Split into chunks (size + overlap)

Add metadata (source, page)

🧠 Think: “Preparing food before cooking”

🟦 3️⃣ Embeddings (Meaning → Numbers)
"Employees accrue PTO..." → [0.023, 0.91, -0.44, ...]


What happens

Each chunk → vector

Captures semantic meaning, not keywords

🧠 Think: “GPS coordinates for meaning”

🟦 4️⃣ Vector Store (FAISS) 💾
FAISS Index
 ├── vector → chunk
 ├── vector → chunk


What happens

Store vectors + text

Saved to disk

Loaded at runtime

✅ Fast
✅ Scalable
✅ No re-ingestion needed

🧠 RUNTIME FLOW (When User Asks a Question)
🟨 5️⃣ User Question
"What is the company's leave policy?"

🟨 6️⃣ Semantic Search (Retriever Layer)

📂 retrieval/retriever.py

question
   ↓
embedding
   ↓
FAISS.similarity_search(k=8)
   ↓
top-K documents


Key rules

Retriever:

❌ No LLM

❌ No prompts

❌ No answers

✅ Only fetch relevant chunks

🧠 Think: “Search engine, not brain”

🟨 7️⃣ Intent-Aware Filtering (RAG Quality Booster)

📂 rag_pipeline.py

Retrieved docs
   ↓
filter_documents_by_intent()
   ↓
ONLY leave-related chunks


Why this matters

Prevents unrelated sections:

ethics

discipline

compensation

🧠 This is why your final answer became clean.

🟨 8️⃣ Context Builder (LLM-safe)
Document objects
   ↓
build_context()
   ↓
Single clean text string

6.1 PTO ...
6.2 Sick Leave ...
6.3 Other Leave ...


Why

LLM understands text, not objects

Control size + ordering

🟦 9️⃣ LCEL RAG Chain (The Brain Wiring)

📂 rag_pipeline.py

{
  "context": retriever,
  "question": RunnablePassthrough()
}
   ↓
Prompt
   ↓
LLM
   ↓
Output Parser


🧠 This is the heart of modern LangChain

🟦 🔟 Prompt (Rules for the Brain)

📂 prompts.py

You are an HR assistant.
Answer ONLY from context.
If not found, say "I don't know".


Purpose

Prevent hallucination

Enforce grounding

Control tone & format

🟦 1️⃣1️⃣ LLM (ChatGroq)
Context + Question
        ↓
Reasoned Answer


Important

LLM does NOT search

LLM does NOT know FAISS

LLM only reasons over provided context

🟦 1️⃣2️⃣ Final Answer 🎯
Clean
Relevant
Grounded
No noise


Exactly what you saw 👇

6.1 PTO
6.2 Sick Leave
6.3 Other Leave Types

🧠 ONE-SCREEN MEMORY DIAGRAM (SAVE THIS)
FILES
  ↓
CHUNKS
  ↓
EMBEDDINGS
  ↓
FAISS (Stored)

USER QUESTION
  ↓
Semantic Search (Retriever)
  ↓
Intent Filtering
  ↓
Context Builder
  ↓
PROMPT + CONTEXT + QUESTION
  ↓
LLM
  ↓
FINAL ANSWER

🎯 Interview One-Line Explanation (VERY IMPORTANT)

“We ingest documents once, store them in a FAISS vector DB, retrieve relevant chunks using semantic search, refine them with intent-aware filtering, build a clean context, and pass that into an LCEL-based RAG chain where the LLM generates grounded answers.”

🔥 That is senior-level wording.

🧭 What you are ready for now

You can confidently move to:

✅ Multi-query RAG

✅ Metadata filters

✅ Tool calling

✅ Agentic RAG




