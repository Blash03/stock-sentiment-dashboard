import requests
import os
import json

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/ProsusAI/finbert"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def analyze_sentiment(headlines):
    results = []
    for item in headlines:
        title = item['title']
        if not title:
            continue
        try:
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={"inputs": title[:512]}
            )
            # Handle response whether it comes back as string or parsed
            raw = response.text
            data = json.loads(raw)
            
            if isinstance(data, list) and len(data) > 0:
                inner = data[0]
                if isinstance(inner, list):
                    scores = inner
                else:
                    scores = data
                best = max(scores, key=lambda x: x['score'])
                label = best['label'].lower()
                score = best['score']
                if label == 'positive':
                    sentiment_score = round(score, 3)
                elif label == 'negative':
                    sentiment_score = round(-score, 3)
                else:
                    sentiment_score = 0.0
                results.append({
                    'title': title,
                    'date': item['date'],
                    'source': item['source'],
                    'url': item['url'],
                    'sentiment': label,
                    'score': sentiment_score
                })
        except Exception as e:
            continue
    return results