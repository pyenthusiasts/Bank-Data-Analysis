"""
Bank Data Analysis Package

A comprehensive toolkit for analyzing banking stock data.
"""

__version__ = "1.0.0"
__author__ = "Python Enthusiasts"

from .data_fetcher import BankDataFetcher
from .analyzer import BankAnalyzer
from .visualizer import BankVisualizer

__all__ = [
    "BankDataFetcher",
    "BankAnalyzer",
    "BankVisualizer",
]
