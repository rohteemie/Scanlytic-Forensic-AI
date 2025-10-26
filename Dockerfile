# Scanlytic-ForensicAI Dockerfile
# 
# This Dockerfile creates a containerized environment for running
# Scanlytic-ForensicAI for digital forensic file analysis.
#
# Build: docker build -t scanlytic-forensicai .
# Run: docker run -v /path/to/files:/data scanlytic-forensicai analyze /data

FROM python:3.11-slim

LABEL maintainer="Rotimi Owolabi"
LABEL description="Scanlytic-ForensicAI - Automated File Classification and Malicious Intent Scoring"
LABEL version="0.1.0"

# Set working directory
WORKDIR /app

# Install system dependencies
# libmagic1: Required for python-magic (file type detection)
# file: Provides the magic database
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libmagic1 \
    file && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
COPY requirements-dev.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install --no-cache-dir -e .

# Create directory for data and reports
RUN mkdir -p /data /reports

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SCANLYTIC_LOGGING_LEVEL=INFO

# Default command shows help
ENTRYPOINT ["scanlytic"]
CMD ["--help"]

# Volume for mounting files to analyze
VOLUME ["/data", "/reports"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD scanlytic --version || exit 1
