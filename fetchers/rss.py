# fetchers/rss.py
import feedparser

def fetch_feed_titles(feed_url, limit=5):
    """
    Returns list of (title, link) tuples from an RSS feed.
    """
    d = feedparser.parse(feed_url)
    items = []
    for entry in d.entries[:limit]:
        title = entry.title if 'title' in entry else ''
        link = entry.link if 'link' in entry else ''
        items.append((title, link))
    return items
