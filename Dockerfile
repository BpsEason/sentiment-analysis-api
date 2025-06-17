# 使用官方 Python 精簡映像
FROM python:3.9-slim-buster

# 設定工作目錄
WORKDIR /app

# 複製並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY app/ .

# 暴露端口
EXPOSE 8000

# 定義啟動命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]