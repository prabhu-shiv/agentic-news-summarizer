# config.example.py
# Copy this file to config.py and fill in your API key

COHERE_API_KEY = "your_cohere_api_key_here"

RELEVANCE_THRESHOLD = 7
MAX_ARTICLES_TO_FETCH = 10
OUTPUT_DIR = "output"

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=Intel+AI&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=AI+semiconductor+Intel&hl=en-US&gl=US&ceid=US:en",
    "https://feeds.feedburner.com/venturebeat/SZYF",
]