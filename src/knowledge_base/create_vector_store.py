from typing import List, Dict, Optional, Set
from pathlib import Path
from uuid import uuid4
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from src.logging import Logger
from .create_chunks import CreateChunks

class VectorStore:
    """
    Creates and manages Chroma vector stores using HuggingFace embeddings.
    Maintains separate collections for lab reports, prescriptions, and combined data.
    """
    
    def __init__(self):
        self.logger = Logger()
        
        # Base path for vector stores
        self.base_persist_dir = Path("chroma_db")
        self.base_persist_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize chunks creator
        self.chunks = CreateChunks()
        
        # Initialize embedding model
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        self.logger.log_system("info", "Initialized VectorStore")

    def _get_persist_directory(self, collection_name: str) -> str:
        """Get the persist directory for a collection"""
        return str(self.base_persist_dir / f"{collection_name}_collection")

    def get_store(self, collection_name: str) -> Chroma:
        """Get a Chroma store with the given collection name"""
        persist_directory = self._get_persist_directory(collection_name)
        return Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding_model,
            persist_directory=persist_directory
        )

    def _sync_documents(self, store: Chroma, documents: List[Document], append: bool = True) -> Chroma:
        """Synchronize documents in the store with current file system state"""
        if not documents:
            if append:
                try:
                    existing_results = store.get()
                    if existing_results and existing_results["ids"]:
                        self.logger.log_system("info", "Clearing store as no documents exist in this category")
                        store.delete(ids=existing_results["ids"])
                except Exception as e:
                    self.logger.log_system("warning", f"Error clearing store: {str(e)}")
                return store
            else:
                # If not appending and no documents, just recreate empty collection
                return self.get_store(store._collection_name)

        # Generate UUIDs for new documents
        doc_ids = [str(uuid4()) for _ in range(len(documents))]

        if not append:
            # For non-append mode, recreate the collection and add all documents
            collection_name = store._collection_name
            persist_directory = self._get_persist_directory(collection_name)
            
            # Properly delete and recreate the store
            try:
                store.delete_collection()
            except Exception as e:
                self.logger.log_system("warning", f"Error deleting collection: {str(e)}")
            
            # Create new store and add documents
            new_store = Chroma(
                collection_name=collection_name,
                embedding_function=self.embedding_model,
                persist_directory=persist_directory
            )
            new_store.add_documents(documents=documents, ids=doc_ids)
            return new_store

        # Handle append mode
        try:
            # Get existing documents and their metadata
            existing_results = store.get()
            if existing_results and existing_results["documents"]:
                existing_docs = existing_results["documents"]
                existing_metadata = existing_results["metadatas"]
                existing_ids = existing_results["ids"]

                # Create sets for efficient lookup
                current_sources = {doc.metadata["source"] for doc in documents}
                existing_sources = {meta["source"] for meta in existing_metadata if meta and "source" in meta}

                # Find documents to remove (sources that no longer exist)
                sources_to_remove = existing_sources - current_sources
                if sources_to_remove:
                    ids_to_remove = [
                        id_ for id_, meta in zip(existing_ids, existing_metadata)
                        if meta.get("source") in sources_to_remove
                    ]
                    if ids_to_remove:
                        self.logger.log_system("info", 
                            f"Removing {len(ids_to_remove)} chunks from {len(sources_to_remove)} moved/deleted files")
                        store.delete(ids=ids_to_remove)

                # Find new documents to add
                new_docs = []
                new_ids = []
                for doc, doc_id in zip(documents, doc_ids):
                    # Check if this exact source is already in the store
                    if doc.metadata["source"] not in existing_sources:
                        new_docs.append(doc)
                        new_ids.append(doc_id)
                
                if new_docs:
                    self.logger.log_system("info", f"Adding {len(new_docs)} new chunks")
                    store.add_documents(documents=new_docs, ids=new_ids)
                else:
                    self.logger.log_system("info", "No new chunks to add")
            else:
                # If store is empty, add all documents
                self.logger.log_system("info", f"Adding {len(documents)} chunks to empty store")
                store.add_documents(documents=documents, ids=doc_ids)
        except Exception as e:
            self.logger.log_system("error", f"Error during sync: {str(e)}")
            # If sync fails, recreate the store
            store.delete_collection()
            new_store = self.get_store(store._collection_name)
            new_store.add_documents(documents=documents, ids=doc_ids)
            return new_store

        return store

    def create_lab_reports_store(self, append: bool = True) -> Optional[Chroma]:
        """Create or update lab reports vector store"""
        try:
            chunks = self.chunks.create_lab_report_chunks()
            store = self.get_store("lab_reports")
            return self._sync_documents(store, chunks, append)
        except Exception as e:
            self.logger.log_system("error", f"Error creating lab reports store: {str(e)}")
            raise

    def create_prescriptions_store(self, append: bool = True) -> Optional[Chroma]:
        """Create or update prescriptions vector store"""
        try:
            chunks = self.chunks.create_prescription_report_chunks()
            store = self.get_store("prescriptions")
            return self._sync_documents(store, chunks, append)
        except Exception as e:
            self.logger.log_system("error", f"Error creating prescriptions store: {str(e)}")
            raise

    def create_combined_store(self, append: bool = True) -> Optional[Chroma]:
        """Create or update combined vector store"""
        try:
            all_docs = self.chunks.process_all_documents()
            chunks = []
            
            if "lab_report_chunks" in all_docs:
                chunks.extend(all_docs["lab_report_chunks"])
            if "prescription_chunks" in all_docs:
                chunks.extend(all_docs["prescription_chunks"])
            
            store = self.get_store("combined")
            # Use append mode to maintain the existing store and only update changed documents
            return self._sync_documents(store, chunks, append=True)
        except Exception as e:
            self.logger.log_system("error", f"Error creating combined store: {str(e)}")
            raise

    def create_all_stores(self) -> Dict[str, Optional[Chroma]]:
        """Create or update all vector stores"""
        return {
            "lab_reports": self.create_lab_reports_store(),
            "prescriptions": self.create_prescriptions_store(),
            "combined": self.create_combined_store()
        }

    def _print_store_stats(self, store_name: str, store: Chroma):
        """Print statistics about a vector store"""
        results = store.get()
        if not results:
            print(f"\n{store_name} Store is empty")
            return
            
        docs = results['documents']
        metadatas = results['metadatas']
        
        # Count unique sources
        sources = {meta["source"] for meta in metadatas if meta and "source" in meta}
        
        # Count chunks per source
        chunks_per_source = {}
        for doc, meta in zip(docs, metadatas):
            source = meta.get("source", "unknown")
            chunks_per_source[source] = chunks_per_source.get(source, 0) + 1
        
        print(f"\n{store_name} Store Statistics:")
        print(f"Total source files: {len(sources)}")
        print(f"Total chunks: {len(docs)}")
        print("\nSource files and their chunks:")
        for source in sorted(sources):
            print(f"  - {source}: {chunks_per_source[source]} chunks")

if __name__ == "__main__":
    print("\nStarting Vector Store Creation/Update")
    print("====================================")
    
    vector_store = VectorStore()
    stores = vector_store.create_all_stores()
    
    print("\nChroma Storage Information:")
    print("===========================")
    
    for store_name, store in stores.items():
        if store is not None:
            vector_store._print_store_stats(store_name, store)