import json
import os
from src.textrank import summarize_textrank, summarize_lead_k
from src.rouge import evaluate_summary
from src.preprocessing import split_sentences


def run_week4_evaluation():
    dataset_path = os.path.join(os.path.dirname(__file__), "data", "vietnamese_news_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    total_articles = len(dataset)
    print("=" * 105)
    print("CHƯƠNG TRÌNH ĐÁNH GIÁ TÓM TẮT VĂN BẢN TIẾNG VIỆT")
    print(f"Tổng số bài báo thực nghiệm: {total_articles} bài thật từ VietNews (mỗi bài >= 10 câu)")
    print("Mô hình so sánh: TextRank (Top-3 giữ thứ tự gốc) vs Baseline Lead-3 (3 câu đầu)")
    print("Độ đo tự cài đặt: ROUGE-1, ROUGE-2, ROUGE-L (Precision, Recall, F1-Score)")
    print("=" * 105)

    # 1. Minh họa chi tiết bài báo đầu tiên
    sample = dataset[0]
    sample_content = sample["content"]
    sample_ref = sample["reference_summary"]

    sample_tr_sum, _ = summarize_textrank(sample_content, top_k=3)
    sample_ld_sum = summarize_lead_k(sample_content, top_k=3)

    print(f"\n[PHẦN 1: MINH HỌA CHI TIẾT BÀI BÁO MẪU {sample['id']}]")
    print(f"Tiêu đề : {sample['title']}")
    print(f"Nguồn   : {sample['source']}")
    print(f"Số câu  : {sample['sentence_count']} câu")

    print("\n--- TÓM TẮT THAM CHIẾU (REFERENCE SUMMARY / BẢN GỐC TÒA SOẠN): ---")
    print(sample_ref)

    print("\n--- KẾT QUẢ TÓM TẮT TEXTRANK (TOP-3, GIỮ THỨ TỰ XUẤT HIỆN BAN ĐẦU): ---")
    print(sample_tr_sum)

    print("\n--- KẾT QUẢ TÓM TẮT BASELINE LEAD-3 (3 CÂU ĐẦU TIÊN CỦA BÀI BÁO): ---")
    print(sample_ld_sum)

    s_tr_eval = evaluate_summary(sample_tr_sum, sample_ref)
    s_ld_eval = evaluate_summary(sample_ld_sum, sample_ref)
    print("\n--- ĐIỂM ROUGE TRÊN BÀI MẪU VN_001: ---")
    print(f"TextRank : ROUGE-1 F1={s_tr_eval['rouge_1']['f1']:.4f} | "
          f"ROUGE-2 F1={s_tr_eval['rouge_2']['f1']:.4f} | "
          f"ROUGE-L F1={s_tr_eval['rouge_l']['f1']:.4f}")
    print(f"Lead-3   : ROUGE-1 F1={s_ld_eval['rouge_1']['f1']:.4f} | "
          f"ROUGE-2 F1={s_ld_eval['rouge_2']['f1']:.4f} | "
          f"ROUGE-L F1={s_ld_eval['rouge_l']['f1']:.4f}")

    # 2. Chạy đánh giá và in đầy đủ kết quả toàn bộ 40 bài báo
    print("\n" + "=" * 105)
    print(f"[PHẦN 2: BẢNG KẾT QUẢ ĐÁNH GIÁ CHI TIẾT TỪNG BÀI BÁO (ĐỦ {total_articles}/{total_articles} BÀI)]")
    print("=" * 105)
    print(f"{'STT':<4} | {'MÃ BÀI':<8} | {'SỐ CÂU':<7} | {'TIÊU ĐỀ BÀI BÁO (RÚT GỌN)':<45} | {'TEXTRANK R-1':<13} | {'LEAD-3 R-1':<11}")
    print("-" * 105)

    tr_r1_list, tr_r2_list, tr_rl_list = [], [], []
    ld_r1_list, ld_r2_list, ld_rl_list = [], [], []

    for idx, article in enumerate(dataset):
        content = article["content"]
        ref = article["reference_summary"]

        tr_summary, _ = summarize_textrank(content, top_k=3)
        ld_summary = summarize_lead_k(content, top_k=3)

        tr_eval = evaluate_summary(tr_summary, ref)
        ld_eval = evaluate_summary(ld_summary, ref)

        tr_r1_list.append(tr_eval["rouge_1"]["f1"])
        tr_r2_list.append(tr_eval["rouge_2"]["f1"])
        tr_rl_list.append(tr_eval["rouge_l"]["f1"])

        ld_r1_list.append(ld_eval["rouge_1"]["f1"])
        ld_r2_list.append(ld_eval["rouge_2"]["f1"])
        ld_rl_list.append(ld_eval["rouge_l"]["f1"])

        short_title = article["title"][:42] + "..." if len(article["title"]) > 42 else article["title"]
        print(f"{idx + 1:02d}   | {article['id']:<8} | {article['sentence_count']:2d} câu | {short_title:<45} | {tr_eval['rouge_1']['f1']:<13.4f} | {ld_eval['rouge_1']['f1']:<11.4f}")

    # 3. Tổng kết điểm trung bình
    avg_tr_r1 = sum(tr_r1_list) / len(tr_r1_list)
    avg_tr_r2 = sum(tr_r2_list) / len(tr_r2_list)
    avg_tr_rl = sum(tr_rl_list) / len(tr_rl_list)

    avg_ld_r1 = sum(ld_r1_list) / len(ld_r1_list)
    avg_ld_r2 = sum(ld_r2_list) / len(ld_r2_list)
    avg_ld_rl = sum(ld_rl_list) / len(ld_rl_list)

    print("=" * 105)
    print(f"\n[PHẦN 3: BẢNG SO SÁNH TỔNG HỢP F1-SCORE TRUNG BÌNH TRÊN TOÀN BỘ {total_articles} BÀI]")
    print("-" * 75)
    print(f"{'PHƯƠNG PHÁP TÓM TẮT':<25} | {'ROUGE-1 F1':<13} | {'ROUGE-2 F1':<13} | {'ROUGE-L F1':<13}")
    print("-" * 75)
    print(f"{'TextRank (Top-3)':<25} | {avg_tr_r1:<13.4f} | {avg_tr_r2:<13.4f} | {avg_tr_rl:<13.4f}")
    print(f"{'Lead-3 (Baseline)':<25} | {avg_ld_r1:<13.4f} | {avg_ld_r2:<13.4f} | {avg_ld_rl:<13.4f}")
    print("=" * 75)

    return {
        "textrank": {"rouge_1": avg_tr_r1, "rouge_2": avg_tr_r2, "rouge_l": avg_tr_rl},
        "lead_3": {"rouge_1": avg_ld_r1, "rouge_2": avg_ld_r2, "rouge_l": avg_ld_rl}
    }


if __name__ == "__main__":
    run_week4_evaluation()
