import json
import yaml
import os
from datetime import datetime
from typing import Dict, Any, Optional

class ConfigManager:
    """Manages configuration saving and loading for neural network visualizations."""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = config_dir
        self.ensure_config_dir()
    
    def ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration for MLP visualization."""
        return {
            "network_structure": {
                "input_neurons": 3,
                "hidden_layers": [4, 4],
                "output_neurons": 2
            },
            "visual_params": {
                "node_diameter": 30,
                "node_color": "#4A90E2",  # Fallback color for backward compatibility
                "layer_colors": ["#4A90E2", "#50C878", "#FF6B6B", "#FFD93D"],  # Colors for each layer
                "edge_width": 1.0,
                "edge_opacity": 0.7,
                "layer_spacing": 150,
                "node_spacing": 60
            },
            "pruning": {
                "enabled": False,
                "neuron_prune_percentage": 0.0,
                "synapse_prune_percentage": 0.0
            },
            "labels": {
                "show_layer_labels": True,
                "input_label": "Input Layer",
                "hidden_label": "Hidden Layer",
                "output_label": "Output Layer"
            },
            "export": {
                "width": 800,
                "height": 600,
                "dpi": 300,
                "background_color": "white"
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        }
    
    def save_config(self, config: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Save configuration to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mlp_config_{timestamp}.yaml"
        
        if "metadata" not in config:
            config["metadata"] = {}
        config["metadata"]["saved_at"] = datetime.now().isoformat()
        
        filepath = os.path.join(self.config_dir, filename)
        
        with open(filepath, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
        
        return filepath
    
    def load_config(self, filepath: str) -> Dict[str, Any]:
        """Load configuration from file."""
        with open(filepath, 'r') as f:
            if filepath.endswith('.json'):
                return json.load(f)
            else:
                return yaml.safe_load(f)
    
    def get_config_files(self) -> list:
        """Get list of available configuration files."""
        config_files = []
        if os.path.exists(self.config_dir):
            for file in os.listdir(self.config_dir):
                if file.endswith(('.yaml', '.yml', '.json')):
                    config_files.append(file)
        return sorted(config_files, reverse=True)  # Most recent first
    
    def auto_save_config(self, config: Dict[str, Any]) -> str:
        """Auto-save configuration with timestamp."""
        return self.save_config(config, f"auto_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml")
    
    def ensure_layer_colors(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure there are enough layer colors for the current network structure."""
        # Calculate total number of layers
        structure = config["network_structure"]
        total_layers = 1 + len(structure["hidden_layers"]) + 1  # input + hidden + output
        
        # Default color palette
        default_colors = [
            "#4A90E2",  # Blue
            "#50C878",  # Green  
            "#FF6B6B",  # Red
            "#FFD93D",  # Yellow
            "#9B59B6",  # Purple
            "#E67E22",  # Orange
            "#1ABC9C",  # Teal
            "#34495E",  # Dark Gray
            "#E74C3C",  # Dark Red
            "#3498DB"   # Light Blue
        ]
        
        # Get current layer colors or use fallback
        current_colors = config["visual_params"].get("layer_colors", [config["visual_params"]["node_color"]])
        
        # Validate and fix invalid colors
        def is_valid_color(color):
            """Check if a color code is valid."""
            if not isinstance(color, str):
                return False
            if not color.startswith('#'):
                return False
            if len(color) != 7:
                return False
            try:
                int(color[1:], 16)  # Try to parse as hex
                return True
            except ValueError:
                return False
        
        # Replace invalid colors with defaults
        for i, color in enumerate(current_colors):
            if not is_valid_color(color):
                current_colors[i] = default_colors[i % len(default_colors)]
        
        # Extend colors if needed
        while len(current_colors) < total_layers:
            # Cycle through default colors
            color_idx = len(current_colors) % len(default_colors)
            current_colors.append(default_colors[color_idx])
        
        # Trim if too many colors
        current_colors = current_colors[:total_layers]
        
        # Update config
        config["visual_params"]["layer_colors"] = current_colors
        
        return config 