"""
Sector Analysis Example

Compare banking sector performance against market indices and other sectors.
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bank_analysis import BankDataFetcher, BankAnalyzer


def sector_analysis():
    """Analyze banking sector against broader market."""

    print("="*70)
    print("Banking Sector Analysis")
    print("="*70)

    # Define tickers for analysis
    tickers = {
        'Banking Sector': ['JPM', 'BAC', 'C', 'WFC', 'GS'],
        'Market Indices': ['SPY', 'DIA', 'QQQ'],  # S&P 500, Dow, Nasdaq
        'Tech Leaders': ['AAPL', 'MSFT', 'GOOGL'],
        'Other Financials': ['V', 'MA', 'AXP']  # Visa, Mastercard, Amex
    }

    start_date = '2020-01-01'
    all_tickers = []
    for group_tickers in tickers.values():
        all_tickers.extend(group_tickers)

    print(f"\nFetching data for {len(all_tickers)} tickers...")

    # Fetch all data
    try:
        fetcher = BankDataFetcher(tickers=all_tickers, start_date=start_date)
        data = fetcher.fetch_data()
        print(f"✓ Fetched {len(data)} days of data")

        # Analyze
        analyzer = BankAnalyzer(data)
        returns = analyzer.calculate_returns()
        cumulative_returns = analyzer.calculate_cumulative_returns()

        # Calculate sector averages
        sector_performance = {}
        for sector_name, sector_tickers in tickers.items():
            available_tickers = [t for t in sector_tickers if t in cumulative_returns.columns]
            if available_tickers:
                sector_cum_return = cumulative_returns[available_tickers].mean(axis=1)
                sector_volatility = returns[available_tickers].mean(axis=1).std()
                sector_sharpe = (
                    returns[available_tickers].mean(axis=1).mean() * 252 - 0.02
                ) / (returns[available_tickers].mean(axis=1).std() * (252 ** 0.5))

                sector_performance[sector_name] = {
                    'cumulative_return': sector_cum_return,
                    'final_return': sector_cum_return.iloc[-1],
                    'volatility': sector_volatility,
                    'sharpe': sector_sharpe,
                    'tickers': available_tickers
                }

        # Display results
        print(f"\n{'='*70}")
        print("Sector Performance Summary")
        print('='*70)

        for sector_name, perf in sorted(
            sector_performance.items(),
            key=lambda x: x[1]['final_return'],
            reverse=True
        ):
            print(f"\n{sector_name}:")
            print(f"  Tickers: {', '.join(perf['tickers'])}")
            print(f"  Total Return: {perf['final_return']:.2%}")
            print(f"  Sharpe Ratio: {perf['sharpe']:.3f}")
            print(f"  Volatility: {perf['volatility']:.6f}")

        # Relative performance analysis
        print(f"\n{'='*70}")
        print("Banking Sector vs Market")
        print('='*70)

        banking_return = sector_performance['Banking Sector']['final_return']
        market_return = sector_performance['Market Indices']['final_return']
        outperformance = banking_return - market_return

        print(f"\nBanking Sector Return: {banking_return:.2%}")
        print(f"Market Indices Return: {market_return:.2%}")
        print(f"Outperformance: {outperformance:+.2%}")

        if outperformance > 0:
            print(f"\n✓ Banking sector OUTPERFORMED the market by {abs(outperformance):.2%}")
        else:
            print(f"\n✗ Banking sector UNDERPERFORMED the market by {abs(outperformance):.2%}")

        # Create visualizations
        output_dir = Path(__file__).parent.parent / 'output' / 'sector_analysis'
        output_dir.mkdir(parents=True, exist_ok=True)

        # Plot 1: Sector comparison
        fig, ax = plt.subplots(figsize=(14, 7))
        for sector_name, perf in sector_performance.items():
            cum_ret = perf['cumulative_return']
            ax.plot(cum_ret.index, cum_ret * 100, linewidth=2.5, label=sector_name)

        ax.set_title('Sector Performance Comparison', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Cumulative Return (%)', fontsize=12)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(output_dir / 'sector_comparison.png', dpi=300, bbox_inches='tight')
        print(f"\n✓ Saved: {output_dir / 'sector_comparison.png'}")
        plt.close()

        # Plot 2: Correlation heatmap
        fig, ax = plt.subplots(figsize=(12, 10))
        correlation = returns.corr()
        sns.heatmap(
            correlation,
            annot=False,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        ax.set_title('Cross-Sector Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_dir / 'cross_sector_correlation.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_dir / 'cross_sector_correlation.png'}")
        plt.close()

        # Plot 3: Risk-Return by sector
        fig, ax = plt.subplots(figsize=(10, 8))
        for sector_name, perf in sector_performance.items():
            ret = perf['final_return'] * 100
            vol = perf['volatility'] * 100
            ax.scatter(vol, ret, s=300, alpha=0.6, label=sector_name)
            ax.annotate(
                sector_name,
                (vol, ret),
                fontsize=10,
                ha='center',
                va='bottom',
                fontweight='bold'
            )

        ax.set_title('Sector Risk-Return Profile', fontsize=16, fontweight='bold')
        ax.set_xlabel('Volatility (%)', fontsize=12)
        ax.set_ylabel('Total Return (%)', fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / 'sector_risk_return.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_dir / 'sector_risk_return.png'}")
        plt.close()

        print(f"\n{'='*70}")
        print("Sector Analysis Complete!")
        print(f"Results saved to: {output_dir}")
        print('='*70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    sector_analysis()
