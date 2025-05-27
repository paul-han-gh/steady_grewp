# Python 3.13 with UV
FROM ghcr.io/astral-sh/uv:python3.13-bookworm

# Install Linux packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       unzip \
       curl \
       ca-certificates \
       procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN curl -fsSL "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip" \
    && unzip awscli-bundle.zip \
    && ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws \
    && rm -f awscli-bundle.zip \
    && rm -rf awscli-bundle

# Remove the UV copy-mode warning
ENV UV_LINK_MODE=copy

# Include pyproject.toml for upcoming `uv sync` command
WORKDIR /app
COPY pyproject.toml ./

# Install Python packages
RUN uv sync
