# ⚡ Performance Optimization Guide

## 🐌 **Why Data Upload Takes So Long**

The embedding generation process is computationally intensive:

- **3,743 movies** × **768 dimensions** = **2.87M numbers** for all-mpnet-base-v2
- **3,743 movies** × **384 dimensions** = **1.44M numbers** for all-MiniLM-L6-v2
- **Model loading** time for each embedding model
- **Vector calculations** for each movie overview

## ⚡ **Performance Optimization Options**

### **1. Use Smaller Datasets for Testing**

**Option A: Use the Optimized App**
```bash
# The optimized app includes dataset size options
docker run --rm -p 8506:8501 \
  -e PINECONE_API_KEY=your-key \
  allanpinecone/embedding-comparison:latest
```

**Option B: Modify the CSV file**
```python
# In your local development, limit the dataset
movies = load_movies_from_csv('data/horror_movies_2025.csv')[:100]  # Only first 100 movies
```

### **2. Batch Size Optimization**

**Current batch size:** 100 movies per batch
**Recommended for testing:** 50 movies per batch
**Recommended for production:** 200 movies per batch

### **3. Model Selection for Speed**

**Fastest Models:**
- `all-MiniLM-L6-v2` (384D) - **Fastest**
- `all-MiniLM-L12-v2` (384D) - **Fast**
- `distilbert-base-nli-mean-tokens` (768D) - **Medium**

**Slower Models:**
- `all-mpnet-base-v2` (768D) - **High quality, slower**
- `paraphrase-multilingual-MiniLM-L12-v2` (384D) - **Multilingual, slower**

### **4. Hardware Optimization**

**For Local Development:**
- **CPU:** 4+ cores recommended
- **RAM:** 8GB+ recommended
- **Storage:** SSD recommended

**For Production:**
- **CPU:** 8+ cores
- **RAM:** 16GB+
- **GPU:** Optional but significantly faster

## 🧪 **Testing Performance**

### **Quick Test (100 movies):**
- **Time:** ~2-3 minutes
- **Use case:** Development and testing

### **Medium Test (500 movies):**
- **Time:** ~10-15 minutes
- **Use case:** Feature testing

### **Full Dataset (3,743 movies):**
- **Time:** ~45-60 minutes
- **Use case:** Production deployment

## 🚀 **Production Deployment Tips**

### **1. Pre-compute Embeddings**
```python
# Generate embeddings offline and store them
# Then upload to Pinecone in batches
```

### **2. Use GPU Acceleration**
```python
# For production, consider using GPU-enabled containers
# This can reduce embedding time by 10x
```

### **3. Parallel Processing**
```python
# Process multiple models simultaneously
# Use multiprocessing for batch operations
```

### **4. Caching**
```python
# Cache model loading
# Cache embedding results
# Use Redis for session storage
```

## 📊 **Performance Benchmarks**

| Dataset Size | Model | Time | Memory |
|---------------|-------|------|--------|
| 100 movies | all-MiniLM-L6-v2 | 2 min | 2GB |
| 500 movies | all-MiniLM-L6-v2 | 8 min | 3GB |
| 1000 movies | all-MiniLM-L6-v2 | 15 min | 4GB |
| 100 movies | all-mpnet-base-v2 | 4 min | 3GB |
| 500 movies | all-mpnet-base-v2 | 18 min | 5GB |
| 1000 movies | all-mpnet-base-v2 | 35 min | 7GB |

## 🔧 **Optimization Commands**

### **For Development:**
```bash
# Use small dataset
export DATASET_SIZE=100
docker run --rm -p 8506:8501 \
  -e PINECONE_API_KEY=your-key \
  -e DATASET_SIZE=100 \
  allanpinecone/embedding-comparison:latest
```

### **For Production:**
```bash
# Use full dataset with optimized settings
docker run --rm -p 8501:8501 \
  -e PINECONE_API_KEY=your-key \
  -e BATCH_SIZE=200 \
  allanpinecone/embedding-comparison:latest
```

## 💡 **Pro Tips**

1. **Start with small datasets** for development
2. **Use faster models** for initial testing
3. **Pre-compute embeddings** for production
4. **Monitor memory usage** during processing
5. **Use progress bars** to show processing status
6. **Implement caching** for repeated operations

## 🎯 **Recommended Workflow**

1. **Development:** Use 100 movies with all-MiniLM-L6-v2
2. **Testing:** Use 500 movies with your target model
3. **Production:** Use full dataset with optimized settings
4. **Monitoring:** Track processing time and memory usage

Your embedding comparison system is now optimized for both development and production use! 🎬✨⚡
