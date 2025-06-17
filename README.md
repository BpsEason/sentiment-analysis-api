```markdown
# AI 情感分析 API

這是一個使用 FastAPI 框架和 Hugging Face `transformers` 函式庫構建的簡單情感分析 API。它利用預訓練的 `distilbert-base-uncased-finetuned-sst-2-english` 模型對輸入文本進行正面或負面情感分類。本專案包含完整的 Docker 容器化支持，方便部署與分享。

## 功能

* **情感分析**：提供一個 API 端點，接受文本輸入並返回其情感（`positive` 或 `negative`）及對應的置信度分數。
* **健康檢查**：提供一個端點，用於檢查 API 服務的運行狀態。
* **互動式文件**：FastAPI 自動生成交互式 API 文檔（Swagger UI 和 ReDoc），便於測試和理解 API。
* **Docker 支援**：提供 Dockerfile 和 Docker Compose 配置，簡化了應用程式的構建、運行和部署。

## 技術棧

* **FastAPI**：高效能的 Python Web 框架，用於快速構建 API。
* **Hugging Face Transformers**：提供預訓練的 AI 模型，用於情感分析。
* **Pydantic**：強大的數據驗證和設定管理庫，確保 API 請求和響應的數據結構正確。
* **Uvicorn**：FastAPI 推薦的 ASGI 伺服器，用於運行應用。
* **Docker**：領先的容器化技術，實現環境隔離和便捷部署。

## 環境需求

* Python 3.8+
* Docker (可選，但強烈推薦用於部署)

## 本地開發設置

### 1. 克隆倉庫

首先，將專案倉庫克隆到您的本地機器上：

```bash
git clone [https://github.com/](https://github.com/)[您的用戶名]/sentiment-analysis-api.git
cd sentiment-analysis-api
```

### 2. 建立並激活虛擬環境 (推薦)

為了管理專案依賴，強烈建議使用 Python 虛擬環境：

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 安裝依賴

激活虛擬環境後，安裝 `requirements.txt` 中列出的所有依賴：

```bash
pip install -r requirements.txt
```

### 4. 運行應用程式

您可以在本地直接運行 FastAPI 應用程式：

```bash
# 從專案根目錄運行，Uvicorn 將會尋找 app/main.py 中的 'app' 實例
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```--reload` 參數在開發過程中非常有用，它會監聽程式碼變更並自動重載伺服器。

## Docker 部署設置 (推薦生產環境)

使用 Docker 可以更輕鬆地部署和管理應用程式，無需擔心環境依賴問題，確保生產環境與開發環境的一致性。

### 1. 安裝 Docker

確保您的系統上已安裝 Docker 和 Docker Compose。您可以從 [Docker 官方網站](https://www.docker.com/get-started) 下載並安裝 Docker Desktop。

### 2. 建構 Docker 映像

在專案根目錄下（`Dockerfile` 和 `docker-compose.yml` 所在的目錄）運行以下命令來構建 Docker 映像：

```bash
docker-compose build
```
首次構建會下載 Python 基礎映像、安裝依賴和模型，可能需要一些時間。

### 3. 運行 Docker 容器

構建完成後，啟動服務：

```bash
docker-compose up -d
```-d` 參數表示在後台運行容器，讓您的終端機保持可用。

### 4. 檢查容器日誌 (可選)

您可以查看容器的實時輸出日誌，以便於監控和調試：

```bash
docker-compose logs -f sentiment-api
```

### 5. 停止並移除容器

當您完成測試並想停止服務時，執行：

```bash
docker-compose down
```
這將停止並移除由 `docker-compose.yml` 定義的所有服務的容器和網絡。

## API 端點

API 應用程式將在 `http://localhost:8000` 上運行。

### 1. 健康檢查

* **GET** `/health`

    用於檢查 API 服務是否正常運行。

    **請求示例**:
    ```bash
    curl http://localhost:8000/health
    ```

    **回應示例**:
    ```json
    {"status": "healthy"}
    ```

### 2. 情感分析

* **POST** `/analyze-sentiment`
* **Content-Type**: `application/json`

    接受文本輸入並返回其情感分析結果。

    **請求體 (JSON)**:
    ```json
    {
      "text": "這部電影真是太棒了！我強烈推薦它。"
    }
    ```

    **請求示例 (使用 curl)**:
    ```bash
    curl -X POST http://localhost:8000/analyze-sentiment \
         -H "Content-Type: application/json" \
         -d '{"text": "我愛這個產品！"}'
    ```

    **回應示例**:
    ```json
    {
      "text": "我愛這個產品！",
      "sentiment": "positive",
      "confidence": "0.9998"
    }
    ```

    **錯誤回應 (空文本)**:
    ```json
    {
      "detail": "輸入文本不能為空"
    }
    ```

### 3. 互動式 API 文檔 (Swagger UI)

訪問 `http://localhost:8000/docs` 即可查看由 FastAPI 自動生成的交互式 API 文檔，並可以直接在頁面上測試您的 API 端點。

## 擴展建議

這個專案為您提供了一個堅實的基礎，您可以在此基礎上進行更多複雜的開發和優化：

* **添加更多 AI 模型**：根據業務需求，集成其他 Hugging Face 模型，例如文本摘要、翻譯、命名實體識別等，每個模型可以作為一個獨立的 API 端點。
* **異步處理**：對於耗時較長的 AI 推理任務，考慮使用 FastAPI 的後台任務 (`background_tasks`) 或整合像 Celery 這樣的任務佇列來實現異步處理，避免阻塞主線程，提高 API 的響應能力。
* **身份驗證與授權**：為您的 API 添加安全性，例如使用 API 鍵、OAuth2 或 JWT 等機制來驗證和授權用戶請求。
* **性能優化**：
    * **模型量化/蒸餾**：對於部署到資源有限的環境，可以對 AI 模型進行量化或蒸餾，以減小模型大小和計算量。
    * **GPU 加速**：如果您的伺服器配備了 GPU，配置 `transformers` 庫使用 GPU 進行推理可以顯著提高性能。
* **日誌記錄**：集成更詳細和結構化的日誌記錄框架（如 Python 內置的 `logging` 模組或第三方庫 `loguru`），以便於監控和排查生產環境中的問題。
* **資料庫整合**：如果您需要保存分析結果、用戶數據或進行模型版本管理，可以整合 PostgreSQL、MongoDB 或 SQLite 等資料庫。
* **CI/CD 流水線**：將應用程式的測試、構建和部署過程自動化，例如使用 GitHub Actions, GitLab CI/CD 或 Jenkins。

## 貢獻

歡迎任何形式的貢獻！如果您有任何改進建議、發現 Bug 或希望添加新功能，請隨時提交 Pull Request 或開 Issue。

## 許可證

這個專案基於 MIT 許可證。詳情請參閱 `LICENSE` 文件 (如果有的話)。
```
