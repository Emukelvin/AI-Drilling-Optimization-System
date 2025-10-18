"""
Drilling Mechanics Module
Implements first-principles equations for drilling mechanics including ROP, torque, WOB calculations.
"""

import numpy as np
from typing import Dict, Tuple


class DrillingMechanics:
    """
    Physics-based drilling mechanics model using first-principles equations.
    """
    
    def __init__(self):
        """Initialize drilling mechanics model with default parameters."""
        self.g = 9.81  # gravitational constant (m/s^2)
        
    def calculate_rop(self, wob: float, rpm: float, bit_diameter: float, 
                      formation_strength: float, bit_wear: float = 0.0) -> float:
        """
        Calculate Rate of Penetration using Bourgoyne and Young model.
        
        Args:
            wob: Weight on Bit (kN)
            rpm: Rotary Speed (RPM)
            bit_diameter: Bit diameter (inches)
            formation_strength: Formation compressive strength (MPa)
            bit_wear: Bit wear factor (0-1, 0=new, 1=fully worn)
            
        Returns:
            ROP in meters per hour
        """
        # Bourgoyne and Young ROP model (simplified)
        # ROP = a1 * (WOB/D)^a2 * (RPM)^a3 * exp(-a4 * formation_strength) * (1 - bit_wear)
        
        a1 = 2.5  # Model coefficient
        a2 = 0.7  # WOB exponent
        a3 = 0.5  # RPM exponent
        a4 = 0.01  # Formation strength coefficient
        
        # Normalize WOB by bit diameter
        wob_normalized = wob / bit_diameter
        
        # Calculate ROP
        rop = (a1 * 
               np.power(wob_normalized, a2) * 
               np.power(rpm, a3) * 
               np.exp(-a4 * formation_strength) * 
               (1.0 - bit_wear))
        
        return max(0, rop)  # ROP cannot be negative
    
    def calculate_torque(self, wob: float, bit_diameter: float, 
                        friction_coefficient: float = 0.3) -> float:
        """
        Calculate drilling torque.
        
        Args:
            wob: Weight on Bit (kN)
            bit_diameter: Bit diameter (inches)
            friction_coefficient: Bit-rock friction coefficient
            
        Returns:
            Torque in kN-m
        """
        # Convert bit diameter to meters
        bit_diameter_m = bit_diameter * 0.0254
        
        # Torque = friction_coefficient * WOB * (bit_diameter / 2)
        torque = friction_coefficient * wob * (bit_diameter_m / 2)
        
        return torque
    
    def calculate_axial_vibration(self, wob: float, rpm: float, 
                                  bit_aggressiveness: float = 0.5) -> float:
        """
        Calculate axial vibration severity index.
        
        Args:
            wob: Weight on Bit (kN)
            rpm: Rotary Speed (RPM)
            bit_aggressiveness: Bit aggressiveness factor (0-1)
            
        Returns:
            Vibration severity index (0-1, higher is worse)
        """
        # Critical RPM where vibration is maximum
        critical_rpm = 120
        
        # Vibration increases with WOB and proximity to critical RPM
        rpm_factor = np.exp(-0.01 * (rpm - critical_rpm)**2)
        wob_factor = min(1.0, wob / 100)  # Normalize WOB
        
        vibration = bit_aggressiveness * rpm_factor * wob_factor
        
        return min(1.0, max(0.0, vibration))
    
    def calculate_bit_wear_rate(self, wob: float, rpm: float, 
                                formation_abrasiveness: float = 0.5) -> float:
        """
        Calculate bit wear rate.
        
        Args:
            wob: Weight on Bit (kN)
            rpm: Rotary Speed (RPM)
            formation_abrasiveness: Formation abrasiveness factor (0-1)
            
        Returns:
            Bit wear rate (fraction per hour)
        """
        # Wear rate increases with WOB, RPM, and formation abrasiveness
        wear_rate = (0.001 * formation_abrasiveness * 
                     (wob / 100) * (rpm / 100))
        
        return wear_rate
    
    def calculate_drilling_efficiency(self, rop: float, wob: float, 
                                     rpm: float, torque: float) -> float:
        """
        Calculate drilling efficiency score.
        
        Args:
            rop: Rate of Penetration (m/hr)
            wob: Weight on Bit (kN)
            rpm: Rotary Speed (RPM)
            torque: Torque (kN-m)
            
        Returns:
            Efficiency score (0-1, higher is better)
        """
        # Mechanical specific energy (MSE) calculation
        # Lower MSE indicates better efficiency
        if rop <= 0:
            return 0.0
        
        # Convert units for MSE calculation
        rop_m_per_sec = rop / 3600  # m/hr to m/s
        angular_velocity = rpm * 2 * np.pi / 60  # rad/s
        
        # MSE = (WOB + (Torque * angular_velocity) / rop) / Area
        # Simplified efficiency metric
        energy_input = wob + torque * angular_velocity
        efficiency = rop / (energy_input + 1e-6)  # Avoid division by zero
        
        # Normalize to 0-1 range
        efficiency_normalized = min(1.0, efficiency / 10)
        
        return efficiency_normalized
    
    def predict_stuck_pipe_risk(self, wob: float, torque: float, 
                                differential_pressure: float) -> float:
        """
        Predict stuck pipe risk based on drilling parameters.
        
        Args:
            wob: Weight on Bit (kN)
            torque: Torque (kN-m)
            differential_pressure: Differential pressure (bar)
            
        Returns:
            Stuck pipe risk score (0-1, higher is worse)
        """
        # High WOB, high torque, and high differential pressure increase risk
        wob_risk = min(1.0, wob / 150)
        torque_risk = min(1.0, torque / 50)
        pressure_risk = min(1.0, differential_pressure / 100)
        
        # Combined risk (weighted average)
        stuck_risk = (0.3 * wob_risk + 0.3 * torque_risk + 
                     0.4 * pressure_risk)
        
        return stuck_risk
    
    def calculate_all_parameters(self, wob: float, rpm: float, 
                                bit_diameter: float, formation_strength: float,
                                mud_density: float, bit_wear: float = 0.0,
                                formation_abrasiveness: float = 0.5) -> Dict[str, float]:
        """
        Calculate all drilling mechanics parameters at once.
        
        Args:
            wob: Weight on Bit (kN)
            rpm: Rotary Speed (RPM)
            bit_diameter: Bit diameter (inches)
            formation_strength: Formation compressive strength (MPa)
            mud_density: Mud density (kg/m³)
            bit_wear: Bit wear factor (0-1)
            formation_abrasiveness: Formation abrasiveness (0-1)
            
        Returns:
            Dictionary of calculated parameters
        """
        rop = self.calculate_rop(wob, rpm, bit_diameter, formation_strength, bit_wear)
        torque = self.calculate_torque(wob, bit_diameter)
        vibration = self.calculate_axial_vibration(wob, rpm)
        wear_rate = self.calculate_bit_wear_rate(wob, rpm, formation_abrasiveness)
        efficiency = self.calculate_drilling_efficiency(rop, wob, rpm, torque)
        
        # Estimate differential pressure based on mud density
        differential_pressure = mud_density * 0.01  # Simplified
        stuck_risk = self.predict_stuck_pipe_risk(wob, torque, differential_pressure)
        
        return {
            'rop': rop,
            'torque': torque,
            'vibration': vibration,
            'bit_wear_rate': wear_rate,
            'efficiency': efficiency,
            'stuck_pipe_risk': stuck_risk,
            'differential_pressure': differential_pressure
        }
