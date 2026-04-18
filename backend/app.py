from flask import Flask, jsonify
from flask_cors import CORS
from data import get_stock_data, get_news
from sentiment import analyze_sentiment
import numpy as np

app = Flask(__name__)
CORS(app)

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
        # Step 1: get news headlines from data.py
        headlines = get_news(ticker.upper())
        
        # Step 2: pass headlines into sentiment.py to score them
        scored = analyze_sentiment(headlines)
        
        # Step 3: calculate overall sentiment score (average of all scores)
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

@app.route('/api/analyze/<ticker>')
def analyze(ticker):
    try:
        # This endpoint combines everything - prices + sentiment
        prices = get_stock_data(ticker.upper())
        headlines = get_news(ticker.upper())
        scored = analyze_sentiment(headlines)

        if scored:
            avg_score = round(sum(item['score'] for item in scored) / len(scored), 3)
        else:
            avg_score = 0.0

        # Calculate correlation label
        if avg_score > 0.2:
            sentiment_label = 'Positive'
        elif avg_score < -0.2:
            sentiment_label = 'Negative'
        else:
            sentiment_label = 'Neutral'

        return jsonify({
            'ticker': ticker.upper(),
            'prices': prices,
            'average_sentiment': avg_score,
            'sentiment_label': sentiment_label,
            'articles': scored
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)