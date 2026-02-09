FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Make scripts executable
RUN chmod +x scripts/wait-for-db.sh scripts/run_pipeline.sh

CMD ["tail", "-f", "/dev/null"]
