# API Documentation

Complete reference for the Bank Data Analysis package.

## Table of Contents

- [BankDataFetcher](#bankdatafetcher)
- [BankAnalyzer](#bankanalyzer)
- [BankVisualizer](#bankvisualizer)
- [Utility Functions](#utility-functions)

## BankDataFetcher

Fetches stock data for banking institutions using Yahoo Finance API.

### Class: `BankDataFetcher`

```python
from bank_analysis import BankDataFetcher

fetcher = BankDataFetcher(tickers=None, start_date='2020-01-01', end_date=None)
```

#### Parameters

- **tickers** (`List[str]`, optional): List of stock ticker symbols. Defaults to `['JPM', 'BAC', 'C', 'WFC', 'GS']`
- **start_date** (`str`): Start date for data retrieval in 'YYYY-MM-DD' format. Default: '2020-01-01'
- **end_date** (`str`, optional): End date for data retrieval. Defaults to today

#### Methods

##### `fetch_data(price_type='Adj Close')`

Fetch stock data from Yahoo Finance.

**Parameters:**
- `price_type` (`str`): Type of price data ('Adj Close', 'Close', 'Open', 'High', 'Low')

**Returns:**
- `pd.DataFrame`: DataFrame containing the requested price data

**Example:**
```python
fetcher = BankDataFetcher(tickers=['JPM', 'BAC'])
data = fetcher.fetch_data()
```

##### `get_ticker_info(ticker)`

Get detailed information about a specific ticker.

**Parameters:**
- `ticker` (`str`): Stock ticker symbol

**Returns:**
- `dict`: Dictionary containing ticker information (name, sector, industry, market cap, etc.)

**Example:**
```python
info = fetcher.get_ticker_info('JPM')
print(info['name'])  # 'JPMorgan Chase & Co.'
```

##### `save_data(filepath, format='csv')`

Save fetched data to a file.

**Parameters:**
- `filepath` (`str`): Path where to save the data
- `format` (`str`): File format ('csv' or 'parquet')

**Example:**
```python
fetcher.save_data('data/raw/prices.csv', format='csv')
```

---

## BankAnalyzer

Analyzes banking stock data to compute returns, correlations, and other metrics.

### Class: `BankAnalyzer`

```python
from bank_analysis import BankAnalyzer

analyzer = BankAnalyzer(data)
```

#### Parameters

- **data** (`pd.DataFrame`): DataFrame containing stock price data

#### Methods

##### `calculate_returns(method='pct_change')`

Calculate returns from price data.

**Parameters:**
- `method` (`str`): Method for calculating returns ('pct_change' or 'log')

**Returns:**
- `pd.DataFrame`: DataFrame containing calculated returns

**Example:**
```python
returns = analyzer.calculate_returns(method='pct_change')
```

##### `get_correlation_matrix()`

Compute correlation matrix of returns.

**Returns:**
- `pd.DataFrame`: Correlation matrix

**Raises:**
- `ValueError`: If returns haven't been calculated yet

**Example:**
```python
correlation = analyzer.get_correlation_matrix()
```

##### `get_summary_statistics()`

Get summary statistics for returns.

**Returns:**
- `pd.DataFrame`: DataFrame with summary statistics (mean, std, min, max, etc.)

**Example:**
```python
stats = analyzer.get_summary_statistics()
print(stats)
```

##### `calculate_volatility(window=30)`

Calculate rolling volatility.

**Parameters:**
- `window` (`int`): Rolling window size in days. Default: 30

**Returns:**
- `pd.DataFrame`: DataFrame with rolling volatility

**Example:**
```python
volatility = analyzer.calculate_volatility(window=30)
```

##### `calculate_cumulative_returns()`

Calculate cumulative returns.

**Returns:**
- `pd.DataFrame`: DataFrame with cumulative returns

**Example:**
```python
cum_returns = analyzer.calculate_cumulative_returns()
```

##### `calculate_sharpe_ratio(risk_free_rate=0.02, periods_per_year=252)`

Calculate Sharpe ratio for each stock.

**Parameters:**
- `risk_free_rate` (`float`): Annual risk-free rate. Default: 0.02 (2%)
- `periods_per_year` (`int`): Number of trading periods per year. Default: 252

**Returns:**
- `pd.Series`: Series with Sharpe ratios for each stock

**Example:**
```python
sharpe = analyzer.calculate_sharpe_ratio(risk_free_rate=0.02)
```

##### `get_price_statistics()`

Get various price statistics.

**Returns:**
- `dict`: Dictionary containing price statistics:
  - `current_price`: Current (most recent) price
  - `min_price`: Minimum price in the period
  - `max_price`: Maximum price in the period
  - `mean_price`: Average price
  - `price_range`: Difference between max and min
  - `percent_change`: Percentage change from start to end

**Example:**
```python
stats = analyzer.get_price_statistics()
print(stats['current_price'])
```

##### `find_best_worst_performers()`

Find the best and worst performing stocks.

**Returns:**
- `Tuple[str, str]`: Tuple of (best_performer, worst_performer) ticker symbols

**Example:**
```python
best, worst = analyzer.find_best_worst_performers()
print(f"Best: {best}, Worst: {worst}")
```

---

## BankVisualizer

Creates visualizations for banking stock analysis.

### Class: `BankVisualizer`

```python
from bank_analysis import BankVisualizer

visualizer = BankVisualizer(data, returns=None)
```

#### Parameters

- **data** (`pd.DataFrame`): Stock price data
- **returns** (`pd.DataFrame`, optional): Stock returns data

#### Methods

##### `plot_prices(title, figsize=(14,7), save_path=None)`

Plot stock prices over time.

**Parameters:**
- `title` (`str`): Chart title
- `figsize` (`Tuple[int, int]`): Figure size. Default: (14, 7)
- `save_path` (`str`, optional): Path to save the figure

**Example:**
```python
visualizer.plot_prices(
    title="Bank Stock Prices",
    save_path='output/prices.png'
)
```

##### `plot_correlation_heatmap(correlation_matrix, title, figsize=(10,8), save_path=None)`

Plot correlation heatmap.

**Parameters:**
- `correlation_matrix` (`pd.DataFrame`): Correlation matrix to plot
- `title` (`str`): Chart title
- `figsize` (`Tuple[int, int]`): Figure size. Default: (10, 8)
- `save_path` (`str`, optional): Path to save the figure

**Example:**
```python
visualizer.plot_correlation_heatmap(
    correlation_matrix,
    title="Returns Correlation",
    save_path='output/correlation.png'
)
```

##### `plot_returns_distribution(figsize=(14,10), save_path=None)`

Plot distribution of returns for each stock.

**Parameters:**
- `figsize` (`Tuple[int, int]`): Figure size. Default: (14, 10)
- `save_path` (`str`, optional): Path to save the figure

**Example:**
```python
visualizer.plot_returns_distribution(save_path='output/distribution.png')
```

##### `plot_cumulative_returns(cumulative_returns, title, figsize=(14,7), save_path=None)`

Plot cumulative returns over time.

**Parameters:**
- `cumulative_returns` (`pd.DataFrame`): DataFrame with cumulative returns
- `title` (`str`): Chart title
- `figsize` (`Tuple[int, int]`): Figure size. Default: (14, 7)
- `save_path` (`str`, optional): Path to save the figure

**Example:**
```python
visualizer.plot_cumulative_returns(
    cumulative_returns,
    title="Cumulative Performance",
    save_path='output/cumulative.png'
)
```

##### `plot_volatility(volatility, title, figsize=(14,7), save_path=None)`

Plot rolling volatility over time.

**Parameters:**
- `volatility` (`pd.DataFrame`): DataFrame with volatility data
- `title` (`str`): Chart title
- `figsize` (`Tuple[int, int]`): Figure size. Default: (14, 7)
- `save_path` (`str`, optional): Path to save the figure

**Example:**
```python
visualizer.plot_volatility(
    volatility,
    title="30-Day Volatility",
    save_path='output/volatility.png'
)
```

##### `create_dashboard(analyzer, save_path=None)`

Create a comprehensive dashboard with multiple plots.

**Parameters:**
- `analyzer` (`BankAnalyzer`): BankAnalyzer instance with computed metrics
- `save_path` (`str`, optional): Path to save the figure

**Example:**
```python
visualizer.create_dashboard(
    analyzer,
    save_path='output/dashboard.png'
)
```

---

## Utility Functions

### `load_config(config_path)`

Load configuration from YAML file.

**Parameters:**
- `config_path` (`str`): Path to the configuration file

**Returns:**
- `dict`: Dictionary containing configuration

**Example:**
```python
from bank_analysis.utils import load_config

config = load_config('config.yaml')
tickers = config['tickers']
```

### `validate_data(data, required_columns=None)`

Validate DataFrame structure and content.

**Parameters:**
- `data` (`pd.DataFrame`): DataFrame to validate
- `required_columns` (`list`, optional): List of required column names

**Returns:**
- `bool`: True if valid

**Raises:**
- `ValueError`: If validation fails

**Example:**
```python
from bank_analysis.utils import validate_data

validate_data(data, required_columns=['JPM', 'BAC'])
```

### `format_currency(value, currency='USD')`

Format number as currency.

**Parameters:**
- `value` (`float`): Numeric value to format
- `currency` (`str`): Currency code. Default: 'USD'

**Returns:**
- `str`: Formatted currency string

**Example:**
```python
from bank_analysis.utils import format_currency

print(format_currency(1234.56))  # "$1,234.56"
```

### `format_percentage(value, decimals=2)`

Format number as percentage.

**Parameters:**
- `value` (`float`): Numeric value to format (e.g., 0.05 for 5%)
- `decimals` (`int`): Number of decimal places. Default: 2

**Returns:**
- `str`: Formatted percentage string

**Example:**
```python
from bank_analysis.utils import format_percentage

print(format_percentage(0.1234))  # "12.34%"
```

### `get_date_range_description(start_date, end_date)`

Create a human-readable description of a date range.

**Parameters:**
- `start_date` (`str`): Start date string
- `end_date` (`str`): End date string

**Returns:**
- `str`: Description string

**Example:**
```python
from bank_analysis.utils import get_date_range_description

desc = get_date_range_description('2020-01-01', '2020-12-31')
print(desc)  # "January 01, 2020 to December 31, 2020 (365 days)"
```
