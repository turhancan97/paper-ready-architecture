#!/usr/bin/env python3
"""
CNN Generator Module for visualizing Convolutional Neural Network architectures.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import requests
from io import BytesIO
import os

class CNNGenerator:
    """Class for generating publication-ready CNN architecture visualizations."""
    
    def __init__(self):
        """Initialize the CNN generator with default parameters."""
        self.default_params = {
            "input_shape": (28, 28, 1),  # MNIST default
            "layer_colors": {
                "input": "#4A90E2",      # Blue
                "conv": "#50C878",       # Green
                "pool": "#FF6B6B",       # Red
                "flatten": "#FFD93D",    # Yellow
                "dense": "#9B59B6",      # Purple
                "output": "#E74C3C"      # Dark Red
            },
            "visual_params": {
                "feature_map_size": 40,   # Size of feature map squares
                "feature_map_spacing": 5,  # Spacing between feature maps
                "layer_spacing": 100,     # Horizontal spacing between layers
                "arrow_length": 30,       # Length of connection arrows
                "arrow_width": 1.5,       # Width of connection arrows
                "arrow_color": "#666666", # Gray color for arrows
                "label_fontsize": 10,     # Font size for layer labels
                "shape_fontsize": 8,      # Font size for tensor shapes
                "padding": 20             # Padding around the entire diagram
            }
        }
        
        # Load default MNIST sample
        self.mnist_sample = self._load_mnist_sample()
        
    def _load_mnist_sample(self):
        """Load a sample MNIST digit (digit '2') for visualization."""
        try:
            
            # Try to load from local assets first
            if os.path.exists("assets/mnist_sample.png"):
                img = Image.open("assets/mnist_sample.png")
                if img.mode != 'L':
                    img = img.convert('L')
                return img
            # If not found locally, download from a reliable source
            url = "https://github.com/myleott/mnist_png/raw/master/testing/2/10.png"
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            if img.mode != 'L':
                img = img.convert('L')
            return img
        except Exception as e:
            print(f"Warning: Could not load MNIST sample: {e}")
            # Create a simple placeholder
            return Image.new('L', (28, 28), color=128)
    
    def _create_feature_map(self, size, color, alpha=1.0):
        """Create a feature map visualization."""
        return patches.Rectangle(
            (0, 0), size, size,
            facecolor=color,
            alpha=alpha,
            edgecolor='black',
            linewidth=1
        )
    
    def _create_layer_block(self, layer_type, num_maps, size, color, label, shape):
        """Create a layer block with feature maps and labels."""
        block = plt.figure(figsize=(size/100, size/100))
        ax = block.add_subplot(111)
        
        # Calculate grid dimensions
        grid_size = int(np.ceil(np.sqrt(num_maps)))
        
        # Create feature maps
        for i in range(num_maps):
            row = i // grid_size
            col = i % grid_size
            x = col * (size + self.default_params["visual_params"]["feature_map_spacing"])
            y = row * (size + self.default_params["visual_params"]["feature_map_spacing"])
            
            feature_map = self._create_feature_map(
                size,
                color,
                alpha=0.8 if i < num_maps else 0.3
            )
            ax.add_patch(feature_map)
            ax.text(
                x + size/2,
                y + size/2,
                str(i+1),
                ha='center',
                va='center',
                color='white',
                fontsize=8
            )
        
        # Add layer label
        ax.text(
            size * grid_size / 2,
            -20,
            label,
            ha='center',
            va='top',
            fontsize=self.default_params["visual_params"]["label_fontsize"]
        )
        
        # Add shape annotation
        ax.text(
            size * grid_size / 2,
            -35,
            f"Shape: {shape}",
            ha='center',
            va='top',
            fontsize=self.default_params["visual_params"]["shape_fontsize"]
        )
        
        ax.set_xlim(-10, size * grid_size + 10)
        ax.set_ylim(-50, size * grid_size + 10)
        ax.axis('off')
        
        return block
    
    def _draw_3d_stack(self, ax, x, y, w, h, depth, color, edgecolor, alpha=0.7, zorder=1):
        """Draw a 3D stack of rectangles for feature maps."""
        offset = 6  # Perspective offset
        for i in range(depth):
            rect = patches.FancyBboxPatch(
                (x + i*offset, y - i*offset), w, h,
                boxstyle="round,pad=0.02",
                linewidth=1,
                facecolor=color,
                edgecolor=edgecolor,
                alpha=alpha,
                zorder=zorder + i
            )
            ax.add_patch(rect)

    def create_diagram(self, config):
        """Create a CNN architecture diagram based on the provided configuration."""
        import matplotlib.patheffects as pe
        fig = plt.figure(figsize=(14, 7))
        ax = fig.add_subplot(111)
        vp = self.default_params["visual_params"]
        lc = self.default_params["layer_colors"]

        input_size = vp["feature_map_size"]
        x_offset = 0
        y_center = 200
        prev_x = x_offset
        prev_y = y_center
        block_w = input_size
        block_h = input_size
        layer_spacing = vp["layer_spacing"] + 20
        stack_depth = 8
        font = {'fontsize': vp["label_fontsize"]}
        shape_font = {'fontsize': vp["shape_fontsize"]}

        # Draw input
        ax.imshow(self.mnist_sample, cmap='gray', extent=(x_offset, x_offset+block_w, y_center-block_h//2, y_center+block_h//2), zorder=10)
        ax.text(x_offset+block_w/2, y_center-block_h//2-30, "Input Layer", ha='center', va='top', **font, path_effects=[pe.withStroke(linewidth=2, foreground="w")])
        ax.text(x_offset+block_w/2, y_center+block_h//2+10, f"{tuple(config['input_shape'])}", ha='center', va='bottom', **shape_font)
        prev_x = x_offset + block_w
        x_offset = prev_x + layer_spacing

        def draw_conn(x0, y0, x1, y1):
            ax.plot([x0, x1], [y0, y1], color=vp["arrow_color"], lw=2, zorder=20)

        # Conv layers
        for idx, layer in enumerate(config.get('conv_layers', [])):
            actual_maps = layer.get('filters', 32)
            num_maps = min(actual_maps, 8)
            self._draw_3d_stack(ax, x_offset, y_center-block_h//2, block_w, block_h, num_maps, lc["conv"], 'black', alpha=0.7, zorder=5)
            draw_conn(prev_x, y_center, x_offset, y_center)
            label = f"Conv_{idx+1}\n({layer.get('kernel_size',3)}x{layer.get('kernel_size',3)} kernel, {layer.get('padding','valid')})\n({actual_maps} filters)"
            label_y = y_center - block_h//2 - 50
            ax.text(x_offset+block_w/2+12, label_y, label, ha='center', va='top', **font, path_effects=[pe.withStroke(linewidth=2, foreground="w")])
            prev_x = x_offset + block_w + (num_maps-1)*6
            x_offset = prev_x + layer_spacing
        # Pool layers
        for idx, layer in enumerate(config.get('pool_layers', [])):
            actual_maps = 4  # Pooling doesn't change channel count in this simple view
            num_maps = 4
            self._draw_3d_stack(ax, x_offset, y_center-block_h//2, block_w, block_h, num_maps, lc["pool"], 'black', alpha=0.7, zorder=5)
            draw_conn(prev_x, y_center, x_offset, y_center)
            label = f"Pool_{idx+1}\n({layer.get('pool_size',2)}x{layer.get('pool_size',2)}, {layer.get('pool_type','max')})\n({actual_maps} maps)"
            label_y = y_center - block_h//2 - 30
            ax.text(x_offset+block_w/2+12, label_y, label, ha='center', va='top', **font, path_effects=[pe.withStroke(linewidth=2, foreground="w")])
            prev_x = x_offset + block_w + 18
            x_offset = prev_x + layer_spacing
        # Flatten
        if config.get('flatten', True):
            flat_w, flat_h = 40, 80
            flat_x, flat_y = x_offset, y_center-flat_h//2
            ax.add_patch(patches.Polygon([
                (flat_x, flat_y),
                (flat_x+flat_w, flat_y+20),
                (flat_x+flat_w, flat_y+flat_h+20),
                (flat_x, flat_y+flat_h)
            ], closed=True, facecolor=lc["flatten"], edgecolor='black', alpha=0.7, zorder=5))
            draw_conn(prev_x, y_center, flat_x, y_center)
            label_y = flat_y + flat_h + 30
            ax.text(flat_x+flat_w/2, label_y, "Flatten", ha='center', va='top', **font, path_effects=[pe.withStroke(linewidth=2, foreground="w")])
            prev_x = flat_x+flat_w
            x_offset = prev_x + layer_spacing
        # Dense layers
        for idx, dense in enumerate(config.get('dense_layers', [])):
            actual_units = dense.get('units', 128)
            units = min(actual_units, 8)
            node_r = 16
            node_spacing = 2*node_r + 6
            start_y = y_center - (units * node_spacing // 2)
            for n in range(units):
                circle = patches.Circle((x_offset+node_r, start_y + n*node_spacing + node_r), node_r, facecolor=lc["dense"], edgecolor='black', alpha=0.7, zorder=10)
                ax.add_patch(circle)
            draw_conn(prev_x, y_center, x_offset+node_r, y_center)
            label = f"Dense_{idx+1}\n({dense.get('activation','relu')})\n({actual_units} units)"
            label_y = start_y + units*node_spacing + 30
            ax.text(x_offset+node_r, label_y, label, ha='center', va='top', **font, path_effects=[pe.withStroke(linewidth=2, foreground="w")])
            prev_x = x_offset + 2*node_r
            x_offset = prev_x + layer_spacing
        # Output layer
        output_units = config.get('output_units', 10)
        node_r = 16
        node_spacing = 2*node_r + 6
        start_y = y_center - (output_units * node_spacing // 2)
        for i in range(output_units):
            cy = start_y + i*node_spacing + node_r
            circle = patches.Circle((x_offset+node_r, cy), node_r, facecolor=lc["output"], edgecolor='black', linewidth=1.5, zorder=10)
            ax.add_patch(circle)
            ax.text(x_offset+node_r, cy, str(i), ha='center', va='center', color='white', fontsize=12, zorder=11)
        draw_conn(prev_x, y_center, x_offset+node_r, y_center)
        ax.text(x_offset+node_r, start_y-20, "Output Layer", ha='center', va='top', **font, path_effects=[pe.withStroke(linewidth=2, foreground="w")])
        ax.text(x_offset+node_r, start_y+output_units*node_spacing+10, f"({output_units},)", ha='center', va='bottom', **shape_font)
        ax.set_xlim(-vp["padding"], x_offset+node_r*2+vp["padding"])
        ax.set_ylim(0, 400)
        ax.axis('off')
        return fig
    
    def save_figure(self, filename, format='png', dpi=300):
        """Save the current figure to a file."""
        plt.savefig(filename, format=format, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
    
    def close_figure(self):
        """Close the current figure."""
        plt.close() 