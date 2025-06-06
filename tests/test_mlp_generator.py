#!/usr/bin/env python3
"""
Tests for MLPGenerator functionality
"""

import sys
import os
import unittest
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mlp_generator import MLPGenerator
from config_manager import ConfigManager


class TestMLPGenerator(unittest.TestCase):
    """Test cases for MLPGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = MLPGenerator()
        self.config_manager = ConfigManager()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.generator.close_figure()
        shutil.rmtree(self.test_dir)
    
    def test_basic_diagram_creation(self):
        """Test basic diagram creation."""
        config = self.config_manager.get_default_config()
        fig = self.generator.create_diagram(config)
        
        # Check that figure was created
        self.assertIsNotNone(fig)
        self.assertIsNotNone(self.generator.fig)
    
    def test_different_network_structures(self):
        """Test various network structures."""
        test_structures = [
            {'input_neurons': 1, 'hidden_layers': [], 'output_neurons': 1},  # Minimal
            {'input_neurons': 3, 'hidden_layers': [4], 'output_neurons': 2},  # Single hidden
            {'input_neurons': 5, 'hidden_layers': [8, 6, 4], 'output_neurons': 3},  # Deep
            {'input_neurons': 10, 'hidden_layers': [20, 15, 10, 5], 'output_neurons': 4},  # Large
        ]
        
        for structure in test_structures:
            with self.subTest(structure=structure):
                config = self.config_manager.get_default_config()
                config['network_structure'] = structure
                config = self.config_manager.ensure_layer_colors(config)
                
                fig = self.generator.create_diagram(config)
                self.assertIsNotNone(fig)
                self.generator.close_figure()
    
    def test_visual_parameters(self):
        """Test different visual parameter combinations."""
        config = self.config_manager.get_default_config()
        
        # Test extreme values
        test_params = [
            {'node_diameter': 10, 'edge_width': 0.5, 'edge_opacity': 0.1},
            {'node_diameter': 80, 'edge_width': 5.0, 'edge_opacity': 1.0},
            {'layer_spacing': 50, 'node_spacing': 20},
            {'layer_spacing': 300, 'node_spacing': 120},
        ]
        
        for params in test_params:
            with self.subTest(params=params):
                config['visual_params'].update(params)
                config = self.config_manager.ensure_layer_colors(config)
                
                fig = self.generator.create_diagram(config)
                self.assertIsNotNone(fig)
                self.generator.close_figure()
    
    def test_custom_colors(self):
        """Test custom color schemes."""
        config = self.config_manager.get_default_config()
        
        # Test user's requested colors
        custom_colors = ['#84A1FB', '#FB84DC', '#84FB9A', '#FBB484']
        config['visual_params']['layer_colors'] = custom_colors
        config['network_structure']['hidden_layers'] = [4, 3]  # 4 layers total
        
        fig = self.generator.create_diagram(config)
        self.assertIsNotNone(fig)
    
    def test_export_formats(self):
        """Test different export formats."""
        config = self.config_manager.get_default_config()
        config = self.config_manager.ensure_layer_colors(config)
        
        fig = self.generator.create_diagram(config)
        
        formats = ['png', 'pdf', 'svg', 'jpeg']
        for fmt in formats:
            with self.subTest(format=fmt):
                test_file = os.path.join(self.test_dir, f'test.{fmt}')
                try:
                    self.generator.save_figure(test_file, fmt, dpi=150)
                    self.assertTrue(os.path.exists(test_file))
                    self.assertGreater(os.path.getsize(test_file), 0)
                except Exception as e:
                    self.fail(f"Failed to save {fmt} format: {e}")
    
    def test_labels_functionality(self):
        """Test label display functionality."""
        config = self.config_manager.get_default_config()
        
        # Test with labels enabled
        config['labels']['show_layer_labels'] = True
        config['labels']['input_label'] = 'Custom Input'
        config['labels']['hidden_label'] = 'Custom Hidden'
        config['labels']['output_label'] = 'Custom Output'
        
        fig = self.generator.create_diagram(config)
        self.assertIsNotNone(fig)
        self.generator.close_figure()
        
        # Test with labels disabled
        config['labels']['show_layer_labels'] = False
        fig = self.generator.create_diagram(config)
        self.assertIsNotNone(fig)
    
    def test_base64_export(self):
        """Test base64 image export functionality."""
        config = self.config_manager.get_default_config()
        config = self.config_manager.ensure_layer_colors(config)
        
        fig = self.generator.create_diagram(config)
        
        # Test base64 export
        base64_data = self.generator.get_figure_as_base64('png', dpi=100)
        self.assertIsInstance(base64_data, str)
        self.assertGreater(len(base64_data), 0)
        
        # Should be valid base64
        import base64
        try:
            decoded = base64.b64decode(base64_data)
            self.assertGreater(len(decoded), 0)
        except Exception as e:
            self.fail(f"Invalid base64 data: {e}")


if __name__ == '__main__':
    unittest.main() 