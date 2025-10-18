# Quick Start Guide

Get up and running with the AI-Driven Autonomous Drilling Optimization System in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Modern web browser

## Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/Emukelvin/AI-Drilling-Optimization-System.git
cd AI-Drilling-Optimization-System

# Install dependencies
pip install -r requirements.txt
```

## First Run (1 minute)

### Generate Training Data

```bash
python main.py generate-data --samples 200
```

This creates synthetic drilling data in `data/synthetic/` directory.

### Run a Quick Simulation

```bash
python main.py simulate
```

You should see output like:

```
🛢️  AI-Driven Autonomous Drilling Optimization System
============================================================

Initializing hybrid digital twin...
✅ Physics models loaded
✅ ML models loaded

Current Drilling Parameters:
  WOB: 80.0 kN
  RPM: 120.0 RPM
  Flow Rate: 1000.0 LPM
  Mud Weight: 1200.0 kg/m³

📊 Performance Metrics:
  ROP: 67.91 m/hr
  Torque: 3.73 kN-m
  ECD: 1205 kg/m³
  Efficiency: 5.35%

⚠️  Overall Risk Score: 36.23%
...
```

## Launch Dashboard (2 minutes)

```bash
python main.py dashboard
```

The dashboard will automatically open in your browser at http://localhost:8501

### Dashboard Features

**Real-Time Monitoring Tab**:
- View live drilling parameters
- Monitor risk scores
- See efficiency and sustainability metrics

**Optimization Tab**:
- Set target ROP
- Get optimized parameter recommendations
- Apply optimizations with one click

**Risk Prediction Tab**:
- Detailed risk analysis
- Compare physics vs ML predictions
- Wellbore stability assessment

**Analytics Tab**:
- Historical performance trends
- Statistical summaries
- Data visualization

**Settings Tab**:
- Configure safety thresholds
- Adjust model parameters
- Generate training data

## Quick Test Scenarios

### Scenario 1: Optimize for Higher ROP

1. Go to **Optimization** tab
2. Set Target ROP to 30 m/hr
3. Click "Optimize Parameters"
4. Review recommendations
5. Click "Apply Optimized Parameters"
6. Go to **Real-Time Monitoring** to see results

### Scenario 2: Risk Analysis

1. Go to **Risk Prediction** tab
2. Adjust parameters in sidebar to increase WOB to 140 kN
3. Observe risk scores increase
4. See alerts appear
5. Reduce WOB back to safe levels

### Scenario 3: Performance Analytics

1. Make several parameter adjustments
2. Go to **Analytics** tab
3. View performance trends
4. Check summary statistics

## Using the Python API

```python
from src.hybrid_twin import DigitalTwin

# Initialize
twin = DigitalTwin()

# Set parameters
drilling = {
    'wob': 80, 'rpm': 120, 'flow_rate': 1000,
    'mud_weight': 1200, 'bit_diameter': 12.25,
    'pipe_od': 5.0, 'tvd': 2000, 'bit_wear': 0.1
}

formation = {
    'formation_strength': 30, 'formation_abrasiveness': 0.5,
    'pore_pressure': 300, 'fracture_gradient': 1800
}

# Update and get results
state = twin.update_state(drilling, formation)
print(f"ROP: {state['rop']:.1f} m/hr")
print(f"Risk: {twin.get_overall_risk_score():.2%}")
```

## Common Issues

**Import errors**: Run `pip install -r requirements.txt`

**Dashboard won't start**: Check if port 8501 is available

**No data**: Run `python main.py generate-data` first

## Next Steps

- Read the [User Manual](docs/USER_MANUAL.md)
- Check [API Reference](docs/API_REFERENCE.md)
- Review [Architecture](docs/ARCHITECTURE.md)
- Try different scenarios and parameter combinations
- Import your own drilling data

## Support

- Open an issue on GitHub
- Check documentation in `docs/` directory
- Review example code in `main.py`

## Key Features to Explore

✅ **Real-time monitoring** of drilling parameters  
✅ **Risk prediction** with hybrid physics+ML approach  
✅ **Autonomous optimization** for target ROP  
✅ **Sustainability tracking** for environmental impact  
✅ **Interactive dashboard** with 5 specialized tabs  
✅ **Synthetic data generation** for testing  
✅ **Configurable safety thresholds**  
✅ **Alert system** for critical events  

Happy drilling! 🛢️
