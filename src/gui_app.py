import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import tkinter.font as tk_font
from PIL import Image, ImageTk
import io
import base64
import os
from typing import Dict, Any

from config_manager import ConfigManager
from mlp_generator import MLPGenerator

class MLPVisualizerGUI:
    """Main GUI application for MLP visualization."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Neural Network Architecture Visualizer")
        self.root.geometry("1400x900")
        
        # Initialize components
        self.config_manager = ConfigManager()
        self.mlp_generator = MLPGenerator()
        self.current_config = self.config_manager.get_default_config()
        
        # GUI variables
        self.preview_image = None
        self.auto_update = tk.BooleanVar(value=True)
        
        self.setup_gui()
        self.update_preview()
    
    def setup_gui(self):
        """Set up the main GUI layout."""
        # Create main frames
        self.create_menu()
        self.create_main_frames()
        self.create_control_panel()
        self.create_preview_panel()
        
        # Bind events
        self.bind_update_events()
    
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Configuration", command=self.new_config)
        file_menu.add_command(label="Load Configuration", command=self.load_config)
        file_menu.add_command(label="Save Configuration", command=self.save_config)
        file_menu.add_separator()
        file_menu.add_command(label="Export Image", command=self.export_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_frames(self):
        """Create main layout frames."""
        # Left panel for controls (increased width to accommodate longer labels)
        self.control_frame = ttk.Frame(self.root, width=450)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.control_frame.pack_propagate(False)
        
        # Right panel for preview
        self.preview_frame = ttk.Frame(self.root)
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_control_panel(self):
        """Create the control panel with all parameters."""
        # Title
        title_label = ttk.Label(self.control_frame, text="MLP Parameters", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Create notebook for organized tabs
        notebook = ttk.Notebook(self.control_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Network Structure Tab
        self.create_structure_tab(notebook)
        
        # Visual Parameters Tab
        self.create_visual_tab(notebook)
        
        # Pruning Tab
        self.create_pruning_tab(notebook)
        
        # Labels Tab
        self.create_labels_tab(notebook)
        
        # Export Tab
        self.create_export_tab(notebook)
        
        # Auto-update checkbox
        auto_update_frame = ttk.Frame(self.control_frame)
        auto_update_frame.pack(fill=tk.X, pady=10)
        
        ttk.Checkbutton(auto_update_frame, text="Auto-update preview", 
                       variable=self.auto_update).pack(side=tk.LEFT)
        
        ttk.Button(auto_update_frame, text="Update", 
                  command=self.update_preview).pack(side=tk.RIGHT)
    
    def create_structure_tab(self, parent):
        """Create network structure controls."""
        structure_frame = ttk.Frame(parent)
        parent.add(structure_frame, text="Network Structure")
        
        # Configure padding for the frame
        structure_frame.grid_configure(padx=10, pady=10)
        
        # Input neurons
        ttk.Label(structure_frame, text="Input Neurons:", width=15).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.input_neurons_var = tk.IntVar(value=self.current_config["network_structure"]["input_neurons"])
        input_spin = ttk.Spinbox(structure_frame, from_=1, to=20, width=10, 
                                textvariable=self.input_neurons_var)
        input_spin.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Hidden layers
        ttk.Label(structure_frame, text="Hidden Layers:", width=15).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.hidden_layers_var = tk.StringVar(value=str(self.current_config["network_structure"]["hidden_layers"])[1:-1])
        hidden_entry = ttk.Entry(structure_frame, textvariable=self.hidden_layers_var, width=15)
        hidden_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Add validation
        def validate_hidden_layers(value):
            """Validate hidden layers input."""
            if not value.strip():
                return True  # Empty is valid
            try:
                # Split by comma and filter out empty strings
                parts = [x.strip() for x in value.split(',')]
                parts = [x for x in parts if x]  # Remove empty strings
                for part in parts:
                    int(part)  # Try to convert to int
                return True
            except ValueError:
                return False
        
        # Register validation function
        vcmd = (self.root.register(validate_hidden_layers), '%P')
        hidden_entry.config(validate='key', validatecommand=vcmd)
        
        ttk.Label(structure_frame, text="e.g., 4,4,3", font=('Arial', 8)).grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # Output neurons
        ttk.Label(structure_frame, text="Output Neurons:", width=15).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.output_neurons_var = tk.IntVar(value=self.current_config["network_structure"]["output_neurons"])
        output_spin = ttk.Spinbox(structure_frame, from_=1, to=20, width=10, 
                                 textvariable=self.output_neurons_var)
        output_spin.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Configure column weights
        structure_frame.columnconfigure(1, weight=1)
    
    def create_visual_tab(self, parent):
        """Create visual parameters controls."""
        visual_frame = ttk.Frame(parent)
        parent.add(visual_frame, text="Visual Parameters")
        
        # Configure padding for the frame
        visual_frame.grid_configure(padx=10, pady=10)
        
        visual_params = self.current_config["visual_params"]
        
        # Node diameter
        ttk.Label(visual_frame, text="Node Diameter:", width=15).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.node_diameter_var = tk.DoubleVar(value=visual_params["node_diameter"])
        diameter_scale = ttk.Scale(visual_frame, from_=10, to=80, orient=tk.HORIZONTAL, 
                                  variable=self.node_diameter_var, length=150)
        diameter_scale.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        diameter_value_label = ttk.Label(visual_frame, text=f"{visual_params['node_diameter']:.0f}")
        diameter_value_label.grid(row=0, column=2, padx=5)
        
        # Layer Colors Section
        ttk.Label(visual_frame, text="Layer Colors:", width=15).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        colors_button_frame = ttk.Frame(visual_frame)
        colors_button_frame.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Button(colors_button_frame, text="Configure Layer Colors...", 
                  command=self.open_layer_colors_dialog).pack(side=tk.LEFT)
        
        # Initialize layer color variables and displays
        self.layer_color_vars = []
        self.layer_color_displays = []
        self.layer_colors_dialog = None
        
        # Create initial layer color variables
        self.initialize_layer_colors()
        
        # Edge width
        ttk.Label(visual_frame, text="Edge Width:", width=15).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.edge_width_var = tk.DoubleVar(value=visual_params["edge_width"])
        width_scale = ttk.Scale(visual_frame, from_=0.5, to=5.0, orient=tk.HORIZONTAL, 
                               variable=self.edge_width_var, length=150)
        width_scale.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        width_value_label = ttk.Label(visual_frame, text=f"{visual_params['edge_width']:.1f}")
        width_value_label.grid(row=3, column=2, padx=5)
        
        # Edge opacity
        ttk.Label(visual_frame, text="Edge Opacity:", width=15).grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.edge_opacity_var = tk.DoubleVar(value=visual_params["edge_opacity"])
        opacity_scale = ttk.Scale(visual_frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL, 
                                 variable=self.edge_opacity_var, length=150)
        opacity_scale.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=5)
        opacity_value_label = ttk.Label(visual_frame, text=f"{visual_params['edge_opacity']:.1f}")
        opacity_value_label.grid(row=4, column=2, padx=5)
        
        # Layer spacing
        ttk.Label(visual_frame, text="Layer Spacing:", width=15).grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.layer_spacing_var = tk.DoubleVar(value=visual_params["layer_spacing"])
        spacing_scale = ttk.Scale(visual_frame, from_=50, to=300, orient=tk.HORIZONTAL, 
                                 variable=self.layer_spacing_var, length=150)
        spacing_scale.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=5)
        spacing_value_label = ttk.Label(visual_frame, text=f"{visual_params['layer_spacing']:.0f}")
        spacing_value_label.grid(row=5, column=2, padx=5)
        
        # Node spacing
        ttk.Label(visual_frame, text="Node Spacing:", width=15).grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        self.node_spacing_var = tk.DoubleVar(value=visual_params["node_spacing"])
        node_spacing_scale = ttk.Scale(visual_frame, from_=20, to=120, orient=tk.HORIZONTAL, 
                                      variable=self.node_spacing_var, length=150)
        node_spacing_scale.grid(row=6, column=1, sticky=tk.EW, pady=5, padx=5)
        node_spacing_value_label = ttk.Label(visual_frame, text=f"{visual_params['node_spacing']:.0f}")
        node_spacing_value_label.grid(row=6, column=2, padx=5)
        
        # Configure column weights
        visual_frame.columnconfigure(1, weight=1)
        
        # Store references to value labels for updates
        self.value_labels = {
            'diameter': diameter_value_label,
            'width': width_value_label,
            'opacity': opacity_value_label,
            'spacing': spacing_value_label,
            'node_spacing': node_spacing_value_label
        }
    
    def create_pruning_tab(self, parent):
        """Create pruning controls."""
        pruning_frame = ttk.Frame(parent)
        parent.add(pruning_frame, text="Pruning")
        
        # Configure padding for the frame
        pruning_frame.grid_configure(padx=10, pady=10)
        
        pruning_config = self.current_config.get("pruning", {"enabled": False, "neuron_prune_percentage": 0.0, "synapse_prune_percentage": 0.0})
        
        # Enable pruning checkbox
        self.pruning_enabled_var = tk.BooleanVar(value=pruning_config["enabled"])
        enable_checkbox = ttk.Checkbutton(pruning_frame, text="Enable Network Pruning", 
                                         variable=self.pruning_enabled_var)
        enable_checkbox.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=10, padx=5)
        
        # Information label
        info_label = ttk.Label(pruning_frame, 
                              text="Pruning removes neurons and synapses to simulate sparse networks.\nOnly hidden layer neurons are pruned (input/output preserved).",
                              font=('Arial', 9), justify=tk.LEFT, foreground='gray')
        info_label.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky=tk.W)
        
        # Neuron pruning percentage
        ttk.Label(pruning_frame, text="Neuron Pruning (%):", width=18).grid(row=2, column=0, sticky=tk.W, pady=10, padx=5)
        self.neuron_prune_var = tk.DoubleVar(value=pruning_config["neuron_prune_percentage"])
        neuron_scale = ttk.Scale(pruning_frame, from_=0, to=90, orient=tk.HORIZONTAL, 
                                variable=self.neuron_prune_var, length=150)
        neuron_scale.grid(row=2, column=1, sticky=tk.EW, pady=10, padx=5)
        neuron_value_label = ttk.Label(pruning_frame, text=f"{pruning_config['neuron_prune_percentage']:.0f}%")
        neuron_value_label.grid(row=2, column=2, padx=5)
        
        # Synapse pruning percentage
        ttk.Label(pruning_frame, text="Synapse Pruning (%):", width=18).grid(row=3, column=0, sticky=tk.W, pady=10, padx=5)
        self.synapse_prune_var = tk.DoubleVar(value=pruning_config["synapse_prune_percentage"])
        synapse_scale = ttk.Scale(pruning_frame, from_=0, to=90, orient=tk.HORIZONTAL, 
                                 variable=self.synapse_prune_var, length=150)
        synapse_scale.grid(row=3, column=1, sticky=tk.EW, pady=10, padx=5)
        synapse_value_label = ttk.Label(pruning_frame, text=f"{pruning_config['synapse_prune_percentage']:.0f}%")
        synapse_value_label.grid(row=3, column=2, padx=5)
        
        # Button to apply random pruning
        random_button = ttk.Button(pruning_frame, text="Apply Random Pruning", 
                                  command=self.apply_random_pruning)
        random_button.grid(row=4, column=0, columnspan=2, pady=15, padx=5, sticky=tk.W)
        
        # Configure column weights
        pruning_frame.columnconfigure(1, weight=1)
        
        # Store references to value labels for updates
        if not hasattr(self, 'pruning_value_labels'):
            self.pruning_value_labels = {}
        self.pruning_value_labels.update({
            'neuron': neuron_value_label,
            'synapse': synapse_value_label
        })
        
        # Update the update_value_labels method to include pruning labels
        original_update = self.update_value_labels
        def updated_update_value_labels():
            original_update()
            try:
                if hasattr(self, 'pruning_value_labels'):
                    self.pruning_value_labels['neuron'].config(text=f"{self.neuron_prune_var.get():.0f}%")
                    self.pruning_value_labels['synapse'].config(text=f"{self.synapse_prune_var.get():.0f}%")
            except:
                pass
        self.update_value_labels = updated_update_value_labels
    
    def apply_random_pruning(self):
        """Apply random pruning with current settings."""
        # Enable pruning
        self.pruning_enabled_var.set(True)
        # Force update preview
        self.update_preview()
    
    def create_labels_tab(self, parent):
        """Create labels controls."""
        labels_frame = ttk.Frame(parent)
        parent.add(labels_frame, text="Labels")
        
        # Configure padding for the frame
        labels_frame.grid_configure(padx=10, pady=10)
        
        labels_config = self.current_config["labels"]
        
        # Show labels checkbox
        self.show_labels_var = tk.BooleanVar(value=labels_config["show_layer_labels"])
        ttk.Checkbutton(labels_frame, text="Show Layer Labels", 
                       variable=self.show_labels_var).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=10, padx=5)
        
        # Label texts
        ttk.Label(labels_frame, text="Input Label:", width=15).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.input_label_var = tk.StringVar(value=labels_config["input_label"])
        ttk.Entry(labels_frame, textvariable=self.input_label_var, width=25).grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        
        ttk.Label(labels_frame, text="Hidden Label:", width=15).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.hidden_label_var = tk.StringVar(value=labels_config["hidden_label"])
        ttk.Entry(labels_frame, textvariable=self.hidden_label_var, width=25).grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        
        ttk.Label(labels_frame, text="Output Label:", width=15).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.output_label_var = tk.StringVar(value=labels_config["output_label"])
        ttk.Entry(labels_frame, textvariable=self.output_label_var, width=25).grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Configure column weights
        labels_frame.columnconfigure(1, weight=1)
    
    def create_export_tab(self, parent):
        """Create export settings controls."""
        export_frame = ttk.Frame(parent)
        parent.add(export_frame, text="Export Settings")
        
        # Configure padding for the frame
        export_frame.grid_configure(padx=10, pady=10)
        
        export_config = self.current_config["export"]
        
        # Dimensions
        ttk.Label(export_frame, text="Width (pixels):", width=15).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.width_var = tk.IntVar(value=export_config["width"])
        ttk.Entry(export_frame, textvariable=self.width_var, width=15).grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        
        ttk.Label(export_frame, text="Height (pixels):", width=15).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.height_var = tk.IntVar(value=export_config["height"])
        ttk.Entry(export_frame, textvariable=self.height_var, width=15).grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        
        # DPI
        ttk.Label(export_frame, text="DPI (resolution):", width=15).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.dpi_var = tk.IntVar(value=export_config["dpi"])
        ttk.Entry(export_frame, textvariable=self.dpi_var, width=15).grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        
        # Format recommendations
        format_info = ttk.Label(export_frame, text="Recommendations:\n• PNG/JPEG: 300+ DPI for papers\n• SVG: DPI affects preview only\n• PDF: Vector format, DPI for raster elements", 
                               font=('Arial', 9), justify=tk.LEFT, foreground='gray')
        format_info.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        
        # Configure column weights
        export_frame.columnconfigure(1, weight=1)
    
    def create_preview_panel(self):
        """Create the preview panel."""
        # Title
        title_label = ttk.Label(self.preview_frame, text="Preview", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(self.preview_frame, bg='white', 
                                       relief=tk.SUNKEN, borderwidth=2)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def bind_update_events(self):
        """Bind events for auto-update."""
        # Bind all variable changes to update method
        variables = [
            self.input_neurons_var, self.output_neurons_var, self.hidden_layers_var,
            self.node_diameter_var, self.edge_width_var,
            self.edge_opacity_var, self.layer_spacing_var, self.node_spacing_var,
            self.show_labels_var, self.input_label_var, self.hidden_label_var,
            self.output_label_var, self.width_var, self.height_var, self.dpi_var,
            self.pruning_enabled_var, self.neuron_prune_var, self.synapse_prune_var
        ]
        
        for var in variables:
            if hasattr(var, 'trace'):
                var.trace('w', self.on_parameter_change)
        
        # Special binding for network structure changes
        self.input_neurons_var.trace('w', self.on_structure_change)
        self.output_neurons_var.trace('w', self.on_structure_change)
        self.hidden_layers_var.trace('w', self.on_structure_change)
    
    def on_structure_change(self, *args):
        """Handle network structure changes."""
        self.root.after_idle(self.recreate_layer_colors)
        self.on_parameter_change()
    
    def recreate_layer_colors(self):
        """Recreate layer color variables when structure changes."""
        self.initialize_layer_colors()
        
        # If dialog is open, refresh it
        if self.layer_colors_dialog is not None and self.layer_colors_dialog.winfo_exists():
            # Clear the dialog content and recreate
            for widget in self.layer_colors_dialog.winfo_children():
                if isinstance(widget, ttk.Frame):
                    # Find the scrollable frame and recreate controls
                    canvas = None
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Canvas):
                            canvas = child
                            break
                    if canvas:
                        scrollable_frame = canvas.nametowidget(canvas.find_all()[0])
                        self.create_dialog_layer_controls(scrollable_frame)
                    break
        
    def on_parameter_change(self, *args):
        """Handle parameter changes."""
        # Update value labels
        self.update_value_labels()
        
        if self.auto_update.get():
            self.root.after_idle(self.update_preview)
    
    def update_value_labels(self):
        """Update the value labels next to sliders."""
        try:
            if hasattr(self, 'value_labels'):
                self.value_labels['diameter'].config(text=f"{self.node_diameter_var.get():.0f}")
                self.value_labels['width'].config(text=f"{self.edge_width_var.get():.1f}")
                self.value_labels['opacity'].config(text=f"{self.edge_opacity_var.get():.1f}")
                self.value_labels['spacing'].config(text=f"{self.layer_spacing_var.get():.0f}")
                self.value_labels['node_spacing'].config(text=f"{self.node_spacing_var.get():.0f}")
        except:
            pass  # Ignore errors during initialization
    
    def initialize_layer_colors(self):
        """Initialize layer color variables without GUI controls."""
        # Get current network structure
        try:
            hidden_layers_str = self.hidden_layers_var.get().strip()
            if hidden_layers_str:
                # Split by comma and filter out empty strings
                layer_parts = [x.strip() for x in hidden_layers_str.split(',')]
                layer_parts = [x for x in layer_parts if x]  # Remove empty strings
                hidden_layers = [int(x) for x in layer_parts]
            else:
                hidden_layers = []
        except:
            hidden_layers = []
        
        # Calculate total layers needed
        total_layers = 1 + len(hidden_layers) + 1  # input + hidden + output
        
        # Ensure we have enough colors
        self.current_config = self.config_manager.ensure_layer_colors(self.current_config)
        layer_colors = self.current_config["visual_params"]["layer_colors"]
        
        # Clear existing variables
        self.layer_color_vars.clear()
        
        # Create color variables
        for i in range(total_layers):
            if i < len(layer_colors):
                color = layer_colors[i]
            else:
                color = "#4A90E2"  # fallback
            
            color_var = tk.StringVar(value=color)
            color_var.trace('w', self.on_parameter_change)
            self.layer_color_vars.append(color_var)
    
    def open_layer_colors_dialog(self):
        """Open the layer colors configuration dialog."""
        if self.layer_colors_dialog is not None and self.layer_colors_dialog.winfo_exists():
            self.layer_colors_dialog.lift()
            return
        
        # Create dialog window
        self.layer_colors_dialog = tk.Toplevel(self.root)
        self.layer_colors_dialog.title("Configure Layer Colors")
        self.layer_colors_dialog.geometry("400x500")
        self.layer_colors_dialog.resizable(True, True)
        
        # Make it modal
        self.layer_colors_dialog.transient(self.root)
        self.layer_colors_dialog.grab_set()
        
        # Create main frame with scrollbar
        main_frame = ttk.Frame(self.layer_colors_dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Layer Colors Configuration", 
                               font=('Arial', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Create scrollable frame
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create layer color controls in the scrollable frame
        self.create_dialog_layer_controls(scrollable_frame)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.layer_colors_dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Preset buttons
        presets_frame = ttk.LabelFrame(buttons_frame, text="Color Presets")
        presets_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(presets_frame, text="Default", 
                  command=self.apply_default_colors).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(presets_frame, text="Academic (Grayscale)", 
                  command=self.apply_academic_colors).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(presets_frame, text="Gradient (Blue→Red)", 
                  command=self.apply_gradient_colors).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(buttons_frame)
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Close", 
                  command=self.layer_colors_dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(action_frame, text="Apply & Close", 
                  command=self.apply_and_close_colors).pack(side=tk.RIGHT, padx=5)
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_dialog_layer_controls(self, parent):
        """Create layer color controls in the dialog."""
        # Clear existing displays
        self.layer_color_displays.clear()
        
        # Get current network structure
        try:
            hidden_layers_str = self.hidden_layers_var.get().strip()
            if hidden_layers_str:
                # Split by comma and filter out empty strings
                layer_parts = [x.strip() for x in hidden_layers_str.split(',')]
                layer_parts = [x for x in layer_parts if x]  # Remove empty strings
                hidden_layers = [int(x) for x in layer_parts]
            else:
                hidden_layers = []
        except:
            hidden_layers = []
        
        # Calculate layer names
        layer_names = ["Input"]
        for i, neurons in enumerate(hidden_layers):
            layer_names.append(f"Hidden {i+1} ({neurons} neurons)")
        layer_names.append("Output")
        
        # Ensure we have enough color variables
        while len(self.layer_color_vars) < len(layer_names):
            color_var = tk.StringVar(value="#4A90E2")
            color_var.trace('w', self.on_parameter_change)
            self.layer_color_vars.append(color_var)
        
        # Create controls for each layer
        for i, name in enumerate(layer_names):
            if i >= len(self.layer_color_vars):
                continue
                
            # Layer frame
            layer_frame = ttk.Frame(parent)
            layer_frame.pack(fill=tk.X, pady=5)
            
            # Layer name label
            name_label = ttk.Label(layer_frame, text=name, width=20, anchor='w')
            name_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Color display
            color = self.layer_color_vars[i].get()
            color_display = tk.Label(layer_frame, width=6, height=2, bg=color, 
                                   relief=tk.RAISED, text=color, fg='white' if self._is_dark_color(color) else 'black',
                                   font=('Arial', 7))
            color_display.pack(side=tk.LEFT, padx=(0, 5))
            self.layer_color_displays.append(color_display)
            
            # Hex color entry with validation
            def validate_hex_input(value):
                """Validate hex color input as user types."""
                if not value:
                    return True  # Empty is valid (will be handled later)
                if not value.startswith('#'):
                    return value == '#'  # Allow typing '#' at start
                if len(value) > 7:
                    return False  # Too long
                try:
                    if len(value) > 1:
                        int(value[1:], 16)  # Try to parse hex digits
                    return True
                except ValueError:
                    return False
            
            vcmd_hex = (self.root.register(validate_hex_input), '%P')
            hex_entry = ttk.Entry(layer_frame, textvariable=self.layer_color_vars[i], width=8, 
                                 font=('Courier', 9), validate='key', validatecommand=vcmd_hex)
            hex_entry.pack(side=tk.LEFT, padx=(0, 5))
            
            # Update display when hex entry changes
            def update_color_display(idx=i):
                try:
                    color = self.layer_color_vars[idx].get()
                    if self._is_valid_hex_color(color):
                        self.layer_color_displays[idx].config(
                            bg=color, 
                            text=color,
                            fg='white' if self._is_dark_color(color) else 'black'
                        )
                except:
                    pass
            
            self.layer_color_vars[i].trace('w', lambda *args, idx=i: update_color_display(idx))
            
            # Choose button
            choose_btn = ttk.Button(layer_frame, text="Pick", 
                                   command=lambda idx=i: self.choose_layer_color_dialog(idx))
            choose_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            # Random color button
            random_btn = ttk.Button(layer_frame, text="Random", 
                                   command=lambda idx=i: self.random_layer_color(idx))
            random_btn.pack(side=tk.LEFT)
    
    def _is_dark_color(self, hex_color):
        """Check if a color is dark (for text contrast)."""
        try:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance < 0.5
        except:
            return False
    
    def _is_valid_hex_color(self, color):
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
    
    def choose_layer_color_dialog(self, layer_idx):
        """Open color chooser dialog for specific layer in the dialog."""
        current_color = self.layer_color_vars[layer_idx].get()
        color = colorchooser.askcolor(color=current_color)
        if color[1]:  # If user didn't cancel
            self.layer_color_vars[layer_idx].set(color[1])
            if layer_idx < len(self.layer_color_displays):
                self.layer_color_displays[layer_idx].config(
                    bg=color[1], 
                    text=color[1],
                    fg='white' if self._is_dark_color(color[1]) else 'black'
                )
            if self.auto_update.get():
                self.update_preview()
    
    def random_layer_color(self, layer_idx):
        """Set a random color for the specified layer."""
        import random
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", 
                 "#F7DC6F", "#BB8FCE", "#85C1E9", "#F8C471", "#82E0AA",
                 "#F1948A", "#85929E", "#5DADE2", "#58D68D", "#F4D03F"]
        
        random_color = random.choice(colors)
        self.layer_color_vars[layer_idx].set(random_color)
        if layer_idx < len(self.layer_color_displays):
            self.layer_color_displays[layer_idx].config(
                bg=random_color, 
                text=random_color,
                fg='white' if self._is_dark_color(random_color) else 'black'
            )
        if self.auto_update.get():
            self.update_preview()
    
    def apply_default_colors(self):
        """Apply default color scheme."""
        default_colors = ["#4A90E2", "#50C878", "#FF6B6B", "#FFD93D", "#9B59B6", 
                         "#E67E22", "#1ABC9C", "#34495E", "#E74C3C", "#3498DB"]
        
        for i, color_var in enumerate(self.layer_color_vars):
            color = default_colors[i % len(default_colors)]
            color_var.set(color)
            if i < len(self.layer_color_displays):
                self.layer_color_displays[i].config(
                    bg=color, 
                    text=color,
                    fg='white' if self._is_dark_color(color) else 'black'
                )
        if self.auto_update.get():
            self.update_preview()
    
    def apply_academic_colors(self):
        """Apply academic (grayscale) color scheme."""
        gray_colors = ["#2D3748", "#4A5568", "#718096", "#A0AEC0", "#CBD5E0",
                      "#E2E8F0", "#F7FAFC", "#1A202C", "#2D3748", "#4A5568"]
        
        for i, color_var in enumerate(self.layer_color_vars):
            color = gray_colors[i % len(gray_colors)]
            color_var.set(color)
            if i < len(self.layer_color_displays):
                self.layer_color_displays[i].config(
                    bg=color, 
                    text=color,
                    fg='white' if self._is_dark_color(color) else 'black'
                )
        if self.auto_update.get():
            self.update_preview()
    
    def apply_gradient_colors(self):
        """Apply gradient (blue to red) color scheme."""
        def interpolate_color(start_color, end_color, factor):
            """Interpolate between two hex colors."""
            start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
            end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
            
            rgb = [int(start_rgb[i] + factor * (end_rgb[i] - start_rgb[i])) for i in range(3)]
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        
        start_color = "#1E3A8A"  # Dark blue
        end_color = "#DC2626"    # Dark red
        
        num_layers = len(self.layer_color_vars)
        for i, color_var in enumerate(self.layer_color_vars):
            factor = i / max(1, num_layers - 1)  # Avoid division by zero
            color = interpolate_color(start_color, end_color, factor)
            color_var.set(color)
            if i < len(self.layer_color_displays):
                self.layer_color_displays[i].config(
                    bg=color, 
                    text=color,
                    fg='white' if self._is_dark_color(color) else 'black'
                )
        if self.auto_update.get():
            self.update_preview()
    
    def apply_and_close_colors(self):
        """Apply colors and close dialog."""
        if self.auto_update.get():
            self.update_preview()
        self.layer_colors_dialog.destroy()
    
    def update_config_from_gui(self):
        """Update current config from GUI values."""
        try:
            # Parse hidden layers with better error handling
            hidden_layers_str = self.hidden_layers_var.get().strip()
            if hidden_layers_str:
                # Split by comma and filter out empty strings
                layer_parts = [x.strip() for x in hidden_layers_str.split(',')]
                layer_parts = [x for x in layer_parts if x]  # Remove empty strings
                hidden_layers = [int(x) for x in layer_parts]
            else:
                hidden_layers = []
            
            self.current_config.update({
                "network_structure": {
                    "input_neurons": self.input_neurons_var.get(),
                    "hidden_layers": hidden_layers,
                    "output_neurons": self.output_neurons_var.get()
                },
                "visual_params": {
                    "node_diameter": self.node_diameter_var.get(),
                    "node_color": self.layer_color_vars[0].get() if self.layer_color_vars else "#4A90E2",
                    "layer_colors": [var.get() for var in self.layer_color_vars],
                    "edge_width": self.edge_width_var.get(),
                    "edge_opacity": self.edge_opacity_var.get(),
                    "layer_spacing": self.layer_spacing_var.get(),
                    "node_spacing": self.node_spacing_var.get()
                },
                "pruning": {
                    "enabled": self.pruning_enabled_var.get(),
                    "neuron_prune_percentage": self.neuron_prune_var.get(),
                    "synapse_prune_percentage": self.synapse_prune_var.get()
                },
                "labels": {
                    "show_layer_labels": self.show_labels_var.get(),
                    "input_label": self.input_label_var.get(),
                    "hidden_label": self.hidden_label_var.get(),
                    "output_label": self.output_label_var.get()
                },
                "export": {
                    "width": self.width_var.get(),
                    "height": self.height_var.get(),
                    "dpi": self.dpi_var.get(),
                    "background_color": "white"
                }
            })
            return True
        except ValueError as e:
            # Handle parsing errors more gracefully
            print(f"Parameter parsing error: {e}")
            return False
        except Exception as e:
            # Handle other errors without showing dialog to prevent recursion
            print(f"Config update error: {e}")
            return False
    
    def update_preview(self):
        """Update the preview image."""
        # Prevent recursive calls during error states
        if hasattr(self, '_updating_preview') and self._updating_preview:
            return
        
        self._updating_preview = True
        
        try:
            if not self.update_config_from_gui():
                return
            
            # Generate new diagram
            self.mlp_generator.close_figure()
            fig = self.mlp_generator.create_diagram(self.current_config)
            
            # Convert to image for display
            img_data = self.mlp_generator.get_figure_as_base64('png', dpi=100)
            
            # Display in canvas
            img_bytes = base64.b64decode(img_data)
            img = Image.open(io.BytesIO(img_bytes))
            
            # Resize to fit canvas
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Canvas is initialized
                img.thumbnail((canvas_width-20, canvas_height-20), Image.Resampling.LANCZOS)
            
            self.preview_image = ImageTk.PhotoImage(img)
            
            # Clear canvas and display image
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(
                self.preview_canvas.winfo_width()//2,
                self.preview_canvas.winfo_height()//2,
                image=self.preview_image
            )
            
            # Auto-save configuration
            self.config_manager.auto_save_config(self.current_config)
            
        except Exception as e:
            print(f"Preview Error: {e}")  # Use print instead of messagebox to prevent recursion
        finally:
            self._updating_preview = False
    
    def new_config(self):
        """Create new configuration."""
        self.current_config = self.config_manager.get_default_config()
        self.load_config_to_gui()
        self.update_preview()
    
    def load_config(self):
        """Load configuration from file."""
        config_files = self.config_manager.get_config_files()
        if not config_files:
            messagebox.showinfo("No Configs", "No saved configurations found.")
            return
        
        # Simple dialog to choose config
        filepath = filedialog.askopenfilename(
            title="Load Configuration",
            initialdir=self.config_manager.config_dir,
            filetypes=[("YAML files", "*.yaml"), ("JSON files", "*.json")]
        )
        
        if filepath:
            try:
                self.current_config = self.config_manager.load_config(filepath)
                self.load_config_to_gui()
                self.update_preview()
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def save_config(self):
        """Save current configuration."""
        if not self.update_config_from_gui():
            return
        
        try:
            filepath = self.config_manager.save_config(self.current_config)
            messagebox.showinfo("Success", f"Configuration saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def load_config_to_gui(self):
        """Load configuration values to GUI."""
        config = self.current_config
        
        # Network structure
        self.input_neurons_var.set(config["network_structure"]["input_neurons"])
        self.hidden_layers_var.set(str(config["network_structure"]["hidden_layers"])[1:-1])
        self.output_neurons_var.set(config["network_structure"]["output_neurons"])
        
        # Visual parameters
        visual = config["visual_params"]
        self.node_diameter_var.set(visual["node_diameter"])
        self.edge_width_var.set(visual["edge_width"])
        self.edge_opacity_var.set(visual["edge_opacity"])
        self.layer_spacing_var.set(visual["layer_spacing"])
        self.node_spacing_var.set(visual["node_spacing"])
        
        # Recreate layer color variables with loaded colors
        self.initialize_layer_colors()
        
        # Pruning parameters
        pruning = config.get("pruning", {"enabled": False, "neuron_prune_percentage": 0.0, "synapse_prune_percentage": 0.0})
        self.pruning_enabled_var.set(pruning["enabled"])
        self.neuron_prune_var.set(pruning["neuron_prune_percentage"])
        self.synapse_prune_var.set(pruning["synapse_prune_percentage"])
        
        # Labels
        labels = config["labels"]
        self.show_labels_var.set(labels["show_layer_labels"])
        self.input_label_var.set(labels["input_label"])
        self.hidden_label_var.set(labels["hidden_label"])
        self.output_label_var.set(labels["output_label"])
        
        # Export
        export = config["export"]
        self.width_var.set(export["width"])
        self.height_var.set(export["height"])
        self.dpi_var.set(export["dpi"])
    
    def export_image(self):
        """Export current diagram to file."""
        if not self.update_config_from_gui():
            return
        
        # Choose file
        filepath = filedialog.asksaveasfilename(
            title="Export Image",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("SVG files", "*.svg"),
                ("PDF files", "*.pdf"),
                ("JPEG files", "*.jpg")
            ]
        )
        
        if filepath:
            try:
                # Generate high-quality image
                self.mlp_generator.close_figure()
                fig = self.mlp_generator.create_diagram(self.current_config)
                
                # Determine format from extension
                format_ext = os.path.splitext(filepath)[1].lower().lstrip('.')
                if format_ext == 'jpg':
                    format_ext = 'jpeg'
                
                # Save with high DPI
                self.mlp_generator.save_figure(filepath, format_ext, self.dpi_var.get())
                
                # Also save the configuration
                config_path = os.path.splitext(filepath)[0] + "_config.yaml"
                self.config_manager.save_config(self.current_config, os.path.basename(config_path))
                
                messagebox.showinfo("Success", f"Image exported to {filepath}\nConfiguration saved to {config_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export image: {str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo("About", 
                           "Neural Network Architecture Visualizer v1.0\n\n"
                           "Create paper-ready visualizations of Multi-Layer Perceptrons\n"
                           "with customizable parameters and clean, minimalist design.")
    
    def run(self):
        """Start the GUI application."""
        # Initial preview update after a delay to ensure canvas is ready
        self.root.after(100, self.update_preview)
        self.root.mainloop()

def main():
    """Main entry point."""
    app = MLPVisualizerGUI()
    app.run()

if __name__ == "__main__":
    main() 