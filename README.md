# AI News Sentiment Tracker

This project fetches real-time market and startup news using Google News RSS and NewsAPI.
It performs sentiment analysis using NLTK VADER and displays results in a Streamlit dashboard with advanced features including sentiment distribution charts and CSV export.

## Setup

1. Clone the repository and navigate to the project directory.
2. Install dependencies: `pip install -r requirements.txt`

## API Key Setup

To use NewsAPI for fetching articles:

1. Sign up for a free API key at [NewsAPI](https://newsapi.org/).
2. Create a `.env` file in the project root.
3. Add your API key: `NEWSAPI_KEY=your_actual_api_key_here`

If the API key is not set in the `.env` file, you can enter it manually in the app when selecting NewsAPI as the source.

## Run Project

streamlit run app.py
