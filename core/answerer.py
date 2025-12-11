# core/answerer.py
import time
from db.init_db import DB_NAME
import sqlite3
from fetchers.wiki import fetch_wiki_summary

FRESH_THRESHOLD = 12 * 3600  # 12 గం = మీకు సరిపోతే మార్చుకో

def db_get_fact(key):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value,sources,last_updated,confidence FROM facts WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row

def db_save_fact(key, value, source, confidence=0.75):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = int(time.time())
    c.execute("REPLACE INTO facts (key,value,sources,last_updated,confidence) VALUES (?,?,?,?,?)",
              (key, value, source, now, confidence))
    conn.commit()
    conn.close()

def answer_query(query_key, force_update=False):
    """
    query_key: short title for wiki, e.g. "Elon Musk", "List of billionaires"
    """
    row = db_get_fact(query_key)
    now = int(time.time())

    if row and not force_update:
        value, sources, last_updated, conf = row
        age = now - int(last_updated)
        if age <= FRESH_THRESHOLD:
            return {
                "answer": value,
                "sources": sources,
                "last_updated": last_updated,
                "confidence": conf,
                "cached": True
            }
        # else fallthrough to refresh

    # fetch from wiki
    text, src = fetch_wiki_summary(query_key)
    if text:
        db_save_fact(query_key, text, src, 0.8)
        return {
            "answer": text,
            "sources": src,
            "last_updated": int(time.time()),
            "confidence": 0.8,
            "cached": False
        }
    else:
        # fallback to cached if exists
        if row:
            value, sources, last_updated, conf = row
            return {
                "answer": value + "\n\n(note: returned cached result; live fetch failed)",
                "sources": sources,
                "last_updated": last_updated,
                "confidence": conf,
                "cached": True
            }
        return {
            "answer": "Sorry — cannot verify right now.",
            "sources": None,
            "last_updated": None,
            "confidence": 0.0,
            "cached": False
        }
