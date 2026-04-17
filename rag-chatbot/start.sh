#!/bin/bash

echo "🤖 RAG Chatbot Startup"
echo "====================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check if requirements are installed
echo "Checking requirements..."
python3 -c "import fastapi, uvicorn, streamlit, chromadb, sentence_transformers, openai, langchain" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing requirements..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install requirements"
        exit 1
    fi
fi

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY environment variable not set!"
    echo "Please set your OpenAI API key:"
    echo "export OPENAI_API_KEY=your-api-key-here"
    echo ""
    echo "Or create a .env file with your API key"
    exit 1
fi

echo "✅ All checks passed!"
echo ""

# Start the application
echo "🚀 Starting RAG Chatbot..."
echo "Choose interface:"
echo "1. FastAPI Web Interface (http://localhost:8000)"
echo "2. Streamlit Interface (http://localhost:8501)"
echo "3. Example Script"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Starting FastAPI..."
        python3 start.py fastapi
        ;;
    2)
        echo "Starting Streamlit..."
        python3 start.py streamlit
        ;;
    3)
        echo "Running example..."
        python3 start.py example
        ;;
    *)
        echo "Invalid choice. Starting FastAPI by default..."
        python3 start.py fastapi
        ;;
esac
