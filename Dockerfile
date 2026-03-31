# Hugging Face Spaces - FastAPI + Flutter
FROM python:3.11-slim

# Set working directory to root /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && echo "precedence ::ffff:0:0/96  10" >> /etc/gai.conf \
    && echo "precedence ::/0  100" >> /etc/gai.conf

# Copy backend requirements first
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy entire project
COPY . .

# Set working directory to backend
WORKDIR /app/backend

# Create uploads directories
RUN mkdir -p uploads/curricula uploads/documents uploads/syllabi uploads/temp

# HF Port
EXPOSE 7860

# Execute
RUN chmod +x start.sh
CMD ["./start.sh"]
