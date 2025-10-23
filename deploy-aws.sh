#!/bin/bash

# 🚀 AWS Deployment Helper Script
# This script helps you deploy to AWS App Runner

echo "🎬 Embedding Comparison System - AWS Deployment"
echo "=============================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check if user is logged in to AWS
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Not logged in to AWS. Please run:"
    echo "   aws configure"
    exit 1
fi

echo "✅ AWS CLI configured"

# Check if Pinecone API key is set
if [ -z "$PINECONE_API_KEY" ]; then
    echo "⚠️  PINECONE_API_KEY not set!"
    echo "🔑 Please set your Pinecone API key:"
    echo "   export PINECONE_API_KEY=your-actual-api-key-here"
    echo ""
    read -p "Enter your Pinecone API key: " api_key
    export PINECONE_API_KEY="$api_key"
fi

echo "✅ Pinecone API key configured"

echo ""
echo "🚀 Ready to deploy to AWS App Runner!"
echo ""
echo "📋 Next steps:"
echo "1. Go to AWS Console → App Runner"
echo "2. Create service → Source code repository"
echo "3. Connect GitHub → Select your repo"
echo "4. Configure → Use apprunner.yaml"
echo "5. Set environment variables:"
echo "   - PINECONE_API_KEY: $PINECONE_API_KEY"
echo "6. Deploy → Wait 5-10 minutes"
echo "7. Access your app at the provided URL!"
echo ""
echo "📖 For detailed instructions, see AWS_DEPLOYMENT.md"
echo ""
echo "🎉 Happy deploying!"
