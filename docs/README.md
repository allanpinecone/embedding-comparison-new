# 🎬 Embedding Model Comparison System

A comprehensive system for comparing different embedding models and dimensions using Pinecone vector database. This system allows you to evaluate how different embedding models and dimension choices impact search results for movie recommendations.

## 🚀 Features

- **Multiple Embedding Models**: Support for various sentence-transformers models
- **Flexible Dimensions**: Compare models with different embedding dimensions
- **Interactive UI**: Streamlit-based interface with 4 dropdown selectors
- **Real-time Comparison**: Side-by-side comparison of search results
- **Visual Analytics**: Charts and metrics for performance analysis
- **Pinecone Integration**: Seamless vector storage and retrieval

## 📋 Available Models

| Model | Dimensions | Description |
|-------|------------|-------------|
| `all-mpnet-base-v2` | 768 | High-quality sentence embeddings, best for semantic similarity |
| `all-MiniLM-L6-v2` | 384 | Fast and efficient, good balance of speed and quality |
| `all-MiniLM-L12-v2` | 384 | Slightly larger model with better performance |
| `paraphrase-multilingual-MiniLM-L12-v2` | 384 | Multilingual model for cross-language similarity |
| `distilbert-base-nli-mean-tokens` | 768 | DistilBERT model optimized for natural language inference |

## 🛠️ Installation

1. **Clone or download the files**:
   ```bash
   # Ensure you have these files in your directory:
   # - embedding_comparison_system.py
   # - streamlit_app.py
   # - requirements.txt
   # - horror_movies_2025.csv
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Pinecone**:
   - Get your Pinecone API key from [pinecone.io](https://pinecone.io)
   - The system is pre-configured with a demo API key, but you can replace it in the code

## 🎯 Usage

### Option 1: Streamlit Web Interface (Recommended)

1. **Launch the web app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Follow the interface steps**:
   - Initialize the system
   - Load movies data
   - Select two models and their dimensions
   - Create Pinecone indices
   - Upload movies to both indices
   - Enter a query and compare results

### Option 2: Command Line Interface

1. **Run the comparison system directly**:
   ```bash
   python embedding_comparison_system.py
   ```

## 🔧 Configuration

### Model Selection
The system provides 4 dropdown selectors:
- **Model 1**: Choose the first embedding model
- **Dimensions 1**: Select dimensions for Model 1
- **Model 2**: Choose the second embedding model (can be the same as Model 1)
- **Dimensions 2**: Select dimensions for Model 2

### Dimension Options
Each model supports different dimension configurations:
- **Native dimensions**: The model's original embedding size
- **Reduced dimensions**: Common sizes like 128, 256, 384, 512
- **Custom dimensions**: Any size up to the model's maximum

## 📊 Comparison Metrics

The system provides several comparison metrics:

- **Average Similarity Score**: Mean similarity across all results
- **Common Movies**: Number of movies found by both models
- **Overlap Percentage**: Percentage of common results
- **Side-by-side Results**: Direct comparison of top results
- **Performance Visualization**: Charts showing model performance

## 🎬 Example Queries

Try these example queries to test the system:

- "scary movies about ghosts and supernatural"
- "psychological horror films"
- "movies with haunted houses"
- "supernatural thriller movies"
- "horror movies set in isolated locations"

## 📁 File Structure

```
├── embedding_comparison_system.py  # Core comparison system
├── streamlit_app.py               # Streamlit web interface
├── requirements.txt               # Python dependencies
├── README.md                      # This documentation
└── horror_movies_2025.csv         # Movie dataset
```

## 🔍 How It Works

1. **Data Loading**: Movies are loaded from the CSV file
2. **Model Selection**: Choose two embedding models and dimensions
3. **Index Creation**: Create separate Pinecone indices for each model
4. **Embedding Generation**: Generate embeddings using sentence-transformers
5. **Vector Storage**: Store embeddings in Pinecone with metadata
6. **Query Processing**: Generate embeddings for user queries
7. **Similarity Search**: Find similar movies using cosine similarity
8. **Results Comparison**: Compare and analyze results from both models

## 🎯 Use Cases

- **Model Evaluation**: Compare different embedding models for your use case
- **Dimension Analysis**: Understand the impact of embedding dimensions
- **Performance Benchmarking**: Measure model performance on your data
- **Research & Development**: Experiment with different configurations
- **Educational**: Learn about embedding models and vector search

## 🚨 Important Notes

- **API Keys**: Replace the demo Pinecone API key with your own
- **Data Privacy**: Ensure your data complies with privacy requirements
- **Resource Usage**: Embedding generation can be computationally intensive
- **Index Management**: The system creates and manages Pinecone indices automatically

## 🐛 Troubleshooting

### Common Issues:

1. **"CSV file not found"**: Ensure `horror_movies_2025.csv` is in the same directory
2. **"Pinecone API error"**: Check your API key and internet connection
3. **"Model loading error"**: Ensure all dependencies are installed correctly
4. **"Memory issues"**: Reduce batch size or use smaller models for large datasets

### Performance Tips:

- Use smaller models for faster processing
- Reduce dimensions for lower memory usage
- Process data in smaller batches
- Monitor Pinecone index usage

## 📈 Future Enhancements

- Support for more embedding models
- Advanced visualization options
- Batch comparison capabilities
- Export functionality for results
- Custom model integration
- Performance benchmarking tools

## 🤝 Contributing

Feel free to extend the system with:
- New embedding models
- Additional visualization options
- Performance optimizations
- UI improvements
- Documentation enhancements

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit, Pinecone, and sentence-transformers**
