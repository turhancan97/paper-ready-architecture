# Tests

This directory contains the test suite for the Neural Network Architecture Visualizer.

## Test Structure

- `test_config_manager.py` - Tests for configuration management functionality
- `test_mlp_generator.py` - Tests for neural network diagram generation
- `test_integration.py` - Integration tests for complete workflows
- `test_gui.py` - Basic component tests (original simple test)
- `run_tests.py` - Test runner script

## Running Tests

### Run All Tests
```bash
cd tests
python run_tests.py
```

### Run Specific Test Module
```bash
cd tests
python run_tests.py config_manager    # or test_config_manager
python run_tests.py mlp_generator     # or test_mlp_generator
python run_tests.py integration       # or test_integration
```

### Run Individual Test Files
```bash
cd tests
python test_config_manager.py
python test_mlp_generator.py
python test_integration.py
```

### Run with Python unittest
```bash
# From project root
python -m unittest discover tests -v

# From tests directory
python -m unittest test_config_manager -v
```

## Test Coverage

The test suite covers:

- **Configuration Management**: Default configs, saving/loading, color validation
- **Diagram Generation**: Various network structures, visual parameters, export formats
- **Integration Workflows**: Complete end-to-end scenarios
- **Error Handling**: Invalid inputs, recovery mechanisms
- **Custom Colors**: User-specified hex colors like `#84A1FB`, `#FB84DC`
- **Export Functionality**: PNG, PDF, SVG, JPEG formats

## Test Requirements

Tests use only standard library modules:
- `unittest` - Test framework
- `tempfile` - Temporary directories for test isolation
- `shutil` - File operations

No additional dependencies beyond the main project requirements. 