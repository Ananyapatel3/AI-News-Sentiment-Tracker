import feedparser
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# ---------------- Google News RSS ----------------
def fetch_articles_from_rss(query, max_articles):
    feed_url = f"https://news.google.com/rss/search?q={query}"
    feed = feedparser.parse(feed_url)

    articles = []
    for entry in feed.entries[:max_articles]:
        articles.append({
            "title": entry.title,
            "content": entry.get("summary", "")
        })

    return articles

# ---------------- NewsAPI ----------------
def fetch_articles_from_newsapi(query, max_articles, api_key):
    if not api_key:
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": max_articles,
        "language": "en",
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = []
    for item in data.get("articles", []):
        articles.append({
            "title": item.get("title", ""),
            "content": item.get("description") or ""
        })

    return articles

# ---------------- Sentiment ----------------
def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# ---------------- Semantic Mapping ----------------
def semantic_mapping(row):
    compound = row["compound"]

    if compound >= 0.05:
        soul = "Positive Soul"
        materialism = "Positive Materialism"
        actions = "Innovating, Nurturing, Internal Transformation"
    elif compound <= -0.05:
        soul = "Negative Soul"
        materialism = "Negative Materialism"
        actions = "Owning, Acting, Dominating"
    else:
        soul = "Neutral"
        materialism = "Neutral"
        actions = "Probing, Scoping"

    return {
        "soul": soul,
        "materialism": materialism,
        "actions": actions,
        "confidence": abs(compound)
    }
