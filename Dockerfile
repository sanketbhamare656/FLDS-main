# Use the official Python image as base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for dlib
RUN apt-get update && apt-get install -y \
    cmake \
    libboost-all-dev \
    libopencv-dev \
    libopenblas-dev \
    liblapack-dev \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
