import logging
import pickle
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import generate_latest
from starlette.responses import Response

from API.prometheusMonitoring import metrics_middleware

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    yield

app = FastAPI(
    title="Sentiment Analysis API",
    description="Serves sentiment predictions for product reviews and exports Prometheus metrics.",
    version="1.0.0",
    lifespan=lifespan,
)
app.middleware("http")(metrics_middleware)

MODEL_FILE = Path(__file__).resolve().parent.parent / "sentiment_analysis_model.pkl"


class PredictRequest(BaseModel):
    review: str


class PredictResponse(BaseModel):
    sentiment: str
    confidence: float


def load_model():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Modello non trovato: {MODEL_FILE}")
    with open(MODEL_FILE, "rb") as f:
        return pickle.load(f)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict_sentiment(request: PredictRequest):
    review = request.review.strip()
    if not review:
        raise HTTPException(status_code=400, detail="Il campo 'review' non può essere vuoto.")

    model = app.state.model
    try:
        prediction = model.predict([review])
    except Exception as exc:
        logger.error("Errore durante la previsione: %s", exc)
        raise HTTPException(status_code=500, detail="Errore durante la previsione del sentimento.")

    sentiment = str(prediction[0])
    confidence = 1.0
    try:
        proba = model.predict_proba([review])
        confidence = float(max(proba[0]))
    except Exception:
        pass

    return PredictResponse(sentiment=sentiment, confidence=confidence)


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain; version=0.0.4; charset=utf-8")
    