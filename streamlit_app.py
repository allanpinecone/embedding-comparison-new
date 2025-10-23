"""
Streamlit UI for Embedding Model Comparison System
Interactive interface for comparing different embedding models and dimensions
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
    page_title="Embedding Model Comparison",
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
    if 'movies_loaded' not in st.session_state:
        st.session_state.movies_loaded = False
    if 'indices_created' not in st.session_state:
        st.session_state.indices_created = {}
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = None

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
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🎬 Embedding Model Comparison System</h1>', unsafe_allow_html=True)
    st.markdown("Compare different embedding models and dimensions for movie recommendation systems")
    
    # Sidebar for configuration
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
        
        # Data loading section
        st.header("📁 Data Management")
        
        if st.button("📥 Load Movies Data"):
            with st.spinner("Loading movies from CSV..."):
                try:
                    movies = load_movies_from_csv('data/horror_movies_2025.csv')
                    st.session_state.movies = movies
                    st.session_state.movies_loaded = True
                    st.success(f"Loaded {len(movies)} movies!")
                except FileNotFoundError:
                    st.error("CSV file not found. Please ensure 'data/horror_movies_2025.csv' is in the current directory.")
                except Exception as e:
                    st.error(f"Error loading movies: {e}")
        
        if st.session_state.movies_loaded:
            st.success(f"✅ {len(st.session_state.movies)} movies loaded")
    
    # Main content area
    if st.session_state.system is None:
        st.warning("⚠️ Please initialize the system first using the sidebar.")
        return
    
    if not st.session_state.movies_loaded:
        st.warning("⚠️ Please load the movies data first using the sidebar.")
        return
    
    # Status indicator
    st.subheader("📊 System Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.system:
            st.success("✅ System Initialized")
        else:
            st.error("❌ System Not Initialized")
    
    with col2:
        if st.session_state.movies_loaded:
            st.success("✅ Movies Loaded")
        else:
            st.error("❌ Movies Not Loaded")
    
    with col3:
        if len(st.session_state.indices_created) >= 2:
            st.success("✅ Indices Created")
        else:
            st.warning(f"⚠️ {len(st.session_state.indices_created)}/2 Indices Created")
    
    with col4:
        if len(st.session_state.indices_created) >= 2:
            st.success("✅ Ready to Search")
        else:
            st.warning("⚠️ Create Indices First")
    
    # Model selection section
    st.header("🔍 Model Selection")
    st.info("💡 **Note**: Each embedding model has fixed dimensions that cannot be changed. The dimension dropdown shows the model's native dimensions.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model 1")
        model1_name = st.selectbox(
            "Select Model 1:",
            options=list(EMBEDDING_MODELS.keys()),
            key="model1_select"
        )
        
        if model1_name:
            model1_dims = st.selectbox(
                "Dimensions for Model 1:",
                options=get_available_dimensions(model1_name),
                key="model1_dims"
            )
            
            model1_config = create_model_config(model1_name, model1_dims)
            st.info(f"**{model1_config.name}** ({model1_config.dimensions}D) - {model1_config.description}")
    
    with col2:
        st.subheader("Model 2")
        model2_name = st.selectbox(
            "Select Model 2:",
            options=list(EMBEDDING_MODELS.keys()),
            key="model2_select"
        )
        
        if model2_name:
            model2_dims = st.selectbox(
                "Dimensions for Model 2:",
                options=get_available_dimensions(model2_name),
                key="model2_dims"
            )
            
            model2_config = create_model_config(model2_name, model2_dims)
            st.info(f"**{model2_config.name}** ({model2_config.dimensions}D) - {model2_config.description}")
    
    # Index management
    st.header("🗄️ Index Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏗️ Create Index 1", key="create_index1"):
            if 'model1_name' in locals() and 'model1_dims' in locals():
                with st.spinner(f"Creating index for {model1_config.name}..."):
                    index1_name = st.session_state.system.create_index(model1_config, "-ui")
                    st.session_state.indices_created['index1'] = {
                        'name': index1_name,
                        'config': model1_config
                    }
                    st.success(f"Index 1 created: {index1_name}")
            else:
                st.error("Please select Model 1 first")
    
    with col2:
        if st.button("🏗️ Create Index 2", key="create_index2"):
            if 'model2_name' in locals() and 'model2_dims' in locals():
                with st.spinner(f"Creating index for {model2_config.name}..."):
                    index2_name = st.session_state.system.create_index(model2_config, "-ui")
                    st.session_state.indices_created['index2'] = {
                        'name': index2_name,
                        'config': model2_config
                    }
                    st.success(f"Index 2 created: {index2_name}")
            else:
                st.error("Please select Model 2 first")
    
    # Data upload section
    if len(st.session_state.indices_created) == 2:
        st.header("📤 Data Upload")
        
        if st.button("🚀 Upload Movies to Both Indices"):
            with st.spinner("Uploading movies to both indices..."):
                progress_bar = st.progress(0)
                
                # Upload to index 1
                st.write("Uploading to Index 1...")
                st.session_state.system.embed_and_upload_movies(
                    st.session_state.movies,
                    st.session_state.indices_created['index1']['config'],
                    st.session_state.indices_created['index1']['name']
                )
                progress_bar.progress(50)
                
                # Upload to index 2
                st.write("Uploading to Index 2...")
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
    
    # Comparison buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔍 Search Model 1", key="search1"):
            if 'index1' in st.session_state.indices_created and query:
                with st.spinner("Searching with Model 1..."):
                    results1 = st.session_state.system.search_movies(
                        query,
                        st.session_state.indices_created['index1']['config'],
                        st.session_state.indices_created['index1']['name'],
                        top_k
                    )
                    st.session_state.model1_results = results1
                    st.success(f"Found {len(results1)} results with Model 1")
    
    with col2:
        if st.button("🔍 Search Model 2", key="search2"):
            if 'index2' in st.session_state.indices_created and query:
                with st.spinner("Searching with Model 2..."):
                    results2 = st.session_state.system.search_movies(
                        query,
                        st.session_state.indices_created['index2']['config'],
                        st.session_state.indices_created['index2']['name'],
                        top_k
                    )
                    st.session_state.model2_results = results2
                    st.success(f"Found {len(results2)} results with Model 2")
    
    with col3:
        if st.button("⚖️ Compare Models", key="compare"):
            if (len(st.session_state.indices_created) == 2 and 
                'model1_results' in st.session_state and 
                'model2_results' in st.session_state):
                
                with st.spinner("Comparing models..."):
                    comparison = st.session_state.system.compare_models(
                        query,
                        st.session_state.indices_created['index1']['config'],
                        st.session_state.indices_created['index2']['config'],
                        st.session_state.indices_created['index1']['name'],
                        st.session_state.indices_created['index2']['name'],
                        top_k
                    )
                    st.session_state.comparison_results = comparison
                    st.success("Comparison completed!")
    
    # Display results
    if 'model1_results' in st.session_state:
        st.header("📊 Model 1 Results")
        results1_df = pd.DataFrame(st.session_state.model1_results)
        if not results1_df.empty:
            st.dataframe(results1_df[['title', 'release_date', 'similarity_score']], use_container_width=True)
        else:
            st.warning("No results found for Model 1. Make sure you've uploaded movies to the index and clicked the search button.")
    
    if 'model2_results' in st.session_state:
        st.header("📊 Model 2 Results")
        results2_df = pd.DataFrame(st.session_state.model2_results)
        if not results2_df.empty:
            st.dataframe(results2_df[['title', 'release_date', 'similarity_score']], use_container_width=True)
        else:
            st.warning("No results found for Model 2. Make sure you've uploaded movies to the index and clicked the search button.")
    
    # Comparison visualization
    if st.session_state.comparison_results:
        st.header("📈 Comparison Analysis")
        
        comparison = st.session_state.comparison_results
        
        # Metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Model 1 Avg Similarity",
                f"{comparison['model1']['avg_similarity']:.3f}",
                f"{comparison['model1']['name']} ({comparison['model1']['dimensions']}D)"
            )
        
        with col2:
            st.metric(
                "Model 2 Avg Similarity",
                f"{comparison['model2']['avg_similarity']:.3f}",
                f"{comparison['model2']['name']} ({comparison['model2']['dimensions']}D)"
            )
        
        with col3:
            st.metric(
                "Common Movies",
                comparison['common_movies'],
                f"out of {top_k} results"
            )
        
        with col4:
            st.metric(
                "Overlap Percentage",
                f"{comparison['overlap_percentage']:.1f}%",
                "between models"
            )
        
        # Side-by-side comparison
        st.subheader("🔍 Side-by-Side Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{comparison['model1']['name']} ({comparison['model1']['dimensions']}D)**")
            model1_df = pd.DataFrame(comparison['model1']['results'])
            if not model1_df.empty:
                st.dataframe(
                    model1_df[['title', 'similarity_score']].rename(
                        columns={'similarity_score': 'Score'}
                    ),
                    use_container_width=True
                )
        
        with col2:
            st.write(f"**{comparison['model2']['name']} ({comparison['model2']['dimensions']}D)**")
            model2_df = pd.DataFrame(comparison['model2']['results'])
            if not model2_df.empty:
                st.dataframe(
                    model2_df[['title', 'similarity_score']].rename(
                        columns={'similarity_score': 'Score'}
                    ),
                    use_container_width=True
                )
        
        # Visualization
        st.subheader("📊 Performance Visualization")
        
        # Create comparison chart
        fig = go.Figure()
        
        # Add bars for average similarity
        fig.add_trace(go.Bar(
            name='Average Similarity',
            x=[comparison['model1']['name'], comparison['model2']['name']],
            y=[comparison['model1']['avg_similarity'], comparison['model2']['avg_similarity']],
            marker_color=['lightblue', 'lightcoral']
        ))
        
        fig.update_layout(
            title="Average Similarity Score Comparison",
            xaxis_title="Model",
            yaxis_title="Average Similarity Score",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Overlap analysis
        if comparison['common_movies'] > 0:
            st.subheader("🎯 Overlap Analysis")
            
            # Find common movies
            titles1 = {r['title'] for r in comparison['model1']['results']}
            titles2 = {r['title'] for r in comparison['model2']['results']}
            common_titles = titles1.intersection(titles2)
            
            if common_titles:
                st.write("**Movies found by both models:**")
                for title in common_titles:
                    st.write(f"• {title}")
    
    # Footer
    st.markdown("---")
    st.markdown("**Embedding Model Comparison System** - Built with Streamlit and Pinecone")

if __name__ == "__main__":
    main()
