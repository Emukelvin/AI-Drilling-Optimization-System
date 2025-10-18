"""
Integration test for the complete AI Drilling Optimization System.
Tests the full workflow from data collection to optimization.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.data_collector import DrillingDataCollector
from src.models.hybrid_twin import HybridDigitalTwin
from src.optimization.optimizer import AutonomousOptimizer


def test_full_workflow():
    """Test complete workflow from data to optimization."""
    print("Running integration test...")
    
    # 1. Data Collection
    print("  1. Testing data collection...")
    collector = DrillingDataCollector()
    data = collector.generate_sample_data(100)
    assert len(data) == 100
    assert 'depth' in data.columns
    print("     ✓ Data collection works")
    
    # 2. Data Preprocessing
    print("  2. Testing data preprocessing...")
    X_train, y_targets, scaler = collector.preprocess_data(data)
    assert X_train.shape[0] == 100
    assert len(y_targets) == 3
    print("     ✓ Data preprocessing works")
    
    # 3. Model Training
    print("  3. Testing model training...")
    twin = HybridDigitalTwin()
    twin.train_ml_component(X_train, y_targets, scaler)
    print("     ✓ Model training works")
    
    # 4. Risk Prediction (Physics only)
    print("  4. Testing physics-based prediction...")
    params = {
        'depth': 5000,
        'wob': 25,
        'rpm': 120,
        'flow_rate': 500,
        'spp': 2500,
        'torque': 15,
        'rop': 60,
        'mud_weight': 12,
        'temperature': 150
    }
    risks_physics = twin.predict_risks(params, use_ml=False)
    assert 'wellbore_instability' in risks_physics
    assert 'stuck_pipe' in risks_physics
    assert 'kick_risk' in risks_physics
    print("     ✓ Physics-based prediction works")
    
    # 5. Risk Prediction (Hybrid)
    print("  5. Testing hybrid prediction...")
    risks_hybrid = twin.predict_risks(params, use_ml=True)
    assert 'wellbore_instability' in risks_hybrid
    print("     ✓ Hybrid prediction works")
    
    # 6. Recommendations
    print("  6. Testing recommendations...")
    recommendations = twin.get_recommendations(risks_hybrid, params)
    assert isinstance(recommendations, list)
    print(f"     ✓ Recommendations works ({len(recommendations)} recommendations)")
    
    # 7. Optimization
    print("  7. Testing optimization...")
    optimizer = AutonomousOptimizer()
    optimized, adjustments = optimizer.optimize_parameters(
        params, risks_hybrid, recommendations
    )
    assert 'wob' in optimized
    assert 'rpm' in optimized
    print("     ✓ Optimization works")
    
    # 8. Sustainability
    print("  8. Testing sustainability optimization...")
    optimized_sustain, metrics = optimizer.optimize_for_sustainability(params)
    assert 'fuel_reduction_percent' in metrics
    assert 'co2_reduction_percent' in metrics
    print("     ✓ Sustainability optimization works")
    
    # 9. Efficiency Score
    print("  9. Testing efficiency calculation...")
    efficiency = optimizer.calculate_efficiency_score(params, risks_hybrid)
    assert 0 <= efficiency <= 100
    print(f"     ✓ Efficiency calculation works (score: {efficiency:.1f})")
    
    # 10. Model Save/Load
    print(" 10. Testing model persistence...")
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        twin.save_models(tmpdir)
        twin2 = HybridDigitalTwin()
        twin2.load_models(tmpdir)
        risks_loaded = twin2.predict_risks(params, use_ml=True)
        assert 'wellbore_instability' in risks_loaded
    print("     ✓ Model persistence works")
    
    print("\n✅ All integration tests passed!")
    print("   The system is fully functional and ready to use.")
    return True


if __name__ == "__main__":
    test_full_workflow()
