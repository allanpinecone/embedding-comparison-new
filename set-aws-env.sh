#!/bin/bash

# 🔧 AWS App Runner Environment Variable Setter
# This script helps you set the PINECONE_API_KEY environment variable

echo "🔧 AWS App Runner Environment Variable Setter"
echo "============================================="

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

# Get Pinecone API key
if [ -z "$PINECONE_API_KEY" ]; then
    echo "🔑 Please enter your Pinecone API key:"
    read -p "PINECONE_API_KEY: " api_key
    export PINECONE_API_KEY="$api_key"
fi

echo "✅ Pinecone API key: ${PINECONE_API_KEY:0:10}..."

# List App Runner services
echo ""
echo "📋 Available App Runner services:"
aws apprunner list-services --query 'ServiceSummaryList[].{Name:ServiceName,Arn:ServiceArn}' --output table

echo ""
echo "🔧 To set the environment variable, you have two options:"
echo ""
echo "1. 🖥️  AWS Console (Recommended):"
echo "   - Go to AWS Console → App Runner"
echo "   - Click your service → Configuration"
echo "   - Edit Environment variables"
echo "   - Add: PINECONE_API_KEY = $PINECONE_API_KEY"
echo ""
echo "2. 💻 AWS CLI (Advanced):"
echo "   - Get your service ARN from the table above"
echo "   - Run the command below with your service ARN"
echo ""
echo "📝 AWS CLI Command (replace YOUR_SERVICE_ARN):"
echo "aws apprunner update-service \\"
echo "  --service-arn YOUR_SERVICE_ARN \\"
echo "  --source-configuration '{\"ImageRepository\":{\"ImageIdentifier\":\"your-image\",\"ImageConfiguration\":{\"Port\":\"8080\",\"RuntimeEnvironmentVariables\":{\"PINECONE_API_KEY\":\"$PINECONE_API_KEY\"}}}}'"
echo ""
echo "🎯 The easiest way is through the AWS Console!"
echo "📖 For detailed instructions, see AWS_ENVIRONMENT_VARIABLES.md"
