"""
Advanced Embedding Comparison System for Pinecone
Supports multiple embedding models with different dimensions and comparison capabilities
"""

import os
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
import numpy as np
from pinecone import Pinecone, ServerlessSpec
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

@dataclass
class EmbeddingModel:
    """Configuration for an embedding model"""
    name: str
    model_id: str
    dimensions: int
    description: str
    max_sequence_length: int = 512

# Available embedding models with their configurations
EMBEDDING_MODELS = {
    'all-mpnet-base-v2': EmbeddingModel(
        name='all-mpnet-base-v2',
        model_id='all-mpnet-base-v2',
        dimensions=768,
        description='High-quality sentence embeddings, best for semantic similarity'
    ),
    'all-MiniLM-L6-v2': EmbeddingModel(
        name='all-MiniLM-L6-v2',
        model_id='all-MiniLM-L6-v2',
        dimensions=384,
        description='Fast and efficient, good balance of speed and quality'
    ),
    'all-MiniLM-L12-v2': EmbeddingModel(
        name='all-MiniLM-L12-v2',
        model_id='all-MiniLM-L12-v2',
        dimensions=384,
        description='Slightly larger model with better performance'
    ),
    'paraphrase-multilingual-MiniLM-L12-v2': EmbeddingModel(
        name='paraphrase-multilingual-MiniLM-L12-v2',
        model_id='paraphrase-multilingual-MiniLM-L12-v2',
        dimensions=384,
        description='Multilingual model for cross-language similarity'
    ),
    'distilbert-base-nli-mean-tokens': EmbeddingModel(
        name='distilbert-base-nli-mean-tokens',
        model_id='distilbert-base-nli-mean-tokens',
        dimensions=768,
        description='DistilBERT model optimized for natural language inference'
    )
}

class EmbeddingComparisonSystem:
    """Main system for comparing different embedding models and dimensions"""
    
    def __init__(self, pinecone_api_key: str):
        self.pc = Pinecone(api_key=pinecone_api_key)
        self.models = {}
        self.loaded_models = {}
        
    def load_model(self, model_config: EmbeddingModel) -> SentenceTransformer:
        """Load a specific embedding model"""
        if model_config.model_id not in self.loaded_models:
            print(f"Loading model: {model_config.name}")
            self.loaded_models[model_config.model_id] = SentenceTransformer(model_config.model_id)
        return self.loaded_models[model_config.model_id]
    
    def create_index(self, model_config: EmbeddingModel, index_suffix: str = "") -> str:
        """Create a Pinecone index for a specific model configuration"""
        # Clean model name for Pinecone (lowercase, alphanumeric and hyphens only)
        clean_name = model_config.name.replace('_', '-').lower()
        index_name = f"movies-{clean_name}-{model_config.dimensions}{index_suffix}"
        
        # Delete existing index if it exists
        if index_name in self.pc.list_indexes().names():
            print(f"Deleting existing index: {index_name}")
            self.pc.delete_index(index_name)
        
        # Create new index
        self.pc.create_index(
            name=index_name,
            dimension=model_config.dimensions,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-west-2'
            )
        )
        
        print(f"Created index: {index_name} with {model_config.dimensions} dimensions")
        return index_name
    
    def embed_and_upload_movies(self, movies: List[Dict], model_config: EmbeddingModel, 
                              index_name: str, batch_size: int = 32) -> None:
        """Embed movies and upload to Pinecone"""
        model = self.load_model(model_config)
        index = self.pc.Index(index_name)
        
        print(f"Embedding {len(movies)} movies with {model_config.name}")
        
        for i in range(0, len(movies), batch_size):
            batch = movies[i:i+batch_size]
            texts = [m['overview'] if m['overview'] else '' for m in batch]
            ids = [str(m['id']) for m in batch]
            
            # Generate embeddings
            embeddings = model.encode(texts)
            
            # Prepare vectors for Pinecone
            vectors = []
            for j, (movie_id, embedding, movie) in enumerate(zip(ids, embeddings, batch)):
                # Clean metadata to handle NaN values and ensure JSON serialization
                def clean_value(value):
                    """Clean a value for JSON serialization"""
                    if pd.isna(value) or value is None or str(value).lower() in ['nan', 'none', '']:
                        return "Unknown"
                    return str(value)
                
                metadata = {
                    'title': clean_value(movie['title']),
                    'release_date': clean_value(movie['release_date']),
                    'original_language': clean_value(movie['original_language']),
                    'model_name': model_config.name,
                    'dimensions': model_config.dimensions
                }
                vectors.append((movie_id, embedding.tolist(), metadata))
            
            # Upload to Pinecone
            index.upsert(vectors)
            
            if (i + batch_size) % 100 == 0:
                print(f"Processed {min(i + batch_size, len(movies))}/{len(movies)} movies")
    
    def search_movies(self, query: str, model_config: EmbeddingModel, 
                     index_name: str, top_k: int = 5) -> List[Dict]:
        """Search for similar movies using a specific model"""
        model = self.load_model(model_config)
        index = self.pc.Index(index_name)
        
        # Generate query embedding
        query_embedding = model.encode([query])
        
        # Search in Pinecone
        results = index.query(
            vector=query_embedding[0].tolist(),
            top_k=top_k,
            include_metadata=True
        )
        
        # Format results
        similar_movies = []
        for match in results['matches']:
            movie_info = {
                'id': match['id'],
                'title': match['metadata']['title'],
                'release_date': match['metadata']['release_date'],
                'similarity_score': match['score'],
                'model_name': match['metadata'].get('model_name', model_config.name),
                'dimensions': match['metadata'].get('dimensions', model_config.dimensions)
            }
            similar_movies.append(movie_info)
        
        return similar_movies
    
    def compare_models(self, query: str, model1_config: EmbeddingModel, 
                      model2_config: EmbeddingModel, index1_name: str, 
                      index2_name: str, top_k: int = 5) -> Dict[str, Any]:
        """Compare results from two different models"""
        print(f"Comparing models: {model1_config.name} vs {model2_config.name}")
        
        # Get results from both models
        results1 = self.search_movies(query, model1_config, index1_name, top_k)
        results2 = self.search_movies(query, model2_config, index2_name, top_k)
        
        # Calculate comparison metrics
        comparison = {
            'query': query,
            'model1': {
                'name': model1_config.name,
                'dimensions': model1_config.dimensions,
                'results': results1,
                'avg_similarity': np.mean([r['similarity_score'] for r in results1]) if results1 else 0
            },
            'model2': {
                'name': model2_config.name,
                'dimensions': model2_config.dimensions,
                'results': results2,
                'avg_similarity': np.mean([r['similarity_score'] for r in results2]) if results2 else 0
            }
        }
        
        # Find common movies between results
        titles1 = {r['title'] for r in results1}
        titles2 = {r['title'] for r in results2}
        common_titles = titles1.intersection(titles2)
        
        comparison['common_movies'] = len(common_titles)
        comparison['overlap_percentage'] = (len(common_titles) / top_k) * 100 if top_k > 0 else 0
        
        return comparison

def load_movies_from_csv(filename: str) -> List[Dict]:
    """Load movies from CSV file with data cleaning"""
    movies = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = pd.read_csv(f)
        for _, row in reader.iterrows():
            # Clean data to handle NaN values
            def clean_value(value):
                """Clean a value for JSON serialization"""
                if pd.isna(value) or value is None or str(value).lower() in ['nan', 'none', '']:
                    return "Unknown"
                return str(value)
            
            movies.append({
                'id': int(row['id']),
                'title': clean_value(row['title']),
                'overview': clean_value(row['overview']),
                'release_date': clean_value(row['release_date']),
                'original_language': clean_value(row['original_language'])
            })
    return movies

def create_comparison_visualization(comparison: Dict[str, Any]) -> go.Figure:
    """Create visualization comparing two models"""
    model1 = comparison['model1']
    model2 = comparison['model2']
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            f"Model 1: {model1['name']} ({model1['dimensions']}D)",
            f"Model 2: {model2['name']} ({model2['dimensions']}D)",
            "Similarity Scores Comparison",
            "Model Performance Metrics"
        ],
        specs=[[{"type": "table"}, {"type": "table"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Model 1 results table
    if model1['results']:
        titles1 = [r['title'] for r in model1['results']]
        scores1 = [r['similarity_score'] for r in model1['results']]
        
        fig.add_trace(
            go.Table(
                header=dict(values=['Rank', 'Title', 'Similarity Score']),
                cells=dict(values=[
                    list(range(1, len(titles1) + 1)),
                    titles1,
                    [f"{score:.3f}" for score in scores1]
                ])
            ),
            row=1, col=1
        )
    
    # Model 2 results table
    if model2['results']:
        titles2 = [r['title'] for r in model2['results']]
        scores2 = [r['similarity_score'] for r in model2['results']]
        
        fig.add_trace(
            go.Table(
                header=dict(values=['Rank', 'Title', 'Similarity Score']),
                cells=dict(values=[
                    list(range(1, len(titles2) + 1)),
                    titles2,
                    [f"{score:.3f}" for score in scores2]
                ])
            ),
            row=1, col=2
        )
    
    # Similarity scores comparison
    if model1['results'] and model2['results']:
        fig.add_trace(
            go.Bar(
                x=[f"Model 1\n{model1['name']}", f"Model 2\n{model2['name']}"],
                y=[model1['avg_similarity'], model2['avg_similarity']],
                name="Average Similarity",
                marker_color=['lightblue', 'lightcoral']
            ),
            row=2, col=1
        )
    
    # Performance metrics
    metrics = ['Common Movies', 'Overlap %']
    values = [comparison['common_movies'], comparison['overlap_percentage']]
    
    fig.add_trace(
        go.Bar(
            x=metrics,
            y=values,
            name="Comparison Metrics",
            marker_color='lightgreen'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        title_text=f"Model Comparison: '{comparison['query']}'",
        showlegend=False
    )
    
    return fig

if __name__ == "__main__":
    # Example usage
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', 'your-pinecone-api-key-here')
    
    # Initialize system
    system = EmbeddingComparisonSystem(PINECONE_API_KEY)
    
    # Load movies
    movies = load_movies_from_csv('data/horror_movies_2025.csv')
    print(f"Loaded {len(movies)} movies")
    
    # Example: Compare two models
    model1 = EMBEDDING_MODELS['all-mpnet-base-v2']
    model2 = EMBEDDING_MODELS['all-MiniLM-L6-v2']
    
    # Create indices
    index1 = system.create_index(model1, "-comparison")
    index2 = system.create_index(model2, "-comparison")
    
    # Upload movies to both indices
    system.embed_and_upload_movies(movies, model1, index1)
    system.embed_and_upload_movies(movies, model2, index2)
    
    # Compare results
    query = "scary movies about ghosts and supernatural"
    comparison = system.compare_models(query, model1, model2, index1, index2)
    
    print(f"Comparison results for: '{query}'")
    print(f"Model 1 ({model1.name}): {len(comparison['model1']['results'])} results")
    print(f"Model 2 ({model2.name}): {len(comparison['model2']['results'])} results")
    print(f"Common movies: {comparison['common_movies']}")
    print(f"Overlap: {comparison['overlap_percentage']:.1f}%")
