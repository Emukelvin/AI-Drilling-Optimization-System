"""
Autonomous optimization engine for real-time drilling parameter adjustments.
"""
import numpy as np
from src.utils import setup_logger, load_config

logger = setup_logger(__name__)


class AutonomousOptimizer:
    """
    Autonomous optimization engine for drilling operations.
    """
    
    def __init__(self, config=None):
        """
        Initialize autonomous optimizer.
        
        Args:
            config (dict, optional): Configuration parameters
        """
        if config is None:
            config = load_config()
        
        self.config = config.get('optimization', {})
        self.max_wob_adjustment = self.config.get('max_wob_adjustment', 10)
        self.max_rpm_adjustment = self.config.get('max_rpm_adjustment', 15)
        self.max_flow_rate_adjustment = self.config.get('max_flow_rate_adjustment', 8)
        
        logger.info("AutonomousOptimizer initialized")
    
    def optimize_parameters(self, current_params, risks, recommendations):
        """
        Calculate optimized drilling parameters based on risks and recommendations.
        
        Args:
            current_params (dict): Current drilling parameters
            risks (dict): Risk predictions
            recommendations (list): Recommended actions
            
        Returns:
            dict: Optimized drilling parameters
        """
        logger.info("Calculating optimized parameters")
        
        optimized = current_params.copy()
        adjustments = []
        
        # Initialize adjustment factors
        wob_factor = 1.0
        rpm_factor = 1.0
        flow_rate_factor = 1.0
        mud_weight_adjustment = 0.0
        
        # Analyze risks and adjust parameters
        if risks['wellbore_instability'] > 0.7:
            # Reduce WOB to minimize wellbore damage
            wob_factor *= 0.90
            adjustments.append("Reduced WOB by 10% due to wellbore instability")
            
            # Increase mud weight
            mud_weight_adjustment += 0.5
            adjustments.append("Increased mud weight by 0.5 ppg")
        
        if risks['stuck_pipe'] > 0.6:
            # Increase flow rate to improve cuttings removal
            flow_rate_factor *= 1.05
            adjustments.append("Increased flow rate by 5% to reduce stuck pipe risk")
            
            # Reduce RPM
            rpm_factor *= 0.90
            adjustments.append("Reduced RPM by 10%")
        
        if risks['kick_risk'] > 0.8:
            # Critical: increase mud weight immediately
            mud_weight_adjustment += 1.0
            adjustments.append("CRITICAL: Increased mud weight by 1.0 ppg due to kick risk")
            
            # Reduce WOB
            wob_factor *= 0.85
            adjustments.append("Reduced WOB by 15%")
        
        # Apply bounded adjustments
        optimized['wob'] = self._apply_bounded_adjustment(
            current_params['wob'],
            wob_factor,
            self.max_wob_adjustment
        )
        
        optimized['rpm'] = self._apply_bounded_adjustment(
            current_params['rpm'],
            rpm_factor,
            self.max_rpm_adjustment
        )
        
        optimized['flow_rate'] = self._apply_bounded_adjustment(
            current_params['flow_rate'],
            flow_rate_factor,
            self.max_flow_rate_adjustment
        )
        
        # Adjust mud weight (with safety limits)
        optimized['mud_weight'] = min(16.0, max(8.5,
            current_params.get('mud_weight', 12) + mud_weight_adjustment
        ))
        
        return optimized, adjustments
    
    def _apply_bounded_adjustment(self, current_value, factor, max_adjustment_percent):
        """
        Apply bounded adjustment to a parameter.
        
        Args:
            current_value (float): Current parameter value
            factor (float): Adjustment factor
            max_adjustment_percent (float): Maximum adjustment percentage
            
        Returns:
            float: Adjusted value
        """
        new_value = current_value * factor
        max_change = current_value * (max_adjustment_percent / 100)
        
        # Limit the change
        if new_value > current_value:
            new_value = min(new_value, current_value + max_change)
        else:
            new_value = max(new_value, current_value - max_change)
        
        return new_value
    
    def calculate_efficiency_score(self, params, risks):
        """
        Calculate drilling efficiency score.
        
        Args:
            params (dict): Drilling parameters
            risks (dict): Risk predictions
            
        Returns:
            float: Efficiency score (0-100)
        """
        # Base efficiency on ROP
        rop_score = min(100, params.get('rop', 0) / 100 * 100)
        
        # Penalize for high risks
        risk_penalty = (
            risks['wellbore_instability'] * 20 +
            risks['stuck_pipe'] * 25 +
            risks['kick_risk'] * 30
        )
        
        efficiency = max(0, rop_score - risk_penalty)
        
        return efficiency
    
    def optimize_for_sustainability(self, params):
        """
        Optimize parameters for reduced environmental impact.
        
        Args:
            params (dict): Current drilling parameters
            
        Returns:
            dict: Sustainability-optimized parameters and metrics
        """
        logger.info("Optimizing for sustainability")
        
        optimized = params.copy()
        
        # Calculate current fuel consumption (simplified model)
        current_fuel = params.get('wob', 25) * params.get('rpm', 120) * 0.001 + 5
        
        # Optimize WOB and RPM for better fuel efficiency
        # Reduce WOB slightly, increase RPM slightly (more efficient drilling)
        optimized['wob'] = params.get('wob', 25) * 0.95
        optimized['rpm'] = params.get('rpm', 120) * 1.03
        
        # Calculate new fuel consumption
        new_fuel = optimized['wob'] * optimized['rpm'] * 0.001 + 5
        
        fuel_reduction = ((current_fuel - new_fuel) / current_fuel) * 100
        co2_reduction = fuel_reduction  # Simplified: proportional to fuel
        
        sustainability_metrics = {
            'fuel_consumption_before': current_fuel,
            'fuel_consumption_after': new_fuel,
            'fuel_reduction_percent': fuel_reduction,
            'co2_reduction_percent': co2_reduction,
            'estimated_co2_saved_kg_per_hour': (current_fuel - new_fuel) * 2.68
        }
        
        return optimized, sustainability_metrics
