# 🚀 AWS Deployment Guide

## Option 1: AWS App Runner (Recommended)

### Quick Setup:
1. **Push to GitHub** (if not already done)
2. **Go to AWS App Runner Console**
3. **Create Service** → **Source**: GitHub
4. **Connect GitHub** and select your repository
5. **Configure:**
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `streamlit run streamlit_app.py --server.port=8080 --server.address=0.0.0.0 --server.headless=true`
   - **Port**: 8080
6. **Environment Variables:**
   - `PINECONE_API_KEY`: your-actual-api-key-here
7. **Deploy!**

### Cost: ~$25-50/month

---

## Option 2: AWS Elastic Beanstalk

### Setup:
1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB:**
   ```bash
   eb init
   eb create production
   ```

3. **Deploy:**
   ```bash
   eb deploy
   ```

### Cost: ~$30-60/month

---

## Option 3: AWS ECS with Fargate

### Setup:
1. **Build Docker image:**
   ```bash
   docker build -t embedding-comparison .
   ```

2. **Push to ECR:**
   ```bash
   aws ecr create-repository --repository-name embedding-comparison
   docker tag embedding-comparison:latest <account>.dkr.ecr.<region>.amazonaws.com/embedding-comparison:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/embedding-comparison:latest
   ```

3. **Create ECS Task Definition**
4. **Create ECS Service**

### Cost: ~$40-80/month

---

## 🔧 Environment Variables

Set these in your AWS service:

```bash
PINECONE_API_KEY=your-actual-pinecone-api-key-here
```

## 📊 Performance Considerations

- **App Runner**: Best for simple deployments
- **Elastic Beanstalk**: Good for traditional web apps
- **ECS Fargate**: Best for containerized microservices

## 🔒 Security Notes

- Never commit API keys to Git
- Use AWS Secrets Manager for production
- Enable HTTPS in production
- Set up proper IAM roles

## 💰 Cost Optimization

- **App Runner**: Pay-per-use, scales to zero
- **Elastic Beanstalk**: Fixed cost, good for consistent traffic
- **ECS Fargate**: Pay-per-use, good for variable workloads
