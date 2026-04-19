# Stock Sentiment Dashboard

A full-stack ML web application that analyzes news sentiment for any stock ticker and visualizes the correlation between sentiment and price movement over time.

**Live Demo:** [stock-sentiment-dashboard-gamma.vercel.app](https://stock-sentiment-dashboard-gamma.vercel.app)

---

## What It Does

Users enter any stock ticker (AAPL, TSLA, NVDA, etc.) and the app:

1. Fetches 30 days of historical price data from Yahoo Finance
2. Pulls the 30 most recent news headlines from NewsAPI
3. Runs each headline through FinBERT — a BERT model fine-tuned on financial text — to classify sentiment as positive, negative, or neutral
4. Displays a dual-axis chart overlaying price movement and sentiment scores
5. Shows a scored news feed with individual sentiment badges for each article

---

## Tech Stack

**Frontend**
- React
- Recharts (data visualization)
- Deployed on Vercel

**Backend**
- Python / Flask (REST API)
- FinBERT via HuggingFace Inference API (NLP sentiment analysis)
- yfinance (stock price data)
- NewsAPI (financial news headlines)
- Deployed on Railway

---

## Architecture
   User → React Frontend (Vercel)
   ↓
   Flask REST API (Railway)
   ↓
   ┌──────┴──────┐
   Yahoo Finance   NewsAPI
   (price data)  (headlines)
   ↓
   FinBERT (HuggingFace)
   (sentiment scoring)

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/stock/<ticker>` | Returns 30 days of closing price data |
| `GET /api/sentiment/<ticker>` | Returns scored news headlines with sentiment labels |

---

## Running Locally

**Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

**Frontend**
```bash
cd frontend
npm install
npm start
```

Set the following environment variables in a `.env` file in the backend folder:
NEWS_API_KEY=your_newsapi_key
HF_TOKEN=your_huggingface_token

---

## Key Technical Decisions

- **FinBERT over general sentiment models** — Financial text contains domain-specific vocabulary (bearish, correction, overbought) that general NLP models misclassify. FinBERT was fine-tuned specifically on financial corpora.
- **HuggingFace Inference API** — Rather than loading the 400MB+ model locally, the app calls HuggingFace's hosted API, keeping the Railway deployment lightweight.
- **Separated frontend and backend** — React is served as static files via Vercel's CDN. Flask runs as a persistent process on Railway. Each platform is used for what it does best.