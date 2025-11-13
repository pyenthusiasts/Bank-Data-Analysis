# Contributing to Bank Data Analysis

Thank you for your interest in contributing to Bank Data Analysis! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Our Standards

- Be respectful and constructive in communication
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of financial concepts
- Familiarity with pandas, matplotlib, and pytest

### Finding Issues to Work On

- Check the [Issues](https://github.com/pyenthusiasts/Bank-Data-Analysis/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to let others know you're working on it

## Development Setup

1. **Fork the repository**

   Click the "Fork" button on GitHub to create your own copy.

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/Bank-Data-Analysis.git
   cd Bank-Data-Analysis
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/pyenthusiasts/Bank-Data-Analysis.git
   ```

4. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

6. **Verify installation**

   ```bash
   pytest
   python examples/basic_analysis.py
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues in existing code
- **New features**: Add new functionality
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Examples**: Create new example scripts
- **Performance**: Optimize existing code
- **Refactoring**: Improve code quality

### Reporting Bugs

When reporting bugs, please include:

- Python version
- Package version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (full traceback)
- Minimal code example

**Example:**

```markdown
**Environment:**
- Python 3.10
- Bank Data Analysis v1.0.0
- Ubuntu 22.04

**Description:**
Fetching data for ticker 'XYZ' raises ValueError.

**Steps to Reproduce:**
1. Create fetcher with ticker 'XYZ'
2. Call fetch_data()
3. Error occurs

**Expected:** Data should be fetched or informative error message
**Actual:** ValueError with unclear message

**Code:**
\```python
fetcher = BankDataFetcher(tickers=['XYZ'])
data = fetcher.fetch_data()
\```

**Error:**
\```
ValueError: No data retrieved
\```
```

### Suggesting Features

When suggesting features:

- Explain the use case
- Describe the expected behavior
- Provide examples if possible
- Consider backward compatibility

## Coding Standards

### Style Guide

We follow PEP 8 with some modifications:

- Line length: 100 characters
- Use double quotes for strings
- Use type hints for function signatures

### Code Formatting

Use `black` for code formatting:

```bash
black src/ tests/ examples/
```

### Linting

Use `flake8` for linting:

```bash
flake8 src/ tests/ examples/
```

### Type Checking

Use `mypy` for type checking:

```bash
mypy src/
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `BankAnalyzer`)
- **Functions/Methods**: snake_case (e.g., `calculate_returns`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_TICKERS`)
- **Private members**: prefix with `_` (e.g., `_internal_method`)

### Example Code

```python
from typing import List, Optional
import pandas as pd


class MyAnalyzer:
    """
    Short description of the class.

    Longer description if needed.

    Attributes:
        data: Description of data attribute
    """

    DEFAULT_WINDOW = 30

    def __init__(self, data: pd.DataFrame):
        """
        Initialize the analyzer.

        Args:
            data: DataFrame containing stock data
        """
        self.data = data

    def calculate_metric(
        self,
        window: int = DEFAULT_WINDOW,
        method: str = "default"
    ) -> pd.DataFrame:
        """
        Calculate a custom metric.

        Args:
            window: Rolling window size
            method: Calculation method

        Returns:
            DataFrame with calculated metrics

        Raises:
            ValueError: If window is invalid
        """
        if window <= 0:
            raise ValueError("Window must be positive")

        # Implementation here
        result = self.data.rolling(window=window).mean()
        return result
```

## Testing

### Writing Tests

- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use fixtures for common setup
- Aim for >80% code coverage

### Example Test

```python
import pytest
import pandas as pd
from bank_analysis import BankAnalyzer


class TestBankAnalyzer:
    """Test cases for BankAnalyzer."""

    def test_calculate_returns(self, sample_data):
        """Test returns calculation."""
        analyzer = BankAnalyzer(sample_data)
        returns = analyzer.calculate_returns()

        assert isinstance(returns, pd.DataFrame)
        assert len(returns) == len(sample_data) - 1

    def test_invalid_method_raises_error(self, sample_data):
        """Test that invalid method raises ValueError."""
        analyzer = BankAnalyzer(sample_data)

        with pytest.raises(ValueError):
            analyzer.calculate_returns(method='invalid')
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/bank_analysis --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py

# Run specific test
pytest tests/test_analyzer.py::TestBankAnalyzer::test_calculate_returns

# Run with verbose output
pytest -v
```

### Test Coverage

Maintain test coverage above 80%:

```bash
pytest --cov=src/bank_analysis --cov-report=term-missing
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Short description of function.

    Longer description if needed. Explain what the function does,
    any important details, etc.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
        TypeError: When param1 is not a string

    Example:
        >>> my_function("test", 5)
        True
    """
```

### Updating Documentation

When adding features:

1. Update relevant docstrings
2. Update API.md if adding new public methods
3. Update TUTORIAL.md if adding user-facing features
4. Update FAQ.md if addressing common questions
5. Update README.md if changing core functionality

## Submitting Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-new-metric` - New features
- `fix/correlation-bug` - Bug fixes
- `docs/update-tutorial` - Documentation
- `test/add-analyzer-tests` - Tests
- `refactor/simplify-fetcher` - Refactoring

### Commit Messages

Write clear, descriptive commit messages:

```
Add Sortino ratio calculation to analyzer

- Implement calculate_sortino_ratio() method
- Add tests for Sortino ratio
- Update documentation
- Add example usage

Closes #123
```

Format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (if needed)
- Reference issues/PRs

### Pull Request Process

1. **Create a branch**

   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**

   - Write code
   - Add tests
   - Update documentation
   - Run tests locally

3. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add my new feature"
   ```

4. **Update your branch**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Push to your fork**

   ```bash
   git push origin feature/my-new-feature
   ```

6. **Create Pull Request**

   - Go to GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Submit!

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Tests
- [ ] Refactoring

## Changes Made
- Change 1
- Change 2

## Testing
Describe how you tested these changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
- [ ] No linting errors

## Related Issues
Closes #123
```

## Review Process

### What to Expect

- Initial review within 3-5 days
- Constructive feedback from maintainers
- Possible requests for changes
- Approval when ready
- Merge to main branch

### Responding to Feedback

- Address all comments
- Push new commits to same branch
- Request re-review when ready
- Be patient and professional

### After Merge

- Your contribution will be credited
- Delete your branch
- Pull latest changes from upstream

## Development Guidelines

### Adding New Features

1. Discuss in an issue first
2. Design the API
3. Write tests (TDD approach)
4. Implement the feature
5. Update documentation
6. Submit PR

### Code Review Checklist

Before submitting, verify:

- [ ] Code is clean and readable
- [ ] Type hints are present
- [ ] Docstrings are complete
- [ ] Tests are comprehensive
- [ ] Tests pass locally
- [ ] No linting errors
- [ ] Documentation is updated
- [ ] Examples are provided (if applicable)
- [ ] Backward compatibility is maintained

## Getting Help

- **Questions**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Real-time help**: Check if there's a community chat

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to Bank Data Analysis! 🎉
