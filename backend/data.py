import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_company_name(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get('longName') or info.get('shortName') or ticker
    except:
        return ticker

def get_stock_data(ticker, days=30):
    end = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(ticker, start=start, end=end)
    df = df[['Close']].reset_index()
    df.columns = ['date', 'close']
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    return df.to_dict(orient='records')

def get_news(ticker):
    company_name = get_company_name(ticker)
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={company_name}+stock&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"pageSize=50&"
        f"apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    articles = response.json().get('articles', [])
    news = []
    for article in articles:
        title = article['title'] or ''
        ticker_match = ticker.lower() in title.lower()
        name_match = company_name.lower() in title.lower()
        if not ticker_match and not name_match:
            continue
        news.append({
            'title': title,
            'date': article['publishedAt'][:10],
            'source': article['source']['name'],
            'url': article['url']
        })
    return news