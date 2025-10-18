# Quick Start Guide

## Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/Emukelvin/AI-Drilling-Optimization-System.git
cd AI-Drilling-Optimization-System

# Install dependencies
pip install -r requirements.txt
```

## Quick Demo (1 minute)

```bash
# Run the demo to see all features
python demo.py
```

## Train Models (2-5 minutes)

```bash
# Quick training (100 samples)
python train.py --samples 100

# Full training (1000 samples, recommended)
python train.py --samples 1000
```

## Launch Dashboard

```bash
# Start interactive dashboard
streamlit run src/dashboard/app.py
```

Then:
1. Click "Train Models" button (first time only)
2. Switch between "Real-time Simulation" and "Historical Analysis" modes
3. Adjust parameters using sidebar controls
4. Monitor risks and recommendations

## Basic Usage Example

```python
from src.models.hybrid_twin import HybridDigitalTwin
from src.data.data_collector import DrillingDataCollector

# Initialize
twin = HybridDigitalTwin()
collector = DrillingDataCollector()

# Train
data = collector.generate_sample_data(500)
X, y, scaler = collector.preprocess_data(data)
twin.train_ml_component(X, y, scaler)

# Predict
params = {
    'depth': 5000, 'wob': 25, 'rpm': 120,
    'flow_rate': 500, 'spp': 2500, 'torque': 15,
    'rop': 60, 'mud_weight': 12, 'temperature': 150
}

risks = twin.predict_risks(params)
print(f"Wellbore instability: {risks['wellbore_instability']:.1%}")
print(f"Stuck pipe risk: {risks['stuck_pipe']:.1%}")
print(f"Kick risk: {risks['kick_risk']:.1%}")
```

## System Features

✅ **Hybrid Digital Twin**: Physics + ML models
✅ **Real-time Risk Prediction**: 3 main drilling hazards
✅ **Autonomous Optimization**: Automated parameter adjustments
✅ **Interactive Dashboard**: Real-time monitoring and visualization
✅ **Sustainability**: CO2 and fuel consumption tracking
✅ **Comprehensive Tests**: 25 unit tests, 100% passing
✅ **Full Documentation**: Setup, user guide, API reference

## Project Structure

```
AI-Drilling-Optimization-System/
├── src/
│   ├── data/          # Data collection and preprocessing
│   ├── models/        # Physics, ML, and hybrid models
│   ├── optimization/  # Autonomous optimizer
│   ├── dashboard/     # Streamlit dashboard
│   └── utils/         # Utilities
├── tests/             # Unit tests (25 tests)
├── docs/              # Documentation
├── config/            # Configuration files
├── train.py           # Model training script
├── demo.py            # Demo script
└── requirements.txt   # Dependencies
```

## Documentation

- 📖 [System Architecture](docs/architecture.md) - Technical details
- 🚀 [Setup Guide](docs/setup.md) - Installation and configuration
- 📘 [User Guide](docs/user_guide.md) - How to use the system
- 📚 [API Reference](docs/api_reference.md) - API documentation

## Key Technologies

- **ML Frameworks**: TensorFlow, PyTorch, Scikit-learn
- **Data Processing**: NumPy, Pandas
- **Visualization**: Streamlit, Plotly, Matplotlib
- **Testing**: Pytest

## Support

For issues or questions:
1. Check documentation
2. Review logs in `logs/` directory
3. Open GitHub issue with details

## Next Steps

1. ✅ Run `python demo.py` to see features
2. ✅ Run `python train.py` to train models
3. ✅ Run `streamlit run src/dashboard/app.py` for dashboard
4. ✅ Read documentation for advanced usage
5. ✅ Customize config in `config/config.yaml`
6. ✅ Integrate with your drilling data

---

**Ready to optimize your drilling operations!** 🛢️
