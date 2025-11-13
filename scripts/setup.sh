#!/bin/bash
# Quick setup script for Bank Data Analysis

set -e  # Exit on error

echo "=================================="
echo "Bank Data Analysis - Setup"
echo "=================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $python_version"

# Check if Python version is >= 3.8
required_version="3.8"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${RED}✗ Python 3.8 or higher is required${NC}"
    echo "  Current version: $python_version"
    exit 1
fi

# Create virtual environment
echo
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"

# Install dependencies
echo
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Install package in development mode
echo
echo "Installing bank-analysis package..."
pip install -e .
echo "✓ Package installed"

# Install development dependencies
echo
read -p "Install development dependencies (testing, linting, etc.)? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "Installing development dependencies..."
    pip install -e ".[dev,jupyter]"
    pip install pre-commit
    echo "✓ Development dependencies installed"

    # Setup pre-commit hooks
    read -p "Setup pre-commit hooks? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        pre-commit install
        echo "✓ Pre-commit hooks installed"
    fi
fi

# Create directory structure
echo
echo "Creating directory structure..."
mkdir -p data/raw data/processed output/plots output/reports logs
touch data/raw/.gitkeep data/processed/.gitkeep output/plots/.gitkeep output/reports/.gitkeep logs/.gitkeep
echo "✓ Directory structure created"

# Run tests
echo
read -p "Run tests to verify installation? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "Running tests..."
    if pytest tests/ -v --tb=short; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
    else
        echo -e "${YELLOW}⚠ Some tests failed, but installation is complete${NC}"
    fi
fi

# Summary
echo
echo "=================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================="
echo
echo "To get started:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo
echo "  2. Run analysis:"
echo "     bank-analysis --config config.yaml"
echo
echo "  3. Or try an example:"
echo "     python examples/basic_analysis.py"
echo
echo "  4. Or use Jupyter:"
echo "     jupyter notebook notebooks/"
echo
echo "  5. View documentation:"
echo "     cat README.md"
echo "     ls docs/"
echo
echo "For more commands, run: make help"
echo

# Deactivate virtual environment
deactivate 2>/dev/null || true

echo "Happy analyzing! 🏦📈"
