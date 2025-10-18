"""
Risk Prediction ML Model
Predicts drilling risks using ensemble machine learning methods.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
from typing import Dict, List, Tuple, Optional
import os


class RiskPredictor:
    """
    ML-based risk predictor for drilling operations.
    Predicts multiple risk types: stuck pipe, wellbore instability, lost circulation, kicks.
    """
    
    def __init__(self):
        """Initialize the risk predictor with ensemble models."""
        self.models = {
            'stuck_pipe': RandomForestClassifier(n_estimators=100, random_state=42),
            'wellbore_instability': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'lost_circulation': RandomForestClassifier(n_estimators=100, random_state=42),
            'kick': GradientBoostingClassifier(n_estimators=100, random_state=42)
        }
        self.scalers = {
            'stuck_pipe': StandardScaler(),
            'wellbore_instability': StandardScaler(),
            'lost_circulation': StandardScaler(),
            'kick': StandardScaler()
        }
        self.is_trained = {risk_type: False for risk_type in self.models.keys()}
        self.feature_names = [
            'wob', 'rpm', 'flow_rate', 'mud_weight', 'ecd', 'torque',
            'rop', 'tvd', 'formation_strength', 'differential_pressure'
        ]
        
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare and engineer features from raw drilling data.
        
        Args:
            data: DataFrame with drilling parameters
            
        Returns:
            DataFrame with engineered features
        """
        features = data.copy()
        
        # Add derived features
        if 'wob' in features.columns and 'rop' in features.columns:
            features['wob_rop_ratio'] = features['wob'] / (features['rop'] + 1e-6)
        
        if 'ecd' in features.columns and 'mud_weight' in features.columns:
            features['ecd_margin'] = features['ecd'] - features['mud_weight']
        
        if 'torque' in features.columns and 'rpm' in features.columns:
            features['specific_energy'] = features['torque'] * features['rpm']
        
        return features
    
    def train(self, data: pd.DataFrame, risk_labels: Dict[str, np.ndarray],
              test_size: float = 0.2) -> Dict[str, Dict[str, float]]:
        """
        Train all risk prediction models.
        
        Args:
            data: Training data with drilling parameters
            risk_labels: Dictionary mapping risk types to their labels
            test_size: Fraction of data to use for testing
            
        Returns:
            Dictionary of training scores for each model
        """
        # Prepare features
        X = self.prepare_features(data)
        
        # Select only available features
        available_features = [f for f in self.feature_names if f in X.columns]
        X = X[available_features]
        
        results = {}
        
        for risk_type, model in self.models.items():
            if risk_type not in risk_labels:
                continue
                
            y = risk_labels[risk_type]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scalers[risk_type].fit_transform(X_train)
            X_test_scaled = self.scalers[risk_type].transform(X_test)
            
            # Train model
            model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = model.score(X_train_scaled, y_train)
            test_score = model.score(X_test_scaled, y_test)
            
            self.is_trained[risk_type] = True
            
            results[risk_type] = {
                'train_score': train_score,
                'test_score': test_score
            }
            
        return results
    
    def predict_risk(self, data: pd.DataFrame, risk_type: str) -> np.ndarray:
        """
        Predict risk for specific risk type.
        
        Args:
            data: DataFrame with drilling parameters
            risk_type: Type of risk to predict
            
        Returns:
            Array of risk probabilities
        """
        if risk_type not in self.models:
            raise ValueError(f"Unknown risk type: {risk_type}")
        
        if not self.is_trained[risk_type]:
            # Return dummy predictions if model not trained
            return np.random.rand(len(data)) * 0.3  # Low random risk
        
        # Prepare features
        X = self.prepare_features(data)
        available_features = [f for f in self.feature_names if f in X.columns]
        X = X[available_features]
        
        # Scale and predict
        X_scaled = self.scalers[risk_type].transform(X)
        
        # Get probability of positive class (high risk)
        if hasattr(self.models[risk_type], 'predict_proba'):
            predictions = self.models[risk_type].predict_proba(X_scaled)[:, 1]
        else:
            predictions = self.models[risk_type].predict(X_scaled)
        
        return predictions
    
    def predict_all_risks(self, data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """
        Predict all risk types at once.
        
        Args:
            data: DataFrame with drilling parameters
            
        Returns:
            Dictionary mapping risk types to their predictions
        """
        predictions = {}
        
        for risk_type in self.models.keys():
            try:
                predictions[risk_type] = self.predict_risk(data, risk_type)
            except Exception as e:
                # Use fallback if prediction fails
                predictions[risk_type] = np.zeros(len(data))
        
        return predictions
    
    def get_risk_score(self, wob: float, rpm: float, flow_rate: float,
                       mud_weight: float, ecd: float, torque: float,
                       rop: float, tvd: float, formation_strength: float,
                       differential_pressure: float) -> Dict[str, float]:
        """
        Get risk scores for a single set of parameters.
        
        Args:
            wob: Weight on Bit (kN)
            rpm: Rotary Speed (RPM)
            flow_rate: Flow rate (LPM)
            mud_weight: Mud weight (kg/m³)
            ecd: Equivalent Circulating Density (kg/m³)
            torque: Torque (kN-m)
            rop: Rate of Penetration (m/hr)
            tvd: True Vertical Depth (m)
            formation_strength: Formation strength (MPa)
            differential_pressure: Differential pressure (bar)
            
        Returns:
            Dictionary of risk scores (0-1 for each risk type)
        """
        # Create single-row DataFrame
        data = pd.DataFrame([{
            'wob': wob,
            'rpm': rpm,
            'flow_rate': flow_rate,
            'mud_weight': mud_weight,
            'ecd': ecd,
            'torque': torque,
            'rop': rop,
            'tvd': tvd,
            'formation_strength': formation_strength,
            'differential_pressure': differential_pressure
        }])
        
        # Get predictions
        predictions = self.predict_all_risks(data)
        
        # Convert to single values
        risk_scores = {
            risk_type: float(pred[0]) 
            for risk_type, pred in predictions.items()
        }
        
        return risk_scores
    
    def save_models(self, directory: str):
        """
        Save trained models to disk.
        
        Args:
            directory: Directory to save models
        """
        os.makedirs(directory, exist_ok=True)
        
        for risk_type in self.models.keys():
            if self.is_trained[risk_type]:
                model_path = os.path.join(directory, f'{risk_type}_model.joblib')
                scaler_path = os.path.join(directory, f'{risk_type}_scaler.joblib')
                
                joblib.dump(self.models[risk_type], model_path)
                joblib.dump(self.scalers[risk_type], scaler_path)
    
    def load_models(self, directory: str):
        """
        Load trained models from disk.
        
        Args:
            directory: Directory containing saved models
        """
        for risk_type in self.models.keys():
            model_path = os.path.join(directory, f'{risk_type}_model.joblib')
            scaler_path = os.path.join(directory, f'{risk_type}_scaler.joblib')
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.models[risk_type] = joblib.load(model_path)
                self.scalers[risk_type] = joblib.load(scaler_path)
                self.is_trained[risk_type] = True
