"""
Analyzer module for computing financial metrics and statistics.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BankAnalyzer:
    """
    Analyzes banking stock data to compute returns, correlations, and other metrics.

    Attributes:
        data (pd.DataFrame): Stock price data
        returns (pd.DataFrame): Computed returns data
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialize the BankAnalyzer.

        Args:
            data: DataFrame containing stock price data
        """
        self.data = data
        self.returns = None

    def calculate_returns(self, method: str = 'pct_change') -> pd.DataFrame:
        """
        Calculate returns from price data.

        Args:
            method: Method for calculating returns ('pct_change' or 'log')

        Returns:
            DataFrame containing calculated returns
        """
        logger.info(f"Calculating returns using {method} method")

        if method == 'pct_change':
            self.returns = self.data.pct_change().dropna()
        elif method == 'log':
            self.returns = np.log(self.data / self.data.shift(1)).dropna()
        else:
            raise ValueError(f"Unknown method: {method}")

        return self.returns

    def get_correlation_matrix(self) -> pd.DataFrame:
        """
        Compute correlation matrix of returns.

        Returns:
            Correlation matrix

        Raises:
            ValueError: If returns haven't been calculated yet
        """
        if self.returns is None:
            raise ValueError("Calculate returns first using calculate_returns()")

        logger.info("Computing correlation matrix")
        return self.returns.corr()

    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics for returns.

        Returns:
            DataFrame with summary statistics
        """
        if self.returns is None:
            raise ValueError("Calculate returns first using calculate_returns()")

        logger.info("Computing summary statistics")
        return self.returns.describe()

    def calculate_volatility(self, window: int = 30) -> pd.DataFrame:
        """
        Calculate rolling volatility.

        Args:
            window: Rolling window size in days

        Returns:
            DataFrame with rolling volatility
        """
        if self.returns is None:
            raise ValueError("Calculate returns first using calculate_returns()")

        logger.info(f"Calculating {window}-day rolling volatility")
        return self.returns.rolling(window=window).std()

    def calculate_cumulative_returns(self) -> pd.DataFrame:
        """
        Calculate cumulative returns.

        Returns:
            DataFrame with cumulative returns
        """
        if self.returns is None:
            raise ValueError("Calculate returns first using calculate_returns()")

        logger.info("Calculating cumulative returns")
        return (1 + self.returns).cumprod() - 1

    def calculate_sharpe_ratio(
        self,
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> pd.Series:
        """
        Calculate Sharpe ratio for each stock.

        Args:
            risk_free_rate: Annual risk-free rate
            periods_per_year: Number of trading periods per year (252 for daily)

        Returns:
            Series with Sharpe ratios
        """
        if self.returns is None:
            raise ValueError("Calculate returns first using calculate_returns()")

        logger.info("Calculating Sharpe ratios")

        mean_return = self.returns.mean() * periods_per_year
        std_return = self.returns.std() * np.sqrt(periods_per_year)

        sharpe_ratio = (mean_return - risk_free_rate) / std_return
        return sharpe_ratio

    def get_price_statistics(self) -> Dict[str, pd.Series]:
        """
        Get various price statistics.

        Returns:
            Dictionary containing price statistics
        """
        logger.info("Computing price statistics")

        return {
            'current_price': self.data.iloc[-1],
            'min_price': self.data.min(),
            'max_price': self.data.max(),
            'mean_price': self.data.mean(),
            'price_range': self.data.max() - self.data.min(),
            'percent_change': ((self.data.iloc[-1] - self.data.iloc[0]) /
                              self.data.iloc[0] * 100)
        }

    def find_best_worst_performers(self) -> Tuple[str, str]:
        """
        Find the best and worst performing stocks.

        Returns:
            Tuple of (best_performer, worst_performer) ticker symbols
        """
        if self.returns is None:
            raise ValueError("Calculate returns first using calculate_returns()")

        cumulative_returns = self.calculate_cumulative_returns()
        final_returns = cumulative_returns.iloc[-1]

        best = final_returns.idxmax()
        worst = final_returns.idxmin()

        logger.info(f"Best performer: {best} ({final_returns[best]:.2%})")
        logger.info(f"Worst performer: {worst} ({final_returns[worst]:.2%})")

        return best, worst
