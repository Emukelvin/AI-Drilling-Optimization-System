"""
Unit tests for autonomous optimizer.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.optimization.optimizer import AutonomousOptimizer


class TestAutonomousOptimizer:
    """Test cases for AutonomousOptimizer."""
    
    def test_initialization(self):
        """Test optimizer initialization."""
        optimizer = AutonomousOptimizer()
        assert optimizer.max_wob_adjustment > 0
        assert optimizer.max_rpm_adjustment > 0
        assert optimizer.max_flow_rate_adjustment > 0
    
    def test_optimize_parameters(self):
        """Test parameter optimization."""
        optimizer = AutonomousOptimizer()
        
        current_params = {
            'depth': 1000,
            'wob': 25,
            'rpm': 120,
            'flow_rate': 500,
            'mud_weight': 12,
            'rop': 60
        }
        
        risks = {
            'wellbore_instability': 0.8,
            'stuck_pipe': 0.7,
            'kick_risk': 0.3
        }
        
        recommendations = []
        
        optimized, adjustments = optimizer.optimize_parameters(
            current_params, risks, recommendations
        )
        
        assert 'wob' in optimized
        assert 'rpm' in optimized
        assert 'flow_rate' in optimized
        assert isinstance(adjustments, list)
    
    def test_bounded_adjustment(self):
        """Test bounded adjustment logic."""
        optimizer = AutonomousOptimizer()
        
        # Test increase
        adjusted = optimizer._apply_bounded_adjustment(100, 1.2, 10)
        assert adjusted <= 110  # Max 10% increase
        
        # Test decrease
        adjusted = optimizer._apply_bounded_adjustment(100, 0.8, 10)
        assert adjusted >= 90  # Max 10% decrease
    
    def test_calculate_efficiency_score(self):
        """Test efficiency score calculation."""
        optimizer = AutonomousOptimizer()
        
        params = {
            'rop': 80,
            'wob': 25,
            'rpm': 120
        }
        
        risks = {
            'wellbore_instability': 0.1,
            'stuck_pipe': 0.1,
            'kick_risk': 0.1
        }
        
        score = optimizer.calculate_efficiency_score(params, risks)
        
        assert score >= 0
        assert score <= 100
    
    def test_optimize_for_sustainability(self):
        """Test sustainability optimization."""
        optimizer = AutonomousOptimizer()
        
        params = {
            'wob': 25,
            'rpm': 120,
            'flow_rate': 500,
            'mud_weight': 12
        }
        
        optimized, metrics = optimizer.optimize_for_sustainability(params)
        
        assert 'wob' in optimized
        assert 'rpm' in optimized
        assert 'fuel_reduction_percent' in metrics
        assert 'co2_reduction_percent' in metrics
    
    def test_high_risk_adjustments(self):
        """Test that high risks trigger significant adjustments."""
        optimizer = AutonomousOptimizer()
        
        current_params = {
            'depth': 1000,
            'wob': 30,
            'rpm': 120,
            'flow_rate': 500,
            'mud_weight': 12,
            'rop': 60
        }
        
        # High risks
        high_risks = {
            'wellbore_instability': 0.9,
            'stuck_pipe': 0.8,
            'kick_risk': 0.9
        }
        
        optimized, adjustments = optimizer.optimize_parameters(
            current_params, high_risks, []
        )
        
        # Should reduce WOB significantly
        assert optimized['wob'] < current_params['wob']
        # Should increase mud weight
        assert optimized['mud_weight'] > current_params['mud_weight']
        # Should have multiple adjustments
        assert len(adjustments) > 0
