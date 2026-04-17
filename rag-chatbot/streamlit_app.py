import streamlit as st
import os
import tempfile
from typing import List
from rag_pipeline import RAGPipeline
from config import config

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize RAG pipeline
@st.cache_resource
def get_rag_pipeline():
    return RAGPipeline()

rag_pipeline = get_rag_pipeline()

# Sidebar
st.sidebar.title("🤖 RAG Chatbot")
st.sidebar.markdown("Upload documents and ask questions powered by Retrieval-Augmented Generation")

# RAG Mode Toggle
rag_mode = st.sidebar.toggle("RAG Mode", value=True, help="Enable RAG for document-based responses")

# File Upload
st.sidebar.subheader("📁 Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Choose files",
    type=['pdf', 'docx', 'txt'],
    accept_multiple_files=True,
    help="Upload PDF, DOCX, or TXT files"
)

if uploaded_files:
    if st.sidebar.button("Process Documents"):
        with st.spinner("Processing documents..."):
            # Save uploaded files temporarily
            temp_files = []
            try:
                for uploaded_file in uploaded_files:
                    # Create temporary file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1])
                    temp_file.write(uploaded_file.getvalue())
                    temp_file.close()
                    temp_files.append(temp_file.name)
                
                # Process documents
                result = rag_pipeline.add_documents(temp_files)
                
                if result['success']:
                    st.sidebar.success(f"✅ {result['message']}")
                else:
                    st.sidebar.error(f"❌ {result['message']}")
                
            except Exception as e:
                st.sidebar.error(f"Error processing files: {str(e)}")
            
            finally:
                # Clean up temporary files
                for temp_file in temp_files:
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

# Knowledge Base Stats
st.sidebar.subheader("📊 Knowledge Base")
try:
    stats = rag_pipeline.get_knowledge_base_stats()
    st.sidebar.metric("Documents", stats['total_documents'])
    st.sidebar.text(f"Model: {stats['embedding_model']}")
except:
    st.sidebar.text("No documents loaded")

# Clear Knowledge Base
if st.sidebar.button("🗑️ Clear Knowledge Base", type="secondary"):
    result = rag_pipeline.clear_knowledge_base()
    if result['success']:
        st.sidebar.success("Knowledge base cleared")
        st.rerun()
    else:
        st.sidebar.error(f"Error: {result['message']}")

# Main Chat Interface
st.title("💬 Chat with RAG Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I'm your RAG-powered chatbot. Upload some documents and ask me questions about them!"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display sources if available
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.text(f"• {source['filename']} (Similarity: {source['similarity']:.1%})")

# Chat input
if prompt := st.chat_input("Ask me anything about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = rag_pipeline.query(prompt, use_rag=rag_mode)
                
                if result['success']:
                    response = result['response']
                    sources = result.get('sources', [])
                    method = result.get('method', 'unknown')
                    
                    # Display response
                    st.markdown(response)
                    
                    # Display sources if available
                    if sources:
                        with st.expander("📚 Sources"):
                            for source in sources:
                                st.text(f"• {source['filename']} (Similarity: {source['similarity']:.1%})")
                    
                    # Display method used
                    method_emoji = "🧠" if method == "rag" else "🤖" if method == "direct_llm" else "❓"
                    st.caption(f"{method_emoji} Method: {method.upper()}")
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": sources
                    })
                else:
                    error_msg = f"❌ {result['response']}"
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.markdown("**RAG Chatbot** - Powered by LangChain, ChromaDB, and OpenAI")
