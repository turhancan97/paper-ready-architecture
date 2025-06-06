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
        
        # Node color
        ttk.Label(visual_frame, text="Node Color:", width=15).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.node_color_var = tk.StringVar(value=visual_params["node_color"])
        color_frame = ttk.Frame(visual_frame)
        color_frame.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        self.color_display = tk.Label(color_frame, width=4, height=1, 
                                     bg=visual_params["node_color"], relief=tk.RAISED)
        self.color_display.pack(side=tk.LEFT)
        ttk.Button(color_frame, text="Choose", 
                  command=self.choose_color).pack(side=tk.LEFT, padx=(5,0))
        
        # Edge width
        ttk.Label(visual_frame, text="Edge Width:", width=15).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.edge_width_var = tk.DoubleVar(value=visual_params["edge_width"])
        width_scale = ttk.Scale(visual_frame, from_=0.5, to=5.0, orient=tk.HORIZONTAL, 
                               variable=self.edge_width_var, length=150)
        width_scale.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        width_value_label = ttk.Label(visual_frame, text=f"{visual_params['edge_width']:.1f}")
        width_value_label.grid(row=2, column=2, padx=5)
        
        # Edge opacity
        ttk.Label(visual_frame, text="Edge Opacity:", width=15).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.edge_opacity_var = tk.DoubleVar(value=visual_params["edge_opacity"])
        opacity_scale = ttk.Scale(visual_frame, from_=0.1, to=1.0, orient=tk.HORIZONTAL, 
                                 variable=self.edge_opacity_var, length=150)
        opacity_scale.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        opacity_value_label = ttk.Label(visual_frame, text=f"{visual_params['edge_opacity']:.1f}")
        opacity_value_label.grid(row=3, column=2, padx=5)
        
        # Layer spacing
        ttk.Label(visual_frame, text="Layer Spacing:", width=15).grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.layer_spacing_var = tk.DoubleVar(value=visual_params["layer_spacing"])
        spacing_scale = ttk.Scale(visual_frame, from_=50, to=300, orient=tk.HORIZONTAL, 
                                 variable=self.layer_spacing_var, length=150)
        spacing_scale.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=5)
        spacing_value_label = ttk.Label(visual_frame, text=f"{visual_params['layer_spacing']:.0f}")
        spacing_value_label.grid(row=4, column=2, padx=5)
        
        # Node spacing
        ttk.Label(visual_frame, text="Node Spacing:", width=15).grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.node_spacing_var = tk.DoubleVar(value=visual_params["node_spacing"])
        node_spacing_scale = ttk.Scale(visual_frame, from_=20, to=120, orient=tk.HORIZONTAL, 
                                      variable=self.node_spacing_var, length=150)
        node_spacing_scale.grid(row=5, column=1, sticky=tk.EW, pady=5, padx=5)
        node_spacing_value_label = ttk.Label(visual_frame, text=f"{visual_params['node_spacing']:.0f}")
        node_spacing_value_label.grid(row=5, column=2, padx=5)
        
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
            self.node_diameter_var, self.node_color_var, self.edge_width_var,
            self.edge_opacity_var, self.layer_spacing_var, self.node_spacing_var,
            self.show_labels_var, self.input_label_var, self.hidden_label_var,
            self.output_label_var, self.width_var, self.height_var, self.dpi_var
        ]
        
        for var in variables:
            if hasattr(var, 'trace'):
                var.trace('w', self.on_parameter_change)
    
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
    
    def choose_color(self):
        """Open color chooser dialog."""
        color = colorchooser.askcolor(color=self.node_color_var.get())
        if color[1]:  # If user didn't cancel
            self.node_color_var.set(color[1])
            self.color_display.config(bg=color[1])
            if self.auto_update.get():
                self.update_preview()
    
    def update_config_from_gui(self):
        """Update current config from GUI values."""
        try:
            # Parse hidden layers
            hidden_layers_str = self.hidden_layers_var.get().strip()
            if hidden_layers_str:
                hidden_layers = [int(x.strip()) for x in hidden_layers_str.split(',')]
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
                    "node_color": self.node_color_var.get(),
                    "edge_width": self.edge_width_var.get(),
                    "edge_opacity": self.edge_opacity_var.get(),
                    "layer_spacing": self.layer_spacing_var.get(),
                    "node_spacing": self.node_spacing_var.get()
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
        except Exception as e:
            messagebox.showerror("Error", f"Invalid parameters: {str(e)}")
            return False
    
    def update_preview(self):
        """Update the preview image."""
        if not self.update_config_from_gui():
            return
        
        try:
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
            messagebox.showerror("Preview Error", f"Failed to update preview: {str(e)}")
    
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
        self.node_color_var.set(visual["node_color"])
        self.color_display.config(bg=visual["node_color"])
        self.edge_width_var.set(visual["edge_width"])
        self.edge_opacity_var.set(visual["edge_opacity"])
        self.layer_spacing_var.set(visual["layer_spacing"])
        self.node_spacing_var.set(visual["node_spacing"])
        
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