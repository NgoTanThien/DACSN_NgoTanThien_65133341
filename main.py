import json
import os
from src.textrank import summarize_textrank, summarize_lead_k
from src.rouge import evaluate_summary
from src.preprocessing import split_sentences


def run_week4_evaluation():
    dataset_path = os.path.join(os.path.dirname(__file__), "data", "vietnamese_news_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print("=" * 90)
    print("CHƯƠNG TRÌNH ĐÁNH GIÁ TÓM TẮT VĂN BẢN TIẾNG VIỆT - TUẦN 4")
    print(f"Dữ liệu: {len(dataset)} bài báo thật từ VietNews (mỗi bài >= 10 câu)")
    print("Mô hình so sánh: TextRank (Top-3 giữ thứ tự gốc) vs Baseline Lead-3")
    print("Độ đo tự cài đặt: ROUGE-1, ROUGE-2, ROUGE-L (Precision, Recall, F1-Score)")
    print("=" * 90)

    tr_r1_f1_list, tr_r2_f1_list, tr_rl_f1_list = [], [], []
    ld_r1_f1_list, ld_r2_f1_list, ld_rl_f1_list = [], [], []

    # Hiển thị chi tiết bài mẫu đầu tiên
    sample_article = dataset[0]
    sample_content = sample_article["content"]
    sample_ref = sample_article["reference_summary"]

    sample_tr_summary, sample_tr_details = summarize_textrank(sample_content, top_k=3)
    sample_lead_summary = summarize_lead_k(sample_content, top_k=3)

    print(f"\n[MINH HỌA CHI TIẾT BÀI BÁO {sample_article['id']}]")
    print(f"Tiêu đề: {sample_article['title']}")
    print(f"Nguồn: {sample_article['source']}")
    print(f"Tổng số câu: {sample_article['sentence_count']}")

    print("\n--- TÓM TẮT THAM CHIẾU (REFERENCE SUMMARY / BẢN GỐC): ---")
    print(sample_ref)

    print("\n--- TÓM TẮT BẰNG PAGERANK TEXTRANK (TOP-3, GIỮ THỨ TỰ GỐC): ---")
    print(sample_tr_summary)

    print("\n--- TÓM TẮT BẰNG BASELINE LEAD-3 (3 CÂU ĐẦU TIÊN): ---")
    print(sample_lead_summary)

    sample_tr_eval = evaluate_summary(sample_tr_summary, sample_ref)
    sample_ld_eval = evaluate_summary(sample_lead_summary, sample_ref)

    print("\n--- ĐIỂM ROUGE TRÊN BÀI MẪU: ---")
    print(f"TextRank: ROUGE-1 F1={sample_tr_eval['rouge_1']['f1']:.4f} | "
          f"ROUGE-2 F1={sample_tr_eval['rouge_2']['f1']:.4f} | "
          f"ROUGE-L F1={sample_tr_eval['rouge_l']['f1']:.4f}")
    print(f"Lead-3  : ROUGE-1 F1={sample_ld_eval['rouge_1']['f1']:.4f} | "
          f"ROUGE-2 F1={sample_ld_eval['rouge_2']['f1']:.4f} | "
          f"ROUGE-L F1={sample_ld_eval['rouge_l']['f1']:.4f}")

    print("\n" + "=" * 90)
    print("CHẠY ĐÁNH GIÁ TRÊN TOÀN BỘ 40 BÀI BÁO THỰC TẾ...")
    print("=" * 90)

    for idx, article in enumerate(dataset):
        content = article["content"]
        ref = article["reference_summary"]

        tr_summary, _ = summarize_textrank(content, top_k=3)
        ld_summary = summarize_lead_k(content, top_k=3)

        tr_eval = evaluate_summary(tr_summary, ref)
        ld_eval = evaluate_summary(ld_summary, ref)

        tr_r1_f1_list.append(tr_eval["rouge_1"]["f1"])
        tr_r2_f1_list.append(tr_eval["rouge_2"]["f1"])
        tr_rl_f1_list.append(tr_eval["rouge_l"]["f1"])

        ld_r1_f1_list.append(ld_eval["rouge_1"]["f1"])
        ld_r2_f1_list.append(ld_eval["rouge_2"]["f1"])
        ld_rl_f1_list.append(ld_eval["rouge_l"]["f1"])

        if (idx + 1) % 10 == 0 or idx == 0:
            print(f"Đã xử lý {idx + 1:02d}/{len(dataset)} bài | "
                  f"[{article['id']}] TextRank R-1: {tr_eval['rouge_1']['f1']:.4f} vs Lead-3 R-1: {ld_eval['rouge_1']['f1']:.4f}")

    # Tính điểm trung bình F1
    avg_tr_r1 = sum(tr_r1_f1_list) / len(tr_r1_f1_list)
    avg_tr_r2 = sum(tr_r2_f1_list) / len(tr_r2_f1_list)
    avg_tr_rl = sum(tr_rl_f1_list) / len(tr_rl_f1_list)

    avg_ld_r1 = sum(ld_r1_f1_list) / len(ld_r1_f1_list)
    avg_ld_r2 = sum(ld_r2_f1_list) / len(ld_r2_f1_list)
    avg_ld_rl = sum(ld_rl_f1_list) / len(ld_rl_f1_list)

    print("\n" + "=" * 90)
    print(f"{'PHƯƠNG PHÁP':<20} | {'ROUGE-1 F1':<15} | {'ROUGE-2 F1':<15} | {'ROUGE-L F1':<15}")
    print("-" * 90)
    print(f"{'TextRank (Top-3)':<20} | {avg_tr_r1:<15.4f} | {avg_tr_r2:<15.4f} | {avg_tr_rl:<15.4f}")
    print(f"{'Lead-3 (Baseline)':<20} | {avg_ld_r1:<15.4f} | {avg_ld_r2:<15.4f} | {avg_ld_rl:<15.4f}")
    print("=" * 90)

    return {
        "textrank": {"rouge_1": avg_tr_r1, "rouge_2": avg_tr_r2, "rouge_l": avg_tr_rl},
        "lead_3": {"rouge_1": avg_ld_r1, "rouge_2": avg_ld_r2, "rouge_l": avg_ld_rl}
    }


if __name__ == "__main__":
    run_week4_evaluation()
