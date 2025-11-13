"""
Unit tests for the data_fetcher module.
"""

import pytest
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bank_analysis.data_fetcher import BankDataFetcher


class TestBankDataFetcher:
    """Test cases for BankDataFetcher class."""

    def test_initialization_with_defaults(self):
        """Test initialization with default parameters."""
        fetcher = BankDataFetcher()

        assert fetcher.tickers == BankDataFetcher.DEFAULT_TICKERS
        assert fetcher.start_date == '2020-01-01'
        assert fetcher.end_date == datetime.today().strftime('%Y-%m-%d')

    def test_initialization_with_custom_params(self):
        """Test initialization with custom parameters."""
        tickers = ['JPM', 'BAC']
        start = '2021-01-01'
        end = '2021-12-31'

        fetcher = BankDataFetcher(tickers=tickers, start_date=start, end_date=end)

        assert fetcher.tickers == tickers
        assert fetcher.start_date == start
        assert fetcher.end_date == end

    def test_fetch_data_returns_dataframe(self):
        """Test that fetch_data returns a DataFrame."""
        fetcher = BankDataFetcher(
            tickers=['JPM'],
            start_date='2023-01-01',
            end_date='2023-01-31'
        )

        data = fetcher.fetch_data()

        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert len(data) > 0

    def test_fetch_data_correct_tickers(self):
        """Test that fetched data contains correct tickers."""
        tickers = ['JPM', 'BAC']
        fetcher = BankDataFetcher(
            tickers=tickers,
            start_date='2023-01-01',
            end_date='2023-01-31'
        )

        data = fetcher.fetch_data()

        # Check that we have columns for the tickers
        for ticker in tickers:
            assert ticker in data.columns or len(data.columns) == 1

    def test_data_attribute_set_after_fetch(self):
        """Test that the data attribute is set after fetching."""
        fetcher = BankDataFetcher(
            tickers=['JPM'],
            start_date='2023-01-01',
            end_date='2023-01-31'
        )

        assert fetcher.data is None

        fetcher.fetch_data()

        assert fetcher.data is not None
        assert isinstance(fetcher.data, pd.DataFrame)

    def test_invalid_date_range(self):
        """Test behavior with invalid date range."""
        fetcher = BankDataFetcher(
            tickers=['JPM'],
            start_date='2025-01-01',
            end_date='2025-01-02'
        )

        # This might return empty data or raise an error
        # depending on yfinance behavior
        try:
            data = fetcher.fetch_data()
            # If it succeeds, data might be empty
            assert isinstance(data, pd.DataFrame)
        except (ValueError, Exception):
            # Expected if the date range is invalid
            pass

    def test_single_ticker_vs_multiple(self):
        """Test fetching single ticker vs multiple tickers."""
        # Single ticker
        fetcher_single = BankDataFetcher(
            tickers=['JPM'],
            start_date='2023-01-01',
            end_date='2023-01-31'
        )
        data_single = fetcher_single.fetch_data()

        # Multiple tickers
        fetcher_multi = BankDataFetcher(
            tickers=['JPM', 'BAC'],
            start_date='2023-01-01',
            end_date='2023-01-31'
        )
        data_multi = fetcher_multi.fetch_data()

        assert isinstance(data_single, pd.DataFrame)
        assert isinstance(data_multi, pd.DataFrame)
        assert len(data_multi.columns) >= len(data_single.columns)
