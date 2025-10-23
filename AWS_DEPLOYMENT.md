# 🚀 AWS Deployment Guide

## Option 1: AWS App Runner (RECOMMENDED - Easiest)

### Prerequisites
- AWS Account
- GitHub repository connected to AWS
- Pinecone API key

### Steps

#### 1. Create App Runner Service
1. Go to **AWS App Runner** in the AWS Console
2. Click **"Create an App Runner service"**
3. Choose **"Source code repository"**
4. Connect your GitHub account
5. Select repository: `allanpinecone/embedding-comparison-new`
6. Select branch: `main`

#### 2. Configure Build Settings
- **Build type**: Use a buildspec file
- **Buildspec file**: `apprunner.yaml` (already configured)

#### 3. Configure Service Settings
- **Service name**: `embedding-comparison-app`
- **Virtual CPU**: 1 vCPU
- **Virtual memory**: 2 GB
- **Environment variables**:
  - `PINECONE_API_KEY`: Your actual Pinecone API key

#### 4. Deploy
- Click **"Create & deploy"**
- Wait 5-10 minutes for deployment
- Get your app URL: `https://xxxxx.us-east-1.awsapprunner.com`

---

## Option 2: AWS Elastic Beanstalk (Alternative)

### Prerequisites
- AWS CLI installed
- EB CLI installed: `pip install awsebcli`

### Steps

#### 1. Initialize Elastic Beanstalk
```bash
cd "/Users/allan/Documents/GitHub/embedding-comparison-new"
eb init
```

#### 2. Create Environment
```bash
eb create production
```

#### 3. Set Environment Variables
```bash
eb setenv PINECONE_API_KEY=your-actual-api-key-here
```

#### 4. Deploy
```bash
eb deploy
```

---

## Option 3: AWS ECS with Fargate (Advanced)

### Using Docker Hub Image
```bash
# Your image is already on Docker Hub
docker run -d \
  --name embedding-comparison \
  -p 80:8501 \
  -e PINECONE_API_KEY=your-actual-api-key-here \
  allanpinecone/embedding-comparison:latest
```

---

## 🔧 Configuration Files

### apprunner.yaml (Already created)
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
  runtime-version: 3.11
  command: streamlit run streamlit_app.py --server.port=8080 --server.address=0.0.0.0 --server.headless=true
  network:
    port: 8080
  env:
    - name: PINECONE_API_KEY
      value: "your-pinecone-api-key-here"
```

### .ebextensions/ (Already created)
- `01_packages.config` - System packages
- `02_python.config` - Python configuration

---

## 💰 Cost Estimates

### AWS App Runner
- **Free tier**: 2,000 vCPU minutes + 40,000 GB-seconds per month
- **After free tier**: ~$25-50/month for small usage

### AWS Elastic Beanstalk
- **Free tier**: 750 hours of t2.micro instances
- **After free tier**: ~$15-30/month

### AWS ECS Fargate
- **No free tier**
- **Cost**: ~$20-40/month

---

## 🎯 Recommendation

**Use AWS App Runner** - it's the easiest and most cost-effective for your use case!

1. **Zero server management**
2. **Auto-scaling**
3. **Built-in HTTPS**
4. **Easy environment variable management**
5. **Perfect for Streamlit apps**

---

## 🚀 Quick Start (App Runner)

1. **Go to AWS Console** → App Runner
2. **Create service** → Source code repository
3. **Connect GitHub** → Select your repo
4. **Configure** → Use `apprunner.yaml`
5. **Set environment variables** → Add your Pinecone API key
6. **Deploy** → Wait 5-10 minutes
7. **Access your app** → Get the URL!

**That's it!** 🎉
