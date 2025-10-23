#!/usr/bin/env python3
"""
Demo script showing how to use the Embedding Model Comparison System
This script demonstrates the key features without the UI
"""

from embedding_comparison_system import EmbeddingComparisonSystem, EMBEDDING_MODELS, load_movies_from_csv
import json

def demo_basic_comparison():
    """Demonstrate basic model comparison functionality"""
    print("🎬 Embedding Model Comparison Demo")
    print("=" * 50)
    
    # Initialize system
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', 'your-pinecone-api-key-here')
    system = EmbeddingComparisonSystem(PINECONE_API_KEY)
    
    # Load movies (using a subset for demo)
    print("📁 Loading movies data...")
    try:
        movies = load_movies_from_csv('../data/horror_movies_2025.csv')
        # Use first 50 movies for demo
        movies = movies[:50]
        print(f"✅ Loaded {len(movies)} movies for demo")
    except FileNotFoundError:
        print("❌ CSV file not found. Please ensure '../data/horror_movies_2025.csv' is accessible.")
        return
    
    # Select two different models for comparison
    model1 = EMBEDDING_MODELS['all-mpnet-base-v2']  # 768 dimensions
    model2 = EMBEDDING_MODELS['all-MiniLM-L6-v2']   # 384 dimensions
    
    print(f"\n🔍 Comparing models:")
    print(f"   Model 1: {model1.name} ({model1.dimensions}D)")
    print(f"   Model 2: {model2.name} ({model2.dimensions}D)")
    
    # Create indices
    print("\n🏗️  Creating Pinecone indices...")
    index1_name = system.create_index(model1, "-demo")
    index2_name = system.create_index(model2, "-demo")
    
    # Upload movies to both indices
    print("\n📤 Uploading movies to both indices...")
    system.embed_and_upload_movies(movies, model1, index1_name)
    system.embed_and_upload_movies(movies, model2, index2_name)
    
    # Test queries
    test_queries = [
        "scary movies about ghosts and supernatural",
        "psychological horror films",
        "movies with haunted houses"
    ]
    
    print("\n🔍 Testing queries...")
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Query {i}: '{query}' ---")
        
        # Get results from both models
        results1 = system.search_movies(query, model1, index1_name, top_k=3)
        results2 = system.search_movies(query, model2, index2_name, top_k=3)
        
        print(f"\nModel 1 ({model1.name}) results:")
        for j, movie in enumerate(results1, 1):
            print(f"  {j}. {movie['title']} (Score: {movie['similarity_score']:.3f})")
        
        print(f"\nModel 2 ({model2.name}) results:")
        for j, movie in enumerate(results2, 1):
            print(f"  {j}. {movie['title']} (Score: {movie['similarity_score']:.3f})")
        
        # Compare results
        comparison = system.compare_models(query, model1, model2, index1_name, index2_name, top_k=3)
        
        print(f"\n📊 Comparison metrics:")
        print(f"   Common movies: {comparison['common_movies']}")
        print(f"   Overlap: {comparison['overlap_percentage']:.1f}%")
        print(f"   Model 1 avg similarity: {comparison['model1']['avg_similarity']:.3f}")
        print(f"   Model 2 avg similarity: {comparison['model2']['avg_similarity']:.3f}")
    
    print("\n✅ Demo completed!")
    print("\n💡 To use the full system with UI, run:")
    print("   python run_comparison.py")
    print("   or")
    print("   streamlit run streamlit_app.py")

def demo_model_configurations():
    """Demonstrate different model configurations"""
    print("\n🔧 Available Model Configurations:")
    print("=" * 40)
    
    for name, model in EMBEDDING_MODELS.items():
        print(f"📦 {name}")
        print(f"   Dimensions: {model.dimensions}")
        print(f"   Description: {model.description}")
        print()

def demo_dimension_impact():
    """Demonstrate how dimensions affect performance"""
    print("\n📏 Dimension Impact Analysis:")
    print("=" * 35)
    
    print("Higher dimensions typically provide:")
    print("✅ Better semantic understanding")
    print("✅ More nuanced similarity matching")
    print("❌ Higher computational cost")
    print("❌ More storage requirements")
    print()
    
    print("Lower dimensions typically provide:")
    print("✅ Faster processing")
    print("✅ Lower storage requirements")
    print("✅ Better for real-time applications")
    print("❌ May lose some semantic nuance")
    print()

if __name__ == "__main__":
    try:
        demo_model_configurations()
        demo_dimension_impact()
        demo_basic_comparison()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check your setup and try again.")
