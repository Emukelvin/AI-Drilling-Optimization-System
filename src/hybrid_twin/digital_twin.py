"""
Hybrid Digital Twin
Integrates physics-based drilling models with ML predictions for real-time optimization.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics_models import DrillingMechanics, DrillingHydraulics
from ml_models import RiskPredictor, WellboreStabilityModel, ROPOptimizer


class DigitalTwin:
    """
    Hybrid Digital Twin combining physics-based models and ML predictions.
    Provides comprehensive real-time drilling optimization and risk prediction.
    """
    
    def __init__(self):
        """Initialize the hybrid digital twin with physics and ML models."""
        # Physics-based models
        self.mechanics = DrillingMechanics()
        self.hydraulics = DrillingHydraulics()
        
        # ML models
        self.risk_predictor = RiskPredictor()
        self.stability_model = WellboreStabilityModel()
        self.rop_optimizer = ROPOptimizer()
        
        # State tracking
        self.current_state = {}
        self.history = []
        
    def update_state(self, drilling_params: Dict[str, float],
                    formation_params: Dict[str, float]) -> Dict[str, float]:
        """
        Update digital twin state with current drilling and formation parameters.
        
        Args:
            drilling_params: Dictionary of drilling parameters
                - wob: Weight on Bit (kN)
                - rpm: Rotary Speed (RPM)
                - flow_rate: Flow rate (LPM)
                - mud_weight: Mud weight (kg/m³)
                - bit_diameter: Bit diameter (inches)
                - pipe_od: Pipe outer diameter (inches)
                - tvd: True Vertical Depth (m)
                - bit_wear: Bit wear factor (0-1)
            formation_params: Dictionary of formation parameters
                - formation_strength: Compressive strength (MPa)
                - formation_abrasiveness: Abrasiveness (0-1)
                - pore_pressure: Pore pressure (bar)
                - fracture_gradient: Fracture gradient (kg/m³)
                
        Returns:
            Comprehensive state dictionary with all calculated parameters
        """
        # Extract parameters
        wob = drilling_params.get('wob', 80)
        rpm = drilling_params.get('rpm', 120)
        flow_rate = drilling_params.get('flow_rate', 1000)
        mud_weight = drilling_params.get('mud_weight', 1200)
        bit_diameter = drilling_params.get('bit_diameter', 12.25)
        pipe_od = drilling_params.get('pipe_od', 5.0)
        tvd = drilling_params.get('tvd', 2000)
        bit_wear = drilling_params.get('bit_wear', 0.0)
        mud_viscosity = drilling_params.get('mud_viscosity', 0.03)
        
        formation_strength = formation_params.get('formation_strength', 30)
        formation_abrasiveness = formation_params.get('formation_abrasiveness', 0.5)
        pore_pressure = formation_params.get('pore_pressure', 300)
        fracture_gradient = formation_params.get('fracture_gradient', 1800)
        
        # Calculate physics-based parameters
        mechanics_params = self.mechanics.calculate_all_parameters(
            wob, rpm, bit_diameter, formation_strength,
            mud_weight, bit_wear, formation_abrasiveness
        )
        
        hydraulics_params = self.hydraulics.calculate_all_parameters(
            flow_rate, mud_weight, mud_viscosity, tvd,
            hole_diameter=bit_diameter, pipe_od=pipe_od,
            formation_fracture_gradient=fracture_gradient,
            formation_pore_pressure=pore_pressure
        )
        
        # Get ML-based risk predictions
        ml_risks = self.risk_predictor.get_risk_score(
            wob, rpm, flow_rate, mud_weight,
            hydraulics_params['ecd'], mechanics_params['torque'],
            mechanics_params['rop'], tvd, formation_strength,
            mechanics_params['differential_pressure']
        )
        
        # Get wellbore stability predictions
        stability_metrics = self.stability_model.predict_instability_risk(
            mud_weight, pore_pressure, fracture_gradient, tvd,
            formation_strength, hydraulics_params['ecd']
        )
        
        # Combine all parameters
        self.current_state = {
            # Drilling parameters
            'wob': wob,
            'rpm': rpm,
            'flow_rate': flow_rate,
            'mud_weight': mud_weight,
            'tvd': tvd,
            
            # Physics-based outputs
            'rop': mechanics_params['rop'],
            'torque': mechanics_params['torque'],
            'vibration': mechanics_params['vibration'],
            'bit_wear_rate': mechanics_params['bit_wear_rate'],
            'efficiency': mechanics_params['efficiency'],
            'ecd': hydraulics_params['ecd'],
            'pump_pressure': hydraulics_params['pump_pressure'],
            'hydraulic_horsepower': hydraulics_params['hydraulic_horsepower'],
            
            # ML-based risk predictions
            'ml_stuck_pipe_risk': ml_risks.get('stuck_pipe', 0),
            'ml_wellbore_instability_risk': ml_risks.get('wellbore_instability', 0),
            'ml_lost_circulation_risk': ml_risks.get('lost_circulation', 0),
            'ml_kick_risk': ml_risks.get('kick', 0),
            
            # Physics-based risk predictions
            'physics_stuck_pipe_risk': mechanics_params['stuck_pipe_risk'],
            'physics_lost_circulation_risk': hydraulics_params['lost_circulation_risk'],
            'physics_kick_risk': hydraulics_params['kick_risk'],
            
            # Wellbore stability
            'stability_index': stability_metrics['stability_index'],
            'instability_risk': stability_metrics['instability_risk'],
            'collapse_risk': stability_metrics['collapse_risk'],
            'fracture_risk': stability_metrics['fracture_risk'],
            
            # Hybrid risk scores (weighted combination of physics and ML)
            'hybrid_stuck_pipe_risk': self._combine_predictions(
                mechanics_params['stuck_pipe_risk'],
                ml_risks.get('stuck_pipe', 0)
            ),
            'hybrid_lost_circulation_risk': self._combine_predictions(
                hydraulics_params['lost_circulation_risk'],
                ml_risks.get('lost_circulation', 0)
            ),
            'hybrid_kick_risk': self._combine_predictions(
                hydraulics_params['kick_risk'],
                ml_risks.get('kick', 0)
            ),
            'hybrid_instability_risk': self._combine_predictions(
                stability_metrics['instability_risk'],
                ml_risks.get('wellbore_instability', 0)
            )
        }
        
        # Store in history
        self.history.append(self.current_state.copy())
        
        return self.current_state
    
    def _combine_predictions(self, physics_pred: float, ml_pred: float,
                            physics_weight: float = 0.6) -> float:
        """
        Combine physics-based and ML predictions using weighted average.
        
        Args:
            physics_pred: Physics-based prediction (0-1)
            ml_pred: ML prediction (0-1)
            physics_weight: Weight for physics prediction
            
        Returns:
            Combined prediction (0-1)
        """
        ml_weight = 1.0 - physics_weight
        combined = physics_weight * physics_pred + ml_weight * ml_pred
        return min(1.0, max(0.0, combined))
    
    def get_overall_risk_score(self) -> float:
        """
        Calculate overall drilling risk score.
        
        Returns:
            Overall risk score (0-1, higher is worse)
        """
        if not self.current_state:
            return 0.5
        
        # Weight different risks
        weights = {
            'hybrid_stuck_pipe_risk': 0.25,
            'hybrid_lost_circulation_risk': 0.25,
            'hybrid_kick_risk': 0.25,
            'hybrid_instability_risk': 0.25
        }
        
        overall_risk = sum(
            self.current_state.get(risk, 0) * weight
            for risk, weight in weights.items()
        )
        
        return overall_risk
    
    def get_efficiency_score(self) -> float:
        """
        Calculate overall drilling efficiency score.
        
        Returns:
            Efficiency score (0-1, higher is better)
        """
        if not self.current_state:
            return 0.5
        
        # Combine multiple efficiency indicators
        drilling_efficiency = self.current_state.get('efficiency', 0.5)
        rop = self.current_state.get('rop', 10)
        vibration = self.current_state.get('vibration', 0.5)
        bit_wear_rate = self.current_state.get('bit_wear_rate', 0.01)
        
        # Normalize ROP (assume 0-50 m/hr range)
        rop_score = min(1.0, rop / 50)
        
        # Low vibration and wear are good
        vibration_score = 1.0 - vibration
        wear_score = 1.0 - min(1.0, bit_wear_rate * 100)
        
        # Weighted combination
        efficiency = (0.4 * drilling_efficiency +
                     0.3 * rop_score +
                     0.15 * vibration_score +
                     0.15 * wear_score)
        
        return efficiency
    
    def get_sustainability_score(self) -> float:
        """
        Calculate sustainability score based on energy efficiency and resource usage.
        
        Returns:
            Sustainability score (0-1, higher is better)
        """
        if not self.current_state:
            return 0.5
        
        # Energy efficiency (lower hydraulic horsepower per meter drilled is better)
        hhp = self.current_state.get('hydraulic_horsepower', 100)
        rop = self.current_state.get('rop', 10)
        
        energy_efficiency = rop / (hhp + 1e-6)
        energy_score = min(1.0, energy_efficiency / 0.5)  # Normalize
        
        # Mud circulation efficiency (lower ECD margin is more efficient)
        ecd = self.current_state.get('ecd', 1200)
        mud_weight = self.current_state.get('mud_weight', 1200)
        ecd_margin = ecd - mud_weight
        circulation_efficiency = 1.0 - min(1.0, ecd_margin / 200)
        
        # Overall sustainability score
        sustainability = 0.6 * energy_score + 0.4 * circulation_efficiency
        
        return sustainability
    
    def optimize_parameters(self, target_rop: float, max_risk: float = 0.3,
                          constraints: Optional[Dict[str, Tuple[float, float]]] = None
                          ) -> Dict[str, float]:
        """
        Optimize drilling parameters to achieve target ROP while maintaining safety.
        
        Args:
            target_rop: Target Rate of Penetration (m/hr)
            max_risk: Maximum acceptable overall risk (0-1)
            constraints: Parameter constraints {param: (min, max)}
            
        Returns:
            Dictionary of optimized parameters
        """
        if constraints is None:
            constraints = {
                'wob': (40, 140),
                'rpm': (80, 160),
                'flow_rate': (700, 1800),
                'mud_weight': (1100, 1400)
            }
        
        # Get current formation parameters
        current_params = self.current_state.copy() if self.current_state else {}
        formation_strength = current_params.get('formation_strength', 30)
        bit_wear = current_params.get('bit_wear', 0.1)
        
        # Use ROP optimizer to find optimal parameters
        optimal_params = self.rop_optimizer.optimize_parameters(
            target_rop, formation_strength, bit_wear, constraints
        )
        
        # Validate safety constraints
        # Simulate the optimal parameters to check risks
        test_drilling_params = {
            'wob': optimal_params['wob'],
            'rpm': optimal_params['rpm'],
            'flow_rate': optimal_params['flow_rate'],
            'mud_weight': optimal_params['mud_weight'],
            'bit_diameter': current_params.get('bit_diameter', 12.25),
            'pipe_od': current_params.get('pipe_od', 5.0),
            'tvd': current_params.get('tvd', 2000),
            'bit_wear': bit_wear
        }
        
        test_formation_params = {
            'formation_strength': formation_strength,
            'formation_abrasiveness': current_params.get('formation_abrasiveness', 0.5),
            'pore_pressure': current_params.get('pore_pressure', 300),
            'fracture_gradient': current_params.get('fracture_gradient', 1800)
        }
        
        # Temporarily update state to check risk
        original_state = self.current_state.copy()
        self.update_state(test_drilling_params, test_formation_params)
        risk_score = self.get_overall_risk_score()
        
        # Restore original state
        self.current_state = original_state
        
        # If risk is too high, reduce parameters
        if risk_score > max_risk:
            safety_factor = max_risk / risk_score
            optimal_params['wob'] *= safety_factor
            optimal_params['rpm'] *= np.sqrt(safety_factor)
            optimal_params['predicted_rop'] *= safety_factor
            optimal_params['risk_adjusted'] = True
        else:
            optimal_params['risk_adjusted'] = False
        
        optimal_params['estimated_risk'] = risk_score
        
        return optimal_params
    
    def get_recommendations(self, target_rop: Optional[float] = None
                          ) -> Dict[str, any]:
        """
        Get comprehensive recommendations for drilling optimization.
        
        Args:
            target_rop: Optional target ROP (if None, tries to maximize)
            
        Returns:
            Dictionary of recommendations
        """
        if not self.current_state:
            return {'status': 'error', 'message': 'No current state available'}
        
        current_rop = self.current_state.get('rop', 0)
        
        # If no target specified, aim for 20% improvement
        if target_rop is None:
            target_rop = current_rop * 1.2
        
        # Get optimized parameters
        optimized = self.optimize_parameters(target_rop)
        
        # Get current risk and efficiency scores
        risk_score = self.get_overall_risk_score()
        efficiency_score = self.get_efficiency_score()
        sustainability_score = self.get_sustainability_score()
        
        recommendations = {
            'current_state': {
                'rop': current_rop,
                'risk_score': risk_score,
                'efficiency_score': efficiency_score,
                'sustainability_score': sustainability_score
            },
            'optimized_parameters': optimized,
            'scores': {
                'current_risk': risk_score,
                'current_efficiency': efficiency_score,
                'current_sustainability': sustainability_score
            },
            'alerts': self._generate_alerts()
        }
        
        return recommendations
    
    def _generate_alerts(self) -> List[Dict[str, str]]:
        """
        Generate safety and operational alerts based on current state.
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        if not self.current_state:
            return alerts
        
        # Check for high risks
        if self.current_state.get('hybrid_stuck_pipe_risk', 0) > 0.6:
            alerts.append({
                'severity': 'high',
                'type': 'stuck_pipe',
                'message': 'High stuck pipe risk detected. Consider reducing WOB and differential pressure.'
            })
        
        if self.current_state.get('hybrid_kick_risk', 0) > 0.6:
            alerts.append({
                'severity': 'critical',
                'type': 'kick',
                'message': 'High kick risk detected. Increase mud weight immediately.'
            })
        
        if self.current_state.get('hybrid_lost_circulation_risk', 0) > 0.6:
            alerts.append({
                'severity': 'high',
                'type': 'lost_circulation',
                'message': 'High lost circulation risk. Reduce ECD by lowering flow rate or mud weight.'
            })
        
        if self.current_state.get('vibration', 0) > 0.7:
            alerts.append({
                'severity': 'medium',
                'type': 'vibration',
                'message': 'High vibration detected. Adjust RPM away from resonance frequency.'
            })
        
        if self.current_state.get('bit_wear_rate', 0) > 0.05:
            alerts.append({
                'severity': 'medium',
                'type': 'bit_wear',
                'message': 'High bit wear rate. Consider trip for bit change soon.'
            })
        
        # Check for low efficiency
        if self.current_state.get('efficiency', 0.5) < 0.3:
            alerts.append({
                'severity': 'low',
                'type': 'efficiency',
                'message': 'Low drilling efficiency. Optimize WOB and RPM for better performance.'
            })
        
        return alerts
    
    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Get drilling history as a pandas DataFrame.
        
        Returns:
            DataFrame with historical drilling data
        """
        if not self.history:
            return pd.DataFrame()
        
        return pd.DataFrame(self.history)
    
    def reset_history(self):
        """Clear drilling history."""
        self.history = []
