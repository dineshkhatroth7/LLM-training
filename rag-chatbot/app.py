from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import os
import tempfile
from typing import List, Optional
import logging
from rag_pipeline import RAGPipeline
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot",
    description="A Retrieval-Augmented Generation chatbot",
    version="1.0.0"
)

# Initialize RAG pipeline
rag_pipeline = RAGPipeline()

# Create templates directory
templates_dir = "templates"
os.makedirs(templates_dir, exist_ok=True)

# Create static directory
static_dir = "static"
os.makedirs(static_dir, exist_ok=True)

# Templates
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main chat interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process documents."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # Save uploaded files temporarily
    temp_files = []
    try:
        for file in files:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
            content = await file.read()
            temp_file.write(content)
            temp_file.close()
            temp_files.append(temp_file.name)
        
        # Process documents
        result = rag_pipeline.add_documents(temp_files)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error uploading files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")
    
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

@app.post("/chat")
async def chat(
    message: str = Form(...),
    use_rag: bool = Form(True)
):
    """Handle chat messages."""
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        result = rag_pipeline.query(message, use_rag=use_rag)
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get knowledge base statistics."""
    try:
        stats = rag_pipeline.get_knowledge_base_stats()
        return JSONResponse(content=stats)
    
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

@app.post("/clear")
async def clear_knowledge_base():
    """Clear the knowledge base."""
    try:
        result = rag_pipeline.clear_knowledge_base()
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error clearing knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing knowledge base: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "RAG Chatbot is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
