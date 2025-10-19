import re

KANJI_OR_KANA = re.compile(r"[\u3040-\u30FF\u4E00-\u9FFF]{2,10}")
STOPWORDS = {"こと", "ため", "よう", "これ", "それ", "あれ", "ニュース", "速報"}


def extract_terms(text: str) -> list[str]:
    candidates = KANJI_OR_KANA.findall(text)
    out = []
    for w in candidates:
        if len(w) < 2 or w in STOPWORDS:
            continue
        out.append(w)
    return out[:50]
