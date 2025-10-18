# API Reference

## Overview

This document provides detailed API reference for the AI Drilling Optimization System modules.

## Table of Contents

- [Data Collection](#data-collection)
- [Physics Model](#physics-model)
- [ML Models](#ml-models)
- [Hybrid Digital Twin](#hybrid-digital-twin)
- [Autonomous Optimizer](#autonomous-optimizer)
- [Utilities](#utilities)

---

## Data Collection

### DrillingDataCollector

Class for collecting and managing drilling operation data.

#### Constructor

```python
from src.data.data_collector import DrillingDataCollector

collector = DrillingDataCollector()
```

#### Methods

##### generate_sample_data(num_samples)

Generate synthetic drilling data for training and testing.

**Parameters:**
- `num_samples` (int): Number of data samples to generate

**Returns:**
- `pd.DataFrame`: Sample drilling data with columns:
  - timestamp, depth, wob, rpm, flow_rate, spp, torque, rop
  - mud_weight, temperature, wellbore_instability, stuck_pipe
  - kick_risk, fuel_consumption, co2_emissions

**Example:**
```python
data = collector.generate_sample_data(1000)
print(data.head())
```

##### collect_realtime_data()

Simulate real-time data collection from drilling sensors.

**Returns:**
- `dict`: Current drilling parameters

**Example:**
```python
current_data = collector.collect_realtime_data()
print(f"Current depth: {current_data['depth']}")
```

##### preprocess_data(data)

Preprocess drilling data for model training.

**Parameters:**
- `data` (pd.DataFrame): Raw drilling data

**Returns:**
- `tuple`: (X_scaled, y_targets, scaler)
  - X_scaled: Normalized features
  - y_targets: Tuple of (wellbore, stuck_pipe, kick) targets
  - scaler: Fitted StandardScaler

**Example:**
```python
X_train, y_targets, scaler = collector.preprocess_data(data)
print(f"Features shape: {X_train.shape}")
```

---

## Physics Model

### PhysicsWellModel

Physics-based model for drilling operations.

#### Constructor

```python
from src.models.physics_model import PhysicsWellModel

physics_model = PhysicsWellModel(config=None)
```

**Parameters:**
- `config` (dict, optional): Configuration dictionary

#### Methods

##### calculate_formation_pressure(depth)

Calculate formation pressure at given depth.

**Parameters:**
- `depth` (float): Depth in feet

**Returns:**
- `float`: Formation pressure in psi

**Example:**
```python
pressure = physics_model.calculate_formation_pressure(5000)
print(f"Formation pressure: {pressure} psi")
```

##### calculate_fracture_pressure(depth)

Calculate fracture pressure at given depth.

**Parameters:**
- `depth` (float): Depth in feet

**Returns:**
- `float`: Fracture pressure in psi

##### calculate_hydrostatic_pressure(depth, mud_weight)

Calculate hydrostatic pressure.

**Parameters:**
- `depth` (float): Depth in feet
- `mud_weight` (float): Mud weight in ppg

**Returns:**
- `float`: Hydrostatic pressure in psi

**Formula:**
```
P = 0.052 × mud_weight × depth
```

##### calculate_rop(wob, rpm, diff_pressure)

Calculate Rate of Penetration.

**Parameters:**
- `wob` (float): Weight on bit (klbs)
- `rpm` (float): Rotary speed (RPM)
- `diff_pressure` (float): Differential pressure (psi)

**Returns:**
- `float`: Rate of penetration (ft/hr)

**Formula:**
```
ROP = k × WOB^0.5 × RPM^0.6 × ΔP^0.1
```

##### calculate_torque(wob, rpm, depth)

Calculate drilling torque.

**Parameters:**
- `wob` (float): Weight on bit (klbs)
- `rpm` (float): Rotary speed (RPM)
- `depth` (float): Depth (feet)

**Returns:**
- `float`: Torque (klb-ft)

##### check_wellbore_stability(depth, mud_weight)

Check wellbore stability based on pressure balance.

**Parameters:**
- `depth` (float): Depth (feet)
- `mud_weight` (float): Mud weight (ppg)

**Returns:**
- `dict`: Stability indicators including:
  - is_stable (bool)
  - formation_pressure (float)
  - fracture_pressure (float)
  - hydrostatic_pressure (float)
  - overbalance (float)
  - underbalance (float)
  - stability_index (float)

**Example:**
```python
stability = physics_model.check_wellbore_stability(5000, 12.0)
if stability['is_stable']:
    print("Wellbore is stable")
else:
    print(f"Stability index: {stability['stability_index']}")
```

##### predict_physics_based_risks(drilling_params)

Predict risks based on physics equations.

**Parameters:**
- `drilling_params` (dict): Current drilling parameters

**Returns:**
- `dict`: Risk predictions (0-1 scale) for:
  - wellbore_instability
  - stuck_pipe
  - kick_risk
  - stability_details

---

## ML Models

### MLRiskPredictor

Machine learning-based risk predictor.

#### Constructor

```python
from src.models.ml_models import MLRiskPredictor

ml_predictor = MLRiskPredictor(config=None)
```

#### Methods

##### train(X_train, y_targets, scaler)

Train ML models on drilling data.

**Parameters:**
- `X_train` (np.ndarray): Training features
- `y_targets` (tuple): Tuple of (wellbore, stuck_pipe, kick) targets
- `scaler`: Feature scaler

**Example:**
```python
ml_predictor.train(X_train, y_targets, scaler)
```

##### predict(X)

Predict risks using trained models.

**Parameters:**
- `X` (np.ndarray): Feature array

**Returns:**
- `dict`: Risk predictions with keys:
  - wellbore_instability
  - stuck_pipe
  - kick_risk

**Example:**
```python
X = np.array([[5000, 25, 120, 500, 2500, 15, 60, 12, 150]])
risks = ml_predictor.predict(X)
print(f"Kick risk: {risks['kick_risk'][0]:.2%}")
```

##### save_models(save_dir)

Save trained models to disk.

**Parameters:**
- `save_dir` (str): Directory to save models

##### load_models(load_dir)

Load trained models from disk.

**Parameters:**
- `load_dir` (str): Directory containing saved models

---

## Hybrid Digital Twin

### HybridDigitalTwin

Combines physics-based and ML models.

#### Constructor

```python
from src.models.hybrid_twin import HybridDigitalTwin

twin = HybridDigitalTwin(config=None)
```

#### Methods

##### train_ml_component(X_train, y_targets, scaler)

Train the ML component of hybrid model.

**Parameters:**
- `X_train` (np.ndarray): Training features
- `y_targets` (tuple): Target values
- `scaler`: Feature scaler

##### predict_risks(drilling_params, use_ml=True)

Predict drilling risks using hybrid model.

**Parameters:**
- `drilling_params` (dict or np.ndarray): Current drilling parameters
- `use_ml` (bool): Whether to use ML model (default: True)

**Returns:**
- `dict`: Combined risk predictions

**Example:**
```python
params = {
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

risks = twin.predict_risks(params, use_ml=True)
print(f"Wellbore instability: {risks['wellbore_instability']:.2%}")
```

##### get_recommendations(risks, drilling_params)

Generate recommendations based on risk predictions.

**Parameters:**
- `risks` (dict): Risk predictions
- `drilling_params` (dict): Current drilling parameters

**Returns:**
- `list`: List of recommendation dicts with keys:
  - risk_type
  - severity
  - action
  - priority

**Example:**
```python
recommendations = twin.get_recommendations(risks, params)
for rec in recommendations:
    print(f"{rec['severity']}: {rec['action']}")
```

##### save_models(save_dir)

Save models to disk.

##### load_models(load_dir)

Load models from disk.

---

## Autonomous Optimizer

### AutonomousOptimizer

Autonomous optimization engine for drilling operations.

#### Constructor

```python
from src.optimization.optimizer import AutonomousOptimizer

optimizer = AutonomousOptimizer(config=None)
```

#### Methods

##### optimize_parameters(current_params, risks, recommendations)

Calculate optimized drilling parameters.

**Parameters:**
- `current_params` (dict): Current drilling parameters
- `risks` (dict): Risk predictions
- `recommendations` (list): Recommended actions

**Returns:**
- `tuple`: (optimized_params, adjustments)
  - optimized_params: Dict of optimized parameters
  - adjustments: List of adjustment descriptions

**Example:**
```python
optimized, adjustments = optimizer.optimize_parameters(
    current_params, risks, recommendations
)
print(f"Optimized WOB: {optimized['wob']} klbs")
for adj in adjustments:
    print(f"- {adj}")
```

##### calculate_efficiency_score(params, risks)

Calculate drilling efficiency score.

**Parameters:**
- `params` (dict): Drilling parameters
- `risks` (dict): Risk predictions

**Returns:**
- `float`: Efficiency score (0-100)

**Example:**
```python
score = optimizer.calculate_efficiency_score(params, risks)
print(f"Efficiency: {score:.1f}/100")
```

##### optimize_for_sustainability(params)

Optimize parameters for reduced environmental impact.

**Parameters:**
- `params` (dict): Current drilling parameters

**Returns:**
- `tuple`: (optimized_params, sustainability_metrics)

**Example:**
```python
optimized, metrics = optimizer.optimize_for_sustainability(params)
print(f"Fuel reduction: {metrics['fuel_reduction_percent']:.1f}%")
print(f"CO2 saved: {metrics['estimated_co2_saved_kg_per_hour']:.2f} kg/hr")
```

---

## Utilities

### Configuration

```python
from src.utils import load_config

config = load_config(config_path=None)
```

Load configuration from YAML file.

### Logging

```python
from src.utils import setup_logger

logger = setup_logger(name, log_file=None, level=logging.INFO)
logger.info("Message")
```

Setup logger with console and file handlers.

### Path Utilities

```python
from src.utils import get_data_path, ensure_dir

data_path = get_data_path('training_data.csv')
ensure_dir('models/trained')
```

---

## Error Handling

All methods may raise the following exceptions:

- `ValueError`: Invalid parameter values
- `FileNotFoundError`: Missing files or directories
- `RuntimeError`: Model not trained or runtime errors

**Example error handling:**
```python
try:
    risks = twin.predict_risks(params)
except ValueError as e:
    print(f"Invalid parameters: {e}")
except RuntimeError as e:
    print(f"Model error: {e}")
```

---

## Type Hints

The codebase uses type hints for better code clarity:

```python
def calculate_rop(self, wob: float, rpm: float, diff_pressure: float) -> float:
    ...
```

---

## Constants and Enums

### Risk Severity Levels
- LOW: 0-30%
- MEDIUM: 30-60%
- HIGH: 60-100%

### Parameter Ranges
- WOB: 10-40 klbs
- RPM: 60-180
- Flow Rate: 300-700 gpm
- Mud Weight: 8.5-16.0 ppg

---

## Complete Example

```python
from src.data.data_collector import DrillingDataCollector
from src.models.hybrid_twin import HybridDigitalTwin
from src.optimization.optimizer import AutonomousOptimizer

# Initialize components
collector = DrillingDataCollector()
twin = HybridDigitalTwin()
optimizer = AutonomousOptimizer()

# Generate and train
data = collector.generate_sample_data(1000)
X_train, y_targets, scaler = collector.preprocess_data(data)
twin.train_ml_component(X_train, y_targets, scaler)

# Real-time prediction
current_data = collector.collect_realtime_data()
risks = twin.predict_risks(current_data, use_ml=True)
recommendations = twin.get_recommendations(risks, current_data)
optimized, adjustments = optimizer.optimize_parameters(
    current_data, risks, recommendations
)

# Display results
print(f"Risks: {risks}")
print(f"Recommendations: {len(recommendations)}")
print(f"Optimized WOB: {optimized['wob']:.2f} klbs")
```
