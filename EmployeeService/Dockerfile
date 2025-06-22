# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy service files
COPY . .

# Default command for nameko service
CMD ["nameko", "run", "--config", "config.yml", "employee"]
