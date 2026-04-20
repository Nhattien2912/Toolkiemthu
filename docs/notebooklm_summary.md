# Tóm Tắt Dự Án TestWebTool Để Đưa Vào NotebookLM

## 1. Tổng quan dự án

Tên dự án: `testwebtool`

Mục tiêu của dự án là xây dựng một hệ thống kiểm thử tự động cho website bán giày, kết hợp:

- kiểm thử giao diện web bằng Selenium
- kiểm thử chức năng bằng pytest
- xuất báo cáo HTML, XML, Excel
- cung cấp dashboard web để chạy test, xem lịch sử chạy và đọc kết quả trực tiếp trên trình duyệt

Website được dùng để kiểm thử:

- Frontend đang test công khai: `https://guangli-shop.netlify.app/`
- Source chuẩn đối chiếu để kiểm thử source-level: `C:\Users\clubb\Desktop\WEB-MERN_t10-2024`


## 2. Bối cảnh đồ án

Đây là đồ án cuối kỳ môn Kiểm thử phần mềm, tập trung vào website bán giày.

Thông tin chính:

- Môn học: Kiểm thử phần mềm
- Mã lớp: `SOTE431079`
- Học kỳ: `II - 2025-2026`
- Trường: Đại học Công nghệ Kỹ thuật TP.HCM

Nhóm thực hiện:

- `24810038` - Trịnh Nhật Tiến
- `24810044` - Nguyễn Công Quốc
- `24810036` - Ngô Quang Lợi


## 3. Phạm vi kiểm thử chính

Hệ thống hiện tập trung kiểm thử sâu vào 2 module trọng tâm trong báo cáo Word:

### Module 1: Quản lý tài khoản

Bao gồm:

- Đăng ký
- Đăng nhập
- Quên mật khẩu

Hướng kiểm thử:

- Black-box testing
- Equivalence partitioning
- Boundary value analysis
- Validation
- UI / layout / keyboard navigation

### Module 2: Quản lý giỏ hàng và thanh toán

Bao gồm:

- Cart
- Voucher
- Checkout

Hướng kiểm thử:

- Business flow testing
- Regression
- Runtime audit
- Source audit


## 4. Công nghệ và thư viện sử dụng

Ngôn ngữ và công cụ:

- Python
- Selenium
- pytest
- pytest-html
- webdriver-manager
- Flask
- openpyxl
- psutil

Kiến trúc chính:

- `pytest` dùng để chạy test
- `Selenium` dùng để điều khiển trình duyệt
- `webdriver-manager` tự tải ChromeDriver
- `Flask` cung cấp dashboard web
- `openpyxl` tạo báo cáo Excel
- `psutil` hỗ trợ pause/resume tiến trình test chạy từ dashboard


## 5. Kiến trúc project

Các thành phần chính:

- `dashboard.py`: Flask app, route dashboard, run suite, stream log, tải report
- `tests/`: toàn bộ test automation
- `pages/`: Page Object Model
- `utils/report_parser.py`: parse XML report để hiển thị dashboard
- `utils/excel_reporter.py`: tạo Excel report theo từng lần chạy
- `utils/cumulative_reporter.py`: tạo Excel tích lũy từ toàn bộ lịch sử chạy
- `templates/`: giao diện HTML cho dashboard
- `static/`: CSS và JavaScript cho dashboard
- `reports/`: nơi lưu HTML, XML, Excel report
- `catalog/test_case_meta.py`: metadata testcase dùng để sinh Excel chi tiết


## 6. Các giao diện chính trên dashboard

Dashboard chạy tại:

- `http://127.0.0.1:5050/dashboard`

Các màn hình chính:

- `/dashboard`: tổng quan test run, lịch sử, chart, log live
- `/reports`: xem report của lần chạy
- `/logs`: xem stdout pytest
- `/project-doc`: giao diện riêng theo cấu trúc đồ án Word
- `/excel-reports`: xem toàn bộ Excel trong thư mục `reports`

Điểm nổi bật:

- chạy test trực tiếp từ web
- chạy headless trong nền, không bật cửa sổ Chrome ra ngoài desktop
- xem log real-time ngay trên trình duyệt
- có thể pause/resume khi đang chạy
- tải HTML report, Excel report, Excel tích lũy


## 7. Các suite test hiện có

Các suite đã cấu hình trên dashboard:

- `Run All - Theo Do An`
- `Run Max - Toan bo test that`
- `Module 1 - Account Management`
- `Module 2 - Cart and Checkout`
- `UC_01_SU - Register`
- `UC_02_SI - Login`
- `UC_03_FP - Forgot Password`
- `Strict Runtime Audit`
- `Strict Source Audit`
- `Source Conformance`

Ý nghĩa:

- `Run All - Theo Do An`: chạy toàn bộ phạm vi đồ án chính
- `Run Max - Toan bo test that`: chạy toàn bộ test thật đang có trong repo, không giới hạn trong 100 case


## 8. Độ phủ hiện tại

Tính đến ngày `14/04/2026`, hệ thống đã được nâng cấp để không còn giới hạn ở `57` case Excel như trước.

### Kết quả hiện tại

- `Run Max` collect được `191` test thật trong repo
- Excel tích lũy hiện tổng hợp được `200` test case
- `199/200` test case đã có kết quả thực từ lịch sử chạy
- Coverage cumulative: `99.5%`

### Tóm tắt cumulative mới nhất

- Total cases: `200`
- Executed cases: `199`
- Passed: `172`
- Failed: `27`
- Not executed: `1`

File cumulative mới nhất:

- `reports/report_excel_cumulative_20260414_002455.xlsx`


## 9. Các lớp kiểm thử đang có

### UI / Functional Selenium tests

Kiểm tra:

- login success / fail
- register validation
- search
- homepage UI
- page detail
- filters
- cart / checkout UI
- account pages

### Runtime audit

Kiểm tra:

- lỗi console browser
- broken images
- broken same-origin links
- lỗi runtime trên homepage, login, checkout

### Source audit

Kiểm tra từ source chuẩn:

- route thiếu
- flow validation sai
- contract frontend/backend lệch
- authorization guard thiếu
- xử lý cart và checkout sai logic

### Source conformance

Kiểm tra:

- route storefront
- signin/signup controls
- validation contracts
- checkout controls
- cart business logic
- header / footer / auth routes / product routes / order schema


## 10. Các lỗi đã phát hiện

Hệ thống hiện cố ý giữ lại một số test fail thật để phản ánh lỗi thực tế của source/web.

Một số nhóm lỗi đã phát hiện:

- thiếu route hoặc thiếu page cho quên mật khẩu
- validation đăng ký không dừng submit đúng chỗ
- contract `paymentMethod` lệch giữa frontend và backend
- payload checkout không map đúng shape backend
- logic xóa item khỏi cart không phân biệt đủ `productId + size + color`
- nhiều route backend chưa chặn truy cập chéo theo `req.user.id`
- runtime console error / broken resource trên frontend public

Các lỗi này đang được đưa vào:

- HTML report
- XML report
- Excel report
- dashboard
- giao diện `project-doc`


## 11. Excel report hiện tại

Hệ thống hiện sinh 2 loại Excel:

### Excel theo từng lần chạy

Mỗi lần `pytest` chạy xong sẽ sinh workbook mới.

Điểm nổi bật:

- nội dung tiếng Việt
- mỗi test case là một sheet
- sheet pass màu xanh
- sheet fail màu đỏ
- sheet chưa chạy màu vàng/trắng
- có sheet tổng hợp đầu tiên
- sheet tổng hợp có hyperlink nhảy tới đúng test case

### Excel tích lũy

File cumulative quét toàn bộ `results_*.xml`, lấy kết quả mới nhất của từng testcase.

Mục đích:

- giảm số case “Chưa thực hiện”
- gom kết quả từ nhiều lần chạy module khác nhau
- tạo một workbook gần đầy đủ nhất để trình bày


## 12. Các cải tiến dashboard đã có

Dashboard hiện hỗ trợ:

- hiển thị command preview trước khi chạy
- chạy test từ browser
- pause/resume run đang chạy
- live log có cuộn dọc ổn định
- state thật của run, tránh kẹt `paused/running` giả
- tự reset state cũ nếu process đã mất
- tải report HTML / Excel / cumulative Excel


## 13. Cách chạy hệ thống

### Cài thư viện

```bash
pip install -r requirements.txt
```

### Chạy dashboard

```bash
py dashboard.py
```

Mở:

- `http://127.0.0.1:5050/project-doc`
- `http://127.0.0.1:5050/dashboard`


## 14. Giá trị học thuật của dự án

Dự án không chỉ dừng ở việc “chạy Selenium”, mà đã phát triển thành một hệ thống TestOps mini phục vụ đồ án:

- có test automation
- có source audit
- có runtime audit
- có cumulative reporting
- có dashboard trigger run
- có workbook chi tiết theo chuẩn testcase
- có dữ liệu đủ để làm báo cáo môn học và trình bày bug findings


## 15. Kết luận ngắn

TestWebTool hiện là một hệ thống kiểm thử tương đối hoàn chỉnh cho đồ án website bán giày, kết hợp kiểm thử giao diện, kiểm thử chức năng, kiểm thử runtime và kiểm thử source-level. Hệ thống đã vượt khỏi mức demo ban đầu, có dashboard web riêng, có Excel/HTML/XML report, có khả năng chạy theo module hoặc chạy tối đa toàn bộ test thật hiện có trong repo, đồng thời ghi nhận được lỗi thực tế để phục vụ báo cáo và đánh giá chất lượng phần mềm.
