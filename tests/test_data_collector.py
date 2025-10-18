"""
Unit tests for data collection module.
"""
import pytest
import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.data_collector import DrillingDataCollector


class TestDrillingDataCollector:
    """Test cases for DrillingDataCollector."""
    
    def test_initialization(self):
        """Test collector initialization."""
        collector = DrillingDataCollector()
        assert collector.current_depth == 0
        assert collector.start_time is not None
    
    def test_generate_sample_data(self):
        """Test sample data generation."""
        collector = DrillingDataCollector()
        data = collector.generate_sample_data(100)
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) == 100
        assert 'depth' in data.columns
        assert 'wob' in data.columns
        assert 'rop' in data.columns
        assert 'wellbore_instability' in data.columns
        assert 'stuck_pipe' in data.columns
        assert 'kick_risk' in data.columns
    
    def test_collect_realtime_data(self):
        """Test real-time data collection."""
        collector = DrillingDataCollector()
        data = collector.collect_realtime_data()
        
        assert isinstance(data, dict)
        assert 'timestamp' in data
        assert 'depth' in data
        assert 'wob' in data
        assert 'rpm' in data
        assert data['depth'] >= 0
    
    def test_preprocess_data(self):
        """Test data preprocessing."""
        collector = DrillingDataCollector()
        raw_data = collector.generate_sample_data(50)
        
        X_scaled, y_targets, scaler = collector.preprocess_data(raw_data)
        
        assert X_scaled.shape[0] == 50
        assert X_scaled.shape[1] == 9  # Number of features
        assert len(y_targets) == 3  # Three target variables
        assert scaler is not None
    
    def test_data_values_in_range(self):
        """Test that generated data values are in reasonable ranges."""
        collector = DrillingDataCollector()
        data = collector.generate_sample_data(100)
        
        assert data['wob'].min() >= 0
        assert data['wob'].max() <= 60
        assert data['rpm'].min() >= 0
        assert data['rpm'].max() <= 300
        assert data['rop'].min() >= 0
        assert data['wellbore_instability'].min() >= 0
        assert data['wellbore_instability'].max() <= 1
