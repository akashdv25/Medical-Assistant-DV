# this file will have a function to load the llm from cerebras langchain

from dotenv import load_dotenv
import os
from typing import List, Dict, Tuple
from langchain_cerebras import ChatCerebras
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.documents import Document


load_dotenv()

class MedicalLLM:
    """Class to handle LLM initialization and medical context interactions"""
    
    def __init__(self, temperature: float = 0.5):
        """
        Initialize the Medical LLM with Cerebras model
        
        Args:
            temperature: Sampling temperature for the model (default: 0.5)
        """
        self.llm = ChatCerebras(
            model="llama-4-scout-17b-16e-instruct",
            temperature=temperature,
            api_key=os.getenv("CEREBRAS_API_KEY"),
        )

        # Define the system prompt template
        self.system_prompt = """You are an advanced RAG-based medical advisor. Your responses must be:
                                1. Based ONLY on the provided medical document context
                                2. Professional and accurate, citing specific parts of the source documents
                                3. Clear about any limitations in the provided context
                                4. Focused solely on medical information from the documents

                                For each piece of information you provide, you MUST cite the source document number in [Doc X] format.
                                If the required information is not in the provided context, state that clearly rather than making assumptions.
                                DO NOT provide medical advice beyond what's explicitly stated in the source documents."""

    def get_response(self, query: str, context_docs: List[Document]) -> Dict[str, any]:
        """
        Get LLM response based on query and retrieved documents
        
        Args:
            query: User's medical query
            context_docs: List of relevant documents retrieved by TopKRetriever
            
        Returns:
            Dictionary containing:
            - response: LLM's response with source citations
            - sources: List of source documents used
            - source_details: Mapping of document numbers to their full source paths
        """
        # Format context and track sources
        context = "\n\nRelevant Medical Documents:\n"
        source_details = {}

        for i, doc in enumerate(context_docs, 1):
            source_path = doc.metadata.get('source', 'Unknown')
            source_details[f"Document {i}"] = source_path
            context += f"\nDocument {i} (Source: {source_path}):\n{doc.page_content}\n"
            
        # Create messages with system prompt, context, and query
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Context: {context}\n\nQuery: {query}\n\nRemember to cite sources as [Doc X]")
        ]
        
        try:
            # Get LLM response
            response = self.llm.invoke(messages)
            

            
            return {
                "response": response.content,
                "source_details": source_details,
                "total_sources": len(context_docs)
            }
        except Exception as e:
            self.logger.log_system("error", f"Error processing query: {str(e)}")
            raise
    

    
if __name__ == "__main__":
    from src.document_vector_retrieval import TopKRetriever

    retriever = TopKRetriever(k=3)
    medical_llm = MedicalLLM(temperature=0.3)

    query = "What medications were prescribed and what were the blood test results?"

    relevant_docs = retriever.search_all_documents(query)
    result = medical_llm.get_response(query=query, context_docs=relevant_docs)

    print(result["response"])
    print(result["source_details"])
    print(result["total_sources"])
    
 