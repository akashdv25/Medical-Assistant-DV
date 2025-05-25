## This is how a basic rag workflow looks like .


### 1. Knowledge Base Creation (Offline Step):

- You start with a collection of documents (PDFs, HTML, articles, etc.).

- These documents are split into small chunks (e.g., 300–500 words) using a text splitter to preserve context.

- Each chunk is converted into a vector embedding using an embedding model (like OpenAI, SentenceTransformer, or HuggingFace models).

- These embeddings (vectors) are stored in a vector database (vector store) such as FAISS, Chroma, Weaviate, Pinecone, etc.

---

### 2. At Query Time (Live User Input):

A user asks a question (query).
The system:

- Embeds the query into a vector (same embedding model as used above).

- Performs a vector similarity search in the vector store to retrieve the top K most similar document chunks (e.g., top_k = 5).

- These top-K chunks are then fed into the prompt of the LLM along with the user’s question ,these act as a reference for the model to answer the question.

---

### 3. LLM Response:

- The LLM (e.g., GPT-4, LLaMA, Mistral) now uses the retrieved document chunks as context.

- It generates a final answer that is grounded in the retrieved knowledge.