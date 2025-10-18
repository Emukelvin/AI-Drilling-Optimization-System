"""
Machine Learning models for drilling risk prediction.
Implements neural networks and ensemble models for risk assessment.
"""
import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from src.utils import setup_logger, load_config, ensure_dir

logger = setup_logger(__name__)


class MLRiskPredictor:
    """
    Machine Learning based risk predictor for drilling operations.
    """
    
    def __init__(self, config=None):
        """
        Initialize ML risk predictor.
        
        Args:
            config (dict, optional): Configuration parameters
        """
        if config is None:
            config = load_config()
        
        self.config = config.get('model', {})
        self.learning_rate = self.config.get('learning_rate', 0.001)
        self.epochs = self.config.get('epochs', 100)
        self.batch_size = self.config.get('batch_size', 32)
        self.validation_split = self.config.get('validation_split', 0.2)
        
        self.models = {
            'wellbore_instability': None,
            'stuck_pipe': None,
            'kick_risk': None
        }
        
        self.rf_models = {
            'wellbore_instability': RandomForestClassifier(n_estimators=100, random_state=42),
            'stuck_pipe': RandomForestClassifier(n_estimators=100, random_state=42),
            'kick_risk': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        self.scaler = None
        
        logger.info("MLRiskPredictor initialized")
    
    def build_neural_network(self, input_shape):
        """
        Build neural network model for risk prediction.
        
        Args:
            input_shape (tuple): Shape of input features
            
        Returns:
            keras.Model: Compiled neural network model
        """
        model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(input_shape,)),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='binary_crossentropy',
            metrics=['accuracy', 'AUC']
        )
        
        return model
    
    def train(self, X_train, y_targets, scaler=None):
        """
        Train ML models on drilling data.
        
        Args:
            X_train (np.ndarray): Training features
            y_targets (tuple): Tuple of target arrays (wellbore, stuck_pipe, kick)
            scaler: Feature scaler
        """
        logger.info("Starting model training")
        
        self.scaler = scaler
        y_wellbore, y_stuck_pipe, y_kick = y_targets
        
        # Convert to binary classification
        y_wellbore_binary = (y_wellbore > 0.5).astype(int)
        y_stuck_pipe_binary = (y_stuck_pipe > 0.5).astype(int)
        y_kick_binary = (y_kick > 0.5).astype(int)
        
        # Train neural networks
        logger.info("Training wellbore instability model")
        self.models['wellbore_instability'] = self.build_neural_network(X_train.shape[1])
        self.models['wellbore_instability'].fit(
            X_train, y_wellbore_binary,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=self.validation_split,
            verbose=0
        )
        
        logger.info("Training stuck pipe model")
        self.models['stuck_pipe'] = self.build_neural_network(X_train.shape[1])
        self.models['stuck_pipe'].fit(
            X_train, y_stuck_pipe_binary,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=self.validation_split,
            verbose=0
        )
        
        logger.info("Training kick risk model")
        self.models['kick_risk'] = self.build_neural_network(X_train.shape[1])
        self.models['kick_risk'].fit(
            X_train, y_kick_binary,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=self.validation_split,
            verbose=0
        )
        
        # Train Random Forest models for ensemble
        logger.info("Training Random Forest ensemble models")
        self.rf_models['wellbore_instability'].fit(X_train, y_wellbore_binary)
        self.rf_models['stuck_pipe'].fit(X_train, y_stuck_pipe_binary)
        self.rf_models['kick_risk'].fit(X_train, y_kick_binary)
        
        logger.info("Model training complete")
    
    def predict(self, X):
        """
        Predict risks using trained models.
        
        Args:
            X (np.ndarray): Feature array
            
        Returns:
            dict: Risk predictions
        """
        if self.scaler is not None:
            X = self.scaler.transform(X)
        
        # Get predictions from both neural network and random forest
        nn_pred_wellbore = self.models['wellbore_instability'].predict(X, verbose=0).flatten()
        nn_pred_stuck = self.models['stuck_pipe'].predict(X, verbose=0).flatten()
        nn_pred_kick = self.models['kick_risk'].predict(X, verbose=0).flatten()
        
        rf_pred_wellbore = self.rf_models['wellbore_instability'].predict_proba(X)[:, 1]
        rf_pred_stuck = self.rf_models['stuck_pipe'].predict_proba(X)[:, 1]
        rf_pred_kick = self.rf_models['kick_risk'].predict_proba(X)[:, 1]
        
        # Ensemble predictions (average)
        predictions = {
            'wellbore_instability': (nn_pred_wellbore + rf_pred_wellbore) / 2,
            'stuck_pipe': (nn_pred_stuck + rf_pred_stuck) / 2,
            'kick_risk': (nn_pred_kick + rf_pred_kick) / 2
        }
        
        return predictions
    
    def save_models(self, save_dir):
        """
        Save trained models to disk.
        
        Args:
            save_dir (str): Directory to save models
        """
        save_path = Path(save_dir)
        ensure_dir(save_path)
        
        logger.info(f"Saving models to {save_path}")
        
        # Save neural network models
        for name, model in self.models.items():
            if model is not None:
                model.save(save_path / f"{name}_nn.h5")
        
        # Save Random Forest models
        for name, model in self.rf_models.items():
            joblib.dump(model, save_path / f"{name}_rf.pkl")
        
        # Save scaler
        if self.scaler is not None:
            joblib.dump(self.scaler, save_path / "scaler.pkl")
        
        logger.info("Models saved successfully")
    
    def load_models(self, load_dir):
        """
        Load trained models from disk.
        
        Args:
            load_dir (str): Directory containing saved models
        """
        load_path = Path(load_dir)
        
        logger.info(f"Loading models from {load_path}")
        
        # Load neural network models
        for name in self.models.keys():
            model_path = load_path / f"{name}_nn.h5"
            if model_path.exists():
                self.models[name] = keras.models.load_model(model_path)
        
        # Load Random Forest models
        for name in self.rf_models.keys():
            model_path = load_path / f"{name}_rf.pkl"
            if model_path.exists():
                self.rf_models[name] = joblib.load(model_path)
        
        # Load scaler
        scaler_path = load_path / "scaler.pkl"
        if scaler_path.exists():
            self.scaler = joblib.load(scaler_path)
        
        logger.info("Models loaded successfully")
