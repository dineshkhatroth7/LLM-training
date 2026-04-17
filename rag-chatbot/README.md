# RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that allows you to upload documents and ask questions about them. The system uses vector embeddings to retrieve relevant document chunks and generates responses using OpenAI's language models.

## Features

- 📁 **Document Upload**: Support for PDF, DOCX, and TXT files
- 🔍 **Semantic Search**: Vector-based similarity search using ChromaDB
- 🤖 **AI Responses**: Powered by OpenAI's GPT models
- 🌐 **Web Interface**: Both FastAPI and Streamlit interfaces
- 📊 **Knowledge Base Stats**: Track uploaded documents and system status
- 🔄 **RAG Toggle**: Switch between RAG and direct LLM responses

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Document      │    │   Vector Store   │    │   LLM Service   │
│   Processor     │───▶│   (ChromaDB)     │───▶│   (OpenAI)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                                │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

1. **Clone or download the project**
   ```bash
   cd rag-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Set your OpenAI API key
   export OPENAI_API_KEY="your-openai-api-key-here"
   
   # Or create a .env file
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   ```

## Usage

### Option 1: FastAPI Web Interface

1. **Start the server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8000`

3. **Upload documents and start chatting!**

### Option 2: Streamlit Interface

1. **Start Streamlit**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8501`

## API Endpoints

- `GET /` - Main chat interface
- `POST /upload` - Upload documents
- `POST /chat` - Send chat messages
- `GET /stats` - Get knowledge base statistics
- `POST /clear` - Clear knowledge base
- `GET /health` - Health check

## Configuration

Edit `config.py` to customize:

- **Chunk Size**: Size of document chunks (default: 1000)
- **Chunk Overlap**: Overlap between chunks (default: 200)
- **Embedding Model**: Sentence transformer model (default: all-MiniLM-L6-v2)
- **LLM Model**: OpenAI model (default: gpt-3.5-turbo)
- **Top K Results**: Number of similar documents to retrieve (default: 3)
- **Similarity Threshold**: Minimum similarity score (default: 0.7)

## How It Works

1. **Document Processing**: Documents are split into chunks using recursive text splitting
2. **Embedding Generation**: Each chunk is converted to vector embeddings using sentence transformers
3. **Vector Storage**: Embeddings are stored in ChromaDB for efficient similarity search
4. **Query Processing**: User queries are converted to embeddings and matched against stored vectors
5. **Context Retrieval**: Most similar document chunks are retrieved as context
6. **Response Generation**: The LLM generates responses using the retrieved context

## Supported File Types

- **PDF**: `.pdf` files
- **Word Documents**: `.docx` files  
- **Text Files**: `.txt` files

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for model downloads

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Make sure you've set the `OPENAI_API_KEY` environment variable
   - Verify your API key is valid and has sufficient credits

2. **Model Download Issues**
   - The first run will download the embedding model (~80MB)
   - Ensure you have a stable internet connection

3. **Memory Issues**
   - Large documents may require more RAM
   - Consider reducing chunk size in `config.py`

4. **File Upload Errors**
   - Check file format is supported (PDF, DOCX, TXT)
   - Ensure files are not corrupted

### Performance Tips

- Use smaller chunk sizes for better precision
- Increase similarity threshold to get more relevant results
- Clear knowledge base periodically to free up memory

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the chatbot!
