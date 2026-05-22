# agents/fetcher.py

import feedparser
import config

def fetch_articles():
    """
    Fetches articles from all RSS feeds defined in config.
    Returns a list of article dicts with title, link, and summary.
    """
    all_articles = []
    seen_links = set()  # Avoid duplicates across feeds

    for feed_url in config.RSS_FEEDS:
        print(f"[Fetcher] Fetching: {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:config.MAX_ARTICLES_TO_FETCH]:
            link = entry.get("link", "")

            if link in seen_links:
                continue
            seen_links.add(link)

            article = {
                "title": entry.get("title", "No Title"),
                "link": link,
                "summary": entry.get("summary", ""),
                "source": feed.feed.get("title", "Unknown Source")
            }
            all_articles.append(article)

    print(f"[Fetcher] Total unique articles fetched: {len(all_articles)}")
    return all_articles