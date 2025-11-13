"""
Unit tests for the utils module.
"""

import pytest
import pandas as pd
import yaml
from pathlib import Path
import tempfile
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bank_analysis.utils import (
    load_config,
    validate_data,
    format_currency,
    format_percentage,
    get_date_range_description
)


class TestUtilFunctions:
    """Test cases for utility functions."""

    def test_load_config_valid_file(self):
        """Test loading a valid YAML configuration file."""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_data = {
                'tickers': ['JPM', 'BAC'],
                'start_date': '2020-01-01'
            }
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            config = load_config(temp_path)
            assert config['tickers'] == ['JPM', 'BAC']
            assert config['start_date'] == '2020-01-01'
        finally:
            Path(temp_path).unlink()

    def test_load_config_nonexistent_file(self):
        """Test loading a non-existent configuration file."""
        with pytest.raises(FileNotFoundError):
            load_config('nonexistent_config.yaml')

    def test_validate_data_valid_dataframe(self):
        """Test validation of a valid DataFrame."""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

        assert validate_data(df) is True

    def test_validate_data_empty_dataframe(self):
        """Test validation of an empty DataFrame."""
        df = pd.DataFrame()

        with pytest.raises(ValueError, match="DataFrame is empty"):
            validate_data(df)

    def test_validate_data_missing_required_columns(self):
        """Test validation with missing required columns."""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

        with pytest.raises(ValueError, match="Missing required columns"):
            validate_data(df, required_columns=['A', 'B', 'C'])

    def test_validate_data_all_nan_column(self):
        """Test validation with a column containing all NaN values."""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [None, None, None]
        })

        with pytest.raises(ValueError, match="all NaN values"):
            validate_data(df)

    def test_format_currency_usd(self):
        """Test currency formatting for USD."""
        assert format_currency(1234.56) == "$1,234.56"
        assert format_currency(1000000) == "$1,000,000.00"
        assert format_currency(0) == "$0.00"

    def test_format_currency_other(self):
        """Test currency formatting for other currencies."""
        assert format_currency(1234.56, 'EUR') == "1,234.56 EUR"
        assert format_currency(1000, 'GBP') == "1,000.00 GBP"

    def test_format_percentage_default(self):
        """Test percentage formatting with default decimals."""
        assert format_percentage(0.1234) == "12.34%"
        assert format_percentage(0.5) == "50.00%"
        assert format_percentage(1.0) == "100.00%"
        assert format_percentage(0.0) == "0.00%"

    def test_format_percentage_custom_decimals(self):
        """Test percentage formatting with custom decimal places."""
        assert format_percentage(0.12345, decimals=3) == "12.345%"
        assert format_percentage(0.12345, decimals=1) == "12.3%"
        assert format_percentage(0.12345, decimals=0) == "12%"

    def test_format_percentage_negative(self):
        """Test percentage formatting with negative values."""
        assert format_percentage(-0.05) == "-5.00%"
        assert format_percentage(-1.0) == "-100.00%"

    def test_get_date_range_description(self):
        """Test date range description generation."""
        description = get_date_range_description('2020-01-01', '2020-12-31')

        assert 'January 01, 2020' in description
        assert 'December 31, 2020' in description
        assert '365 days' in description or '366 days' in description  # Leap year

    def test_get_date_range_description_short_range(self):
        """Test date range description for a short period."""
        description = get_date_range_description('2020-01-01', '2020-01-10')

        assert 'January 01, 2020' in description
        assert 'January 10, 2020' in description
        assert '9 days' in description

    def test_get_date_range_description_same_day(self):
        """Test date range description for the same day."""
        description = get_date_range_description('2020-01-01', '2020-01-01')

        assert 'January 01, 2020' in description
        assert '0 days' in description


class TestDataValidation:
    """Additional test cases for data validation."""

    def test_validate_data_with_some_nan(self):
        """Test validation with some (but not all) NaN values."""
        df = pd.DataFrame({
            'A': [1, 2, None],
            'B': [4, 5, 6]
        })

        # Should pass - not all values are NaN
        assert validate_data(df) is True

    def test_validate_data_required_columns_present(self):
        """Test validation when all required columns are present."""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        })

        assert validate_data(df, required_columns=['A', 'B']) is True

    def test_validate_data_single_column(self):
        """Test validation of single-column DataFrame."""
        df = pd.DataFrame({
            'A': [1, 2, 3]
        })

        assert validate_data(df) is True
