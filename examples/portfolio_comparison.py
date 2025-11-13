"""
Portfolio Comparison Example

This script demonstrates how to compare different portfolios
of banking stocks and analyze their relative performance.
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bank_analysis import BankDataFetcher, BankAnalyzer, BankVisualizer


def compare_portfolios():
    """Compare performance of different banking stock portfolios."""

    print("="*70)
    print("Portfolio Comparison Analysis")
    print("="*70)

    # Define different portfolios
    portfolios = {
        'Large Banks': ['JPM', 'BAC', 'WFC', 'C'],
        'Investment Banks': ['JPM', 'GS', 'MS'],
        'Regional Banks': ['USB', 'PNC', 'TFC'],
        'All Major Banks': ['JPM', 'BAC', 'C', 'WFC', 'GS', 'MS']
    }

    start_date = '2020-01-01'
    results = {}

    # Analyze each portfolio
    for portfolio_name, tickers in portfolios.items():
        print(f"\n{'='*70}")
        print(f"Analyzing: {portfolio_name}")
        print(f"Tickers: {', '.join(tickers)}")
        print('='*70)

        try:
            # Fetch data
            fetcher = BankDataFetcher(tickers=tickers, start_date=start_date)
            data = fetcher.fetch_data()

            # Analyze
            analyzer = BankAnalyzer(data)
            returns = analyzer.calculate_returns()
            cumulative_returns = analyzer.calculate_cumulative_returns()
            sharpe = analyzer.calculate_sharpe_ratio()

            # Calculate portfolio metrics (equal weight)
            portfolio_return = returns.mean(axis=1)
            portfolio_cumulative = (1 + portfolio_return).cumprod() - 1
            portfolio_volatility = portfolio_return.std()
            portfolio_sharpe = (
                portfolio_return.mean() * 252 - 0.02
            ) / (portfolio_return.std() * (252 ** 0.5))

            results[portfolio_name] = {
                'data': data,
                'returns': returns,
                'cumulative_returns': cumulative_returns,
                'portfolio_cumulative': portfolio_cumulative,
                'sharpe': sharpe,
                'portfolio_sharpe': portfolio_sharpe,
                'portfolio_volatility': portfolio_volatility,
                'tickers': tickers
            }

            # Display portfolio summary
            print(f"\nPortfolio Summary:")
            print(f"  Total Return: {portfolio_cumulative.iloc[-1]:.2%}")
            print(f"  Sharpe Ratio: {portfolio_sharpe:.3f}")
            print(f"  Volatility: {portfolio_volatility:.6f}")

            print(f"\nIndividual Stock Performance:")
            for ticker in tickers:
                if ticker in cumulative_returns.columns:
                    final_return = cumulative_returns[ticker].iloc[-1]
                    stock_sharpe = sharpe[ticker] if ticker in sharpe.index else float('nan')
                    print(f"  {ticker}: {final_return:>8.2%}  (Sharpe: {stock_sharpe:>6.3f})")

        except Exception as e:
            print(f"Error analyzing {portfolio_name}: {e}")
            continue

    # Compare portfolios
    print(f"\n{'='*70}")
    print("Portfolio Comparison Summary")
    print('='*70)

    comparison_data = []
    for name, result in results.items():
        comparison_data.append({
            'Portfolio': name,
            'Total Return': result['portfolio_cumulative'].iloc[-1],
            'Sharpe Ratio': result['portfolio_sharpe'],
            'Volatility': result['portfolio_volatility'],
            'Num Stocks': len(result['tickers'])
        })

    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.sort_values('Total Return', ascending=False)

    print(f"\n{comparison_df.to_string(index=False)}")

    # Identify best portfolio
    best_return = comparison_df.iloc[0]
    best_sharpe = comparison_df.loc[comparison_df['Sharpe Ratio'].idxmax()]

    print(f"\n{'='*70}")
    print("Key Findings:")
    print('='*70)
    print(f"\n🏆 Best Total Return: {best_return['Portfolio']}")
    print(f"   Return: {best_return['Total Return']:.2%}")

    print(f"\n📊 Best Risk-Adjusted Return: {best_sharpe['Portfolio']}")
    print(f"   Sharpe Ratio: {best_sharpe['Sharpe Ratio']:.3f}")

    # Create visualizations
    print(f"\n{'='*70}")
    print("Generating Visualizations")
    print('='*70)

    output_dir = Path(__file__).parent.parent / 'output' / 'portfolio_comparison'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Plot 1: Cumulative returns comparison
    fig, ax = plt.subplots(figsize=(14, 7))
    for name, result in results.items():
        portfolio_cum = result['portfolio_cumulative']
        ax.plot(portfolio_cum.index, portfolio_cum * 100, linewidth=2, label=name)

    ax.set_title('Portfolio Cumulative Returns Comparison', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cumulative Return (%)', fontsize=12)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(output_dir / 'portfolio_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir / 'portfolio_comparison.png'}")
    plt.close()

    # Plot 2: Risk-Return scatter
    fig, ax = plt.subplots(figsize=(10, 8))
    for name, result in results.items():
        ret = result['portfolio_cumulative'].iloc[-1] * 100
        vol = result['portfolio_volatility'] * 100
        ax.scatter(vol, ret, s=200, alpha=0.6, label=name)
        ax.annotate(name, (vol, ret), fontsize=9, ha='center', va='bottom')

    ax.set_title('Portfolio Risk-Return Profile', fontsize=16, fontweight='bold')
    ax.set_xlabel('Volatility (%)', fontsize=12)
    ax.set_ylabel('Total Return (%)', fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'risk_return_profile.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir / 'risk_return_profile.png'}")
    plt.close()

    # Plot 3: Sharpe ratio comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    sharpe_data = [(name, result['portfolio_sharpe']) for name, result in results.items()]
    sharpe_data.sort(key=lambda x: x[1], reverse=True)
    names, sharpes = zip(*sharpe_data)

    colors = ['green' if s > 1 else 'orange' if s > 0.5 else 'red' for s in sharpes]
    ax.barh(names, sharpes, color=colors, alpha=0.7)
    ax.set_xlabel('Sharpe Ratio', fontsize=12)
    ax.set_title('Portfolio Sharpe Ratios', fontsize=16, fontweight='bold')
    ax.axvline(x=1.0, color='black', linestyle='--', linewidth=1, label='Target: 1.0')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(output_dir / 'sharpe_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir / 'sharpe_comparison.png'}")
    plt.close()

    print(f"\n{'='*70}")
    print("Portfolio Comparison Complete!")
    print(f"Results saved to: {output_dir}")
    print('='*70)


if __name__ == '__main__':
    compare_portfolios()
