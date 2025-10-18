# System Architecture

## Overview

The AI Drilling Optimization System is a modular, scalable system that combines physics-based modeling with machine learning to provide real-time drilling optimization and risk prediction.

## Architecture Components

### 1. Data Collection Layer (`src/data/`)

**DrillingDataCollector**
- Simulates real-time data collection from drilling sensors
- Generates synthetic training data
- Preprocesses data for ML models
- Handles feature scaling and normalization

**Key Features:**
- Real-time data streaming simulation
- Historical data generation
- Feature engineering
- Data validation and cleaning

### 2. Modeling Layer (`src/models/`)

#### PhysicsWellModel
Physics-based model implementing fundamental drilling equations:

**Capabilities:**
- Formation pressure calculation
- Fracture pressure estimation
- Hydrostatic pressure modeling
- ROP prediction
- Torque calculation
- Hydraulic horsepower computation
- Wellbore stability analysis

**Equations Implemented:**
```
Formation Pressure = gradient × depth
Hydrostatic Pressure = 0.052 × mud_weight × depth
ROP = k × WOB^0.5 × RPM^0.6 × ΔP^0.1
Torque = bit_torque + friction_torque + viscous_torque
```

#### MLRiskPredictor
Machine learning models for risk prediction:

**Models:**
- Neural Networks (TensorFlow/Keras)
  - 3 hidden layers with dropout
  - Binary classification for each risk type
  - Adam optimizer
- Random Forest ensemble
  - 100 estimators per risk type
  - Feature importance analysis

**Risk Types:**
1. Wellbore Instability
2. Stuck Pipe
3. Kick Risk

#### HybridDigitalTwin
Combines physics and ML models:

**Architecture:**
```
Input Parameters
    ↓
Physics Model (30%) + ML Model (70%)
    ↓
Combined Risk Predictions
    ↓
Recommendation Engine
    ↓
Optimized Parameters
```

### 3. Optimization Layer (`src/optimization/`)

**AutonomousOptimizer**
Real-time parameter optimization engine:

**Features:**
- Risk-based parameter adjustment
- Bounded optimization (safety constraints)
- Sustainability optimization
- Efficiency score calculation

**Optimization Strategy:**
- If wellbore instability > 0.7: Reduce WOB, increase mud weight
- If stuck pipe risk > 0.6: Increase flow rate, reduce RPM
- If kick risk > 0.8: CRITICAL - increase mud weight immediately

### 4. Dashboard Layer (`src/dashboard/`)

**Interactive Streamlit Dashboard**

**Real-time Mode:**
- Live parameter monitoring
- Risk indicator gauges
- Optimization recommendations
- Historical trend charts
- Sustainability metrics

**Historical Analysis Mode:**
- Batch data analysis
- Statistical summaries
- Correlation analysis
- Performance trends

### 5. Utility Layer (`src/utils/`)

**Support Functions:**
- Configuration management
- Logging setup
- Path utilities
- Directory management

## Data Flow

```
┌─────────────────────┐
│  Sensor Data Input  │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Data Collector     │
│  - Preprocessing    │
│  - Validation       │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────────────────────┐
│     Hybrid Digital Twin             │
│  ┌────────────┐  ┌────────────┐    │
│  │  Physics   │  │     ML     │    │
│  │   Model    │  │   Models   │    │
│  └─────┬──────┘  └──────┬─────┘    │
│        │                 │          │
│        └────────┬────────┘          │
│                 ↓                   │
│        ┌────────────────┐           │
│        │  Risk Fusion   │           │
│        └────────┬───────┘           │
└─────────────────┼───────────────────┘
                  │
                  ↓
┌─────────────────────────────────────┐
│   Autonomous Optimizer              │
│   - Parameter Adjustment            │
│   - Constraint Satisfaction         │
│   - Sustainability Optimization     │
└──────────┬──────────────────────────┘
           │
           ↓
┌─────────────────────┐
│   Dashboard         │
│   - Visualization   │
│   - Recommendations │
│   - Alerts          │
└─────────────────────┘
```

## Risk Prediction Pipeline

1. **Data Acquisition**: Collect current drilling parameters
2. **Feature Extraction**: Extract relevant features for models
3. **Physics Analysis**: Calculate physics-based risk indicators
4. **ML Inference**: Run trained models for risk prediction
5. **Fusion**: Combine physics and ML predictions
6. **Thresholding**: Compare against configured thresholds
7. **Recommendation**: Generate actionable recommendations

## Optimization Pipeline

1. **Risk Assessment**: Evaluate current risks
2. **Parameter Analysis**: Analyze current parameter values
3. **Constraint Definition**: Apply operational constraints
4. **Optimization**: Calculate optimal parameter adjustments
5. **Validation**: Ensure adjustments are safe and bounded
6. **Application**: Apply optimized parameters

## Scalability Considerations

**Horizontal Scaling:**
- Stateless services for easy replication
- Modular design allows component-wise scaling
- Queue-based architecture for high-throughput scenarios

**Vertical Scaling:**
- Efficient algorithms (O(n) or better)
- Batch processing support
- Model optimization techniques

**Future Extensions:**
- Multiple well monitoring
- Distributed training
- Cloud deployment
- Real-time data streaming integration
- API for rig control systems

## Security Considerations

- Input validation on all parameters
- Bounded optimization to prevent unsafe operations
- Logging and audit trails
- Configuration-based safety thresholds
- Emergency shutdown protocols

## Performance Metrics

**Model Performance:**
- Accuracy, Precision, Recall for risk prediction
- F1 Score for balanced evaluation
- AUC-ROC for classification performance

**System Performance:**
- Latency: < 100ms for prediction
- Throughput: 100+ predictions/second
- Dashboard refresh: 2-5 seconds

## Integration Points

**Input Integration:**
- Sensor data APIs
- SCADA systems
- Drilling databases
- Real-time data streams

**Output Integration:**
- Rig control systems
- Alarm systems
- Reporting dashboards
- Data historians
