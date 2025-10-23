"""
Optimized Streamlit UI for Embedding Model Comparison System
Includes options for smaller datasets for faster testing
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import os
from embedding_comparison_system import EmbeddingComparisonSystem, EMBEDDING_MODELS, load_movies_from_csv

# Page configuration
st.set_page_config(
    page_title="Embedding Model Comparison (Optimized)",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .model-comparison {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def clear_session_state():
    """Clear all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def initialize_session_state():
    """Initialize session state variables"""
    if 'system' not in st.session_state:
        st.session_state.system = None
    if 'movies' not in st.session_state:
        st.session_state.movies = None
    if 'indices_created' not in st.session_state:
        st.session_state.indices_created = {}
    if 'model1_results' not in st.session_state:
        st.session_state.model1_results = None
    if 'model2_results' not in st.session_state:
        st.session_state.model2_results = None

def load_system(api_key: str):
    """Load the embedding comparison system with provided API key"""
    if st.session_state.system is None:
        st.session_state.system = EmbeddingComparisonSystem(api_key)

def get_available_dimensions(model_name: str) -> list:
    """Get available dimensions for a specific model"""
    model = EMBEDDING_MODELS[model_name]
    # Only return the model's native dimensions since sentence-transformers models have fixed output dimensions
    return [model.dimensions]

def create_model_config(model_name: str, dimensions: int):
    """Create a model configuration - returns the base model since dimensions are fixed"""
    # Return the base model directly since sentence-transformers models have fixed dimensions
    return EMBEDDING_MODELS[model_name]

def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🎬 Embedding Model Comparison System</h1>', unsafe_allow_html=True)
    st.markdown("**Compare different embedding models and dimensions using Pinecone vector database**")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Clear session state button
        if st.button("🗑️ Clear All Data", help="Clear all session data and start fresh"):
            clear_session_state()
            st.success("✅ Session cleared! Please refresh the page.")
            st.rerun()
        
        # Pinecone API Key input
        pinecone_key = st.text_input(
            "Pinecone API Key",
            value="",
            type="password",
            help="Enter your Pinecone API key or set PINECONE_API_KEY environment variable"
        )
        
        # Load system button
        if st.button("🔧 Initialize System"):
            if not pinecone_key or pinecone_key == "your-pinecone-api-key-here":
                st.error("❌ Please enter a valid Pinecone API key!")
            else:
                with st.spinner("Initializing system..."):
                    load_system(pinecone_key)
                    st.success("✅ System initialized!")
        
        # Dataset size selection
        st.header("📊 Dataset Options")
        dataset_size = st.selectbox(
            "Choose dataset size:",
            ["Full Dataset (3,743 movies)", "Small Test (100 movies)", "Medium Test (500 movies)"],
            help="Smaller datasets for faster testing"
        )
        
        # Load movies button
        if st.button("📁 Load Movies Data"):
            with st.spinner("Loading movies data..."):
                movies = load_movies_from_csv('data/horror_movies_2025.csv')
                
                # Apply dataset size filter
                if "Small Test" in dataset_size:
                    movies = movies[:100]
                    st.info("📊 Using small test dataset (100 movies)")
                elif "Medium Test" in dataset_size:
                    movies = movies[:500]
                    st.info("📊 Using medium test dataset (500 movies)")
                else:
                    st.info("📊 Using full dataset (3,743 movies)")
                
                st.session_state.movies = movies
                st.success(f"✅ Loaded {len(movies)} movies!")
    
    # Main content
    if st.session_state.system is None:
        st.warning("⚠️ Please initialize the system first using the sidebar.")
        return
    
    if st.session_state.movies is None:
        st.warning("⚠️ Please load movies data first using the sidebar.")
        return
    
    # Model selection
    st.header("🤖 Model Selection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model 1")
        model1_name = st.selectbox(
            "Select Model 1:",
            list(EMBEDDING_MODELS.keys()),
            key="model1"
        )
        model1_dimensions = st.selectbox(
            "Dimensions:",
            get_available_dimensions(model1_name),
            key="dim1"
        )
        model1_config = create_model_config(model1_name, model1_dimensions)
        st.info(f"**{model1_config.name}** ({model1_config.dimensions}D) - {model1_config.description}")
    
    with col2:
        st.subheader("Model 2")
        model2_name = st.selectbox(
            "Select Model 2:",
            list(EMBEDDING_MODELS.keys()),
            key="model2"
        )
        model2_dimensions = st.selectbox(
            "Dimensions:",
            get_available_dimensions(model2_name),
            key="dim2"
        )
        model2_config = create_model_config(model2_name, model2_dimensions)
        st.info(f"**{model2_config.name}** ({model2_config.dimensions}D) - {model2_config.description}")
    
    st.info("💡 **Note**: Each embedding model has fixed dimensions that cannot be changed. The dimension dropdown shows the model's native dimensions.")
    
    # Index creation
    st.header("🏗️ Index Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏗️ Create Index 1"):
            with st.spinner("Creating index 1..."):
                index1_name = st.session_state.system.create_index(model1_config, "-ui")
                st.session_state.indices_created['index1'] = {
                    'name': index1_name,
                    'config': model1_config
                }
                st.success(f"✅ Index 1 created: {index1_name}")
    
    with col2:
        if st.button("🏗️ Create Index 2"):
            with st.spinner("Creating index 2..."):
                index2_name = st.session_state.system.create_index(model2_config, "-ui")
                st.session_state.indices_created['index2'] = {
                    'name': index2_name,
                    'config': model2_config
                }
                st.success(f"✅ Index 2 created: {index2_name}")
    
    # Data upload
    if 'index1' in st.session_state.indices_created and 'index2' in st.session_state.indices_created:
        st.header("📤 Data Upload")
        
        if st.button("📤 Upload Movies to Both Indices"):
            with st.spinner("Uploading movies to both indices..."):
                progress_bar = st.progress(0)
                
                # Upload to index 1
                st.session_state.system.embed_and_upload_movies(
                    st.session_state.movies,
                    st.session_state.indices_created['index1']['config'],
                    st.session_state.indices_created['index1']['name']
                )
                progress_bar.progress(50)
                
                # Upload to index 2
                st.session_state.system.embed_and_upload_movies(
                    st.session_state.movies,
                    st.session_state.indices_created['index2']['config'],
                    st.session_state.indices_created['index2']['name']
                )
                progress_bar.progress(100)
                
                st.success("✅ Movies uploaded to both indices!")
    
    # Query and comparison section
    st.header("🔍 Query & Comparison")
    
    # Query input
    query = st.text_input(
        "Enter your movie query:",
        placeholder="e.g., 'scary movies about ghosts and supernatural'",
        value="scary movies about ghosts and supernatural"
    )
    
    top_k = st.slider("Number of results to return:", min_value=3, max_value=20, value=5)
    
    # Search buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Search Model 1"):
            if 'index1' in st.session_state.indices_created:
                with st.spinner("Searching with Model 1..."):
                    results = st.session_state.system.search_movies(
                        query,
                        st.session_state.indices_created['index1']['config'],
                        st.session_state.indices_created['index1']['name'],
                        top_k
                    )
                    st.session_state.model1_results = results
                    st.success("✅ Model 1 search completed!")
            else:
                st.error("❌ Please create Index 1 first!")
    
    with col2:
        if st.button("🔍 Search Model 2"):
            if 'index2' in st.session_state.indices_created:
                with st.spinner("Searching with Model 2..."):
                    results = st.session_state.system.search_movies(
                        query,
                        st.session_state.indices_created['index2']['config'],
                        st.session_state.indices_created['index2']['name'],
                        top_k
                    )
                    st.session_state.model2_results = results
                    st.success("✅ Model 2 search completed!")
            else:
                st.error("❌ Please create Index 2 first!")
    
    # Results display
    if st.session_state.model1_results or st.session_state.model2_results:
        st.header("📊 Comparison Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Model 1: {model1_config.name}")
            if st.session_state.model1_results:
                for i, result in enumerate(st.session_state.model1_results, 1):
                    with st.expander(f"#{i}: {result['title']} (Score: {result['similarity_score']:.3f})"):
                        st.write(f"**Release Date:** {result['release_date']}")
                        st.write(f"**Language:** {result['original_language']}")
                        st.write(f"**Overview:** {result['overview']}")
            else:
                st.warning("No results found for Model 1. Make sure you've uploaded movies to the index and clicked the search button.")
        
        with col2:
            st.subheader(f"Model 2: {model2_config.name}")
            if st.session_state.model2_results:
                for i, result in enumerate(st.session_state.model2_results, 1):
                    with st.expander(f"#{i}: {result['title']} (Score: {result['similarity_score']:.3f})"):
                        st.write(f"**Release Date:** {result['release_date']}")
                        st.write(f"**Language:** {result['original_language']}")
                        st.write(f"**Overview:** {result['overview']}")
            else:
                st.warning("No results found for Model 2. Make sure you've uploaded movies to the index and clicked the search button.")

if __name__ == "__main__":
    main()
