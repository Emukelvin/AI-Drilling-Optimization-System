"""
Physics-based well model for drilling operations.
Implements fundamental drilling physics equations.
"""
import numpy as np
from src.utils import setup_logger, load_config

logger = setup_logger(__name__)


class PhysicsWellModel:
    """
    Physics-based model for drilling operations.
    Implements fundamental equations for pressure, torque, and hydraulics.
    """
    
    def __init__(self, config=None):
        """
        Initialize physics model with configuration.
        
        Args:
            config (dict, optional): Configuration parameters
        """
        if config is None:
            config = load_config()
        
        self.config = config.get('physics', {})
        self.formation_pressure_gradient = self.config.get('formation_pressure_gradient', 0.465)
        self.fracture_gradient = self.config.get('fracture_gradient', 0.8)
        self.temperature_gradient = self.config.get('temperature_gradient', 0.015)
        
        logger.info("PhysicsWellModel initialized")
    
    def calculate_formation_pressure(self, depth):
        """
        Calculate formation pressure at given depth.
        
        Args:
            depth (float): Depth in feet
            
        Returns:
            float: Formation pressure in psi
        """
        return self.formation_pressure_gradient * depth
    
    def calculate_fracture_pressure(self, depth):
        """
        Calculate fracture pressure at given depth.
        
        Args:
            depth (float): Depth in feet
            
        Returns:
            float: Fracture pressure in psi
        """
        return self.fracture_gradient * depth
    
    def calculate_hydrostatic_pressure(self, depth, mud_weight):
        """
        Calculate hydrostatic pressure.
        
        Args:
            depth (float): Depth in feet
            mud_weight (float): Mud weight in ppg
            
        Returns:
            float: Hydrostatic pressure in psi
        """
        return 0.052 * mud_weight * depth
    
    def calculate_rop(self, wob, rpm, diff_pressure):
        """
        Calculate Rate of Penetration using simplified model.
        
        Args:
            wob (float): Weight on bit (klbs)
            rpm (float): Rotary speed (RPM)
            diff_pressure (float): Differential pressure (psi)
            
        Returns:
            float: Rate of penetration (ft/hr)
        """
        # Simplified ROP model
        k = 0.5  # Formation drillability constant
        rop = k * (wob ** 0.5) * (rpm ** 0.6) * (diff_pressure ** 0.1)
        return max(0, rop)
    
    def calculate_torque(self, wob, rpm, depth):
        """
        Calculate drilling torque.
        
        Args:
            wob (float): Weight on bit (klbs)
            rpm (float): Rotary speed (RPM)
            depth (float): Depth (feet)
            
        Returns:
            float: Torque (klb-ft)
        """
        # Simplified torque model
        bit_torque = 0.5 * wob  # Torque at bit
        friction_torque = 0.001 * depth  # Friction along drillstring
        viscous_torque = 0.01 * rpm  # Viscous drag
        
        total_torque = bit_torque + friction_torque + viscous_torque
        return total_torque
    
    def calculate_hydraulic_horsepower(self, flow_rate, pressure):
        """
        Calculate hydraulic horsepower.
        
        Args:
            flow_rate (float): Flow rate (gpm)
            pressure (float): Pressure (psi)
            
        Returns:
            float: Hydraulic horsepower
        """
        hhp = (flow_rate * pressure) / 1714
        return hhp
    
    def check_wellbore_stability(self, depth, mud_weight):
        """
        Check wellbore stability based on pressure balance.
        
        Args:
            depth (float): Depth (feet)
            mud_weight (float): Mud weight (ppg)
            
        Returns:
            dict: Stability indicators
        """
        formation_pressure = self.calculate_formation_pressure(depth)
        fracture_pressure = self.calculate_fracture_pressure(depth)
        hydrostatic_pressure = self.calculate_hydrostatic_pressure(depth, mud_weight)
        
        # Check if wellbore is stable
        overbalance = hydrostatic_pressure - formation_pressure
        underbalance = fracture_pressure - hydrostatic_pressure
        
        is_stable = (overbalance > 0) and (underbalance > 0)
        
        return {
            'is_stable': is_stable,
            'formation_pressure': formation_pressure,
            'fracture_pressure': fracture_pressure,
            'hydrostatic_pressure': hydrostatic_pressure,
            'overbalance': overbalance,
            'underbalance': underbalance,
            'stability_index': min(overbalance, underbalance) / formation_pressure
        }
    
    def predict_physics_based_risks(self, drilling_params):
        """
        Predict risks based on physics equations.
        
        Args:
            drilling_params (dict): Current drilling parameters
            
        Returns:
            dict: Risk predictions
        """
        depth = drilling_params.get('depth', 0)
        mud_weight = drilling_params.get('mud_weight', 12)
        wob = drilling_params.get('wob', 25)
        torque = drilling_params.get('torque', 15)
        
        # Check wellbore stability
        stability = self.check_wellbore_stability(depth, mud_weight)
        
        # Predict stuck pipe risk based on torque
        expected_torque = self.calculate_torque(wob, drilling_params.get('rpm', 120), depth)
        torque_ratio = torque / expected_torque if expected_torque > 0 else 1.0
        stuck_pipe_risk = min(1.0, max(0, (torque_ratio - 1) * 2))
        
        # Predict kick risk based on pressure balance
        kick_risk = 0.0 if stability['overbalance'] > 200 else min(1.0, 1 - stability['overbalance'] / 200)
        
        return {
            'wellbore_instability': 0.0 if stability['is_stable'] else 1.0 - abs(stability['stability_index']),
            'stuck_pipe': stuck_pipe_risk,
            'kick_risk': kick_risk,
            'stability_details': stability
        }
