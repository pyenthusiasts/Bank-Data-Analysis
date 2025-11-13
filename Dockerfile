# Bank Data Analysis - Docker Image

FROM python:3.11-slim

# Set metadata
LABEL maintainer="Python Enthusiasts"
LABEL description="Bank Data Analysis - Financial stock analysis toolkit"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy package files
COPY setup.py pyproject.toml README.md ./
COPY src/ ./src/
COPY config.yaml ./

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data/raw data/processed output/plots output/reports logs

# Copy examples and notebooks
COPY examples/ ./examples/
COPY notebooks/ ./notebooks/

# Set default command
CMD ["bank-analysis", "--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import bank_analysis; print('healthy')" || exit 1

# Expose port for Jupyter (if needed)
EXPOSE 8888

# Add labels for better organization
LABEL org.opencontainers.image.source="https://github.com/pyenthusiasts/Bank-Data-Analysis"
LABEL org.opencontainers.image.url="https://github.com/pyenthusiasts/Bank-Data-Analysis"
LABEL org.opencontainers.image.documentation="https://github.com/pyenthusiasts/Bank-Data-Analysis/tree/main/docs"
LABEL org.opencontainers.image.licenses="MIT"
