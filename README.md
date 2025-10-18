# 🛢️ AI-Driven Autonomous Drilling Optimization System

A comprehensive Python desktop software prototype that leverages real-time hybrid digital twin models integrating physics-based well models and AI/ML algorithms for autonomous drilling optimization.

## 🎯 Overview

This system autonomously optimizes drilling parameters (WOB, RPM, mud weight, ECD, bit selection, etc.) to minimize risks like stuck pipe, kicks, and wellbore instability while maximizing ROP and minimizing NPT (Non-Productive Time).

## ✨ Key Features

### 1. **Hybrid Digital Twin**
- Combines first-principles drilling hydraulics/mechanics equations
- Integrates machine learning models trained on drilling datasets
- Real-time fusion of physics-based and ML predictions

### 2. **Real-Time Risk Prediction**
- Predicts wellbore instability events
- Detects stuck pipe conditions
- Identifies lost circulation risks
- Monitors kick indicators

### 3. **Autonomous Optimization**
- Real-time recommendations for drilling parameters
- Autonomous adjustments to maximize ROP
- Minimizes Non-Productive Time (NPT)
- Safety-constrained optimization

### 4. **Visualization & Decision Support**
- Interactive Streamlit dashboard
- Real-time risk monitoring
- Performance analytics
- Efficiency scoring

### 5. **Sustainability Integration**
- Energy efficiency optimization
- Carbon footprint reduction
- Sustainable drilling fluid usage tracking
- Hydraulic horsepower optimization

## 🏗️ Architecture

```
AI-Drilling-Optimization-System/
├── src/
│   ├── physics_models/        # First-principles drilling models
│   │   ├── drilling_mechanics.py    # ROP, torque, WOB calculations
│   │   └── drilling_hydraulics.py   # ECD, pressure, flow calculations
│   ├── ml_models/             # Machine learning models
│   │   ├── risk_predictor.py        # Multi-risk ML predictor
│   │   ├── wellbore_stability.py    # Stability prediction
│   │   └── rop_optimizer.py         # ROP optimization
│   ├── hybrid_twin/           # Digital twin integration
│   │   └── digital_twin.py          # Hybrid model integration
│   ├── dashboard/             # User interface
│   │   └── app.py                   # Streamlit dashboard
│   └── utils/                 # Utilities
│       ├── data_generator.py        # Synthetic data generation
│       └── config.py                # Configuration management
├── data/                      # Data storage
│   ├── synthetic/             # Generated training data
│   └── real/                  # Real well data (user-provided)
├── config/                    # Configuration files
├── docs/                      # Documentation
├── tests/                     # Test suite
├── main.py                    # Main application entry point
└── requirements.txt           # Python dependencies
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Emukelvin/AI-Drilling-Optimization-System.git
cd AI-Drilling-Optimization-System
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate synthetic training data**
```bash
python main.py generate-data --samples 1000
```

## 📊 Usage

### Option 1: Interactive Dashboard (Recommended)

Launch the Streamlit dashboard for full interactive experience:

```bash
python main.py dashboard
```

The dashboard provides:
- Real-time monitoring of drilling parameters
- Risk prediction and alerts
- Parameter optimization
- Performance analytics
- System configuration

### Option 2: Console Simulation

Run a console-based simulation:

```bash
python main.py simulate
```

### Option 3: Python API

Use the system programmatically:

```python
from src.hybrid_twin import DigitalTwin

# Initialize digital twin
twin = DigitalTwin()

# Set drilling parameters
drilling_params = {
    'wob': 80.0,           # Weight on Bit (kN)
    'rpm': 120.0,          # Rotary Speed (RPM)
    'flow_rate': 1000.0,   # Flow Rate (LPM)
    'mud_weight': 1200.0,  # Mud Weight (kg/m³)
    'bit_diameter': 12.25, # Bit Diameter (inches)
    'pipe_od': 5.0,        # Pipe OD (inches)
    'tvd': 2000.0,         # True Vertical Depth (m)
    'bit_wear': 0.1        # Bit Wear (0-1)
}

formation_params = {
    'formation_strength': 30.0,      # MPa
    'formation_abrasiveness': 0.5,   # 0-1
    'pore_pressure': 300.0,          # bar
    'fracture_gradient': 1800.0      # kg/m³
}

# Update state
state = twin.update_state(drilling_params, formation_params)

# Get risk scores
risk_score = twin.get_overall_risk_score()
efficiency = twin.get_efficiency_score()
sustainability = twin.get_sustainability_score()

# Get optimization recommendations
recommendations = twin.get_recommendations(target_rop=25.0)
```

## 🔬 Technical Details

### Physics-Based Models

#### Drilling Mechanics
- **ROP Calculation**: Bourgoyne and Young model
- **Torque**: Friction-based torque modeling
- **Vibration**: Axial vibration prediction
- **Bit Wear**: Time-based wear modeling
- **MSE**: Mechanical Specific Energy calculation

#### Drilling Hydraulics
- **ECD**: Equivalent Circulating Density
- **Pressure Loss**: Darcy-Weisbach friction calculations
- **Flow Regime**: Reynolds number-based classification
- **Pump Pressure**: System pressure requirements
- **Hydraulic Horsepower**: Energy efficiency metrics

### Machine Learning Models

#### Risk Predictor
- **Algorithm**: Random Forest & Gradient Boosting ensemble
- **Predictions**: Stuck pipe, kicks, lost circulation, instability
- **Features**: WOB, RPM, flow rate, mud weight, ECD, torque, ROP, TVD
- **Training**: Synthetic and real drilling data

#### Wellbore Stability Model
- **Algorithm**: Random Forest Regressor
- **Predictions**: Stability index, collapse risk, fracture risk
- **Approach**: Physics-informed ML

#### ROP Optimizer
- **Algorithm**: Gradient Boosting Regressor
- **Function**: Parameter optimization for target ROP
- **Constraints**: Safety limits and operational bounds

### Hybrid Digital Twin

The hybrid approach combines:
- **Physics models** (60% weight): Reliable, explainable predictions
- **ML models** (40% weight): Adaptive learning from data
- **Weighted fusion**: Configurable weighting for different scenarios

## 📈 Case Studies

The system includes three validation scenarios:

1. **Normal Drilling**: Standard conditions, moderate formation
2. **High Risk**: Challenging formations, high pressure/strength
3. **Optimal**: Ideal conditions for maximum ROP

Generate case study data:
```bash
python main.py generate-data --samples 200
```

Case study data is saved in `data/synthetic/` directory.

## 🎛️ Configuration

Edit default parameters in `src/utils/config.py` or create a custom YAML config:

```yaml
drilling:
  default_wob: 80
  default_rpm: 120
  default_flow_rate: 1000
  default_mud_weight: 1200

safety:
  max_risk_threshold: 0.7
  min_efficiency_threshold: 0.3
  
optimization:
  target_rop: 20
  max_acceptable_risk: 0.3
```

## 🔒 Safety Features

- **Real-time risk monitoring**: Continuous evaluation of drilling risks
- **Automated alerts**: Critical, high, medium, and low severity alerts
- **Safety constraints**: Optimization respects operational limits
- **Multi-level validation**: Physics and ML cross-validation

## 🌱 Sustainability Metrics

The system tracks:
- **Energy efficiency**: ROP per hydraulic horsepower
- **Mud circulation efficiency**: ECD optimization
- **Carbon footprint**: Power consumption monitoring
- **Resource optimization**: Reduced NPT and material waste

## 🧪 Testing

Run tests (when implemented):
```bash
pytest tests/
```

## 📚 Documentation

Detailed documentation available in `docs/` directory:
- API Reference
- Physics Models Guide
- ML Models Guide
- User Manual
- Integration Guide

## 🔄 Future Enhancements

- [ ] Real-time data integration from rig control systems
- [ ] Advanced ML models (LSTM, Transformers for time series)
- [ ] Multi-well learning and transfer learning
- [ ] Cloud deployment and API service
- [ ] Mobile app for remote monitoring
- [ ] Integration with major drilling software platforms

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Developed as part of AI-Driven Drilling Optimization Research

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: [Your Contact Information]

## 🙏 Acknowledgments

- Physics models based on established drilling engineering principles
- ML approaches inspired by recent research in drilling optimization
- Built with Python, TensorFlow, Scikit-learn, Streamlit, and other open-source tools

---

**Note**: This is a prototype system for research and development purposes. Real-world deployment requires validation with actual drilling data and integration with safety systems.
