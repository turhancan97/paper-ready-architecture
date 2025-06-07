import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import random
from typing import List, Tuple, Dict, Any, Set
import io
import base64

class MLPGenerator:
    """Generates Multi-Layer Perceptron visualizations with customizable parameters."""
    
    def __init__(self):
        self.fig = None
        self.ax = None
        
    def create_diagram(self, config: Dict[str, Any]) -> plt.Figure:
        """Create MLP diagram based on configuration."""
        # Extract configuration
        structure = config["network_structure"]
        visual = config["visual_params"]
        labels = config["labels"]
        export_config = config["export"]
        pruning = config.get("pruning", {"enabled": False, "neuron_prune_percentage": 0.0, "synapse_prune_percentage": 0.0})
        
        # Create figure with clean style
        plt.style.use('default')
        self.fig, self.ax = plt.subplots(1, 1, figsize=(
            export_config["width"] / 100, 
            export_config["height"] / 100
        ))
        
        # Set clean, minimalist style
        self.ax.set_facecolor(export_config["background_color"])
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # Build layer structure
        layers = [structure["input_neurons"]] + structure["hidden_layers"] + [structure["output_neurons"]]
        
        # Apply pruning if enabled
        if pruning["enabled"]:
            layers, pruned_neurons, pruned_connections = self._apply_pruning(layers, pruning)
        else:
            pruned_neurons = set()
            pruned_connections = set()
        
        # Calculate positions
        positions = self._calculate_positions(layers, visual)
        
        # Draw connections first (so they appear behind nodes)
        self._draw_connections(positions, visual, pruned_connections)
        
        # Draw nodes
        self._draw_nodes(positions, visual, pruned_neurons)
        
        # Draw labels if requested
        if labels["show_layer_labels"]:
            self._draw_labels(positions, labels, layers)
        
        # Set appropriate limits
        self._set_limits(positions, visual)
        
        plt.tight_layout()
        return self.fig
    
    def _apply_pruning(self, layers: List[int], pruning: Dict[str, Any]) -> Tuple[List[int], Set[Tuple[int, int]], Set[Tuple[int, int, int, int]]]:
        """Apply pruning to neurons and synapses. Returns modified layers, pruned neurons, and pruned connections."""
        neuron_prune_pct = pruning["neuron_prune_percentage"] / 100.0
        synapse_prune_pct = pruning["synapse_prune_percentage"] / 100.0
        
        # Set random seed for consistent results based on pruning parameters and network structure
        # This ensures the same pruning pattern for the same configuration
        seed_str = f"{neuron_prune_pct}_{synapse_prune_pct}_{len(layers)}_{'-'.join(map(str, layers))}"
        seed = abs(hash(seed_str)) % 2**32
        random.seed(seed)
        
        pruned_neurons = set()  # (layer_idx, neuron_idx)
        pruned_connections = set()  # (from_layer, from_neuron, to_layer, to_neuron)
        
        # Original layers for position calculation
        original_layers = layers.copy()
        
        # Prune neurons in hidden layers only (not input/output)
        if neuron_prune_pct > 0:
            for layer_idx in range(1, len(layers) - 1):  # Skip input (0) and output (last)
                layer_size = layers[layer_idx]
                num_to_prune = int(layer_size * neuron_prune_pct)
                
                if num_to_prune > 0:
                    # Randomly select neurons to prune
                    neurons_to_prune = random.sample(range(layer_size), min(num_to_prune, layer_size))
                    for neuron_idx in neurons_to_prune:
                        pruned_neurons.add((layer_idx, neuron_idx))
        
        # Remove all connections involving pruned neurons (they shouldn't exist)
        for layer_idx in range(len(layers) - 1):
            from_layer_size = layers[layer_idx]
            to_layer_size = layers[layer_idx + 1]
            
            for from_neuron in range(from_layer_size):
                for to_neuron in range(to_layer_size):
                    # If either neuron in the connection is pruned, remove the connection
                    if (layer_idx, from_neuron) in pruned_neurons or (layer_idx + 1, to_neuron) in pruned_neurons:
                        pruned_connections.add((layer_idx, from_neuron, layer_idx + 1, to_neuron))
        
        # Prune additional synapses (only from remaining valid connections)
        if synapse_prune_pct > 0:
            for layer_idx in range(len(layers) - 1):
                from_layer_size = layers[layer_idx]
                to_layer_size = layers[layer_idx + 1]
                
                # Generate only valid connections (between non-pruned neurons)
                valid_connections = []
                for from_neuron in range(from_layer_size):
                    for to_neuron in range(to_layer_size):
                        # Only include connections between non-pruned neurons
                        if (layer_idx, from_neuron) not in pruned_neurons and (layer_idx + 1, to_neuron) not in pruned_neurons:
                            connection = (layer_idx, from_neuron, layer_idx + 1, to_neuron)
                            # And only if not already pruned due to neuron removal
                            if connection not in pruned_connections:
                                valid_connections.append(connection)
                
                # Calculate how many additional synapses to prune from valid connections
                num_to_prune = int(len(valid_connections) * synapse_prune_pct)
                
                if num_to_prune > 0:
                    # Randomly select connections to prune from valid connections only
                    connections_to_prune = random.sample(valid_connections, min(num_to_prune, len(valid_connections)))
                    for conn in connections_to_prune:
                        pruned_connections.add(conn)
        
        return original_layers, pruned_neurons, pruned_connections
    
    def _calculate_positions(self, layers: List[int], visual: Dict[str, Any]) -> List[List[Tuple[float, float]]]:
        """Calculate node positions for each layer."""
        positions = []
        x_start = 0
        
        for i, layer_size in enumerate(layers):
            layer_positions = []
            x = x_start + i * visual["layer_spacing"]
            
            # Center the layer vertically
            total_height = (layer_size - 1) * visual["node_spacing"]
            y_start = -total_height / 2
            
            for j in range(layer_size):
                y = y_start + j * visual["node_spacing"]
                layer_positions.append((x, y))
            
            positions.append(layer_positions)
        
        return positions
    
    def _draw_connections(self, positions: List[List[Tuple[float, float]]], visual: Dict[str, Any], pruned_connections: Set[Tuple[int, int, int, int]]):
        """Draw connections between layers."""
        for i in range(len(positions) - 1):
            current_layer = positions[i]
            next_layer = positions[i + 1]
            
            for start_idx, start_pos in enumerate(current_layer):
                for end_idx, end_pos in enumerate(next_layer):
                    # Check if this connection is pruned
                    if (i, start_idx, i + 1, end_idx) not in pruned_connections:
                        self.ax.plot(
                            [start_pos[0], end_pos[0]], 
                            [start_pos[1], end_pos[1]],
                            color='black',
                            linewidth=visual["edge_width"],
                            alpha=visual["edge_opacity"],
                            zorder=1
                        )
    
    def _draw_nodes(self, positions: List[List[Tuple[float, float]]], visual: Dict[str, Any], pruned_neurons: Set[Tuple[int, int]]):
        """Draw neural network nodes with layer-specific colors."""
        radius = visual["node_diameter"] / 2
        
        # Get layer colors, fallback to single color if not available
        layer_colors = visual.get("layer_colors", [visual["node_color"]])
        fallback_color = visual["node_color"]
        
        for layer_idx, layer_positions in enumerate(positions):
            # Get color for this layer, use fallback if not enough colors defined
            if layer_idx < len(layer_colors):
                layer_color = layer_colors[layer_idx]
            else:
                layer_color = fallback_color
            
            for neuron_idx, pos in enumerate(layer_positions):
                # Draw node with layer-specific color only if not pruned
                if (layer_idx, neuron_idx) not in pruned_neurons:
                    circle = patches.Circle(
                        pos, 
                        radius, 
                        facecolor=layer_color,
                        edgecolor='black',
                        linewidth=1.5,
                        zorder=2
                    )
                    self.ax.add_patch(circle)
    
    def _draw_labels(self, positions: List[List[Tuple[float, float]]], labels: Dict[str, Any], layers: List[int]):
        """Draw layer labels."""
        for i, layer_positions in enumerate(positions):
            if not layer_positions:
                continue
                
            # Calculate label position (center of layer, below the nodes)
            x_center = layer_positions[0][0]
            y_min = min(pos[1] for pos in layer_positions)
            label_y = y_min - 60  # Position below nodes
            
            # Determine label text
            if i == 0:
                label_text = labels["input_label"]
            elif i == len(positions) - 1:
                label_text = labels["output_label"]
            else:
                label_text = f"{labels['hidden_label']} {i}"
            
            # Add neuron count
            label_text += f"\n({layers[i]} neurons)"
            
            self.ax.text(
                x_center, 
                label_y,
                label_text,
                ha='center',
                va='top',
                fontsize=10,
                fontweight='normal',
                color='black'
            )
    
    def _set_limits(self, positions: List[List[Tuple[float, float]]], visual: Dict[str, Any]):
        """Set appropriate axis limits."""
        all_x = [pos[0] for layer in positions for pos in layer]
        all_y = [pos[1] for layer in positions for pos in layer]
        
        margin = visual["node_diameter"]
        
        self.ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        self.ax.set_ylim(min(all_y) - margin * 2, max(all_y) + margin)
    
    def save_figure(self, filepath: str, format: str = 'png', dpi: int = 300):
        """Save the figure in specified format."""
        if self.fig is None:
            raise ValueError("No figure to save. Call create_diagram first.")
        
        if format.lower() == 'svg':
            self.fig.savefig(filepath, format='svg', dpi=dpi, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
        elif format.lower() == 'pdf':
            self.fig.savefig(filepath, format='pdf', dpi=dpi, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
        else:  # PNG and other raster formats
            self.fig.savefig(filepath, format=format, dpi=dpi, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
    
    def get_figure_as_base64(self, format: str = 'png', dpi: int = 150) -> str:
        """Get figure as base64 string for GUI preview."""
        if self.fig is None:
            return ""
        
        buffer = io.BytesIO()
        self.fig.savefig(buffer, format=format, dpi=dpi, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
        buffer.seek(0)
        
        img_data = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        
        return img_data
    
    def close_figure(self):
        """Close the current figure to free memory."""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None 