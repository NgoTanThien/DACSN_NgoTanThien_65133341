import re
from typing import List, Tuple, Dict, Counter


def rouge_tokenize(text: str) -> List[str]:
    """
    Tách từ phục vụ đánh giá ROUGE: chuyển chữ thường và tách theo từ.
    """
    if not text:
        return []
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = [w.strip() for w in cleaned.split() if w.strip()]
    return tokens


def get_ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
    """Tạo danh sách n-gram từ dãy tokens."""
    if len(tokens) < n:
        return []
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def compute_rouge_n(
    cand_tokens: List[str],
    ref_tokens: List[str],
    n: int = 1
) -> Dict[str, float]:
    """
    Tính ROUGE-N (N=1 hoặc N=2) tự cài đặt:
    Recall = Overlap_count / len(ref_ngrams)
    Precision = Overlap_count / len(cand_ngrams)
    F1 = 2 * P * R / (P + R)
    """
    cand_ngrams = get_ngrams(cand_tokens, n)
    ref_ngrams = get_ngrams(ref_tokens, n)

    if not ref_ngrams or not cand_ngrams:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    cand_counter = Counter(cand_ngrams)
    ref_counter = Counter(ref_ngrams)

    overlap = 0
    for ngram, count in cand_counter.items():
        if ngram in ref_counter:
            overlap += min(count, ref_counter[ngram])

    recall = overlap / len(ref_ngrams)
    precision = overlap / len(cand_ngrams)

    if precision + recall > 0.0:
        f1 = (2.0 * precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def compute_lcs_length(tokens_a: List[str], tokens_b: List[str]) -> int:
    """
    Tính độ dài chuỗi con chung dài nhất (Longest Common Subsequence - LCS)
    sử dụng quy hoạch động.
    """
    m = len(tokens_a)
    n = len(tokens_b)
    if m == 0 or n == 0:
        return 0

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if tokens_a[i - 1] == tokens_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def compute_rouge_l(
    cand_tokens: List[str],
    ref_tokens: List[str]
) -> Dict[str, float]:
    """
    Tính ROUGE-L dựa trên LCS tự cài đặt:
    Recall = LCS / len(ref_tokens)
    Precision = LCS / len(cand_tokens)
    F1 = 2 * P * R / (P + R)
    """
    m = len(ref_tokens)
    n = len(cand_tokens)

    if m == 0 or n == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    lcs_len = compute_lcs_length(ref_tokens, cand_tokens)

    recall = lcs_len / m
    precision = lcs_len / n

    if precision + recall > 0.0:
        f1 = (2.0 * precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def evaluate_summary(candidate: str, reference: str) -> Dict[str, Dict[str, float]]:
    """
    Đánh giá tóm tắt dự đoán so với tóm tắt tham chiếu theo bộ chỉ số ROUGE-1, ROUGE-2, ROUGE-L.
    """
    cand_tokens = rouge_tokenize(candidate)
    ref_tokens = rouge_tokenize(reference)

    rouge_1 = compute_rouge_n(cand_tokens, ref_tokens, n=1)
    rouge_2 = compute_rouge_n(cand_tokens, ref_tokens, n=2)
    rouge_l = compute_rouge_l(cand_tokens, ref_tokens)

    return {
        "rouge_1": rouge_1,
        "rouge_2": rouge_2,
        "rouge_l": rouge_l
    }
