from flask import Flask, jsonify
from data import get_stock_data, get_news
from sentiment import analyze_sentiment

app = Flask(__name__)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

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