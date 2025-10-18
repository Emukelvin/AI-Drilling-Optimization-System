"""
Hybrid Digital Twin combining physics-based and ML models.
"""
import numpy as np
from src.models.physics_model import PhysicsWellModel
from src.models.ml_models import MLRiskPredictor
from src.utils import setup_logger, load_config

logger = setup_logger(__name__)


class HybridDigitalTwin:
    """
    Hybrid Digital Twin combining physics-based and machine learning models.
    """
    
    def __init__(self, config=None):
        """
        Initialize hybrid digital twin.
        
        Args:
            config (dict, optional): Configuration parameters
        """
        if config is None:
            config = load_config()
        
        self.config = config
        self.physics_model = PhysicsWellModel(config)
        self.ml_model = MLRiskPredictor(config)
        
        # Weights for combining physics and ML predictions
        self.physics_weight = 0.3
        self.ml_weight = 0.7
        
        logger.info("HybridDigitalTwin initialized")
    
    def train_ml_component(self, X_train, y_targets, scaler):
        """
        Train the ML component of the hybrid model.
        
        Args:
            X_train (np.ndarray): Training features
            y_targets (tuple): Target values
            scaler: Feature scaler
        """
        logger.info("Training ML component of hybrid digital twin")
        self.ml_model.train(X_train, y_targets, scaler)
    
    def predict_risks(self, drilling_params, use_ml=True):
        """
        Predict drilling risks using hybrid model.
        
        Args:
            drilling_params (dict or np.ndarray): Current drilling parameters
            use_ml (bool): Whether to use ML model (requires trained model)
            
        Returns:
            dict: Combined risk predictions
        """
        # Get physics-based predictions
        if isinstance(drilling_params, dict):
            physics_risks = self.physics_model.predict_physics_based_risks(drilling_params)
        else:
            # For array input, create a dummy dict with default values
            physics_risks = {
                'wellbore_instability': 0.0,
                'stuck_pipe': 0.0,
                'kick_risk': 0.0
            }
        
        # Get ML predictions if available
        if use_ml and self.ml_model.models['wellbore_instability'] is not None:
            if isinstance(drilling_params, np.ndarray):
                X = drilling_params
            else:
                # Convert dict to array
                X = np.array([[
                    drilling_params.get('depth', 0),
                    drilling_params.get('wob', 25),
                    drilling_params.get('rpm', 120),
                    drilling_params.get('flow_rate', 500),
                    drilling_params.get('spp', 2500),
                    drilling_params.get('torque', 15),
                    drilling_params.get('rop', 60),
                    drilling_params.get('mud_weight', 12),
                    drilling_params.get('temperature', 100)
                ]])
            
            ml_risks = self.ml_model.predict(X)
            
            # Combine physics and ML predictions
            combined_risks = {
                'wellbore_instability': (
                    self.physics_weight * physics_risks['wellbore_instability'] +
                    self.ml_weight * ml_risks['wellbore_instability'][0]
                ),
                'stuck_pipe': (
                    self.physics_weight * physics_risks['stuck_pipe'] +
                    self.ml_weight * ml_risks['stuck_pipe'][0]
                ),
                'kick_risk': (
                    self.physics_weight * physics_risks['kick_risk'] +
                    self.ml_weight * ml_risks['kick_risk'][0]
                )
            }
        else:
            # Use only physics predictions
            combined_risks = physics_risks
        
        return combined_risks
    
    def get_recommendations(self, risks, drilling_params):
        """
        Generate recommendations based on risk predictions.
        
        Args:
            risks (dict): Risk predictions
            drilling_params (dict): Current drilling parameters
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        risk_thresholds = self.config.get('risk_thresholds', {})
        wellbore_threshold = risk_thresholds.get('wellbore_instability', 0.7)
        stuck_pipe_threshold = risk_thresholds.get('stuck_pipe', 0.6)
        kick_threshold = risk_thresholds.get('kick_risk', 0.8)
        
        # Wellbore instability recommendations
        if risks['wellbore_instability'] > wellbore_threshold:
            recommendations.append({
                'risk_type': 'Wellbore Instability',
                'severity': 'HIGH',
                'action': 'Increase mud weight by 0.5-1.0 ppg',
                'priority': 1
            })
            recommendations.append({
                'risk_type': 'Wellbore Instability',
                'severity': 'HIGH',
                'action': 'Reduce weight on bit (WOB) by 10-15%',
                'priority': 1
            })
        
        # Stuck pipe recommendations
        if risks['stuck_pipe'] > stuck_pipe_threshold:
            recommendations.append({
                'risk_type': 'Stuck Pipe',
                'severity': 'HIGH',
                'action': 'Increase circulation rate by 10-15%',
                'priority': 1
            })
            recommendations.append({
                'risk_type': 'Stuck Pipe',
                'severity': 'HIGH',
                'action': 'Reduce rotary speed (RPM) by 10%',
                'priority': 2
            })
        
        # Kick risk recommendations
        if risks['kick_risk'] > kick_threshold:
            recommendations.append({
                'risk_type': 'Kick Risk',
                'severity': 'CRITICAL',
                'action': 'Increase mud weight immediately',
                'priority': 1
            })
            recommendations.append({
                'risk_type': 'Kick Risk',
                'severity': 'CRITICAL',
                'action': 'Monitor flow rate and standpipe pressure closely',
                'priority': 1
            })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'])
        
        return recommendations
    
    def save_models(self, save_dir):
        """
        Save models to disk.
        
        Args:
            save_dir (str): Directory to save models
        """
        self.ml_model.save_models(save_dir)
    
    def load_models(self, load_dir):
        """
        Load models from disk.
        
        Args:
            load_dir (str): Directory containing saved models
        """
        self.ml_model.load_models(load_dir)
