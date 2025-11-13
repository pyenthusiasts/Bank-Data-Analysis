"""
Advanced example showing custom analysis with configuration.

This script demonstrates:
1. Loading configuration from YAML
2. Custom ticker selection
3. Advanced metrics calculation
4. Custom visualization
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bank_analysis import BankDataFetcher, BankAnalyzer, BankVisualizer
from bank_analysis.utils import load_config, format_percentage, format_currency


def main():
    """Run a custom advanced analysis."""

    print("="*60)
    print("Custom Banking Stock Analysis")
    print("="*60)

    # Load configuration
    config_path = Path(__file__).parent.parent / 'config.yaml'
    config = load_config(str(config_path))

    # Extract config values
    tickers = config['tickers']
    start_date = config['date_range']['start']
    risk_free_rate = config['analysis']['risk_free_rate']
    volatility_window = config['analysis']['volatility_window']

    print(f"\nConfiguration loaded from: {config_path}")
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Start Date: {start_date}")
    print(f"Risk-Free Rate: {risk_free_rate}")
    print(f"Volatility Window: {volatility_window} days\n")

    # Fetch and analyze data
    print("Fetching and analyzing data...")
    fetcher = BankDataFetcher(tickers=tickers, start_date=start_date)
    data = fetcher.fetch_data()

    analyzer = BankAnalyzer(data)
    returns = analyzer.calculate_returns()

    # Advanced analysis
    print("\nPerforming advanced analysis...")

    # 1. Price statistics
    price_stats = analyzer.get_price_statistics()

    # 2. Volatility analysis
    volatility = analyzer.calculate_volatility(window=volatility_window)
    current_volatility = volatility.iloc[-1]
    avg_volatility = volatility.mean()

    # 3. Sharpe ratios
    sharpe_ratios = analyzer.calculate_sharpe_ratio(risk_free_rate=risk_free_rate)

    # 4. Cumulative returns
    cumulative_returns = analyzer.calculate_cumulative_returns()

    # Display detailed results
    print("\n" + "="*60)
    print("Detailed Analysis Results")
    print("="*60)

    print("\n1. PRICE STATISTICS")
    print("-" * 60)
    stats_df = pd.DataFrame({
        'Current Price': price_stats['current_price'],
        'Min Price': price_stats['min_price'],
        'Max Price': price_stats['max_price'],
        'Mean Price': price_stats['mean_price'],
        'Total % Change': price_stats['percent_change']
    })
    print(stats_df.round(2))

    print("\n2. VOLATILITY ANALYSIS")
    print("-" * 60)
    vol_df = pd.DataFrame({
        'Current Vol': current_volatility,
        'Average Vol': avg_volatility,
        'Max Vol': volatility.max(),
        'Min Vol': volatility.min()
    })
    print(vol_df.round(6))

    print("\n3. RISK-ADJUSTED PERFORMANCE (Sharpe Ratios)")
    print("-" * 60)
    sharpe_df = pd.DataFrame({
        'Sharpe Ratio': sharpe_ratios,
        'Rank': range(1, len(sharpe_ratios) + 1)
    }).sort_values('Sharpe Ratio', ascending=False)
    print(sharpe_df.round(4))

    print("\n4. CUMULATIVE PERFORMANCE")
    print("-" * 60)
    final_returns = cumulative_returns.iloc[-1].sort_values(ascending=False)
    for ticker, ret in final_returns.items():
        print(f"  {ticker}: {format_percentage(ret)}")

    # Identify insights
    print("\n" + "="*60)
    print("Key Insights")
    print("="*60)

    best_performer = final_returns.idxmax()
    worst_performer = final_returns.idxmin()
    most_volatile = current_volatility.idxmax()
    least_volatile = current_volatility.idxmin()
    best_sharpe = sharpe_ratios.idxmax()

    print(f"\n📊 Best Overall Performer: {best_performer}")
    print(f"   Total Return: {format_percentage(final_returns[best_performer])}")

    print(f"\n📈 Best Risk-Adjusted Performer: {best_sharpe}")
    print(f"   Sharpe Ratio: {sharpe_ratios[best_sharpe]:.4f}")

    print(f"\n⚡ Most Volatile: {most_volatile}")
    print(f"   Current Volatility: {current_volatility[most_volatile]:.6f}")

    print(f"\n🛡️  Least Volatile: {least_volatile}")
    print(f"   Current Volatility: {current_volatility[least_volatile]:.6f}")

    # Generate custom visualizations
    print("\n" + "="*60)
    print("Generating Custom Visualizations")
    print("="*60)

    visualizer = BankVisualizer(data, returns)
    output_dir = Path(__file__).parent.parent / 'output' / 'custom_analysis'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create all visualizations
    visualizer.plot_prices(
        title="Banking Stocks - Price Trends (Custom Analysis)",
        save_path=str(output_dir / 'custom_prices.png')
    )

    visualizer.plot_volatility(
        volatility,
        title=f"Banking Stocks - {volatility_window}-Day Rolling Volatility",
        save_path=str(output_dir / 'custom_volatility.png')
    )

    visualizer.create_dashboard(
        analyzer,
        save_path=str(output_dir / 'custom_dashboard.png')
    )

    print(f"\n✓ Custom visualizations saved to: {output_dir}")

    print("\n" + "="*60)
    print("Custom Analysis Complete!")
    print("="*60)


if __name__ == '__main__':
    main()
