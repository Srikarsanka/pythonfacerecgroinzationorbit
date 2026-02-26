# Use Python 3.10-slim (Provides a modern debian base with new libstdc++)
FROM python:3.10-slim

# Install system dependencies needed for Pillow, InsightFace, OpenCV, and C++ Libraries
RUN apt-get update && apt-get install -y \
      libgl1-mesa-glx \
      libglib2.0-0 \
      libjpeg62-turbo \
      libpng16-16 \
      ffmpeg \
      build-essential \
      libstdc++6 \
      && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your Python backend
COPY . .

# Azure App Service routes traffic to port 8000 by default for custom containers
EXPOSE 8000

# Start FastAPI using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
