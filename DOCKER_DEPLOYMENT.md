# 🐳 Docker Deployment Guide

## 🚀 **Your Docker Image is Ready!**

**Docker Hub Repository:** `allanpinecone/embedding-comparison`

**Available Tags:**
- `latest` - Latest version
- `v1.0` - Version 1.0

---

## 🏃‍♂️ **Quick Start**

### **Run Locally:**
```bash
# Pull the image
docker pull allanpinecone/embedding-comparison:latest

# Run with environment variables
docker run -p 8501:8501 \
  -e PINECONE_API_KEY=your-actual-api-key-here \
  allanpinecone/embedding-comparison:latest
```

### **Access the Application:**
- **Local URL:** http://localhost:8501
- **Network URL:** http://your-ip:8501

---

## 🔧 **Deployment Options**

### **1. Docker Compose (Recommended)**
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  embedding-comparison:
    image: allanpinecone/embedding-comparison:latest
    ports:
      - "8501:8501"
    environment:
      - PINECONE_API_KEY=${PINECONE_API_KEY}
    restart: unless-stopped
```

**Run:**
```bash
docker-compose up -d
```

### **2. AWS ECS with Fargate**
```bash
# Create ECS task definition using the image
# allanpinecone/embedding-comparison:latest
```

### **3. Google Cloud Run**
```bash
# Deploy to Cloud Run
gcloud run deploy embedding-comparison \
  --image allanpinecone/embedding-comparison:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PINECONE_API_KEY=your-key
```

### **4. Azure Container Instances**
```bash
# Deploy to Azure Container Instances
az container create \
  --resource-group myResourceGroup \
  --name embedding-comparison \
  --image allanpinecone/embedding-comparison:latest \
  --ports 8501 \
  --environment-variables PINECONE_API_KEY=your-key
```

---

## 🔒 **Environment Variables**

**Required:**
- `PINECONE_API_KEY` - Your Pinecone API key

**Optional:**
- `STREAMLIT_SERVER_PORT` - Port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS` - Address (default: 0.0.0.0)

---

## 📊 **Resource Requirements**

**Minimum:**
- **CPU:** 1 vCPU
- **Memory:** 2 GB RAM
- **Storage:** 6 GB

**Recommended:**
- **CPU:** 2 vCPU
- **Memory:** 4 GB RAM
- **Storage:** 10 GB

---

## 🚀 **Production Deployment**

### **AWS ECS Fargate:**
1. **Create ECS Cluster**
2. **Create Task Definition** with the image
3. **Create Service** with load balancer
4. **Set Environment Variables**

### **Kubernetes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: embedding-comparison
spec:
  replicas: 1
  selector:
    matchLabels:
      app: embedding-comparison
  template:
    metadata:
      labels:
        app: embedding-comparison
    spec:
      containers:
      - name: embedding-comparison
        image: allanpinecone/embedding-comparison:latest
        ports:
        - containerPort: 8501
        env:
        - name: PINECONE_API_KEY
          valueFrom:
            secretKeyRef:
              name: pinecone-secret
              key: api-key
---
apiVersion: v1
kind: Service
metadata:
  name: embedding-comparison-service
spec:
  selector:
    app: embedding-comparison
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

---

## 🔄 **Updates**

**Pull Latest Version:**
```bash
docker pull allanpinecone/embedding-comparison:latest
```

**Update Running Container:**
```bash
docker-compose pull
docker-compose up -d
```

---

## 🐛 **Troubleshooting**

**Check Container Logs:**
```bash
docker logs <container-id>
```

**Debug Container:**
```bash
docker run -it --rm allanpinecone/embedding-comparison:latest /bin/bash
```

**Health Check:**
```bash
curl http://localhost:8501/_stcore/health
```

---

## 📈 **Monitoring**

**Container Stats:**
```bash
docker stats <container-id>
```

**Resource Usage:**
```bash
docker exec <container-id> top
```

---

## 🎯 **Next Steps**

1. **Choose your deployment platform**
2. **Set up environment variables**
3. **Deploy the container**
4. **Configure monitoring**
5. **Set up CI/CD pipeline**

Your embedding comparison system is now ready for production deployment! 🎬✨🐳
