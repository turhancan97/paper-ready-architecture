#!/usr/bin/env python3
"""
Test script for CNN visualization functionality.
"""

import os
import sys
sys.path.append('src')

from config_manager import ConfigManager
from cnn_generator import CNNGenerator

def test_cnn_visualization():
    """Test the CNN visualization functionality."""
    print("🧪 Testing CNN visualization...")
    
    # Initialize components
    config_manager = ConfigManager()
    cnn_generator = CNNGenerator()
    
    # Load LeNet configuration
    config = config_manager.load_config("configs/lenet_config.yaml")
    
    # Create output directory
    os.makedirs("test_outputs", exist_ok=True)
    
    # Generate diagram
    print("📸 Generating LeNet architecture diagram...")
    fig = cnn_generator.create_diagram(config)
    
    # Save diagram
    output_path = "test_outputs/lenet_architecture.png"
    cnn_generator.save_figure(output_path, "png", 300)
    cnn_generator.close_figure()
    
    print(f"✅ Diagram saved to: {output_path}")
    
    # Test custom configuration
    print("\n📸 Testing custom CNN configuration...")
    custom_config = {
        "network_type": "cnn",
        "input_shape": [32, 32, 3],  # CIFAR-10 input shape
        "conv_layers": [
            {
                "filters": 32,
                "kernel_size": 3,
                "stride": 1,
                "padding": "same",
                "activation": "relu",
                "output_shape": [32, 32, 32]
            },
            {
                "filters": 64,
                "kernel_size": 3,
                "stride": 1,
                "padding": "same",
                "activation": "relu",
                "output_shape": [32, 32, 64]
            }
        ],
        "pool_layers": [
            {
                "filters": 32,  # Number of input channels
                "pool_type": "max",
                "pool_size": 2,
                "stride": 2,
                "padding": "valid",
                "output_shape": [16, 16, 32]
            },
            {
                "filters": 64,  # Number of input channels
                "pool_type": "max",
                "pool_size": 2,
                "stride": 2,
                "padding": "valid",
                "output_shape": [8, 8, 64]
            }
        ],
        "flatten": True,
        "flatten_shape": [1, 4096],  # 8 * 8 * 64 = 4096
        "dense_layers": [
            {
                "units": 512,
                "activation": "relu"
            },
            {
                "units": 256,
                "activation": "relu"
            }
        ],
        "output_units": 10,
        "output_activation": "softmax"
    }
    
    # Generate custom diagram
    fig = cnn_generator.create_diagram(custom_config)
    
    # Save custom diagram
    output_path = "test_outputs/custom_cnn_architecture.png"
    cnn_generator.save_figure(output_path, "png", 300)
    cnn_generator.close_figure()
    
    print(f"✅ Custom diagram saved to: {output_path}")
    print("\n✨ CNN visualization tests completed successfully!")

if __name__ == "__main__":
    test_cnn_visualization() 