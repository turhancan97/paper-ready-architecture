#!/usr/bin/env python3
"""
Example: Programmatic Usage of MLP Generator
============================================

This script demonstrates how to use the MLP generator programmatically
without the GUI, useful for batch generation or integration into other tools.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.mlp_generator import MLPGenerator
from src.config_manager import ConfigManager

def create_basic_mlp():
    """Create a basic MLP diagram programmatically."""
    
    # Initialize components
    generator = MLPGenerator()
    config_manager = ConfigManager()
    
    # Get default configuration
    config = config_manager.get_default_config()
    
    # Customize the configuration
    config["network_structure"] = {
        "input_neurons": 4,
        "hidden_layers": [6, 4],
        "output_neurons": 3
    }
    
    config["visual_params"]["node_color"] = "#2E86AB"
    config["visual_params"]["edge_opacity"] = 0.6
    config["visual_params"]["layer_spacing"] = 120
    
    config["labels"]["show_layer_labels"] = True
    
    # Generate the diagram
    fig = generator.create_diagram(config)
    
    # Save in multiple formats
    generator.save_figure("basic_mlp.png", "png", dpi=300)
    generator.save_figure("basic_mlp.svg", "svg", dpi=300)
    generator.save_figure("basic_mlp.pdf", "pdf", dpi=300)
    
    # Save the configuration
    config_manager.save_config(config, "basic_mlp_config.yaml")
    
    print("✅ Basic MLP diagrams created:")
    print("   - basic_mlp.png")
    print("   - basic_mlp.svg") 
    print("   - basic_mlp.pdf")
    print("   - basic_mlp_config.yaml")
    
    generator.close_figure()

def create_deep_network():
    """Create a deeper network example."""
    
    generator = MLPGenerator()
    config_manager = ConfigManager()
    
    config = config_manager.get_default_config()
    
    # Deep network configuration
    config["network_structure"] = {
        "input_neurons": 10,
        "hidden_layers": [8, 6, 4, 3],
        "output_neurons": 2
    }
    
    config["visual_params"]["node_diameter"] = 25
    config["visual_params"]["node_color"] = "#A23B72"
    config["visual_params"]["edge_width"] = 0.8
    config["visual_params"]["layer_spacing"] = 100
    config["visual_params"]["node_spacing"] = 45
    
    config["labels"]["show_layer_labels"] = False  # Cleaner look for deep networks
    
    fig = generator.create_diagram(config)
    generator.save_figure("deep_network.png", "png", dpi=300)
    config_manager.save_config(config, "deep_network_config.yaml")
    
    print("✅ Deep network diagram created:")
    print("   - deep_network.png")
    print("   - deep_network_config.yaml")
    
    generator.close_figure()

def create_minimal_network():
    """Create a minimal, paper-ready network."""
    
    generator = MLPGenerator()
    config_manager = ConfigManager()
    
    config = config_manager.get_default_config()
    
    # Minimal configuration
    config["network_structure"] = {
        "input_neurons": 2,
        "hidden_layers": [3],
        "output_neurons": 1
    }
    
    config["visual_params"]["node_diameter"] = 35
    config["visual_params"]["node_color"] = "#404040"  # Gray for academic papers
    config["visual_params"]["edge_width"] = 1.2
    config["visual_params"]["edge_opacity"] = 0.8
    config["visual_params"]["layer_spacing"] = 140
    
    config["labels"]["show_layer_labels"] = True
    config["labels"]["input_label"] = "Input"
    config["labels"]["hidden_label"] = "Hidden"
    config["labels"]["output_label"] = "Output"
    
    fig = generator.create_diagram(config)
    generator.save_figure("minimal_network.svg", "svg", dpi=300)  # SVG for papers
    config_manager.save_config(config, "minimal_network_config.yaml")
    
    print("✅ Minimal network diagram created:")
    print("   - minimal_network.svg (vector format for papers)")
    print("   - minimal_network_config.yaml")
    
    generator.close_figure()

if __name__ == "__main__":
    print("🧠 Generating example MLP diagrams...")
    print()
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    os.chdir("output")
    
    create_basic_mlp()
    print()
    create_deep_network()
    print()
    create_minimal_network()
    print()
    print("🎉 All examples generated successfully!")
    print("💡 Check the 'output' directory for the generated files.") 