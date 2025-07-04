#!/usr/bin/env python3
"""
CNN Configuration Dialog for the Paper-Ready Architecture Generator.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import yaml
import os
from cnn_layer_dialog import CNNLayerDialog

class CNNDialog:
    """Dialog for configuring CNN architecture parameters."""
    
    def __init__(self, parent, config_manager, initial_config=None):
        """Initialize the CNN configuration dialog."""
        self.parent = parent
        self.config_manager = config_manager
        self.result = None
        self.initial_config = initial_config or {}
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("CNN Architecture Configuration")
        self.dialog.geometry("800x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.input_tab = ttk.Frame(notebook)
        self.conv_tab = ttk.Frame(notebook)
        self.pool_tab = ttk.Frame(notebook)
        self.dense_tab = ttk.Frame(notebook)
        self.visual_tab = ttk.Frame(notebook)
        
        notebook.add(self.input_tab, text="Input Layer")
        notebook.add(self.conv_tab, text="Convolutional Layers")
        notebook.add(self.pool_tab, text="Pooling Layers")
        notebook.add(self.dense_tab, text="Dense Layers")
        notebook.add(self.visual_tab, text="Visual Settings")
        
        # Initialize UI components
        self._create_input_tab()
        self._create_conv_tab()
        self._create_pool_tab()
        self._create_dense_tab()
        self._create_visual_tab()
        # If initial_config is provided, populate fields
        self._populate_from_initial_config()
        
        # Create buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create buttons
        ttk.Button(
            button_frame,
            text="Save Configuration",
            command=self._save_config
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Center the dialog
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_input_tab(self):
        """Create the input layer configuration tab."""
        frame = ttk.LabelFrame(self.input_tab, text="Input Layer Parameters", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input shape
        ttk.Label(frame, text="Input Shape:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        shape_frame = ttk.Frame(frame)
        shape_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        self.height_var = tk.StringVar(value="28")
        self.width_var = tk.StringVar(value="28")
        self.channels_var = tk.StringVar(value="1")
        
        ttk.Label(shape_frame, text="Height:").pack(side=tk.LEFT)
        ttk.Entry(shape_frame, textvariable=self.height_var, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(shape_frame, text="Width:").pack(side=tk.LEFT)
        ttk.Entry(shape_frame, textvariable=self.width_var, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(shape_frame, text="Channels:").pack(side=tk.LEFT)
        ttk.Entry(shape_frame, textvariable=self.channels_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Input type
        ttk.Label(frame, text="Input Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.input_type_var = tk.StringVar(value="grayscale")
        ttk.Radiobutton(
            frame,
            text="Grayscale",
            variable=self.input_type_var,
            value="grayscale"
        ).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Radiobutton(
            frame,
            text="RGB",
            variable=self.input_type_var,
            value="rgb"
        ).grid(row=1, column=1, sticky=tk.E, pady=5)
    
    def _create_conv_tab(self):
        """Create the convolutional layers configuration tab."""
        frame = ttk.LabelFrame(self.conv_tab, text="Convolutional Layers", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create listbox for layers
        self.conv_listbox = tk.Listbox(frame, height=10)
        self.conv_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create buttons frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame,
            text="Add Layer",
            command=self._add_conv_layer
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Edit Layer",
            command=self._edit_conv_layer
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Remove Layer",
            command=self._remove_conv_layer
        ).pack(side=tk.LEFT, padx=5)
        
        # Initialize conv layers list
        self.conv_layers = []
    
    def _create_pool_tab(self):
        """Create the pooling layers configuration tab."""
        frame = ttk.LabelFrame(self.pool_tab, text="Pooling Layers", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create listbox for layers
        self.pool_listbox = tk.Listbox(frame, height=10)
        self.pool_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create buttons frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame,
            text="Add Layer",
            command=self._add_pool_layer
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Edit Layer",
            command=self._edit_pool_layer
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Remove Layer",
            command=self._remove_pool_layer
        ).pack(side=tk.LEFT, padx=5)
        
        # Initialize pool layers list
        self.pool_layers = []
    
    def _create_dense_tab(self):
        """Create the dense layers configuration tab."""
        frame = ttk.LabelFrame(self.dense_tab, text="Dense Layers", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create listbox for layers
        self.dense_listbox = tk.Listbox(frame, height=10)
        self.dense_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create buttons frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame,
            text="Add Layer",
            command=self._add_dense_layer
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Edit Layer",
            command=self._edit_dense_layer
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Remove Layer",
            command=self._remove_dense_layer
        ).pack(side=tk.LEFT, padx=5)
        
        # Initialize dense layers list
        self.dense_layers = []
    
    def _create_visual_tab(self):
        """Create the visual settings configuration tab."""
        frame = ttk.LabelFrame(self.visual_tab, text="Visual Settings", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Feature map size
        ttk.Label(frame, text="Feature Map Size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.feature_map_size_var = tk.StringVar(value="40")
        ttk.Entry(frame, textvariable=self.feature_map_size_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Layer spacing
        ttk.Label(frame, text="Layer Spacing:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.layer_spacing_var = tk.StringVar(value="100")
        ttk.Entry(frame, textvariable=self.layer_spacing_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Arrow settings
        ttk.Label(frame, text="Arrow Length:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.arrow_length_var = tk.StringVar(value="30")
        ttk.Entry(frame, textvariable=self.arrow_length_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(frame, text="Arrow Width:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.arrow_width_var = tk.StringVar(value="1.5")
        ttk.Entry(frame, textvariable=self.arrow_width_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Font sizes
        ttk.Label(frame, text="Label Font Size:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.label_fontsize_var = tk.StringVar(value="10")
        ttk.Entry(frame, textvariable=self.label_fontsize_var, width=10).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(frame, text="Shape Font Size:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.shape_fontsize_var = tk.StringVar(value="8")
        ttk.Entry(frame, textvariable=self.shape_fontsize_var, width=10).grid(row=5, column=1, sticky=tk.W, pady=5)
    
    def _add_conv_layer(self):
        """Add a new convolutional layer."""
        dialog = CNNLayerDialog(self.dialog, "conv")
        config = dialog.show()
        if config:
            self.conv_layers.append(config)
            self._update_conv_listbox()
    
    def _edit_conv_layer(self):
        """Edit the selected convolutional layer."""
        selection = self.conv_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a layer to edit.")
            return
        
        index = selection[0]
        if index < len(self.conv_layers):
            dialog = CNNLayerDialog(self.dialog, "conv", self.conv_layers[index])
            config = dialog.show()
            if config:
                self.conv_layers[index] = config
                self._update_conv_listbox()
    
    def _remove_conv_layer(self):
        """Remove the selected convolutional layer."""
        selection = self.conv_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a layer to remove.")
            return
        
        index = selection[0]
        if index < len(self.conv_layers):
            del self.conv_layers[index]
            self._update_conv_listbox()
    
    def _add_pool_layer(self):
        """Add a new pooling layer."""
        dialog = CNNLayerDialog(self.dialog, "pool")
        config = dialog.show()
        if config:
            self.pool_layers.append(config)
            self._update_pool_listbox()
    
    def _edit_pool_layer(self):
        """Edit the selected pooling layer."""
        selection = self.pool_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a layer to edit.")
            return
        
        index = selection[0]
        if index < len(self.pool_layers):
            dialog = CNNLayerDialog(self.dialog, "pool", self.pool_layers[index])
            config = dialog.show()
            if config:
                self.pool_layers[index] = config
                self._update_pool_listbox()
    
    def _remove_pool_layer(self):
        """Remove the selected pooling layer."""
        selection = self.pool_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a layer to remove.")
            return
        
        index = selection[0]
        if index < len(self.pool_layers):
            del self.pool_layers[index]
            self._update_pool_listbox()
    
    def _add_dense_layer(self):
        """Add a new dense layer."""
        dialog = CNNLayerDialog(self.dialog, "dense")
        config = dialog.show()
        if config:
            self.dense_layers.append(config)
            self._update_dense_listbox()
    
    def _edit_dense_layer(self):
        """Edit the selected dense layer."""
        selection = self.dense_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a layer to edit.")
            return
        
        index = selection[0]
        if index < len(self.dense_layers):
            dialog = CNNLayerDialog(self.dialog, "dense", self.dense_layers[index])
            config = dialog.show()
            if config:
                self.dense_layers[index] = config
                self._update_dense_listbox()
    
    def _remove_dense_layer(self):
        """Remove the selected dense layer."""
        selection = self.dense_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a layer to remove.")
            return
        
        index = selection[0]
        if index < len(self.dense_layers):
            del self.dense_layers[index]
            self._update_dense_listbox()
    
    def _update_conv_listbox(self):
        """Update the convolutional layers listbox."""
        self.conv_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.conv_layers):
            filters = layer.get('filters', 32)
            kernel_size = layer.get('kernel_size', 3)
            activation = layer.get('activation', 'relu')
            self.conv_listbox.insert(tk.END, f"Conv {i+1}: {filters} filters, {kernel_size}x{kernel_size}, {activation}")
    
    def _update_pool_listbox(self):
        """Update the pooling layers listbox."""
        self.pool_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.pool_layers):
            pool_type = layer.get('pool_type', 'max')
            pool_size = layer.get('pool_size', 2)
            self.pool_listbox.insert(tk.END, f"Pool {i+1}: {pool_type}, {pool_size}x{pool_size}")
    
    def _update_dense_listbox(self):
        """Update the dense layers listbox."""
        self.dense_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.dense_layers):
            units = layer.get('units', 128)
            activation = layer.get('activation', 'relu')
            self.dense_listbox.insert(tk.END, f"Dense {i+1}: {units} units, {activation}")
    
    def _save_config(self):
        """Save the current configuration."""
        config = {
            "network_type": "cnn",
            "input_shape": [
                int(self.height_var.get()),
                int(self.width_var.get()),
                int(self.channels_var.get())
            ],
            "conv_layers": self.conv_layers,
            "pool_layers": self.pool_layers,
            "dense_layers": self.dense_layers,
            "flatten": True,
            "flatten_shape": [1, 256],
            "output_units": 10,
            "output_activation": "softmax",
            "visual_params": {
                "feature_map_size": int(float(self.feature_map_size_var.get())),
                "layer_spacing": int(float(self.layer_spacing_var.get())),
                "arrow_length": int(float(self.arrow_length_var.get())),
                "arrow_width": float(self.arrow_width_var.get()),
                "label_fontsize": int(float(self.label_fontsize_var.get())),
                "shape_fontsize": int(float(self.shape_fontsize_var.get()))
            }
        }
        
        # Save configuration
        self.config_manager.save_config(config, "cnn_config.yaml")
        self.result = config
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and return the result."""
        self.dialog.wait_window()
        return self.result

    def _populate_from_initial_config(self):
        cfg = self.initial_config
        # Input shape
        if 'input_shape' in cfg:
            shape = cfg['input_shape']
            if len(shape) == 3:
                self.height_var.set(str(shape[0]))
                self.width_var.set(str(shape[1]))
                self.channels_var.set(str(shape[2]))
        # Conv layers
        self.conv_layers = list(cfg.get('conv_layers', []))
        self._update_conv_listbox()
        # Pool layers
        self.pool_layers = list(cfg.get('pool_layers', []))
        self._update_pool_listbox()
        # Dense layers
        self.dense_layers = list(cfg.get('dense_layers', []))
        self._update_dense_listbox()
        # Visual params
        vis = cfg.get('visual_params', {})
        if 'feature_map_size' in vis:
            self.feature_map_size_var.set(str(vis['feature_map_size']))
        if 'layer_spacing' in vis:
            self.layer_spacing_var.set(str(vis['layer_spacing']))
        if 'arrow_length' in vis:
            self.arrow_length_var.set(str(vis['arrow_length']))
        if 'arrow_width' in vis:
            self.arrow_width_var.set(str(vis['arrow_width']))
        if 'label_fontsize' in vis:
            self.label_fontsize_var.set(str(vis['label_fontsize']))
        if 'shape_fontsize' in vis:
            self.shape_fontsize_var.set(str(vis['shape_fontsize'])) 