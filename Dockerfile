# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables to prevent Python from writing .pyc files and to ensure that output is sent straight to the terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Install uv and other dependencies
RUN pip install --upgrade pip && pip install uv

# Copy the pyproject.toml and uv.lock files to the working directory
COPY pyproject.toml uv.lock ./
COPY . .

# Install the dependencies specified in the pyproject.toml file using uv
RUN uv sync --frozen --no-dev

# Start the pipeline in the uv-managed environment
CMD ["uv", "run", "python", "src/dataset.py"]
