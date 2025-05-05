# Base image
FROM python:3.12-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
COPY requirements/ ./requirements/
RUN pip install --upgrade pip && \
    pip install -r requirements/base.txt

# Copy code
COPY . .

# Give permissions to scripts (if using entrypoint.sh)
# RUN chmod +x ./entrypoint.sh

# Set entry point
# ENTRYPOINT ["./entrypoint.sh"]
