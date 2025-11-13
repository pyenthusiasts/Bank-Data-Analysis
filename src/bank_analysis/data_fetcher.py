"""
Data fetcher module for downloading banking stock data.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BankDataFetcher:
    """
    Fetches stock data for banking institutions using Yahoo Finance API.

    Attributes:
        tickers (List[str]): List of stock ticker symbols
        start_date (str): Start date for data retrieval (YYYY-MM-DD)
        end_date (str): End date for data retrieval (YYYY-MM-DD)
    """

    DEFAULT_TICKERS = ['JPM', 'BAC', 'C', 'WFC', 'GS']

    def __init__(
        self,
        tickers: Optional[List[str]] = None,
        start_date: str = '2020-01-01',
        end_date: Optional[str] = None
    ):
        """
        Initialize the BankDataFetcher.

        Args:
            tickers: List of bank ticker symbols. Defaults to major US banks.
            start_date: Start date for data retrieval. Defaults to '2020-01-01'.
            end_date: End date for data retrieval. Defaults to today.
        """
        self.tickers = tickers or self.DEFAULT_TICKERS
        self.start_date = start_date
        self.end_date = end_date or datetime.today().strftime('%Y-%m-%d')
        self.data = None

    def fetch_data(self, price_type: str = 'Adj Close') -> pd.DataFrame:
        """
        Fetch stock data from Yahoo Finance.

        Args:
            price_type: Type of price data to fetch ('Adj Close', 'Close', 'Open', etc.)

        Returns:
            DataFrame containing the requested price data

        Raises:
            ValueError: If no data is retrieved
        """
        logger.info(f"Fetching {price_type} data for {self.tickers}")
        logger.info(f"Date range: {self.start_date} to {self.end_date}")

        try:
            data = yf.download(
                self.tickers,
                start=self.start_date,
                end=self.end_date,
                progress=False
            )

            if isinstance(data.columns, pd.MultiIndex):
                self.data = data[price_type]
            else:
                self.data = data

            if self.data.empty:
                raise ValueError("No data retrieved from Yahoo Finance")

            logger.info(f"Successfully fetched {len(self.data)} rows of data")
            return self.data

        except Exception as e:
            logger.error(f"Error fetching data: {str(e)}")
            raise

    def get_ticker_info(self, ticker: str) -> dict:
        """
        Get detailed information about a specific ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary containing ticker information
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'website': info.get('website', 'N/A')
            }
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {str(e)}")
            return {}

    def save_data(self, filepath: str, format: str = 'csv') -> None:
        """
        Save fetched data to a file.

        Args:
            filepath: Path where to save the data
            format: File format ('csv' or 'parquet')
        """
        if self.data is None:
            raise ValueError("No data to save. Call fetch_data() first.")

        if format == 'csv':
            self.data.to_csv(filepath)
        elif format == 'parquet':
            self.data.to_parquet(filepath)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Data saved to {filepath}")
