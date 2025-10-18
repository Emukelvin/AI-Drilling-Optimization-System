# API Reference

## Core Components

### Hybrid Digital Twin

#### DigitalTwin Class

Main class for hybrid digital twin integration.

```python
from src.hybrid_twin import DigitalTwin

twin = DigitalTwin()
```

**Methods:**

##### `update_state(drilling_params, formation_params)`
Updates the digital twin state with current parameters.

**Parameters:**
- `drilling_params` (dict): Drilling parameter dictionary
  - `wob` (float): Weight on Bit (kN)
  - `rpm` (float): Rotary Speed (RPM)
  - `flow_rate` (float): Flow rate (LPM)
  - `mud_weight` (float): Mud weight (kg/m³)
  - `bit_diameter` (float): Bit diameter (inches)
  - `pipe_od` (float): Pipe outer diameter (inches)
  - `tvd` (float): True vertical depth (m)
  - `bit_wear` (float): Bit wear factor (0-1)

- `formation_params` (dict): Formation parameter dictionary
  - `formation_strength` (float): Compressive strength (MPa)
  - `formation_abrasiveness` (float): Abrasiveness (0-1)
  - `pore_pressure` (float): Pore pressure (bar)
  - `fracture_gradient` (float): Fracture gradient (kg/m³)

**Returns:**
- `dict`: Complete state dictionary with all calculated parameters

##### `get_overall_risk_score()`
Calculate overall drilling risk score.

**Returns:**
- `float`: Risk score (0-1, higher is worse)

##### `get_efficiency_score()`
Calculate overall drilling efficiency score.

**Returns:**
- `float`: Efficiency score (0-1, higher is better)

##### `get_sustainability_score()`
Calculate sustainability score.

**Returns:**
- `float`: Sustainability score (0-1, higher is better)

##### `optimize_parameters(target_rop, max_risk, constraints)`
Optimize drilling parameters to achieve target ROP.

**Parameters:**
- `target_rop` (float): Target Rate of Penetration (m/hr)
- `max_risk` (float): Maximum acceptable overall risk (0-1)
- `constraints` (dict, optional): Parameter constraints

**Returns:**
- `dict`: Optimized parameters

##### `get_recommendations(target_rop)`
Get comprehensive recommendations for drilling optimization.

**Parameters:**
- `target_rop` (float, optional): Target ROP

**Returns:**
- `dict`: Recommendations including current state, optimized parameters, and alerts

---

### Physics Models

#### DrillingMechanics Class

Physics-based drilling mechanics model.

```python
from src.physics_models import DrillingMechanics

mechanics = DrillingMechanics()
```

**Key Methods:**

- `calculate_rop(wob, rpm, bit_diameter, formation_strength, bit_wear)`: Calculate Rate of Penetration
- `calculate_torque(wob, bit_diameter, friction_coefficient)`: Calculate drilling torque
- `calculate_axial_vibration(wob, rpm, bit_aggressiveness)`: Calculate vibration severity
- `calculate_bit_wear_rate(wob, rpm, formation_abrasiveness)`: Calculate bit wear rate
- `predict_stuck_pipe_risk(wob, torque, differential_pressure)`: Predict stuck pipe risk

#### DrillingHydraulics Class

Physics-based drilling hydraulics model.

```python
from src.physics_models import DrillingHydraulics

hydraulics = DrillingHydraulics()
```

**Key Methods:**

- `calculate_ecd(mud_weight, flow_rate, tvd, hole_diameter, pipe_od)`: Calculate ECD
- `calculate_friction_pressure_loss(flow_rate, mud_density, mud_viscosity, pipe_length, pipe_diameter)`: Calculate pressure loss
- `predict_lost_circulation_risk(ecd, formation_fracture_gradient, mud_weight)`: Predict lost circulation risk
- `predict_kick_risk(mud_weight, formation_pore_pressure)`: Predict kick risk
- `calculate_hydraulic_horsepower(flow_rate, pressure)`: Calculate hydraulic horsepower

---

### ML Models

#### RiskPredictor Class

ML-based risk prediction model.

```python
from src.ml_models import RiskPredictor

predictor = RiskPredictor()
```

**Methods:**

- `train(data, risk_labels, test_size)`: Train risk prediction models
- `predict_risk(data, risk_type)`: Predict specific risk type
- `predict_all_risks(data)`: Predict all risk types
- `get_risk_score(...)`: Get risk scores for single parameter set
- `save_models(directory)`: Save trained models
- `load_models(directory)`: Load trained models

#### WellboreStabilityModel Class

Wellbore stability prediction model.

```python
from src.ml_models import WellboreStabilityModel

stability = WellboreStabilityModel()
```

**Methods:**

- `calculate_stability_index(mud_weight, pore_pressure, fracture_gradient, tvd, formation_strength)`: Calculate stability index
- `predict_instability_risk(...)`: Predict various instability risks
- `predict_collapse_pressure(formation_strength, pore_pressure, tvd)`: Predict collapse pressure

#### ROPOptimizer Class

ROP optimization model.

```python
from src.ml_models import ROPOptimizer

optimizer = ROPOptimizer()
```

**Methods:**

- `predict_rop(wob, rpm, flow_rate, mud_weight, formation_strength, bit_wear)`: Predict ROP
- `optimize_parameters(target_rop, formation_strength, bit_wear, constraints)`: Find optimal parameters
- `recommend_adjustments(current_rop, target_rop, current_params, formation_strength)`: Recommend parameter adjustments

---

### Utilities

#### DrillingDataGenerator Class

Generate synthetic drilling data.

```python
from src.utils import DrillingDataGenerator

generator = DrillingDataGenerator()
```

**Methods:**

- `generate_complete_dataset(num_samples, well_depth)`: Generate complete synthetic dataset
- `generate_case_study_data(scenario)`: Generate scenario-specific data
- `generate_risk_labels(data)`: Generate risk labels for training
- `save_dataset(data, filepath)`: Save dataset to CSV
- `load_dataset(filepath)`: Load dataset from CSV

#### Config Class

Configuration management.

```python
from src.utils import Config

config = Config()
```

**Methods:**

- `get(key_path, default)`: Get configuration value
- `set(key_path, value)`: Set configuration value
- `get_drilling_params()`: Get default drilling parameters
- `get_formation_params()`: Get default formation parameters
- `save_to_file(filepath)`: Save configuration to YAML
- `load_from_file(filepath)`: Load configuration from YAML

---

## Example Usage

### Complete Workflow Example

```python
from src.hybrid_twin import DigitalTwin
from src.utils import DrillingDataGenerator, Config

# Initialize
config = Config()
twin = DigitalTwin()
generator = DrillingDataGenerator()

# Generate training data
data = generator.generate_complete_dataset(1000)
generator.save_dataset(data, 'data/synthetic/training_data.csv')

# Set up parameters
drilling_params = {
    'wob': 80.0,
    'rpm': 120.0,
    'flow_rate': 1000.0,
    'mud_weight': 1200.0,
    'bit_diameter': 12.25,
    'pipe_od': 5.0,
    'tvd': 2000.0,
    'bit_wear': 0.1
}

formation_params = {
    'formation_strength': 30.0,
    'formation_abrasiveness': 0.5,
    'pore_pressure': 300.0,
    'fracture_gradient': 1800.0
}

# Update state
state = twin.update_state(drilling_params, formation_params)

# Get metrics
risk = twin.get_overall_risk_score()
efficiency = twin.get_efficiency_score()
sustainability = twin.get_sustainability_score()

print(f"ROP: {state['rop']:.2f} m/hr")
print(f"Risk: {risk:.2%}")
print(f"Efficiency: {efficiency:.2%}")
print(f"Sustainability: {sustainability:.2%}")

# Optimize
recommendations = twin.get_recommendations(target_rop=25.0)
optimized = recommendations['optimized_parameters']

print(f"\nOptimized WOB: {optimized['wob']:.1f} kN")
print(f"Expected ROP: {optimized['predicted_rop']:.1f} m/hr")
```

### Risk Monitoring Example

```python
from src.hybrid_twin import DigitalTwin

twin = DigitalTwin()

# Update state
state = twin.update_state(drilling_params, formation_params)

# Check specific risks
if state['hybrid_stuck_pipe_risk'] > 0.6:
    print("WARNING: High stuck pipe risk!")
    
if state['hybrid_kick_risk'] > 0.6:
    print("CRITICAL: High kick risk detected!")

# Get alerts
alerts = twin._generate_alerts()
for alert in alerts:
    print(f"{alert['severity'].upper()}: {alert['message']}")
```

### Optimization Example

```python
from src.hybrid_twin import DigitalTwin

twin = DigitalTwin()

# Current state
state = twin.update_state(drilling_params, formation_params)
current_rop = state['rop']

# Optimize for higher ROP with safety constraints
target_rop = current_rop * 1.5  # 50% improvement
max_risk = 0.3  # Maximum acceptable risk

optimized = twin.optimize_parameters(
    target_rop=target_rop,
    max_risk=max_risk,
    constraints={
        'wob': (40, 140),
        'rpm': (80, 160),
        'flow_rate': (700, 1800),
        'mud_weight': (1100, 1400)
    }
)

print(f"Current ROP: {current_rop:.1f} m/hr")
print(f"Target ROP: {target_rop:.1f} m/hr")
print(f"Optimized ROP: {optimized['predicted_rop']:.1f} m/hr")
print(f"Risk: {optimized['estimated_risk']:.2%}")
```
