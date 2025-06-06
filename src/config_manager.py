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
                "node_color": "#4A90E2",
                "edge_width": 1.0,
                "edge_opacity": 0.7,
                "layer_spacing": 150,
                "node_spacing": 60
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
        
        # Update metadata
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