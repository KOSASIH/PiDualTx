from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import tensorflow as tf
import numpy as np
import uvicorn
import aioredis
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-service")

# Pydantic schema for input features
class PredictionRequest(BaseModel):
    historical_prices: list[float] = Field(..., description="Historical Pi prices for the sequence")
    sequence_length: int = Field(..., gt=0, description="Sequence length for LSTM model")

class PredictionResponse(BaseModel):
    predicted_price: float
    confidence: float

app = FastAPI(title="Pi Price Prediction AI Service",
              description="Provides Pi Network price prediction using LSTM neural network",
              version="1.0.0")

# Enable CORS from all origins (adjust for production security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis = None

model = None

@app.on_event("startup")
async def startup_event():
    global redis
    global model
    # Initialize Redis connection
    try:
        redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
        logger.info(f"Connected to Redis at {REDIS_URL}")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        raise e

    # Load LSTM model from saved file - adjust path as needed
    try:
        model_path = os.getenv("MODEL_PATH", "backend/ai-service/src/lstm_model")
        model = tf.keras.models.load_model(model_path)
        logger.info(f"LSTM model loaded from {model_path}")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise e


@app.post("/predict", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    """
    Predict Pi price based on historical prices using LSTM model.
    The request should contain a sequence of historical prices.
    Result is cached for speed.
    """
    # Validate length of historical_prices matches sequence_length
    if len(request.historical_prices) != request.sequence_length:
        raise HTTPException(status_code=400, detail="Length of historical_prices does not match sequence_length.")

    # Create a key for caching
    cache_key = f"pi_pred:{','.join(map(str, request.historical_prices))}"

    # Try to retrieve cached prediction
    cached = await redis.get(cache_key)
    if cached:
        predicted_price, confidence = map(float, cached.split(","))
        return PredictionResponse(predicted_price=predicted_price, confidence=confidence)

    # Normalize input sequence - simple min-max scaling between 0 and 1 for demo
    prices = np.array(request.historical_prices, dtype=np.float32)
    min_price = np.min(prices)
    max_price = np.max(prices)
    if max_price == min_price:
        norm_prices = np.zeros_like(prices)
    else:
        norm_prices = (prices - min_price) / (max_price - min_price)

    # Prepare input for LSTM (batch_size=1, seq_length, features=1)
    input_seq = norm_prices.reshape((1, request.sequence_length, 1))

    try:
        pred_norm = model.predict(input_seq)
        pred_norm_val = float(pred_norm[0, 0])
    except Exception as e:
        logger.error(f"Model prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Model inference failed")

    # Denormalize prediction
    predicted_price = pred_norm_val * (max_price - min_price) + min_price

    # Dummy confidence for demo (in real cases, would be derived from model uncertainty)
    confidence = 0.95

    # Cache result for 10 minutes (600 seconds)
    await redis.set(cache_key, f"{predicted_price},{confidence}", ex=600)

    return PredictionResponse(predicted_price=predicted_price, confidence=confidence)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

