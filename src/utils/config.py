"""
Configuration management for the drilling optimization system.
"""

import yaml
import os
from typing import Dict, Any


class Config:
    """
    Configuration manager for the application.
    """
    
    DEFAULT_CONFIG = {
        'drilling': {
            'default_wob': 80,  # kN
            'default_rpm': 120,  # RPM
            'default_flow_rate': 1000,  # LPM
            'default_mud_weight': 1200,  # kg/m³
            'default_bit_diameter': 12.25,  # inches
            'default_pipe_od': 5.0,  # inches
            'default_tvd': 2000,  # m
            'mud_viscosity': 0.03,  # Pa·s
            'max_wob': 150,  # kN
            'max_rpm': 200,  # RPM
            'max_flow_rate': 2000,  # LPM
        },
        'formation': {
            'default_strength': 30,  # MPa
            'default_abrasiveness': 0.5,  # 0-1
            'default_pore_pressure': 300,  # bar
            'default_fracture_gradient': 1800,  # kg/m³
        },
        'safety': {
            'max_risk_threshold': 0.7,  # 0-1
            'min_efficiency_threshold': 0.3,  # 0-1
            'max_vibration': 0.8,  # 0-1
            'max_bit_wear_rate': 0.08,  # fraction per hour
        },
        'optimization': {
            'target_rop': 20,  # m/hr
            'max_acceptable_risk': 0.3,  # 0-1
            'physics_weight': 0.6,  # Weight for physics-based predictions
            'ml_weight': 0.4,  # Weight for ML predictions
        },
        'ml': {
            'model_directory': 'models/trained',
            'training_test_split': 0.2,
            'random_seed': 42,
        },
        'data': {
            'synthetic_data_dir': 'data/synthetic',
            'real_data_dir': 'data/real',
            'num_training_samples': 1000,
        },
        'dashboard': {
            'title': 'AI-Driven Autonomous Drilling Optimization System',
            'port': 8501,
            'refresh_rate': 5,  # seconds
        }
    }
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to YAML config file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
    
    def load_from_file(self, filepath: str):
        """
        Load configuration from YAML file.
        
        Args:
            filepath: Path to YAML config file
        """
        with open(filepath, 'r') as f:
            user_config = yaml.safe_load(f)
        
        # Deep merge user config with defaults
        self._deep_merge(self.config, user_config)
    
    def save_to_file(self, filepath: str):
        """
        Save current configuration to YAML file.
        
        Args:
            filepath: Path to save YAML config file
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def _deep_merge(self, base: Dict, update: Dict):
        """
        Recursively merge update dict into base dict.
        
        Args:
            base: Base dictionary
            update: Dictionary with updates
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated path.
        
        Args:
            key_path: Dot-separated path (e.g., 'drilling.default_wob')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value by dot-separated path.
        
        Args:
            key_path: Dot-separated path (e.g., 'drilling.default_wob')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_drilling_params(self) -> Dict[str, float]:
        """Get default drilling parameters."""
        return self.config['drilling'].copy()
    
    def get_formation_params(self) -> Dict[str, float]:
        """Get default formation parameters."""
        return self.config['formation'].copy()
    
    def get_safety_thresholds(self) -> Dict[str, float]:
        """Get safety thresholds."""
        return self.config['safety'].copy()
    
    def get_optimization_params(self) -> Dict[str, float]:
        """Get optimization parameters."""
        return self.config['optimization'].copy()
