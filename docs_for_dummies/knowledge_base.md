## Knowledge Base Creation : ` Available Tools and Packages ` 

### 1. Document Loader & Text Splitter

| Library                  | Strengths                                                                                                                                                          | Weaknesses                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| **LangChain**            | ✅ Built-in loaders for PDF, HTML, Notion, CSV, etc.<br>✅ Smart text splitter (recursive, by sentences, etc.)<br>✅ Integration-ready with embeddings and vector DBs | ❌ Heavier dependency<br>❌ Overkill for very simple use cases  |
| **LlamaIndex**           | ✅ Good for hierarchical document indexing<br>✅ Supports node-based splitting<br>✅ Works well for long documents                                                    | ❌ Steeper learning curve<br>❌ Not modular like LangChain      |
| **Unstructured.io**      | ✅ Extracts structured data from messy PDFs, HTML, scanned images<br>✅ OCR support                                                                                  | ❌ Requires some setup<br>❌ Heavier memory use for large files |
| **PyMuPDF / pdfplumber** | ✅ Great for custom PDF parsing<br>✅ Lightweight                                                                                                                    | ❌ Manual splitting required<br>❌ No high-level abstraction    |

<br>

`We will LangChain for building end-to-end pipelines.`


<br>

### 2. Embedding Models / Libraries

| Tool/Library                 | Models Supported                          | Strengths                                                           | Weaknesses                                              |
| ---------------------------- | ----------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| **OpenAI API**               | `text-embedding-3-small`, `ada-002`, etc. | ✅ Very high-quality embeddings<br>✅ Easy API<br>✅ Fast inference    | ❌ Paid API<br>❌ Can't run locally                       |
| **HuggingFace Transformers** | `sentence-transformers`, `BAAI/bge`, etc. | ✅ Open-source<br>✅ Can run locally<br>✅ Many fine-tuned models      | ❌ Slower than OpenAI<br>❌ More complex setup (GPU)      |
| **SentenceTransformers**     | `all-MiniLM`, `paraphrase-MPNet`, etc.    | ✅ Extremely simple API<br>✅ Fast on CPU/GPU<br>✅ HuggingFace-backed | ❌ May need tuning for domain-specific data              |
| **Cohere / Mistral AI**      | Hosted embeddings API                     | ✅ Good quality<br>✅ Fast<br>✅ Easy to use with SDKs                 | ❌ Requires API key<br>❌ Privacy concerns with cloud use |

<br>

`We will be using Huggingface embeddings as embedding model`

<br>

### 3. Vector Stores / Databases

| Vector Store | Type        | Strengths                                                                 | Weaknesses                                             |
| ------------ | ----------- | ------------------------------------------------------------------------- | ------------------------------------------------------ |
| **FAISS**    | Local       | ✅ Fast and free<br>✅ Great for prototyping<br>✅ No internet needed        | ❌ No persistence<br>❌ No scalability<br>❌ No filtering |
| **Chroma**   | Local       | ✅ Simple to use<br>✅ Built-in persistence<br>✅ Pythonic API               | ❌ Not production-scale yet<br>❌ Limited documentation  |
| **Weaviate** | Cloud/Local | ✅ Hybrid search (vector + keyword)<br>✅ REST & GraphQL APIs<br>✅ Scalable | ❌ Heavier setup<br>❌ Requires Docker or Cloud          |
| **Pinecone** | Cloud       | ✅ Fully managed<br>✅ High performance<br>✅ Metadata filtering             | ❌ Paid plans<br>❌ Not local<br>❌ Requires API key      |
| **Milvus**   | Local/Cloud | ✅ Handles billions of vectors<br>✅ Scalable and open source               | ❌ Complex setup<br>❌ Overkill for small projects       |
| **Qdrant**   | Local/Cloud | ✅ Great hybrid search<br>✅ Scalable<br>✅ REST/gRPC API                    | ❌ Slightly more setup than FAISS or Chroma             |


| Vector Store | Type        | Strengths                                                                 | Weaknesses                                             |
| ------------ | ----------- | ------------------------------------------------------------------------- | ------------------------------------------------------ |
| **FAISS**    | Local       | ✅ Fast and free<br>✅ Great for prototyping<br>✅ No internet needed        | ❌ No persistence<br>❌ No scalability<br>❌ No filtering |
| **Chroma**   | Local       | ✅ Simple to use<br>✅ Built-in persistence<br>✅ Pythonic API               | ❌ Not production-scale yet<br>❌ Limited documentation  |
| **Weaviate** | Cloud/Local | ✅ Hybrid search (vector + keyword)<br>✅ REST & GraphQL APIs<br>✅ Scalable | ❌ Heavier setup<br>❌ Requires Docker or Cloud          |
| **Pinecone** | Cloud       | ✅ Fully managed<br>✅ High performance<br>✅ Metadata filtering             | ❌ Paid plans<br>❌ Not local<br>❌ Requires API key      |
| **Milvus**   | Local/Cloud | ✅ Handles billions of vectors<br>✅ Scalable and open source               | ❌ Complex setup<br>❌ Overkill for small projects       |
| **Qdrant**   | Local/Cloud | ✅ Great hybrid search<br>✅ Scalable<br>✅ REST/gRPC API                    | ❌ Slightly more setup than FAISS or Chroma             |

<br>

`we will use chromadb as vector store`

<br>


## Our Final Approach

| Step             | Recommended Tool                          |
| ---------------- | ----------------------------------------- |
| Document loading | `LangChain.document_loaders`  |
| Text splitting   | `LangChain.text_splitter`                 |
| Embeddings       | `Hugging face embeddings`    |
| Vector store     | `Chroma` (local)    |
