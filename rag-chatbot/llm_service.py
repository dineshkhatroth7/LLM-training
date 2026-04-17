import openai
from typing import List, Dict, Any, Optional
import logging
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """Handles interactions with OpenAI's language models."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model = model
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Set the API key
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        logger.info(f"LLM service initialized with model: {model}")
    
    def generate_response(self, messages: List[Dict[str, str]], max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate a response using the language model."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error while generating a response. Please try again."
    
    def create_rag_prompt(self, query: str, context_docs: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Create a prompt for RAG-based response generation."""
        # Format context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1} (Source: {doc['metadata'].get('filename', 'Unknown')}):\n{doc['content']}"
            for i, doc in enumerate(context_docs)
        ])
        
        system_prompt = """You are a helpful AI assistant that answers questions based on the provided context documents. 
        Use the information from the context to provide accurate and helpful responses. 
        If the context doesn't contain enough information to answer the question, say so clearly.
        Always cite which document(s) you used for your answer when possible."""
        
        user_prompt = f"""Context Documents:
{context}

Question: {query}

Please provide a comprehensive answer based on the context documents above."""
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def generate_rag_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate a RAG-based response using retrieved context."""
        if not context_docs:
            return "I don't have enough information in my knowledge base to answer this question. Please try uploading some documents first."
        
        # Create RAG prompt
        messages = self.create_rag_prompt(query, context_docs)
        
        # Generate response
        return self.generate_response(messages)
    
    def generate_conversation_response(self, conversation_history: List[Dict[str, str]], query: str) -> str:
        """Generate a response considering conversation history."""
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Maintain context from the conversation history and provide relevant responses."}
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        return self.generate_response(messages)
