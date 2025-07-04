#!/usr/bin/env python3
"""
Main GUI for the Paper-Ready Architecture Generator.
Supports both MLP and CNN visualization modes.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import yaml
from config_manager import ConfigManager
from mlp_generator import MLPGenerator
from cnn_generator import CNNGenerator
from cnn_dialog import CNNDialog

class ArchitectureGeneratorGUI:
    """Main GUI class for the architecture generator."""
    
    def __init__(self):
        """Initialize the GUI."""
        self.root = tk.Tk()
        self.root.title("Paper-Ready Architecture Generator")
        self.root.geometry("1200x800")
        
        # Initialize components
        self.config_manager = ConfigManager()
        self.mlp_generator = MLPGenerator()
        self.cnn_generator = CNNGenerator()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create mode selection
        self._create_mode_selection()
        
        # Create configuration section
        self._create_config_section()
        
        # Create preview section
        self._create_preview_section()
        
        # Create export section
        self._create_export_section()
        
        # Initialize current mode
        self.current_mode = "mlp"
        self._update_ui_for_mode()
    
    def _create_mode_selection(self):
        """Create the mode selection section."""
        mode_frame = ttk.LabelFrame(self.main_frame, text="Network Type", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.mode_var = tk.StringVar(value="mlp")
        ttk.Radiobutton(
            mode_frame,
            text="Multi-Layer Perceptron (MLP)",
            variable=self.mode_var,
            value="mlp",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            mode_frame,
            text="Convolutional Neural Network (CNN)",
            variable=self.mode_var,
            value="cnn",
            command=self._on_mode_change
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_config_section(self):
        """Create the configuration section."""
        config_frame = ttk.LabelFrame(self.main_frame, text="Configuration", padding="10")
        config_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create buttons frame
        button_frame = ttk.Frame(config_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            button_frame,
            text="New Configuration",
            command=self._new_config
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Load Configuration",
            command=self._load_config
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Save Configuration",
            command=self._save_config
        ).pack(side=tk.LEFT, padx=5)
        
        # Create configuration editor
        self.config_editor = tk.Text(config_frame, wrap=tk.WORD, width=40, height=20)
        self.config_editor.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.config_editor, command=self.config_editor.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.config_editor.config(yscrollcommand=scrollbar.set)
    
    def _create_preview_section(self):
        """Create the preview section."""
        preview_frame = ttk.LabelFrame(self.main_frame, text="Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, bg="white")
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create preview buttons
        button_frame = ttk.Frame(preview_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Generate Preview",
            command=self._generate_preview
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_export_section(self):
        """Create the export section."""
        export_frame = ttk.LabelFrame(self.main_frame, text="Export", padding="10")
        export_frame.pack(fill=tk.X)
        
        # Create export options
        options_frame = ttk.Frame(export_frame)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(options_frame, text="Format:").pack(side=tk.LEFT, padx=5)
        self.format_var = tk.StringVar(value="png")
        ttk.Combobox(
            options_frame,
            textvariable=self.format_var,
            values=["png", "pdf", "svg"],
            width=10,
            state="readonly"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(options_frame, text="DPI:").pack(side=tk.LEFT, padx=5)
        self.dpi_var = tk.StringVar(value="300")
        ttk.Entry(options_frame, textvariable=self.dpi_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Create export button
        ttk.Button(
            export_frame,
            text="Export Diagram",
            command=self._export_diagram
        ).pack(side=tk.RIGHT, padx=5)
    
    def _on_mode_change(self):
        """Handle mode change."""
        new_mode = self.mode_var.get()
        if new_mode != self.current_mode:
            self.current_mode = new_mode
            self._update_ui_for_mode()
    
    def _update_ui_for_mode(self):
        """Update UI elements based on current mode."""
        if self.current_mode == "mlp":
            # Load default MLP config
            config = self.config_manager.load_config("mlp_config.yaml")
        else:
            # Load default CNN config
            config = self.config_manager.load_config("lenet_config.yaml")
        
        # Update config editor
        self.config_editor.delete(1.0, tk.END)
        self.config_editor.insert(1.0, yaml.dump(config, default_flow_style=False))
    
    def _new_config(self):
        """Create a new configuration."""
        if self.current_mode == "mlp":
            # Show MLP configuration dialog
            # TODO: Implement MLP dialog
            pass
        else:
            # Show CNN configuration dialog
            dialog = CNNDialog(self.root, self.config_manager)
            config = dialog.show()
            if config:
                self.config_editor.delete(1.0, tk.END)
                self.config_editor.insert(1.0, yaml.dump(config, default_flow_style=False))
    
    def _load_config(self):
        """Load a configuration from file."""
        file_path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")],
            initialdir="configs"
        )
        
        if file_path:
            try:
                config = self.config_manager.load_config(file_path)
                self.config_editor.delete(1.0, tk.END)
                self.config_editor.insert(1.0, yaml.dump(config, default_flow_style=False))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def _save_config(self):
        """Save the current configuration."""
        try:
            config = yaml.safe_load(self.config_editor.get(1.0, tk.END))
            file_path = filedialog.asksaveasfilename(
                title="Save Configuration",
                defaultextension=".yaml",
                filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")],
                initialdir="configs"
            )
            
            if file_path:
                self.config_manager.save_config(config, file_path)
                messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def _generate_preview(self):
        """Generate a preview of the architecture."""
        try:
            config = yaml.safe_load(self.config_editor.get(1.0, tk.END))
            
            if self.current_mode == "mlp":
                fig = self.mlp_generator.create_diagram(config)
            else:
                fig = self.cnn_generator.create_diagram(config)
            
            # Save preview to temporary file
            temp_path = "temp_preview.png"
            if self.current_mode == "mlp":
                self.mlp_generator.save_figure(temp_path, "png", 100)
            else:
                self.cnn_generator.save_figure(temp_path, "png", 100)
            
            # Load and display preview
            from PIL import Image, ImageTk
            image = Image.open(temp_path)
            photo = ImageTk.PhotoImage(image)
            
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(
                self.preview_canvas.winfo_width() // 2,
                self.preview_canvas.winfo_height() // 2,
                image=photo,
                anchor=tk.CENTER
            )
            self.preview_canvas.image = photo  # Keep reference
            
            # Clean up
            os.remove(temp_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview: {str(e)}")
    
    def _export_diagram(self):
        """Export the architecture diagram."""
        try:
            config = yaml.safe_load(self.config_editor.get(1.0, tk.END))
            format = self.format_var.get()
            dpi = int(self.dpi_var.get())
            
            file_path = filedialog.asksaveasfilename(
                title="Export Diagram",
                defaultextension=f".{format}",
                filetypes=[(f"{format.upper()} files", f"*.{format}"), ("All files", "*.*")],
                initialdir="exports"
            )
            
            if file_path:
                if self.current_mode == "mlp":
                    fig = self.mlp_generator.create_diagram(config)
                    self.mlp_generator.save_figure(file_path, format, dpi)
                else:
                    fig = self.cnn_generator.create_diagram(config)
                    self.cnn_generator.save_figure(file_path, format, dpi)
                
                messagebox.showinfo("Success", "Diagram exported successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export diagram: {str(e)}")
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = ArchitectureGeneratorGUI()
    app.run() 