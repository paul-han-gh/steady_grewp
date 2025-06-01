# Stage 1: Get the AWS CLI from the public ECR image
FROM public.ecr.aws/aws-cli/aws-cli:latest AS aws_cli_builder

# Stage 2: Install Python dependencies with UV
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS uv_builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# Cache uv.lock and pyproject.toml before copying project for leaner build
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy project now that dependencies have been installed
COPY . /app

# Final Stage: Latest Python debian image
FROM python:3.13.3 AS final

# Copy the application from the UV build stage
COPY --from=uv_builder --chown=app:app /app /app

# Add Python modules to the Path
ENV PATH="/app/.venv/bin:$PATH"

# Copy the AWS CLI from the builder
COPY --from=aws_cli_builder /usr/local/aws-cli/ /usr/local/aws-cli/

# Add the AWS CLI to the PATH
ENV PATH="/usr/local/aws-cli/v2/current/bin:$PATH"
