import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_stock_data(ticker, days=30):
    end = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(ticker, start=start, end=end)
    df = df[['Close']].reset_index()
    df.columns = ['date', 'close']
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    return df.to_dict(orient='records')

def get_news(ticker):
    if not NEWS_API_KEY:
        return []

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={ticker}+stock&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize=12&"
        f"apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url, timeout=12)
        response.raise_for_status()
        articles = response.json().get('articles', [])
    except requests.RequestException:
        return []

    news = []
    for article in articles:
        title = article.get('title')
        published_at = article.get('publishedAt')
        source = article.get('source', {}).get('name')
        article_url = article.get('url')
        if not title or not published_at:
            continue

        news.append({
            'title': title,
            'date': published_at[:10],
            'source': source or 'Unknown',
            'url': article_url or ''
        })
    return news