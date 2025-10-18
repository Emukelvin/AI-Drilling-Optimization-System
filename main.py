"""
AI-Driven Autonomous Drilling Optimization System
Main application entry point
"""

import sys
import os
import argparse

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils import DrillingDataGenerator, Config
from hybrid_twin import DigitalTwin


def generate_training_data(num_samples: int = 1000):
    """
    Generate synthetic training data.
    
    Args:
        num_samples: Number of samples to generate
    """
    print(f"Generating {num_samples} synthetic drilling data samples...")
    
    generator = DrillingDataGenerator()
    data = generator.generate_complete_dataset(num_samples)
    
    # Save data
    filepath = 'data/synthetic/training_data.csv'
    generator.save_dataset(data, filepath)
    
    print(f"✅ Data saved to {filepath}")
    
    # Generate case study data
    for scenario in ['normal', 'high_risk', 'optimal']:
        case_data = generator.generate_case_study_data(scenario)
        case_filepath = f'data/synthetic/case_study_{scenario}.csv'
        generator.save_dataset(case_data, case_filepath)
        print(f"✅ Case study '{scenario}' saved to {case_filepath}")


def run_dashboard():
    """Launch the Streamlit dashboard."""
    import subprocess
    
    dashboard_path = os.path.join('src', 'dashboard', 'app.py')
    
    print("🚀 Launching dashboard...")
    print("📊 Dashboard will open in your browser")
    print("Press Ctrl+C to stop\n")
    
    subprocess.run(['streamlit', 'run', dashboard_path])


def run_simulation():
    """Run a simple console-based simulation."""
    print("🛢️  AI-Driven Autonomous Drilling Optimization System")
    print("=" * 60)
    print()
    
    # Initialize
    config = Config()
    digital_twin = DigitalTwin()
    
    print("Initializing hybrid digital twin...")
    print("✅ Physics models loaded")
    print("✅ ML models loaded")
    print()
    
    # Set up drilling parameters
    drilling_params = {
        'wob': 80.0,
        'rpm': 120.0,
        'flow_rate': 1000.0,
        'mud_weight': 1200.0,
        'bit_diameter': 12.25,
        'pipe_od': 5.0,
        'tvd': 2000.0,
        'bit_wear': 0.1
    }
    
    formation_params = {
        'formation_strength': 30.0,
        'formation_abrasiveness': 0.5,
        'pore_pressure': 300.0,
        'fracture_gradient': 1800.0
    }
    
    print("Current Drilling Parameters:")
    print(f"  WOB: {drilling_params['wob']} kN")
    print(f"  RPM: {drilling_params['rpm']} RPM")
    print(f"  Flow Rate: {drilling_params['flow_rate']} LPM")
    print(f"  Mud Weight: {drilling_params['mud_weight']} kg/m³")
    print()
    
    # Update state
    print("Calculating drilling performance...")
    state = digital_twin.update_state(drilling_params, formation_params)
    
    print("\n📊 Performance Metrics:")
    print(f"  ROP: {state['rop']:.2f} m/hr")
    print(f"  Torque: {state['torque']:.2f} kN-m")
    print(f"  ECD: {state['ecd']:.0f} kg/m³")
    print(f"  Efficiency: {state['efficiency']:.2%}")
    print()
    
    # Risk assessment
    overall_risk = digital_twin.get_overall_risk_score()
    print(f"⚠️  Overall Risk Score: {overall_risk:.2%}")
    print()
    
    print("Risk Breakdown:")
    print(f"  Stuck Pipe: {state['hybrid_stuck_pipe_risk']:.2%}")
    print(f"  Kick Risk: {state['hybrid_kick_risk']:.2%}")
    print(f"  Lost Circulation: {state['hybrid_lost_circulation_risk']:.2%}")
    print(f"  Wellbore Instability: {state['hybrid_instability_risk']:.2%}")
    print()
    
    # Get recommendations
    print("🎯 Generating optimization recommendations...")
    recommendations = digital_twin.get_recommendations(target_rop=25.0)
    
    print("\nOptimized Parameters:")
    optimized = recommendations['optimized_parameters']
    print(f"  WOB: {optimized['wob']:.1f} kN")
    print(f"  RPM: {optimized['rpm']:.1f} RPM")
    print(f"  Flow Rate: {optimized['flow_rate']:.1f} LPM")
    print(f"  Mud Weight: {optimized['mud_weight']:.1f} kg/m³")
    print(f"  Expected ROP: {optimized['predicted_rop']:.1f} m/hr")
    print()
    
    # Alerts
    alerts = recommendations['alerts']
    if alerts:
        print("⚠️  Active Alerts:")
        for alert in alerts:
            severity_icon = "🔴" if alert['severity'] == 'critical' else "🟡" if alert['severity'] == 'high' else "🟢"
            print(f"  {severity_icon} {alert['type'].upper()}: {alert['message']}")
        print()
    
    # Sustainability
    sustainability = digital_twin.get_sustainability_score()
    print(f"🌱 Sustainability Score: {sustainability:.2%}")
    print()
    
    print("=" * 60)
    print("✅ Simulation complete!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='AI-Driven Autonomous Drilling Optimization System'
    )
    
    parser.add_argument(
        'command',
        choices=['dashboard', 'simulate', 'generate-data'],
        help='Command to run'
    )
    
    parser.add_argument(
        '--samples',
        type=int,
        default=1000,
        help='Number of samples for data generation'
    )
    
    args = parser.parse_args()
    
    if args.command == 'dashboard':
        run_dashboard()
    elif args.command == 'simulate':
        run_simulation()
    elif args.command == 'generate-data':
        generate_training_data(args.samples)


if __name__ == '__main__':
    main()
