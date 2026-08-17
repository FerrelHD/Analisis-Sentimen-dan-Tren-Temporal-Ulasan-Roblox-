
import pandas as pd
from collections import Counter
import re
import numpy as np
try:
    from wordcloud import WordCloud, STOPWORDS as WC_STOPWORDS
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

STOPWORDS_ID = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "aku", "saya", "kamu", "dia", "kami", "kita", "mereka",
    "nya", "aja", "kok", "sih", "lah", "ya", "yg", "gk", "ga", "nggak", "tidak", "bukan", "tp", "tpi", "tapi",
    "buat", "untuk", "dengan", "pada", "dalam", "jadi", "udah", "sudah", "belum", "lebih", "banget", "bgt",
    "kalo", "kalau", "karena", "biar", "supaya", "agar", "sama", "juga", "lagi", "masih", "pun", "atau",
    "the", "and", "to", "of", "is", "in", "it", "this", "that", "for", "on", "with", "not"
}

def build_wordcloud_frequencies(texts, top_n=40):
    if not WORDCLOUD_AVAILABLE or not texts:
        print("WORDCLOUD_AVAILABLE is", WORDCLOUD_AVAILABLE)
        print("texts length is", len(texts))
        return {}

    all_words = []
    stopwords = set(WC_STOPWORDS) | set(STOPWORDS_ID)
    for t in texts:
        if not t:
            continue
        tokens = [w for w in re.findall(r"[a-zA-Z_]+", str(t).lower()) if len(w) >= 3 and w not in stopwords]
        all_words.extend(tokens)

    freq = dict(Counter(all_words).most_common(top_n))
    print("Word frequencies generated with", len(freq), "words")
    print("Sample:", list(freq.items())[:5])
    return freq


def test():
    # Load our data
    df = pd.read_csv("data/processed/sentiment_comparison_full.csv")
    pos_texts = df[df['sentiment_after'] == 'positif']['cleaned_content'].fillna("").astype(str).tolist()
    print("Testing positive texts...")
    word_freq = build_wordcloud_frequencies(pos_texts)
    if word_freq:
        print("Word frequencies are there!")


if __name__ == "__main__":
    test()
