"""
Main training script for the AI Drilling Optimization System.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data.data_collector import DrillingDataCollector
from src.models.hybrid_twin import HybridDigitalTwin
from src.utils import setup_logger, load_config, ensure_dir

logger = setup_logger(__name__, 'logs/training.log')


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description='Train AI Drilling Optimization Models')
    parser.add_argument('--samples', type=int, default=1000,
                       help='Number of training samples to generate')
    parser.add_argument('--output-dir', type=str, default='models',
                       help='Directory to save trained models')
    parser.add_argument('--config', type=str, default=None,
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("AI Drilling Optimization System - Model Training")
    logger.info("=" * 60)
    
    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        config = load_config()
    
    logger.info(f"Loaded configuration")
    
    # Initialize components
    logger.info("Initializing components...")
    data_collector = DrillingDataCollector()
    digital_twin = HybridDigitalTwin(config)
    
    # Generate training data
    logger.info(f"Generating {args.samples} training samples...")
    training_data = data_collector.generate_sample_data(args.samples)
    logger.info(f"Training data shape: {training_data.shape}")
    
    # Save sample data
    ensure_dir('data')
    training_data.to_csv('data/training_data.csv', index=False)
    logger.info("Saved training data to data/training_data.csv")
    
    # Preprocess data
    logger.info("Preprocessing data...")
    X_train, y_targets, scaler = data_collector.preprocess_data(training_data)
    logger.info(f"Features shape: {X_train.shape}")
    
    # Train models
    logger.info("Training hybrid digital twin models...")
    digital_twin.train_ml_component(X_train, y_targets, scaler)
    
    # Save models
    ensure_dir(args.output_dir)
    logger.info(f"Saving models to {args.output_dir}...")
    digital_twin.save_models(args.output_dir)
    
    logger.info("=" * 60)
    logger.info("Training completed successfully!")
    logger.info("=" * 60)
    logger.info(f"Models saved to: {args.output_dir}")
    logger.info(f"Training data saved to: data/training_data.csv")
    logger.info("")
    logger.info("Next steps:")
    logger.info("  1. Run the dashboard: streamlit run src/dashboard/app.py")
    logger.info("  2. Or use the models in your own scripts")


if __name__ == "__main__":
    main()
