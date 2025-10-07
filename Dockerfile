FROM python:3.11-slim

WORKDIR /app

# Install system packages (needed for psycopg2/Postgres, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run app (update if your entry is different)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]