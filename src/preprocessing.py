import re
from typing import List, Set

VIETNAMESE_STOPWORDS: Set[str] = {
    "và", "của", "là", "có", "được", "trong", "cho", "với", "các", "những",
    "một", "người", "đã", "khi", "đến", "ở", "tại", "này", "đó", "ra", "vào",
    "theo", "từ", "về", "nhiều", "trên", "cũng", "như", "để", "sẽ", "không",
    "nhưng", "vì", "nên", "nếu", "thì", "mà", "bởi", "do", "qua", "lại",
    "còn", "đang", "rất", "hơn", "nhất", "cùng", "việc", "so", "tới", "bằng"
}

COMMON_ABBREVIATIONS: List[str] = [
    "TP", "TAND", "VKSND", "CSGT", "CSĐT", "SN", "ThS", "TS", "PGS", "GS", "BS",
    "HĐXX", "UBND", "HĐND", "QL", "BTV", "PV", "SN", "TW"
]


def split_sentences(text: str) -> List[str]:
    """
    Tách văn bản thành danh sách các câu tiếng Việt hoàn chỉnh:
    - Bảo vệ các từ viết tắt phổ biến (TP., TAND., SN., TS., v.v.).
    - Bảo vệ tên viết tắt có dấu chấm (N.V. B., Th., Tr.).
    - Bảo vệ số thập phân (3.2 tỷ, 1.5 triệu).
    - Tách theo các dấu kết thúc câu chuẩn (. ? ! …) hoặc xuống dòng.
    - Loại bỏ các dòng chú thích ảnh hoặc tàn dư ngắn không phải là câu văn.
    """
    if not text or not text.strip():
        return []

    normalized = re.sub(r"\r\n|\r", "\n", text.strip())

    # Bảo vệ các từ viết tắt chuyên môn
    for ab in COMMON_ABBREVIATIONS:
        normalized = re.sub(rf"\b{ab}\.\s*", f"{ab}<DOT> ", normalized, flags=re.IGNORECASE)

    # Bảo vệ tên viết tắt và chữ cái đầu (ví dụ: N.V. B., Th., Tr.)
    normalized = re.sub(r"\b([A-ZĐ][a-zà-ỹ]?)\.\s*", r"\1<DOT> ", normalized)

    # Bảo vệ số thập phân (3.2 tỷ, 1.5 triệu)
    normalized = re.sub(r"(\d+)\.(\d+)", r"\1<NUMDOT>\2", normalized)

    # Tách câu
    raw_parts = re.split(r"(?<=[.?!…])\s+|\n+", normalized)

    sentences: List[str] = []
    for part in raw_parts:
        cleaned = part.replace("<DOT>", ".").replace("<NUMDOT>", ".").strip()
        # Loại bỏ chú thích ảnh nếu có
        cleaned = re.sub(r"^\s*[(]?(Ảnh|Nguồn|Theo|Ảnh minh họa):.*$", "", cleaned).strip()
        # Một câu văn tiếng Việt hoàn chỉnh phải có ít nhất 15 ký tự và chứa khoảng trắng
        if len(cleaned) >= 15 and " " in cleaned:
            sentences.append(cleaned)

    return sentences


def tokenize_and_clean(sentence: str, remove_stopwords: bool = True) -> List[str]:
    lowered = sentence.lower()
    cleaned = re.sub(r"[^\w\s]", " ", lowered)
    cleaned = re.sub(r"\d+", " ", cleaned)
    tokens = [w.strip() for w in cleaned.split() if len(w.strip()) > 1]
    if remove_stopwords:
        tokens = [w for w in tokens if w not in VIETNAMESE_STOPWORDS]
    return tokens


def preprocess_document(text: str) -> tuple[List[str], List[List[str]]]:
    original_sentences = split_sentences(text)
    tokenized_sentences = [tokenize_and_clean(s) for s in original_sentences]
    return original_sentences, tokenized_sentences

