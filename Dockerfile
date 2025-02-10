# Step 1: Use an official Python image as the base image
FROM python:3.9-slim

# Step 2: Install system dependencies for building dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory to /app
WORKDIR /app

# Step 4: Copy the application files to the /app directory
COPY . /app

# Step 5: Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Step 6: Expose port 8000 to the outside world
EXPOSE 8000

# Step 7: Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
