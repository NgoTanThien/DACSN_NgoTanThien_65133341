from typing import List, Tuple


def normalize_transition_matrix(matrix_w: List[List[float]]) -> List[List[float]]:
    n = len(matrix_w)
    matrix_m = [[0.0 for _ in range(n)] for _ in range(n)]

    for j in range(n):
        row_sum = sum(matrix_w[j])
        if row_sum > 0.0:
            for i in range(n):
                matrix_m[j][i] = matrix_w[j][i] / row_sum
        else:
            uniform_prob = 1.0 / n
            for i in range(n):
                matrix_m[j][i] = uniform_prob

    return matrix_m


def run_pagerank_iterative(
    matrix_w: List[List[float]],
    damping_factor: float = 0.85,
    epsilon: float = 1e-5,
    max_iterations: int = 100
) -> Tuple[List[float], int]:
    n = len(matrix_w)
    if n == 0:
        return [], 0

    matrix_m = normalize_transition_matrix(matrix_w)

    scores = [1.0 / n for _ in range(n)]
    base_score = (1.0 - damping_factor) / n
    actual_iterations = 0

    for iteration in range(1, max_iterations + 1):
        actual_iterations = iteration
        new_scores = [0.0 for _ in range(n)]

        for i in range(n):
            incoming_weighted_sum = 0.0
            for j in range(n):
                incoming_weighted_sum += matrix_m[j][i] * scores[j]
            new_scores[i] = base_score + damping_factor * incoming_weighted_sum

        diff = sum(abs(new_scores[i] - scores[i]) for i in range(n))
        scores = new_scores

        if diff < epsilon:
            break

    return scores, actual_iterations

