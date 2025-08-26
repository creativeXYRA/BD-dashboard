FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variable for the port
ENV PORT=8080

# Use gunicorn to run the app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:server