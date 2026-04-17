#!/usr/bin/env python3
"""
Example script to test the RAG pipeline without the web interface.
"""

import os
from rag_pipeline import RAGPipeline
from config import config

def main():
    print("🤖 RAG Chatbot Example")
    print("=" * 50)
    
    # Initialize RAG pipeline
    print("Initializing RAG pipeline...")
    rag = RAGPipeline()
    
    # Check if OpenAI API key is set
    if not config.OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print("✅ RAG pipeline initialized successfully!")
    
    # Example: Add some sample documents (if they exist)
    sample_docs = [
        "sample_document.txt",
        "example.pdf",
        "test.docx"
    ]
    
    existing_docs = [doc for doc in sample_docs if os.path.exists(doc)]
    
    if existing_docs:
        print(f"\n📁 Found {len(existing_docs)} sample documents:")
        for doc in existing_docs:
            print(f"  - {doc}")
        
        print("\nProcessing documents...")
        result = rag.add_documents(existing_docs)
        
        if result['success']:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['message']}")
    else:
        print("\n📁 No sample documents found.")
        print("You can create a sample document or upload files via the web interface.")
    
    # Get knowledge base stats
    stats = rag.get_knowledge_base_stats()
    print(f"\n📊 Knowledge Base Stats:")
    print(f"  - Total documents: {stats['total_documents']}")
    print(f"  - Embedding model: {stats['embedding_model']}")
    
    # Interactive chat loop
    print("\n💬 Interactive Chat (type 'quit' to exit)")
    print("=" * 50)
    
    while True:
        try:
            # Get user input
            query = input("\nYou: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            # Process query
            print("\n🤖 Bot: ", end="", flush=True)
            result = rag.query(query)
            
            if result['success']:
                print(result['response'])
                
                # Show sources if available
                if result.get('sources'):
                    print(f"\n📚 Sources:")
                    for source in result['sources']:
                        print(f"  - {source['filename']} (Similarity: {source['similarity']:.1%})")
                
                print(f"\n🔧 Method: {result.get('method', 'unknown').upper()}")
            else:
                print(f"❌ {result['response']}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
