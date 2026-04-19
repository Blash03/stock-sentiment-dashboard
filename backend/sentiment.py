import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/ProsusAI/finbert"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def _score_prediction(item):
    best = max(item, key=lambda entry: entry["score"])
    label = best["label"].lower()
    score = best["score"]
    if label == "positive":
        sentiment_score = round(score, 3)
    elif label == "negative":
        sentiment_score = round(-score, 3)
    else:
        sentiment_score = 0.0
    return label, sentiment_score

def analyze_sentiment(headlines):
    if not headlines or not HF_TOKEN:
        return []

    trimmed = [item for item in headlines if item.get("title")][:10]
    if not trimmed:
        return []

    payload = {"inputs": [item["title"][:512] for item in trimmed]}

    results = []
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

        for meta, prediction in zip(trimmed, data):
            if not isinstance(prediction, list) or not prediction:
                continue
            label, sentiment_score = _score_prediction(prediction)
            results.append({
                "title": meta["title"],
                "date": meta["date"],
                "source": meta["source"],
                "url": meta["url"],
                "sentiment": label,
                "score": sentiment_score,
            })
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return []

    return results