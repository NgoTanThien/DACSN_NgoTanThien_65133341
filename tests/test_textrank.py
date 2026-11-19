"""
Bộ kiểm thử tự động (Unit Test) cho các module lõi Tuần 3:
- Kiểm thử tách câu và lọc hư từ tiếng Việt (src/preprocessing.py)
- Kiểm thử độ tương đồng và ma trận trọng số cạnh W (src/similarity.py)
- Kiểm thử chuẩn hóa ma trận Markov và thuật toán PageRank lặp hội tụ (src/pagerank.py)
"""

import unittest
from src.preprocessing import split_sentences, tokenize_and_clean
from src.similarity import compute_sentence_similarity, build_similarity_matrix
from src.pagerank import normalize_transition_matrix, run_pagerank_iterative


class TestTextRankWeek3(unittest.TestCase):
    def test_split_sentences(self):
        text = "Hôm nay trời nắng đẹp. Tôi đi học ở trường! Bạn có đi không?"
        sentences = split_sentences(text)
        self.assertEqual(len(sentences), 3)
        self.assertEqual(sentences[0], "Hôm nay trời nắng đẹp.")

    def test_tokenize_and_clean(self):
        sentence = "Hội thảo và phát triển trí tuệ nhân tạo tại Nha Trang."
        tokens = tokenize_and_clean(sentence, remove_stopwords=True)
        self.assertNotIn("và", tokens)
        self.assertNotIn("tại", tokens)
        self.assertIn("hội", tokens)
        self.assertIn("trí", tokens)

    def test_similarity_matrix_symmetry_and_zero_diagonal(self):
        tokenized = [
            ["hội", "thảo", "trí", "tuệ", "nhân", "tạo"],
            ["hội", "thảo", "công", "nghệ", "mới"],
            ["bóng", "đá", "việt", "nam"]
        ]
        matrix_w = build_similarity_matrix(tokenized)
        self.assertEqual(len(matrix_w), 3)
        for i in range(3):
            self.assertEqual(matrix_w[i][i], 0.0)
        self.assertAlmostEqual(matrix_w[0][1], matrix_w[1][0], places=6)
        self.assertGreater(matrix_w[0][1], 0.0)
        self.assertEqual(matrix_w[0][2], 0.0)

    def test_pagerank_convergence_and_dangling_node(self):
        matrix_w = [
            [0.0, 0.5, 0.0],
            [0.5, 0.0, 0.0],
            [0.0, 0.0, 0.0]  # Đỉnh cô lập (dangling node)
        ]
        matrix_m = normalize_transition_matrix(matrix_w)
        for row in matrix_m:
            self.assertAlmostEqual(sum(row), 1.0, places=6)

        scores, iterations = run_pagerank_iterative(matrix_w, damping_factor=0.85, epsilon=1e-5)
        self.assertEqual(len(scores), 3)
        self.assertAlmostEqual(sum(scores), 1.0, places=5)
        self.assertGreater(iterations, 0)
        self.assertGreater(scores[0], scores[2])


if __name__ == "__main__":
    unittest.main()
