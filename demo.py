"""
Demo script to showcase the AI Drilling Optimization System capabilities.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data.data_collector import DrillingDataCollector
from src.models.hybrid_twin import HybridDigitalTwin
from src.optimization.optimizer import AutonomousOptimizer
from src.utils import setup_logger

logger = setup_logger(__name__)


def main():
    """Demonstrate system capabilities."""
    print("=" * 70)
    print("AI Drilling Optimization System - Demo")
    print("=" * 70)
    print()
    
    # Initialize components
    print("1. Initializing components...")
    collector = DrillingDataCollector()
    twin = HybridDigitalTwin()
    optimizer = AutonomousOptimizer()
    print("   ✓ Components initialized")
    print()
    
    # Train models
    print("2. Training models on sample data...")
    training_data = collector.generate_sample_data(500)
    X_train, y_targets, scaler = collector.preprocess_data(training_data)
    twin.train_ml_component(X_train, y_targets, scaler)
    print(f"   ✓ Trained on {len(training_data)} samples")
    print()
    
    # Simulate real-time drilling
    print("3. Simulating real-time drilling scenario...")
    print()
    
    # Scenario 1: Normal drilling
    print("   Scenario 1: Normal Drilling Conditions")
    print("   " + "-" * 60)
    
    params1 = {
        'depth': 3000,
        'wob': 25,
        'rpm': 120,
        'flow_rate': 500,
        'spp': 2500,
        'torque': 15,
        'rop': 65,
        'mud_weight': 12,
        'temperature': 115
    }
    
    print(f"   Current Parameters:")
    print(f"     • Depth: {params1['depth']} ft")
    print(f"     • WOB: {params1['wob']} klbs")
    print(f"     • RPM: {params1['rpm']}")
    print(f"     • ROP: {params1['rop']} ft/hr")
    print()
    
    risks1 = twin.predict_risks(params1, use_ml=True)
    print(f"   Risk Assessment:")
    print(f"     • Wellbore Instability: {risks1['wellbore_instability']*100:.1f}%")
    print(f"     • Stuck Pipe: {risks1['stuck_pipe']*100:.1f}%")
    print(f"     • Kick Risk: {risks1['kick_risk']*100:.1f}%")
    print()
    
    recommendations1 = twin.get_recommendations(risks1, params1)
    if recommendations1:
        print(f"   Recommendations: {len(recommendations1)} action(s)")
        for rec in recommendations1[:3]:
            print(f"     • [{rec['severity']}] {rec['action']}")
    else:
        print("   ✓ All parameters optimal")
    print()
    
    # Scenario 2: High risk drilling
    print("   Scenario 2: High Risk Conditions")
    print("   " + "-" * 60)
    
    params2 = {
        'depth': 8000,
        'wob': 35,
        'rpm': 140,
        'flow_rate': 450,
        'spp': 2900,
        'torque': 22,
        'rop': 85,
        'mud_weight': 11.5,
        'temperature': 190
    }
    
    print(f"   Current Parameters:")
    print(f"     • Depth: {params2['depth']} ft")
    print(f"     • WOB: {params2['wob']} klbs (HIGH)")
    print(f"     • RPM: {params2['rpm']}")
    print(f"     • Torque: {params2['torque']} klb-ft (HIGH)")
    print()
    
    risks2 = twin.predict_risks(params2, use_ml=True)
    print(f"   Risk Assessment:")
    print(f"     • Wellbore Instability: {risks2['wellbore_instability']*100:.1f}%")
    print(f"     • Stuck Pipe: {risks2['stuck_pipe']*100:.1f}%")
    print(f"     • Kick Risk: {risks2['kick_risk']*100:.1f}%")
    print()
    
    recommendations2 = twin.get_recommendations(risks2, params2)
    print(f"   Recommendations: {len(recommendations2)} action(s)")
    for rec in recommendations2[:5]:
        print(f"     • [{rec['severity']}] {rec['action']}")
    print()
    
    optimized2, adjustments2 = optimizer.optimize_parameters(
        params2, risks2, recommendations2
    )
    
    print(f"   Optimized Parameters:")
    print(f"     • WOB: {params2['wob']:.1f} → {optimized2['wob']:.1f} klbs")
    print(f"     • RPM: {params2['rpm']:.0f} → {optimized2['rpm']:.0f}")
    print(f"     • Mud Weight: {params2['mud_weight']:.1f} → {optimized2['mud_weight']:.1f} ppg")
    print()
    
    # Scenario 3: Sustainability optimization
    print("   Scenario 3: Sustainability Optimization")
    print("   " + "-" * 60)
    
    params3 = {
        'depth': 5000,
        'wob': 28,
        'rpm': 115,
        'flow_rate': 520,
        'mud_weight': 12.5
    }
    
    optimized3, metrics3 = optimizer.optimize_for_sustainability(params3)
    
    print(f"   Environmental Impact:")
    print(f"     • Fuel Consumption: {metrics3['fuel_consumption_before']:.2f} → {metrics3['fuel_consumption_after']:.2f} gal/hr")
    print(f"     • Fuel Reduction: {metrics3['fuel_reduction_percent']:.1f}%")
    print(f"     • CO2 Reduction: {metrics3['co2_reduction_percent']:.1f}%")
    print(f"     • CO2 Saved: {metrics3['estimated_co2_saved_kg_per_hour']:.2f} kg/hr")
    print()
    
    efficiency = optimizer.calculate_efficiency_score(params3, risks1)
    print(f"   Drilling Efficiency Score: {efficiency:.1f}/100")
    print()
    
    # Summary
    print("=" * 70)
    print("Demo Complete!")
    print()
    print("Next Steps:")
    print("  1. Run the training script: python train.py --samples 1000")
    print("  2. Launch the dashboard: streamlit run src/dashboard/app.py")
    print("  3. Explore the API in docs/api_reference.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
