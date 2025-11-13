# 🏦 Bank Data Analysis

A comprehensive Python toolkit for analyzing banking stock performance with advanced metrics, visualizations, and risk analysis.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
  - [Jupyter Notebooks](#jupyter-notebooks)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Data Fetching**: Automated retrieval of banking stock data using Yahoo Finance API
- **Comprehensive Analysis**:
  - Daily, cumulative, and log returns calculation
  - Correlation analysis between stocks
  - Volatility analysis (rolling and historical)
  - Risk-adjusted performance metrics (Sharpe ratio)
  - Price statistics and trends
- **Advanced Visualizations**:
  - Price trend charts
  - Correlation heatmaps
  - Returns distribution plots
  - Cumulative performance tracking
  - Rolling volatility charts
  - Comprehensive dashboards
- **Modular Architecture**: Clean, reusable, and testable code
- **Multiple Interfaces**: CLI, Python API, and Jupyter notebooks
- **Configuration Management**: YAML-based configuration
- **Comprehensive Testing**: Unit tests with pytest
- **Type Hints**: Full type annotation support

## 🚀 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Bank-Data-Analysis.git
cd Bank-Data-Analysis

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Using pip (after publishing to PyPI)

```bash
pip install bank-data-analysis
```

## 🎯 Quick Start

### Command Line

```bash
# Run analysis with default configuration
bank-analysis --config config.yaml

# Analyze specific stocks
bank-analysis --tickers JPM BAC C --start 2020-01-01

# Generate visualizations and save data
bank-analysis --save-data --output-dir results/
```

### Python API

```python
from bank_analysis import BankDataFetcher, BankAnalyzer, BankVisualizer

# Fetch data
fetcher = BankDataFetcher(tickers=['JPM', 'BAC', 'C'], start_date='2020-01-01')
data = fetcher.fetch_data()

# Analyze
analyzer = BankAnalyzer(data)
returns = analyzer.calculate_returns()
sharpe_ratios = analyzer.calculate_sharpe_ratio()

# Visualize
visualizer = BankVisualizer(data, returns)
visualizer.plot_prices()
visualizer.create_dashboard(analyzer)
```

### Jupyter Notebook

```bash
# Launch Jupyter
jupyter notebook

# Open the enhanced analysis notebook
# notebooks/banking_analysis_enhanced.ipynb
```

## 📖 Usage

### Command Line Interface

The package provides a powerful CLI for quick analysis:

```bash
# Full analysis with all features
bank-analysis --config config.yaml --save-data

# Custom date range
bank-analysis --tickers JPM BAC --start 2021-01-01 --end 2023-12-31

# Skip plots (analysis only)
bank-analysis --no-plots --save-data

# Verbose logging
bank-analysis --log-level DEBUG
```

### Python API

#### Data Fetching

```python
from bank_analysis import BankDataFetcher

# Initialize fetcher
fetcher = BankDataFetcher(
    tickers=['JPM', 'BAC', 'C', 'WFC', 'GS'],
    start_date='2020-01-01'
)

# Fetch data
data = fetcher.fetch_data()

# Save data
fetcher.save_data('data/raw/bank_prices.csv')

# Get ticker information
info = fetcher.get_ticker_info('JPM')
```

#### Analysis

```python
from bank_analysis import BankAnalyzer

# Initialize analyzer
analyzer = BankAnalyzer(data)

# Calculate returns
returns = analyzer.calculate_returns(method='pct_change')

# Get correlation matrix
correlation = analyzer.get_correlation_matrix()

# Calculate metrics
volatility = analyzer.calculate_volatility(window=30)
sharpe_ratios = analyzer.calculate_sharpe_ratio(risk_free_rate=0.02)
cumulative_returns = analyzer.calculate_cumulative_returns()

# Find best/worst performers
best, worst = analyzer.find_best_worst_performers()

# Get price statistics
stats = analyzer.get_price_statistics()
```

#### Visualization

```python
from bank_analysis import BankVisualizer

# Initialize visualizer
visualizer = BankVisualizer(data, returns)

# Create individual plots
visualizer.plot_prices(save_path='output/prices.png')
visualizer.plot_correlation_heatmap(correlation, save_path='output/correlation.png')
visualizer.plot_cumulative_returns(cumulative_returns, save_path='output/cumulative.png')
visualizer.plot_volatility(volatility, save_path='output/volatility.png')

# Create comprehensive dashboard
visualizer.create_dashboard(analyzer, save_path='output/dashboard.png')
```

### Jupyter Notebooks

Two notebooks are provided:

1. **banking_analysis_enhanced.ipynb**: Comprehensive analysis with detailed explanations
2. **banking_data_analysis_original.ipynb**: Original simple analysis

## 📁 Project Structure

```
Bank-Data-Analysis/
├── src/
│   └── bank_analysis/
│       ├── __init__.py          # Package initialization
│       ├── data_fetcher.py      # Data fetching module
│       ├── analyzer.py          # Analysis module
│       ├── visualizer.py        # Visualization module
│       ├── utils.py             # Utility functions
│       └── cli.py               # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── test_data_fetcher.py
│   ├── test_analyzer.py
│   └── test_utils.py
├── notebooks/
│   ├── banking_analysis_enhanced.ipynb
│   └── banking_data_analysis_original.ipynb
├── examples/
│   ├── basic_analysis.py        # Basic usage example
│   └── custom_analysis.py       # Advanced usage example
├── docs/
│   ├── API.md                   # API documentation
│   ├── TUTORIAL.md              # Tutorial guide
│   └── FAQ.md                   # Frequently asked questions
├── data/
│   ├── raw/                     # Raw data storage
│   └── processed/               # Processed data storage
├── output/
│   ├── plots/                   # Generated visualizations
│   └── reports/                 # Analysis reports
├── config.yaml                  # Configuration file
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup
├── pyproject.toml              # Build configuration
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # This file
└── CONTRIBUTING.md             # Contribution guidelines
```

## ⚙️ Configuration

The `config.yaml` file controls analysis parameters:

```yaml
# Stock tickers to analyze
tickers:
  - JPM   # JPMorgan Chase
  - BAC   # Bank of America
  - C     # Citigroup
  - WFC   # Wells Fargo
  - GS    # Goldman Sachs

# Date range
date_range:
  start: '2020-01-01'
  end: null  # null means today

# Analysis parameters
analysis:
  price_type: 'Adj Close'
  returns_method: 'pct_change'
  volatility_window: 30
  risk_free_rate: 0.02
  trading_days_per_year: 252

# Visualization settings
visualization:
  style: 'whitegrid'
  default_figsize: [14, 7]
  dpi: 300
```

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- **[API Documentation](docs/API.md)**: Complete API reference
- **[Tutorial](docs/TUTORIAL.md)**: Step-by-step guide
- **[FAQ](docs/FAQ.md)**: Common questions and answers

## 🧪 Testing

Run tests using pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/bank_analysis --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py

# Run with verbose output
pytest -v
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/pyenthusiasts/Bank-Data-Analysis.git
cd Bank-Data-Analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/ examples/

# Type checking
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Data provided by [Yahoo Finance](https://finance.yahoo.com/)
- Built with [yfinance](https://github.com/ranaroussi/yfinance), [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/), and [seaborn](https://seaborn.pydata.org/)

## 📧 Contact

**Python Enthusiasts**

- GitHub: [@pyenthusiasts](https://github.com/pyenthusiasts)
- Issues: [GitHub Issues](https://github.com/pyenthusiasts/Bank-Data-Analysis/issues)

## 🗺️ Roadmap

- [ ] Add more financial institutions (European, Asian banks)
- [ ] Implement portfolio optimization
- [ ] Add fundamental analysis (P/E ratios, earnings, etc.)
- [ ] Machine learning price prediction
- [ ] Real-time data streaming
- [ ] Interactive web dashboard
- [ ] Export to Excel/PDF reports
- [ ] Sector comparison analysis

---

**Made with ❤️ by Python Enthusiasts**
