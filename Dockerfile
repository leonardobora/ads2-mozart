# Multi-stage Dockerfile for ADS2 Mozart CNN Project

# Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.9-slim as production

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash mozart && \
    chown -R mozart:mozart /app
USER mozart

# Set Python path
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import src; print('✅ Health check passed')" || exit 1

# Default command
CMD ["python", "-c", "print('🎵 ADS2 Mozart CNN - Ready to classify music content!')"]

# Development stage (for local development)
FROM production as development

USER root

# Install development dependencies
RUN pip install --no-cache-dir \
    jupyter \
    ipykernel \
    black \
    flake8 \
    mypy \
    pytest \
    pytest-cov

# Switch back to mozart user
USER mozart

# Expose Jupyter port
EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]