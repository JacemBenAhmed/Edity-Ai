FROM python:3.10-slim

# Prevents Python from writing .pyc files and enables unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Default environment
ENV HOST=0.0.0.0 \
    PORT=8000

# Expose API port
EXPOSE 8000

# Start the FastAPI app with uvicorn
CMD ["python", "server.py"]

