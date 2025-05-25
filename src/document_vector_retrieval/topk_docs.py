from typing import List
from langchain_core.documents import Document
from src.knowledge_base import VectorStore
from src.logging import Logger

class TopKRetriever:
    """Retrieves top-k most relevant documents from vector stores (lab_reports, prescriptions, or combined)"""
    
    # Define available collections
    COMBINED_STORE = "combined"
    LAB_REPORTS_STORE = "lab_reports"
    PRESCRIPTIONS_STORE = "prescriptions"
    
    def __init__(self, k: int = 5):
        """
        Initialize the retriever and create/update vector stores
        
        Args:
            k: Number of documents to retrieve (default: 5)
        """
        self.logger = Logger()
        self.vector_store = VectorStore()
        self.k = k
        
        # Create/update all stores on initialization
        self.logger.log_system("info", "Creating/updating vector stores...")
        self.stores = self.vector_store.create_all_stores()
        if not self.stores:
            self.logger.log_system("warning", "No vector stores were created. Check if there are documents in the docs directory.")
        
    def get_relevant_documents(self, query: str, collection: str = COMBINED_STORE) -> List[Document]:
        """
        Get the top-k most relevant documents for a query from a specific collection
        
        Args:
            query: Search query
            collection: Which collection to search ("lab_reports", "prescriptions", or "combined")
            
        Returns:
            List of relevant documents
        """
        if collection not in [self.COMBINED_STORE, self.LAB_REPORTS_STORE, self.PRESCRIPTIONS_STORE]:
            raise ValueError(f"Invalid collection: {collection}. Must be one of: combined, lab_reports, prescriptions")
            
        try:
            # Ensure store exists and is populated
            if collection == self.COMBINED_STORE:
                store = self.vector_store.create_combined_store()
            elif collection == self.LAB_REPORTS_STORE:
                store = self.vector_store.create_lab_reports_store()
            else:
                store = self.vector_store.create_prescriptions_store()
                
            if not store:
                self.logger.log_system("warning", f"No documents found in {collection} store")
                return []
                
            results = store.similarity_search(query, k=self.k)
            self.logger.log_system("info", f"Found {len(results)} relevant documents in {collection} store")
            return results
        except Exception as e:
            self.logger.log_system("error", f"Error retrieving documents from {collection} store: {str(e)}")
            raise
            
    def search_lab_reports(self, query: str) -> List[Document]:
        """
        Search specifically in lab reports collection
        
        Args:
            query: Search query
            
        Returns:
            List of relevant lab report documents
        """
        return self.get_relevant_documents(query, collection=self.LAB_REPORTS_STORE)
        
    def search_prescriptions(self, query: str) -> List[Document]:
        """
        Search specifically in prescriptions collection
        
        Args:
            query: Search query
            
        Returns:
            List of relevant prescription documents
        """
        return self.get_relevant_documents(query, collection=self.PRESCRIPTIONS_STORE)
        
    def search_all_documents(self, query: str) -> List[Document]:
        """
        Search in the combined collection (all documents)
        
        Args:
            query: Search query
            
        Returns:
            List of relevant documents from all collections
        """
        return self.get_relevant_documents(query, collection=self.COMBINED_STORE)

if __name__ == "__main__":
    # Example usage
    print("\nInitializing TopKRetriever and creating vector stores...")
    retriever = TopKRetriever(k=3)
    
    # Test different search methods
    print("\nSearching Lab Reports:")
    print("=====================")
    lab_results = retriever.search_lab_reports("medical examination results")
    for i, doc in enumerate(lab_results, 1):
        print(f"\n{i}. Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"   Content: {doc.page_content[:200]}...")
        
    print("\nSearching Prescriptions:")
    print("======================")
    prescription_results = retriever.search_prescriptions("prescribed medications")
    for i, doc in enumerate(prescription_results, 1):
        print(f"\n{i}. Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"   Content: {doc.page_content[:200]}...")
        
    print("\nSearching All Documents:")
    print("======================")
    all_results = retriever.search_all_documents("patient medical records")
    for i, doc in enumerate(all_results, 1):
        print(f"\n{i}. Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"   Content: {doc.page_content[:200]}...")