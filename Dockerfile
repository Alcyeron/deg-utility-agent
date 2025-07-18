# Use an official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OPENDSS_URL=https://3.6.26.113:5000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install google-adk and other requirements
RUN pip install --upgrade pip
RUN pip install google-adk


# Copy project files
COPY multi-tool-agent/ ./multi-tool-agent/

# Expose the default ADK API server port
EXPOSE 8000

# Start the ADK API server
CMD ["adk", "api_server", "multi-tool-agent", "--host", "0.0.0.0", "--port", "8000"] 