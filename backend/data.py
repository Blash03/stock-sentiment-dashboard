import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
REQUEST_TIMEOUT = 10
COMPANY_ALIASES = {
    "AAPL": "Apple",
    "AMZN": "Amazon",
    "GOOGL": "Google",
    "GOOG": "Google",
    "META": "Meta",
    "MSFT": "Microsoft",
    "NFLX": "Netflix",
    "NVDA": "Nvidia",
    "TSLA": "Tesla",
}

def get_company_name(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get('longName') or info.get('shortName') or ticker
    except:
        return ticker

def get_stock_data(ticker, days=30):
    end = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        threads=False,
        timeout=REQUEST_TIMEOUT,
    )
    if df.empty:
        raise RuntimeError(f"No price data returned for {ticker}. Yahoo Finance may be unavailable or rate-limiting requests.")
    df = df[['Close']].reset_index()
    df.columns = ['date', 'close']
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    return df.to_dict(orient='records')

def get_news(ticker, days=30, limit=30):
    end = datetime.today()
    start = end - timedelta(days=days)
    company_alias = COMPANY_ALIASES.get(ticker)
    query = f"{ticker} stock"
    response = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": query,
            "from": start.strftime("%Y-%m-%d"),
            "to": end.strftime("%Y-%m-%d"),
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100,
            "apiKey": NEWS_API_KEY,
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    articles = response.json().get('articles', [])
    news = []

    for article in articles:
        title = article['title'] or ''
        description = article.get('description') or ''
        search_text = f"{title} {description}".lower()
        published_at = article.get('publishedAt', '')
        date = published_at[:10]
        if not date:
            continue
        ticker_match = ticker.lower() in search_text
        alias_match = company_alias and company_alias.lower() in search_text
        stock_match = 'stock' in search_text
        if not ticker_match and not alias_match and not stock_match:
            continue
        news.append({
            'title': title,
            'date': date,
            'source': article['source']['name'],
            'url': article['url']
        })
        if len(news) >= limit:
            break
    return news
