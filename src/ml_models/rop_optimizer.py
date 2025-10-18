"""
ROP Optimizer ML Model
Uses ML to optimize Rate of Penetration based on historical data and real-time conditions.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Dict, Tuple, Optional, List


class ROPOptimizer:
    """
    ML-based ROP optimizer that learns optimal drilling parameters from historical data.
    """
    
    def __init__(self):
        """Initialize ROP optimizer model."""
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = ['wob', 'rpm', 'flow_rate', 'mud_weight', 
                             'formation_strength', 'bit_wear']
        
    def train(self, X_train: pd.DataFrame, y_train: np.ndarray) -> float:
        """
        Train the ROP optimization model.
        
        Args:
            X_train: Training features (drilling parameters)
            y_train: Training labels (achieved ROP values)
            
        Returns:
            Training score (R²)
        """
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.is_trained = True
        
        return self.model.score(X_scaled, y_train)
    
    def predict_rop(self, wob: float, rpm: float, flow_rate: float,
                   mud_weight: float, formation_strength: float,
                   bit_wear: float = 0.0) -> float:
        """
        Predict ROP for given drilling parameters.
        
        Args:
            wob: Weight on Bit (kN)
            rpm: Rotary Speed (RPM)
            flow_rate: Flow rate (LPM)
            mud_weight: Mud weight (kg/m³)
            formation_strength: Formation strength (MPa)
            bit_wear: Bit wear factor (0-1)
            
        Returns:
            Predicted ROP (m/hr)
        """
        if not self.is_trained:
            # Use simple physics-based estimate as fallback
            rop = (2.5 * np.power(wob / 12.25, 0.7) * np.power(rpm, 0.5) * 
                   np.exp(-0.01 * formation_strength) * (1.0 - bit_wear))
            return max(0, rop)
        
        # Create feature DataFrame
        X = pd.DataFrame([{
            'wob': wob,
            'rpm': rpm,
            'flow_rate': flow_rate,
            'mud_weight': mud_weight,
            'formation_strength': formation_strength,
            'bit_wear': bit_wear
        }])
        
        X_scaled = self.scaler.transform(X)
        predicted_rop = self.model.predict(X_scaled)[0]
        
        return max(0, predicted_rop)
    
    def optimize_parameters(self, target_rop: float, formation_strength: float,
                           bit_wear: float, constraints: Dict[str, Tuple[float, float]],
                           num_samples: int = 1000) -> Dict[str, float]:
        """
        Find optimal drilling parameters to achieve target ROP within constraints.
        
        Args:
            target_rop: Target Rate of Penetration (m/hr)
            formation_strength: Formation strength (MPa)
            bit_wear: Current bit wear (0-1)
            constraints: Dict of parameter constraints {param: (min, max)}
            num_samples: Number of parameter combinations to try
            
        Returns:
            Dictionary of optimal parameters
        """
        # Default constraints
        default_constraints = {
            'wob': (20, 150),
            'rpm': (60, 180),
            'flow_rate': (500, 2000),
            'mud_weight': (1000, 1500)
        }
        default_constraints.update(constraints)
        
        # Generate random parameter combinations
        wob_samples = np.random.uniform(
            default_constraints['wob'][0],
            default_constraints['wob'][1],
            num_samples
        )
        rpm_samples = np.random.uniform(
            default_constraints['rpm'][0],
            default_constraints['rpm'][1],
            num_samples
        )
        flow_rate_samples = np.random.uniform(
            default_constraints['flow_rate'][0],
            default_constraints['flow_rate'][1],
            num_samples
        )
        mud_weight_samples = np.random.uniform(
            default_constraints['mud_weight'][0],
            default_constraints['mud_weight'][1],
            num_samples
        )
        
        # Predict ROP for all combinations
        best_params = None
        best_score = float('inf')
        
        for i in range(num_samples):
            predicted_rop = self.predict_rop(
                wob_samples[i],
                rpm_samples[i],
                flow_rate_samples[i],
                mud_weight_samples[i],
                formation_strength,
                bit_wear
            )
            
            # Score based on distance to target and efficiency
            rop_diff = abs(predicted_rop - target_rop)
            
            # Penalize high WOB and RPM (wear and vibration)
            efficiency_penalty = (wob_samples[i] / 150) * 0.1 + (rpm_samples[i] / 180) * 0.1
            
            score = rop_diff + efficiency_penalty * target_rop
            
            if score < best_score:
                best_score = score
                best_params = {
                    'wob': wob_samples[i],
                    'rpm': rpm_samples[i],
                    'flow_rate': flow_rate_samples[i],
                    'mud_weight': mud_weight_samples[i],
                    'predicted_rop': predicted_rop
                }
        
        return best_params
    
    def recommend_adjustments(self, current_rop: float, target_rop: float,
                            current_params: Dict[str, float],
                            formation_strength: float) -> Dict[str, Dict[str, float]]:
        """
        Recommend parameter adjustments to reach target ROP.
        
        Args:
            current_rop: Current ROP (m/hr)
            target_rop: Target ROP (m/hr)
            current_params: Current drilling parameters
            formation_strength: Formation strength (MPa)
            
        Returns:
            Dictionary of recommended adjustments with rationale
        """
        recommendations = {}
        
        rop_gap = target_rop - current_rop
        
        if abs(rop_gap) < 0.5:  # Within tolerance
            return {'status': 'optimal', 'message': 'Parameters are near optimal'}
        
        # Test individual parameter adjustments
        params_to_test = ['wob', 'rpm', 'flow_rate']
        
        for param in params_to_test:
            if param not in current_params:
                continue
            
            # Try increasing parameter
            test_params = current_params.copy()
            adjustment = current_params[param] * 0.1  # 10% increase
            test_params[param] = current_params[param] + adjustment
            
            predicted_rop_up = self.predict_rop(
                test_params.get('wob', 80),
                test_params.get('rpm', 120),
                test_params.get('flow_rate', 1000),
                test_params.get('mud_weight', 1200),
                formation_strength,
                test_params.get('bit_wear', 0.0)
            )
            
            # Try decreasing parameter
            test_params[param] = current_params[param] - adjustment
            predicted_rop_down = self.predict_rop(
                test_params.get('wob', 80),
                test_params.get('rpm', 120),
                test_params.get('flow_rate', 1000),
                test_params.get('mud_weight', 1200),
                formation_strength,
                test_params.get('bit_wear', 0.0)
            )
            
            # Determine best direction
            rop_improvement_up = abs(predicted_rop_up - target_rop) - abs(current_rop - target_rop)
            rop_improvement_down = abs(predicted_rop_down - target_rop) - abs(current_rop - target_rop)
            
            if rop_improvement_up < rop_improvement_down and rop_improvement_up < 0:
                recommendations[param] = {
                    'current': current_params[param],
                    'recommended': current_params[param] + adjustment,
                    'change': adjustment,
                    'expected_rop_improvement': -rop_improvement_up
                }
            elif rop_improvement_down < 0:
                recommendations[param] = {
                    'current': current_params[param],
                    'recommended': current_params[param] - adjustment,
                    'change': -adjustment,
                    'expected_rop_improvement': -rop_improvement_down
                }
        
        return recommendations
    
    def save_model(self, filepath: str):
        """Save model to disk."""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }, filepath)
    
    def load_model(self, filepath: str):
        """Load model from disk."""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.is_trained = data['is_trained']
