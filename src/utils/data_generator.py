"""
Drilling Data Generator
Generates synthetic drilling data for training and testing.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
import os


class DrillingDataGenerator:
    """
    Generates synthetic drilling data with realistic parameter correlations.
    """
    
    def __init__(self, random_seed: int = 42):
        """
        Initialize data generator.
        
        Args:
            random_seed: Random seed for reproducibility
        """
        np.random.seed(random_seed)
        
    def generate_well_trajectory(self, total_depth: float, 
                                 num_points: int = 100) -> pd.DataFrame:
        """
        Generate a synthetic well trajectory.
        
        Args:
            total_depth: Total depth of well (m)
            num_points: Number of trajectory points
            
        Returns:
            DataFrame with depth, inclination, and azimuth
        """
        depths = np.linspace(0, total_depth, num_points)
        
        # Generate realistic inclination (0-45 degrees)
        # Starts vertical, may build angle in middle section
        inclination = np.zeros(num_points)
        build_start = int(num_points * 0.3)
        build_end = int(num_points * 0.7)
        
        if build_end > build_start:
            max_inclination = np.random.uniform(0, 45)
            build_section = np.linspace(0, max_inclination, build_end - build_start)
            inclination[build_start:build_end] = build_section
            inclination[build_end:] = max_inclination
        
        # Generate azimuth (compass direction)
        azimuth = np.random.uniform(0, 360, num_points)
        
        trajectory = pd.DataFrame({
            'depth': depths,
            'tvd': depths * np.cos(np.radians(inclination)),  # True vertical depth
            'inclination': inclination,
            'azimuth': azimuth
        })
        
        return trajectory
    
    def generate_formation_data(self, trajectory: pd.DataFrame) -> pd.DataFrame:
        """
        Generate formation properties along the well trajectory.
        
        Args:
            trajectory: Well trajectory DataFrame
            
        Returns:
            DataFrame with formation properties
        """
        num_points = len(trajectory)
        
        # Formation strength increases with depth (with variability)
        base_strength = 20 + trajectory['tvd'] * 0.01
        formation_strength = base_strength + np.random.normal(0, 5, num_points)
        formation_strength = np.clip(formation_strength, 10, 100)
        
        # Pore pressure increases with depth
        pore_pressure = 100 + trajectory['tvd'] * 0.1  # bar
        pore_pressure += np.random.normal(0, 20, num_points)
        pore_pressure = np.clip(pore_pressure, 50, 800)
        
        # Fracture gradient
        fracture_gradient = 1500 + trajectory['tvd'] * 0.15  # kg/m³
        fracture_gradient += np.random.normal(0, 50, num_points)
        fracture_gradient = np.clip(fracture_gradient, 1400, 2200)
        
        # Formation type (0=shale, 1=sandstone, 2=limestone)
        formation_type = np.random.choice([0, 1, 2], num_points)
        
        # Abrasiveness (0-1)
        abrasiveness = np.random.uniform(0.3, 0.8, num_points)
        
        formation_data = trajectory.copy()
        formation_data['formation_strength'] = formation_strength
        formation_data['pore_pressure'] = pore_pressure
        formation_data['fracture_gradient'] = fracture_gradient
        formation_data['formation_type'] = formation_type
        formation_data['abrasiveness'] = abrasiveness
        
        return formation_data
    
    def generate_drilling_parameters(self, num_samples: int,
                                    add_noise: bool = True) -> pd.DataFrame:
        """
        Generate synthetic drilling parameters.
        
        Args:
            num_samples: Number of samples to generate
            add_noise: Whether to add realistic noise to parameters
            
        Returns:
            DataFrame with drilling parameters
        """
        # Generate base parameters
        wob = np.random.uniform(40, 140, num_samples)
        rpm = np.random.uniform(60, 180, num_samples)
        flow_rate = np.random.uniform(600, 1800, num_samples)
        mud_weight = np.random.uniform(1000, 1500, num_samples)
        bit_diameter = np.random.choice([8.5, 12.25, 17.5], num_samples)
        pipe_od = bit_diameter * 0.4  # Approximate ratio
        
        if add_noise:
            # Add correlated noise
            wob += np.random.normal(0, 5, num_samples)
            rpm += np.random.normal(0, 5, num_samples)
            flow_rate += np.random.normal(0, 50, num_samples)
            mud_weight += np.random.normal(0, 20, num_samples)
        
        # Clip to realistic ranges
        wob = np.clip(wob, 20, 150)
        rpm = np.clip(rpm, 50, 200)
        flow_rate = np.clip(flow_rate, 500, 2000)
        mud_weight = np.clip(mud_weight, 900, 1600)
        
        drilling_params = pd.DataFrame({
            'wob': wob,
            'rpm': rpm,
            'flow_rate': flow_rate,
            'mud_weight': mud_weight,
            'bit_diameter': bit_diameter,
            'pipe_od': pipe_od
        })
        
        return drilling_params
    
    def generate_complete_dataset(self, num_samples: int = 1000,
                                 well_depth: float = 3000) -> pd.DataFrame:
        """
        Generate a complete synthetic drilling dataset with correlations.
        
        Args:
            num_samples: Number of data samples
            well_depth: Total well depth (m)
            
        Returns:
            Complete DataFrame with all parameters
        """
        # Generate well trajectory and formation data
        trajectory = self.generate_well_trajectory(well_depth, num_samples)
        formation_data = self.generate_formation_data(trajectory)
        
        # Generate drilling parameters
        drilling_params = self.generate_drilling_parameters(num_samples)
        
        # Combine all data
        complete_data = pd.concat([formation_data, drilling_params], axis=1)
        
        # Add time index
        complete_data['time'] = pd.date_range(
            start='2024-01-01', periods=num_samples, freq='h'
        )
        
        # Calculate bit wear (increases over time)
        complete_data['bit_wear'] = np.linspace(0, 0.5, num_samples)
        complete_data['bit_wear'] += np.random.uniform(-0.05, 0.05, num_samples)
        complete_data['bit_wear'] = np.clip(complete_data['bit_wear'], 0, 1)
        
        return complete_data
    
    def generate_risk_labels(self, data: pd.DataFrame) -> Dict[str, np.ndarray]:
        """
        Generate synthetic risk labels based on drilling parameters.
        
        Args:
            data: Drilling data DataFrame
            
        Returns:
            Dictionary of risk labels for each risk type
        """
        num_samples = len(data)
        
        # Stuck pipe risk: high WOB + low flow rate
        stuck_pipe_score = (
            (data['wob'] / 150) * 0.5 +
            (1 - data['flow_rate'] / 2000) * 0.3 +
            np.random.uniform(0, 0.2, num_samples)
        )
        stuck_pipe_labels = (stuck_pipe_score > 0.6).astype(int)
        
        # Wellbore instability: high/low mud weight extremes
        mud_optimal = 1200
        mud_deviation = np.abs(data['mud_weight'] - mud_optimal) / mud_optimal
        instability_score = mud_deviation * 2 + np.random.uniform(0, 0.2, num_samples)
        instability_labels = (instability_score > 0.4).astype(int)
        
        # Lost circulation: high flow rate + high mud weight
        lost_circ_score = (
            (data['flow_rate'] / 2000) * 0.5 +
            (data['mud_weight'] / 1600) * 0.5 +
            np.random.uniform(0, 0.2, num_samples)
        )
        lost_circ_labels = (lost_circ_score > 0.7).astype(int)
        
        # Kick risk: low mud weight
        kick_score = (1 - data['mud_weight'] / 1600) + np.random.uniform(0, 0.2, num_samples)
        kick_labels = (kick_score > 0.6).astype(int)
        
        return {
            'stuck_pipe': stuck_pipe_labels,
            'wellbore_instability': instability_labels,
            'lost_circulation': lost_circ_labels,
            'kick': kick_labels
        }
    
    def save_dataset(self, data: pd.DataFrame, filepath: str):
        """
        Save dataset to CSV file.
        
        Args:
            data: DataFrame to save
            filepath: Path to save file
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
    
    def load_dataset(self, filepath: str) -> pd.DataFrame:
        """
        Load dataset from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            Loaded DataFrame
        """
        return pd.read_csv(filepath)
    
    def generate_case_study_data(self, scenario: str = 'normal') -> pd.DataFrame:
        """
        Generate specific case study scenarios for validation.
        
        Args:
            scenario: Scenario type ('normal', 'high_risk', 'optimal')
            
        Returns:
            Case study DataFrame
        """
        num_samples = 200
        
        if scenario == 'normal':
            # Standard drilling conditions
            data = self.generate_complete_dataset(num_samples, 2500)
            
        elif scenario == 'high_risk':
            # Challenging drilling conditions
            data = self.generate_complete_dataset(num_samples, 3500)
            # Increase formation strength and pressure
            data['formation_strength'] *= 1.5
            data['pore_pressure'] *= 1.3
            
        elif scenario == 'optimal':
            # Ideal drilling conditions
            data = self.generate_complete_dataset(num_samples, 2000)
            # Reduce formation complexity
            data['formation_strength'] *= 0.8
            data['abrasiveness'] *= 0.6
            
        else:
            raise ValueError(f"Unknown scenario: {scenario}")
        
        return data
