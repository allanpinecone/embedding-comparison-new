# 🔒 Security Guide

## Environment Variables Setup

This system uses environment variables to keep sensitive information secure. **Never commit API keys or secrets to version control.**

### 🔑 Required Environment Variables

#### PINECONE_API_KEY
Your Pinecone API key for vector database operations.

**How to get it:**
1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Sign in to your account
3. Navigate to API Keys section
4. Copy your API key

**How to set it:**

**Option 1: Environment File (Recommended)**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
PINECONE_API_KEY=your-actual-api-key-here
```

**Option 2: Export in Terminal**
```bash
export PINECONE_API_KEY=your-actual-api-key-here
```

**Option 3: Streamlit Secrets (For Production)**
Create `.streamlit/secrets.toml`:
```toml
PINECONE_API_KEY = "your-actual-api-key-here"
```

### 🚨 Security Best Practices

1. **Never commit `.env` files** - They're in `.gitignore`
2. **Use different keys for development/production**
3. **Rotate API keys regularly**
4. **Don't share API keys in chat/email**
5. **Use environment variables in production**

### 🔧 Setup Commands

```bash
# First time setup
./setup.sh

# Set your API key
export PINECONE_API_KEY=your-actual-api-key-here

# Start the system
python start_system.py
```

### ✅ Verification

The system will show an error if the API key is missing or invalid. Check the console output for authentication status.
