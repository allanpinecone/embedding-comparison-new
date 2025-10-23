#!/bin/bash
# Setup script for Embedding Model Comparison System

echo "🎬 Embedding Model Comparison System Setup"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ Error: Please run this script from the embedding-comparison directory"
    echo "   Current directory: $(pwd)"
    exit 1
fi

echo "📁 Setting up virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the system:"
echo "   python start_system.py"
echo ""
echo "📖 For documentation:"
echo "   See docs/"
