# 從一個包含 Python 3.9 的映像檔開始
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 將 requirements.txt 複製到容器中
COPY requirements.txt .

# 安裝所有依賴項
RUN pip install --no-cache-dir -r requirements.txt

# 將應用程式程式碼複製到容器中
COPY . .

# 定義環境變數，以確保 Dash 應用程式在 Cloud Run 上運行
ENV PORT=8080

# 告訴容器當它啟動時，要運行哪個指令
CMD ["python", "app.py"]