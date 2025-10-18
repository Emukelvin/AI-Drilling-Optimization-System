# User Manual

## Getting Started

### Installation

1. **Prerequisites**
   - Python 3.8 or higher
   - pip package manager
   - At least 2GB free RAM
   - Modern web browser for dashboard

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python main.py simulate
   ```

### First Run

Generate synthetic training data before first use:

```bash
python main.py generate-data --samples 1000
```

This creates training datasets in `data/synthetic/` directory.

---

## Using the Dashboard

### Launching

Start the interactive dashboard:

```bash
python main.py dashboard
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

### Dashboard Sections

#### 1. Real-Time Monitoring Tab

**Purpose**: Monitor current drilling operations in real-time

**Features**:
- Key performance metrics (ROP, Risk, Efficiency, Sustainability, ECD)
- Detailed drilling parameters table
- Performance metrics display
- Active alerts and warnings

**How to Use**:
1. Adjust drilling parameters using sidebar sliders
2. Observe real-time updates in metrics
3. Monitor alerts for safety warnings
4. Review detailed parameter tables

**Key Metrics Explained**:
- **ROP (Rate of Penetration)**: Speed of drilling in meters per hour
- **Overall Risk**: Combined risk score from all risk categories
- **Efficiency**: How effectively energy is converted to drilling progress
- **Sustainability**: Environmental impact score
- **ECD (Equivalent Circulating Density)**: Effective mud weight during circulation

#### 2. Optimization Tab

**Purpose**: Find optimal drilling parameters for target performance

**Features**:
- Target ROP setting
- Maximum risk tolerance
- Optimization algorithm
- Current vs optimized comparison
- Apply optimized parameters

**How to Use**:
1. Set your target ROP using slider
2. Set maximum acceptable risk level
3. Click "Optimize Parameters" button
4. Review recommended parameter changes
5. Click "Apply Optimized Parameters" to use recommendations

**Best Practices**:
- Start with conservative targets
- Always review risk scores before applying
- Test optimized parameters in simulation first
- Monitor alerts after applying changes

#### 3. Risk Prediction Tab

**Purpose**: Detailed analysis of drilling risks

**Features**:
- Individual risk scores for each risk type
- Physics vs ML vs Hybrid comparison
- Wellbore stability gauge
- Pressure-related risk analysis

**Risk Types**:
- **Stuck Pipe**: Risk of drill string becoming stuck
- **Kick**: Risk of formation fluid influx
- **Lost Circulation**: Risk of mud loss to formation
- **Wellbore Instability**: Risk of wellbore collapse or fracture

**Risk Levels**:
- 🟢 Green (0-30%): Low risk, safe operations
- 🟡 Yellow (30-60%): Moderate risk, caution advised
- 🔴 Red (60-100%): High risk, immediate action required

**How to Interpret**:
- Compare physics-based, ML-based, and hybrid predictions
- Hybrid predictions combine both approaches for reliability
- Monitor stability index for wellbore health
- Watch for collapse and fracture risks

#### 4. Analytics Tab

**Purpose**: Historical performance analysis

**Features**:
- Performance trends over time
- ROP, risk, efficiency, and sustainability charts
- Summary statistics
- Historical data export

**How to Use**:
1. Review trend charts for patterns
2. Check summary statistics for averages
3. Identify periods of high performance or risk
4. Use insights to improve future operations

**Key Insights**:
- Increasing ROP trends indicate optimization success
- Rising risk scores suggest parameter adjustment needed
- Efficiency trends show energy usage patterns
- Sustainability scores track environmental impact

#### 5. Settings Tab

**Purpose**: Configure system parameters and thresholds

**Features**:
- Safety threshold configuration
- Model weight adjustment (physics vs ML)
- Data generation tools
- System information

**Configuration Options**:
- **Maximum Risk Threshold**: System-wide risk limit
- **Minimum Efficiency Threshold**: Acceptable efficiency floor
- **Maximum Vibration**: Vibration tolerance
- **Maximum Bit Wear Rate**: Bit replacement criteria
- **Physics Model Weight**: Balance between physics and ML predictions

---

## Using the Console Simulation

### Basic Simulation

Run a quick simulation without the dashboard:

```bash
python main.py simulate
```

**Output Includes**:
- Current drilling parameters
- Performance metrics (ROP, torque, ECD, efficiency)
- Risk assessment breakdown
- Optimized parameter recommendations
- Active alerts
- Sustainability score

**Use Cases**:
- Quick parameter testing
- Batch simulations
- Script integration
- Headless environments

---

## Working with Data

### Synthetic Data Generation

Generate training datasets:

```bash
# Generate 1000 samples
python main.py generate-data --samples 1000

# Generate larger dataset
python main.py generate-data --samples 5000
```

**Generated Files**:
- `data/synthetic/training_data.csv`: Main training dataset
- `data/synthetic/case_study_normal.csv`: Normal conditions scenario
- `data/synthetic/case_study_high_risk.csv`: High risk scenario
- `data/synthetic/case_study_optimal.csv`: Optimal conditions scenario

### Using Real Data

1. **Prepare Data**:
   - Format your data as CSV with required columns
   - Include: wob, rpm, flow_rate, mud_weight, formation_strength, etc.

2. **Place Data**:
   - Copy CSV files to `data/real/` directory

3. **Load Data**:
   ```python
   from src.utils import DrillingDataGenerator
   
   generator = DrillingDataGenerator()
   data = generator.load_dataset('data/real/your_data.csv')
   ```

### Data Format

Required columns for training data:
- `wob`: Weight on Bit (kN)
- `rpm`: Rotary Speed (RPM)
- `flow_rate`: Flow rate (LPM)
- `mud_weight`: Mud weight (kg/m³)
- `formation_strength`: Formation strength (MPa)
- `tvd`: True vertical depth (m)
- `bit_diameter`: Bit diameter (inches)

Optional columns:
- `rop`: Rate of penetration (m/hr)
- `torque`: Drilling torque (kN-m)
- `ecd`: Equivalent circulating density (kg/m³)
- Risk labels for supervised learning

---

## Configuration

### Using Configuration Files

Create custom configuration in YAML:

```yaml
# config/my_config.yaml
drilling:
  default_wob: 100
  default_rpm: 140
  
safety:
  max_risk_threshold: 0.5
```

Load configuration:

```python
from src.utils import Config

config = Config('config/my_config.yaml')
```

### Environment-Specific Settings

Create different configs for different scenarios:
- `config/shallow_well.yaml`: Shallow well parameters
- `config/deep_well.yaml`: Deep well parameters
- `config/hard_formation.yaml`: Hard formation settings

---

## Safety Guidelines

### Risk Management

1. **Monitor Risk Scores**:
   - Always keep overall risk below 0.7
   - Critical risks require immediate action
   - Review alerts regularly

2. **Parameter Changes**:
   - Make incremental adjustments
   - Test changes in simulation first
   - Monitor system response

3. **Optimization**:
   - Set conservative risk limits
   - Validate recommendations
   - Consider operational constraints

### Best Practices

1. **Data Quality**:
   - Use recent, relevant data
   - Validate data accuracy
   - Remove outliers

2. **Model Updates**:
   - Retrain models periodically
   - Validate predictions
   - Monitor model performance

3. **System Monitoring**:
   - Check dashboard regularly
   - Respond to alerts promptly
   - Document unusual events

---

## Troubleshooting

### Common Issues

**Dashboard won't start**:
- Check if port 8501 is available
- Verify Streamlit installation: `pip install streamlit`
- Try: `streamlit run src/dashboard/app.py`

**Import errors**:
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.8+)

**No data displayed**:
- Generate training data: `python main.py generate-data`
- Check data directory exists: `data/synthetic/`

**Optimization not working**:
- Ensure reasonable target ROP
- Check parameter constraints
- Review formation parameters

**High risk scores**:
- Review drilling parameters
- Check formation properties
- Adjust mud weight or flow rate
- Reduce WOB or RPM

---

## Support

For additional help:
1. Check documentation in `docs/` directory
2. Review API reference
3. Open GitHub issue
4. Contact support team

---

## Appendix

### Parameter Ranges

**Typical Operating Ranges**:
- WOB: 40-150 kN
- RPM: 60-200 RPM
- Flow Rate: 500-2000 LPM
- Mud Weight: 1000-1600 kg/m³
- Bit Diameter: 6-17.5 inches

**Formation Properties**:
- Strength: 10-100 MPa
- Pore Pressure: 50-800 bar
- Fracture Gradient: 1400-2200 kg/m³

### Glossary

- **ROP**: Rate of Penetration - drilling speed
- **WOB**: Weight on Bit - downward force
- **RPM**: Rotations Per Minute - bit rotation speed
- **ECD**: Equivalent Circulating Density
- **MSE**: Mechanical Specific Energy
- **NPT**: Non-Productive Time
- **TVD**: True Vertical Depth
- **HHP**: Hydraulic Horsepower
