"""
Streamlit Dashboard for AI-Driven Autonomous Drilling Optimization System
Interactive web interface for real-time monitoring and optimization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hybrid_twin import DigitalTwin
from utils import DrillingDataGenerator, Config

# Page configuration
st.set_page_config(
    page_title="AI Drilling Optimization System",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .risk-high {
        color: #ff4444;
        font-weight: bold;
    }
    .risk-medium {
        color: #ffaa00;
        font-weight: bold;
    }
    .risk-low {
        color: #44ff44;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


class DrillingDashboard:
    """Main dashboard application class."""
    
    def __init__(self):
        """Initialize the dashboard."""
        self.config = Config()
        self.digital_twin = DigitalTwin()
        self.data_generator = DrillingDataGenerator()
        
        # Initialize session state
        if 'initialized' not in st.session_state:
            self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        st.session_state.initialized = True
        st.session_state.simulation_running = False
        st.session_state.current_depth = 0
        st.session_state.history_data = []
        
        # Load default parameters
        st.session_state.drilling_params = self.config.get_drilling_params()
        st.session_state.formation_params = self.config.get_formation_params()
    
    def run(self):
        """Run the main dashboard application."""
        # Header
        st.title("🛢️ AI-Driven Autonomous Drilling Optimization System")
        st.markdown("**Hybrid Digital Twin for Real-Time Drilling Optimization**")
        
        # Sidebar
        self._render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Real-Time Monitoring",
            "🎯 Optimization",
            "⚠️ Risk Prediction",
            "📈 Analytics",
            "⚙️ Settings"
        ])
        
        with tab1:
            self._render_monitoring_tab()
        
        with tab2:
            self._render_optimization_tab()
        
        with tab3:
            self._render_risk_prediction_tab()
        
        with tab4:
            self._render_analytics_tab()
        
        with tab5:
            self._render_settings_tab()
    
    def _render_sidebar(self):
        """Render the sidebar with controls."""
        st.sidebar.header("Control Panel")
        
        # Simulation controls
        st.sidebar.subheader("Simulation Control")
        
        if st.sidebar.button("▶️ Start Simulation", use_container_width=True):
            st.session_state.simulation_running = True
        
        if st.sidebar.button("⏸️ Pause Simulation", use_container_width=True):
            st.session_state.simulation_running = False
        
        if st.sidebar.button("🔄 Reset", use_container_width=True):
            self._initialize_session_state()
            st.rerun()
        
        st.sidebar.divider()
        
        # Drilling parameters
        st.sidebar.subheader("Drilling Parameters")
        
        wob = st.sidebar.slider(
            "Weight on Bit (kN)",
            min_value=20.0,
            max_value=150.0,
            value=float(st.session_state.drilling_params['default_wob']),
            step=5.0
        )
        
        rpm = st.sidebar.slider(
            "Rotary Speed (RPM)",
            min_value=50.0,
            max_value=200.0,
            value=float(st.session_state.drilling_params['default_rpm']),
            step=10.0
        )
        
        flow_rate = st.sidebar.slider(
            "Flow Rate (LPM)",
            min_value=500.0,
            max_value=2000.0,
            value=float(st.session_state.drilling_params['default_flow_rate']),
            step=50.0
        )
        
        mud_weight = st.sidebar.slider(
            "Mud Weight (kg/m³)",
            min_value=1000.0,
            max_value=1600.0,
            value=float(st.session_state.drilling_params['default_mud_weight']),
            step=50.0
        )
        
        # Update parameters
        st.session_state.drilling_params.update({
            'wob': wob,
            'rpm': rpm,
            'flow_rate': flow_rate,
            'mud_weight': mud_weight
        })
        
        st.sidebar.divider()
        
        # Formation parameters
        st.sidebar.subheader("Formation Properties")
        
        formation_strength = st.sidebar.slider(
            "Formation Strength (MPa)",
            min_value=10.0,
            max_value=100.0,
            value=float(st.session_state.formation_params['default_strength']),
            step=5.0
        )
        
        pore_pressure = st.sidebar.slider(
            "Pore Pressure (bar)",
            min_value=100.0,
            max_value=600.0,
            value=float(st.session_state.formation_params['default_pore_pressure']),
            step=50.0
        )
        
        st.session_state.formation_params.update({
            'formation_strength': formation_strength,
            'pore_pressure': pore_pressure
        })
    
    def _render_monitoring_tab(self):
        """Render the real-time monitoring tab."""
        st.header("Real-Time Monitoring")
        
        # Update digital twin state
        drilling_params = {
            'wob': st.session_state.drilling_params['wob'],
            'rpm': st.session_state.drilling_params['rpm'],
            'flow_rate': st.session_state.drilling_params['flow_rate'],
            'mud_weight': st.session_state.drilling_params['mud_weight'],
            'bit_diameter': st.session_state.drilling_params['default_bit_diameter'],
            'pipe_od': st.session_state.drilling_params['default_pipe_od'],
            'tvd': st.session_state.drilling_params['default_tvd'],
            'bit_wear': 0.1
        }
        
        formation_params = {
            'formation_strength': st.session_state.formation_params['formation_strength'],
            'formation_abrasiveness': st.session_state.formation_params['default_abrasiveness'],
            'pore_pressure': st.session_state.formation_params['pore_pressure'],
            'fracture_gradient': st.session_state.formation_params['default_fracture_gradient']
        }
        
        current_state = self.digital_twin.update_state(drilling_params, formation_params)
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "ROP",
                f"{current_state['rop']:.1f} m/hr",
                delta=None
            )
        
        with col2:
            risk_score = self.digital_twin.get_overall_risk_score()
            risk_color = "🟢" if risk_score < 0.3 else "🟡" if risk_score < 0.6 else "🔴"
            st.metric(
                "Overall Risk",
                f"{risk_color} {risk_score:.2f}",
                delta=None
            )
        
        with col3:
            efficiency = self.digital_twin.get_efficiency_score()
            st.metric(
                "Efficiency",
                f"{efficiency:.2%}",
                delta=None
            )
        
        with col4:
            sustainability = self.digital_twin.get_sustainability_score()
            st.metric(
                "Sustainability",
                f"{sustainability:.2%}",
                delta=None
            )
        
        with col5:
            st.metric(
                "ECD",
                f"{current_state['ecd']:.0f} kg/m³",
                delta=f"{current_state['ecd'] - st.session_state.drilling_params['mud_weight']:.0f}"
            )
        
        st.divider()
        
        # Detailed parameters
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Drilling Parameters")
            
            params_data = {
                "Parameter": ["WOB", "RPM", "Torque", "Flow Rate", "Mud Weight"],
                "Value": [
                    f"{current_state['wob']:.1f} kN",
                    f"{current_state['rpm']:.0f} RPM",
                    f"{current_state['torque']:.1f} kN-m",
                    f"{current_state['flow_rate']:.0f} LPM",
                    f"{current_state['mud_weight']:.0f} kg/m³"
                ]
            }
            st.dataframe(params_data, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("Performance Metrics")
            
            metrics_data = {
                "Metric": ["ROP", "Efficiency", "Vibration", "Bit Wear Rate", "HHP"],
                "Value": [
                    f"{current_state['rop']:.2f} m/hr",
                    f"{current_state['efficiency']:.2%}",
                    f"{current_state['vibration']:.2%}",
                    f"{current_state['bit_wear_rate']:.4f} /hr",
                    f"{current_state['hydraulic_horsepower']:.1f} HP"
                ]
            }
            st.dataframe(metrics_data, use_container_width=True, hide_index=True)
        
        # Alerts
        alerts = self.digital_twin._generate_alerts()
        if alerts:
            st.subheader("⚠️ Active Alerts")
            for alert in alerts:
                if alert['severity'] == 'critical':
                    st.error(f"**{alert['type'].upper()}**: {alert['message']}")
                elif alert['severity'] == 'high':
                    st.warning(f"**{alert['type'].upper()}**: {alert['message']}")
                else:
                    st.info(f"**{alert['type'].upper()}**: {alert['message']}")
    
    def _render_optimization_tab(self):
        """Render the optimization tab."""
        st.header("Autonomous Optimization")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            target_rop = st.slider(
                "Target ROP (m/hr)",
                min_value=5.0,
                max_value=50.0,
                value=20.0,
                step=1.0
            )
        
        with col2:
            max_risk = st.slider(
                "Max Acceptable Risk",
                min_value=0.1,
                max_value=0.8,
                value=0.3,
                step=0.05
            )
        
        if st.button("🎯 Optimize Parameters", use_container_width=True):
            with st.spinner("Optimizing drilling parameters..."):
                recommendations = self.digital_twin.get_recommendations(target_rop)
                
                st.success("✅ Optimization complete!")
                
                # Display current vs optimized
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Current Parameters")
                    current = recommendations['current_state']
                    st.metric("ROP", f"{current['rop']:.1f} m/hr")
                    st.metric("Risk Score", f"{current['risk_score']:.2f}")
                    st.metric("Efficiency", f"{current['efficiency_score']:.2%}")
                
                with col2:
                    st.subheader("Optimized Parameters")
                    optimized = recommendations['optimized_parameters']
                    
                    st.write("**Recommended Changes:**")
                    st.write(f"WOB: {optimized['wob']:.1f} kN")
                    st.write(f"RPM: {optimized['rpm']:.1f} RPM")
                    st.write(f"Flow Rate: {optimized['flow_rate']:.1f} LPM")
                    st.write(f"Mud Weight: {optimized['mud_weight']:.1f} kg/m³")
                    st.write(f"**Expected ROP: {optimized['predicted_rop']:.1f} m/hr**")
                
                # Apply button
                if st.button("✅ Apply Optimized Parameters"):
                    st.session_state.drilling_params.update({
                        'wob': optimized['wob'],
                        'rpm': optimized['rpm'],
                        'flow_rate': optimized['flow_rate'],
                        'mud_weight': optimized['mud_weight']
                    })
                    st.success("Parameters applied successfully!")
                    st.rerun()
    
    def _render_risk_prediction_tab(self):
        """Render the risk prediction tab."""
        st.header("Risk Prediction & Analysis")
        
        # Get current state
        if not self.digital_twin.current_state:
            st.info("Please start monitoring to see risk predictions.")
            return
        
        current_state = self.digital_twin.current_state
        
        # Risk scores
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            risk_val = current_state.get('hybrid_stuck_pipe_risk', 0)
            risk_color = "🟢" if risk_val < 0.3 else "🟡" if risk_val < 0.6 else "🔴"
            st.metric("Stuck Pipe Risk", f"{risk_color} {risk_val:.2%}")
        
        with col2:
            risk_val = current_state.get('hybrid_kick_risk', 0)
            risk_color = "🟢" if risk_val < 0.3 else "🟡" if risk_val < 0.6 else "🔴"
            st.metric("Kick Risk", f"{risk_color} {risk_val:.2%}")
        
        with col3:
            risk_val = current_state.get('hybrid_lost_circulation_risk', 0)
            risk_color = "🟢" if risk_val < 0.3 else "🟡" if risk_val < 0.6 else "🔴"
            st.metric("Lost Circulation", f"{risk_color} {risk_val:.2%}")
        
        with col4:
            risk_val = current_state.get('hybrid_instability_risk', 0)
            risk_color = "🟢" if risk_val < 0.3 else "🟡" if risk_val < 0.6 else "🔴"
            st.metric("Instability Risk", f"{risk_color} {risk_val:.2%}")
        
        st.divider()
        
        # Risk comparison chart
        st.subheader("Risk Analysis - Physics vs ML vs Hybrid")
        
        risk_types = ['Stuck Pipe', 'Lost Circulation', 'Kick', 'Instability']
        physics_risks = [
            current_state.get('physics_stuck_pipe_risk', 0),
            current_state.get('physics_lost_circulation_risk', 0),
            current_state.get('physics_kick_risk', 0),
            current_state.get('instability_risk', 0)
        ]
        ml_risks = [
            current_state.get('ml_stuck_pipe_risk', 0),
            current_state.get('ml_lost_circulation_risk', 0),
            current_state.get('ml_kick_risk', 0),
            current_state.get('ml_wellbore_instability_risk', 0)
        ]
        hybrid_risks = [
            current_state.get('hybrid_stuck_pipe_risk', 0),
            current_state.get('hybrid_lost_circulation_risk', 0),
            current_state.get('hybrid_kick_risk', 0),
            current_state.get('hybrid_instability_risk', 0)
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Physics-Based',
            x=risk_types,
            y=physics_risks,
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='ML-Based',
            x=risk_types,
            y=ml_risks,
            marker_color='lightgreen'
        ))
        
        fig.add_trace(go.Bar(
            name='Hybrid',
            x=risk_types,
            y=hybrid_risks,
            marker_color='orange'
        ))
        
        fig.update_layout(
            barmode='group',
            title='Risk Prediction Comparison',
            xaxis_title='Risk Type',
            yaxis_title='Risk Score',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Wellbore stability
        st.subheader("Wellbore Stability Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            stability_index = current_state.get('stability_index', 0.5)
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stability_index,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Stability Index"},
                gauge={
                    'axis': {'range': [0, 1]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 0.3], 'color': "red"},
                        {'range': [0.3, 0.7], 'color': "yellow"},
                        {'range': [0.7, 1], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.3
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            collapse_risk = current_state.get('collapse_risk', 0)
            fracture_risk = current_state.get('fracture_risk', 0)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Collapse Risk', 'Fracture Risk'],
                y=[collapse_risk, fracture_risk],
                marker_color=['#ff6b6b', '#ffa500']
            ))
            
            fig.update_layout(
                title='Pressure-Related Risks',
                yaxis_title='Risk Score',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_analytics_tab(self):
        """Render the analytics tab."""
        st.header("Performance Analytics")
        
        # Generate sample historical data for visualization
        if len(self.digital_twin.history) < 10:
            st.info("Generating sample historical data for analytics...")
            
            # Generate sample data
            for i in range(50):
                drilling_params = {
                    'wob': 80 + np.random.normal(0, 10),
                    'rpm': 120 + np.random.normal(0, 10),
                    'flow_rate': 1000 + np.random.normal(0, 100),
                    'mud_weight': 1200 + np.random.normal(0, 50),
                    'bit_diameter': 12.25,
                    'pipe_od': 5.0,
                    'tvd': 2000 + i * 10,
                    'bit_wear': i * 0.01
                }
                
                formation_params = {
                    'formation_strength': 30 + np.random.normal(0, 5),
                    'formation_abrasiveness': 0.5,
                    'pore_pressure': 300 + i * 2,
                    'fracture_gradient': 1800
                }
                
                self.digital_twin.update_state(drilling_params, formation_params)
        
        # Get history dataframe
        history_df = self.digital_twin.get_history_dataframe()
        
        if history_df.empty:
            st.warning("No historical data available yet.")
            return
        
        # Time series plots
        st.subheader("Performance Trends")
        
        # Create subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Rate of Penetration', 'Overall Risk Score',
                          'Efficiency Score', 'Sustainability Score')
        )
        
        x_axis = list(range(len(history_df)))
        
        # ROP
        fig.add_trace(
            go.Scatter(x=x_axis, y=history_df['rop'], name='ROP', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Risk score
        risk_scores = [
            (row['hybrid_stuck_pipe_risk'] + row['hybrid_kick_risk'] +
             row['hybrid_lost_circulation_risk'] + row['hybrid_instability_risk']) / 4
            for _, row in history_df.iterrows()
        ]
        fig.add_trace(
            go.Scatter(x=x_axis, y=risk_scores, name='Risk', line=dict(color='red')),
            row=1, col=2
        )
        
        # Efficiency
        fig.add_trace(
            go.Scatter(x=x_axis, y=history_df['efficiency'], name='Efficiency', line=dict(color='green')),
            row=2, col=1
        )
        
        # Sustainability (calculate)
        sustainability_scores = []
        for _, row in history_df.iterrows():
            hhp = row.get('hydraulic_horsepower', 100)
            rop = row.get('rop', 10)
            energy_eff = rop / (hhp + 1e-6)
            sustainability_scores.append(min(1.0, energy_eff / 0.5))
        
        fig.add_trace(
            go.Scatter(x=x_axis, y=sustainability_scores, name='Sustainability', line=dict(color='purple')),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_rop = history_df['rop'].mean()
            st.metric("Avg ROP", f"{avg_rop:.1f} m/hr")
        
        with col2:
            avg_risk = np.mean(risk_scores)
            st.metric("Avg Risk", f"{avg_risk:.2%}")
        
        with col3:
            avg_efficiency = history_df['efficiency'].mean()
            st.metric("Avg Efficiency", f"{avg_efficiency:.2%}")
        
        with col4:
            avg_sustainability = np.mean(sustainability_scores)
            st.metric("Avg Sustainability", f"{avg_sustainability:.2%}")
    
    def _render_settings_tab(self):
        """Render the settings tab."""
        st.header("System Settings")
        
        st.subheader("Safety Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_risk = st.slider(
                "Maximum Risk Threshold",
                min_value=0.1,
                max_value=1.0,
                value=0.7,
                step=0.05
            )
            
            min_efficiency = st.slider(
                "Minimum Efficiency Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.05
            )
        
        with col2:
            max_vibration = st.slider(
                "Maximum Vibration",
                min_value=0.0,
                max_value=1.0,
                value=0.8,
                step=0.05
            )
            
            max_wear_rate = st.slider(
                "Maximum Bit Wear Rate (/hr)",
                min_value=0.0,
                max_value=0.2,
                value=0.08,
                step=0.01
            )
        
        st.subheader("Model Configuration")
        
        physics_weight = st.slider(
            "Physics Model Weight (vs ML)",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.05,
            help="Weight given to physics-based predictions vs ML predictions"
        )
        
        st.info(f"ML Model Weight: {1.0 - physics_weight:.2f}")
        
        st.subheader("Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Generate Training Data"):
                with st.spinner("Generating synthetic training data..."):
                    data = self.data_generator.generate_complete_dataset(1000)
                    filepath = 'data/synthetic/training_data.csv'
                    self.data_generator.save_dataset(data, filepath)
                    st.success(f"Generated 1000 samples and saved to {filepath}")
        
        with col2:
            if st.button("🔄 Reset System"):
                self._initialize_session_state()
                self.digital_twin.reset_history()
                st.success("System reset successfully!")
                st.rerun()
        
        st.subheader("About")
        
        st.markdown("""
        **AI-Driven Autonomous Drilling Optimization System**
        
        Version: 1.0.0
        
        This system combines:
        - Physics-based drilling models (mechanics & hydraulics)
        - Machine learning risk prediction
        - Hybrid digital twin technology
        - Real-time optimization algorithms
        - Sustainability metrics
        
        Developed for autonomous drilling optimization with focus on safety and efficiency.
        """)


def main():
    """Main entry point for the dashboard."""
    dashboard = DrillingDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
