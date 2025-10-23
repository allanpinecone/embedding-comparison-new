#!/bin/bash

# 🧪 Docker Image Testing Script
# This script helps you test the embedding-comparison Docker image locally

echo "🎬 Embedding Comparison System - Docker Test"
echo "============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if API key is set
if [ -z "$PINECONE_API_KEY" ]; then
    echo "⚠️  PINECONE_API_KEY not set!"
    echo "🔑 Please set your Pinecone API key:"
    echo "   export PINECONE_API_KEY=your-actual-api-key-here"
    echo ""
    read -p "Enter your Pinecone API key: " api_key
    export PINECONE_API_KEY="$api_key"
fi

echo "🚀 Starting Docker container..."
echo "📱 The app will be available at: http://localhost:8504"
echo "⏹️  Press Ctrl+C to stop the container"
echo ""

# Run the container (using port 8504 to avoid any conflicts)
docker run --rm -p 8504:8501 \
  -e PINECONE_API_KEY="$PINECONE_API_KEY" \
  allanpinecone/embedding-comparison:latest
