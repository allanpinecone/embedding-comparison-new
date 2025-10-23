#!/usr/bin/env python3
"""
Test script to verify the embedding comparison system is working
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from embedding_comparison_system import EmbeddingComparisonSystem, EMBEDDING_MODELS, load_movies_from_csv
        print("✅ Core system imports successful")
    except ImportError as e:
        print(f"❌ Core system import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✅ Streamlit import successful")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        import plotly.express as px
        print("✅ Data processing imports successful")
    except ImportError as e:
        print(f"❌ Data processing import failed: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ Sentence transformers import successful")
    except ImportError as e:
        print(f"❌ Sentence transformers import failed: {e}")
        return False
    
    try:
        from pinecone import Pinecone, ServerlessSpec
        print("✅ Pinecone import successful")
    except ImportError as e:
        print(f"❌ Pinecone import failed: {e}")
        return False
    
    return True

def test_model_configurations():
    """Test that model configurations are valid"""
    print("\n🔧 Testing model configurations...")
    
    try:
        from embedding_comparison_system import EMBEDDING_MODELS
        
        print(f"✅ Found {len(EMBEDDING_MODELS)} embedding models:")
        for name, model in EMBEDDING_MODELS.items():
            print(f"   - {name}: {model.dimensions}D - {model.description}")
        
        return True
    except Exception as e:
        print(f"❌ Model configuration test failed: {e}")
        return False

def test_csv_file():
    """Test that the CSV file exists and is readable"""
    print("\n📁 Testing CSV file...")
    
    csv_file = '../data/horror_movies_2025.csv'
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return False
    
    try:
        from embedding_comparison_system import load_movies_from_csv
        movies = load_movies_from_csv(csv_file)
        print(f"✅ CSV file loaded successfully: {len(movies)} movies")
        
        # Show sample movie
        if movies:
            sample = movies[0]
            print(f"   Sample movie: {sample['title']} ({sample['release_date']})")
        
        return True
    except Exception as e:
        print(f"❌ CSV file test failed: {e}")
        return False

def test_system_initialization():
    """Test that the system can be initialized"""
    print("\n🚀 Testing system initialization...")
    
    try:
        from embedding_comparison_system import EmbeddingComparisonSystem
        
        # Test with dummy API key (won't actually connect)
        PINECONE_API_KEY = 'test-key'
        system = EmbeddingComparisonSystem(PINECONE_API_KEY)
        print("✅ System initialization successful")
        
        # Test model loading (this will download models if not cached)
        print("   Testing model loading...")
        from embedding_comparison_system import EMBEDDING_MODELS
        model_config = list(EMBEDDING_MODELS.values())[0]
        model = system.load_model(model_config)
        print(f"✅ Model loading successful: {model_config.name}")
        
        return True
    except Exception as e:
        print(f"❌ System initialization test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎬 Embedding Model Comparison System - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_model_configurations,
        test_csv_file,
        test_system_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n💡 To start the web interface, run:")
        print("   streamlit run streamlit_app.py")
        print("\n💡 To run the demo, run:")
        print("   python demo_comparison.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
