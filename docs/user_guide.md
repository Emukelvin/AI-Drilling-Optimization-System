# User Guide

## Introduction

This guide provides comprehensive instructions for using the AI Drilling Optimization System to monitor drilling operations, predict risks, and optimize parameters in real-time.

## Dashboard Overview

### Launching the Dashboard

```bash
streamlit run src/dashboard/app.py
```

The dashboard opens at `http://localhost:8501` with two main modes:
1. **Real-time Simulation**: Live drilling monitoring and optimization
2. **Historical Analysis**: Analyze past drilling data and trends

## Real-time Simulation Mode

### Getting Started

1. **Train Models** (First Time Only)
   - Click the "Train Models" button in the header
   - Wait 1-2 minutes for training to complete
   - Status will change to "🟢 Trained"

2. **Monitor Real-time Data**
   - View live drilling metrics (Depth, ROP, WOB, RPM, Torque)
   - Observe risk indicators for three main hazards
   - Review optimization recommendations

### Understanding the Dashboard Sections

#### 1. Real-time Drilling Metrics

Located at the top of the dashboard, showing:

- **Depth (ft)**: Current drilling depth with rate of change
- **ROP (ft/hr)**: Rate of Penetration - drilling speed
- **WOB (klbs)**: Weight on Bit - force applied to drill bit
- **RPM**: Rotary speed of the drill string
- **Torque (klb-ft)**: Rotational resistance

**Interpretation:**
- Higher ROP = faster drilling (but monitor for risks)
- WOB typically 20-30 klbs for optimal drilling
- RPM usually 80-150 depending on formation
- Monitor torque for stuck pipe indicators

#### 2. Risk Assessment

Three risk indicators with color-coded severity:

**Wellbore Instability**
- 🟢 Green (0-30%): Stable wellbore
- 🟡 Yellow (30-60%): Monitor closely
- 🔴 Red (60-100%): High risk - take action

**Stuck Pipe Risk**
- Caused by: High torque, poor hole cleaning
- Actions: Increase circulation, reduce RPM

**Kick Risk**
- Most critical risk (formation fluid influx)
- Immediate action required if red
- Monitor pressure and flow rate

#### 3. Optimization Recommendations

System-generated recommendations based on current risks:

**Priority Levels:**
- Priority 1: Immediate action required
- Priority 2: Action recommended soon
- Priority 3: Monitor and consider

**Example Recommendations:**
```
🔴 CRITICAL: Kick Risk: Increase mud weight immediately
🟡 HIGH: Wellbore Instability: Reduce weight on bit by 10-15%
🟢 LOW: Monitor standpipe pressure trends
```

#### 4. Real-time Monitoring Charts

**ROP Chart:**
- Shows drilling speed over time
- Look for consistent trends
- Sudden drops may indicate problems

**Risk Trends:**
- Three lines showing risk evolution
- Helps identify patterns
- Early warning system

#### 5. Sustainability Metrics

Environmental impact tracking:

- **Fuel Consumption**: Gallons per hour
- **CO2 Emissions**: Kilograms per hour
- **Target Reduction**: Configured goal (default 15%)
- **Efficiency Score**: Overall drilling efficiency (0-100)

### Using Manual Controls

The sidebar allows manual parameter adjustment:

#### Weight on Bit (WOB)
- Range: 10-40 klbs
- Optimal: Usually 20-30 klbs
- ⬆️ Increase for: Faster drilling in hard formations
- ⬇️ Decrease for: Wellbore stability, reduce bit wear

#### Rotary Speed (RPM)
- Range: 60-180 RPM
- Optimal: Usually 100-140 RPM
- ⬆️ Increase for: Better hole cleaning, faster drilling
- ⬇️ Decrease for: Reduce stuck pipe risk, tool damage

#### Flow Rate
- Range: 300-700 gpm
- Optimal: Usually 450-550 gpm
- ⬆️ Increase for: Better cuttings removal, cool bit
- ⬇️ Decrease for: Reduce pressure losses, wellbore erosion

#### Mud Weight
- Range: 8.5-16.0 ppg (pounds per gallon)
- Optimal: Depends on formation pressure
- ⬆️ Increase for: Control formation pressure, prevent kicks
- ⬇️ Decrease for: Increase ROP, reduce formation damage

### Sustainability Optimization

Enable "Sustainability Optimization" in sidebar to:

- Automatically adjust parameters for fuel efficiency
- Reduce CO2 emissions
- Maintain drilling performance
- Track environmental KPIs

**Expected Results:**
- 10-15% fuel reduction
- Proportional CO2 reduction
- Minimal impact on ROP

## Historical Analysis Mode

### Using Historical Analysis

1. Click "Historical Analysis" mode in sidebar
2. Click "Generate Historical Data"
3. View summary statistics and charts

### Available Analyses

#### Summary Statistics
- Mean, median, std dev for all parameters
- Min/max values
- Quartile analysis

#### ROP vs Depth Chart
- Shows how drilling speed changes with depth
- Identifies efficient zones
- Spots problematic formations

#### WOB vs ROP Scatter
- Correlation between weight and drilling speed
- Color-coded by depth
- Optimal WOB identification

### Interpreting Historical Data

**Good Indicators:**
- Consistent ROP across depth intervals
- Low risk levels (<30%)
- Efficient parameter utilization

**Warning Signs:**
- Declining ROP trends
- Increasing risk trends
- High parameter variability

## Best Practices

### Operational Best Practices

1. **Monitor Continuously**
   - Keep dashboard open during operations
   - Set up on dedicated monitor
   - Review every 5-10 minutes

2. **Respond to Alerts**
   - Priority 1: Immediate action
   - Priority 2: Within 15 minutes
   - Priority 3: Plan for next activity

3. **Document Decisions**
   - Note parameter changes
   - Record reasons for adjustments
   - Track outcomes

4. **Review Historical Trends**
   - Daily review of efficiency scores
   - Weekly sustainability reports
   - Monthly performance analysis

### Parameter Adjustment Guidelines

**Conservative Approach:**
- Make small changes (5-10%)
- Wait 10-15 minutes to see effects
- Document each change

**Emergency Situations:**
- Kick risk: Immediate mud weight increase
- Stuck pipe: Stop rotation, increase circulation
- Wellbore collapse: Reduce WOB, increase mud weight

### Optimization Strategies

**For Maximum ROP:**
```
1. Maintain optimal WOB (25-30 klbs)
2. High RPM (120-140)
3. Good circulation (500+ gpm)
4. Monitor bit wear
```

**For Wellbore Stability:**
```
1. Appropriate mud weight
2. Moderate WOB (20-25 klbs)
3. Steady ROP
4. Good hole cleaning
```

**For Sustainability:**
```
1. Enable sustainability optimization
2. Balance ROP with fuel consumption
3. Use efficient parameter combinations
4. Monitor emissions trends
```

## Advanced Features

### Customizing Risk Thresholds

Edit `config/config.yaml`:

```yaml
risk_thresholds:
  wellbore_instability: 0.7  # Adjust 0-1
  stuck_pipe: 0.6
  kick_risk: 0.8
```

### Adjusting Optimization Constraints

```yaml
optimization:
  update_interval: 5
  max_wob_adjustment: 10  # Percentage
  max_rpm_adjustment: 15
  max_flow_rate_adjustment: 8
```

### Training with Custom Data

Replace synthetic data with your drilling data:

```python
from src.models.hybrid_twin import HybridDigitalTwin
import pandas as pd

# Load your data
data = pd.read_csv('your_drilling_data.csv')

# Train models
twin = HybridDigitalTwin()
# ... preprocessing and training code
```

## Troubleshooting

### Dashboard Issues

**Dashboard not updating:**
- Check refresh rate in config
- Verify models are trained
- Restart dashboard

**High risk false positives:**
- Retrain with more data
- Adjust risk thresholds
- Review parameter ranges

**Slow performance:**
- Reduce data history size
- Decrease refresh rate
- Close other applications

### Model Performance Issues

**Low accuracy:**
- Increase training samples
- Add more features
- Adjust model hyperparameters

**Overfitting:**
- Increase dropout rate
- Reduce model complexity
- Use more training data

## Tips and Tricks

1. **Multiple Monitors**: Display dashboard on second screen
2. **Screenshot Alerts**: Capture screen when risks are high
3. **Export Data**: Save historical data for reporting
4. **Compare Operations**: Use historical mode to compare wells
5. **Seasonal Adjustments**: Adjust thresholds based on experience

## Support and Feedback

For issues or questions:
- Check documentation first
- Review logs in `logs/` directory
- Submit GitHub issue with details
- Include screenshots if relevant

## Next Steps

- Explore [API Reference](api_reference.md) for programmatic usage
- Review [Architecture](architecture.md) for technical details
- Check [Setup Guide](setup.md) for advanced configuration
