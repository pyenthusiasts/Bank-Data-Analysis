"""
Visualizer module for creating plots and charts of banking data.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class BankVisualizer:
    """
    Creates visualizations for banking stock analysis.

    Attributes:
        data (pd.DataFrame): Stock price data
        returns (pd.DataFrame): Stock returns data
    """

    def __init__(self, data: pd.DataFrame, returns: Optional[pd.DataFrame] = None):
        """
        Initialize the BankVisualizer.

        Args:
            data: DataFrame containing stock price data
            returns: Optional DataFrame containing returns data
        """
        self.data = data
        self.returns = returns

    def plot_prices(
        self,
        title: str = "Adjusted Close Prices of Major Banks",
        figsize: Tuple[int, int] = (14, 7),
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot stock prices over time.

        Args:
            title: Chart title
            figsize: Figure size as (width, height)
            save_path: Optional path to save the figure
        """
        logger.info("Plotting price data")

        fig, ax = plt.subplots(figsize=figsize)
        self.data.plot(ax=ax, linewidth=2)

        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price ($)", fontsize=12)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")

        plt.show()

    def plot_correlation_heatmap(
        self,
        correlation_matrix: pd.DataFrame,
        title: str = "Correlation Matrix of Daily Returns",
        figsize: Tuple[int, int] = (10, 8),
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot correlation heatmap.

        Args:
            correlation_matrix: Correlation matrix to plot
            title: Chart title
            figsize: Figure size as (width, height)
            save_path: Optional path to save the figure
        """
        logger.info("Plotting correlation heatmap")

        fig, ax = plt.subplots(figsize=figsize)

        sns.heatmap(
            correlation_matrix,
            annot=True,
            fmt='.3f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )

        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")

        plt.show()

    def plot_returns_distribution(
        self,
        figsize: Tuple[int, int] = (14, 10),
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot distribution of returns for each stock.

        Args:
            figsize: Figure size as (width, height)
            save_path: Optional path to save the figure
        """
        if self.returns is None:
            raise ValueError("Returns data not provided")

        logger.info("Plotting returns distribution")

        n_stocks = len(self.returns.columns)
        n_cols = 2
        n_rows = (n_stocks + 1) // 2

        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten()

        for i, col in enumerate(self.returns.columns):
            ax = axes[i]
            self.returns[col].hist(bins=50, ax=ax, alpha=0.7, edgecolor='black')
            ax.axvline(self.returns[col].mean(), color='red',
                      linestyle='--', linewidth=2, label=f'Mean: {self.returns[col].mean():.4f}')
            ax.set_title(f'{col} Returns Distribution', fontweight='bold')
            ax.set_xlabel('Returns')
            ax.set_ylabel('Frequency')
            ax.legend()
            ax.grid(True, alpha=0.3)

        # Hide extra subplots
        for i in range(n_stocks, len(axes)):
            axes[i].set_visible(False)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")

        plt.show()

    def plot_cumulative_returns(
        self,
        cumulative_returns: pd.DataFrame,
        title: str = "Cumulative Returns",
        figsize: Tuple[int, int] = (14, 7),
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot cumulative returns over time.

        Args:
            cumulative_returns: DataFrame with cumulative returns
            title: Chart title
            figsize: Figure size as (width, height)
            save_path: Optional path to save the figure
        """
        logger.info("Plotting cumulative returns")

        fig, ax = plt.subplots(figsize=figsize)

        for col in cumulative_returns.columns:
            ax.plot(cumulative_returns.index,
                   cumulative_returns[col] * 100,
                   linewidth=2,
                   label=col)

        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Cumulative Return (%)", fontsize=12)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")

        plt.show()

    def plot_volatility(
        self,
        volatility: pd.DataFrame,
        title: str = "Rolling Volatility",
        figsize: Tuple[int, int] = (14, 7),
        save_path: Optional[str] = None
    ) -> None:
        """
        Plot rolling volatility over time.

        Args:
            volatility: DataFrame with volatility data
            title: Chart title
            figsize: Figure size as (width, height)
            save_path: Optional path to save the figure
        """
        logger.info("Plotting volatility")

        fig, ax = plt.subplots(figsize=figsize)
        volatility.plot(ax=ax, linewidth=2)

        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Volatility", fontsize=12)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Plot saved to {save_path}")

        plt.show()

    def create_dashboard(
        self,
        analyzer,
        save_path: Optional[str] = None
    ) -> None:
        """
        Create a comprehensive dashboard with multiple plots.

        Args:
            analyzer: BankAnalyzer instance with computed metrics
            save_path: Optional path to save the figure
        """
        logger.info("Creating comprehensive dashboard")

        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # Price plot
        ax1 = fig.add_subplot(gs[0, :])
        self.data.plot(ax=ax1, linewidth=2)
        ax1.set_title("Stock Prices", fontsize=14, fontweight='bold')
        ax1.set_ylabel("Price ($)")
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='best')

        # Cumulative returns
        ax2 = fig.add_subplot(gs[1, 0])
        cum_returns = analyzer.calculate_cumulative_returns()
        (cum_returns * 100).plot(ax=ax2, linewidth=2)
        ax2.set_title("Cumulative Returns", fontsize=14, fontweight='bold')
        ax2.set_ylabel("Return (%)")
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='best', fontsize=8)

        # Correlation heatmap
        ax3 = fig.add_subplot(gs[1, 1])
        corr = analyzer.get_correlation_matrix()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, ax=ax3, cbar_kws={"shrink": 0.8})
        ax3.set_title("Correlation Matrix", fontsize=14, fontweight='bold')

        # Volatility
        ax4 = fig.add_subplot(gs[2, 0])
        volatility = analyzer.calculate_volatility()
        volatility.plot(ax=ax4, linewidth=2)
        ax4.set_title("30-Day Rolling Volatility", fontsize=14, fontweight='bold')
        ax4.set_ylabel("Volatility")
        ax4.grid(True, alpha=0.3)
        ax4.legend(loc='best', fontsize=8)

        # Summary statistics table
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.axis('tight')
        ax5.axis('off')

        stats = analyzer.get_summary_statistics().T
        table_data = stats[['mean', 'std', 'min', 'max']].round(6)

        table = ax5.table(
            cellText=table_data.values,
            rowLabels=table_data.index,
            colLabels=table_data.columns,
            cellLoc='center',
            loc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        ax5.set_title("Returns Statistics", fontsize=14, fontweight='bold', pad=20)

        plt.suptitle("Banking Stocks Analysis Dashboard",
                    fontsize=18, fontweight='bold', y=0.995)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Dashboard saved to {save_path}")

        plt.show()
