# core/update_now.py
import sys
from core.answerer import answer_query

def main():
    if len(sys.argv) < 2:
        print("Usage: python core/update_now.py \"Query Key\"")
        return
    key = sys.argv[1]
    res = answer_query(key, force_update=True)
    print("=== FORCE UPDATE RESULT ===")
    print("Answer:", res.get("answer")[:2000])
    print("Sources:", res.get("sources"))
    print("Last updated:", res.get("last_updated"))
    print("Confidence:", res.get("confidence"))
    print("Cached:", res.get("cached"))

if __name__ == "__main__":
    main()
