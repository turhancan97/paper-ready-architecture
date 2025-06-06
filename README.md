# Neural Network Architecture Visualizer

A Python application for creating paper-ready visualizations of Multi-Layer Perceptron (MLP) architectures with customizable parameters and clean, minimalist design.

## Features

- **Real-time Preview**: See changes instantly as you adjust parameters
- **Customizable Parameters**:
  - Node diameter and color
  - Edge width and opacity
  - Layer spacing and node spacing
  - Hidden layer configuration
  - Number of neurons per layer
- **Multiple Export Formats**: PNG, PDF, SVG, JPEG
- **Configuration Management**: Save and load parameter configurations for reproducibility
- **Academic Style**: Clean, minimalist design perfect for research papers
- **Optional Labels**: Toggle layer labels on/off

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd paper-ready-architecture
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### GUI Interface

The application provides an intuitive GUI with:

1. **Control Panel** (left side):
   - **Network Structure**: Configure input, hidden layers, and output neurons
   - **Visual Parameters**: Adjust node size, colors, edge properties, and spacing
   - **Labels**: Toggle and customize layer labels
   - **Export Settings**: Set dimensions and DPI for export

2. **Preview Panel** (right side):
   - Real-time visualization of your neural network
   - Auto-updates as you change parameters

### Key Parameters

- **Input Neurons**: Number of neurons in the input layer (1-20)
- **Hidden Layers**: Comma-separated list of neurons per hidden layer (e.g., "4,4,3")
- **Output Neurons**: Number of neurons in the output layer (1-20)
- **Node Diameter**: Size of neural network nodes (10-80)
- **Node Color**: Color of the nodes (click "Choose" to select)
- **Edge Width**: Thickness of connections between neurons (0.5-5.0)
- **Edge Opacity**: Transparency of connections (0.1-1.0)
- **Layer Spacing**: Horizontal distance between layers (50-300)
- **Node Spacing**: Vertical distance between nodes in same layer (20-120)

### Exporting Images

1. Adjust your parameters as desired
2. Go to **File → Export Image**
3. Choose format (PNG, PDF, SVG, JPEG) and location
4. The configuration will be automatically saved alongside the image

### Configuration Management

- **Auto-save**: Configurations are automatically saved as you work
- **Manual Save**: File → Save Configuration
- **Load**: File → Load Configuration to restore previous settings

## Examples

### Basic MLP
- Input: 3 neurons
- Hidden: 4, 4 neurons
- Output: 2 neurons

### Deep Network
- Input: 5 neurons
- Hidden: 8, 6, 4 neurons
- Output: 3 neurons

## File Structure

```
paper-ready-architecture/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── __init__.py        # Package initialization
│   ├── gui_app.py         # Main GUI application
│   ├── mlp_generator.py   # Neural network diagram generator
│   └── config_manager.py  # Configuration management
└── configs/               # Saved configurations (created automatically)
```

## Dependencies

- matplotlib: For generating diagrams
- numpy: Numerical computations
- Pillow: Image processing
- PyYAML: Configuration file handling
- tkinter: GUI framework (usually included with Python)

## Contributing

This project is designed for academic and research use. Feel free to extend it with additional neural network architectures or visualization features.

## License

MIT License - see LICENSE file for details.

## Academic Use

This tool is specifically designed for creating high-quality figures for academic papers. The generated diagrams follow clean, minimalist design principles suitable for scientific publications.

### Recommended Settings for Papers:
- **DPI**: 300 or higher
- **Format**: SVG (for vector graphics) or PNG (for raster)
- **Colors**: Use contrasting colors that work well in grayscale
- **Node Size**: Adjust based on your paper's figure size requirements