# 🔧 AWS App Runner Troubleshooting Guide

## ❌ **Error: "The specified runtime version is not supported"**

### **Problem:**
```
[AppRunner] Failed to build your application source code. 
Reason: The specified runtime version is not supported. 
Refer to the Release information in the App Runner Developer guide for supported runtime versions.
```

### **Solution:**

AWS App Runner has specific Python runtime version requirements. Here are the supported versions:

#### **✅ Supported Python Versions:**
- **Python 3.8** (recommended for compatibility)
- **Python 3.9** 
- **Python 3.10**

#### **❌ NOT Supported:**
- **Python 3.11** (too new)
- **Python 3.7** (too old)

---

## 🔧 **How to Fix:**

### **Option 1: Update apprunner.yaml (Recommended)**

Replace your current `apprunner.yaml` with one of these:

#### **For Python 3.10:**
```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Installing dependencies..."
      - pip install -r requirements.txt
      - echo "Build completed"
run:
  runtime-version: 3.10
  command: streamlit run streamlit_app_optimized.py --server.port=8080 --server.address=0.0.0.0 --server.headless=true
  network:
    port: 8080
```

#### **For Python 3.9:**
```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Installing dependencies..."
      - pip install -r requirements.txt
      - echo "Build completed"
run:
  runtime-version: 3.9
  command: streamlit run streamlit_app_optimized.py --server.port=8080 --server.address=0.0.0.0 --server.headless=true
  network:
    port: 8080
```

#### **For Python 3.8 (Most Compatible):**
```yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Installing dependencies..."
      - pip install -r requirements.txt
      - echo "Build completed"
run:
  runtime-version: 3.8
  command: streamlit run streamlit_app_optimized.py --server.port=8080 --server.address=0.0.0.0 --server.headless=true
  network:
    port: 8080
```

### **Option 2: Use Alternative Configuration Files**

I've created alternative configuration files:
- `apprunner-python39.yaml` - For Python 3.9
- `apprunner-python38.yaml` - For Python 3.8

To use them:
1. **Rename** your current `apprunner.yaml` to `apprunner-old.yaml`
2. **Rename** one of the alternative files to `apprunner.yaml`
3. **Commit and push** to GitHub
4. **Redeploy** in AWS App Runner

---

## 🚀 **Step-by-Step Fix:**

1. **Update the configuration file**:
   ```bash
   cd "/Users/allan/Documents/GitHub/embedding-comparison-new"
   # Edit apprunner.yaml to use runtime-version: 3.10 (or 3.9, or 3.8)
   ```

2. **Commit the changes**:
   ```bash
   git add apprunner.yaml
   git commit -m "Fix Python runtime version for AWS App Runner"
   git push origin main
   ```

3. **Redeploy in AWS App Runner**:
   - Go to your App Runner service
   - Click "Deploy" or "Redeploy"
   - Wait for the build to complete

---

## 🔍 **Alternative: Use Docker Image Instead**

If you continue having issues with source code deployment, you can use your Docker image:

### **Docker-based Deployment:**

1. **Go to AWS App Runner**
2. **Create new service** → **Container image**
3. **Use your Docker Hub image**: `allanpinecone/embedding-comparison:latest`
4. **Set environment variables**:
   - `PINECONE_API_KEY`: Your actual API key
5. **Deploy**

This bypasses the Python runtime version issue entirely!

---

## 📋 **Quick Reference:**

| Python Version | Status | Recommendation |
|----------------|--------|----------------|
| 3.8            | ✅ Supported | Most compatible |
| 3.9            | ✅ Supported | Good choice |
| 3.10           | ✅ Supported | Modern choice |
| 3.11           | ❌ Not supported | Use 3.10 instead |

---

## 🎯 **Recommended Action:**

**Use Python 3.10** - it's the most recent supported version and should work with all your dependencies.

Update your `apprunner.yaml` to:
```yaml
runtime-version: 3.10
```

Then commit, push, and redeploy! 🚀
