# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# The application is started with gunicorn, which listens on the port provided by Cloud Run
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:server

