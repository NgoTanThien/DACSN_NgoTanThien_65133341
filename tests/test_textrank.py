import math
import unittest
from src.preprocessing import split_sentences, tokenize_and_clean, preprocess_document
from src.similarity import compute_sentence_similarity, build_similarity_matrix
from src.pagerank import normalize_transition_matrix, run_pagerank_iterative
from src.textrank import summarize_textrank, summarize_lead_k
from src.rouge import compute_rouge_n, compute_rouge_l, evaluate_summary, rouge_tokenize


class TestTextRankWeek4(unittest.TestCase):
    """
    Bộ kiểm thử đơn vị (Unit Tests) Tuần 4 theo yêu cầu của Giảng viên hướng dẫn:
    1. Kiểm thử ma trận đối xứng và đường chéo bằng 0.
    2. Kiểm thử tổng điểm PageRank xấp xỉ 1.0 (chuẩn hóa phân phối xác suất).
    3. Kiểm thử ví dụ 3 câu tính tay có nghiệm giải tích chính xác.
    4. Kiểm thử giải thuật chọn Top-K bảo toàn thứ tự ban đầu của câu.
    5. Kiểm thử các độ đo ROUGE-1, ROUGE-2 và ROUGE-L tự cài đặt.
    6. Kiểm thử baseline Lead-K.
    """

    def test_similarity_matrix_symmetry_and_zero_diagonal(self):
        """Yêu cầu 1: Ma trận đối xứng W_ij = W_ji và đường chéo W_ii = 0."""
        tokenized = [
            ["trí", "tuệ", "nhân", "tạo", "phát", "triển"],
            ["mô", "hình", "trí", "tuệ", "nhân", "tạo", "học", "máy"],
            ["du", "lịch", "biển", "đảo", "nha", "trang"],
            ["thời", "tiết", "mát", "mẻ"]
        ]
        matrix_w = build_similarity_matrix(tokenized)
        n = len(tokenized)

        self.assertEqual(len(matrix_w), n)
        for i in range(n):
            self.assertEqual(len(matrix_w[i]), n)
            # Đường chéo chính bằng 0
            self.assertEqual(matrix_w[i][i], 0.0)
            for j in range(n):
                # Ma trận đối xứng W[i][j] == W[j][i]
                self.assertAlmostEqual(matrix_w[i][j], matrix_w[j][i], places=7)

        # Cặp câu có từ chung phải có trọng số dương
        self.assertGreater(matrix_w[0][1], 0.0)
        # Cặp câu không có từ chung phải có trọng số bằng 0
        self.assertEqual(matrix_w[0][2], 0.0)

    def test_pagerank_sum_to_one(self):
        """Yêu cầu 2: Tổng điểm PageRank trên toàn bộ đồ thị phải xấp xỉ 1.0."""
        # Giả lập ma trận tương đồng đồ thị 4 đỉnh
        matrix_w = [
            [0.0, 0.4, 0.2, 0.0],
            [0.4, 0.0, 0.5, 0.1],
            [0.2, 0.5, 0.0, 0.0],
            [0.0, 0.1, 0.0, 0.0]
        ]
        scores, iterations = run_pagerank_iterative(
            matrix_w, damping_factor=0.85, epsilon=1e-6, max_iterations=200
        )
        self.assertEqual(len(scores), 4)
        # Tổng điểm bằng 1.0 (sai số nhỏ hơn 1e-5)
        self.assertAlmostEqual(sum(scores), 1.0, places=5)
        self.assertGreater(iterations, 0)
        # Đỉnh liên kết nhiều nhất (đỉnh 1 liên kết với cả 0, 2, 3) có điểm cao nhất
        self.assertEqual(scores.index(max(scores)), 1)

    def test_three_sentences_hand_calculated(self):
        """
        Yêu cầu 3: Ví dụ 3 câu tính tay (Hand-calculated example).
        Xét 3 câu:
        S1: "học sinh đi học" -> token: ["học", "sinh", "học"] (len=3)
        S2: "học sinh thi đại học" -> token: ["học", "sinh", "thi", "đại", "học"] (len=5)
        S3: "trời mưa to" -> token: ["trời", "mưa", "to"] (len=3)

        Trọng số tương đồng:
        - Giữa S1 và S2: từ chung = {"học", "sinh"} -> overlap = 2
          Mẫu số = ln(3 + 1) + ln(5 + 1) = ln(4) + ln(6)
          W_12 = W_21 = 2 / (ln(4) + ln(6)) > 0
        - Giữa S1, S2 với S3: không có từ chung -> W_13 = W_23 = 0 (S3 là đỉnh cô lập)

        Chuẩn hóa hàng:
        - Hàng 1: [0, 1, 0]
        - Hàng 2: [1, 0, 0]
        - Hàng 3 (tổng = 0): phân phối đều [1/3, 1/3, 1/3]

        Hệ phương trình PageRank tại hội tụ (d = 0.85):
        PR(S3) = (1 - 0.85)/3 + 0.85 * (1/3) * PR(S3)
               = 0.05 / (1 - 0.85/3) = 0.15 / 2.15 = 3 / 43 ≈ 0.069767
        Do đối xứng: PR(S1) = PR(S2) = (1 - 3/43) / 2 = 20 / 43 ≈ 0.465116
        """
        tokens_s1 = ["học", "sinh", "học"]
        tokens_s2 = ["học", "sinh", "thi", "đại", "học"]
        tokens_s3 = ["trời", "mưa", "to"]

        tokenized = [tokens_s1, tokens_s2, tokens_s3]
        matrix_w = build_similarity_matrix(tokenized)

        expected_w12 = 2.0 / (math.log(4.0) + math.log(6.0))
        self.assertAlmostEqual(matrix_w[0][1], expected_w12, places=6)
        self.assertAlmostEqual(matrix_w[1][0], expected_w12, places=6)
        self.assertEqual(matrix_w[0][2], 0.0)
        self.assertEqual(matrix_w[1][2], 0.0)

        scores, iters = run_pagerank_iterative(
            matrix_w, damping_factor=0.85, epsilon=1e-6, max_iterations=200
        )

        expected_pr_s1 = 20.0 / 43.0  # ≈ 0.465116
        expected_pr_s2 = 20.0 / 43.0  # ≈ 0.465116
        expected_pr_s3 = 3.0 / 43.0   # ≈ 0.069767

        self.assertAlmostEqual(scores[0], expected_pr_s1, places=4)
        self.assertAlmostEqual(scores[1], expected_pr_s2, places=4)
        self.assertAlmostEqual(scores[2], expected_pr_s3, places=4)
        self.assertAlmostEqual(sum(scores), 1.0, places=5)

    def test_top_k_order_preservation(self):
        """Kiểm thử Top-K trích chọn giữ nguyên thứ tự ban đầu của câu."""
        text = (
            "Câu mở đầu giới thiệu bối cảnh. "
            "Câu thứ hai nêu chi tiết công nghệ trí tuệ nhân tạo học máy. "
            "Câu thứ ba nói về ứng dụng học máy trí tuệ nhân tạo trong y tế thực tế. "
            "Câu thứ tư kết luận ngắn gọn."
        )
        summary, details = summarize_textrank(text, top_k=2)

        # Lấy 2 câu được chọn trong summary
        selected_sentences = split_sentences(summary)
        self.assertEqual(len(selected_sentences), 2)

        # Kiểm tra chỉ số xuất hiện của 2 câu trong bài gốc phải theo thứ tự tăng dần
        orig_sentences = split_sentences(text)
        idx1 = orig_sentences.index(selected_sentences[0])
        idx2 = orig_sentences.index(selected_sentences[1])
        self.assertLess(idx1, idx2)

    def test_rouge_metrics(self):
        """Kiểm thử tính toán ROUGE-1, ROUGE-2 và ROUGE-L."""
        cand = "Học sinh đi học chăm chỉ"
        ref = "Học sinh đi học mỗi ngày"

        cand_tokens = rouge_tokenize(cand)  # 5 từ: học, sinh, đi, học, chăm, chỉ
        ref_tokens = rouge_tokenize(ref)    # 5 từ: học, sinh, đi, học, mỗi, ngày

        # ROUGE-1
        r1 = compute_rouge_n(cand_tokens, ref_tokens, n=1)
        # Các từ chung: học (2 lần), sinh (1 lần), đi (1 lần) => 4 từ chung
        # Recall = 4 / 6, Precision = 4 / 6 => F1 = 4 / 6 ≈ 0.6667
        self.assertAlmostEqual(r1["recall"], 4.0 / 6.0, places=4)
        self.assertAlmostEqual(r1["precision"], 4.0 / 6.0, places=4)

        # ROUGE-2
        r2 = compute_rouge_n(cand_tokens, ref_tokens, n=2)
        # Bigrams cand: (học, sinh), (sinh, đi), (đi, học), (học, chăm), (chăm, chỉ)
        # Bigrams ref: (học, sinh), (sinh, đi), (đi, học), (học, mỗi), (mỗi, ngày)
        # Trùng 3 bigrams: (học, sinh), (sinh, đi), (đi, học)
        self.assertAlmostEqual(r2["recall"], 3.0 / 5.0, places=4)
        self.assertAlmostEqual(r2["precision"], 3.0 / 5.0, places=4)

        # ROUGE-L (LCS)
        rl = compute_rouge_l(cand_tokens, ref_tokens)
        # LCS: ["học", "sinh", "đi", "học"] => độ dài 4
        self.assertAlmostEqual(rl["recall"], 4.0 / 6.0, places=4)
        self.assertAlmostEqual(rl["precision"], 4.0 / 6.0, places=4)

    def test_lead_k_baseline(self):
        """Kiểm thử phương pháp cơ sở Lead-K."""
        text = "Câu 1 là mở đầu. Câu 2 là thân bài. Câu 3 là dẫn chứng. Câu 4 là kết."
        lead_2 = summarize_lead_k(text, top_k=2)
        sentences = split_sentences(lead_2)
        self.assertEqual(len(sentences), 2)
        self.assertEqual(sentences[0], "Câu 1 là mở đầu.")
        self.assertEqual(sentences[1], "Câu 2 là thân bài.")


if __name__ == "__main__":
    unittest.main()
