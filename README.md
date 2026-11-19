ĐỒ ÁN CƠ SỞ NGÀNH: TÓM TẮT VĂN BẢN TRÍCH RÚT BẰNG THUẬT TOÁN TEXTRANK

1. THÔNG TIN CHUNG
- Học phần: Đồ án Cơ sở ngành
- Đề tài: Tóm tắt trích rút bằng thuật toán TextRank trên tin tức tiếng Việt
- Sinh viên thực hiện: Ngô Tấn Thiện
- Mã số sinh viên: 65133341
- Lớp: 66.CNPM - Khoa Công nghệ Thông tin, Trường Đại học Nha Trang
- Giảng viên hướng dẫn: Thầy Ngô Nguyễn Tường Nghi (nghinnt@ntu.edu.vn)

--------------------------------------------------------------------------------

2. NHIỆM VỤ TUẦN 3 
- Chốt bộ dữ liệu tin tức tiếng Việt có tóm tắt tham chiếu chuẩn (data/vietnamese_news_dataset.json) gồm 10 bài báo đa chủ đề từ VnExpress, Tuổi Trẻ, Dân Trí, Thanh Niên.
- Cài đặt module tách câu tiếng Việt, chuẩn hóa từ vựng và lọc bỏ hư từ (src/preprocessing.py).
- Cài đặt module xây dựng đồ thị câu và tính ma trận tương đồng trọng số cạnh W theo công thức Mihalcea và Tarau (src/similarity.py).
- Cài đặt module chuẩn hóa ma trận chuyển tiếp Markov M và thuật toán PageRank lặp (Power Iteration) với hệ số d = 0.85, kiểm tra điều kiện hội tụ chuẩn L1 nhỏ hơn 1e-5 (src/pagerank.py).

--------------------------------------------------------------------------------

3. CẤU TRÚC THƯ MỤC MÃ NGUỒN
- data/vietnamese_news_dataset.json : Bộ dữ liệu 10 bài báo tiếng Việt có tóm tắt tham chiếu chuẩn.
- src/preprocessing.py              : Module tách câu, làm sạch văn bản và lọc hư từ tiếng Việt.
- src/similarity.py                 : Module xây dựng đồ thị câu và tính ma trận tương đồng W.
- src/pagerank.py                   : Module chuẩn hóa ma trận Markov M và thuật toán lặp PageRank.
- main.py                           : Chương trình chạy thử nghiệm tách câu, ma trận tương đồng và PageRank lặp.
- README.md                         : Tài liệu mô tả dự án và hướng dẫn chạy chương trình.

--------------------------------------------------------------------------------

4. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH
Yêu cầu: Python 3.9 trở lên (chỉ dùng thư viện chuẩn của Python, không phụ thuộc thư viện ngoài).

Lệnh chạy tại thư mục gốc của dự án:
python main.py

Kết quả đầu ra trên màn hình console:
- Hiển thị danh sách các câu sau khi tách từ bài báo mẫu.
- Hiển thị ma trận tương đồng giữa các câu (W) kích thước N x N.
- Hiển thị điểm phân hạng PageRank lặp của từng đỉnh câu và số vòng lặp hội tụ thực tế.
    