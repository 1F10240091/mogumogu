# Base image
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    tesseract-ocr-jpn \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Install Python dependencies
FROM base AS deps
COPY backend/requirements.txt backend/requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Production image
FROM base AS runner
COPY --from=deps /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY backend/app ./app
COPY backend/pyproject.toml ./

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]