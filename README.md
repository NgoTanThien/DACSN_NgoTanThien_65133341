ĐỒ ÁN CƠ SỞ NGÀNH: TÓM TẮT VĂN BẢN TRÍCH RÚT BẰNG THUẬT TOÁN TEXTRANK
SO SÁNH VỚI BASELINE LEAD-K BẰNG ĐỘ ĐO ROUGE TỰ CÀI ĐẶT

1. THÔNG TIN CHUNG
- Học phần: Đồ án Cơ sở ngành
- Đề tài: Tóm tắt trích rút bằng thuật toán TextRank trên tin tức tiếng Việt
- Sinh viên thực hiện: Ngô Tấn Thiện
- Mã số sinh viên: 65133341
- Lớp sinh viên: 65.CNTT-1 - Khoa Công nghệ Thông tin, Trường Đại học Nha Trang
- Giảng viên hướng dẫn: ThS. Ngô Nguyễn Tường Nghi (nghinnt@ntu.edu.vn)
- Hạn nộp báo cáo Tuần 4: 23:59:59 ngày 25/11/2026

--------------------------------------------------------------------------------

2. NỘI DUNG HOÀN THÀNH TRONG TUẦN 4
- Dữ liệu thực tế: Cập nhật 40 bài báo thật có tóm tắt tham chiếu từ bộ ngữ liệu VietNews, mỗi bài có ít nhất 10 câu văn và ghi rõ nguồn gốc (data/vietnamese_news_dataset.json).
- Thuật toán tóm tắt:
  + Cài đặt trích chọn Top-K giữ nguyên thứ tự xuất hiện ban đầu của câu (src/textrank.py).
  + Cài đặt phương pháp đường cơ sở Lead-K trích K câu đầu (src/textrank.py).
- Độ đo tự viết: Cài đặt từ đầu ROUGE-1, ROUGE-2 (n-gram overlap) và ROUGE-L (Longest Common Subsequence qua quy hoạch động) trong src/rouge.py.
- Kiểm thử tự động (Unit Test): Viết 6 bài test đạt 100% trong tests/test_textrank.py, đáp ứng đầy đủ yêu cầu của Giảng viên (ma trận đối xứng, tổng PageRank = 1, ví dụ 3 câu tính tay có nghiệm giải tích).
- Đánh giá thực nghiệm: Chạy so sánh TextRank với Lead-K trên toàn bộ 40 bài báo và phân tích hiện tượng Lead Bias trong tin tức báo chí.

--------------------------------------------------------------------------------

3. CẤU TRÚC THƯ MỤC DỰ ÁN
- data/vietnamese_news_dataset.json : Bộ dữ liệu 40 bài báo thật từ VietNews (mỗi bài >= 10 câu).
- src/preprocessing.py              : Module tách câu, chuẩn hóa và lọc hư từ tiếng Việt.
- src/similarity.py                 : Module tính ma trận tương đồng trọng số cạnh W.
- src/pagerank.py                   : Module chuẩn hóa Markov M và giải thuật PageRank lặp.
- src/textrank.py                   : Module tóm tắt trích rút TextRank Top-K (giữ thứ tự gốc) và Lead-K.
- src/rouge.py                      : Module tự cài đặt ROUGE-1, ROUGE-2, ROUGE-L.
- tests/test_textrank.py            : Bộ 6 bài kiểm thử đơn vị tự động.
- main.py                           : Chương trình đánh giá tóm tắt trên toàn bộ 40 bài báo.
- BAO_CAO_TUAN_4_TEXTRANK.docx      : Báo cáo Word Tuần 4 (đúng bìa lớp 65.CNTT-1).
- BAO_CAO_TUAN_4_TEXTRANK.md        : Báo cáo định dạng văn bản Tuần 4.
- README.md                         : Tài liệu hướng dẫn và mô tả dự án.

--------------------------------------------------------------------------------

4. HƯỚNG DẪN THỰC THI

Yêu cầu môi trường: Python 3.9 trở lên.

a. Chạy bộ kiểm thử tự động (Unit Tests):
python -m unittest -v tests/test_textrank.py

Kết quả kỳ vọng: 6/6 tests PASS (thời gian chạy dưới 0.01s).

b. Chạy chương trình đánh giá so sánh trên toàn bộ dữ liệu:
python main.py

Kết quả thực nghiệm trên 40 bài báo:
- TextRank (Top-3) : ROUGE-1 F1 = 0.2420 | ROUGE-2 F1 = 0.1282 | ROUGE-L F1 = 0.1735
- Lead-3 (Baseline): ROUGE-1 F1 = 0.2673 | ROUGE-2 F1 = 0.1496 | ROUGE-L F1 = 0.1929
