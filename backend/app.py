from flask import Flask, jsonify
from data import get_stock_data, get_news
from sentiment import analyze_sentiment
import os

app = Flask(__name__)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

@app.route('/api/debug/sentiment')
def debug_sentiment():
    import requests
    hf_token = os.getenv("HF_TOKEN")
    headers = {"Authorization": f"Bearer {hf_token}"}
    try:
        response = requests.post(
            "https://router.huggingface.co/hf-inference/models/ProsusAI/finbert",
            headers=headers,
            json={"inputs": "Apple stock hits record high"}
        )
        return jsonify({
            'status_code': response.status_code,
            'response': response.text[:500]
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/debug')
def debug():
    hf_token = os.getenv("HF_TOKEN")
    news_key = os.getenv("NEWS_API_KEY")
    return jsonify({
        'hf_token_present': hf_token is not None,
        'hf_token_length': len(hf_token) if hf_token else 0,
        'news_key_present': news_key is not None,
        'news_key_length': len(news_key) if news_key else 0,
    })

@app.route('/api/stock/<ticker>')
def stock(ticker):
    try:
        data = get_stock_data(ticker.upper())
        return jsonify({'ticker': ticker.upper(), 'prices': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sentiment/<ticker>')
def sentiment(ticker):
    try:
        headlines = get_news(ticker.upper())
        scored = analyze_sentiment(headlines)
        if scored:
            avg_score = round(sum(item['score'] for item in scored) / len(scored), 3)
        else:
            avg_score = 0.0
        return jsonify({
            'ticker': ticker.upper(),
            'average_sentiment': avg_score,
            'articles': scored
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)