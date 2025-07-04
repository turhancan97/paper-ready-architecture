#!/usr/bin/env python3
"""
CNN Layer Configuration Dialog for the Paper-Ready Architecture Generator.
"""

import tkinter as tk
from tkinter import ttk

class CNNLayerDialog:
    """Dialog for configuring individual CNN layers."""
    
    def __init__(self, parent, layer_type, layer_config=None):
        """Initialize the CNN layer configuration dialog."""
        self.parent = parent
        self.layer_type = layer_type
        self.layer_config = layer_config or {}
        self.result = None
        
        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"{layer_type.capitalize()} Layer Configuration")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create form
        self._create_form(main_frame)
        
        # Create buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create buttons
        ttk.Button(
            button_frame,
            text="OK",
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
    
    def _create_form(self, parent):
        """Create the form based on layer type."""
        # Create a separate frame for the form that uses grid
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        if self.layer_type == "conv":
            self._create_conv_form(form_frame)
        elif self.layer_type == "pool":
            self._create_pool_form(form_frame)
        elif self.layer_type == "dense":
            self._create_dense_form(form_frame)
    
    def _create_conv_form(self, parent):
        """Create the convolutional layer form."""
        # Number of filters
        ttk.Label(parent, text="Number of Filters:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.filters_var = tk.StringVar(value=str(self.layer_config.get("filters", 32)))
        ttk.Entry(parent, textvariable=self.filters_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Kernel size
        ttk.Label(parent, text="Kernel Size:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.kernel_size_var = tk.StringVar(value=str(self.layer_config.get("kernel_size", 3)))
        ttk.Entry(parent, textvariable=self.kernel_size_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Stride
        ttk.Label(parent, text="Stride:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.stride_var = tk.StringVar(value=str(self.layer_config.get("stride", 1)))
        ttk.Entry(parent, textvariable=self.stride_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Padding
        ttk.Label(parent, text="Padding:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.padding_var = tk.StringVar(value=self.layer_config.get("padding", "valid"))
        ttk.Combobox(
            parent,
            textvariable=self.padding_var,
            values=["valid", "same"],
            width=10,
            state="readonly"
        ).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Activation
        ttk.Label(parent, text="Activation:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.activation_var = tk.StringVar(value=self.layer_config.get("activation", "relu"))
        ttk.Combobox(
            parent,
            textvariable=self.activation_var,
            values=["relu", "leaky_relu", "sigmoid", "tanh", "none"],
            width=10,
            state="readonly"
        ).grid(row=4, column=1, sticky=tk.W, pady=5)
    
    def _create_pool_form(self, parent):
        """Create the pooling layer form."""
        # Pool type
        ttk.Label(parent, text="Pool Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pool_type_var = tk.StringVar(value=self.layer_config.get("pool_type", "max"))
        ttk.Combobox(
            parent,
            textvariable=self.pool_type_var,
            values=["max", "average"],
            width=10,
            state="readonly"
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Pool size
        ttk.Label(parent, text="Pool Size:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pool_size_var = tk.StringVar(value=str(self.layer_config.get("pool_size", 2)))
        ttk.Entry(parent, textvariable=self.pool_size_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Stride
        ttk.Label(parent, text="Stride:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.stride_var = tk.StringVar(value=str(self.layer_config.get("stride", 2)))
        ttk.Entry(parent, textvariable=self.stride_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Padding
        ttk.Label(parent, text="Padding:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.padding_var = tk.StringVar(value=self.layer_config.get("padding", "valid"))
        ttk.Combobox(
            parent,
            textvariable=self.padding_var,
            values=["valid", "same"],
            width=10,
            state="readonly"
        ).grid(row=3, column=1, sticky=tk.W, pady=5)
    
    def _create_dense_form(self, parent):
        """Create the dense layer form."""
        # Number of units
        ttk.Label(parent, text="Number of Units:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.units_var = tk.StringVar(value=str(self.layer_config.get("units", 128)))
        ttk.Entry(parent, textvariable=self.units_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Activation
        ttk.Label(parent, text="Activation:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.activation_var = tk.StringVar(value=self.layer_config.get("activation", "relu"))
        ttk.Combobox(
            parent,
            textvariable=self.activation_var,
            values=["relu", "leaky_relu", "sigmoid", "tanh", "softmax", "none"],
            width=10,
            state="readonly"
        ).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Use bias
        ttk.Label(parent, text="Use Bias:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.use_bias_var = tk.BooleanVar(value=self.layer_config.get("use_bias", True))
        ttk.Checkbutton(
            parent,
            variable=self.use_bias_var
        ).grid(row=2, column=1, sticky=tk.W, pady=5)
    
    def _save_config(self):
        """Save the current configuration."""
        try:
            if self.layer_type == "conv":
                config = {
                    "filters": int(self.filters_var.get()),
                    "kernel_size": int(self.kernel_size_var.get()),
                    "stride": int(self.stride_var.get()),
                    "padding": self.padding_var.get(),
                    "activation": self.activation_var.get()
                }
            elif self.layer_type == "pool":
                config = {
                    "pool_type": self.pool_type_var.get(),
                    "pool_size": int(self.pool_size_var.get()),
                    "stride": int(self.stride_var.get()),
                    "padding": self.padding_var.get()
                }
            elif self.layer_type == "dense":
                config = {
                    "units": int(self.units_var.get()),
                    "activation": self.activation_var.get(),
                    "use_bias": self.use_bias_var.get()
                }
            
            self.result = config
            self.dialog.destroy()
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def show(self):
        """Show the dialog and return the result."""
        self.dialog.wait_window()
        return self.result 