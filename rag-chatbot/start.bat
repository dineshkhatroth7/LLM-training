@echo off
echo 🤖 RAG Chatbot Startup
echo =====================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking requirements...
python -c "import fastapi, uvicorn, streamlit, chromadb, sentence_transformers, openai, langchain" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)

REM Check if API key is set
if "%OPENAI_API_KEY%"=="" (
    echo ❌ OPENAI_API_KEY environment variable not set!
    echo Please set your OpenAI API key:
    echo set OPENAI_API_KEY=your-api-key-here
    echo.
    echo Or create a .env file with your API key
    pause
    exit /b 1
)

echo ✅ All checks passed!
echo.

REM Start the application
echo 🚀 Starting RAG Chatbot...
echo Choose interface:
echo 1. FastAPI Web Interface (http://localhost:8000)
echo 2. Streamlit Interface (http://localhost:8501)
echo 3. Example Script
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo Starting FastAPI...
    python start.py fastapi
) else if "%choice%"=="2" (
    echo Starting Streamlit...
    python start.py streamlit
) else if "%choice%"=="3" (
    echo Running example...
    python start.py example
) else (
    echo Invalid choice. Starting FastAPI by default...
    python start.py fastapi
)

pause
