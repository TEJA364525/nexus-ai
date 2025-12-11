# fetchers/wiki.py
import requests

WIKI_SUMMARY_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"

def fetch_wiki_summary(title):
    """
    title: string, e.g. "Elon Musk" or "List of billionaires"
    returns: (text, source_url) or (None, None)
    """
    try:
        url = WIKI_SUMMARY_API.format(title.replace(" ", "_"))
        resp = requests.get(url, timeout=12, headers={"User-Agent":"NexusVeritas/1.0"})
        if resp.status_code == 200:
            data = resp.json()
            extract = data.get("extract")
            return extract, url
        else:
            return None, None
    except Exception as e:
        return None, None
