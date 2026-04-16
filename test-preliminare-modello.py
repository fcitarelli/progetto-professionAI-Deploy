# Test preliminare del modello di sentiment analysis. lo script non serve nel progetto.


import pickle
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

MODEL_FILE = Path(__file__).resolve().parent / 'sentiment_analysis_model.pkl'

if not MODEL_FILE.exists():
    raise FileNotFoundError(f"Modello non trovato: {MODEL_FILE}")

with open(MODEL_FILE, 'rb') as f:
    loaded_pipeline = pickle.load(f)

text_to_predict = ["I'm so bad"]
predicted_sentiment = loaded_pipeline.predict(text_to_predict)
print(f"Predicted sentiment: {predicted_sentiment[0]}")

try:
    proba = loaded_pipeline.predict_proba(text_to_predict)
    print(f"Confidence scores: {proba[0]}")
except AttributeError:
    print("Il modello non supporta predict_proba.")
