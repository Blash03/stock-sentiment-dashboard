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
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={ticker}+stock&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize=30&"
        f"apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    articles = response.json().get('articles', [])
    news = []
    for article in articles:
        news.append({
            'title': article['title'],
            'date': article['publishedAt'][:10],
            'source': article['source']['name'],
            'url': article['url']
        })
    return news