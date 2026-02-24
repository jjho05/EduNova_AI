# Hugging Face Spaces - FastAPI + Flutter
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF processing and PostgreSQL
# Also force IPv6 preference for Supabase free-tier connection issues
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && echo "precedence ::ffff:0:0/96  10" >> /etc/gai.conf \
    && echo "precedence ::/0  100" >> /etc/gai.conf

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for uploads
RUN mkdir -p uploads/curricula uploads/documents uploads/syllabi uploads/temp

# Expose port 7860 (Hugging Face standard)
EXPOSE 7860

# Make start script executable
RUN chmod +x start.sh

# Run the application
CMD ["./start.sh"]
