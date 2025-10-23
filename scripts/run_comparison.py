#!/usr/bin/env python3
"""
Launcher script for the Embedding Model Comparison System
Provides easy access to both CLI and web interface
"""

import sys
import subprocess
import os
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'embedding_comparison_system.py',
        'streamlit_app.py',
        'requirements.txt',
        'horror_movies_2025.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def run_streamlit():
    """Launch the Streamlit web interface"""
    print("🚀 Launching Streamlit web interface...")
    print("📱 The web interface will open in your browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\n💡 Tips:")
    print("   - Use the sidebar to configure the system")
    print("   - Load movies data first")
    print("   - Select two models and create indices")
    print("   - Upload movies and start comparing!")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def run_cli():
    """Run the command line interface"""
    print("🖥️  Running command line interface...")
    try:
        subprocess.run([sys.executable, 'embedding_comparison_system.py'])
    except KeyboardInterrupt:
        print("\n👋 CLI stopped")

def main():
    """Main launcher function"""
    print("🎬 Embedding Model Comparison System Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not check_requirements():
        print("\n❌ Please ensure you're in the correct directory with all required files")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Failed to install requirements")
        sys.exit(1)
    
    print("\n🎯 Choose your interface:")
    print("1. 🌐 Web Interface (Streamlit) - Recommended")
    print("2. 🖥️  Command Line Interface")
    print("3. ❌ Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            run_streamlit()
            break
        elif choice == '2':
            run_cli()
            break
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
