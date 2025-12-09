FROM python:3.12-slim-bookworm AS builder

ARG DEBIAN_PACKAGES="build-essential libpq5 curl"

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/home/app/.venv \
    UV_LINK_MODE=copy \
    PATH=/home/app/.venv/bin:$PATH

RUN apt-get update && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create virtualenv
RUN python -m venv $UV_PROJECT_ENVIRONMENT

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install uv inside venv and sync dependencies
RUN pip install --no-cache-dir --upgrade pip uv
RUN uv sync --frozen



FROM python:3.12-slim-bookworm AS runtime

ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/home/app/.venv \
    UV_LINK_MODE=copy \
    COVERAGE_FILE=/tmp/.coverage

# Create user
RUN useradd -ms /bin/bash app -d /home/app -u 1000

WORKDIR /app
RUN mkdir -p /app/coverage && chown app:app /app/coverage
USER app

# Copy only runtime files
COPY --chown=app:app --from=builder /home/app/.venv /home/app/.venv
COPY --chown=app:app . .

# Entry point
ENTRYPOINT ["/bin/bash","docker-entrypoint.sh"]
