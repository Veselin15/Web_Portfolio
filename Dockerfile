# 1. Use the official Python image (lightweight and fast)
FROM python:3.10-slim-bookworm

# 2. Install system dependencies (required for PostgreSQL and others)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy requirements and install them (leveraging Docker cache)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire project code
COPY . /app/

# 6. Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default command (will be overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
