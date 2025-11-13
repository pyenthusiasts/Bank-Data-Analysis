"""
Unit tests for the analyzer module.
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bank_analysis.analyzer import BankAnalyzer


@pytest.fixture
def sample_price_data():
    """Create sample price data for testing."""
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    data = pd.DataFrame({
        'STOCK_A': np.random.uniform(90, 110, 100),
        'STOCK_B': np.random.uniform(45, 55, 100),
        'STOCK_C': np.random.uniform(190, 210, 100)
    }, index=dates)
    return data


class TestBankAnalyzer:
    """Test cases for BankAnalyzer class."""

    def test_initialization(self, sample_price_data):
        """Test analyzer initialization."""
        analyzer = BankAnalyzer(sample_price_data)

        assert analyzer.data is not None
        assert analyzer.returns is None
        assert len(analyzer.data) == len(sample_price_data)

    def test_calculate_returns_pct_change(self, sample_price_data):
        """Test returns calculation using pct_change method."""
        analyzer = BankAnalyzer(sample_price_data)
        returns = analyzer.calculate_returns(method='pct_change')

        assert isinstance(returns, pd.DataFrame)
        assert len(returns) == len(sample_price_data) - 1  # One row lost to pct_change
        assert returns.columns.equals(sample_price_data.columns)
        assert analyzer.returns is not None

    def test_calculate_returns_log(self, sample_price_data):
        """Test returns calculation using log method."""
        analyzer = BankAnalyzer(sample_price_data)
        returns = analyzer.calculate_returns(method='log')

        assert isinstance(returns, pd.DataFrame)
        assert len(returns) == len(sample_price_data) - 1
        assert returns.columns.equals(sample_price_data.columns)

    def test_calculate_returns_invalid_method(self, sample_price_data):
        """Test that invalid method raises ValueError."""
        analyzer = BankAnalyzer(sample_price_data)

        with pytest.raises(ValueError):
            analyzer.calculate_returns(method='invalid_method')

    def test_get_correlation_matrix(self, sample_price_data):
        """Test correlation matrix calculation."""
        analyzer = BankAnalyzer(sample_price_data)
        analyzer.calculate_returns()
        corr_matrix = analyzer.get_correlation_matrix()

        assert isinstance(corr_matrix, pd.DataFrame)
        assert corr_matrix.shape == (3, 3)  # 3x3 for 3 stocks
        # Diagonal should be 1.0
        np.testing.assert_array_almost_equal(np.diag(corr_matrix), np.ones(3))
        # Matrix should be symmetric
        np.testing.assert_array_almost_equal(corr_matrix, corr_matrix.T)

    def test_get_correlation_matrix_without_returns(self, sample_price_data):
        """Test that correlation calculation fails without returns."""
        analyzer = BankAnalyzer(sample_price_data)

        with pytest.raises(ValueError):
            analyzer.get_correlation_matrix()

    def test_get_summary_statistics(self, sample_price_data):
        """Test summary statistics calculation."""
        analyzer = BankAnalyzer(sample_price_data)
        analyzer.calculate_returns()
        summary = analyzer.get_summary_statistics()

        assert isinstance(summary, pd.DataFrame)
        assert 'mean' in summary.index
        assert 'std' in summary.index
        assert 'min' in summary.index
        assert 'max' in summary.index
        assert len(summary.columns) == 3  # 3 stocks

    def test_calculate_volatility(self, sample_price_data):
        """Test volatility calculation."""
        analyzer = BankAnalyzer(sample_price_data)
        analyzer.calculate_returns()
        volatility = analyzer.calculate_volatility(window=10)

        assert isinstance(volatility, pd.DataFrame)
        assert volatility.shape[1] == sample_price_data.shape[1]

    def test_calculate_cumulative_returns(self, sample_price_data):
        """Test cumulative returns calculation."""
        analyzer = BankAnalyzer(sample_price_data)
        analyzer.calculate_returns()
        cum_returns = analyzer.calculate_cumulative_returns()

        assert isinstance(cum_returns, pd.DataFrame)
        assert cum_returns.shape == analyzer.returns.shape
        # First cumulative return should be close to first return
        np.testing.assert_array_almost_equal(
            cum_returns.iloc[0].values,
            analyzer.returns.iloc[0].values,
            decimal=4
        )

    def test_calculate_sharpe_ratio(self, sample_price_data):
        """Test Sharpe ratio calculation."""
        analyzer = BankAnalyzer(sample_price_data)
        analyzer.calculate_returns()
        sharpe = analyzer.calculate_sharpe_ratio(risk_free_rate=0.02)

        assert isinstance(sharpe, pd.Series)
        assert len(sharpe) == 3  # 3 stocks
        # Sharpe ratio should be finite numbers
        assert all(np.isfinite(sharpe))

    def test_get_price_statistics(self, sample_price_data):
        """Test price statistics calculation."""
        analyzer = BankAnalyzer(sample_price_data)
        stats = analyzer.get_price_statistics()

        assert 'current_price' in stats
        assert 'min_price' in stats
        assert 'max_price' in stats
        assert 'mean_price' in stats
        assert 'price_range' in stats
        assert 'percent_change' in stats

        # Verify some logical relationships
        assert all(stats['min_price'] <= stats['max_price'])
        assert all(stats['price_range'] == stats['max_price'] - stats['min_price'])

    def test_find_best_worst_performers(self, sample_price_data):
        """Test finding best and worst performers."""
        analyzer = BankAnalyzer(sample_price_data)
        analyzer.calculate_returns()
        best, worst = analyzer.find_best_worst_performers()

        assert isinstance(best, str)
        assert isinstance(worst, str)
        assert best in sample_price_data.columns
        assert worst in sample_price_data.columns

    def test_empty_dataframe(self):
        """Test behavior with empty DataFrame."""
        empty_df = pd.DataFrame()
        analyzer = BankAnalyzer(empty_df)

        # Should handle empty data gracefully or raise appropriate error
        assert analyzer.data.empty

    def test_returns_persistence(self, sample_price_data):
        """Test that calculated returns persist in the object."""
        analyzer = BankAnalyzer(sample_price_data)

        assert analyzer.returns is None

        returns1 = analyzer.calculate_returns()
        returns2 = analyzer.returns

        pd.testing.assert_frame_equal(returns1, returns2)
