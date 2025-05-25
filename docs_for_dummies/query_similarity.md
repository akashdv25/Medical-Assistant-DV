## Query Similarity Search Implementation : ` Available Tools and our Approach `

query -> embeddings on same model -> .similarity search(vector store)-> top k documents

### 1. Embedding the User Query

This step uses the same embedding model you used for documents

| Tool/Library                                              | Strengths                                            | Weaknesses                                          |
| --------------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------- |
| `sentence-transformers`                                   | ✅ Local<br>✅ Fast on CPU/GPU<br>✅ HuggingFace models | ❌ Larger models need GPU                            |
| `OpenAIEmbeddings` (LangChain)                            | ✅ Easy to use<br>✅ High quality via API              | ❌ Paid API<br>❌ Requires API key                    |
| `HuggingFaceEmbeddings` (LangChain)                       | ✅ Any HuggingFace model<br>✅ Works offline           | ❌ Slightly more setup<br>❌ Not all models work well |
| `InstructorEmbeddings` (for instruction-tuned embeddings) | ✅ Often better for question-type queries             | ❌ Larger model size                                 |


<br>

`Use Case`
<br>

`from langchain.embeddings import HuggingFaceEmbeddings`
<br>

`embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
`

### 2. Vector Similarity Search in ChromaDB

| Feature         | Chroma via LangChain                     |
| --------------- | ---------------------------------------- |
| Top-k retrieval | ✅ Supported via `search_kwargs`          |
| Filtering       | ✅ (Limited metadata filtering supported) |
| Simple API      | ✅ `retriever.get_relevant_documents()`   |

<br>

`Use Case`
<br>

``from langchain.vectorstores import Chroma``

``retriever = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
).as_retriever(search_kwargs={"k": 5})``

### 3. LLM for Answer Generation (With Context)

| Tool/Library                   | Strengths                                                        | Weaknesses                                 |
| ------------------------------ | ---------------------------------------------------------------- | ------------------------------------------ |
| `langchain.chains.RetrievalQA` | ✅ Simple 1-line integration<br>✅ Handles context prep and prompt | ❌ Less customizable than DIY approach      |
| `LLMChain` + custom prompt     | ✅ Full control of prompt structure                               | ❌ Requires manual context formatting       |
| `ConversationalRetrievalChain` | ✅ Maintains memory of past chats                                 | ❌ Requires chat-based LLM and memory setup |
<br>

## Summary table 
| Step              | Tool/Package                                                         | Why Use It                                    |
| ----------------- | -------------------------------------------------------------------- | --------------------------------------------- |
| Embed user query  |  `HuggingFaceEmbeddings` | Converts query to vector                      |
| Vector search     | `Chroma` + `as_retriever()`                                          | Retrieves top-K relevant document chunks      |
| Answer generation | `RetrievalQA`, `ConversationalRetrievalChain`, `LLMChain`            | Combines chunks + query into a prompt for LLM |
| Memory | `ConversationBufferMemory`                                           | Adds chat memory for follow-ups               |



