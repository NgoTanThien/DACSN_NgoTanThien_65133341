from typing import List, Tuple, Dict, Any
from src.preprocessing import split_sentences, preprocess_document
from src.similarity import build_similarity_matrix
from src.pagerank import run_pagerank_iterative


def summarize_textrank(
    document: str,
    top_k: int = 3,
    damping_factor: float = 0.85,
    epsilon: float = 1e-5,
    max_iterations: int = 100
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Tóm tắt trích rút văn bản sử dụng giải thuật TextRank:
    1. Tiền xử lý văn bản thành các câu gốc và tập từ khóa đã làm sạch.
    2. Xây dựng ma trận tương đồng trọng số giữa các câu.
    3. Chạy thuật toán PageRank lặp đến khi hội tụ để tính điểm trọng số mỗi câu.
    4. Trích chọn Top-K câu có điểm số cao nhất.
    5. Sắp xếp lại Top-K câu theo đúng thứ tự xuất hiện ban đầu trong văn bản
       nhằm bảo toàn mạch liên kết tự nhiên của bài viết.
    """
    original_sentences, tokenized_sentences = preprocess_document(document)
    total_sentences = len(original_sentences)

    if total_sentences == 0:
        return "", []

    if total_sentences <= top_k:
        details = [
            {"index": idx, "sentence": s, "score": 1.0 / total_sentences}
            for idx, s in enumerate(original_sentences)
        ]
        return " ".join(original_sentences), details

    matrix_w = build_similarity_matrix(tokenized_sentences)
    scores, iterations = run_pagerank_iterative(
        matrix_w,
        damping_factor=damping_factor,
        epsilon=epsilon,
        max_iterations=max_iterations
    )

    ranked_items = sorted(
        enumerate(scores),
        key=lambda item: item[1],
        reverse=True
    )

    top_k_items = ranked_items[:top_k]

    # Sắp xếp lại theo chỉ số xuất hiện ban đầu (giữ thứ tự gốc)
    preserved_order_items = sorted(top_k_items, key=lambda item: item[0])

    selected_sentences = [original_sentences[idx] for idx, _ in preserved_order_items]
    summary_text = " ".join(selected_sentences)

    details = [
        {
            "original_index": idx,
            "sentence": original_sentences[idx],
            "score": score,
            "rank": rank + 1
        }
        for rank, (idx, score) in enumerate(ranked_items)
    ]

    return summary_text, details


def summarize_lead_k(document: str, top_k: int = 3) -> str:
    """
    Tóm tắt baseline Lead-K:
    Trích chọn trực tiếp K câu đầu tiên của bài báo (thường mang thông tin sapo chính).
    """
    original_sentences = split_sentences(document)
    if not original_sentences:
        return ""
    selected = original_sentences[:top_k]
    return " ".join(selected)
