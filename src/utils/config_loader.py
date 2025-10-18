"""
Configuration loader utility for the AI Drilling Optimization System.
"""
import yaml
import os
from pathlib import Path


def load_config(config_path=None):
    """
    Load configuration from YAML file.
    
    Args:
        config_path (str, optional): Path to config file. If None, uses default.
        
    Returns:
        dict: Configuration dictionary
    """
    if config_path is None:
        # Go up to project root and find config
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def get_data_path(filename=None):
    """
    Get path to data directory or specific file.
    
    Args:
        filename (str, optional): Specific filename to get path for.
        
    Returns:
        Path: Path object for data directory or file
    """
    data_dir = Path(__file__).parent.parent.parent / "data"
    
    if filename:
        return data_dir / filename
    return data_dir


def ensure_dir(directory):
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory (str or Path): Directory path
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
