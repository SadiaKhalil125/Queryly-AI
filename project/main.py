#!/usr/bin/env python3
"""
Queryly AI - Main Entry Point
=============================

This is the main entry point for the Queryly AI application.
The application can be run either through this file or directly
using streamlit run user_interface.py

Author: Queryly AI Team
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

def main():
    """
    Main entry point for the Queryly AI application.
    """
    try:
        # Import and run the Streamlit interface
        import streamlit.web.cli as stcli
        import streamlit as st
        
        # Set the page config
        st.set_page_config(
            page_title="Queryly AI",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Run the user interface
        from user_interface import load_css
        
        # Load custom CSS
        load_css()
        
        print("🚀 Starting Queryly AI...")
        print("📱 Open your browser and navigate to: http://localhost:8501")
        print("⚡ Queryly AI is ready to assist with SQL learning!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting Queryly AI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
