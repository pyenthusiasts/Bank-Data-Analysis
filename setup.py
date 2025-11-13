"""
Setup script for the Bank Data Analysis package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="bank-data-analysis",
    version="1.0.0",
    author="Python Enthusiasts",
    author_email="",
    description="A comprehensive toolkit for analyzing banking stock data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyenthusiasts/Bank-Data-Analysis",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "yfinance>=0.2.28",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipython>=8.12.0",
            "notebook>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bank-analysis=bank_analysis.cli:main",
        ],
    },
)
