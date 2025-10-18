"""
Unit tests for hybrid digital twin.
"""
import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.hybrid_twin import HybridDigitalTwin
from src.data.data_collector import DrillingDataCollector


class TestHybridDigitalTwin:
    """Test cases for HybridDigitalTwin."""
    
    def test_initialization(self):
        """Test digital twin initialization."""
        twin = HybridDigitalTwin()
        assert twin.physics_model is not None
        assert twin.ml_model is not None
    
    def test_predict_risks_physics_only(self):
        """Test risk prediction using physics model only."""
        twin = HybridDigitalTwin()
        
        drilling_params = {
            'depth': 1000,
            'wob': 25,
            'rpm': 120,
            'flow_rate': 500,
            'spp': 2500,
            'torque': 15,
            'rop': 60,
            'mud_weight': 12,
            'temperature': 100
        }
        
        risks = twin.predict_risks(drilling_params, use_ml=False)
        
        assert 'wellbore_instability' in risks
        assert 'stuck_pipe' in risks
        assert 'kick_risk' in risks
        # Check the numeric risk values
        assert isinstance(risks['wellbore_instability'], (int, float))
        assert isinstance(risks['stuck_pipe'], (int, float))
        assert isinstance(risks['kick_risk'], (int, float))
    
    def test_train_and_predict(self):
        """Test training ML component and making predictions."""
        twin = HybridDigitalTwin()
        collector = DrillingDataCollector()
        
        # Generate small training dataset
        training_data = collector.generate_sample_data(100)
        X_train, y_targets, scaler = collector.preprocess_data(training_data)
        
        # Train
        twin.train_ml_component(X_train, y_targets, scaler)
        
        # Predict
        drilling_params = {
            'depth': 1000,
            'wob': 25,
            'rpm': 120,
            'flow_rate': 500,
            'spp': 2500,
            'torque': 15,
            'rop': 60,
            'mud_weight': 12,
            'temperature': 100
        }
        
        risks = twin.predict_risks(drilling_params, use_ml=True)
        
        assert 'wellbore_instability' in risks
        assert 'stuck_pipe' in risks
        assert 'kick_risk' in risks
    
    def test_get_recommendations(self):
        """Test recommendation generation."""
        twin = HybridDigitalTwin()
        
        # High risks
        risks = {
            'wellbore_instability': 0.8,
            'stuck_pipe': 0.7,
            'kick_risk': 0.85
        }
        
        drilling_params = {
            'depth': 1000,
            'wob': 25,
            'rpm': 120
        }
        
        recommendations = twin.get_recommendations(risks, drilling_params)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        for rec in recommendations:
            assert 'risk_type' in rec
            assert 'severity' in rec
            assert 'action' in rec
            assert 'priority' in rec
    
    def test_recommendations_sorted_by_priority(self):
        """Test that recommendations are sorted by priority."""
        twin = HybridDigitalTwin()
        
        risks = {
            'wellbore_instability': 0.8,
            'stuck_pipe': 0.7,
            'kick_risk': 0.85
        }
        
        drilling_params = {'depth': 1000}
        
        recommendations = twin.get_recommendations(risks, drilling_params)
        
        # Check that priorities are in order
        priorities = [rec['priority'] for rec in recommendations]
        assert priorities == sorted(priorities)
    
    def test_low_risks_few_recommendations(self):
        """Test that low risks generate few or no recommendations."""
        twin = HybridDigitalTwin()
        
        # Low risks
        risks = {
            'wellbore_instability': 0.2,
            'stuck_pipe': 0.3,
            'kick_risk': 0.1
        }
        
        drilling_params = {'depth': 1000}
        
        recommendations = twin.get_recommendations(risks, drilling_params)
        
        # Should have few or no recommendations
        assert len(recommendations) <= 2
