"""
Pytest configuration and shared fixtures.
"""

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_stock_data():
    """
    Create sample stock data for testing.

    Returns a DataFrame with 3 stocks over 100 days.
    """
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=100, freq='D')

    data = pd.DataFrame({
        'JPM': np.cumsum(np.random.randn(100)) + 100,
        'BAC': np.cumsum(np.random.randn(100)) + 50,
        'C': np.cumsum(np.random.randn(100)) + 75
    }, index=dates)

    # Ensure positive prices
    data = data.abs() + 50

    return data


@pytest.fixture
def sample_returns():
    """
    Create sample returns data for testing.

    Returns a DataFrame with returns for 3 stocks over 99 days.
    """
    np.random.seed(42)
    dates = pd.date_range('2020-01-02', periods=99, freq='D')

    returns = pd.DataFrame({
        'JPM': np.random.randn(99) * 0.02,
        'BAC': np.random.randn(99) * 0.025,
        'C': np.random.randn(99) * 0.03
    }, index=dates)

    return returns


@pytest.fixture
def sample_config():
    """
    Create sample configuration dictionary.
    """
    return {
        'tickers': ['JPM', 'BAC', 'C', 'WFC', 'GS'],
        'date_range': {
            'start': '2020-01-01',
            'end': None
        },
        'analysis': {
            'price_type': 'Adj Close',
            'returns_method': 'pct_change',
            'volatility_window': 30,
            'risk_free_rate': 0.02,
            'trading_days_per_year': 252
        },
        'visualization': {
            'style': 'whitegrid',
            'default_figsize': [14, 7],
            'dpi': 300
        }
    }
