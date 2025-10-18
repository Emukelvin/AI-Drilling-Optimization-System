"""
Unit tests for physics model.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.physics_model import PhysicsWellModel


class TestPhysicsWellModel:
    """Test cases for PhysicsWellModel."""
    
    def test_initialization(self):
        """Test model initialization."""
        model = PhysicsWellModel()
        assert model.formation_pressure_gradient > 0
        assert model.fracture_gradient > 0
    
    def test_calculate_formation_pressure(self):
        """Test formation pressure calculation."""
        model = PhysicsWellModel()
        pressure = model.calculate_formation_pressure(1000)
        
        assert pressure > 0
        assert pressure == 1000 * model.formation_pressure_gradient
    
    def test_calculate_fracture_pressure(self):
        """Test fracture pressure calculation."""
        model = PhysicsWellModel()
        pressure = model.calculate_fracture_pressure(1000)
        
        assert pressure > 0
        assert pressure == 1000 * model.fracture_gradient
    
    def test_calculate_hydrostatic_pressure(self):
        """Test hydrostatic pressure calculation."""
        model = PhysicsWellModel()
        pressure = model.calculate_hydrostatic_pressure(1000, 12)
        
        assert pressure > 0
        # P = 0.052 * mud_weight * depth
        expected = 0.052 * 12 * 1000
        assert abs(pressure - expected) < 0.01
    
    def test_calculate_rop(self):
        """Test ROP calculation."""
        model = PhysicsWellModel()
        rop = model.calculate_rop(25, 120, 500)
        
        assert rop >= 0
    
    def test_calculate_torque(self):
        """Test torque calculation."""
        model = PhysicsWellModel()
        torque = model.calculate_torque(25, 120, 1000)
        
        assert torque > 0
    
    def test_check_wellbore_stability(self):
        """Test wellbore stability check."""
        model = PhysicsWellModel()
        stability = model.check_wellbore_stability(1000, 12)
        
        assert 'is_stable' in stability
        assert 'formation_pressure' in stability
        assert 'fracture_pressure' in stability
        assert 'hydrostatic_pressure' in stability
        assert isinstance(stability['is_stable'], bool)
    
    def test_predict_physics_based_risks(self):
        """Test physics-based risk prediction."""
        model = PhysicsWellModel()
        
        drilling_params = {
            'depth': 1000,
            'mud_weight': 12,
            'wob': 25,
            'torque': 15,
            'rpm': 120
        }
        
        risks = model.predict_physics_based_risks(drilling_params)
        
        assert 'wellbore_instability' in risks
        assert 'stuck_pipe' in risks
        assert 'kick_risk' in risks
        assert risks['wellbore_instability'] >= 0
        assert risks['wellbore_instability'] <= 1
