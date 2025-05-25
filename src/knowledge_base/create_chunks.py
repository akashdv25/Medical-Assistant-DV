from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from src import Logger
from .data_ingestion import Ingestion


class CreateChunks:
   
    """
    A class to create text chunks from medical documents using recursive character splitting.
    
    This class handles the chunking of both lab reports and prescriptions, with configurable
    chunk sizes and overlaps. It includes logging and error handling for better monitoring.
    
    Attributes:
        chunk_size (int): The size of each text chunk in characters
        chunk_overlap (int): The number of characters to overlap between chunks
        logger (Logger): Logger instance for tracking operations
        lab_reports (List[Document]): List of loaded lab report documents
        prescriptions (List[Document]): List of loaded prescription documents
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the CreateChunks class.
        
        Args:
            chunk_size (int, optional): Size of each chunk in characters. Defaults to 1000.
            chunk_overlap (int, optional): Overlap between chunks in characters. Defaults to 200.
        """
        self.logger = Logger()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        try:
            self.logger.log_system("info", "Initializing document ingestion")
            documents_object = Ingestion()
            self.lab_reports = documents_object.load_lab_reports()
            self.prescriptions = documents_object.load_prescriptions()
            self.logger.log_system("info", 
                f"Successfully loaded {len(self.lab_reports)} lab reports and "
                f"{len(self.prescriptions)} prescriptions"
            )
        except Exception as e:
            self.logger.log_system("error", f"Failed to initialize document ingestion: {str(e)}")
            self.lab_reports = []
            self.prescriptions = []

    def _create_chunks(self, documents: List[Document], doc_type: str) -> List[Document]:
        """
        Internal method to create chunks from a list of documents.
        
        Args:
            documents (List[Document]): List of documents to be chunked
            doc_type (str): Type of documents being processed ('lab_reports' or 'prescriptions')
            
        Returns:
            List[Document]: List of document chunks with preserved metadata
        """
        try:
            self.logger.log_system("info", 
                f"Starting to create chunks for {doc_type} with "
                f"chunk_size={self.chunk_size}, overlap={self.chunk_overlap}"
            )
            
            if not documents:
                self.logger.log_system("warning", f"No {doc_type} documents to process")
                return []
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                add_start_index=True
            )
            
            chunks = text_splitter.split_documents(documents)
            
            # Log chunk statistics
            self.logger.log_system("info", 
                f"Created {len(chunks)} chunks from {len(documents)} {doc_type}. "
                f"Average chunk size: {sum(len(chunk.page_content) for chunk in chunks)/len(chunks):.2f} "
                f"characters"
            )
            
            return chunks
            
        except Exception as e:
            self.logger.log_system("error", f"Error creating chunks for {doc_type}: {str(e)}")
            return []

    def create_lab_report_chunks(self) -> List[Document]:
        """
        Create chunks from lab report documents.
        
        Returns:
            List[Document]: List of chunked lab report documents
        """
        return self._create_chunks(self.lab_reports, "lab_reports")
    
    def create_prescription_report_chunks(self) -> List[Document]:
        """
        Create chunks from prescription documents.
        
        Returns:
            List[Document]: List of chunked prescription documents
        """
        return self._create_chunks(self.prescriptions, "prescriptions")
    
    def get_chunk_statistics(self, chunks: List[Document]) -> dict:
        """
        Get statistical information about the chunks.
        
        Args:
            chunks (List[Document]): List of document chunks
            
        Returns:
            dict: Dictionary containing chunk statistics
        """
        try:
            if not chunks:
                return {"total_chunks": 0, "avg_size": 0, "min_size": 0, "max_size": 0}
            
            chunk_sizes = [len(chunk.page_content) for chunk in chunks]
            stats = {
                "total_chunks": len(chunks),
                "avg_size": sum(chunk_sizes) / len(chunks),
                "min_size": min(chunk_sizes),
                "max_size": max(chunk_sizes)
            }
            
            self.logger.log_system("info", f"Chunk statistics: {stats}")
            return stats
            
        except Exception as e:
            self.logger.log_system("error", f"Error calculating chunk statistics: {str(e)}")
            return {}

    def process_all_documents(self) -> dict:
        """
        Process both lab reports and prescriptions and return all chunks.
        
        Returns:
            dict: Dictionary containing both types of chunks and their statistics
        """
        try:
            lab_chunks = self.create_lab_report_chunks()
            prescription_chunks = self.create_prescription_report_chunks()
            
            result = {
                "lab_report_chunks": lab_chunks,
                "prescription_chunks": prescription_chunks,
                "lab_report_stats": self.get_chunk_statistics(lab_chunks),
                "prescription_stats": self.get_chunk_statistics(prescription_chunks)
            }
            
            self.logger.log_system("info", "Successfully processed all documents")
            return result
            
        except Exception as e:
            self.logger.log_system("error", f"Error processing all documents: {str(e)}")
            return {}
        


# sample run
if __name__ == "__main__":
    chunks = CreateChunks()

    print("--------------------------------")
    print("Processing all documents")
    print("--------------------------------")
    print(chunks.process_all_documents())
    print("--------------------------------")
    print("Processing lab report chunks")
    print("--------------------------------")
    print(chunks.create_lab_report_chunks())
    print("--------------------------------")
    print("Processing prescription chunks")
    print("--------------------------------")
    print(chunks.create_prescription_report_chunks())
    print("--------------------------------")