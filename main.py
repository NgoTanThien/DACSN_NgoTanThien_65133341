import json
import os
from src.preprocessing import preprocess_document
from src.similarity import build_similarity_matrix
from src.pagerank import run_pagerank_iterative


def format_matrix(matrix: list[list[float]]) -> str:
    """Định dạng ma trận tương đồng để hiển thị trực quan."""
    lines = []
    header = "      " + " ".join(f"S{j+1:02d}   " for j in range(len(matrix)))
    lines.append(header)
    for i, row in enumerate(matrix):
        row_str = f"S{i+1:02d} | " + " ".join(f"{val:0.4f}" for val in row)
        lines.append(row_str)
    return "\n".join(lines)


def run_week3():
    dataset_path = os.path.join(os.path.dirname(__file__), "data", "vietnamese_news_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print("=" * 80)
    print(f"CHẠY THỬ NGHIỆM TUẦN 3 - BỘ DỮ LIỆU TIN TỨC TIẾNG VIỆT ({len(dataset)} BÀI BÁO)")
    print("=" * 80)

    for idx, article in enumerate(dataset):
        sentences, tokenized = preprocess_document(article["content"])
        sim_matrix = build_similarity_matrix(tokenized)
        scores, iterations = run_pagerank_iterative(
            sim_matrix,
            damping_factor=0.85,
            epsilon=1e-5,
            max_iterations=100
        )

        if idx == 0:
            print(f"\n[BÀI BÁO MẪU: {article['id']} - {article['title']}]")
            print("\n1. Kết quả tách câu:")
            for s_idx, sent in enumerate(sentences):
                print(f"   Câu {s_idx + 1}: {sent}")

            print("\n2. Ma trận tương đồng giữa các câu (W):")
            print(format_matrix(sim_matrix))

            print(f"\n3. Kết quả PageRank lặp (Hội tụ sau {iterations} vòng lặp với epsilon = 1e-5):")
            for s_idx, score in enumerate(scores):
                print(f"   Đỉnh câu S{s_idx + 1:02d}: WS = {score:.6f}")
            print("-" * 80)
        else:
            print(f"[{article['id']}] Số câu: {len(sentences):02d} | Hội tụ PageRank sau {iterations:02d} vòng lặp")

    print("=" * 80)


if __name__ == "__main__":
    run_week3()
