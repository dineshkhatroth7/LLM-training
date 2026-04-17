from typing import List, Dict, Any, Optional
import logging
from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_service import LLMService
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    """Main RAG pipeline that combines retrieval and generation."""
    
    def __init__(self):
        # Initialize components
        self.document_processor = DocumentProcessor(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        
        self.vector_store = VectorStore(
            persist_directory=config.CHROMA_PERSIST_DIRECTORY,
            embedding_model=config.EMBEDDING_MODEL
        )
        
        self.llm_service = LLMService(model=config.LLM_MODEL)
        
        logger.info("RAG pipeline initialized")
    
    def add_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        """Add documents to the knowledge base."""
        try:
            # Process documents
            documents = self.document_processor.process_multiple_documents(file_paths)
            
            if not documents:
                return {
                    "success": False,
                    "message": "No documents were successfully processed",
                    "processed_count": 0
                }
            
            # Convert to vector store format
            vector_docs = []
            for doc in documents:
                vector_docs.append({
                    'page_content': doc.page_content,
                    'metadata': doc.metadata
                })
            
            # Add to vector store
            self.vector_store.add_documents(vector_docs)
            
            return {
                "success": True,
                "message": f"Successfully processed and added {len(documents)} document chunks",
                "processed_count": len(documents)
            }
        
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            return {
                "success": False,
                "message": f"Error processing documents: {str(e)}",
                "processed_count": 0
            }
    
    def query(self, question: str, use_rag: bool = True) -> Dict[str, Any]:
        """Query the RAG system."""
        try:
            if not use_rag:
                # Direct LLM response without retrieval
                messages = [{"role": "user", "content": question}]
                response = self.llm_service.generate_response(messages)
                
                return {
                    "success": True,
                    "response": response,
                    "sources": [],
                    "method": "direct_llm"
                }
            
            # RAG-based response
            # Retrieve relevant documents
            retrieved_docs = self.vector_store.search_similar(
                query=question,
                top_k=config.TOP_K_RESULTS,
                similarity_threshold=config.SIMILARITY_THRESHOLD
            )
            
            if not retrieved_docs:
                return {
                    "success": True,
                    "response": "I don't have enough relevant information in my knowledge base to answer this question. Please try uploading some documents first or rephrase your question.",
                    "sources": [],
                    "method": "rag_no_context"
                }
            
            # Generate response using retrieved context
            response = self.llm_service.generate_rag_response(question, retrieved_docs)
            
            # Format sources
            sources = [
                {
                    "filename": doc['metadata'].get('filename', 'Unknown'),
                    "similarity": doc['similarity'],
                    "chunk_id": doc['metadata'].get('chunk_id', 'Unknown')
                }
                for doc in retrieved_docs
            ]
            
            return {
                "success": True,
                "response": response,
                "sources": sources,
                "method": "rag"
            }
        
        except Exception as e:
            logger.error(f"Error querying RAG system: {str(e)}")
            return {
                "success": False,
                "response": f"Error processing query: {str(e)}",
                "sources": [],
                "method": "error"
            }
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        return self.vector_store.get_collection_stats()
    
    def clear_knowledge_base(self) -> Dict[str, Any]:
        """Clear the knowledge base."""
        try:
            self.vector_store.clear_collection()
            return {
                "success": True,
                "message": "Knowledge base cleared successfully"
            }
        except Exception as e:
            logger.error(f"Error clearing knowledge base: {str(e)}")
            return {
                "success": False,
                "message": f"Error clearing knowledge base: {str(e)}"
            }
