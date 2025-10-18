"""
Simple test script to verify all components are working correctly.
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_physics_models():
    """Test physics-based models."""
    print("Testing Physics Models...")
    
    from physics_models import DrillingMechanics, DrillingHydraulics
    
    mechanics = DrillingMechanics()
    hydraulics = DrillingHydraulics()
    
    # Test mechanics
    rop = mechanics.calculate_rop(80, 120, 12.25, 30, 0.1)
    assert rop > 0, "ROP should be positive"
    print(f"  ✓ Mechanics: ROP = {rop:.2f} m/hr")
    
    # Test hydraulics
    ecd = hydraulics.calculate_ecd(1200, 1000, 2000, 12.25, 5.0)
    assert ecd >= 1200, "ECD should be >= mud weight"
    print(f"  ✓ Hydraulics: ECD = {ecd:.0f} kg/m³")
    
    print("✅ Physics models working correctly\n")


def test_ml_models():
    """Test ML models."""
    print("Testing ML Models...")
    
    from ml_models import RiskPredictor, WellboreStabilityModel, ROPOptimizer
    import pandas as pd
    
    # Test risk predictor
    predictor = RiskPredictor()
    risks = predictor.get_risk_score(80, 120, 1000, 1200, 1205, 3.7, 68, 2000, 30, 12)
    assert len(risks) == 4, "Should return 4 risk types"
    print(f"  ✓ Risk Predictor: {len(risks)} risk scores calculated")
    
    # Test stability model
    stability = WellboreStabilityModel()
    stability_index = stability.calculate_stability_index(1200, 300, 1800, 2000, 30)
    assert 0 <= stability_index <= 1, "Stability index should be 0-1"
    print(f"  ✓ Stability Model: Stability Index = {stability_index:.2f}")
    
    # Test ROP optimizer
    optimizer = ROPOptimizer()
    predicted_rop = optimizer.predict_rop(80, 120, 1000, 1200, 30, 0.1)
    assert predicted_rop > 0, "Predicted ROP should be positive"
    print(f"  ✓ ROP Optimizer: Predicted ROP = {predicted_rop:.2f} m/hr")
    
    print("✅ ML models working correctly\n")


def test_hybrid_twin():
    """Test hybrid digital twin."""
    print("Testing Hybrid Digital Twin...")
    
    from hybrid_twin import DigitalTwin
    
    twin = DigitalTwin()
    
    drilling_params = {
        'wob': 80.0, 'rpm': 120.0, 'flow_rate': 1000.0,
        'mud_weight': 1200.0, 'bit_diameter': 12.25,
        'pipe_od': 5.0, 'tvd': 2000.0, 'bit_wear': 0.1
    }
    
    formation_params = {
        'formation_strength': 30.0, 'formation_abrasiveness': 0.5,
        'pore_pressure': 300.0, 'fracture_gradient': 1800.0
    }
    
    # Test state update
    state = twin.update_state(drilling_params, formation_params)
    assert 'rop' in state, "State should contain ROP"
    print(f"  ✓ State Update: ROP = {state['rop']:.2f} m/hr")
    
    # Test risk score
    risk = twin.get_overall_risk_score()
    assert 0 <= risk <= 1, "Risk should be 0-1"
    print(f"  ✓ Risk Score: {risk:.2%}")
    
    # Test efficiency
    efficiency = twin.get_efficiency_score()
    assert 0 <= efficiency <= 1, "Efficiency should be 0-1"
    print(f"  ✓ Efficiency: {efficiency:.2%}")
    
    # Test optimization
    recommendations = twin.get_recommendations(target_rop=25.0)
    assert 'optimized_parameters' in recommendations
    print(f"  ✓ Optimization: Generated recommendations")
    
    print("✅ Hybrid Digital Twin working correctly\n")


def test_utilities():
    """Test utility modules."""
    print("Testing Utilities...")
    
    from utils import DrillingDataGenerator, Config
    
    # Test data generator
    generator = DrillingDataGenerator(random_seed=42)
    data = generator.generate_complete_dataset(num_samples=50, well_depth=2000)
    assert len(data) == 50, "Should generate 50 samples"
    print(f"  ✓ Data Generator: Generated {len(data)} samples")
    
    # Test config
    config = Config()
    wob = config.get('drilling.default_wob')
    assert wob is not None, "Should load default config"
    print(f"  ✓ Config: Default WOB = {wob} kN")
    
    print("✅ Utilities working correctly\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("AI Drilling Optimization System - Component Tests")
    print("=" * 60)
    print()
    
    try:
        test_physics_models()
        test_ml_models()
        test_hybrid_twin()
        test_utilities()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nSystem is ready to use. Try:")
        print("  python main.py simulate       # Run simulation")
        print("  python main.py dashboard      # Launch dashboard")
        print("  python main.py generate-data  # Generate training data")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
