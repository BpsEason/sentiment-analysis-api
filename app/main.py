from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import Dict

# 初始化 FastAPI 應用
app = FastAPI(
    title="AI 情感分析 API",
    description="使用預訓練模型進行情感分析的簡單 API。",
    version="1.0.0"
)

# 初始化情感分析模型
try:
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
except Exception as e:
    raise Exception(f"情感分析模型載入失敗：{str(e)}")

# 定義輸入數據模型
class TextInput(BaseModel):
    text: str

# 健康檢查端點
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 情感分析端點
@app.post("/analyze-sentiment")
async def analyze_sentiment(input: TextInput) -> Dict[str, str]:
    try:
        # 驗證輸入文本
        if not input.text.strip():
            raise HTTPException(status_code=400, detail="輸入文本不能為空")
        
        # 執行情感分析
        result = sentiment_analyzer(input.text)[0]
        label = result['label']
        score = result['score']
        
        return {
            "text": input.text,
            "sentiment": label.lower(),
            "confidence": f"{score:.4f}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"情感分析錯誤：{str(e)}")

# 本地測試運行（僅用於非 Docker 環境）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)