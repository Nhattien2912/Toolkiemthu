from __future__ import annotations


SOURCE_PROJECT_ROOT = r"C:\Users\clubb\Desktop\WEB-MERN_t10-2024"

REGISTER_TEST_CASES = [
    {"stt": 1, "code": "REG_01", "scenario": "Đăng ký thành công (Happy Path).", "action": "Nhập đầy đủ và hợp lệ: Tên, Email, SĐT, Pass, Re-pass.", "expected": "Đăng ký thành công, chuyển hướng trang Đăng nhập hoặc gửi OTP."},
    {"stt": 2, "code": "REG_02", "scenario": "Bỏ trống tất cả các trường bắt buộc.", "action": "Click Đăng ký mà không nhập gì.", "expected": "Hiển thị lỗi Vui lòng nhập... ở dưới tất cả các trường."},
    {"stt": 3, "code": "REG_03", "scenario": "Đăng ký với Email đã tồn tại.", "action": "Nhập Email của 1 user đã có trong CSDL.", "expected": "Báo lỗi Email đã được sử dụng."},
    {"stt": 4, "code": "REG_04", "scenario": "Đăng ký với SĐT đã tồn tại.", "action": "Nhập SĐT của 1 user đã có trong CSDL.", "expected": "Báo lỗi Số điện thoại đã tồn tại."},
    {"stt": 5, "code": "REG_05", "scenario": "Định dạng Email không hợp lệ.", "action": "Nhập: test@.com, test.com, test@domain.", "expected": "Báo lỗi Định dạng email không hợp lệ."},
    {"stt": 6, "code": "REG_06", "scenario": "Định dạng SĐT không hợp lệ (chữ cái).", "action": "Nhập: 0901abc123.", "expected": "Báo lỗi hoặc chặn không cho nhập chữ cái."},
    {"stt": 7, "code": "REG_07", "scenario": "SĐT không đủ độ dài.", "action": "Nhập SĐT có 8 số: 09012345.", "expected": "Báo lỗi Số điện thoại phải có 10 chữ số."},
    {"stt": 8, "code": "REG_08", "scenario": "Mật khẩu quá ngắn.", "action": "Nhập mật khẩu: 12345 (5 ký tự).", "expected": "Báo lỗi Mật khẩu phải từ 8 ký tự trở lên."},
    {"stt": 9, "code": "REG_09", "scenario": "Xác nhận mật khẩu không khớp.", "action": "Pass: Abc@1234 / Re-pass: Abc@1235.", "expected": "Báo lỗi Mật khẩu xác nhận không trùng khớp."},
    {"stt": 10, "code": "REG_10", "scenario": "Mã OTP không hợp lệ (nếu có).", "action": "Nhập sai mã OTP gửi về mail/SĐT.", "expected": "Báo lỗi Mã xác thực không hợp lệ."},
    {"stt": 11, "code": "REG_11", "scenario": "Mã OTP hết hạn (nếu có).", "action": "Nhập đúng OTP nhưng sau thời gian quy định (vd > 5 phút).", "expected": "Báo lỗi Mã xác thực đã hết hạn."},
    {"stt": 12, "code": "REG_12", "scenario": "Kiểm thử bảo mật (SQL Injection).", "action": "Nhập Tên đăng nhập: ' OR 1=1 --", "expected": "Báo lỗi ký tự không hợp lệ, không dính SQLi."},
    {"stt": 63, "code": "REG_13", "scenario": "Trim khoảng trắng ở username và SĐT khi đăng ký.", "action": "Nhập username/SĐT có khoảng trắng đầu cuối rồi bấm Đăng ký.", "expected": "Hệ thống trim dữ liệu trước khi validate và lưu."},
    {"stt": 64, "code": "REG_14", "scenario": "Username quá ngắn.", "action": "Nhập username chỉ 2 ký tự.", "expected": "Báo lỗi username không hợp lệ hoặc không đủ độ dài."},
    {"stt": 65, "code": "REG_15", "scenario": "Mật khẩu thiếu ký tự đặc biệt.", "action": "Nhập mật khẩu Abcd1234.", "expected": "Báo lỗi mật khẩu phải có ký tự đặc biệt."},
    {"stt": 66, "code": "REG_16", "scenario": "Chặn XSS trong họ tên.", "action": "Nhập họ tên <script>alert(1)</script>.", "expected": "Hệ thống không lưu/chạy script và phải escape hoặc reject input."},
    {"stt": 81, "code": "REG_17", "scenario": "Email đăng ký phải được trim và chuẩn hóa chữ thường.", "action": "Nhập Email có khoảng trắng và chữ hoa rồi gửi form.", "expected": "Backend trim/lowercase email trước khi kiểm tra trùng và lưu."},
    {"stt": 82, "code": "REG_18", "scenario": "SĐT chỉ được chứa chữ số.", "action": "Nhập SĐT có dấu cách hoặc ký tự đặc biệt.", "expected": "Hệ thống reject hoặc normalize trước khi lưu."},
    {"stt": 83, "code": "REG_19", "scenario": "Mật khẩu quá dài bất thường.", "action": "Nhập mật khẩu dài trên 128 ký tự.", "expected": "Hệ thống xử lý an toàn, không crash và không lưu dữ liệu không hợp lệ."},
    {"stt": 84, "code": "REG_20", "scenario": "Username trùng khác hoa/thường.", "action": "Đăng ký username trùng nhưng đổi chữ hoa/thường.", "expected": "Hệ thống phát hiện trùng và không tạo tài khoản thứ hai."},
    {"stt": 85, "code": "REG_21", "scenario": "Chặn bấm Đăng ký liên tục.", "action": "Bấm nút Đăng ký nhiều lần rất nhanh.", "expected": "Nút submit bị loading/disabled hoặc backend chặn duplicate request."},
    {"stt": 86, "code": "REG_22", "scenario": "Response đăng ký không được trả mật khẩu.", "action": "Gọi API đăng ký hợp lệ và kiểm tra JSON response.", "expected": "Response không chứa password hoặc hashedPassword."},
    {"stt": 87, "code": "REG_23", "scenario": "Tài khoản mới phải có trạng thái active mặc định.", "action": "Tạo tài khoản mới rồi kiểm tra dữ liệu user trả về.", "expected": "User mới có isActive=true hoặc trạng thái tương đương."},
    {"stt": 88, "code": "REG_24", "scenario": "API đăng ký xử lý lỗi server an toàn.", "action": "Đối chiếu source route signup trong nhánh catch.", "expected": "Route gọi handleError và không lộ stack trace nhạy cảm."},
]

LOGIN_TEST_CASES = [
    {"stt": 13, "code": "LOG_01", "scenario": "Đăng nhập bằng Email thành công.", "action": "Nhập đúng Email và Mật khẩu.", "expected": "Chuyển hướng về Trang chủ, header hiển thị Avatar user."},
    {"stt": 14, "code": "LOG_02", "scenario": "Đăng nhập bằng SĐT thành công.", "action": "Nhập đúng SĐT và Mật khẩu.", "expected": "Đăng nhập thành công."},
    {"stt": 15, "code": "LOG_03", "scenario": "Bỏ trống trường dữ liệu.", "action": "Để trống User/Pass và bấm Đăng nhập.", "expected": "Báo lỗi Vui lòng nhập tài khoản và mật khẩu."},
    {"stt": 16, "code": "LOG_04", "scenario": "Sai mật khẩu.", "action": "Nhập đúng Email, sai mật khẩu.", "expected": "Báo lỗi Tài khoản hoặc mật khẩu không chính xác."},
    {"stt": 37, "code": "LOG_05", "scenario": "Đăng nhập thành công bằng tài khoản Google (A1).", "action": "Cửa sổ OAuth hiện ra, xác thực thành công và chuyển về Trang chủ.", "expected": "OAuth xác thực thành công và người dùng quay về Trang chủ."},
    {"stt": 18, "code": "LOG_06", "scenario": "Sai mật khẩu quá số lần quy định.", "action": "Nhập sai pass liên tục 5 lần.", "expected": "Khóa tài khoản tạm thời / Yêu cầu nhập Captcha."},
    {"stt": 19, "code": "LOG_07", "scenario": "Đăng nhập bằng tài khoản bị khóa.", "action": "Dùng tài khoản đã bị Admin chuyển inactive=false.", "expected": "Báo lỗi Tài khoản của bạn đã bị khóa, vui lòng liên hệ CSKH."},
    {"stt": 20, "code": "LOG_08", "scenario": "Kiểm tra Ghi nhớ đăng nhập.", "action": "Tick Remember me -> Đăng nhập -> Tắt trình duyệt -> Mở lại.", "expected": "User vẫn giữ trạng thái đăng nhập."},
    {"stt": 21, "code": "LOG_09", "scenario": "Kiểm tra phân quyền (Authorization).", "action": "Dùng tk Customer cố gắng truy cập /admin/dashboard.", "expected": "Bị chặn (Redirect về trang chủ hoặc lỗi 403)."},
    {"stt": 22, "code": "LOG_10", "scenario": "Kiểm tra nút Back sau khi Logout.", "action": "Đăng nhập -> Đăng xuất -> Bấm nút Back trên trình duyệt.", "expected": "Không truy cập được trang thông tin cá nhân, yêu cầu đăng nhập lại."},
    {"stt": 23, "code": "LOG_11", "scenario": "Phân biệt chữ hoa/thường Mật khẩu.", "action": "Pass là Abc@123, nhập abc@123.", "expected": "Báo lỗi sai mật khẩu (Pass có phân biệt hoa/thường)."},
    {"stt": 24, "code": "LOG_12", "scenario": "Khoảng trắng trong tài khoản.", "action": "Nhập Email có khoảng trắng ở đầu/cuối: test@mail.com", "expected": "Đăng nhập thành công (Hệ thống tự động Trim() khoảng trắng)."},
    {"stt": 67, "code": "LOG_13", "scenario": "Tài khoản không tồn tại.", "action": "Nhập Email chưa từng đăng ký.", "expected": "Báo lỗi Tài khoản không tồn tại."},
    {"stt": 68, "code": "LOG_14", "scenario": "Token không lưu sai nơi khi không tick Remember me.", "action": "Đăng nhập không tick Remember me.", "expected": "Token chỉ lưu sessionStorage, không lưu localStorage dài hạn."},
    {"stt": 69, "code": "LOG_15", "scenario": "Đăng xuất xóa sạch token và thông tin user.", "action": "Đăng nhập rồi bấm Đăng xuất.", "expected": "Token/user trong localStorage và sessionStorage bị xóa."},
    {"stt": 70, "code": "LOG_16", "scenario": "Ô mật khẩu đăng nhập phải mask và không autocomplete nguy hiểm.", "action": "Kiểm tra input password trên form đăng nhập.", "expected": "Input có type=password và cấu hình autocomplete phù hợp."},
    {"stt": 89, "code": "LOG_17", "scenario": "Bỏ trống riêng tài khoản đăng nhập.", "action": "Chỉ nhập mật khẩu, để trống username/email/SĐT.", "expected": "Báo lỗi Tên đăng nhập hoặc số điện thoại là bắt buộc."},
    {"stt": 90, "code": "LOG_18", "scenario": "Bỏ trống riêng mật khẩu đăng nhập.", "action": "Nhập username/email nhưng để trống mật khẩu.", "expected": "Báo lỗi Mật khẩu là bắt buộc."},
    {"stt": 91, "code": "LOG_19", "scenario": "Đăng nhập bằng SĐT dùng đúng nhánh truy vấn phone.", "action": "Nhập chuỗi 10-15 chữ số vào ô đăng nhập.", "expected": "Backend tìm user theo trường phone thay vì username."},
    {"stt": 92, "code": "LOG_20", "scenario": "Response đăng nhập không được trả password.", "action": "Đăng nhập thành công và kiểm tra JSON user.", "expected": "JSON response không chứa password/hash."},
    {"stt": 93, "code": "LOG_21", "scenario": "Token cookie phải có cấu hình bảo mật.", "action": "Đối chiếu hàm sendTokenCookie trong auth helper.", "expected": "Cookie có httpOnly, sameSite và secure theo môi trường phù hợp."},
    {"stt": 94, "code": "LOG_22", "scenario": "Route admin phải yêu cầu auth middleware.", "action": "Dùng Customer truy cập route quản trị.", "expected": "Route admin có auth guard và role guard trước khi trả dữ liệu."},
    {"stt": 95, "code": "LOG_23", "scenario": "Không lộ lý do sai username hay password.", "action": "Đăng nhập sai username hoặc sai password.", "expected": "Thông báo lỗi chung, không chỉ rõ sai trường nào."},
    {"stt": 96, "code": "LOG_24", "scenario": "Logout phải xóa token ở cả header và app state.", "action": "Đăng nhập rồi đăng xuất từ header.", "expected": "Header/app clear localStorage, sessionStorage và cập nhật trạng thái UI."},
]

PASSWORD_TEST_CASES = [
    {"stt": 25, "code": "PWD_01", "scenario": "Thay đổi mật khẩu thành công.", "action": "Nhập đúng Pass cũ, Pass mới hợp lệ, Pass xác nhận khớp.", "expected": "Báo thành công, cập nhật CSDL."},
    {"stt": 26, "code": "PWD_02", "scenario": "Bỏ trống các trường bắt buộc.", "action": "Bấm Lưu nhưng để trống.", "expected": "Cảnh báo yêu cầu điền đầy đủ."},
    {"stt": 27, "code": "PWD_03", "scenario": "Nhập sai Mật khẩu hiện tại.", "action": "Nhập sai Pass cũ.", "expected": "Báo lỗi Mật khẩu hiện tại không đúng."},
    {"stt": 28, "code": "PWD_04", "scenario": "Mật khẩu mới trùng mật khẩu cũ.", "action": "Pass mới nhập y hệt Pass cũ.", "expected": "Báo lỗi Mật khẩu mới phải khác mật khẩu hiện tại."},
    {"stt": 29, "code": "PWD_05", "scenario": "Mật khẩu mới quá ngắn.", "action": "Nhập Pass mới < 8 ký tự.", "expected": "Báo lỗi yêu cầu độ dài."},
    {"stt": 30, "code": "PWD_06", "scenario": "Xác nhận mật khẩu không khớp.", "action": "Pass mới và Pass xác nhận khác nhau.", "expected": "Báo lỗi Mật khẩu xác nhận không khớp."},
    {"stt": 31, "code": "PWD_07", "scenario": "Kiểm tra chức năng Ẩn/Hiện pass.", "action": "Click icon Mắt ở ô nhập mật khẩu.", "expected": "Hiển thị rõ ký tự (Text) / Chuyển thành dấu chấm (Password)."},
    {"stt": 32, "code": "PWD_08", "scenario": "Kiểm tra hành vi sau khi đổi pass.", "action": "Đổi pass thành công.", "expected": "Hệ thống tự động bắt Đăng xuất và yêu cầu Login lại."},
    {"stt": 33, "code": "PWD_09", "scenario": "Dùng pass cũ để đăng nhập lại.", "action": "Đăng xuất, Login bằng Pass cũ.", "expected": "Báo lỗi sai mật khẩu."},
    {"stt": 34, "code": "PWD_10", "scenario": "Tấn công CSRF (Bảo mật).", "action": "Thử gọi API đổi mật khẩu từ một client ngoài mà không có token.", "expected": "Trả về mã lỗi 401 Unauthorized."},
    {"stt": 71, "code": "PWD_11", "scenario": "Mật khẩu mới thiếu chữ hoa/số/ký tự đặc biệt.", "action": "Nhập mật khẩu mới yếu như abcdefgh.", "expected": "Backend reject theo password policy."},
    {"stt": 72, "code": "PWD_12", "scenario": "Người dùng không được đổi mật khẩu của user khác.", "action": "Dùng token user A gọi API change-password cho user B.", "expected": "Trả về 401/403 và không cập nhật mật khẩu user B."},
    {"stt": 73, "code": "PWD_13", "scenario": "Form đổi mật khẩu không được cho submit lặp nhanh 2 lần.", "action": "Bấm Lưu 2 lần liên tiếp.", "expected": "Nút submit bị disable/loading hoặc backend có cơ chế chặn duplicate request."},
    {"stt": 97, "code": "PWD_14", "scenario": "Thiếu mật khẩu hiện tại khi đổi mật khẩu.", "action": "Gửi API chỉ có mật khẩu mới.", "expected": "Backend báo currentPassword là bắt buộc."},
    {"stt": 98, "code": "PWD_15", "scenario": "Thiếu mật khẩu mới khi đổi mật khẩu.", "action": "Gửi API chỉ có mật khẩu hiện tại.", "expected": "Backend báo newPassword là bắt buộc."},
    {"stt": 99, "code": "PWD_16", "scenario": "Mật khẩu mới phải được hash trước khi lưu.", "action": "Đổi mật khẩu thành công rồi đối chiếu source xử lý.", "expected": "Source dùng hashPassword hoặc bcrypt trước khi cập nhật DB."},
    {"stt": 100, "code": "PWD_17", "scenario": "Response đổi mật khẩu không trả password.", "action": "Gọi API đổi mật khẩu thành công.", "expected": "Response không chứa password/hash."},
    {"stt": 101, "code": "PWD_18", "scenario": "Route đổi mật khẩu phải yêu cầu token.", "action": "Đối chiếu route change-password.", "expected": "Route có auth middleware hoặc kiểm tra token bắt buộc."},
    {"stt": 102, "code": "PWD_19", "scenario": "Đổi mật khẩu phải dùng chung password policy với đăng ký.", "action": "Nhập password mới thiếu độ phức tạp.", "expected": "Backend gọi isValidPassword hoặc rule tương đương."},
    {"stt": 103, "code": "PWD_20", "scenario": "User id không tồn tại khi đổi mật khẩu.", "action": "Gọi API change-password với user id không tồn tại.", "expected": "Backend trả 404/400 rõ ràng, không crash server."},
]

CART_TEST_CASES = [
    {"stt": 35, "code": "CRT_01", "scenario": "Thêm sản phẩm thành công.", "action": "Chọn Size/Color, Số lượng = 1, Click Thêm giỏ hàng.", "expected": "Báo thành công, icon giỏ hàng tăng lên 1."},
    {"stt": 36, "code": "CRT_02", "scenario": "Thêm SP chưa chọn thuộc tính.", "action": "Bỏ qua Size/Color, Click Thêm.", "expected": "Báo lỗi/Highlight yêu cầu chọn Kích cỡ, Màu sắc."},
    {"stt": 37, "code": "CRT_03", "scenario": "Thêm SP vượt quá tồn kho.", "action": "Tồn kho có 5, nhập số lượng 6.", "expected": "Báo lỗi Số lượng vượt quá tồn kho hiện tại."},
    {"stt": 38, "code": "CRT_04", "scenario": "Thêm số lượng âm/bằng 0.", "action": "Nhập số lượng 0 hoặc -1.", "expected": "Không cho nhập hoặc quy về mặc định là 1."},
    {"stt": 39, "code": "CRT_05", "scenario": "Cộng dồn số lượng.", "action": "Thêm cùng 1 SP (cùng size/color) 2 lần liên tiếp.", "expected": "Trong giỏ chỉ có 1 dòng SP đó, số lượng = 2."},
    {"stt": 40, "code": "CRT_06", "scenario": "Phân tách SP khác thuộc tính.", "action": "Thêm Giày A (Size 40) và Giày A (Size 41).", "expected": "Trong giỏ hàng tách thành 2 dòng riêng biệt."},
    {"stt": 41, "code": "CRT_07", "scenario": "Cập nhật số lượng trong giỏ hợp lệ.", "action": "Bấm nút [+] tăng số lượng lên 2 trong trang Giỏ hàng.", "expected": "Tự động tính lại Thành tiền của SP đó và Tổng tạm tính."},
    {"stt": 42, "code": "CRT_08", "scenario": "Cập nhật số lượng vượt tồn kho.", "action": "Tăng số lượng trong giỏ lớn hơn tồn kho.", "expected": "Báo lỗi và reset về số lượng max đang có."},
    {"stt": 43, "code": "CRT_09", "scenario": "Cập nhật số lượng bằng text.", "action": "Xóa số trong input, gõ chữ abc.", "expected": "Input tự động block chữ, chỉ nhận số."},
    {"stt": 44, "code": "CRT_10", "scenario": "Xóa 1 sản phẩm khỏi giỏ.", "action": "Bấm icon Thùng rác/Xóa tại 1 SP.", "expected": "Xóa SP đó, load lại giỏ hàng và trừ Tổng tiền."},
    {"stt": 45, "code": "CRT_11", "scenario": "Giỏ hàng khi chưa đăng nhập.", "action": "Khách vãng lai thêm SP vào giỏ (lưu Session).", "expected": "Giỏ hàng lưu thành công."},
    {"stt": 46, "code": "CRT_12", "scenario": "Merge giỏ hàng sau khi Login.", "action": "Khách có giỏ hàng Session -> Đăng nhập.", "expected": "Giỏ hàng cũ của Session gộp vào giỏ hàng của User."},
    {"stt": 47, "code": "CRT_13", "scenario": "Mất mạng khi thêm giỏ hàng.", "action": "Tắt Wifi, click Thêm giỏ hàng.", "expected": "Hiển thị lỗi kết nối, không crash web."},
    {"stt": 74, "code": "CRT_14", "scenario": "Cart identity phải gồm productId + size + color.", "action": "Thêm cùng product nhưng khác size/color rồi xóa 1 dòng.", "expected": "Chỉ dòng đúng biến thể bị xóa/cập nhật."},
    {"stt": 75, "code": "CRT_15", "scenario": "Tổng tiền giỏ hàng phải tính lại phía server.", "action": "Gửi request add/update cart có totalPrice giả mạo.", "expected": "Server không tin totalPrice từ client."},
    {"stt": 76, "code": "CRT_16", "scenario": "Chỉ chủ giỏ hàng mới được đọc/sửa giỏ hàng của mình.", "action": "Dùng token user A gọi API giỏ hàng của user B.", "expected": "Trả về 401/403 hoặc không trả dữ liệu user B."},
    {"stt": 104, "code": "CRT_17", "scenario": "API thêm giỏ hàng phải yêu cầu token.", "action": "Gọi addCart không có Authorization token.", "expected": "Backend trả 401/403."},
    {"stt": 105, "code": "CRT_18", "scenario": "Thiếu productId khi thêm giỏ hàng.", "action": "Gửi addCart thiếu productId.", "expected": "Backend báo productId là bắt buộc."},
    {"stt": 106, "code": "CRT_19", "scenario": "Thiếu size khi thêm giỏ hàng.", "action": "Gửi addCart thiếu size.", "expected": "Backend báo phải chọn size."},
    {"stt": 107, "code": "CRT_20", "scenario": "Thiếu color khi thêm giỏ hàng.", "action": "Gửi addCart thiếu color.", "expected": "Backend báo phải chọn màu sắc."},
    {"stt": 108, "code": "CRT_21", "scenario": "Số lượng giỏ hàng phải là số nguyên.", "action": "Gửi quantity dạng 1.5 hoặc chuỗi.", "expected": "Backend reject dữ liệu không phải số nguyên hợp lệ."},
    {"stt": 109, "code": "CRT_22", "scenario": "Tổng tiền phải cập nhật sau khi xóa sản phẩm.", "action": "Xóa một dòng sản phẩm trong cart.", "expected": "Backend tính lại subtotal/total sau remove."},
    {"stt": 110, "code": "CRT_23", "scenario": "getCart không được nhận userId tùy ý từ URL nếu token khác.", "action": "User A gọi getCart của User B.", "expected": "Backend so khớp req.user.id với userId."},
    {"stt": 111, "code": "CRT_24", "scenario": "Cart không được lưu sản phẩm trùng biến thể.", "action": "Thêm cùng productId + size + color nhiều lần.", "expected": "Backend tăng quantity dòng cũ, không tạo dòng trùng."},
]

CHECKOUT_TEST_CASES = [
    {"stt": 48, "code": "CHK_01", "scenario": "Đặt hàng COD thành công.", "action": "Giỏ hàng có SP, đủ thông tin nhận, chọn Thanh toán khi nhận hàng.", "expected": "Chuyển sang trang Thành công, tạo đơn trong CSDL trạng thái Pending."},
    {"stt": 49, "code": "CHK_02", "scenario": "Checkout khi giỏ hàng trống.", "action": "Nhập URL /checkout trực tiếp khi giỏ trống.", "expected": "Redirect về trang Giỏ hàng / Trang chủ, báo lỗi Giỏ hàng trống."},
    {"stt": 50, "code": "CHK_03", "scenario": "Bỏ trống thông tin giao hàng.", "action": "Xóa SĐT hoặc Địa chỉ và bấm Đặt hàng.", "expected": "Báo lỗi yêu cầu nhập đủ thông tin bắt buộc."},
    {"stt": 51, "code": "CHK_04", "scenario": "Thanh toán Online thành công.", "action": "Chọn Momo/VNPAY -> Nhập thẻ test -> Thanh toán.", "expected": "Cổng TT báo thành công, redirect về web với trạng thái Đã thanh toán."},
    {"stt": 52, "code": "CHK_05", "scenario": "Hủy Thanh toán Online giữa chừng.", "action": "Chọn Momo -> Trang cổng TT mở ra -> Bấm Hủy/Quay lại.", "expected": "Đơn hàng vẫn tạo nhưng trạng thái Chờ thanh toán / Thanh toán thất bại."},
    {"stt": 53, "code": "CHK_06", "scenario": "Áp dụng Voucher hợp lệ.", "action": "Nhập mã GIAM100K.", "expected": "Hệ thống báo thành công, Tổng tiền trừ đi 100.000đ."},
    {"stt": 54, "code": "CHK_07", "scenario": "Voucher sai/không tồn tại.", "action": "Nhập mã SAIBET.", "expected": "Báo lỗi Mã giảm giá không hợp lệ."},
    {"stt": 55, "code": "CHK_08", "scenario": "Voucher đã hết hạn.", "action": "Nhập mã đã qua ngày kết thúc.", "expected": "Báo lỗi Mã giảm giá đã hết hạn sử dụng."},
    {"stt": 56, "code": "CHK_09", "scenario": "Voucher không đủ điều kiện.", "action": "Nhập mã yêu cầu đơn > 500k cho đơn hàng giá 200k.", "expected": "Báo lỗi Đơn hàng chưa đạt giá trị tối thiểu."},
    {"stt": 57, "code": "CHK_10", "scenario": "Xóa Voucher đã áp dụng.", "action": "Bấm nút X ở mục Voucher đang dùng.", "expected": "Hệ thống hủy Voucher, cộng lại Tổng tiền như ban đầu."},
    {"stt": 58, "code": "CHK_11", "scenario": "Kiểm tra cước phí vận chuyển.", "action": "Đổi địa chỉ nhận hàng (vd HCM vs Hà Nội).", "expected": "Hệ thống tự động tính phí Ship tương ứng (nếu có logic phí ship)."},
    {"stt": 59, "code": "CHK_12", "scenario": "Kiểm tra trừ Tồn kho (White-box).", "action": "Checkout thành công SP A (Mua 1). Tồn kho cũ 10.", "expected": "Truy vấn DB: Tồn kho SP A giảm xuống còn 9."},
    {"stt": 60, "code": "CHK_13", "scenario": "SP hết hàng trong lúc Checkout.", "action": "Mở 2 Tab. Tab 1 giữ trang Checkout. Tab 2 mua sạch SP đó. Tab 1 bấm Đặt hàng.", "expected": "Báo lỗi Sản phẩm hiện đã hết hàng và reload giỏ hàng."},
    {"stt": 61, "code": "CHK_14", "scenario": "Email xác nhận đặt hàng.", "action": "Đặt hàng thành công.", "expected": "Kiểm tra Inbox nhận được mail chi tiết hóa đơn."},
    {"stt": 62, "code": "CHK_15", "scenario": "Làm sạch giỏ hàng sau thanh toán.", "action": "Đặt hàng thành công, quay lại trang Giỏ hàng.", "expected": "Giỏ hàng trống rỗng, số lượng icon = 0."},
    {"stt": 77, "code": "CHK_16", "scenario": "Payment method frontend/backend phải đồng nhất.", "action": "Submit checkout với COD/Online theo UI.", "expected": "Giá trị paymentMethod khớp enum backend và không bị reject sai."},
    {"stt": 78, "code": "CHK_17", "scenario": "Checkout không được tạo đơn khi không có token.", "action": "Gọi API tạo đơn hàng không có Authorization token.", "expected": "Trả về 401/403 Unauthorized."},
    {"stt": 79, "code": "CHK_18", "scenario": "Chặn double submit đặt hàng.", "action": "Bấm Xác nhận đặt hàng 2 lần liên tiếp.", "expected": "Chỉ tạo 1 đơn hoặc nút submit bị disable/loading."},
    {"stt": 80, "code": "CHK_19", "scenario": "Tổng tiền đơn hàng phải tính lại phía server.", "action": "Gửi order payload có totalPrice nhỏ hơn thực tế.", "expected": "Server tính lại tổng tiền từ cart/voucher, không tin totalPrice client."},
    {"stt": 112, "code": "CHK_20", "scenario": "Thiếu số điện thoại khi checkout.", "action": "Gửi order thiếu phone.", "expected": "Backend báo số điện thoại là bắt buộc."},
    {"stt": 113, "code": "CHK_21", "scenario": "Số điện thoại checkout sai định dạng.", "action": "Gửi phone=abc hoặc phone quá ngắn.", "expected": "Backend reject phone không hợp lệ."},
    {"stt": 114, "code": "CHK_22", "scenario": "Thiếu địa chỉ giao hàng khi checkout.", "action": "Gửi order thiếu address.", "expected": "Backend báo địa chỉ là bắt buộc."},
    {"stt": 115, "code": "CHK_23", "scenario": "Thiếu phương thức thanh toán.", "action": "Gửi order không có paymentMethod.", "expected": "Backend reject request và không tạo đơn."},
    {"stt": 116, "code": "CHK_24", "scenario": "Tạo đơn thành công phải trả mã đơn hàng.", "action": "Checkout COD thành công.", "expected": "Response có order id duy nhất để tra cứu."},
    {"stt": 117, "code": "CHK_25", "scenario": "Voucher phải giảm usage limit sau khi dùng.", "action": "Áp voucher rồi đặt hàng thành công.", "expected": "Backend cập nhật số lượt sử dụng voucher."},
]

TEST_CASE_GROUPS = [
    {"group_id": "register", "title": "Nhóm Đăng ký tài khoản", "suite_id": "uc-01-su", "module": "Module 1", "description": "Bao phủ đăng ký mới, validation, dữ liệu trùng lặp và nhánh OTP.", "cases": REGISTER_TEST_CASES},
    {"group_id": "login", "title": "Nhóm Đăng nhập", "suite_id": "uc-02-si", "module": "Module 1", "description": "Bao phủ login theo email / SĐT, sai thông tin, phân quyền, remember me và hành vi session.", "cases": LOGIN_TEST_CASES},
    {"group_id": "password", "title": "Nhóm Thay đổi mật khẩu", "suite_id": "uc-03-cp", "module": "Module 1", "description": "Bao phủ validation đổi mật khẩu, hành vi sau đổi mật khẩu và kiểm tra bảo mật cơ bản.", "cases": PASSWORD_TEST_CASES},
    {"group_id": "cart", "title": "Nhóm Giỏ hàng", "suite_id": "uc-04-add-to-cart", "module": "Module 2", "description": "Bao phủ thêm sản phẩm, cập nhật số lượng, merge giỏ hàng và xử lý ngoại lệ phía cart.", "cases": CART_TEST_CASES},
    {"group_id": "checkout", "title": "Nhóm Checkout và Thanh toán", "suite_id": "uc-05-checkout", "module": "Module 2", "description": "Bao phủ COD, online payment, voucher, tồn kho, email xác nhận và làm sạch giỏ hàng.", "cases": CHECKOUT_TEST_CASES},
]

_ALL_TEST_CASES = {
    case["code"]: case
    for group in TEST_CASE_GROUPS
    for case in group["cases"]
}

BASE37_CASE_CODES = [
    "REG_01", "REG_02", "REG_03", "REG_04", "REG_08", "REG_09", "REG_12",
    "LOG_01", "LOG_02", "LOG_03", "LOG_04", "LOG_05", "LOG_06", "LOG_07", "LOG_08", "LOG_09",
    "PWD_01", "PWD_02", "PWD_03", "PWD_04", "PWD_05",
    "CRT_01", "CRT_02", "CRT_04", "CRT_05", "CRT_06", "CRT_07", "CRT_10", "CRT_11",
    "CHK_01", "CHK_02", "CHK_03", "CHK_06", "CHK_07", "CHK_08", "CHK_09", "CHK_15",
]

EXTENDED80_CASE_CODES = [
    case["code"]
    for group in TEST_CASE_GROUPS
    for case in group["cases"]
    if case["code"] not in BASE37_CASE_CODES
]

TIEN_TEST_CASES = [
    {"stt": 38, "code": "REG_13", "scenario": "Nhập dữ liệu có khoảng trắng đầu/cuối.", "action": 'username = " user123 "', "expected": "Hệ thống tự trim và xử lý hợp lệ."},
    {"stt": 39, "code": "REG_14", "scenario": "Nhập SĐT chứa ký tự khoảng trắng.", "action": '"0987 654 321"', "expected": 'Báo lỗi "Số điện thoại không hợp lệ".'},
    {"stt": 40, "code": "REG_15", "scenario": "Nhập password chứa khoảng trắng.", "action": '"Abc@ 1234"', "expected": "Báo lỗi mật khẩu không hợp lệ."},
    {"stt": 41, "code": "REG_16", "scenario": "Nhập username có ký tự đặc biệt.", "action": '"user@@@"', "expected": "Báo lỗi hoặc không cho nhập."},
    {"stt": 42, "code": "REG_17", "scenario": "Nhập username quá dài.", "action": ">255 ký tự", "expected": "Báo lỗi độ dài vượt quá giới hạn."},
    {"stt": 43, "code": "LOG_10", "scenario": "Đăng nhập với khoảng trắng trong username.", "action": '" user123 "', "expected": "Hệ thống trim và login đúng."},
    {"stt": 44, "code": "LOG_11", "scenario": "Đăng nhập với password có khoảng trắng.", "action": '" pass123 "', "expected": "Báo lỗi đăng nhập thất bại."},
    {"stt": 45, "code": "LOG_12", "scenario": "Refresh trang sau khi login.", "action": "Login -> F5", "expected": "Vẫn giữ trạng thái đăng nhập."},
    {"stt": 46, "code": "LOG_13", "scenario": "Truy cập trang sau login khi đã logout.", "action": "Logout -> truy cập lại URL protected", "expected": "Bị redirect về login."},
    {"stt": 47, "code": "PWD_06", "scenario": "Đổi mật khẩu khi chưa đăng nhập.", "action": "Không có token", "expected": "Bị chặn (Unauthorized)."},
    {"stt": 48, "code": "PWD_07", "scenario": "Đổi mật khẩu với newPassword giống currentPassword.", "action": "pass cũ = pass mới", "expected": "Báo lỗi không cho trùng."},
    {"stt": 49, "code": "PWD_08", "scenario": "Đổi mật khẩu thành công và đăng nhập lại.", "action": "Đổi pass -> login pass mới", "expected": "Login thành công."},
    {"stt": 50, "code": "CRT_12", "scenario": "Thêm sản phẩm với số lượng lớn.", "action": "quantity = 999", "expected": "Hệ thống giới hạn hoặc xử lý hợp lệ."},
    {"stt": 51, "code": "CRT_13", "scenario": "Thêm sản phẩm khi giỏ hàng chưa tồn tại.", "action": "user chưa có cart", "expected": "Tạo cart mới."},
    {"stt": 52, "code": "CRT_14", "scenario": "Thêm sản phẩm khi giá có giảm giá.", "action": "product có discount", "expected": "Tính đúng giá sau giảm."},
    {"stt": 53, "code": "CRT_15", "scenario": "Thêm sản phẩm nhiều lần liên tục.", "action": "click add liên tục", "expected": "Không bị duplicate sai."},
    {"stt": 54, "code": "CRT_16", "scenario": "Thêm sản phẩm khi chưa đăng nhập (API).", "action": "không có token", "expected": "Bị chặn."},
    {"stt": 55, "code": "CRT_17", "scenario": "Sau khi thêm sản phẩm kiểm tra totalPrice.", "action": "thêm nhiều SP", "expected": "Tổng tiền tính đúng."},
    {"stt": 56, "code": "CHK_16", "scenario": "Nhập thông tin có khoảng trắng.", "action": '" Nguyễn Văn A "', "expected": "Hệ thống trim dữ liệu."},
    {"stt": 57, "code": "CHK_17", "scenario": "Nhập SĐT có ký tự chữ.", "action": '"09abc12345"', "expected": "Báo lỗi SĐT không hợp lệ."},
    {"stt": 58, "code": "CHK_18", "scenario": "Chọn phương thức thanh toán không hợp lệ.", "action": "paymentMethod = null", "expected": "Báo lỗi."},
    {"stt": 59, "code": "CHK_19", "scenario": "Đặt hàng khi chưa đăng nhập.", "action": "chưa login", "expected": "Bị redirect login."},
    {"stt": 60, "code": "CHK_20", "scenario": "Đặt hàng với danh sách sản phẩm rỗng.", "action": "items = []", "expected": "Báo lỗi không tạo đơn."},
    {"stt": 61, "code": "CHK_21", "scenario": "Sau khi đặt hàng kiểm tra trạng thái đơn.", "action": "tạo order", "expected": 'status = "Pending".'},
    {"stt": 62, "code": "CHK_22", "scenario": "Sau khi đặt hàng kiểm tra xóa giỏ hàng DB.", "action": "tạo order", "expected": "Cart bị xóa."},
    {"stt": 63, "code": "VCH_06", "scenario": "Áp dụng voucher khi total = minOrderValue.", "action": "total = min", "expected": "Voucher hợp lệ."},
    {"stt": 64, "code": "VCH_07", "scenario": "Áp dụng voucher đạt giới hạn usage.", "action": "used = limit", "expected": "Báo lỗi hết lượt."},
    {"stt": 65, "code": "VCH_08", "scenario": "Áp dụng voucher nhiều lần liên tiếp.", "action": "apply nhiều lần", "expected": "Không vượt usageLimit."},
]

TIEN_TEST_CASE_CODES = [case["code"] for case in TIEN_TEST_CASES]


CUSTOM_EXTRA_TEST_CASES = [
    {"stt": 66, "code": "REG_18", "unique_id": "REG_18_CASE_SENSITIVE", "scenario": "Nhập username phân biệt hoa/thường.", "action": '"User123" vs "user123"', "expected": "Hệ thống phân biệt hoặc báo trùng theo rule."},
    {"stt": 67, "code": "REG_19", "unique_id": "REG_19_NUMERIC_USERNAME", "scenario": "Nhập username toàn số.", "action": '"123456"', "expected": "Báo lỗi username không hợp lệ."},
    {"stt": 68, "code": "REG_20", "unique_id": "REG_20_LONG_PHONE", "scenario": "Nhập SĐT vượt độ dài.", "action": ">15 số", "expected": "Báo lỗi SĐT không hợp lệ."},
    {"stt": 70, "code": "REG_22", "unique_id": "REG_22_UNICODE_USERNAME", "scenario": "Nhập ký tự Unicode trong username.", "action": '"tiến123"', "expected": "Lưu đúng dữ liệu UTF-8."},
    {"stt": 76, "code": "CRT_18", "unique_id": "CRT_18_STOCK_ZERO", "scenario": "Thêm sản phẩm khi số lượng tồn kho = 0.", "action": 'Product có stock = 0 -> click "Thêm vào giỏ".', "expected": 'Hiển thị lỗi "Sản phẩm đã hết hàng".'},
    {"stt": 77, "code": "CRT_19", "unique_id": "CRT_19_INVALID_SIZE", "scenario": "Thêm sản phẩm với size không tồn tại.", "action": "Chọn size không hợp lệ.", "expected": 'Hiển thị lỗi "Size không hợp lệ".'},
    {"stt": 78, "code": "CRT_20", "unique_id": "CRT_20_INVALID_COLOR", "scenario": "Thêm sản phẩm với màu không tồn tại.", "action": "Chọn color không hợp lệ.", "expected": 'Hiển thị lỗi "Màu sắc không hợp lệ".'},
    {"stt": 79, "code": "CRT_21", "unique_id": "CRT_21_CART_RELOAD", "scenario": "Kiểm tra giỏ hàng sau khi reload trang.", "action": "Thêm sản phẩm -> refresh (F5).", "expected": "Giỏ hàng vẫn giữ nguyên dữ liệu."},
    {"stt": 80, "code": "CRT_22", "unique_id": "CRT_22_REMOVE_LAST_ITEM", "scenario": "Xóa sản phẩm cuối cùng trong giỏ hàng.", "action": "Xóa item cuối trong giỏ.", "expected": "Giỏ hàng rỗng, tổng tiền = 0."},
    {"stt": 81, "code": "CHK_23", "unique_id": "CHK_23_VALID_CHECKOUT", "scenario": "Đặt hàng với đầy đủ thông tin hợp lệ.", "action": "Nhập đầy đủ thông tin -> đặt hàng.", "expected": 'Tạo đơn hàng thành công, chuyển trang "Thành công".'},
    {"stt": 82, "code": "CHK_24", "unique_id": "CHK_24_LONG_NOTES", "scenario": "Nhập ghi chú đơn hàng vượt độ dài cho phép.", "action": "notes > 255 ký tự.", "expected": "Hệ thống vẫn lưu hoặc cắt bớt hợp lệ."},
    {"stt": 83, "code": "CHK_25", "unique_id": "CHK_25_TOTAL_AFTER_VOUCHER", "scenario": "Kiểm tra tổng tiền sau khi áp dụng voucher.", "action": "Nhập mã giảm giá hợp lệ.", "expected": "Tổng tiền được tính đúng sau khi giảm."},
    {"stt": 84, "code": "CHK_26", "unique_id": "CHK_26_DOUBLE_SUBMIT", "scenario": "Người dùng bấm đặt hàng nhiều lần liên tiếp.", "action": 'Click "Đặt hàng" nhiều lần nhanh.', "expected": "Chỉ tạo 1 đơn hàng duy nhất."},
    {"stt": 85, "code": "CHK_27", "unique_id": "CHK_27_UNIQUE_ORDER_CODE", "scenario": "Kiểm tra mã đơn hàng sau khi tạo.", "action": "Tạo nhiều đơn hàng.", "expected": "Mỗi đơn có mã khác nhau (unique)."},
    {"stt": 76, "code": "CRT_18", "unique_id": "CRT_18_BAD_PRODUCT_ID", "scenario": "Thêm sản phẩm với productId không tồn tại.", "action": 'Nhập productId sai -> click "Thêm vào giỏ".', "expected": 'Hiển thị lỗi "Sản phẩm không tồn tại".'},
    {"stt": 77, "code": "CRT_19", "unique_id": "CRT_19_NO_DISCOUNT_PRICE", "scenario": "Kiểm tra giá sản phẩm khi không có giảm giá.", "action": "Product có discount = 0 -> thêm vào giỏ.", "expected": "Giá sản phẩm được giữ nguyên."},
    {"stt": 78, "code": "CRT_20", "unique_id": "CRT_20_CART_IMAGE", "scenario": "Kiểm tra ảnh sản phẩm trong giỏ hàng.", "action": "Thêm sản phẩm vào giỏ.", "expected": "Hệ thống lưu đúng ảnh đầu tiên của sản phẩm vào giỏ hàng."},
    {"stt": 79, "code": "CRT_21", "unique_id": "CRT_21_MULTI_PRODUCT_TOTAL", "scenario": "Kiểm tra tổng tiền khi giỏ có nhiều sản phẩm khác nhau.", "action": "Thêm nhiều sản phẩm khác nhau vào giỏ.", "expected": "totalPrice bằng tổng price của tất cả item."},
    {"stt": 80, "code": "CRT_22", "unique_id": "CRT_22_ADD_CART_RESPONSE", "scenario": "Kiểm tra phản hồi sau khi thêm sản phẩm thành công.", "action": "Thêm sản phẩm hợp lệ vào giỏ.", "expected": 'API trả về status = true và message thêm thành công.'},
    {"stt": 81, "code": "CHK_23", "unique_id": "CHK_23_MISSING_PROVINCE", "scenario": "Thiếu tỉnh/thành khi đặt hàng.", "action": 'province = null -> bấm "Đặt hàng".', "expected": 'Báo lỗi "Vui lòng chọn tỉnh thành".'},
    {"stt": 82, "code": "CHK_24", "unique_id": "CHK_24_MISSING_DISTRICT", "scenario": "Thiếu quận/huyện khi đặt hàng.", "action": 'district = null -> bấm "Đặt hàng".', "expected": 'Báo lỗi "Vui lòng chọn huyện".'},
    {"stt": 83, "code": "CHK_25", "unique_id": "CHK_25_MISSING_WARD", "scenario": "Thiếu xã/phường khi đặt hàng.", "action": 'ward = null -> bấm "Đặt hàng".', "expected": 'Báo lỗi "Vui lòng chọn xã".'},
    {"stt": 84, "code": "CHK_26", "unique_id": "CHK_26_MISSING_DETAIL", "scenario": "Thiếu địa chỉ chi tiết khi đặt hàng.", "action": 'detail = null -> bấm "Đặt hàng".', "expected": 'Báo lỗi "Số nhà hoặc thôn làng nơi gần bạn nhất".'},
    {"stt": 85, "code": "CHK_27", "unique_id": "CHK_27_CREATE_ORDER_RESPONSE", "scenario": "Kiểm tra phản hồi sau khi tạo đơn hàng thành công.", "action": "Nhập đầy đủ thông tin hợp lệ -> đặt hàng.", "expected": 'API trả về status = true, type = "success" và thông tin order.'},
]

CUSTOM_EXTRA_TEST_CASE_IDS = [case["unique_id"] for case in CUSTOM_EXTRA_TEST_CASES]


RISK_TEST_CASES = [
    {
        "stt": 86,
        "code": "LOG_10",
        "unique_id": "LOG_10_LOGOUT_FLOW",
        "scenario": "Đăng xuất tài khoản (Logout).",
        "action": 'Click vào nút "Đăng xuất" trên Header.',
        "expected": "Hệ thống xóa Token/Cookie, chuyển trạng thái về Khách vãng lai, tự động Redirect về trang Đăng nhập hoặc Trang chủ.",
    },
    {
        "stt": 106,
        "code": "VCH_09",
        "unique_id": "VCH_09_VOUCHER_TRIM",
        "scenario": "Xử lý khoảng trắng khi nhập mã Voucher.",
        "action": 'Nhập mã " GIAM100K " có khoảng trắng đầu/cuối rồi bấm Áp dụng.',
        "expected": "Hệ thống tự động cắt bỏ khoảng trắng đầu/cuối bằng trim và áp dụng mã thành công nếu mã hợp lệ.",
    },
    {
        "stt": 105,
        "code": "CHK_34",
        "unique_id": "CHK_34_NOTES_LENGTH_LIMIT",
        "scenario": "Giới hạn ký tự của ô Ghi chú đơn hàng (Notes).",
        "action": "Dán đoạn văn bản cực dài hơn 2000 ký tự vào ô Ghi chú và bấm Đặt hàng.",
        "expected": "Hệ thống chặn bằng maxlength hoặc cắt bớt chuỗi, không crash server hoặc lỗi CSDL.",
    },
    {
        "stt": 95,
        "code": "CHK_31",
        "unique_id": "CHK_31_XSS_CHECKOUT",
        "scenario": "Kiểm thử bảo mật XSS trên form Thanh toán.",
        "action": "Nhập <script>alert('hack')</script> vào Địa chỉ chi tiết hoặc Ghi chú rồi đặt hàng.",
        "expected": "Hệ thống không thực thi script; dữ liệu được sanitize/escape hoặc báo lỗi ký tự không hợp lệ.",
    },
    {
        "stt": 112,
        "code": "CHK_35",
        "unique_id": "CHK_35_DOUBLE_CLICK_PREVENTION",
        "scenario": "Ngăn chặn việc bấm Submit nhiều lần (Double-Click Prevention).",
        "action": 'Điền đủ form Checkout và spam click thật nhanh vào nút "Xác nhận đặt hàng".',
        "expected": 'Nút submit bị disabled hoặc chuyển "Đang xử lý..." ngay sau click đầu tiên; hệ thống chỉ tạo đúng 1 đơn.',
    },
    {
        "stt": 114,
        "code": "CHK_37",
        "unique_id": "CHK_37_NEGATIVE_QUANTITY_API",
        "scenario": "Chỉnh sửa payload API Checkout bằng số âm.",
        "action": 'Gọi API /api/order/create với items: [{productId: "...", quantity: -5}].',
        "expected": 'Backend validate lại, chặn request và báo lỗi "Số lượng không hợp lệ"; tuyệt đối không tạo đơn hàng tổng tiền âm.',
    },
]

RISK_TEST_CASE_IDS = [case["unique_id"] for case in RISK_TEST_CASES]


EXCEL62_CASE_CODES = [
    "REG_01", "REG_02", "REG_03", "REG_04", "REG_08", "REG_09", "REG_12",
    "LOG_01", "LOG_02", "LOG_03", "LOG_04", "LOG_06", "LOG_07", "LOG_08", "LOG_09",
    "PWD_01", "PWD_02", "PWD_03", "PWD_04", "PWD_05", "PWD_08",
    "CRT_01", "CRT_02", "CRT_04", "CRT_05", "CRT_06", "CRT_07", "CRT_10", "CRT_11",
    "CHK_01", "CHK_02", "CHK_03", "CHK_06", "CHK_07", "CHK_08", "CHK_09", "CHK_15",
    "LOG_05",
    "REG_13", "REG_14", "REG_15", "REG_16", "REG_17",
    "CRT_12", "CRT_13", "CRT_14", "VCH_08",
    "REG_18", "REG_22",
    "CHK_23", "CHK_24", "CHK_25", "CHK_26",
    "LOG_10", "CHK_35", "VCH_09", "CHK_34", "CHK_31",
]

_EXCEL62_OVERRIDES = {
    "REG_18": {
        "stt": 47,
        "scenario": "Nhập username phân biệt hoa/thường.",
        "action": '"User123" vs "user123"',
        "expected": "Hệ thống phân biệt hoặc báo trùng theo rule.",
        "nodeid": "tests/test_custom_extra_cases.py::test_custom_extra_case[REG_18_CASE_SENSITIVE]",
    },
    "REG_22": {
        "stt": 48,
        "scenario": "Nhập ký tự Unicode trong username.",
        "action": '"tiến123"',
        "expected": "Lưu đúng dữ liệu UTF-8.",
        "nodeid": "tests/test_custom_extra_cases.py::test_custom_extra_case[REG_22_UNICODE_USERNAME]",
    },
    "CHK_23": {
        "stt": 49,
        "scenario": "Thiếu tỉnh/thành khi đặt hàng.",
        "action": 'province = null -> bấm "Đặt hàng".',
        "expected": 'Báo lỗi "Vui lòng chọn tỉnh thành".',
        "nodeid": "tests/test_custom_extra_cases.py::test_custom_extra_case[CHK_23_MISSING_PROVINCE]",
    },
    "CHK_24": {
        "stt": 50,
        "scenario": "Thiếu quận/huyện khi đặt hàng.",
        "action": 'district = null -> bấm "Đặt hàng".',
        "expected": 'Báo lỗi "Vui lòng chọn huyện".',
        "nodeid": "tests/test_custom_extra_cases.py::test_custom_extra_case[CHK_24_MISSING_DISTRICT]",
    },
    "CHK_25": {
        "stt": 51,
        "scenario": "Thiếu xã/phường khi đặt hàng.",
        "action": 'ward = null -> bấm "Đặt hàng".',
        "expected": 'Báo lỗi "Vui lòng chọn xã".',
        "nodeid": "tests/test_custom_extra_cases.py::test_custom_extra_case[CHK_25_MISSING_WARD]",
    },
    "CHK_26": {
        "stt": 52,
        "scenario": "Thiếu địa chỉ chi tiết khi đặt hàng.",
        "action": 'detail = null -> bấm "Đặt hàng".',
        "expected": 'Báo lỗi "Số nhà hoặc thôn làng nơi gần bạn nhất".',
        "nodeid": "tests/test_custom_extra_cases.py::test_custom_extra_case[CHK_26_MISSING_DETAIL]",
    },
    "LOG_10": {
        "stt": 53,
        "scenario": "Đăng xuất tài khoản (Logout).",
        "action": 'Click vào nút "Đăng xuất" trên Header.',
        "expected": "Hệ thống xóa Token/Cookie, chuyển trạng thái về Khách vãng lai, tự động Redirect về trang Đăng nhập hoặc Trang chủ.",
        "nodeid": "tests/test_risk_cases.py::test_risk_case[LOG_10_LOGOUT_FLOW]",
    },
    "CHK_35": {
        "stt": 54,
        "scenario": "Ngăn chặn việc bấm Submit nhiều lần (Double-Click Prevention).",
        "action": 'Tại form Thanh toán, điền đủ thông tin và spam click vào nút "Xác nhận đặt hàng".',
        "expected": 'Nút submit bị disabled hoặc chuyển "Đang xử lý..." ngay sau click đầu tiên; hệ thống chỉ tạo đúng 1 đơn.',
        "nodeid": "tests/test_risk_cases.py::test_risk_case[CHK_35_DOUBLE_CLICK_PREVENTION]",
    },
    "VCH_09": {
        "stt": 55,
        "scenario": "Xử lý khoảng trắng khi nhập mã Voucher.",
        "action": 'Nhập mã " GIAM100K " có khoảng trắng đầu/cuối rồi bấm Áp dụng.',
        "expected": "Hệ thống tự động cắt bỏ khoảng trắng đầu/cuối bằng trim và áp dụng mã thành công nếu mã hợp lệ.",
        "nodeid": "tests/test_risk_cases.py::test_risk_case[VCH_09_VOUCHER_TRIM]",
    },
    "CHK_34": {
        "stt": 56,
        "scenario": "Giới hạn ký tự của ô Ghi chú đơn hàng (Notes).",
        "action": "Dán đoạn văn bản cực dài hơn 2000 ký tự vào ô Ghi chú và bấm Đặt hàng.",
        "expected": "Hệ thống chặn bằng maxlength hoặc cắt bớt chuỗi, không crash server hoặc lỗi CSDL.",
        "nodeid": "tests/test_risk_cases.py::test_risk_case[CHK_34_NOTES_LENGTH_LIMIT]",
    },
    "CHK_31": {
        "stt": 95,
        "scenario": "Kiểm thử bảo mật XSS trên form Thanh toán.",
        "action": "Nhập <script>alert('hack')</script> vào Địa chỉ chi tiết hoặc Ghi chú rồi đặt hàng.",
        "expected": "Hệ thống không thực thi script; dữ liệu được sanitize/escape hoặc báo lỗi ký tự không hợp lệ.",
        "nodeid": "tests/test_risk_cases.py::test_risk_case[CHK_31_XSS_CHECKOUT]",
    },
}

_EXCEL62_TIEN_NODEIDS = {
    "REG_13": "tests/test_tien_test_cases.py::test_tien_case[REG_13]",
    "REG_14": "tests/test_tien_test_cases.py::test_tien_case[REG_14]",
    "REG_15": "tests/test_tien_test_cases.py::test_tien_case[REG_15]",
    "REG_16": "tests/test_tien_test_cases.py::test_tien_case[REG_16]",
    "REG_17": "tests/test_tien_test_cases.py::test_tien_case[REG_17]",
    "CRT_12": "tests/test_tien_test_cases.py::test_tien_case[CRT_12]",
    "CRT_13": "tests/test_tien_test_cases.py::test_tien_case[CRT_13]",
    "CRT_14": "tests/test_tien_test_cases.py::test_tien_case[CRT_14]",
    "VCH_08": "tests/test_tien_test_cases.py::test_tien_case[VCH_08]",
}


def _tc62_nodeid_for(code: str) -> str | None:
    for group in TEST_CASE_GROUPS:
        for case in group["cases"]:
            if case["code"] == code:
                function_name = {
                    "register": "test_tc62_register",
                    "login": "test_tc62_login",
                    "password": "test_tc62_password",
                    "cart": "test_tc62_cart",
                    "checkout": "test_tc62_checkout",
                }[group["group_id"]]
                return f"tests/test_tc62_suite.py::{function_name}[{code}]"
    return None


def _excel62_case_for(code: str) -> dict:
    if code in _EXCEL62_OVERRIDES:
        data = {"code": code, **_EXCEL62_OVERRIDES[code]}
        data["source"] = "Excel chi tiết / suite bổ sung"
        return data

    for group in TEST_CASE_GROUPS:
        for case in group["cases"]:
            if case["code"] == code:
                data = {
                    "stt": case["stt"],
                    "code": code,
                    "scenario": case["scenario"],
                    "action": case["action"],
                    "expected": case["expected"],
                    "nodeid": _EXCEL62_TIEN_NODEIDS.get(code) or _tc62_nodeid_for(code),
                    "source": group["title"],
                }
                return data

    for case in TIEN_TEST_CASES:
        if case["code"] == code:
            return {
                "stt": case["stt"],
                "code": code,
                "scenario": case["scenario"],
                "action": case["action"],
                "expected": case["expected"],
                "nodeid": _EXCEL62_TIEN_NODEIDS.get(code) or f"tests/test_tien_test_cases.py::test_tien_case[{code}]",
                "source": "Test Case Của Tiến",
            }

    raise KeyError(f"Chưa map được testcase Excel 62: {code}")


EXCEL62_TEST_CASES = [_excel62_case_for(code) for code in EXCEL62_CASE_CODES]
EXCEL62_TEST_NODEIDS = [case["nodeid"] for case in EXCEL62_TEST_CASES if case.get("nodeid")]


def _cases_for(codes: list[str]) -> list[dict]:
    return [_ALL_TEST_CASES[code] for code in codes]


TEST_CASE_SUBGROUPS = [
    {
        "subgroup_id": "reg-happy-path",
        "suite_id": "tc62-reg-happy-path",
        "module": "Module 1",
        "parent_group": "Đăng ký",
        "title": "Register - Happy Path",
        "technique": "Positive / Smoke",
        "focus": "Kiểm tra luồng đăng ký hợp lệ và điểm chuyển OTP/Đăng nhập.",
        "codes": ["REG_01"],
        "cases": _cases_for(["REG_01"]),
    },
    {
        "subgroup_id": "reg-required",
        "suite_id": "tc62-reg-required",
        "module": "Module 1",
        "parent_group": "Đăng ký",
        "title": "Register - Required Fields",
        "technique": "Required Field Validation",
        "focus": "Bấm Đăng ký khi bỏ trống tất cả trường bắt buộc.",
        "codes": ["REG_02"],
        "cases": _cases_for(["REG_02"]),
    },
    {
        "subgroup_id": "reg-duplicate",
        "suite_id": "tc62-reg-duplicate",
        "module": "Module 1",
        "parent_group": "Đăng ký",
        "title": "Register - Duplicate Data",
        "technique": "Equivalence Partitioning",
        "focus": "Email/SĐT đã tồn tại trong hệ thống phải bị chặn.",
        "codes": ["REG_03", "REG_04"],
        "cases": _cases_for(["REG_03", "REG_04"]),
    },
    {
        "subgroup_id": "reg-format-boundary",
        "suite_id": "tc62-reg-format-boundary",
        "module": "Module 1",
        "parent_group": "Đăng ký",
        "title": "Register - Format & Boundary",
        "technique": "Boundary Value / Invalid Format",
        "focus": "Email sai format, SĐT sai/quá ngắn, password ngắn và confirm pass sai.",
        "codes": ["REG_05", "REG_06", "REG_07", "REG_08", "REG_09"],
        "cases": _cases_for(["REG_05", "REG_06", "REG_07", "REG_08", "REG_09"]),
    },
    {
        "subgroup_id": "reg-otp-security",
        "suite_id": "tc62-reg-otp-security",
        "module": "Module 1",
        "parent_group": "Đăng ký",
        "title": "Register - OTP & Security",
        "technique": "Negative / Security",
        "focus": "OTP sai/hết hạn và payload SQL injection không được tạo tài khoản.",
        "codes": ["REG_10", "REG_11", "REG_12"],
        "cases": _cases_for(["REG_10", "REG_11", "REG_12"]),
    },
    {
        "subgroup_id": "reg-input-hardening",
        "suite_id": "tc80-reg-input-hardening",
        "module": "Module 1",
        "parent_group": "Đăng ký",
        "title": "Register - Input Hardening",
        "technique": "Security / Boundary",
        "focus": "Trim input, username length, password complexity và XSS trong họ tên.",
        "codes": ["REG_13", "REG_14", "REG_15", "REG_16"],
        "cases": _cases_for(["REG_13", "REG_14", "REG_15", "REG_16"]),
    },
    {
        "subgroup_id": "login-success",
        "suite_id": "tc62-login-success",
        "module": "Module 1",
        "parent_group": "Đăng nhập",
        "title": "Login - Success Paths",
        "technique": "Positive / Equivalence",
        "focus": "Đăng nhập thành công bằng username/email và SĐT.",
        "codes": ["LOG_01", "LOG_02"],
        "cases": _cases_for(["LOG_01", "LOG_02"]),
    },
    {
        "subgroup_id": "login-negative",
        "suite_id": "tc62-login-negative",
        "module": "Module 1",
        "parent_group": "Đăng nhập",
        "title": "Login - Invalid Credentials",
        "technique": "Negative / Validation",
        "focus": "Bỏ trống, sai mật khẩu và tài khoản không tồn tại.",
        "codes": ["LOG_03", "LOG_04", "LOG_05"],
        "cases": _cases_for(["LOG_03", "LOG_04", "LOG_05"]),
    },
    {
        "subgroup_id": "login-security-session",
        "suite_id": "tc62-login-security-session",
        "module": "Module 1",
        "parent_group": "Đăng nhập",
        "title": "Login - Security & Session",
        "technique": "Authorization / Session",
        "focus": "Lockout, inactive account, remember me, admin guard, logout-back, case-sensitive password và trim input.",
        "codes": ["LOG_06", "LOG_07", "LOG_08", "LOG_09", "LOG_10", "LOG_11", "LOG_12"],
        "cases": _cases_for(["LOG_06", "LOG_07", "LOG_08", "LOG_09", "LOG_10", "LOG_11", "LOG_12"]),
    },
    {
        "subgroup_id": "login-oauth-storage",
        "suite_id": "tc80-login-oauth-storage",
        "module": "Module 1",
        "parent_group": "Đăng nhập",
        "title": "Login - OAuth & Token Storage",
        "technique": "OAuth / Security",
        "focus": "Google OAuth, nơi lưu token, logout clear storage và cấu hình password input.",
        "codes": ["LOG_13", "LOG_14", "LOG_15", "LOG_16"],
        "cases": _cases_for(["LOG_13", "LOG_14", "LOG_15", "LOG_16"]),
    },
    {
        "subgroup_id": "pwd-validation",
        "suite_id": "tc62-pwd-validation",
        "module": "Module 1",
        "parent_group": "Đổi mật khẩu",
        "title": "Password - Validation",
        "technique": "Required / Negative",
        "focus": "Đổi pass thành công, bỏ trống và sai mật khẩu hiện tại.",
        "codes": ["PWD_01", "PWD_02", "PWD_03"],
        "cases": _cases_for(["PWD_01", "PWD_02", "PWD_03"]),
    },
    {
        "subgroup_id": "pwd-policy-security",
        "suite_id": "tc62-pwd-policy-security",
        "module": "Module 1",
        "parent_group": "Đổi mật khẩu",
        "title": "Password - Policy & Security",
        "technique": "Boundary / Security",
        "focus": "Pass mới trùng pass cũ, quá ngắn, confirm sai, hiện/ẩn pass, logout sau đổi pass và CSRF.",
        "codes": ["PWD_04", "PWD_05", "PWD_06", "PWD_07", "PWD_08", "PWD_09", "PWD_10"],
        "cases": _cases_for(["PWD_04", "PWD_05", "PWD_06", "PWD_07", "PWD_08", "PWD_09", "PWD_10"]),
    },
    {
        "subgroup_id": "pwd-api-hardening",
        "suite_id": "tc80-pwd-api-hardening",
        "module": "Module 1",
        "parent_group": "Đổi mật khẩu",
        "title": "Password - API Hardening",
        "technique": "Security / API Contract",
        "focus": "Password policy nâng cao, chặn đổi pass user khác và chặn double submit.",
        "codes": ["PWD_11", "PWD_12", "PWD_13"],
        "cases": _cases_for(["PWD_11", "PWD_12", "PWD_13"]),
    },
    {
        "subgroup_id": "cart-add-flow",
        "suite_id": "tc62-cart-add-flow",
        "module": "Module 2",
        "parent_group": "Giỏ hàng",
        "title": "Cart - Add Product Flow",
        "technique": "Business Flow / Boundary",
        "focus": "Thêm sản phẩm, bắt buộc chọn thuộc tính, tồn kho, số lượng 0/âm, cộng dồn và tách biến thể.",
        "codes": ["CRT_01", "CRT_02", "CRT_03", "CRT_04", "CRT_05", "CRT_06"],
        "cases": _cases_for(["CRT_01", "CRT_02", "CRT_03", "CRT_04", "CRT_05", "CRT_06"]),
    },
    {
        "subgroup_id": "cart-update-delete",
        "suite_id": "tc62-cart-update-delete",
        "module": "Module 2",
        "parent_group": "Giỏ hàng",
        "title": "Cart - Update/Delete",
        "technique": "Regression / UI Contract",
        "focus": "Cập nhật số lượng, chặn text, vượt tồn kho và xóa sản phẩm.",
        "codes": ["CRT_07", "CRT_08", "CRT_09", "CRT_10"],
        "cases": _cases_for(["CRT_07", "CRT_08", "CRT_09", "CRT_10"]),
    },
    {
        "subgroup_id": "cart-session-network",
        "suite_id": "tc62-cart-session-network",
        "module": "Module 2",
        "parent_group": "Giỏ hàng",
        "title": "Cart - Session & Network",
        "technique": "Session / Resilience",
        "focus": "Giỏ hàng guest, merge sau login và lỗi kết nối khi add cart.",
        "codes": ["CRT_11", "CRT_12", "CRT_13"],
        "cases": _cases_for(["CRT_11", "CRT_12", "CRT_13"]),
    },
    {
        "subgroup_id": "cart-integrity-security",
        "suite_id": "tc80-cart-integrity-security",
        "module": "Module 2",
        "parent_group": "Giỏ hàng",
        "title": "Cart - Integrity & Authorization",
        "technique": "Security / Data Integrity",
        "focus": "Định danh biến thể cart, server-side total và authorization giỏ hàng.",
        "codes": ["CRT_14", "CRT_15", "CRT_16"],
        "cases": _cases_for(["CRT_14", "CRT_15", "CRT_16"]),
    },
    {
        "subgroup_id": "checkout-core",
        "suite_id": "tc62-checkout-core",
        "module": "Module 2",
        "parent_group": "Checkout",
        "title": "Checkout - Core Flow",
        "technique": "Business Flow / Validation",
        "focus": "Đặt hàng COD, checkout khi giỏ trống và validation thông tin giao hàng.",
        "codes": ["CHK_01", "CHK_02", "CHK_03"],
        "cases": _cases_for(["CHK_01", "CHK_02", "CHK_03"]),
    },
    {
        "subgroup_id": "checkout-online-payment",
        "suite_id": "tc62-checkout-online-payment",
        "module": "Module 2",
        "parent_group": "Checkout",
        "title": "Checkout - Online Payment",
        "technique": "Payment Flow",
        "focus": "Thanh toán online thành công và hủy thanh toán giữa chừng.",
        "codes": ["CHK_04", "CHK_05"],
        "cases": _cases_for(["CHK_04", "CHK_05"]),
    },
    {
        "subgroup_id": "checkout-voucher",
        "suite_id": "tc62-checkout-voucher",
        "module": "Module 2",
        "parent_group": "Checkout",
        "title": "Checkout - Voucher",
        "technique": "Decision Table",
        "focus": "Voucher hợp lệ, sai mã, hết hạn, không đủ điều kiện và xóa voucher.",
        "codes": ["CHK_06", "CHK_07", "CHK_08", "CHK_09", "CHK_10"],
        "cases": _cases_for(["CHK_06", "CHK_07", "CHK_08", "CHK_09", "CHK_10"]),
    },
    {
        "subgroup_id": "checkout-fulfillment",
        "suite_id": "tc62-checkout-fulfillment",
        "module": "Module 2",
        "parent_group": "Checkout",
        "title": "Checkout - Fulfillment",
        "technique": "White-box / Integration",
        "focus": "Phí ship, trừ tồn kho, hết hàng lúc checkout, email xác nhận và làm sạch giỏ hàng.",
        "codes": ["CHK_11", "CHK_12", "CHK_13", "CHK_14", "CHK_15"],
        "cases": _cases_for(["CHK_11", "CHK_12", "CHK_13", "CHK_14", "CHK_15"]),
    },
    {
        "subgroup_id": "checkout-security-integrity",
        "suite_id": "tc80-checkout-security-integrity",
        "module": "Module 2",
        "parent_group": "Checkout",
        "title": "Checkout - Security & Integrity",
        "technique": "Security / Source Audit",
        "focus": "Đồng bộ payment enum, auth token, double submit và server-side total.",
        "codes": ["CHK_16", "CHK_17", "CHK_18", "CHK_19"],
        "cases": _cases_for(["CHK_16", "CHK_17", "CHK_18", "CHK_19"]),
    },
]

TEST_CASE_EXCEL_REFERENCE = {
    "path": r"C:\Users\clubb\Downloads\Danh sách 62 Test Case Chi Tiết.xlsx",
    "listed_cases": 37,
    "base_cases": len(BASE37_CASE_CODES),
    "extended_cases": len(EXTENDED80_CASE_CODES),
    "automation_cases": sum(len(group["cases"]) for group in TEST_CASE_GROUPS),
    "detail_sheets_found": 33,
    "detail_sheets_missing": 84,
    "note": "File Excel gốc có 37 mã TC dùng làm bộ nền trong đồ án. Bộ automation hiện có 80 mã mở rộng không trùng bộ nền, tổng cộng 117 TC; LOG_9 được chuẩn hóa thành LOG_09 khi đối chiếu.",
    "missing_detail_codes": [
        "LOG_05", "LOG_10", "LOG_11", "LOG_12",
        "PWD_06", "PWD_07", "PWD_09", "PWD_10",
        "CRT_03", "CRT_05", "CRT_08", "CRT_09", "CRT_11", "CRT_12", "CRT_13",
        "CHK_01", "CHK_02", "CHK_04", "CHK_05", "CHK_06", "CHK_07", "CHK_08",
        "CHK_09", "CHK_10", "CHK_11", "CHK_12", "CHK_13", "CHK_14", "CHK_15",
        "REG_13", "REG_14", "REG_15", "REG_16",
        "LOG_13", "LOG_14", "LOG_15", "LOG_16",
        "PWD_11", "PWD_12", "PWD_13",
        "CRT_14", "CRT_15", "CRT_16",
        "CHK_16", "CHK_17", "CHK_18", "CHK_19",
    ],
}

TEST_CASE_SUMMARY = {
    "total_cases": sum(len(group["cases"]) for group in TEST_CASE_GROUPS),
    "base_37_cases": len(BASE37_CASE_CODES),
    "extended_80_cases": len(EXTENDED80_CASE_CODES),
    "tien_cases": len(TIEN_TEST_CASES),
    "custom_extra_cases": len(CUSTOM_EXTRA_TEST_CASES),
    "risk_cases": len(RISK_TEST_CASES),
    "excel62_cases": len(EXCEL62_TEST_CASES),
    "group_count": len(TEST_CASE_GROUPS),
    "subgroup_count": len(TEST_CASE_SUBGROUPS),
    "module_1_cases": len(REGISTER_TEST_CASES) + len(LOGIN_TEST_CASES) + len(PASSWORD_TEST_CASES),
    "module_2_cases": len(CART_TEST_CASES) + len(CHECKOUT_TEST_CASES),
}


PROJECT_WORD_DATA = {
    "institution": [
        "BỘ GIÁO DỤC VÀ ĐÀO TẠO",
        "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT TP HCM",
        "KHOA CÔNG NGHỆ THÔNG TIN",
    ],
    "title": "Báo cáo cuối kỳ: XÂY DỰNG KIỂM THỬ WEBSITE BÁN GIÀY",
    "course": "Kiểm thử phần mềm",
    "class_code": "SOTE431079",
    "instructor": "Ths Nguyễn Trần Thi Văn",
    "semester": "Học kỳ II: 2025-2026",
    "city_line": "TP HCM, ngày ... tháng ... năm 2026",
    "source_project_root": SOURCE_PROJECT_ROOT,
    "source_note": (
        "Dữ liệu báo cáo dưới đây được cập nhật theo bản Word mới và được đối chiếu trực tiếp "
        "với source chuẩn WEB-MERN_t10-2024 để tăng chiều sâu kiểm thử. Nội dung trên giao diện "
        "không chỉ mô tả use case mà còn gắn với các điểm có thể automation, source audit và bug thực tế."
    ),
    "students": [
        {"student_id": "24810036", "name": "NGÔ QUANG LỢI"},
        {"student_id": "24810038", "name": "NGUYỄN CÔNG QUỐC"},
        {"student_id": "24810044", "name": "TRỊNH NHẬT TIẾN"},
    ],
    "chapters": [
        "Chương 1. Tổng quan về đề tài",
        "Chương 2. Yêu cầu đặc tả Use Case",
        "Chương 3. Kế hoạch kiểm thử (Test Plan)",
        "Chương 4. Cơ sở lý thuyết",
        "Chương 5. Kiểm thử hộp trắng (White-box Testing)",
        "Chương 6. Kiểm thử hộp đen (Black-box Testing)",
        "Chương 7. Quản lý lỗi (Bug Management)",
        "Chương 8. Tổng kết",
    ],
    "goals": [
        "Vận dụng các kỹ thuật thiết kế test case hộp đen như phân vùng tương đương, giá trị biên, bảng quyết định và đoán lỗi vào dự án website bán giày.",
        "Xây dựng Test Plan và bộ test case có độ bao phủ cao cho các luồng nghiệp vụ trọng yếu của khách hàng.",
        "Thực thi kiểm thử tự động và thủ công, ghi nhận bug theo chuẩn, xuất báo cáo HTML/XML/Excel/Word phục vụ đồ án.",
        "Đánh giá chất lượng hiện tại của website và chỉ ra các điểm cần tối ưu về luồng nghiệp vụ, UI/UX và tính đúng đắn giữa frontend/backend.",
    ],
    "rationale": [
        "Website bán giày có nghiệp vụ phức tạp hơn bán lẻ thông thường do phải quản lý biến thể Size, Màu sắc và trạng thái tồn kho theo thời gian thực.",
        "Các lỗi nhỏ như cho phép đặt hàng khi hết size, tính sai phí vận chuyển hoặc áp voucher sai có thể ảnh hưởng trực tiếp đến doanh thu và uy tín hệ thống.",
        "Nhóm chọn đề tài này để đưa lý thuyết kiểm thử phần mềm vào một dự án có luồng nghiệp vụ thực tế và dễ phát sinh lỗi logic.",
    ],
    "test_object": {
        "app_name": "Hệ thống website bán giày trực tuyến",
        "platform": "Web Application",
        "environment": [
            "Trình duyệt chính: Google Chrome",
            "Hệ điều hành kiểm thử: Windows 10/11",
            "Site public đang test: https://guangli-shop.netlify.app/",
            f"Source chuẩn đối chiếu: {SOURCE_PROJECT_ROOT}",
        ],
    },
    "scope_statement": (
        "Nhóm không kiểm thử toàn bộ 100% tính năng mà tập trung đi sâu vào 2 module cốt lõi ảnh hưởng trực tiếp "
        "đến trải nghiệm người dùng, tính bảo mật và quy trình tạo doanh thu: xác thực/tài khoản và giao dịch cốt lõi."
    ),
    "analysis_summary": [
        "Module 1 đối chiếu trực tiếp với frontend/src/Pages/AuthSignIn, frontend/src/Pages/AuthSignUp, frontend/src/Pages/MyAccount, server/routes/userRoutes.js và server/middlewares/validate.js.",
        "Module 2 đối chiếu trực tiếp với frontend/src/Pages/ProductDetails, frontend/src/Pages/Cart, frontend/src/Pages/Checkout, frontend/src/Components/Voucher, server/routes/cartRoutes.js và server/routes/orderRoutes.js.",
        "Phần kiểm thử hiện đã có đủ lớp UI automation, runtime audit, source audit và source conformance để phát hiện lỗi thật thay vì chỉ mô tả lý thuyết.",
    ],
    "test_case_summary": TEST_CASE_SUMMARY,
    "test_case_suites": TEST_CASE_GROUPS,
    "test_case_subgroups": TEST_CASE_SUBGROUPS,
    "tien_test_cases": TIEN_TEST_CASES,
    "custom_extra_test_cases": CUSTOM_EXTRA_TEST_CASES,
    "risk_test_cases": RISK_TEST_CASES,
    "excel62_test_cases": EXCEL62_TEST_CASES,
    "excel62_workbook_path": r"C:\Users\clubb\Downloads\Danh sách 62 Test Case Chi Tiết (1).xlsx",
    "test_case_excel_reference": TEST_CASE_EXCEL_REFERENCE,
    "functional_requirements": [
        {
            "stt": "1",
            "task": "Đăng ký tài khoản",
            "type": "Xử lý / Lưu trữ",
            "rules": "Email hoặc SĐT chưa từng đăng ký; mật khẩu có ít nhất 1 ký tự đặc biệt, 1 chữ in hoa, 1 số và dài tối thiểu 8 ký tự.",
            "form": "FORM_DK",
            "notes": "Tạo mới thông tin người dùng trong cơ sở dữ liệu.",
        },
        {
            "stt": "2",
            "task": "Đăng nhập hệ thống",
            "type": "Tra cứu / Xử lý",
            "rules": "Email hoặc SĐT và mật khẩu phải khớp DB; sai thông tin phải hiển thị cảnh báo; có thể khóa tạm nếu sai quá 5 lần.",
            "form": "FORM_DN",
            "notes": "Lưu trạng thái đăng nhập bằng cookie hoặc token để tiếp tục mua hàng.",
        },
        {
            "stt": "3",
            "task": "Thay đổi mật khẩu",
            "type": "Xử lý / Cập nhật",
            "rules": "Bắt buộc nhập đúng mật khẩu hiện tại; mật khẩu mới và nhập lại mật khẩu mới phải trùng khớp.",
            "form": "FORM_TDMK",
            "notes": "Yêu cầu đăng nhập lại sau khi đổi mật khẩu thành công.",
        },
        {
            "stt": "4",
            "task": "Thêm giày vào giỏ hàng",
            "type": "Xử lý",
            "rules": "Bắt buộc chọn Size và Màu sắc; số lượng thêm không vượt quá tồn kho.",
            "form": "Nút thêm vào giỏ hàng / Trang chi tiết sản phẩm",
            "notes": "Nếu cùng product-size-color đã có trong giỏ thì chỉ tăng số lượng, không tạo dòng mới.",
        },
        {
            "stt": "5",
            "task": "Cập nhật / Xóa sản phẩm trong giỏ",
            "type": "Xử lý",
            "rules": "Số lượng cập nhật phải > 0; nếu giảm về 0 hoặc bấm xóa thì sản phẩm bị loại khỏi giỏ.",
            "form": "Trang giỏ hàng",
            "notes": "Tổng tiền tạm tính phải cập nhật ngay khi số lượng thay đổi.",
        },
        {
            "stt": "6",
            "task": "Nhập thông tin thanh toán",
            "type": "Xử lý",
            "rules": "Bắt buộc nhập Họ tên, SĐT, địa chỉ nhận hàng chi tiết.",
            "form": "FORM_CHECKOUT",
            "notes": "Thông báo lỗi phải hiển thị màu đỏ tại trường thiếu dữ liệu.",
        },
        {
            "stt": "7",
            "task": "Xác nhận đặt hàng",
            "type": "Xử lý / Lưu trữ",
            "rules": "Tổng tiền = Giá giày x Số lượng + phí vận chuyển; tồn kho phải bị trừ ngay khi xác nhận đơn.",
            "form": "Trang theo dõi đơn hàng",
            "notes": "Hệ thống phải sinh một mã đơn hàng duy nhất.",
        },
    ],
    "non_functional_requirements": [
        {
            "stt": "1",
            "task": "Bảo mật dữ liệu",
            "type": "Hệ thống",
            "rules": "Mật khẩu phải được mã hóa trước khi lưu; tự động đăng xuất nếu không hoạt động trong 30 phút.",
            "form": "Toàn hệ thống",
            "notes": "Ưu tiên kiểm tra chặt cho module tài khoản và lúc checkout.",
        },
        {
            "stt": "2",
            "task": "Hiệu suất và tốc độ",
            "type": "Hệ thống",
            "rules": "Response time cho Thêm vào giỏ hoặc Xác nhận đặt hàng phải dưới 3 giây; tải trang không quá 5 giây với mạng tiêu chuẩn.",
            "form": "Toàn hệ thống",
            "notes": "Đảm bảo trải nghiệm mua sắm không bị gián đoạn.",
        },
        {
            "stt": "3",
            "task": "Tính tương thích",
            "type": "Hệ thống",
            "rules": "Hoạt động ổn định trên Google Chrome, Safari và Microsoft Edge.",
            "form": "Giao diện",
            "notes": "Automation hiện tập trung trên Google Chrome.",
        },
        {
            "stt": "4",
            "task": "Tính khả dụng",
            "type": "Hệ thống",
            "rules": "Giao diện phải responsive trên mobile/tablet, không vỡ layout; lỗi phải rõ ràng, màu đỏ dễ nhìn.",
            "form": "Giao diện",
            "notes": "Đây là phần nhóm đang test sâu bằng UI/layout assertions.",
        },
    ],
    "actors": [
        {
            "actor": "Khách vãng lai (Client / Guest)",
            "use_cases": [
                "Xem sản phẩm (trang chủ, duyệt danh mục, tìm kiếm, xem chi tiết)",
                "Thêm vào giỏ hàng",
                "Đăng ký tài khoản",
                "Đăng nhập hệ thống",
                "Gửi liên hệ hỗ trợ",
            ],
        },
        {
            "actor": "Khách hàng (Customer)",
            "use_cases": [
                "Quản lý giỏ hàng",
                "Đặt hàng và Thanh toán",
                "Theo dõi đơn hàng",
                "Quản lý tài khoản / đổi mật khẩu / cập nhật thông tin",
                "Đánh giá sản phẩm",
                "Quản lý sản phẩm yêu thích",
            ],
        },
        {
            "actor": "Quản trị viên (Admin)",
            "use_cases": [
                "Đăng nhập quản trị",
                "Xem thống kê Dashboard",
                "Quản lý danh mục, sản phẩm, đơn hàng, người dùng, voucher",
                "Quản lý giao diện banner/logo",
            ],
        },
    ],
    "modules": [
        {
            "id": "module-1",
            "title": "Module 1: Xác thực và Quản lý tài khoản",
            "subtitle": "Đăng ký / Đăng nhập / Thay đổi mật khẩu",
            "scope": "Áp dụng Black-box Testing với phân lớp tương đương, giá trị biên, validation form và kiểm tra UI/UX. Đồng thời đối chiếu source để phát hiện gap về reset/forgot password và contract xác thực.",
            "suite_id": "module-1",
            "source_files": [
                r"frontend\src\Pages\AuthSignUp\index.js",
                r"frontend\src\Pages\AuthSignIn\index.js",
                r"frontend\src\Pages\MyAccount\MyAccount.jsx",
                r"server\routes\userRoutes.js",
                r"server\middlewares\validate.js",
            ],
            "focus_checks": [
                "Bắt lỗi trường bắt buộc, sai định dạng phone, password yếu, confirmPassword không khớp và tài khoản trùng lặp.",
                "Đăng nhập bằng username hoặc phone, sai thông tin, tài khoản bị khóa, trạng thái session/token sau login.",
                "Kiểm tra tab đổi mật khẩu, số lượng field, yêu cầu current password và tính đồng bộ với đặc tả báo cáo.",
                "Đối chiếu điểm vào Quên mật khẩu để chỉ ra khoảng trống giữa đặc tả yêu cầu và website public hiện tại.",
            ],
            "detailed_tests": [
                {
                    "case_id": "M1-STEP-01",
                    "title": "Đăng ký với dữ liệu hợp lệ",
                    "steps": [
                        "Mở trang chủ, vào Đăng nhập rồi chuyển sang Đăng ký.",
                        "Nhập username mới, full name, phone hợp lệ, password đạt chuẩn và confirmPassword trùng khớp.",
                        "Gửi form và theo dõi thông báo trả về.",
                    ],
                    "expected": "Tài khoản mới được tạo thành công hoặc có thông báo success phù hợp.",
                },
                {
                    "case_id": "M1-STEP-02",
                    "title": "Đăng nhập bằng username hoặc phone",
                    "steps": [
                        "Mở trang Đăng nhập.",
                        "Nhập username đúng và password đúng, sau đó lặp lại với phone đúng.",
                        "Nhấn Đăng nhập và kiểm tra token/session được lưu.",
                    ],
                    "expected": "Đăng nhập thành công ở cả hai nhánh username và phone.",
                },
                {
                    "case_id": "M1-STEP-03",
                    "title": "Đổi mật khẩu từ trang My Account",
                    "steps": [
                        "Đăng nhập rồi mở trang My Account.",
                        "Chuyển sang tab Thay đổi mật khẩu.",
                        "Kiểm tra số lượng ô mật khẩu và mức độ khớp với yêu cầu đặc tả.",
                    ],
                    "expected": "Phải có đủ trường để nhập mật khẩu hiện tại, mật khẩu mới và nhập lại mật khẩu mới.",
                },
                {
                    "case_id": "M1-STEP-04",
                    "title": "Đối chiếu điểm vào Quên mật khẩu",
                    "steps": [
                        "Mở trang Đăng nhập.",
                        "Click Quên mật khẩu?.",
                        "Theo dõi route và phản hồi UI sau click.",
                    ],
                    "expected": "Phải chuyển sang luồng reset password hoặc màn hình tương đương.",
                },
            ],
            "detected_bugs": [
                {
                    "bug_id": "BUG_FP_01",
                    "severity": "HIGH",
                    "title": "Link Quên mật khẩu trên frontend chính chưa có route hợp lệ",
                    "evidence": r"frontend\src\Pages\AuthSignIn\index.js:222-223",
                    "impact": "Đặc tả reset/forgot password không đi được qua bước điều hướng đầu tiên.",
                },
                {
                    "bug_id": "BUG_SU_01",
                    "severity": "MEDIUM",
                    "title": "Validation đăng ký phía client không return ngay khi gặp lỗi",
                    "evidence": r"frontend\src\Pages\AuthSignUp\index.js:71-126",
                    "impact": "Form có thể tiếp tục đi xuống luồng submit dù đã set cảnh báo validation.",
                },
                {
                    "bug_id": "BUG_CP_01",
                    "severity": "MEDIUM",
                    "title": "Màn hình đổi mật khẩu chưa có ô nhập lại mật khẩu mới",
                    "evidence": r"frontend\src\Pages\MyAccount\MyAccount.jsx:220-241",
                    "impact": "Không đáp ứng đúng yêu cầu đặc tả bắt buộc xác nhận lại mật khẩu mới.",
                },
            ],
        },
        {
            "id": "module-2",
            "title": "Module 2: Giao dịch cốt lõi",
            "subtitle": "Quản lý Giỏ hàng và Thanh toán (Checkout)",
            "scope": "Áp dụng Black-box Testing cho luồng thêm, sửa, xóa sản phẩm trong giỏ hàng và checkout. Kết hợp White-box/Source Audit cho phần tính tiền, voucher, contract paymentMethod và logic phân biệt biến thể product-size-color.",
            "suite_id": "module-2",
            "source_files": [
                r"frontend\src\Pages\ProductDetails\index.js",
                r"frontend\src\Pages\Cart\index.js",
                r"frontend\src\Pages\Checkout\index.js",
                r"frontend\src\Components\Voucher\index.js",
                r"server\routes\cartRoutes.js",
                r"server\routes\orderRoutes.js",
                r"server\middlewares\validate.js",
            ],
            "focus_checks": [
                "Thêm vào giỏ phải bắt buộc chọn Size/Màu và không được vượt quá số lượng tồn kho.",
                "Cập nhật hoặc xóa sản phẩm trong giỏ phải phân biệt đầy đủ productId + size + color.",
                "Voucher phải đúng minOrderValue, usageLimit, kiểu phần trăm/tiền mặt và phải cập nhật tổng tiền tức thời.",
                "Checkout phải đồng bộ dữ liệu giao hàng, paymentMethod và shape payload giữa frontend/backend.",
            ],
            "detailed_tests": [
                {
                    "case_id": "M2-STEP-01",
                    "title": "Thêm đúng biến thể sản phẩm vào giỏ",
                    "steps": [
                        "Mở trang chi tiết sản phẩm.",
                        "Chọn size, màu và số lượng hợp lệ.",
                        "Nhấn Thêm vào giỏ hàng và theo dõi badge giỏ hàng.",
                    ],
                    "expected": "Sản phẩm được thêm thành công và nếu cùng biến thể đã tồn tại thì chỉ tăng số lượng.",
                },
                {
                    "case_id": "M2-STEP-02",
                    "title": "Cập nhật và xóa item trong giỏ",
                    "steps": [
                        "Mở trang giỏ hàng đã seed dữ liệu.",
                        "Tăng/giảm số lượng rồi xóa một item cụ thể.",
                        "Đối chiếu tổng tiền và danh sách item còn lại.",
                    ],
                    "expected": "Tổng tiền cập nhật đúng và chỉ item được chọn mới bị xóa.",
                },
                {
                    "case_id": "M2-STEP-03",
                    "title": "Áp voucher ở ngưỡng minOrderValue",
                    "steps": [
                        "Chuẩn bị tổng tiền đúng bằng minOrderValue của voucher.",
                        "Nhập voucher và nhấn Áp dụng.",
                        "Lặp lại với tổng tiền thấp hơn minOrderValue đúng 1 đơn vị.",
                    ],
                    "expected": "Voucher được chấp nhận ở ngưỡng bằng và bị từ chối ở ngưỡng thấp hơn.",
                },
                {
                    "case_id": "M2-STEP-04",
                    "title": "Checkout với COD và thông tin giao hàng hợp lệ",
                    "steps": [
                        "Mở trang Checkout với giỏ hàng đã có dữ liệu.",
                        "Nhập đủ họ tên, số điện thoại, địa chỉ chi tiết và ghi chú.",
                        "Chọn COD rồi xác nhận đặt hàng.",
                    ],
                    "expected": "Frontend và backend phải hiểu cùng một paymentMethod để tạo đơn hàng thành công.",
                },
            ],
            "detected_bugs": [
                {
                    "bug_id": "BUG_CO_01",
                    "severity": "HIGH",
                    "title": "Frontend và backend lệch chuẩn paymentMethod",
                    "evidence": r"frontend\src\Pages\Checkout\index.js:431-436 | server\middlewares\validate.js:67",
                    "impact": "Frontend gửi cash/payment trong khi backend chỉ chấp nhận COD/Online.",
                },
                {
                    "bug_id": "BUG_CA_01",
                    "severity": "HIGH",
                    "title": "API removeCart chỉ dựa vào productId, bỏ qua size và color",
                    "evidence": r"server\routes\cartRoutes.js:184-200",
                    "impact": "Có thể xóa nhầm item nếu cùng một sản phẩm tồn tại nhiều biến thể.",
                },
                {
                    "bug_id": "BUG_UI_01",
                    "severity": "MEDIUM",
                    "title": "Điều kiện render dùng sai chính tả lenght",
                    "evidence": r"frontend\src\Pages\Cart\index.js:274 | frontend\src\Pages\Checkout\index.js:398",
                    "impact": "Logic hiển thị trạng thái rỗng hoặc điều kiện business bị sai ý định thiết kế.",
                },
            ],
        },
    ],
    "use_cases": [
        {
            "use_case_id": "UC_01_SU",
            "title": "Đăng ký tài khoản",
            "actor": "Guest (Khách chưa có tài khoản)",
            "description": "Cho phép khách đăng ký tài khoản bằng thông tin cá nhân. Hệ thống sử dụng OTP để xác thực và chỉ chấp nhận dữ liệu đầu vào hợp lệ.",
            "precondition": "Truy cập thành công vào trang chủ website.",
            "postcondition": "Tài khoản mới được tạo thành công trong CSDL.",
            "main_flow": [
                "Từ trang chủ bấm Đăng nhập.",
                "Chuyển sang trang Đăng nhập rồi bấm Đăng ký.",
                "Nhập Họ tên, Tên đăng nhập, Số điện thoại, Mật khẩu, Nhập lại mật khẩu.",
                "Bấm Đăng ký và chờ phản hồi xác thực.",
            ],
            "exception_flow": [
                "Bỏ trống trường bắt buộc.",
                "Số điện thoại sai định dạng hoặc trùng lặp.",
                "Username trùng lặp.",
                "Mật khẩu không đạt chuẩn hoặc confirmPassword không khớp.",
                "OTP sai hoặc hết hạn.",
            ],
            "suite_id": "uc-01-su",
            "detailed_tests": [
                {
                    "test_id": "UC01-T01",
                    "title": "Happy path - đăng ký hợp lệ",
                    "technique": "Phân lớp tương đương (hợp lệ)",
                    "steps": [
                        "Mở form Đăng ký.",
                        "Nhập dữ liệu hợp lệ cho tất cả trường.",
                        "Gửi form và theo dõi phản hồi.",
                    ],
                    "expected": "Tài khoản được tạo thành công.",
                },
                {
                    "test_id": "UC01-T02",
                    "title": "Thiếu trường bắt buộc",
                    "technique": "Phân lớp tương đương (không hợp lệ)",
                    "steps": [
                        "Để trống lần lượt từng trường username, phone, fullName, password, confirmPassword.",
                        "Gửi form.",
                    ],
                    "expected": "Form phải dừng ở lỗi đầu tiên và hiển thị message phù hợp.",
                },
                {
                    "test_id": "UC01-T03",
                    "title": "Phone sai định dạng hoặc trùng lặp",
                    "technique": "Giá trị biên / bảng quyết định",
                    "steps": [
                        "Nhập phone sai format hoặc dùng lại phone đã có trong hệ thống.",
                        "Gửi form.",
                    ],
                    "expected": "Hiển thị lỗi rõ ràng, không tạo user.",
                },
                {
                    "test_id": "UC01-T04",
                    "title": "Confirm password không khớp",
                    "technique": "Bảng quyết định",
                    "steps": [
                        "Nhập password hợp lệ.",
                        "Nhập confirmPassword khác password.",
                        "Gửi form.",
                    ],
                    "expected": "Hiển thị lỗi xác nhận mật khẩu không khớp.",
                },
            ],
            "bug_findings": [
                {
                    "bug_id": "UC01-BUG-01",
                    "severity": "MEDIUM",
                    "title": "Form đăng ký không return ngay sau nhánh validation lỗi",
                    "evidence": r"frontend\src\Pages\AuthSignUp\index.js:71-126",
                    "impact": "Làm lệch hành vi kỳ vọng của test validation phía client.",
                    "reproduction_steps": [
                        "Mở form Đăng ký.",
                        "Để trống username nhưng nhập các trường còn lại hợp lệ.",
                        "Nhấn Đăng ký và theo dõi hành vi form không dừng dứt khoát theo lỗi đầu tiên.",
                    ],
                },
            ],
        },
        {
            "use_case_id": "UC_02_SI",
            "title": "Đăng nhập tài khoản",
            "actor": "Guest (Khách chưa đăng nhập)",
            "description": "Cho phép người dùng đăng nhập bằng Username hoặc Số điện thoại kết hợp với Mật khẩu.",
            "precondition": "Tài khoản hợp lệ đã tồn tại trong hệ thống và đang hoạt động.",
            "postcondition": "Đăng nhập thành công, hệ thống cấp token/cookie và chuyển trạng thái thành Client.",
            "main_flow": [
                "Từ trang chủ chọn Đăng nhập.",
                "Nhập Username hoặc Số điện thoại cùng Mật khẩu.",
                "Nhấn Đăng nhập.",
                "Hệ thống xác thực và thiết lập phiên nếu thành công.",
            ],
            "exception_flow": [
                "Bỏ trống usernameOrPhone.",
                "Bỏ trống password.",
                "Sai thông tin đăng nhập.",
                "Tài khoản bị khóa hoặc không hoạt động.",
            ],
            "suite_id": "uc-02-si",
            "detailed_tests": [
                {
                    "test_id": "UC02-T01",
                    "title": "Đăng nhập bằng username hợp lệ",
                    "technique": "Phân lớp tương đương (hợp lệ)",
                    "steps": [
                        "Mở trang Đăng nhập.",
                        "Nhập username đúng và password đúng.",
                        "Nhấn Đăng nhập.",
                    ],
                    "expected": "Đăng nhập thành công.",
                },
                {
                    "test_id": "UC02-T02",
                    "title": "Đăng nhập bằng phone hợp lệ",
                    "technique": "Phân lớp tương đương (hợp lệ)",
                    "steps": [
                        "Nhập số điện thoại đúng và password đúng.",
                        "Nhấn Đăng nhập.",
                    ],
                    "expected": "Đăng nhập thành công qua nhánh phone.",
                },
                {
                    "test_id": "UC02-T03",
                    "title": "Thiếu ID hoặc mật khẩu",
                    "technique": "Phân lớp tương đương (không hợp lệ)",
                    "steps": [
                        "Để trống usernameOrPhone hoặc password.",
                        "Nhấn Đăng nhập.",
                    ],
                    "expected": "Hiển thị đúng lỗi required, không tạo session.",
                },
                {
                    "test_id": "UC02-T04",
                    "title": "Sai thông tin hoặc tài khoản bị khóa",
                    "technique": "Bảng quyết định",
                    "steps": [
                        "Nhập password sai hoặc dùng user không hoạt động.",
                        "Nhấn Đăng nhập.",
                    ],
                    "expected": "Thông báo lỗi phù hợp, không đăng nhập.",
                },
            ],
            "bug_findings": [],
        },
        {
            "use_case_id": "UC_03_CP",
            "title": "Thay đổi mật khẩu",
            "actor": "Customer",
            "description": "Cho phép khách hàng đã đăng nhập thay đổi mật khẩu từ trang tài khoản bằng cách nhập mật khẩu hiện tại và mật khẩu mới hợp lệ.",
            "precondition": "Người dùng đã đăng nhập và đang ở trang My Account.",
            "postcondition": "Mật khẩu mới được cập nhật, người dùng phải đăng nhập lại.",
            "main_flow": [
                "Mở trang My Account.",
                "Chuyển sang tab Thay đổi mật khẩu.",
                "Nhập mật khẩu hiện tại, mật khẩu mới và nhập lại mật khẩu mới.",
                "Nhấn xác nhận đổi mật khẩu.",
            ],
            "exception_flow": [
                "Thiếu mật khẩu hiện tại.",
                "Mật khẩu mới không đạt chuẩn.",
                "Nhập lại mật khẩu mới không khớp.",
            ],
            "suite_id": "uc-03-cp",
            "detailed_tests": [
                {
                    "test_id": "UC03-T01",
                    "title": "Hiển thị đúng form đổi mật khẩu",
                    "technique": "UI validation",
                    "steps": [
                        "Đăng nhập rồi mở My Account.",
                        "Click tab Thay đổi mật khẩu.",
                        "Quan sát số lượng và nhãn các ô nhập.",
                    ],
                    "expected": "Form phải có trường current password, new password và confirm new password.",
                },
                {
                    "test_id": "UC03-T02",
                    "title": "Đối chiếu contract dữ liệu đổi mật khẩu",
                    "technique": "Source review / decision table",
                    "steps": [
                        "Đối chiếu đặc tả báo cáo với source MyAccount.",
                        "Kiểm tra payload gửi lên API change-password.",
                    ],
                    "expected": "Frontend phải gửi đủ trường theo đặc tả đổi mật khẩu.",
                },
            ],
            "bug_findings": [
                {
                    "bug_id": "UC03-BUG-01",
                    "severity": "MEDIUM",
                    "title": "Form đổi mật khẩu thiếu ô nhập lại mật khẩu mới",
                    "evidence": r"frontend\src\Pages\MyAccount\MyAccount.jsx:220-241",
                    "impact": "Không đáp ứng yêu cầu nghiệp vụ phải xác nhận lại mật khẩu mới trước khi cập nhật.",
                    "reproduction_steps": [
                        "Đăng nhập rồi vào My Account.",
                        "Mở tab Thay đổi mật khẩu.",
                        "Quan sát chỉ có currentPassword và newPassword, không thấy confirm new password.",
                    ],
                },
            ],
        },
        {
            "use_case_id": "UC_04_AD_TO_CART",
            "title": "Thêm sản phẩm vào giỏ hàng",
            "actor": "Khách vãng lai (Client), Khách hàng (Customer)",
            "description": "Cho phép người dùng chọn biến thể sản phẩm và lưu tạm thời vào giỏ hàng trước khi thanh toán.",
            "precondition": "Người dùng đang ở trang danh sách hoặc chi tiết sản phẩm.",
            "postcondition": "Sản phẩm được thêm vào giỏ, số lượng ở badge giỏ hàng tăng tương ứng.",
            "main_flow": [
                "Người dùng xem danh sách hoặc chi tiết sản phẩm.",
                "Chọn màu sắc, kích cỡ và số lượng cần mua.",
                "Nhấn Thêm vào giỏ hàng.",
                "Hệ thống kiểm tra tồn kho và cập nhật giỏ hàng.",
            ],
            "exception_flow": [
                "Chưa chọn size hoặc màu.",
                "Số lượng vượt quá tồn kho.",
                "Sản phẩm cùng biến thể đã có trong giỏ thì chỉ được cộng dồn số lượng.",
            ],
            "suite_id": "uc-04-add-to-cart",
            "detailed_tests": [
                {
                    "test_id": "UC04-T01",
                    "title": "Thêm item hợp lệ vào giỏ",
                    "technique": "Phân lớp tương đương (hợp lệ)",
                    "steps": [
                        "Mở trang chi tiết sản phẩm.",
                        "Chọn size, màu và quantity hợp lệ.",
                        "Nhấn Thêm vào giỏ hàng.",
                    ],
                    "expected": "Item được thêm thành công và badge giỏ hàng cập nhật.",
                },
                {
                    "test_id": "UC04-T02",
                    "title": "Thiếu thuộc tính bắt buộc",
                    "technique": "Phân lớp tương đương (không hợp lệ)",
                    "steps": [
                        "Không chọn size hoặc màu.",
                        "Nhấn Thêm vào giỏ hàng.",
                    ],
                    "expected": "Hệ thống phải báo vui lòng chọn thuộc tính bắt buộc.",
                },
                {
                    "test_id": "UC04-T03",
                    "title": "Biến thể đã có trong giỏ",
                    "technique": "Bảng quyết định",
                    "steps": [
                        "Thêm một biến thể vào giỏ.",
                        "Lặp lại thao tác với cùng product-size-color.",
                    ],
                    "expected": "Chỉ tăng số lượng, không sinh dòng mới.",
                },
            ],
            "bug_findings": [
                {
                    "bug_id": "UC04-BUG-01",
                    "severity": "HIGH",
                    "title": "Xóa item trong giỏ không phân biệt đầy đủ biến thể",
                    "evidence": r"server\routes\cartRoutes.js:184-200",
                    "impact": "Dễ kéo theo sai lệch khi kiểm thử luồng thêm/xóa lại cùng một sản phẩm khác size màu.",
                    "reproduction_steps": [
                        "Cho cùng một product tồn tại 2 biến thể trong giỏ.",
                        "Xóa một biến thể.",
                        "Theo dõi item còn lại bị ảnh hưởng không đúng.",
                    ],
                },
            ],
        },
        {
            "use_case_id": "UC_05_CHECKOUT",
            "title": "Đặt hàng và Thanh toán (Checkout)",
            "actor": "Khách hàng (Customer)",
            "description": "Người dùng xác nhận thông tin giao hàng, áp dụng voucher và chọn phương thức thanh toán để hoàn tất đơn hàng.",
            "precondition": "Giỏ hàng phải có ít nhất một sản phẩm và người dùng phải đăng nhập.",
            "postcondition": "Đơn hàng được tạo mới với trạng thái chờ xác nhận, tồn kho giảm tương ứng và giỏ hàng được làm trống.",
            "main_flow": [
                "Từ giỏ hàng bấm Thanh toán.",
                "Hệ thống kiểm tra trạng thái đăng nhập.",
                "Hiển thị form giao hàng, danh sách sản phẩm, tổng tiền, voucher và paymentMethod.",
                "Người dùng nhập địa chỉ, chọn COD hoặc Chuyển khoản rồi xác nhận đặt hàng.",
            ],
            "exception_flow": [
                "Thiếu thông tin giao hàng bắt buộc.",
                "Voucher không hợp lệ hoặc không đủ điều kiện tổng tiền.",
                "Lỗi xử lý paymentMethod hoặc lỗi thanh toán trực tuyến.",
            ],
            "suite_id": "uc-05-checkout",
            "detailed_tests": [
                {
                    "test_id": "UC05-T01",
                    "title": "Checkout với COD hợp lệ",
                    "technique": "Phân lớp tương đương (hợp lệ)",
                    "steps": [
                        "Mở Checkout với giỏ hàng đã seed.",
                        "Nhập đầy đủ thông tin giao hàng.",
                        "Chọn COD và đặt hàng.",
                    ],
                    "expected": "Đơn hàng được tạo thành công nếu frontend/backend thống nhất paymentMethod.",
                },
                {
                    "test_id": "UC05-T02",
                    "title": "Thiếu thông tin giao hàng",
                    "technique": "Phân lớp tương đương (không hợp lệ)",
                    "steps": [
                        "Bỏ trống Họ tên hoặc SĐT hoặc địa chỉ.",
                        "Nhấn đặt hàng.",
                    ],
                    "expected": "Hệ thống highlight lỗi tại trường thiếu và giữ lại dữ liệu đã nhập.",
                },
                {
                    "test_id": "UC05-T03",
                    "title": "Áp voucher ở ngưỡng điều kiện",
                    "technique": "Giá trị biên",
                    "steps": [
                        "Chuẩn bị tổng tiền bằng minOrderValue của voucher.",
                        "Áp dụng voucher rồi lặp lại với tổng tiền thấp hơn đúng 1 đơn vị.",
                    ],
                    "expected": "Voucher chỉ được áp dụng ở ngưỡng hợp lệ.",
                },
            ],
            "bug_findings": [
                {
                    "bug_id": "UC05-BUG-01",
                    "severity": "HIGH",
                    "title": "paymentMethod giữa frontend và backend không cùng miền giá trị",
                    "evidence": r"frontend\src\Pages\Checkout\index.js:431-436 | server\middlewares\validate.js:67",
                    "impact": "Luồng checkout hợp lệ trên UI có thể fail ở bước validate server.",
                    "reproduction_steps": [
                        "Mở Checkout và chọn thanh toán khi nhận hàng.",
                        "Gửi form đặt hàng.",
                        "Đối chiếu payload frontend gửi cash/payment trong khi backend yêu cầu COD/Online.",
                    ],
                },
            ],
        },
    ],
    "major_bug_findings": [
        {
            "bug_id": "BUG_FP_01",
            "module": "Module 1",
            "severity": "HIGH",
            "title": "Điểm vào Quên mật khẩu bị gãy trên frontend chính",
            "evidence": r"frontend\src\Pages\AuthSignIn\index.js:222-223",
            "summary": "Link Quên mật khẩu không có route thực để đi vào flow reset password.",
        },
        {
            "bug_id": "BUG_CO_01",
            "module": "Module 2",
            "severity": "HIGH",
            "title": "Lệch chuẩn paymentMethod giữa frontend và backend",
            "evidence": r"frontend\src\Pages\Checkout\index.js:431-436 | server\middlewares\validate.js:67",
            "summary": "Frontend gửi cash/payment nhưng backend chỉ chấp nhận COD/Online.",
        },
        {
            "bug_id": "BUG_CA_01",
            "module": "Module 2",
            "severity": "HIGH",
            "title": "removeCart bỏ qua size và color",
            "evidence": r"server\routes\cartRoutes.js:184-200",
            "summary": "Có nguy cơ xóa nhầm item khi cùng productId có nhiều biến thể khác nhau.",
        },
        {
            "bug_id": "BUG_CP_01",
            "module": "Module 1",
            "severity": "MEDIUM",
            "title": "Đổi mật khẩu thiếu ô confirm mật khẩu mới",
            "evidence": r"frontend\src\Pages\MyAccount\MyAccount.jsx:220-241",
            "summary": "Không khớp với yêu cầu nghiệp vụ phải nhập lại mật khẩu mới.",
        },
        {
            "bug_id": "BUG_SU_01",
            "module": "Module 1",
            "severity": "MEDIUM",
            "title": "Validation đăng ký không return sớm",
            "evidence": r"frontend\src\Pages\AuthSignUp\index.js:71-126",
            "summary": "Làm sai hành vi mong đợi của form validation phía client.",
        },
    ],
    "white_box_sections": [
        {
            "id": "WBT_SU",
            "title": "Kiểm thử hộp trắng chức năng Đăng ký",
            "summary": "Phân tích route /signup: required fields, validate phone, validate password, nhánh username trùng, phone trùng và luồng save user.",
            "note": "Có thể vẽ CFG và tính cyclomatic complexity dựa trên userRoutes.js.",
        },
        {
            "id": "WBT_SI",
            "title": "Kiểm thử hộp trắng chức năng Đăng nhập",
            "summary": "Phân tích route /signin: bỏ trống input, phân nhánh username/phone, user không tồn tại, sai password, user bị khóa và cấp token.",
            "note": "Có thể trình bày basis paths cho phần login bằng userRoutes.js.",
        },
        {
            "id": "WBT_CO",
            "title": "Kiểm thử hộp trắng logic Checkout và Voucher",
            "summary": "Đối chiếu nhánh validate paymentMethod, shape payload, điều kiện minOrderValue và xử lý cộng trừ tổng tiền đơn hàng.",
            "note": "Đây là phần white-box có giá trị cao vì trực tiếp ảnh hưởng doanh thu và tính đúng đắn nghiệp vụ.",
        },
    ],
    "task_assignments": [
        {
            "owner": "NGÔ QUANG LỢI",
            "responsibility": "Thiết kế dashboard TestOps, tích hợp report HTML/XML/Excel/Word, source audit và tổng hợp số liệu đồ án.",
        },
        {
            "owner": "NGUYỄN CÔNG QUỐC",
            "responsibility": "Phụ trách Module 1: đăng ký, đăng nhập, đổi mật khẩu, validation form và bug report phía tài khoản.",
        },
        {
            "owner": "TRỊNH NHẬT TIẾN",
            "responsibility": "Phụ trách Module 2: giỏ hàng, voucher, checkout, boundary/business flow và bug report phía giao dịch.",
        },
    ],
}
