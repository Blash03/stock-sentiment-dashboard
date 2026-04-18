from transformers import pipeline

# Load FinBERT once when the file is imported
finbert = pipeline(
    "text-classification",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert"
)

def analyze_sentiment(headlines):
    results = []
    
    for item in headlines:
        title = item['title']
        
        # Skip if title is missing
        if not title:
            continue
        
        # Run headline through FinBERT (cap at 512 tokens - model limit)
        output = finbert(title[:512])[0]
        
        label = output['label']    # 'positive', 'negative', or 'neutral'
        score = output['score']    # confidence between 0 and 1
        
        # Convert to -1 to +1 scale
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
    
    return results