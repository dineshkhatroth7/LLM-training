import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Manages vector embeddings and similarity search using ChromaDB."""
    
    def __init__(self, persist_directory: str = "./chroma_db", embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"Vector store initialized with {self.collection.count()} documents")
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector store."""
        if not documents:
            logger.warning("No documents to add")
            return
        
        # Extract texts and metadata
        texts = [doc['page_content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Generate IDs
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Added {len(documents)} documents to vector store")
    
    def search_similar(self, query: str, top_k: int = 3, similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Process results
        similar_docs = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            # Convert distance to similarity score (ChromaDB uses cosine distance)
            similarity = 1 - distance
            
            if similarity >= similarity_threshold:
                similar_docs.append({
                    'content': doc,
                    'metadata': metadata,
                    'similarity': similarity,
                    'rank': i + 1
                })
        
        logger.info(f"Found {len(similar_docs)} similar documents for query")
        return similar_docs
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        count = self.collection.count()
        return {
            'total_documents': count,
            'embedding_model': self.embedding_model_name,
            'persist_directory': self.persist_directory
        }
    
    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        # Delete the collection and recreate it
        self.client.delete_collection("documents")
        self.collection = self.client.create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Collection cleared")
    
    def delete_documents(self, ids: List[str]) -> None:
        """Delete specific documents by IDs."""
        self.collection.delete(ids=ids)
        logger.info(f"Deleted {len(ids)} documents")
