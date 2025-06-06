#!/usr/bin/env python3
"""
Integration tests for complete workflows
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


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.generator = MLPGenerator()
        self.config_manager = ConfigManager(config_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.generator.close_figure()
        shutil.rmtree(self.test_dir)
    
    def test_complete_workflow(self):
        """Test complete workflow: create config -> generate diagram -> save config -> export image."""
        # Step 1: Create and customize configuration
        config = self.config_manager.get_default_config()
        config['network_structure'] = {
            'input_neurons': 4,
            'hidden_layers': [6, 4],
            'output_neurons': 3
        }
        config['visual_params']['layer_colors'] = ['#84A1FB', '#FB84DC', '#84FB9A', '#FBB484']
        config['visual_params']['node_diameter'] = 35
        config['visual_params']['edge_width'] = 1.5
        
        # Step 2: Ensure layer colors are properly set
        config = self.config_manager.ensure_layer_colors(config)
        
        # Step 3: Generate diagram
        fig = self.generator.create_diagram(config)
        self.assertIsNotNone(fig)
        
        # Step 4: Save configuration
        config_path = self.config_manager.save_config(config, 'workflow_test.yaml')
        self.assertTrue(os.path.exists(config_path))
        
        # Step 5: Export image in multiple formats
        formats = ['png', 'pdf', 'svg']
        for fmt in formats:
            output_path = os.path.join(self.test_dir, f'test_output.{fmt}')
            self.generator.save_figure(output_path, fmt, dpi=150)
            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(os.path.getsize(output_path), 0)
        
        # Step 6: Load configuration and verify
        loaded_config = self.config_manager.load_config(config_path)
        self.assertEqual(loaded_config['network_structure']['input_neurons'], 4)
        self.assertEqual(loaded_config['visual_params']['node_diameter'], 35)
    
    def test_user_requested_colors_workflow(self):
        """Test workflow with user's specifically requested colors."""
        # Create config with user's colors
        config = self.config_manager.get_default_config()
        config['network_structure'] = {
            'input_neurons': 3,
            'hidden_layers': [5, 4],
            'output_neurons': 2
        }
        
        # Use the exact colors the user mentioned
        user_colors = ['#84A1FB', '#FB84DC', '#84FBA1', '#FBA184']
        config['visual_params']['layer_colors'] = user_colors
        config['visual_params']['node_diameter'] = 40
        
        # Process and generate
        config = self.config_manager.ensure_layer_colors(config)
        fig = self.generator.create_diagram(config)
        
        # Verify colors were preserved
        final_colors = config['visual_params']['layer_colors']
        for i, expected_color in enumerate(user_colors):
            self.assertEqual(final_colors[i], expected_color, 
                           f"Color {i} was changed from {expected_color} to {final_colors[i]}")
        
        # Export test
        output_path = os.path.join(self.test_dir, 'user_colors_test.png')
        self.generator.save_figure(output_path, 'png', dpi=300)
        self.assertTrue(os.path.exists(output_path))
    
    def test_academic_style_workflow(self):
        """Test academic-style configuration workflow."""
        config = self.config_manager.get_default_config()
        
        # Academic configuration
        config.update({
            'network_structure': {
                'input_neurons': 4,
                'hidden_layers': [6, 4],
                'output_neurons': 3
            },
            'visual_params': {
                'node_diameter': 25,
                'node_color': '#2C3E50',
                'layer_colors': ['#2C3E50', '#34495E', '#5D6D7E', '#85929E'],
                'edge_width': 1.2,
                'edge_opacity': 0.8,
                'layer_spacing': 120,
                'node_spacing': 50
            },
            'labels': {
                'show_layer_labels': True,
                'input_label': 'Features',
                'hidden_label': 'Processing',
                'output_label': 'Classes'
            },
            'export': {
                'width': 800,
                'height': 600,
                'dpi': 300,
                'background_color': 'white'
            }
        })
        
        # Generate and export
        config = self.config_manager.ensure_layer_colors(config)
        fig = self.generator.create_diagram(config)
        self.assertIsNotNone(fig)
        
        # Save as academic template
        template_path = self.config_manager.save_config(config, 'academic_template.yaml')
        self.assertTrue(os.path.exists(template_path))
        
        # Export high-quality image
        output_path = os.path.join(self.test_dir, 'academic_style.png')
        self.generator.save_figure(output_path, 'png', dpi=300)
        self.assertTrue(os.path.exists(output_path))
    
    def test_error_recovery_workflow(self):
        """Test error recovery in workflows."""
        # Start with intentionally problematic config
        config = self.config_manager.get_default_config()
        config['visual_params']['layer_colors'] = ['#INVALID', '#BADCOLOR', '#FF6B6B']
        config['network_structure']['hidden_layers'] = [4, 3, 2]  # 5 layers total
        
        # Should auto-fix invalid colors
        config = self.config_manager.ensure_layer_colors(config)
        colors = config['visual_params']['layer_colors']
        
        # Verify all colors are now valid
        for i, color in enumerate(colors):
            self.assertTrue(color.startswith('#'), f"Color {i} doesn't start with #: {color}")
            self.assertEqual(len(color), 7, f"Color {i} wrong length: {color}")
            try:
                int(color[1:], 16)  # Should be valid hex
            except ValueError:
                self.fail(f"Color {i} is not valid hex: {color}")
        
        # Should generate successfully despite original invalid colors
        fig = self.generator.create_diagram(config)
        self.assertIsNotNone(fig)
        
        # Should export successfully
        output_path = os.path.join(self.test_dir, 'error_recovery_test.png')
        self.generator.save_figure(output_path, 'png', dpi=150)
        self.assertTrue(os.path.exists(output_path))


if __name__ == '__main__':
    unittest.main() 