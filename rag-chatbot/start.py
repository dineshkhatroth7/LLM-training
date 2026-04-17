#!/usr/bin/env python3
"""
Startup script for the RAG Chatbot.
This script provides an easy way to start the application with different interfaces.
"""

import os
import sys
import subprocess
import argparse
from config import config

def check_requirements():
    """Check if all required packages are installed."""
    try:
        import fastapi
        import uvicorn
        import streamlit
        import chromadb
        import sentence_transformers
        import openai
        import langchain
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if OpenAI API key is set."""
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key:")
        print("  Windows: set OPENAI_API_KEY=your-api-key-here")
        print("  Linux/Mac: export OPENAI_API_KEY=your-api-key-here")
        return False
    print("✅ OpenAI API key is configured")
    return True

def start_fastapi():
    """Start the FastAPI web interface."""
    print("🚀 Starting FastAPI web interface...")
    print(f"📱 Open your browser to: http://{config.HOST}:{config.PORT}")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--host", config.HOST, 
            "--port", str(config.PORT),
            "--reload" if config.DEBUG else "--no-reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def start_streamlit():
    """Start the Streamlit interface."""
    print("🚀 Starting Streamlit interface...")
    print("📱 Open your browser to: http://localhost:8501")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def run_example():
    """Run the example script."""
    print("🚀 Running example script...")
    try:
        subprocess.run([sys.executable, "example.py"])
    except KeyboardInterrupt:
        print("\n👋 Example stopped")

def main():
    parser = argparse.ArgumentParser(description="RAG Chatbot Startup Script")
    parser.add_argument(
        "interface", 
        choices=["fastapi", "streamlit", "example"], 
        nargs="?",
        default="fastapi",
        help="Interface to start (default: fastapi)"
    )
    parser.add_argument(
        "--skip-checks", 
        action="store_true",
        help="Skip requirement and API key checks"
    )
    
    args = parser.parse_args()
    
    print("🤖 RAG Chatbot Startup")
    print("=" * 50)
    
    # Run checks unless skipped
    if not args.skip_checks:
        if not check_requirements():
            return 1
        
        if not check_api_key():
            return 1
    
    print(f"\n🎯 Starting {args.interface} interface...")
    
    # Start the selected interface
    if args.interface == "fastapi":
        start_fastapi()
    elif args.interface == "streamlit":
        start_streamlit()
    elif args.interface == "example":
        run_example()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
