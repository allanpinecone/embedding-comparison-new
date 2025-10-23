#!/usr/bin/env python3
"""
Quick launcher for the Embedding Comparison System
"""

import os
import sys
import subprocess

def main():
    print("🎬 Embedding Model Comparison System")
    print("=" * 50)
    print("Repository: embedding-comparison")
    print("Starting the system...")
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("❌ Virtual environment not found!")
        print("🔧 Please run setup first:")
        print("   ./setup.sh")
        return
    
    # Check if API key is set
    api_key = os.getenv('PINECONE_API_KEY')
    if not api_key or api_key == 'your-pinecone-api-key-here':
        print("⚠️  PINECONE_API_KEY not set!")
        print("🔑 Please set your Pinecone API key:")
        print("   export PINECONE_API_KEY=your-actual-api-key-here")
        print("   or see SECURITY.md for more options")
        return
    
    # We're already in the system directory
    # No need to change directories
    
    # Start Streamlit
    print("🚀 Launching web interface...")
    print("📱 Open your browser to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Use the virtual environment python
        venv_python = 'venv/bin/python'
        subprocess.run([venv_python, '-m', 'streamlit', 'run', 'streamlit_app.py'])
    except KeyboardInterrupt:
        print("\n👋 System stopped")

if __name__ == "__main__":
    main()
