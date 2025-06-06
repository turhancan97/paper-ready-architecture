#!/usr/bin/env python3
"""
Simple test to verify GUI initialization
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config_manager import ConfigManager
from src.mlp_generator import MLPGenerator

def test_components():
    """Test that all components can be initialized."""
    print("🧪 Testing components...")
    
    # Test ConfigManager
    try:
        config_manager = ConfigManager()
        config = config_manager.get_default_config()
        print("✅ ConfigManager: OK")
    except Exception as e:
        print(f"❌ ConfigManager failed: {e}")
        return False
    
    # Test MLPGenerator
    try:
        generator = MLPGenerator()
        fig = generator.create_diagram(config)
        generator.close_figure()
        print("✅ MLPGenerator: OK")
    except Exception as e:
        print(f"❌ MLPGenerator failed: {e}")
        return False
    
    # Test GUI components (import only)
    try:
        from src.gui_app import MLPVisualizerGUI
        print("✅ GUI imports: OK")
    except Exception as e:
        print(f"❌ GUI import failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔧 Testing Neural Network Visualizer components...")
    print()
    
    if test_components():
        print()
        print("🎉 All tests passed!")
        print("💡 You can now run 'python main.py' to start the GUI application.")
    else:
        print()
        print("❌ Some tests failed. Please check the error messages above.")
        sys.exit(1) 