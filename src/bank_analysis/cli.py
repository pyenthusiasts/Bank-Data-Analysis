"""
Command-line interface for bank data analysis.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
import yaml

from .data_fetcher import BankDataFetcher
from .analyzer import BankAnalyzer
from .visualizer import BankVisualizer
from .utils import load_config, setup_logging, create_directory_structure


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Bank Data Analysis - Analyze banking stock performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full analysis with default config
  bank-analysis --config config.yaml

  # Analyze specific tickers
  bank-analysis --tickers JPM BAC C --start 2020-01-01

  # Generate only visualizations
  bank-analysis --plot-only

  # Save results to specific directory
  bank-analysis --output-dir results/
        """
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    parser.add_argument(
        '--tickers',
        nargs='+',
        help='Stock ticker symbols to analyze (overrides config)'
    )

    parser.add_argument(
        '--start',
        type=str,
        help='Start date (YYYY-MM-DD) (overrides config)'
    )

    parser.add_argument(
        '--end',
        type=str,
        help='End date (YYYY-MM-DD) (overrides config)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Output directory for plots and reports (default: output)'
    )

    parser.add_argument(
        '--plot-only',
        action='store_true',
        help='Only generate plots (skip data fetching)'
    )

    parser.add_argument(
        '--no-plots',
        action='store_true',
        help='Skip plot generation'
    )

    parser.add_argument(
        '--save-data',
        action='store_true',
        help='Save processed data to CSV files'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: INFO)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Bank Data Analysis v1.0.0'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(log_level=args.log_level)

    # Load configuration
    config = {}
    if Path(args.config).exists():
        config = load_config(args.config)
        print(f"✓ Configuration loaded from {args.config}")
    else:
        print(f"⚠ Configuration file not found: {args.config}")
        print("  Using command-line arguments or defaults")

    # Get parameters (CLI args override config)
    tickers = args.tickers or config.get('tickers', ['JPM', 'BAC', 'C', 'WFC', 'GS'])
    start_date = args.start or config.get('date_range', {}).get('start', '2020-01-01')
    end_date = args.end or config.get('date_range', {}).get('end')

    print("\n" + "="*60)
    print("Bank Data Analysis")
    print("="*60)
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Date Range: {start_date} to {end_date or 'today'}")
    print("="*60 + "\n")

    try:
        # Create output directory structure
        create_directory_structure(args.output_dir)

        if not args.plot_only:
            # Fetch data
            print("📊 Fetching stock data...")
            fetcher = BankDataFetcher(
                tickers=tickers,
                start_date=start_date,
                end_date=end_date
            )
            data = fetcher.fetch_data()
            print(f"✓ Fetched {len(data)} days of data\n")

            # Analyze data
            print("📈 Analyzing data...")
            analyzer = BankAnalyzer(data)
            returns = analyzer.calculate_returns()
            correlation_matrix = analyzer.get_correlation_matrix()
            cumulative_returns = analyzer.calculate_cumulative_returns()
            volatility = analyzer.calculate_volatility()
            sharpe_ratios = analyzer.calculate_sharpe_ratio()
            print("✓ Analysis complete\n")

            # Print summary
            print("="*60)
            print("Analysis Summary")
            print("="*60)

            best, worst = analyzer.find_best_worst_performers()
            print(f"\n🏆 Best Performer: {best}")
            print(f"   Cumulative Return: {cumulative_returns.iloc[-1][best]:.2%}")

            print(f"\n📉 Worst Performer: {worst}")
            print(f"   Cumulative Return: {cumulative_returns.iloc[-1][worst]:.2%}")

            print("\n📊 Sharpe Ratios (Risk-Adjusted Performance):")
            for ticker in sharpe_ratios.sort_values(ascending=False).index:
                print(f"   {ticker}: {sharpe_ratios[ticker]:.3f}")

            print("\n" + "="*60 + "\n")

            # Save data if requested
            if args.save_data:
                print("💾 Saving processed data...")
                output_path = Path(args.output_dir) / 'data'
                output_path.mkdir(exist_ok=True)

                data.to_csv(output_path / 'prices.csv')
                returns.to_csv(output_path / 'returns.csv')
                cumulative_returns.to_csv(output_path / 'cumulative_returns.csv')
                correlation_matrix.to_csv(output_path / 'correlation_matrix.csv')
                print(f"✓ Data saved to {output_path}\n")

        if not args.no_plots:
            print("🎨 Generating visualizations...")

            if args.plot_only:
                # Load data from file
                print("Loading existing data...")
                # This is a simplified version - in production, you'd load from saved files
                print("⚠ Plot-only mode requires existing data. Please run full analysis first.")
                return

            visualizer = BankVisualizer(data, returns)
            plot_path = Path(args.output_dir) / 'plots'
            plot_path.mkdir(exist_ok=True)

            # Generate all plots
            visualizer.plot_prices(save_path=str(plot_path / 'prices.png'))
            visualizer.plot_correlation_heatmap(
                correlation_matrix,
                save_path=str(plot_path / 'correlation.png')
            )
            visualizer.plot_cumulative_returns(
                cumulative_returns,
                save_path=str(plot_path / 'cumulative_returns.png')
            )
            visualizer.plot_volatility(
                volatility,
                save_path=str(plot_path / 'volatility.png')
            )
            visualizer.plot_returns_distribution(
                save_path=str(plot_path / 'returns_distribution.png')
            )
            visualizer.create_dashboard(
                analyzer,
                save_path=str(plot_path / 'dashboard.png')
            )

            print(f"✓ Plots saved to {plot_path}\n")

        print("="*60)
        print("✓ Analysis Complete!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
