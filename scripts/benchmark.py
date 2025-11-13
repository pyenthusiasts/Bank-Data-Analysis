"""
Performance benchmarking script for the bank_analysis package.

This script measures the performance of various operations to help
identify bottlenecks and track performance over time.
"""

import time
import sys
from pathlib import Path
from typing import Dict, List, Callable
import statistics

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bank_analysis import BankDataFetcher, BankAnalyzer, BankVisualizer


class Benchmark:
    """Simple benchmarking utility."""

    def __init__(self, name: str):
        self.name = name
        self.results: List[float] = []

    def run(self, func: Callable, runs: int = 3) -> Dict:
        """Run benchmark multiple times and return statistics."""
        print(f"\nRunning: {self.name}")
        print(f"  Iterations: {runs}")

        self.results = []
        for i in range(runs):
            start_time = time.time()
            func()
            elapsed = time.time() - start_time
            self.results.append(elapsed)
            print(f"  Run {i+1}: {elapsed:.3f}s")

        stats = {
            'name': self.name,
            'runs': runs,
            'mean': statistics.mean(self.results),
            'median': statistics.median(self.results),
            'min': min(self.results),
            'max': max(self.results),
            'stdev': statistics.stdev(self.results) if len(self.results) > 1 else 0
        }

        print(f"  Mean: {stats['mean']:.3f}s")
        print(f"  Median: {stats['median']:.3f}s")
        print(f"  Min: {stats['min']:.3f}s")
        print(f"  Max: {stats['max']:.3f}s")
        print(f"  StdDev: {stats['stdev']:.3f}s")

        return stats


def main():
    """Run all benchmarks."""

    print("="*70)
    print("Bank Data Analysis - Performance Benchmarks")
    print("="*70)

    all_results = []

    # Setup test data
    print("\nSetting up test data...")
    tickers = ['JPM', 'BAC', 'C', 'WFC', 'GS']
    start_date = '2023-01-01'
    end_date = '2023-12-31'

    # Benchmark 1: Data Fetching
    def fetch_data():
        fetcher = BankDataFetcher(tickers=tickers, start_date=start_date, end_date=end_date)
        return fetcher.fetch_data()

    bench = Benchmark("Data Fetching (5 tickers, 1 year)")
    result = bench.run(fetch_data, runs=3)
    all_results.append(result)

    # Get data for subsequent tests
    print("\nPreparing data for analysis benchmarks...")
    data = fetch_data()
    print(f"✓ Data shape: {data.shape}")

    # Benchmark 2: Returns Calculation
    def calc_returns():
        analyzer = BankAnalyzer(data)
        return analyzer.calculate_returns()

    bench = Benchmark("Returns Calculation")
    result = bench.run(calc_returns, runs=5)
    all_results.append(result)

    # Setup analyzer with returns for subsequent tests
    analyzer = BankAnalyzer(data)
    returns = analyzer.calculate_returns()

    # Benchmark 3: Correlation Matrix
    def calc_correlation():
        return analyzer.get_correlation_matrix()

    bench = Benchmark("Correlation Matrix Calculation")
    result = bench.run(calc_correlation, runs=5)
    all_results.append(result)

    # Benchmark 4: Volatility Calculation
    def calc_volatility():
        return analyzer.calculate_volatility(window=30)

    bench = Benchmark("Volatility Calculation (30-day window)")
    result = bench.run(calc_volatility, runs=5)
    all_results.append(result)

    # Benchmark 5: Cumulative Returns
    def calc_cumulative():
        return analyzer.calculate_cumulative_returns()

    bench = Benchmark("Cumulative Returns Calculation")
    result = bench.run(calc_cumulative, runs=5)
    all_results.append(result)

    # Benchmark 6: Sharpe Ratio
    def calc_sharpe():
        return analyzer.calculate_sharpe_ratio()

    bench = Benchmark("Sharpe Ratio Calculation")
    result = bench.run(calc_sharpe, runs=5)
    all_results.append(result)

    # Benchmark 7: Price Statistics
    def calc_stats():
        return analyzer.get_price_statistics()

    bench = Benchmark("Price Statistics Calculation")
    result = bench.run(calc_stats, runs=5)
    all_results.append(result)

    # Benchmark 8: Best/Worst Performers
    def find_performers():
        return analyzer.find_best_worst_performers()

    bench = Benchmark("Find Best/Worst Performers")
    result = bench.run(find_performers, runs=5)
    all_results.append(result)

    # Benchmark 9: Complete Analysis Pipeline
    def full_pipeline():
        fetcher = BankDataFetcher(tickers=tickers, start_date=start_date, end_date=end_date)
        data = fetcher.fetch_data()
        analyzer = BankAnalyzer(data)
        returns = analyzer.calculate_returns()
        correlation = analyzer.get_correlation_matrix()
        cumulative = analyzer.calculate_cumulative_returns()
        volatility = analyzer.calculate_volatility()
        sharpe = analyzer.calculate_sharpe_ratio()
        stats = analyzer.get_price_statistics()
        best, worst = analyzer.find_best_worst_performers()
        return data, returns, correlation, cumulative, volatility, sharpe, stats, best, worst

    bench = Benchmark("Full Analysis Pipeline")
    result = bench.run(full_pipeline, runs=3)
    all_results.append(result)

    # Summary
    print("\n" + "="*70)
    print("Benchmark Summary")
    print("="*70)
    print(f"\n{'Operation':<45} {'Mean (s)':>12} {'Median (s)':>12}")
    print("-"*70)

    total_time = 0
    for result in all_results:
        print(f"{result['name']:<45} {result['mean']:>12.3f} {result['median']:>12.3f}")
        total_time += result['mean']

    print("-"*70)
    print(f"{'Total Time':< 45} {total_time:>12.3f}")

    # Performance tips
    print("\n" + "="*70)
    print("Performance Tips")
    print("="*70)
    print("""
1. Data Fetching is the slowest operation - cache results when possible
2. Reuse analyzer objects instead of creating new ones
3. Calculate metrics only when needed
4. Use smaller date ranges for faster iteration during development
5. Consider using parquet format for faster data I/O
6. Process stocks in batches for large-scale analysis
    """)

    # Save results
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)

    import json
    output_file = output_dir / 'benchmark_results.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\n✓ Results saved to: {output_file}")

    print("\n" + "="*70)
    print("Benchmarking Complete!")
    print("="*70)


if __name__ == '__main__':
    main()
