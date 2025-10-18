"""
Interactive Streamlit Dashboard for AI Drilling Optimization System.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.data_collector import DrillingDataCollector
from src.models.hybrid_twin import HybridDigitalTwin
from src.optimization.optimizer import AutonomousOptimizer
from src.utils import load_config, setup_logger

logger = setup_logger(__name__)

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
    </style>
    """, unsafe_allow_html=True)


class DrillingDashboard:
    """
    Main dashboard class for drilling optimization system.
    """
    
    def __init__(self):
        """Initialize dashboard components."""
        self.config = load_config()
        self.data_collector = DrillingDataCollector()
        self.digital_twin = HybridDigitalTwin(self.config)
        self.optimizer = AutonomousOptimizer(self.config)
        
        # Initialize session state
        if 'data_history' not in st.session_state:
            st.session_state.data_history = []
        if 'risk_history' not in st.session_state:
            st.session_state.risk_history = []
        if 'trained' not in st.session_state:
            st.session_state.trained = False
    
    def train_models(self):
        """Train ML models on sample data."""
        if not st.session_state.trained:
            with st.spinner("Training ML models... This may take a minute."):
                # Generate training data
                training_data = self.data_collector.generate_sample_data(1000)
                X_train, y_targets, scaler = self.data_collector.preprocess_data(training_data)
                
                # Train models
                self.digital_twin.train_ml_component(X_train, y_targets, scaler)
                
                st.session_state.trained = True
                logger.info("Models trained successfully")
    
    def render_header(self):
        """Render dashboard header."""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.title("🛢️ AI Drilling Optimization System")
            st.markdown("*Real-time autonomous drilling optimization with hybrid digital twin*")
        
        with col2:
            if st.button("🔄 Train Models", use_container_width=True):
                self.train_models()
                st.success("✅ Models trained!")
        
        with col3:
            status = "🟢 Trained" if st.session_state.trained else "🔴 Not Trained"
            st.metric("Model Status", status)
    
    def render_sidebar(self):
        """Render sidebar with controls."""
        st.sidebar.header("⚙️ Controls")
        
        # Mode selection
        mode = st.sidebar.radio(
            "Operation Mode",
            ["Real-time Simulation", "Historical Analysis"]
        )
        
        st.sidebar.markdown("---")
        
        # Manual parameter inputs
        st.sidebar.subheader("Manual Parameters")
        wob = st.sidebar.slider("Weight on Bit (klbs)", 10.0, 40.0, 25.0)
        rpm = st.sidebar.slider("Rotary Speed (RPM)", 60, 180, 120)
        flow_rate = st.sidebar.slider("Flow Rate (gpm)", 300, 700, 500)
        mud_weight = st.sidebar.slider("Mud Weight (ppg)", 8.5, 16.0, 12.0)
        
        st.sidebar.markdown("---")
        
        # Sustainability settings
        st.sidebar.subheader("🌱 Sustainability")
        optimize_sustainability = st.sidebar.checkbox("Enable Sustainability Optimization", value=True)
        
        return mode, {
            'wob': wob,
            'rpm': rpm,
            'flow_rate': flow_rate,
            'mud_weight': mud_weight
        }, optimize_sustainability
    
    def render_realtime_metrics(self, current_data, risks):
        """Render real-time metrics."""
        st.subheader("📊 Real-time Drilling Metrics")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Depth (ft)", f"{current_data['depth']:.1f}", 
                     delta=f"{np.random.uniform(-2, 2):.1f} ft/hr")
        
        with col2:
            st.metric("ROP (ft/hr)", f"{current_data['rop']:.1f}",
                     delta=f"{np.random.uniform(-5, 5):.1f}")
        
        with col3:
            st.metric("WOB (klbs)", f"{current_data['wob']:.1f}")
        
        with col4:
            st.metric("RPM", f"{current_data['rpm']:.0f}")
        
        with col5:
            st.metric("Torque (klb-ft)", f"{current_data['torque']:.1f}")
    
    def render_risk_indicators(self, risks):
        """Render risk indicators."""
        st.subheader("⚠️ Risk Assessment")
        
        col1, col2, col3 = st.columns(3)
        
        def get_risk_color(risk_value):
            if risk_value < 0.3:
                return "🟢"
            elif risk_value < 0.6:
                return "🟡"
            else:
                return "🔴"
        
        with col1:
            risk_val = risks['wellbore_instability']
            st.metric(
                "Wellbore Instability",
                f"{get_risk_color(risk_val)} {risk_val*100:.1f}%"
            )
            st.progress(min(1.0, risk_val))
        
        with col2:
            risk_val = risks['stuck_pipe']
            st.metric(
                "Stuck Pipe Risk",
                f"{get_risk_color(risk_val)} {risk_val*100:.1f}%"
            )
            st.progress(min(1.0, risk_val))
        
        with col3:
            risk_val = risks['kick_risk']
            st.metric(
                "Kick Risk",
                f"{get_risk_color(risk_val)} {risk_val*100:.1f}%"
            )
            st.progress(min(1.0, risk_val))
    
    def render_recommendations(self, recommendations):
        """Render optimization recommendations."""
        st.subheader("💡 Optimization Recommendations")
        
        if recommendations:
            for rec in recommendations[:5]:  # Show top 5
                severity_icon = "🔴" if rec['severity'] == "CRITICAL" else "🟡" if rec['severity'] == "HIGH" else "🟢"
                st.info(f"{severity_icon} **{rec['risk_type']}**: {rec['action']}")
        else:
            st.success("✅ All parameters optimal. No immediate actions required.")
    
    def render_charts(self):
        """Render data visualization charts."""
        st.subheader("📈 Real-time Monitoring")
        
        if len(st.session_state.data_history) > 1:
            df = pd.DataFrame(st.session_state.data_history)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # ROP and Depth chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(len(df))),
                    y=df['rop'],
                    name='ROP (ft/hr)',
                    line=dict(color='blue')
                ))
                fig.update_layout(
                    title="Rate of Penetration",
                    xaxis_title="Time",
                    yaxis_title="ROP (ft/hr)",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Risk trends
                if st.session_state.risk_history:
                    risk_df = pd.DataFrame(st.session_state.risk_history)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=list(range(len(risk_df))),
                        y=risk_df['wellbore_instability'],
                        name='Wellbore Instability',
                        line=dict(color='red')
                    ))
                    fig.add_trace(go.Scatter(
                        x=list(range(len(risk_df))),
                        y=risk_df['stuck_pipe'],
                        name='Stuck Pipe',
                        line=dict(color='orange')
                    ))
                    fig.add_trace(go.Scatter(
                        x=list(range(len(risk_df))),
                        y=risk_df['kick_risk'],
                        name='Kick Risk',
                        line=dict(color='purple')
                    ))
                    fig.update_layout(
                        title="Risk Trends",
                        xaxis_title="Time",
                        yaxis_title="Risk Level",
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    def render_sustainability_metrics(self, current_data):
        """Render sustainability metrics."""
        st.subheader("🌱 Sustainability Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate metrics
        fuel_consumption = current_data.get('wob', 25) * current_data.get('rpm', 120) * 0.001 + 5
        co2_emissions = fuel_consumption * 2.68
        
        with col1:
            st.metric("Fuel Consumption", f"{fuel_consumption:.2f} gal/hr")
        
        with col2:
            st.metric("CO2 Emissions", f"{co2_emissions:.2f} kg/hr")
        
        with col3:
            target_reduction = self.config.get('sustainability', {}).get('target_fuel_reduction', 15)
            st.metric("Target Reduction", f"{target_reduction}%")
        
        with col4:
            efficiency = self.optimizer.calculate_efficiency_score(current_data, 
                                                                   st.session_state.get('current_risks', {}))
            st.metric("Efficiency Score", f"{efficiency:.1f}/100")
    
    def run(self):
        """Run the dashboard."""
        self.render_header()
        
        mode, manual_params, optimize_sustainability = self.render_sidebar()
        
        st.markdown("---")
        
        if mode == "Real-time Simulation":
            # Real-time mode
            placeholder = st.empty()
            
            while True:
                with placeholder.container():
                    # Collect current data
                    current_data = self.data_collector.collect_realtime_data()
                    current_data.update(manual_params)
                    
                    # Predict risks
                    risks = self.digital_twin.predict_risks(
                        current_data,
                        use_ml=st.session_state.trained
                    )
                    
                    # Get recommendations
                    recommendations = self.digital_twin.get_recommendations(risks, current_data)
                    
                    # Optimize parameters
                    if optimize_sustainability:
                        optimized, sustainability_metrics = self.optimizer.optimize_for_sustainability(current_data)
                    else:
                        optimized, adjustments = self.optimizer.optimize_parameters(
                            current_data, risks, recommendations
                        )
                    
                    # Update history
                    st.session_state.data_history.append(current_data)
                    st.session_state.risk_history.append(risks)
                    st.session_state.current_risks = risks
                    
                    # Keep only last 100 points
                    if len(st.session_state.data_history) > 100:
                        st.session_state.data_history.pop(0)
                        st.session_state.risk_history.pop(0)
                    
                    # Render components
                    self.render_realtime_metrics(current_data, risks)
                    st.markdown("---")
                    self.render_risk_indicators(risks)
                    st.markdown("---")
                    self.render_recommendations(recommendations)
                    st.markdown("---")
                    self.render_charts()
                    st.markdown("---")
                    self.render_sustainability_metrics(current_data)
                
                time.sleep(self.config.get('dashboard', {}).get('refresh_rate', 2))
        
        else:
            # Historical analysis mode
            st.info("📊 Historical Analysis Mode - Generate and analyze historical data")
            
            if st.button("Generate Historical Data"):
                with st.spinner("Generating historical data..."):
                    historical_data = self.data_collector.generate_sample_data(500)
                    st.session_state.historical_data = historical_data
                    st.success("✅ Historical data generated!")
            
            if 'historical_data' in st.session_state:
                data = st.session_state.historical_data
                
                # Display summary statistics
                st.subheader("Summary Statistics")
                st.dataframe(data.describe())
                
                # Display charts
                st.subheader("Historical Trends")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.line(data, x='depth', y='rop', title='ROP vs Depth')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.scatter(data, x='wob', y='rop', color='depth', title='WOB vs ROP')
                    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main function to run dashboard."""
    dashboard = DrillingDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
