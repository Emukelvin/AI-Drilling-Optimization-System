"""
Data collection module for drilling operations.
Simulates real-time data collection from drilling sensors.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from src.utils import setup_logger

logger = setup_logger(__name__)


class DrillingDataCollector:
    """
    Collects and manages drilling operation data.
    """
    
    def __init__(self):
        """Initialize the data collector."""
        self.current_depth = 0
        self.start_time = datetime.now()
        logger.info("DrillingDataCollector initialized")
    
    def generate_sample_data(self, num_samples=1000):
        """
        Generate sample drilling data for training and testing.
        
        Args:
            num_samples (int): Number of data samples to generate
            
        Returns:
            pd.DataFrame: Sample drilling data
        """
        logger.info(f"Generating {num_samples} sample data points")
        
        np.random.seed(42)
        
        # Generate synthetic drilling parameters
        depth = np.linspace(0, 10000, num_samples)  # feet
        wob = np.random.normal(25, 5, num_samples)  # klbs (Weight on Bit)
        rpm = np.random.normal(120, 20, num_samples)  # RPM
        flow_rate = np.random.normal(500, 50, num_samples)  # gpm
        spp = np.random.normal(2500, 300, num_samples)  # psi (Standpipe Pressure)
        torque = np.random.normal(15, 3, num_samples)  # klb-ft
        rop = np.random.normal(60, 15, num_samples)  # ft/hr (Rate of Penetration)
        mud_weight = np.random.normal(12, 1, num_samples)  # ppg
        temperature = 70 + depth * 0.015 + np.random.normal(0, 5, num_samples)  # degF
        
        # Generate risk indicators (0 = no risk, 1 = high risk)
        wellbore_instability = ((wob > 30) | (rop > 80)).astype(int) * np.random.rand(num_samples)
        stuck_pipe = ((torque > 18) | (spp > 2800)).astype(int) * np.random.rand(num_samples)
        kick_risk = ((flow_rate < 450) | (spp < 2200)).astype(int) * np.random.rand(num_samples)
        
        # Calculate fuel consumption (simplified model)
        fuel_consumption = (wob * rpm * 0.001 + 5) * np.random.uniform(0.9, 1.1, num_samples)
        
        # Calculate CO2 emissions (kg/hr)
        co2_emissions = fuel_consumption * 2.68  # conversion factor
        
        data = pd.DataFrame({
            'timestamp': [self.start_time + timedelta(minutes=i*5) for i in range(num_samples)],
            'depth': depth,
            'wob': wob,
            'rpm': rpm,
            'flow_rate': flow_rate,
            'spp': spp,
            'torque': torque,
            'rop': rop,
            'mud_weight': mud_weight,
            'temperature': temperature,
            'wellbore_instability': wellbore_instability,
            'stuck_pipe': stuck_pipe,
            'kick_risk': kick_risk,
            'fuel_consumption': fuel_consumption,
            'co2_emissions': co2_emissions
        })
        
        logger.info("Sample data generation complete")
        return data
    
    def collect_realtime_data(self):
        """
        Simulate real-time data collection from drilling sensors.
        
        Returns:
            dict: Current drilling parameters
        """
        self.current_depth += np.random.uniform(0, 2)  # Incremental depth
        
        data = {
            'timestamp': datetime.now(),
            'depth': self.current_depth,
            'wob': np.random.normal(25, 5),
            'rpm': np.random.normal(120, 20),
            'flow_rate': np.random.normal(500, 50),
            'spp': np.random.normal(2500, 300),
            'torque': np.random.normal(15, 3),
            'rop': np.random.normal(60, 15),
            'mud_weight': np.random.normal(12, 1),
            'temperature': 70 + self.current_depth * 0.015 + np.random.normal(0, 5)
        }
        
        return data
    
    def preprocess_data(self, data):
        """
        Preprocess drilling data for model training.
        
        Args:
            data (pd.DataFrame): Raw drilling data
            
        Returns:
            tuple: Processed features and targets
        """
        logger.info("Preprocessing data")
        
        # Select features for ML models
        feature_columns = ['depth', 'wob', 'rpm', 'flow_rate', 'spp', 
                          'torque', 'rop', 'mud_weight', 'temperature']
        
        X = data[feature_columns].values
        
        # Handle any missing values
        X = np.nan_to_num(X, nan=0.0)
        
        # Normalize features
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Extract targets (risk indicators)
        if 'wellbore_instability' in data.columns:
            y_wellbore = data['wellbore_instability'].values
            y_stuck_pipe = data['stuck_pipe'].values
            y_kick = data['kick_risk'].values
            
            logger.info("Data preprocessing complete with targets")
            return X_scaled, (y_wellbore, y_stuck_pipe, y_kick), scaler
        
        logger.info("Data preprocessing complete without targets")
        return X_scaled, None, scaler
