#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DishDazzle - Utilities Module
Provides logging, configuration, and helper functions
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Base paths
BASE_DIR = Path(os.path.dirname(os.path.dirname(__file__)))
CONFIG_DIR = BASE_DIR / 'config'
CONFIG_FILE = CONFIG_DIR / 'config.json'
LOG_DIR = BASE_DIR / 'logs'

# Default configuration
DEFAULT_CONFIG = {
    "openai_api_key": "",
    "theme": "light",
    "log_level": "INFO",
    "cache_enabled": True,
    "max_cache_size": 100
}


def setup_logging(log_level: Optional[str] = None) -> None:
    """Set up logging configuration
    
    Args:
        log_level: Optional log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create log directory if it doesn't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Get log level from config if not provided
    if log_level is None:
        config = load_config()
        log_level = config.get("log_level", "INFO")
    
    # Convert string to logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure logging
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_DIR / 'dishdazzle.log'),
            logging.StreamHandler()
        ]
    )
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized with level {log_level}")


def load_config() -> Dict[str, Any]:
    """Load configuration from config file
    
    Returns:
        Dictionary containing configuration values
    """
    # Create config directory if it doesn't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # If config file doesn't exist, create it with default values
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        # Ensure all default keys are present
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
        
        return config
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading config: {e}")
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to config file
    
    Args:
        config: Dictionary containing configuration values
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create config directory if it doesn't exist
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        
        logger = logging.getLogger(__name__)
        logger.info("Configuration saved successfully")
        return True
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error saving config: {e}")
        return False


def update_config(key: str, value: Any) -> bool:
    """Update a specific configuration value
    
    Args:
        key: Configuration key to update
        value: New value for the key
        
    Returns:
        True if successful, False otherwise
    """
    try:
        config = load_config()
        config[key] = value
        return save_config(config)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error updating config: {e}")
        return False


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a specific configuration value
    
    Args:
        key: Configuration key to retrieve
        default: Default value if key is not found
        
    Returns:
        The configuration value or default if not found
    """
    config = load_config()
    return config.get(key, default)


def export_recipe_to_json(recipe_data: Dict[str, Any], file_path: str) -> bool:
    """Export a recipe to a JSON file
    
    Args:
        recipe_data: Recipe data to export
        file_path: Path to save the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(recipe_data, f, indent=4)
        
        logger = logging.getLogger(__name__)
        logger.info(f"Recipe exported successfully to {file_path}")
        return True
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error exporting recipe: {e}")
        return False


def import_recipe_from_json(file_path: str) -> Optional[Dict[str, Any]]:
    """Import a recipe from a JSON file
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Recipe data dictionary if successful, None otherwise
    """
    try:
        with open(file_path, 'r') as f:
            recipe_data = json.load(f)
        
        logger = logging.getLogger(__name__)
        logger.info(f"Recipe imported successfully from {file_path}")
        return recipe_data
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error importing recipe: {e}")
        return None


def format_cooking_time(minutes: int) -> str:
    """Format cooking time from minutes to a human-readable string
    
    Args:
        minutes: Cooking time in minutes
        
    Returns:
        Formatted cooking time string (e.g., "1 hour 30 minutes")
    """
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours != 1 else ''} {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"


def get_difficulty_color(difficulty: str) -> str:
    """Get a color for a difficulty level
    
    Args:
        difficulty: Difficulty level (Easy, Medium, Hard)
        
    Returns:
        Hex color code for the difficulty
    """
    difficulty_colors = {
        "Easy": "#4CAF50",  # Green
        "Medium": "#FF9800",  # Orange
        "Hard": "#F44336"  # Red
    }
    
    return difficulty_colors.get(difficulty, "#9E9E9E")  # Default to gray