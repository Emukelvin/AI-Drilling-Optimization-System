"""
Wellbore Stability ML Model
Predicts wellbore stability issues using advanced ML techniques.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from typing import Dict, Tuple, Optional


class WellboreStabilityModel:
    """
    ML model for predicting wellbore stability based on stress, pore pressure, and mud weight.
    """
    
    def __init__(self):
        """Initialize wellbore stability model."""
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def calculate_stability_index(self, mud_weight: float, pore_pressure: float,
                                  fracture_gradient: float, tvd: float,
                                  formation_strength: float) -> float:
        """
        Calculate wellbore stability index using physics-based approach.
        
        Args:
            mud_weight: Mud weight (kg/m³)
            pore_pressure: Pore pressure (bar)
            fracture_gradient: Fracture gradient (kg/m³)
            tvd: True Vertical Depth (m)
            formation_strength: Formation strength (MPa)
            
        Returns:
            Stability index (0-1, higher is more stable)
        """
        # Calculate hydrostatic pressure
        g = 9.81
        hydrostatic_pressure = (mud_weight * g * tvd) / 100000  # bar
        
        # Calculate pressure window
        pressure_window = (fracture_gradient * g * tvd) / 100000 - pore_pressure
        
        if pressure_window <= 0:
            return 0.0
        
        # Calculate position within window
        pressure_margin_low = hydrostatic_pressure - pore_pressure
        pressure_margin_high = (fracture_gradient * g * tvd) / 100000 - hydrostatic_pressure
        
        # Stability is best when in middle of window
        if pressure_margin_low <= 0 or pressure_margin_high <= 0:
            stability = 0.0
        else:
            # Normalized stability (0-1)
            min_margin = min(pressure_margin_low, pressure_margin_high)
            stability = min(1.0, min_margin / (pressure_window / 4))
        
        # Factor in formation strength
        strength_factor = min(1.0, formation_strength / 50)  # Normalize
        
        combined_stability = 0.7 * stability + 0.3 * strength_factor
        
        return combined_stability
    
    def predict_collapse_pressure(self, formation_strength: float, 
                                  pore_pressure: float, tvd: float) -> float:
        """
        Predict wellbore collapse pressure.
        
        Args:
            formation_strength: Formation compressive strength (MPa)
            pore_pressure: Pore pressure (bar)
            tvd: True Vertical Depth (m)
            
        Returns:
            Collapse pressure (bar)
        """
        # Simplified Mohr-Coulomb criterion
        # Collapse pressure increases with depth and pore pressure
        depth_factor = tvd / 1000  # Normalize depth
        strength_factor = formation_strength / 10
        
        collapse_pressure = pore_pressure * (1 - 0.1 * strength_factor) * (1 + 0.05 * depth_factor)
        
        return max(pore_pressure * 0.9, collapse_pressure)
    
    def predict_instability_risk(self, mud_weight: float, pore_pressure: float,
                                fracture_gradient: float, tvd: float,
                                formation_strength: float, ecd: float) -> Dict[str, float]:
        """
        Predict various wellbore instability risks.
        
        Args:
            mud_weight: Mud weight (kg/m³)
            pore_pressure: Pore pressure (bar)
            fracture_gradient: Fracture gradient (kg/m³)
            tvd: True Vertical Depth (m)
            formation_strength: Formation strength (MPa)
            ecd: Equivalent Circulating Density (kg/m³)
            
        Returns:
            Dictionary of instability risk metrics
        """
        # Calculate stability index
        stability_index = self.calculate_stability_index(
            mud_weight, pore_pressure, fracture_gradient, tvd, formation_strength
        )
        
        # Calculate collapse pressure
        collapse_pressure = self.predict_collapse_pressure(
            formation_strength, pore_pressure, tvd
        )
        
        # Calculate hydrostatic and ECD pressures
        g = 9.81
        hydrostatic_pressure = (mud_weight * g * tvd) / 100000
        ecd_pressure = (ecd * g * tvd) / 100000
        fracture_pressure = (fracture_gradient * g * tvd) / 100000
        
        # Collapse risk (mud weight too low)
        collapse_risk = max(0, 1 - (hydrostatic_pressure - collapse_pressure) / (pore_pressure * 0.1))
        collapse_risk = min(1.0, collapse_risk)
        
        # Fracture risk (ECD too high)
        fracture_risk = max(0, (ecd_pressure - fracture_pressure) / (fracture_pressure * 0.1))
        fracture_risk = min(1.0, fracture_risk)
        
        # Overall instability risk
        instability_risk = 1.0 - stability_index
        
        return {
            'stability_index': stability_index,
            'instability_risk': instability_risk,
            'collapse_risk': collapse_risk,
            'fracture_risk': fracture_risk,
            'collapse_pressure': collapse_pressure
        }
    
    def train(self, X_train: pd.DataFrame, y_train: np.ndarray) -> float:
        """
        Train the wellbore stability model.
        
        Args:
            X_train: Training features
            y_train: Training labels (stability scores)
            
        Returns:
            Training score
        """
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.is_trained = True
        
        return self.model.score(X_scaled, y_train)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict wellbore stability.
        
        Args:
            X: Input features
            
        Returns:
            Predicted stability scores
        """
        if not self.is_trained:
            # Use physics-based calculation as fallback
            results = []
            for _, row in X.iterrows():
                stability = self.calculate_stability_index(
                    row.get('mud_weight', 1200),
                    row.get('pore_pressure', 300),
                    row.get('fracture_gradient', 1800),
                    row.get('tvd', 2000),
                    row.get('formation_strength', 30)
                )
                results.append(stability)
            return np.array(results)
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
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
