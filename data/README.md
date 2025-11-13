# Data Directory

This directory contains data files for the Bank Data Analysis project.

## Directory Structure

```
data/
├── raw/           # Raw data files from data sources
├── processed/     # Cleaned and processed data
└── README.md      # This file
```

## Data Sources

### Raw Data (`raw/`)

Raw data is fetched from Yahoo Finance using the `yfinance` library. This includes:

- **Adjusted Close Prices**: Stock prices adjusted for splits and dividends
- **Trading Volume**: Daily trading volumes
- **Historical Data**: Going back as far as available for each ticker

Files in this directory:
- `bank_prices_YYYY-MM-DD.csv` - Historical price data
- `ticker_info.json` - Metadata about each ticker

### Processed Data (`processed/`)

Processed data includes calculated metrics and analysis results:

- `bank_returns.csv` - Daily returns calculated from prices
- `bank_cumulative_returns.csv` - Cumulative returns over time
- `bank_correlation_matrix.csv` - Correlation matrix of returns
- `bank_volatility.csv` - Rolling volatility metrics
- `bank_statistics.csv` - Summary statistics

## Data Format

### Price Data

CSV files with the following format:

```csv
Date,JPM,BAC,C,WFC,GS
2020-01-02,139.40,35.18,79.98,53.94,230.58
2020-01-03,138.38,35.06,79.40,53.51,228.71
...
```

- **Index**: Date (YYYY-MM-DD)
- **Columns**: Stock ticker symbols
- **Values**: Adjusted close prices in USD

### Returns Data

CSV files with calculated daily returns:

```csv
Date,JPM,BAC,C,WFC,GS
2020-01-03,-0.0073,-0.0034,-0.0072,-0.0080,-0.0081
2020-01-04,0.0045,0.0028,0.0051,0.0037,0.0042
...
```

- **Index**: Date (YYYY-MM-DD)
- **Columns**: Stock ticker symbols
- **Values**: Daily percentage returns (decimal format, e.g., -0.0073 = -0.73%)

## Usage Examples

### Loading Data

```python
import pandas as pd

# Load price data
prices = pd.read_csv('data/raw/bank_prices.csv', index_col='Date', parse_dates=True)

# Load returns data
returns = pd.read_csv('data/processed/bank_returns.csv', index_col='Date', parse_dates=True)

# Load correlation matrix
correlation = pd.read_csv('data/processed/bank_correlation_matrix.csv', index_col=0)
```

### Saving Data

```python
from bank_analysis import BankDataFetcher

# Fetch and save data
fetcher = BankDataFetcher(tickers=['JPM', 'BAC', 'C'])
data = fetcher.fetch_data()
fetcher.save_data('data/raw/bank_prices.csv')
```

## Data Management

### Best Practices

1. **Version Control**: Don't commit large data files to git
2. **Naming Convention**: Use descriptive names with dates
3. **Documentation**: Keep notes on data sources and transformations
4. **Backup**: Regularly backup important analysis results

### Cleaning Up

To remove old data files:

```bash
# Remove files older than 30 days
find data/ -name "*.csv" -mtime +30 -delete
```

### Data Refresh

To refresh data:

```bash
# Using CLI
bank-analysis --save-data --output-dir data/

# Using Python
python -c "
from bank_analysis import BankDataFetcher
fetcher = BankDataFetcher()
data = fetcher.fetch_data()
fetcher.save_data('data/raw/bank_prices.csv')
"
```

## Data Privacy and Security

- All data is publicly available market data
- No personal or proprietary information is stored
- Data is sourced from Yahoo Finance's public API

## Troubleshooting

### Missing Data

If you encounter missing data:

1. Check internet connection
2. Verify ticker symbols are correct
3. Check date range (weekends/holidays have no data)
4. Re-fetch the data

### Corrupted Files

If files appear corrupted:

1. Delete the file
2. Re-run the analysis
3. Check disk space

### Large File Sizes

To reduce file sizes:

- Use parquet format instead of CSV
- Compress with gzip
- Filter to only needed date ranges

```python
# Save as parquet (smaller size)
data.to_parquet('data/raw/bank_prices.parquet')

# Save as compressed CSV
data.to_csv('data/raw/bank_prices.csv.gz', compression='gzip')
```

## Data Update Frequency

Recommended update frequency:

- **Daily Analysis**: Fetch data daily
- **Weekly Analysis**: Fetch data weekly
- **Historical Analysis**: Fetch once, save, and reuse

## Notes

- `.gitignore` is configured to exclude large data files
- Keep processed data for reproducibility
- Document any manual data modifications
- Maintain data lineage (track transformations)
