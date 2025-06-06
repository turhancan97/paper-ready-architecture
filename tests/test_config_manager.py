#!/usr/bin/env python3
"""
Tests for ConfigManager functionality
"""

import sys
import os
import unittest
import tempfile
import shutil
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.config_manager = ConfigManager(config_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_default_config(self):
        """Test default configuration generation."""
        config = self.config_manager.get_default_config()
        
        # Check required sections exist
        self.assertIn('network_structure', config)
        self.assertIn('visual_params', config)
        self.assertIn('labels', config)
        self.assertIn('export', config)
        self.assertIn('metadata', config)
        
        # Check network structure defaults
        network = config['network_structure']
        self.assertEqual(network['input_neurons'], 3)
        self.assertEqual(network['hidden_layers'], [4, 4])
        self.assertEqual(network['output_neurons'], 2)
        
        # Check visual params
        visual = config['visual_params']
        self.assertIn('node_diameter', visual)
        self.assertIn('layer_colors', visual)
        self.assertIn('edge_width', visual)
        self.assertIn('edge_opacity', visual)
    
    def test_layer_colors_validation(self):
        """Test layer color validation and fixing."""
        config = self.config_manager.get_default_config()
        
        # Test with invalid colors
        config['visual_params']['layer_colors'] = ['#INVALID', '#FF6B6B']
        config['network_structure']['hidden_layers'] = [4, 3]  # 4 layers total
        
        fixed_config = self.config_manager.ensure_layer_colors(config)
        colors = fixed_config['visual_params']['layer_colors']
        
        # Should have 4 colors (input + 2 hidden + output)
        self.assertEqual(len(colors), 4)
        
        # First color should be fixed (invalid replaced)
        self.assertNotEqual(colors[0], '#INVALID')
        self.assertTrue(colors[0].startswith('#'))
        self.assertEqual(len(colors[0]), 7)
        
        # Second color should remain the same (was valid)
        self.assertEqual(colors[1], '#FF6B6B')
    
    def test_save_and_load_config(self):
        """Test configuration saving and loading."""
        config = self.config_manager.get_default_config()
        config['network_structure']['input_neurons'] = 5
        config['visual_params']['node_diameter'] = 50
        
        # Save config
        filepath = self.config_manager.save_config(config, 'test_config.yaml')
        self.assertTrue(os.path.exists(filepath))
        
        # Load config
        loaded_config = self.config_manager.load_config(filepath)
        
        # Check data integrity
        self.assertEqual(loaded_config['network_structure']['input_neurons'], 5)
        self.assertEqual(loaded_config['visual_params']['node_diameter'], 50)
        self.assertIn('saved_at', loaded_config['metadata'])
    
    def test_hex_color_validation(self):
        """Test hex color validation in ensure_layer_colors."""
        config = self.config_manager.get_default_config()
        
        test_cases = [
            ('#FF6B6B', True),   # Valid
            ('#84A1FB', True),   # Valid
            ('#INVALID', False), # Invalid
            ('#GGG111', False),  # Invalid hex chars
            ('#12345', False),   # Too short
            ('#1234567', False), # Too long
            ('FF6B6B', False),   # Missing #
        ]
        
        for color, should_be_valid in test_cases:
            config['visual_params']['layer_colors'] = [color]
            config['network_structure']['hidden_layers'] = []  # 2 layers total
            
            result_config = self.config_manager.ensure_layer_colors(config)
            result_color = result_config['visual_params']['layer_colors'][0]
            
            if should_be_valid:
                self.assertEqual(result_color, color, f"Valid color {color} was changed")
            else:
                self.assertNotEqual(result_color, color, f"Invalid color {color} was not fixed")
                # Should be replaced with a valid color
                self.assertTrue(result_color.startswith('#'))
                self.assertEqual(len(result_color), 7)


if __name__ == '__main__':
    unittest.main() 