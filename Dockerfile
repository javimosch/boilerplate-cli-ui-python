# Multi-stage Dockerfile for agent-first Python CLI
FROM python:3.10-slim as builder

WORKDIR /app

# Copy project files
COPY pyproject.toml ./
COPY requirements.txt ./
COPY src/ ./src/
COPY schemas/ ./schemas/

# Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.10-slim

WORKDIR /app

# Copy from builder
COPY --from=builder /app /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BOILERPLATE_PORT=8080
ENV BOILERPLATE_HOST=0.0.0.0
ENV BOILERPLATE_LOG_LEVEL=INFO
ENV BOILERPLATE_NO_INTERACTIVE=1
ENV NO_COLOR=1

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -m src.main status || exit 1

# Default command
CMD ["python", "-m", "src.main"]