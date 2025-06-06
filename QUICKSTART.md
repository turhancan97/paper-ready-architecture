# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Create Your First Neural Network Diagram!

## 🎛️ Basic Usage

### GUI Application
- **Left Panel**: Adjust all parameters (network structure, layer colors, visual style, labels)
- **Right Panel**: Real-time preview of your neural network
- **Auto-update**: Enable/disable real-time updates as you change parameters

### Key Parameters to Try
1. **Network Structure**: 
   - Input neurons: `3`
   - Hidden layers: `4, 4` (comma-separated)
   - Output neurons: `2`

2. **Visual Tweaks**:
   - Node diameter: `30-50` (good for papers)
   - Layer colors: Click "Configure Layer Colors..." button
     - Try presets: Default, Academic, or Gradient
     - Individual color picking for each layer
   - Edge opacity: `0.6-0.8` (for clean look)
   - Layer spacing: `120-150`

3. **Export**:
   - Use **SVG** for vector graphics (perfect for papers)
   - Use **PNG** with 300+ DPI for high-quality raster

## 💡 Pro Tips

- **For Academic Papers**: Use SVG format, grayscale colors, DPI 300+
- **Configuration Save**: Every change auto-saves, you can also manually save configs
- **Batch Generation**: Check `examples/basic_usage.py` for programmatic usage

## 🔧 Troubleshooting

If you get import errors, run the test script first:
```bash
python test_gui.py
```

## 📖 Full Documentation
See `README.md` for complete documentation and advanced features. 