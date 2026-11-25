BỘ GIÁO DỤC VÀ ĐÀO TẠO
TRƯỜNG ĐẠI HỌC NHA TRANG
KHOA CÔNG NGHỆ THÔNG TIN

BÁO CÁO TIẾN ĐỘ ĐỒ ÁN CƠ SỞ NGÀNH - TUẦN 4

ĐỀ TÀI: TÓM TẮT TRÍCH RÚT VĂN BẢN TIẾNG VIỆT BẰNG THUẬT TOÁN TEXTRANK
SO SÁNH VỚI BASELINE LEAD-K BẰNG ĐỘ ĐO ROUGE TỰ CÀI ĐẶT

THÔNG TIN CHUNG:
- Giảng viên hướng dẫn: ThS. Ngô Nguyễn Tường Nghi
- Sinh viên thực hiện: Ngô Tấn Thiện
- Mã số sinh viên: 65133341
- Lớp: 65.CNTT-1 (Đã cập nhật chuẩn hóa bìa theo nhắc nhở của Giảng viên)
- Hạn nộp báo cáo: 23:59:59 ngày 25/11/2026
- Địa chỉ kho mã nguồn GitHub: https://github.com/NgoTanThien/DACSN_NgoTanThien_65133341

================================================================================

1. TỔNG QUAN NHIỆM VỤ TUẦN 4

Theo yêu cầu và hướng dẫn của Thầy Ngô Nguyễn Tường Nghi, các mục tiêu thực hiện trong Tuần 4 bao gồm:
1.1. Thay thế bộ dữ liệu thử nghiệm bằng 30 đến 50 bài báo tin tức tiếng Việt thật lấy từ bộ ngữ liệu chuẩn VietNews, có tóm tắt tham chiếu (reference summary), ghi rõ nguồn gốc từng bài và mỗi bài có tối thiểu 10 câu văn. Bộ dữ liệu được sàng lọc cân đối, mỗi bài có từ 12 đến 20 câu hoàn chỉnh, không có bài quá dài hoặc quá ngắn.
1.2. Cài đặt hoàn chỉnh giải thuật trích chọn Top-K có sắp xếp lại theo thứ tự xuất hiện ban đầu (giữ thứ tự gốc) và phương pháp đường cơ sở Lead-K (trích K câu đầu).
1.3. Tự cài đặt từ đầu (from scratch) bộ ba độ đo đánh giá ROUGE-1, ROUGE-2 (n-gram overlap) và ROUGE-L (Longest Common Subsequence - chuỗi con chung dài nhất).
1.4. Xây dựng tối thiểu 3 bài kiểm thử đơn vị (Unit Tests) tự động:
- Kiểm thử ma trận đối xứng và đường chéo bằng 0.
- Kiểm thử tổng điểm PageRank toàn đồ thị xấp xỉ 1.0.
- Kiểm thử ví dụ 3 câu tính tay có nghiệm giải tích chính xác.
1.5. Cập nhật và sửa thông tin lớp trên bìa báo cáo sang đúng lớp: 65.CNTT-1.
1.6. Chạy đánh giá so sánh TextRank và Lead-K trên toàn bộ tập dữ liệu, phân tích kết quả chuyên môn và đồng bộ mã nguồn lên GitHub.

================================================================================

2. BỘ DỮ LIỆU TIN TỨC TIẾNG VIỆT THỰC TẾ (40 BÀI BÁO TỪ VIETNEWS)

Dữ liệu được trích xuất từ kho ngữ liệu mở VietNews (VNDS - Vietnamese Dataset for Summarization) công khai từ các cơ quan báo chí chính thống tại Việt Nam (VnExpress, Dân Trí, Người Đưa Tin, Tuổi Trẻ, v.v.).
Dữ liệu lưu tại file data/vietnamese_news_dataset.json với cấu trúc mỗi bài gồm:
- id: Mã định danh bài báo (VN_001 đến VN_040).
- guid: Mã tham chiếu gốc trong tập dữ liệu VietNews.
- source: Nguồn báo chí và chuyên mục (Pháp luật, Kinh tế, Y tế, Thời sự, Giáo dục).
- title: Tiêu đề bài báo.
- sentence_count: Số lượng câu văn trong bài báo.
- reference_summary: Tóm tắt tham chiếu do biên tập viên / chuyên gia viết.
- content: Toàn bộ nội dung bài báo đã chuẩn hóa tiếng Việt.

Thống kê thực tế bộ dữ liệu:
- Tổng số lượng bài báo: 40 bài (đáp ứng đúng khoảng 30-50 bài của Giảng viên).
- Tiêu chí chuẩn hóa: Mỗi bài báo đều có từ 12 đến 20 câu văn hoàn chỉnh (bảo đảm >= 10 câu, không bị bài quá dài hay bài quá ngắn).
- Bài có số câu ít nhất: 12 câu.
- Bài có số câu nhiều nhất: 20 câu.
- Số câu trung bình mỗi bài báo: 15.03 câu/bài.
- Tất cả 40 bài đều có nguồn gốc rõ ràng và tóm tắt tham chiếu tương ứng.

Bảng minh họa một số bài báo tiêu biểu trong tập dữ liệu:
- VN_001 | Nguồn: VietNews - Pháp luật / Tòa án | 12 câu | Tiêu đề: Bản án cho đối tượng giả danh công an để lừa đảo
- VN_002 | Nguồn: VietNews - Thời sự / Chính sách | 19 câu | Tiêu đề: VEC từ chối phục vụ vĩnh viễn 2 ô tô gây rối trạm thu phí
- VN_003 | Nguồn: VietNews - Pháp luật / Tòa án | 16 câu | Tiêu đề: VKSND tỉnh Sóc Trăng xin lỗi oan sai nữ hoàng lục bình
- VN_004 | Nguồn: VietNews - Pháp luật / Tòa án | 18 câu | Tiêu đề: Đề nghị truy tố 2 giám đốc vụ chìm tàu ở Cần Giờ
- VN_005 | Nguồn: VietNews - Pháp luật / Tòa án | 16 câu | Tiêu đề: Tên trộm thuê người cẩu trộm máy ủi trong khu công nghiệp
- VN_006 | Nguồn: VietNews - Pháp luật / Tòa án | 19 câu | Tiêu đề: Chiếc xe kia morning đời cũ và manh mối truy bắt kẻ giết người
- VN_007 | Nguồn: VietNews - Xã hội / Đời sống | 19 câu | Tiêu đề: Khởi tố vụ án phá rừng tại Kon Tum
- VN_008 | Nguồn: VietNews - Pháp luật / Tòa án | 16 câu | Tiêu đề: Vụ thanh niên treo cổ, hai tay bị trói ở Hoài Đức

================================================================================

3. THIẾT KẾ VÀ CÀI ĐẶT CÁC GIẢI THUẬT CỐT LÕI

3.1. Cài đặt trích chọn Top-K bảo toàn thứ tự gốc (src/textrank.py)
Trong mô hình tóm tắt văn bản trích rút, nếu chỉ lấy K câu có điểm PageRank cao nhất rồi ghép tuần tự theo thứ tự điểm số giảm dần, đoạn văn tóm tắt sẽ bị đảo lộn thời gian và logic ngữ nghĩa.
Giải pháp đã cài đặt:
- Bước 1: Sau khi giải thuật PageRank hội tụ, ghi nhận vector điểm số và thứ tự ban đầu của từng câu: (index_gốc, score).
- Bước 2: Sắp xếp theo score giảm dần để trích chọn Top-K câu có trọng số thông tin lớn nhất.
- Bước 3: Sắp xếp lại K câu này theo index_gốc tăng dần (đúng vị trí xuất hiện ban đầu trong văn bản).
- Bước 4: Ghép các câu thành đoạn tóm tắt hoàn chỉnh.

3.2. Cài đặt phương pháp đường cơ sở Lead-K (src/textrank.py)
- Phương pháp Lead-K trích xuất trực tiếp K câu đầu tiên của bài báo (thường K = 3).
- Đây là phương pháp baseline tiêu chuẩn trong xử lý tin tức vì các nhà báo thường áp dụng mô hình tháp ngược (Inverted Pyramid), đưa những thông tin quan trọng nhất vào phần sapo mở đầu.

3.3. Tự cài đặt các độ đo ROUGE (src/rouge.py)
Tất cả các độ đo ROUGE được sinh viên tự lập trình từ công thức toán học:
a) ROUGE-1 (Unigram Overlap):
- Đếm số lượng từ đơn trùng nhau giữa tóm tắt mô hình và tóm tắt tham chiếu.
- Sử dụng cơ chế clipping count để tránh tình trạng câu tóm tắt lặp lại một từ nhiều lần làm tăng điểm giả tạo.
- Precision = Overlap / Tổng từ tóm tắt mô hình
- Recall = Overlap / Tổng từ tóm tắt tham chiếu
- F1 = 2 x Precision x Recall / (Precision + Recall)

b) ROUGE-2 (Bigram Overlap):
- Tạo danh sách các cặp 2 từ liền kề (w_i, w_i+1) cho cả hai bản tóm tắt.
- Đếm số lượng bigram trùng lặp có giới hạn tần số xuất hiện.
- Đánh giá khả năng bảo toàn cụm từ và độ liên kết ngữ pháp cục bộ.

c) ROUGE-L (Longest Common Subsequence):
- Sử dụng giải thuật Quy hoạch động (Dynamic Programming) với bảng quy hoạch dp[m+1][n+1] để tính độ dài chuỗi con chung dài nhất (LCS).
- Không yêu cầu các từ phải đứng sát cạnh nhau liên tiếp, phản ánh cấu trúc dòng chảy câu.
- Precision = LCS_len / n
- Recall = LCS_len / m
- F1 = 2 x Precision x Recall / (Precision + Recall)

================================================================================

4. KẾT QUẢ KIỂM THỬ ĐƠN VỊ (UNIT TESTS)

Bộ kiểm thử được viết trong file tests/test_textrank.py và thực thi bằng framework unittest của Python.
Toàn bộ 6/6 test cases đều vượt qua thành công:

4.1. Bảng tổng hợp kiểm thử:
- Test 1: test_similarity_matrix_symmetry_and_zero_diagonal -> PASS (0.001s)
  Mục đích: Xác nhận ma trận trọng số đối xứng W_ij = W_ji và đường chéo W_ii = 0.
- Test 2: test_pagerank_sum_to_one -> PASS (0.001s)
  Mục đích: Xác nhận tổng vector phân phối xác suất PageRank toàn đồ thị xấp xỉ 1.0 (chuẩn hóa ngẫu nhiên).
- Test 3: test_three_sentences_hand_calculated -> PASS (0.001s)
  Mục đích: Xác nhận giải thuật số lặp khớp chính xác với nghiệm giải tích tính bằng tay trên ví dụ 3 câu.
- Test 4: test_top_k_order_preservation -> PASS (0.001s)
  Mục đích: Xác nhận các câu trong tóm tắt Top-K xuất hiện theo đúng thứ tự ban đầu của văn bản.
- Test 5: test_rouge_metrics -> PASS (0.001s)
  Mục đích: Kiểm thử tính đúng đắn của các công thức ROUGE-1, ROUGE-2, ROUGE-L trên ví dụ chuẩn.
- Test 6: test_lead_k_baseline -> PASS (0.001s)
  Mục đích: Kiểm tra hàm trích xuất K câu đầu tiên.

4.2. Chi tiết ví dụ 3 câu tính tay có nghiệm giải tích chính xác:
Xét 3 câu văn bản:
- S1: "học sinh đi học" -> token: ["học", "sinh", "học"], độ dài = 3.
- S2: "học sinh thi đại học" -> token: ["học", "sinh", "thi", "đại", "học"], độ dài = 5.
- S3: "trời mưa to" -> token: ["trời", "mưa", "to"], độ dài = 3.

Tính toán thủ công:
- Từ chung giữa S1 và S2: {"học", "sinh"} (số từ chung = 2).
  Mẫu số chuẩn hóa: ln(3 + 1) + ln(5 + 1) = ln(4) + ln(6) = 1.386294 + 1.791759 = 3.178054.
  Trọng số cạnh: W_12 = W_21 = 2 / 3.178054 = 0.629316.
- Câu S3 không có từ chung nào với S1 và S2 nên W_13 = W_31 = 0 và W_23 = W_32 = 0 (S3 là đỉnh cô lập).

Ma trận chuyển trạng thái Markov:
- Hàng 1 chỉ nối sang S2 nên M_1 = [0, 1, 0].
- Hàng 2 chỉ nối sang S1 nên M_2 = [1, 0, 0].
- Hàng 3 (tổng hàng = 0) chia xác suất đều cho 3 đỉnh: M_3 = [1/3, 1/3, 1/3].

Hệ phương trình PageRank tại điểm dừng hội tụ (damping factor d = 0.85):
- Do tính đối xứng giữa S1 và S2: PR(S1) = PR(S2).
- Đỉnh S3 chỉ nhận xác suất phân bổ từ chính nó và xác suất ngẫu nhiên:
  PR(S3) = (1 - 0.85)/3 + 0.85 x (1/3) x PR(S3) = 0.05 + (0.85/3) x PR(S3).
  PR(S3) x (1 - 0.85/3) = 0.05.
  PR(S3) x (2.15/3) = 0.05 => PR(S3) = 0.15 / 2.15 = 3 / 43 ≈ 0.069767 (hay 6.98%).
- Do tổng điểm PageRank của 3 đỉnh bằng 1.0:
  PR(S1) = PR(S2) = (1 - 3/43) / 2 = 20 / 43 ≈ 0.465116 (hay 46.51%).
- Kết quả chạy hàm run_pagerank_iterative:
  PR(S1) = 0.465116, PR(S2) = 0.465116, PR(S3) = 0.069767, tổng bằng 1.000000.
  Kết quả số lặp hoàn toàn trùng khớp với nghiệm giải tích tính tay.

================================================================================

5. KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ SO SÁNH TRÊN 40 BÀI BÁO

5.1. Bảng số liệu ROUGE thực tế (chạy trên toàn bộ 40 bài báo VietNews cân đối):
Chương trình main.py đã thực hiện tóm tắt và đánh giá tự động trên toàn bộ 40 bài báo, điểm số F1-Score trung bình thu được như sau:

Phương pháp              ROUGE-1 F1     ROUGE-2 F1     ROUGE-L F1
TextRank (Top-3)         0.2241         0.1119         0.1492
Lead-3 (Baseline)        0.2502         0.1433         0.1833

5.2. Phân tích kết quả chuyên môn (Insight kỹ thuật):
- Hiện tượng Lead Bias trong dữ liệu tin tức:
  Điểm ROUGE của phương pháp Lead-3 đạt 0.2502 (nhỉnh hơn TextRank là 0.2241). Đây là một kết quả hoàn toàn phù hợp với lý thuyết Xử lý ngôn ngữ tự nhiên. Thể loại tin tức báo chí luôn được viết theo cấu trúc kim tự tháp ngược (Inverted Pyramid): câu đầu tiên (sapo) luôn tóm tắt trọn vẹn thông tin quan trọng nhất của sự kiện (5W1H: Ai, Cái gì, Ở đâu, Khi nào, Tại sao). Tóm tắt tham chiếu do biên tập viên viết cũng tập trung cao độ vào những câu mở đầu này.
- Ý nghĩa khoa học và ưu điểm của TextRank:
  Mặc dù gặp bất lợi do cấu trúc Lead Bias của tin tức, TextRank vẫn đạt kết quả rất tốt (ROUGE-1 = 0.2241) hoàn toàn bằng giải thuật đồ thị không giám sát (unsupervised). TextRank không giả định thông tin quan trọng phải nằm ở đầu bài, mà tìm kiếm những câu có tính kết nối thông tin toàn cục trên toàn bộ bài báo. Đối với các thể loại văn bản khác (như báo cáo nghiên cứu khoa học, tài liệu pháp lý, truyện kể), thông tin then chốt thường nằm rải rác ở thân bài và kết luận; khi đó TextRank sẽ phát huy sức mạnh vượt trội so với Lead-K.
- Hiệu quả của cơ chế giữ thứ tự gốc:
  Các câu được TextRank trích xuất khi được sắp xếp lại theo đúng thứ tự xuất hiện ban đầu giúp văn bản tóm tắt đọc rất mạch lạc, liên kết tự nhiên, không bị xáo trộn logic thời gian.

================================================================================

6. KẾT LUẬN VÀ KẾ HOẠCH TUẦN TIẾP THEO

6.1. Kết quả đạt được trong Tuần 4:
- Đã chuẩn bị bộ dữ liệu thực tế gồm 40 bài báo VietNews chuẩn, có tóm tắt tham chiếu, mỗi bài cân đối từ 12 đến 20 câu văn.
- Cài đặt thành công Top-K giữ nguyên thứ tự gốc và Lead-K baseline.
- Tự lập trình hoàn chỉnh bộ ba độ đo ROUGE-1, ROUGE-2, ROUGE-L từ các công thức toán học.
- Xây dựng 6 unit tests tự động, đặc biệt có chứng minh nghiệm giải tích 3 câu tính tay.
- Sửa đổi bìa báo cáo sang đúng lớp 65.CNTT-1 theo nhắc nhở của Giảng viên hướng dẫn.
- Mã nguồn và báo cáo được đồng bộ hoàn toàn lên GitHub.

6.2. Kế hoạch Tuần 5:
- Nghiên cứu kết hợp trọng số vị trí câu (Position Weighting) vào đồ thị TextRank để dung hòa giữa tính kết nối ngữ nghĩa toàn cục và ưu thế của các câu mở đầu trong tin tức.
- Xây dựng ứng dụng web demo tóm tắt văn bản trực quan.
