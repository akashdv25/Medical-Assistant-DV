# Medical Assistant RAG System

## Knowledge Base Entry Point: TopKRetriever

The `TopKRetriever` class serves as the main entry point for our medical document retrieval system. It automatically manages and searches through three vector stores:
- Lab Reports (`lab_reports_collection`)
- Prescriptions (`prescriptions_collection`) 
- Combined Documents (`combined_collection`)

### How It Works

1. **Initialization & Synchronization**
```python
from src.document_vector_retrieval.topk_docs import TopKRetriever

# Creates/updates all vector stores automatically
retriever = TopKRetriever(k=3)  # k = number of documents to retrieve
```

2. **Document Organization**
- Lab reports are stored in `docs/lab_reports/`
- Prescriptions are stored in `docs/prescriptions/`
- When files are added/moved, the vector stores are automatically updated on TopKRetriever initialization

3. **Search Methods**
```python
# Search only lab reports
lab_results = retriever.search_lab_reports("query about lab tests")

# Search only prescriptions
prescription_results = retriever.search_prescriptions("query about medications")

# Search all medical documents
all_results = retriever.search_all_documents("general medical query")
```

4. **Results Format**
Each result includes:
- Source document path (`doc.metadata['source']`)
- Relevant content (`doc.page_content`)
- Top-k most relevant matches

### Vector Store Synchronization

The system maintains three Chroma vector stores:
```
chroma_db/
├── lab_reports_collection/
├── prescriptions_collection/
└── combined_collection/
```

Synchronization happens automatically when:
1. TopKRetriever is initialized
2. A search method is called
3. The vector stores are created if they don't exist
4. Existing stores are updated with new/moved documents

### Example Usage

```python
# Initialize retriever
retriever = TopKRetriever(k=3)

# Search for lab results
results = retriever.search_lab_reports("blood test results")
for doc in results:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:200]}...")
```

```python
#search for prescriptions
results = retriever.search_prescriptions("prescribed medications")
for doc in results:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:200]}...")
```

```python
#search for all documents
results = retriever.search_all_documents("patient medical records")
for doc in results:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:200]}...")
```