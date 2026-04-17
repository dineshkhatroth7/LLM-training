import os
from typing import Optional

class Config:
    # OpenAI API Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Vector Database Configuration
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    
    # Document Processing Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Model Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    # RAG Configuration
    TOP_K_RESULTS: int = 3
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

config = Config()
