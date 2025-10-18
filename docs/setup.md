# Setup Guide

## Prerequisites

### System Requirements
- Operating System: Linux, macOS, or Windows 10+
- Python: 3.8 or higher
- RAM: 8GB minimum, 16GB recommended
- Storage: 5GB free space
- Internet connection (for initial setup)

### Python Version Check
```bash
python --version
# Should show Python 3.8 or higher
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Emukelvin/AI-Drilling-Optimization-System.git
cd AI-Drilling-Optimization-System
```

### 2. Create Virtual Environment (Recommended)

**On Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- TensorFlow 2.13+
- PyTorch 2.0+
- Scikit-learn 1.3+
- Streamlit 1.28+
- NumPy, Pandas, and other dependencies

### 4. Verify Installation

```bash
python -c "import tensorflow as tf; import torch; import sklearn; import streamlit; print('All packages installed successfully!')"
```

## Initial Configuration

### 1. Review Configuration File

Edit `config/config.yaml` to customize settings:

```bash
# On Linux/macOS
nano config/config.yaml

# On Windows
notepad config/config.yaml
```

Key settings to review:
- Model hyperparameters
- Risk thresholds
- Optimization constraints
- Dashboard refresh rate

### 2. Create Required Directories

The system will create these automatically, but you can create them manually:

```bash
mkdir -p logs models data/sample
```

## Training the Models

### Quick Training

Train with default settings (1000 samples):

```bash
python train.py
```

### Custom Training

Train with more samples for better accuracy:

```bash
python train.py --samples 5000 --output-dir models
```

Training options:
- `--samples`: Number of training samples (default: 1000)
- `--output-dir`: Output directory for models (default: models)
- `--config`: Custom config file path

**Expected output:**
```
AI Drilling Optimization System - Model Training
============================================================
Generating 1000 training samples...
Training data shape: (1000, 15)
Preprocessing data...
Training hybrid digital twin models...
Saving models to models...
Training completed successfully!
```

Training typically takes 2-5 minutes depending on:
- Number of samples
- Hardware (CPU/GPU)
- Number of epochs (configured in config.yaml)

## Running the Dashboard

### Start the Dashboard

```bash
streamlit run src/dashboard/app.py
```

The dashboard will automatically open in your default browser at:
```
http://localhost:8501
```

### Dashboard First Use

1. Click "Train Models" button (if not already trained)
2. Wait for training to complete (~1-2 minutes)
3. Switch between "Real-time Simulation" and "Historical Analysis" modes
4. Adjust parameters using sidebar controls

### Accessing from Other Devices

To access the dashboard from other devices on your network:

```bash
streamlit run src/dashboard/app.py --server.address 0.0.0.0
```

Then access from other devices using:
```
http://<your-ip-address>:8501
```

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_data_collector.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

View coverage report:
```bash
# On Linux/macOS
open htmlcov/index.html

# On Windows
start htmlcov/index.html
```

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Error:** `ModuleNotFoundError: No module named 'tensorflow'`

**Solution:**
```bash
pip install tensorflow>=2.13.0
```

#### 2. TensorFlow GPU Issues

**Error:** TensorFlow not using GPU

**Solution:**
```bash
# Check GPU availability
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Install GPU-enabled TensorFlow (if you have NVIDIA GPU)
pip install tensorflow-gpu>=2.13.0
```

#### 3. Port Already in Use

**Error:** `OSError: [Errno 98] Address already in use`

**Solution:**
```bash
# Use a different port
streamlit run src/dashboard/app.py --server.port 8502
```

#### 4. Memory Issues

**Error:** `MemoryError` during training

**Solution:**
- Reduce number of training samples
- Reduce batch size in config.yaml
- Close other applications

```bash
# Train with fewer samples
python train.py --samples 500
```

#### 5. YAML Configuration Error

**Error:** `yaml.scanner.ScannerError`

**Solution:**
- Check config.yaml for proper indentation
- Ensure no tabs (use spaces only)
- Validate YAML syntax online

### Getting Help

If you encounter issues:

1. Check the logs in `logs/` directory
2. Review error messages carefully
3. Search existing GitHub issues
4. Create a new issue with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce

## Development Setup

### For Contributors

1. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest-cov black flake8 mypy
```

2. Setup pre-commit hooks:
```bash
# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Type checking
mypy src/
```

3. Run tests before committing:
```bash
pytest tests/ -v
```

## Next Steps

After successful setup:

1. Read the [User Guide](user_guide.md) for usage instructions
2. Review [API Reference](api_reference.md) for programmatic usage
3. Check [System Architecture](architecture.md) for technical details

## Uninstallation

To remove the system:

```bash
# Deactivate virtual environment
deactivate

# Remove directory
cd ..
rm -rf AI-Drilling-Optimization-System
```
