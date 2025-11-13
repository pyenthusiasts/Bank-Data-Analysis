"""
Basic example of using the bank_analysis package.

This script demonstrates how to:
1. Fetch banking stock data
2. Calculate returns and statistics
3. Generate visualizations
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bank_analysis import BankDataFetcher, BankAnalyzer, BankVisualizer


def main():
    """Run a basic analysis of banking stocks."""

    print("="*60)
    print("Basic Banking Stock Analysis")
    print("="*60)

    # Define tickers and date range
    tickers = ['JPM', 'BAC', 'C', 'WFC', 'GS']
    start_date = '2020-01-01'

    print(f"\nAnalyzing: {', '.join(tickers)}")
    print(f"From: {start_date} to today\n")

    # Step 1: Fetch data
    print("Step 1: Fetching data...")
    fetcher = BankDataFetcher(tickers=tickers, start_date=start_date)
    data = fetcher.fetch_data()
    print(f"✓ Fetched {len(data)} days of data")

    # Step 2: Analyze data
    print("\nStep 2: Analyzing data...")
    analyzer = BankAnalyzer(data)
    returns = analyzer.calculate_returns()
    print("✓ Calculated returns")

    # Step 3: Get statistics
    print("\nStep 3: Computing statistics...")
    correlation = analyzer.get_correlation_matrix()
    summary = analyzer.get_summary_statistics()
    cumulative = analyzer.calculate_cumulative_returns()
    sharpe = analyzer.calculate_sharpe_ratio()

    print("✓ Computed correlation matrix")
    print("✓ Computed summary statistics")
    print("✓ Computed cumulative returns")
    print("✓ Computed Sharpe ratios")

    # Step 4: Display results
    print("\n" + "="*60)
    print("Results Summary")
    print("="*60)

    print("\nCumulative Returns (Total % Change):")
    for ticker in cumulative.columns:
        final_return = cumulative[ticker].iloc[-1]
        print(f"  {ticker}: {final_return:>8.2%}")

    print("\nSharpe Ratios (Risk-Adjusted Performance):")
    for ticker in sharpe.sort_values(ascending=False).index:
        print(f"  {ticker}: {sharpe[ticker]:>8.3f}")

    best, worst = analyzer.find_best_worst_performers()
    print(f"\n🏆 Best Performer: {best}")
    print(f"📉 Worst Performer: {worst}")

    # Step 5: Create visualizations
    print("\n" + "="*60)
    print("Generating Visualizations")
    print("="*60)

    visualizer = BankVisualizer(data, returns)

    # Create output directory
    output_dir = Path(__file__).parent.parent / 'output' / 'examples'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\nCreating plots...")
    visualizer.plot_prices(save_path=str(output_dir / 'example_prices.png'))
    print("✓ Price trends plot saved")

    visualizer.plot_correlation_heatmap(
        correlation,
        save_path=str(output_dir / 'example_correlation.png')
    )
    print("✓ Correlation heatmap saved")

    visualizer.plot_cumulative_returns(
        cumulative,
        save_path=str(output_dir / 'example_cumulative_returns.png')
    )
    print("✓ Cumulative returns plot saved")

    visualizer.create_dashboard(
        analyzer,
        save_path=str(output_dir / 'example_dashboard.png')
    )
    print("✓ Dashboard saved")

    print(f"\n✓ All plots saved to: {output_dir}")

    print("\n" + "="*60)
    print("Analysis Complete!")
    print("="*60)


if __name__ == '__main__':
    main()
