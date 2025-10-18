"""
Drilling Hydraulics Module
Implements first-principles equations for drilling hydraulics including ECD, pressure losses, flow rates.
"""

import numpy as np
from typing import Dict, Tuple


class DrillingHydraulics:
    """
    Physics-based drilling hydraulics model using first-principles equations.
    """
    
    def __init__(self):
        """Initialize drilling hydraulics model with default parameters."""
        self.g = 9.81  # gravitational constant (m/s^2)
        
    def calculate_annular_velocity(self, flow_rate: float, hole_diameter: float,
                                   pipe_od: float) -> float:
        """
        Calculate annular velocity.
        
        Args:
            flow_rate: Flow rate (liters per minute)
            hole_diameter: Hole diameter (inches)
            pipe_od: Pipe outer diameter (inches)
            
        Returns:
            Annular velocity (m/s)
        """
        # Convert to SI units
        flow_rate_m3_per_sec = flow_rate / 60000  # LPM to m³/s
        hole_diameter_m = hole_diameter * 0.0254  # inches to meters
        pipe_od_m = pipe_od * 0.0254
        
        # Calculate annular area
        annular_area = np.pi * (hole_diameter_m**2 - pipe_od_m**2) / 4
        
        # Velocity = Flow rate / Area
        velocity = flow_rate_m3_per_sec / annular_area if annular_area > 0 else 0
        
        return velocity
    
    def calculate_reynolds_number(self, velocity: float, diameter: float,
                                  mud_density: float, mud_viscosity: float) -> float:
        """
        Calculate Reynolds number for flow regime determination.
        
        Args:
            velocity: Flow velocity (m/s)
            diameter: Hydraulic diameter (m)
            mud_density: Mud density (kg/m³)
            mud_viscosity: Mud viscosity (Pa·s)
            
        Returns:
            Reynolds number (dimensionless)
        """
        if mud_viscosity <= 0:
            return 0
        
        reynolds = (mud_density * velocity * diameter) / mud_viscosity
        
        return reynolds
    
    def calculate_friction_pressure_loss(self, flow_rate: float, mud_density: float,
                                        mud_viscosity: float, pipe_length: float,
                                        pipe_diameter: float) -> float:
        """
        Calculate friction pressure loss in pipe.
        
        Args:
            flow_rate: Flow rate (LPM)
            mud_density: Mud density (kg/m³)
            mud_viscosity: Mud viscosity (Pa·s)
            pipe_length: Pipe length (m)
            pipe_diameter: Pipe diameter (inches)
            
        Returns:
            Pressure loss (bar)
        """
        # Convert units
        flow_rate_m3_per_sec = flow_rate / 60000
        pipe_diameter_m = pipe_diameter * 0.0254
        
        # Calculate velocity
        pipe_area = np.pi * pipe_diameter_m**2 / 4
        velocity = flow_rate_m3_per_sec / pipe_area if pipe_area > 0 else 0
        
        # Calculate Reynolds number
        re = self.calculate_reynolds_number(velocity, pipe_diameter_m, 
                                           mud_density, mud_viscosity)
        
        # Calculate friction factor (Darcy-Weisbach)
        if re < 2300:  # Laminar flow
            f = 64 / re if re > 0 else 0
        else:  # Turbulent flow (simplified Colebrook)
            f = 0.316 / (re**0.25) if re > 0 else 0
        
        # Pressure loss (Darcy-Weisbach equation)
        pressure_loss_pa = (f * pipe_length * mud_density * velocity**2) / (2 * pipe_diameter_m)
        pressure_loss_bar = pressure_loss_pa / 100000  # Pa to bar
        
        return pressure_loss_bar
    
    def calculate_ecd(self, mud_weight: float, flow_rate: float, 
                     tvd: float, hole_diameter: float, pipe_od: float,
                     mud_viscosity: float = 0.03) -> float:
        """
        Calculate Equivalent Circulating Density (ECD).
        
        Args:
            mud_weight: Static mud weight (kg/m³)
            flow_rate: Flow rate (LPM)
            tvd: True Vertical Depth (m)
            hole_diameter: Hole diameter (inches)
            pipe_od: Pipe outer diameter (inches)
            mud_viscosity: Mud viscosity (Pa·s)
            
        Returns:
            ECD (kg/m³)
        """
        # Calculate annular pressure loss
        annular_length = tvd  # Simplified
        annular_hydraulic_diameter = (hole_diameter - pipe_od) * 0.0254
        
        pressure_loss = self.calculate_friction_pressure_loss(
            flow_rate, mud_weight, mud_viscosity, 
            annular_length, hole_diameter - pipe_od
        )
        
        # Convert pressure loss to equivalent mud weight
        pressure_loss_pa = pressure_loss * 100000  # bar to Pa
        ecd_increase = pressure_loss_pa / (self.g * tvd) if tvd > 0 else 0
        
        ecd = mud_weight + ecd_increase
        
        return ecd
    
    def predict_lost_circulation_risk(self, ecd: float, formation_fracture_gradient: float,
                                     mud_weight: float) -> float:
        """
        Predict lost circulation risk based on ECD and formation pressure.
        
        Args:
            ecd: Equivalent Circulating Density (kg/m³)
            formation_fracture_gradient: Formation fracture gradient (kg/m³)
            mud_weight: Static mud weight (kg/m³)
            
        Returns:
            Lost circulation risk score (0-1, higher is worse)
        """
        # Risk increases as ECD approaches fracture gradient
        if formation_fracture_gradient <= 0:
            return 0
        
        ecd_margin = (formation_fracture_gradient - ecd) / formation_fracture_gradient
        
        # Risk is high when margin is low
        risk = 1.0 - max(0, min(1.0, ecd_margin / 0.2))  # 20% margin is safe
        
        return risk
    
    def predict_kick_risk(self, mud_weight: float, formation_pore_pressure: float) -> float:
        """
        Predict kick risk based on mud weight and pore pressure.
        
        Args:
            mud_weight: Mud weight (kg/m³)
            formation_pore_pressure: Formation pore pressure (bar)
            
        Returns:
            Kick risk score (0-1, higher is worse)
        """
        # Estimate hydrostatic pressure from mud weight
        # Assuming a reference depth of 1000m
        reference_depth = 1000
        hydrostatic_pressure = (mud_weight * self.g * reference_depth) / 100000  # bar
        
        # Risk increases as mud weight approaches pore pressure
        if formation_pore_pressure <= 0:
            return 0
        
        pressure_margin = (hydrostatic_pressure - formation_pore_pressure) / formation_pore_pressure
        
        # Risk is high when margin is low or negative
        risk = 1.0 - max(0, min(1.0, pressure_margin / 0.1))  # 10% margin is safe
        
        return risk
    
    def calculate_pump_pressure(self, flow_rate: float, mud_density: float,
                               mud_viscosity: float, total_system_length: float,
                               average_diameter: float) -> float:
        """
        Calculate required pump pressure.
        
        Args:
            flow_rate: Flow rate (LPM)
            mud_density: Mud density (kg/m³)
            mud_viscosity: Mud viscosity (Pa·s)
            total_system_length: Total system length (m)
            average_diameter: Average system diameter (inches)
            
        Returns:
            Pump pressure (bar)
        """
        # Calculate total friction pressure loss
        pressure_loss = self.calculate_friction_pressure_loss(
            flow_rate, mud_density, mud_viscosity,
            total_system_length, average_diameter
        )
        
        # Add bit pressure drop (simplified as 20% of friction loss)
        bit_pressure_drop = 0.2 * pressure_loss
        
        total_pressure = pressure_loss + bit_pressure_drop
        
        return total_pressure
    
    def calculate_hydraulic_horsepower(self, flow_rate: float, pressure: float) -> float:
        """
        Calculate hydraulic horsepower.
        
        Args:
            flow_rate: Flow rate (LPM)
            pressure: Pressure (bar)
            
        Returns:
            Hydraulic horsepower (HP)
        """
        # Convert units
        flow_rate_m3_per_sec = flow_rate / 60000
        pressure_pa = pressure * 100000
        
        # Power = Flow rate × Pressure
        power_watts = flow_rate_m3_per_sec * pressure_pa
        power_hp = power_watts / 745.7  # Watts to HP
        
        return power_hp
    
    def calculate_all_parameters(self, flow_rate: float, mud_weight: float,
                                mud_viscosity: float, tvd: float,
                                hole_diameter: float, pipe_od: float,
                                formation_fracture_gradient: float,
                                formation_pore_pressure: float) -> Dict[str, float]:
        """
        Calculate all hydraulics parameters at once.
        
        Args:
            flow_rate: Flow rate (LPM)
            mud_weight: Mud weight (kg/m³)
            mud_viscosity: Mud viscosity (Pa·s)
            tvd: True Vertical Depth (m)
            hole_diameter: Hole diameter (inches)
            pipe_od: Pipe outer diameter (inches)
            formation_fracture_gradient: Formation fracture gradient (kg/m³)
            formation_pore_pressure: Formation pore pressure (bar)
            
        Returns:
            Dictionary of calculated parameters
        """
        annular_velocity = self.calculate_annular_velocity(flow_rate, hole_diameter, pipe_od)
        ecd = self.calculate_ecd(mud_weight, flow_rate, tvd, hole_diameter, pipe_od, mud_viscosity)
        lost_circ_risk = self.predict_lost_circulation_risk(ecd, formation_fracture_gradient, mud_weight)
        kick_risk = self.predict_kick_risk(mud_weight, formation_pore_pressure)
        
        # Calculate pump pressure
        total_length = tvd * 2  # Down and up
        avg_diameter = (hole_diameter + pipe_od) / 2
        pump_pressure = self.calculate_pump_pressure(flow_rate, mud_weight, mud_viscosity,
                                                     total_length, avg_diameter)
        
        hhp = self.calculate_hydraulic_horsepower(flow_rate, pump_pressure)
        
        return {
            'annular_velocity': annular_velocity,
            'ecd': ecd,
            'lost_circulation_risk': lost_circ_risk,
            'kick_risk': kick_risk,
            'pump_pressure': pump_pressure,
            'hydraulic_horsepower': hhp
        }
