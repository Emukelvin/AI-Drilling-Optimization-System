# AI Drilling Optimization System 🛢️

AI-Driven Autonomous Drilling Optimization System using hybrid digital twin models for real-time drilling optimization, risk prediction, and sustainability integration.

## 🌟 Features

- **Hybrid Digital Twin**: Combines physics-based well models with machine learning models trained on drilling datasets
- **Real-Time Risk Prediction**: ML models predict risks such as wellbore instability, stuck pipe, and kicks
- **Autonomous Optimization**: Real-time parameter adjustments to optimize drilling efficiency
- **Interactive Dashboard**: Streamlit-based dashboard for real-time monitoring and visualization
- **Sustainability Integration**: Optimization for reduced carbon footprint and fuel consumption

## 🏗️ System Architecture

```
AI-Drilling-Optimization-System/
├── src/
│   ├── data/              # Data collection and preprocessing
│   ├── models/            # Physics models, ML models, and hybrid digital twin
│   ├── optimization/      # Autonomous optimization engine
│   ├── dashboard/         # Interactive Streamlit dashboard
│   └── utils/             # Utility functions and helpers
├── tests/                 # Unit tests
├── config/                # Configuration files
├── docs/                  # Documentation
└── data/                  # Training and sample data
```

## 📋 Requirements

- Python 3.8+
- TensorFlow 2.13+
- PyTorch 2.0+
- Scikit-learn 1.3+
- Streamlit 1.28+
- NumPy, Pandas, and other dependencies (see requirements.txt)

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Emukelvin/AI-Drilling-Optimization-System.git
cd AI-Drilling-Optimization-System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Training the Models

Train the ML models on synthetic drilling data:

```bash
python train.py --samples 1000 --output-dir models
```

Options:
- `--samples`: Number of training samples to generate (default: 1000)
- `--output-dir`: Directory to save trained models (default: models)
- `--config`: Path to custom configuration file

### Running the Dashboard

Launch the interactive dashboard:

```bash
streamlit run src/dashboard/app.py
```

The dashboard will open in your web browser at `http://localhost:8501`.

## 📊 Dashboard Features

### Real-time Simulation Mode
- Live drilling parameter monitoring
- Risk assessment with visual indicators
- Automated optimization recommendations
- Sustainability metrics tracking
- Interactive charts and visualizations

### Historical Analysis Mode
- Generate and analyze historical drilling data
- Statistical analysis and trends
- Performance comparisons

## 🧪 Running Tests

Run the unit tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## 📖 Usage Examples

### Using the Hybrid Digital Twin

```python
from src.models.hybrid_twin import HybridDigitalTwin
from src.data.data_collector import DrillingDataCollector

# Initialize components
twin = HybridDigitalTwin()
collector = DrillingDataCollector()

# Train models
training_data = collector.generate_sample_data(1000)
X_train, y_targets, scaler = collector.preprocess_data(training_data)
twin.train_ml_component(X_train, y_targets, scaler)

# Predict risks
drilling_params = {
    'depth': 5000,
    'wob': 25,
    'rpm': 120,
    'flow_rate': 500,
    'spp': 2500,
    'torque': 15,
    'rop': 60,
    'mud_weight': 12,
    'temperature': 150
}

risks = twin.predict_risks(drilling_params, use_ml=True)
print(f"Risks: {risks}")

# Get recommendations
recommendations = twin.get_recommendations(risks, drilling_params)
for rec in recommendations:
    print(f"{rec['risk_type']}: {rec['action']}")
```

### Using the Autonomous Optimizer

```python
from src.optimization.optimizer import AutonomousOptimizer

optimizer = AutonomousOptimizer()

# Optimize parameters
optimized, adjustments = optimizer.optimize_parameters(
    current_params=drilling_params,
    risks=risks,
    recommendations=recommendations
)

print(f"Optimized WOB: {optimized['wob']:.2f} klbs")
print(f"Optimized RPM: {optimized['rpm']:.0f}")

# Optimize for sustainability
optimized_sustain, metrics = optimizer.optimize_for_sustainability(drilling_params)
print(f"Fuel reduction: {metrics['fuel_reduction_percent']:.1f}%")
print(f"CO2 reduction: {metrics['co2_reduction_percent']:.1f}%")
```

## 🔧 Configuration

Edit `config/config.yaml` to customize:

- Model hyperparameters (learning rate, epochs, batch size)
- Risk thresholds for different hazards
- Optimization constraints (max parameter adjustments)
- Physics model parameters
- Sustainability targets
- Dashboard settings

## 🌱 Sustainability Features

The system includes several sustainability-focused features:

- **Fuel Consumption Monitoring**: Real-time tracking of rig fuel usage
- **CO2 Emissions Calculation**: Automatic calculation of carbon emissions
- **Optimization for Efficiency**: Parameter adjustments to reduce environmental impact
- **Sustainability Metrics Dashboard**: Visual tracking of environmental KPIs

## 📚 Documentation

For detailed documentation, see:

- [System Architecture](docs/architecture.md)
- [Setup Guide](docs/setup.md)
- [User Guide](docs/user_guide.md)
- [API Reference](docs/api_reference.md)

## 🧪 Model Components

### Physics-Based Well Model
Implements fundamental drilling physics equations:
- Formation and fracture pressure calculations
- Hydrostatic pressure modeling
- Rate of penetration (ROP) prediction
- Torque and hydraulic calculations
- Wellbore stability analysis

### Machine Learning Models
- Neural network models (TensorFlow/Keras)
- Random Forest ensemble models
- Multi-target risk prediction (wellbore instability, stuck pipe, kicks)
- Feature scaling and preprocessing

### Hybrid Digital Twin
- Combines physics and ML predictions
- Weighted ensemble approach
- Real-time risk assessment
- Automated recommendation generation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built with TensorFlow, PyTorch, Scikit-learn
- Dashboard powered by Streamlit
- Visualization with Plotly

---

**Note**: This system uses synthetic data for training and demonstration purposes. For production use, replace with real drilling data from your operations.
