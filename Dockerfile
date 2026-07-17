# syntax=docker/dockerfile:1
FROM python:3.13-slim AS builder

WORKDIR /build
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data
COPY web ./web
RUN python -m pip install --upgrade pip \
    && python -m pip wheel --wheel-dir /wheels .

FROM python:3.13-slim AS runtime

RUN useradd --create-home --uid 10001 appuser
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FDAI_HOST=0.0.0.0 \
    FDAI_PORT=3000

COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

COPY scripts/smoke_test.py ./scripts/smoke_test.py
RUN mkdir -p logs artifacts \
    && chown -R appuser:appuser /app

USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python scripts/smoke_test.py || exit 1
CMD ["python", "-m", "forward_deployed_ai_lab"]
