# cli.py
from core.answerer import answer_query

def pretty_print(res):
    print("\n=== NEXUS VERITAS ANSWER ===\n")
    print(res["answer"][:2000])  # long text truncate if huge
    print("\n---")
    if res["sources"]:
        print("Source:", res["sources"])
    if res["last_updated"]:
        import time
        print("Last updated (epoch):", res["last_updated"], "=>", time.ctime(res["last_updated"]))
    print("Confidence:", res["confidence"])
    print("From cache:", res["cached"])
    print("\n===========================\n")

def main():
    print("Nexus Veritas CLI — type 'exit' to quit")
    while True:
        q = input("Ask (e.g. 'Elon Musk' or 'List of billionaires') > ").strip()
        if not q:
            continue
        if q.lower() in ("exit","quit"):
            break
        res = answer_query(q)
        pretty_print(res)

if __name__ == "__main__":
    main()
