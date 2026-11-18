import re
from typing import List, Set

VIETNAMESE_STOPWORDS: Set[str] = {
    "và", "của", "là", "có", "được", "trong", "cho", "với", "các", "những",
    "một", "người", "đã", "khi", "đến", "ở", "tại", "này", "đó", "ra", "vào",
    "theo", "từ", "về", "nhiều", "trên", "cũng", "như", "để", "sẽ", "không",
    "nhưng", "vì", "nên", "nếu", "thì", "mà", "bởi", "do", "qua", "lại",
    "còn", "đang", "rất", "hơn", "nhất", "cùng", "việc", "so", "tới", "bằng"
}

def split_sentences(text: str) -> List[str]:
    if not text or not text.strip():
        return []

    normalized = re.sub(r'\r\n|\r', '\n', text.strip())
    raw_parts = re.split(r'(?<=[.?!…])\s+|\n+', normalized)

    sentences: List[str] = []
    for part in raw_parts:
        cleaned = part.strip()
        if len(cleaned) > 0:
            sentences.append(cleaned)

    return sentences

def tokenize_and_clean(sentence: str, remove_stopwords: bool = True) -> List[str]:
    lowered = sentence.lower()
    cleaned = re.sub(r'[^\w\s]', ' ', lowered)
    cleaned = re.sub(r'\d+', ' ', cleaned)
    tokens = [w.strip() for w in cleaned.split() if len(w.strip()) > 1]
    if remove_stopwords:
        tokens = [w for w in tokens if w not in VIETNAMESE_STOPWORDS]
    return tokens

def preprocess_document(text: str) -> tuple[List[str], List[List[str]]]:
    original_sentences = split_sentences(text)
    tokenized_sentences = [tokenize_and_clean(s) for s in original_sentences]
    return original_sentences, tokenized_sentences

