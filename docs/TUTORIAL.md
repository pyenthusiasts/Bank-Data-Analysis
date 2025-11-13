# Tutorial: Getting Started with Bank Data Analysis

This tutorial will guide you through using the Bank Data Analysis package to analyze banking stocks.

## Prerequisites

- Python 3.8 or higher
- Basic knowledge of Python and pandas
- Understanding of basic financial concepts (returns, volatility, etc.)

## Installation

```bash
git clone https://github.com/pyenthusiasts/Bank-Data-Analysis.git
cd Bank-Data-Analysis
pip install -r requirements.txt
pip install -e .
```

## Lesson 1: Fetching Data

Let's start by fetching stock data for major banks.

```python
from bank_analysis import BankDataFetcher

# Create a fetcher for specific banks
tickers = ['JPM', 'BAC', 'C']  # JPMorgan, Bank of America, Citigroup
fetcher = BankDataFetcher(
    tickers=tickers,
    start_date='2023-01-01',
    end_date='2023-12-31'
)

# Fetch the data
data = fetcher.fetch_data()
print(data.head())
```

**Output:**
```
            JPM        BAC         C
2023-01-03  130.15    31.89    42.10
2023-01-04  132.21    32.15    42.56
...
```

## Lesson 2: Basic Analysis

Now let's analyze the data to calculate returns and statistics.

```python
from bank_analysis import BankAnalyzer

# Create analyzer
analyzer = BankAnalyzer(data)

# Calculate daily returns
returns = analyzer.calculate_returns()
print(f"Average daily returns:\n{returns.mean()}")

# Get summary statistics
summary = analyzer.get_summary_statistics()
print(f"\nSummary statistics:\n{summary}")
```

## Lesson 3: Correlation Analysis

Understanding how stocks move together is crucial.

```python
# Calculate correlation matrix
correlation = analyzer.get_correlation_matrix()
print(f"Correlation matrix:\n{correlation}")

# Interpretation:
# - Values close to 1.0 mean stocks move together
# - Values close to -1.0 mean stocks move opposite
# - Values close to 0.0 mean no relationship
```

## Lesson 4: Performance Analysis

Let's identify the best and worst performers.

```python
# Calculate cumulative returns
cumulative_returns = analyzer.calculate_cumulative_returns()

# Find best and worst performers
best, worst = analyzer.find_best_worst_performers()
print(f"\nBest performer: {best}")
print(f"Worst performer: {worst}")

# Get final cumulative returns
final_returns = cumulative_returns.iloc[-1]
for ticker in final_returns.index:
    print(f"{ticker}: {final_returns[ticker]:.2%}")
```

## Lesson 5: Risk Analysis

Volatility measures risk. Let's analyze it.

```python
# Calculate 30-day rolling volatility
volatility = analyzer.calculate_volatility(window=30)

# Current volatility
current_vol = volatility.iloc[-1]
print(f"\nCurrent volatility:\n{current_vol}")

# Average volatility
avg_vol = volatility.mean()
print(f"\nAverage volatility:\n{avg_vol}")
```

## Lesson 6: Risk-Adjusted Returns

The Sharpe ratio shows return per unit of risk.

```python
# Calculate Sharpe ratios
sharpe_ratios = analyzer.calculate_sharpe_ratio(risk_free_rate=0.02)
print(f"\nSharpe ratios:\n{sharpe_ratios.sort_values(ascending=False)}")

# Higher Sharpe ratio = better risk-adjusted performance
```

## Lesson 7: Visualization

Let's create some charts to visualize our findings.

```python
from bank_analysis import BankVisualizer

# Create visualizer
visualizer = BankVisualizer(data, returns)

# Plot price trends
visualizer.plot_prices(
    title="Banking Stocks Price Trends",
    save_path='tutorial_prices.png'
)

# Plot correlation heatmap
visualizer.plot_correlation_heatmap(
    correlation,
    title="Stock Correlations",
    save_path='tutorial_correlation.png'
)

# Plot cumulative returns
visualizer.plot_cumulative_returns(
    cumulative_returns,
    title="Cumulative Performance",
    save_path='tutorial_cumulative.png'
)

# Create comprehensive dashboard
visualizer.create_dashboard(
    analyzer,
    save_path='tutorial_dashboard.png'
)
```

## Lesson 8: Using Configuration Files

For repeated analyses, use a configuration file.

**config.yaml:**
```yaml
tickers:
  - JPM
  - BAC
  - C
  - WFC
  - GS

date_range:
  start: '2023-01-01'
  end: null  # today

analysis:
  volatility_window: 30
  risk_free_rate: 0.02
```

**Python code:**
```python
from bank_analysis.utils import load_config

# Load configuration
config = load_config('config.yaml')

# Use config values
fetcher = BankDataFetcher(
    tickers=config['tickers'],
    start_date=config['date_range']['start']
)
```

## Lesson 9: Command Line Usage

The CLI makes quick analysis easy.

```bash
# Run full analysis
bank-analysis --config config.yaml

# Analyze specific stocks
bank-analysis --tickers JPM BAC C --start 2023-01-01

# Save results
bank-analysis --save-data --output-dir results/
```

## Lesson 10: Advanced Analysis

Combine everything for comprehensive analysis.

```python
from bank_analysis import BankDataFetcher, BankAnalyzer, BankVisualizer
from bank_analysis.utils import load_config, format_percentage

# Load configuration
config = load_config('config.yaml')

# Fetch data
fetcher = BankDataFetcher(
    tickers=config['tickers'],
    start_date=config['date_range']['start']
)
data = fetcher.fetch_data()

# Analyze
analyzer = BankAnalyzer(data)
returns = analyzer.calculate_returns()
correlation = analyzer.get_correlation_matrix()
sharpe = analyzer.calculate_sharpe_ratio()
cumulative = analyzer.calculate_cumulative_returns()

# Generate report
print("="*60)
print("Banking Stock Analysis Report")
print("="*60)

print(f"\nPeriod: {data.index[0]} to {data.index[-1]}")
print(f"Stocks analyzed: {', '.join(config['tickers'])}")

print("\nPerformance Summary:")
for ticker in cumulative.columns:
    final_return = cumulative[ticker].iloc[-1]
    sharpe_ratio = sharpe[ticker]
    print(f"{ticker}: {format_percentage(final_return)} "
          f"(Sharpe: {sharpe_ratio:.3f})")

best, worst = analyzer.find_best_worst_performers()
print(f"\nBest performer: {best}")
print(f"Worst performer: {worst}")

# Create visualizations
visualizer = BankVisualizer(data, returns)
visualizer.create_dashboard(analyzer, save_path='final_dashboard.png')

print("\n✓ Analysis complete! Check final_dashboard.png")
```

## Next Steps

- Explore the [API Documentation](API.md) for detailed reference
- Check out example scripts in the `examples/` directory
- Read the [FAQ](FAQ.md) for common questions
- Try the enhanced Jupyter notebook for interactive analysis

## Common Patterns

### Pattern 1: Quick Daily Analysis

```python
# Morning routine: check yesterday's performance
from bank_analysis import BankDataFetcher, BankAnalyzer
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
fetcher = BankDataFetcher(start_date=yesterday)
data = fetcher.fetch_data()

analyzer = BankAnalyzer(data)
returns = analyzer.calculate_returns()
print(f"Yesterday's returns:\n{returns.iloc[-1]}")
```

### Pattern 2: Compare Time Periods

```python
# Compare Q1 vs Q2 performance
fetcher_q1 = BankDataFetcher(start_date='2023-01-01', end_date='2023-03-31')
fetcher_q2 = BankDataFetcher(start_date='2023-04-01', end_date='2023-06-30')

data_q1 = fetcher_q1.fetch_data()
data_q2 = fetcher_q2.fetch_data()

analyzer_q1 = BankAnalyzer(data_q1)
analyzer_q2 = BankAnalyzer(data_q2)

# Compare returns
returns_q1 = analyzer_q1.calculate_returns()
returns_q2 = analyzer_q2.calculate_returns()

print(f"Q1 average returns: {returns_q1.mean()}")
print(f"Q2 average returns: {returns_q2.mean()}")
```

### Pattern 3: Custom Stock List

```python
# Analyze your custom portfolio
my_portfolio = ['JPM', 'MS', 'GS']  # Investment banks only

fetcher = BankDataFetcher(tickers=my_portfolio)
data = fetcher.fetch_data()

analyzer = BankAnalyzer(data)
analyzer.calculate_returns()

sharpe = analyzer.calculate_sharpe_ratio()
print(f"Portfolio Sharpe ratios:\n{sharpe.sort_values(ascending=False)}")
```

## Tips and Best Practices

1. **Always check data quality**: Verify that fetched data has no missing values
2. **Use appropriate date ranges**: Ensure sufficient data for meaningful analysis
3. **Save intermediate results**: Don't refetch data unnecessarily
4. **Configure logging**: Use log levels to debug issues
5. **Handle errors gracefully**: Wrap API calls in try-except blocks
6. **Version your analyses**: Save configuration files with your results

## Troubleshooting

**Issue: No data returned**
- Check internet connection
- Verify ticker symbols are correct
- Try a different date range

**Issue: Import errors**
- Ensure package is installed: `pip install -e .`
- Check Python version >= 3.8

**Issue: Plots not showing**
- In Jupyter, use `%matplotlib inline`
- In scripts, use `plt.show()` or save to file

Happy analyzing! 🏦📈
