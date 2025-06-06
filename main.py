#!/usr/bin/env python3
"""
Neural Network Architecture Visualizer
=======================================

A tool for creating paper-ready visualizations of Multi-Layer Perceptron architectures
with customizable parameters and clean, minimalist design.

Usage:
    python main.py

Features:
- Real-time preview with adjustable parameters
- Export to multiple formats (PNG, PDF, SVG)
- Configuration save/load functionality
- Clean, academic-style visualizations
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui_app import main

if __name__ == "__main__":
    main() 