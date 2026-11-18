import math
from typing import List
def compute_sentence_similarity(tokens_i: List[str], tokens_j: List[str]) -> float:

    if not tokens_i or not tokens_j:
        return 0.0

    set_i = set(tokens_i)
    set_j = set(tokens_j)
    common_words = set_i.intersection(set_j)
    overlap_count = len(common_words)

    if overlap_count == 0:
        return 0.0

    len_i = len(tokens_i)
    len_j = len(tokens_j)
    denominator = math.log(len_i + 1.0) + math.log(len_j + 1.0)

    if denominator <= 0.0:
        return 0.0

    return overlap_count / denominator


def build_similarity_matrix(tokenized_sentences: List[List[str]]) -> List[List[float]]:
    n = len(tokenized_sentences)
    matrix_w = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            sim = compute_sentence_similarity(tokenized_sentences[i], tokenized_sentences[j])
            matrix_w[i][j] = sim
            matrix_w[j][i] = sim
    return matrix_w

