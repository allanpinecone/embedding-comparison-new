# 🔧 AWS App Runner Environment Variables Guide

## 📍 **Where to Find Environment Variables in AWS App Runner**

### **Step-by-Step Instructions:**

1. **Go to AWS Console** → **App Runner**
2. **Click on your service name** (e.g., `embedding-comparison-app`)
3. **Click the "Configuration" tab** (next to "Overview", "Logs", etc.)
4. **Scroll down to "Environment variables"** section
5. **Click "Edit"** button next to "Environment variables"
6. **Add new environment variable**:
   - **Key**: `PINECONE_API_KEY`
   - **Value**: Your actual Pinecone API key
7. **Click "Save"**
8. **Click "Deploy"** to apply changes

### **Visual Guide:**
```
AWS Console → App Runner → [Your Service] → Configuration → Environment variables → Edit
```

---

## 🎯 **Alternative: Use AWS CLI**

If you prefer command line:

```bash
# Set environment variable
aws apprunner update-service \
  --service-arn "arn:aws:apprunner:region:account:service/your-service-name" \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "your-image",
      "ImageConfiguration": {
        "Port": "8080",
        "RuntimeEnvironmentVariables": {
          "PINECONE_API_KEY": "your-actual-api-key-here"
        }
      }
    }
  }'
```

---

## 🔍 **Troubleshooting**

### **If you can't find the Environment Variables section:**

1. **Make sure you're in the right place**:
   - AWS Console → App Runner → [Your Service Name] → Configuration
2. **Check if your service is still deploying**:
   - Wait for deployment to complete
3. **Try refreshing the page**
4. **Make sure you have the right permissions**

### **If the Environment Variables section is missing:**

1. **Your service might be using a different source** (not source code repository)
2. **Try creating a new service** with the correct configuration
3. **Make sure you selected "Source code repository"** when creating the service

---

## 🚀 **Quick Test**

After setting the environment variable:

1. **Go to your app URL** (provided by App Runner)
2. **Check if the API key input is empty** (it should be)
3. **Enter your Pinecone API key** in the UI
4. **Test the functionality**

---

## 📝 **Notes**

- **Environment variables are set at the service level**
- **Changes require a new deployment**
- **The app will restart when you save changes**
- **Make sure to use the exact key name**: `PINECONE_API_KEY`

---

## 🆘 **Still Having Issues?**

If you're still not seeing the Environment Variables section:

1. **Check your App Runner service type**:
   - Should be "Source code repository"
   - Not "Container image"
2. **Verify your service is fully created**
3. **Try the AWS CLI method above**
4. **Contact AWS support if needed**

The Environment Variables section should be visible in the Configuration tab of your App Runner service! 🎬✨
