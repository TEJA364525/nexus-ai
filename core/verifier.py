# core/verifier.py
from difflib import SequenceMatcher

def similarity(a, b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a[:1000], b[:1000]).ratio()

def compute_confidence(texts):
    if not texts:
        return 0.0
    base = texts[0]
    scores = []
    for t in texts[1:]:
        scores.append(similarity(base, t))
    if not scores:
        return 0.6  # only 1 source found → medium confidence
    avg = sum(scores) / len(scores)
    conf = 0.5 + (avg * 0.5)  # map similarity to 0.5–1.0 range
    return min(1.0, conf)
