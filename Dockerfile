FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run 會提供 PORT 環境變數，這裡只是為了在 CMD 中使用它
# Cloud Run will provide the PORT environment variable; we just define it here to use it in CMD.
ENV PORT=8080

# 使用 exec gunicorn 啟動應用程式，並確保它綁定到 $PORT
# Use exec gunicorn to start the app, ensuring it binds to $PORT.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:server