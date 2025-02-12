# Use an official Python 3.12 slim image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies with no cache to reduce image size
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Start the FastAPI application using Uvicorn on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 