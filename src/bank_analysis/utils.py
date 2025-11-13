"""
Utility functions for the bank analysis package.
"""

import pandas as pd
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        raise


def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None) -> None:
    """
    Setup logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')

    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    logger.info(f"Logging configured at {log_level} level")


def validate_data(data: pd.DataFrame, required_columns: Optional[list] = None) -> bool:
    """
    Validate DataFrame structure and content.

    Args:
        data: DataFrame to validate
        required_columns: Optional list of required column names

    Returns:
        True if valid, raises ValueError otherwise
    """
    if data.empty:
        raise ValueError("DataFrame is empty")

    if required_columns:
        missing_cols = set(required_columns) - set(data.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

    if data.isnull().all().any():
        raise ValueError("DataFrame contains columns with all NaN values")

    logger.info("Data validation passed")
    return True


def create_directory_structure(base_path: str) -> None:
    """
    Create standard directory structure for the project.

    Args:
        base_path: Base path for the project
    """
    directories = [
        'data/raw',
        'data/processed',
        'output/plots',
        'output/reports',
        'logs'
    ]

    for directory in directories:
        path = Path(base_path) / directory
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {path}")


def format_currency(value: float, currency: str = 'USD') -> str:
    """
    Format number as currency.

    Args:
        value: Numeric value to format
        currency: Currency code (default: USD)

    Returns:
        Formatted currency string
    """
    if currency == 'USD':
        return f"${value:,.2f}"
    else:
        return f"{value:,.2f} {currency}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format number as percentage.

    Args:
        value: Numeric value to format (e.g., 0.05 for 5%)
        decimals: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def get_date_range_description(start_date: str, end_date: str) -> str:
    """
    Create a human-readable description of a date range.

    Args:
        start_date: Start date string
        end_date: End date string

    Returns:
        Description string
    """
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    days = (end - start).days

    return f"{start.strftime('%B %d, %Y')} to {end.strftime('%B %d, %Y')} ({days} days)"
