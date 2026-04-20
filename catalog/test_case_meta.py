# Test case metadata for Excel report generation.
# Key format: "classname::test_name" matching pytest XML output.
# classname uses dots (e.g. "tests.test_login"), matching pytest's XML classname attribute.

TEST_CASE_META = {

    # =========================================================================
    # Module DN - Đăng Nhập (Login)
    # =========================================================================
    "tests.test_login::test_login_success": {
        "id": "DN_01",
        "description": "Đăng nhập thành công với tài khoản hợp lệ",
        "technique": "Equivalence Partitioning (Valid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Tài khoản hợp lệ tồn tại trong hệ thống (tạo qua API)",
        ],
        "test_data": [
            "Username: (sinh ngẫu nhiên qua API)",
            "Password: Abcd123@",
        ],
        "steps": [
            {"detail": "Mở trình duyệt Chrome hoặc Edge", "expected": "Trình duyệt được mở thành công"},
            {"detail": "Truy cập https://guangli-shop.netlify.app/", "expected": "Trang chủ hiển thị"},
            {"detail": "Nhấn vào nút Đăng Nhập trên thanh điều hướng", "expected": "Form Đăng Nhập hiển thị"},
            {"detail": "Nhập Username và Password hợp lệ", "expected": "Dữ liệu được nhập thành công"},
            {"detail": "Nhấn nút ĐĂNG NHẬP", "expected": "Thông báo 'Đăng nhập thành công.' hiển thị, token lưu vào sessionStorage"},
        ],
    },

    "tests.test_login::test_login_invalid": {
        "id": "DN_02",
        "description": "Đăng nhập thất bại với tài khoản không tồn tại",
        "technique": "Equivalence Partitioning (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [
            "Username: wrong_user",
            "Password: wrong_password",
        ],
        "steps": [
            {"detail": "Mở trình duyệt, truy cập trang đăng nhập", "expected": "Trang đăng nhập hiển thị"},
            {"detail": "Nhập Username: wrong_user", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhập Password: wrong_password", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhấn nút ĐĂNG NHẬP", "expected": "Thông báo lỗi đăng nhập hiển thị, không có token"},
        ],
    },

    "tests.test_login::test_login_success_persists_after_refresh": {
        "id": "DN_03",
        "description": "Session đăng nhập được giữ sau khi refresh trình duyệt",
        "technique": "Functional Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Tài khoản hợp lệ tồn tại trong hệ thống (tạo qua API)",
        ],
        "test_data": [
            "Username: (sinh ngẫu nhiên qua API)",
            "Password: Abcd123@",
        ],
        "steps": [
            {"detail": "Mở trình duyệt, truy cập trang đăng nhập", "expected": "Form đăng nhập hiển thị"},
            {"detail": "Đăng nhập với tài khoản hợp lệ", "expected": "Đăng nhập thành công"},
            {"detail": "Nhấn F5 hoặc reload trang", "expected": "Trang reload"},
            {"detail": "Kiểm tra sessionStorage", "expected": "Token và user vẫn còn trong sessionStorage"},
        ],
    },

    "tests.test_login::test_login_invalid_with_existing_username": {
        "id": "DN_04",
        "description": "Đăng nhập thất bại khi dùng username đúng nhưng sai mật khẩu",
        "technique": "Equivalence Partitioning (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Tài khoản hợp lệ tồn tại trong hệ thống",
        ],
        "test_data": [
            "Username: (tài khoản tồn tại - sinh qua API)",
            "Password: wrong_password (sai mật khẩu)",
        ],
        "steps": [
            {"detail": "Mở trình duyệt, truy cập trang đăng nhập", "expected": "Form đăng nhập hiển thị"},
            {"detail": "Nhập Username đúng (tồn tại trong hệ thống)", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhập Password sai: wrong_password", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhấn nút ĐĂNG NHẬP", "expected": "Hiển thị thông báo lỗi, không có token"},
        ],
    },

    "tests.test_login::test_login_invalid_with_existing_phone": {
        "id": "DN_05",
        "description": "Đăng nhập thất bại khi dùng số điện thoại đúng nhưng sai mật khẩu",
        "technique": "Equivalence Partitioning (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Tài khoản hợp lệ tồn tại trong hệ thống (có SĐT)",
        ],
        "test_data": [
            "Phone: (SĐT của tài khoản test - sinh qua API)",
            "Password: wrong_password (sai mật khẩu)",
        ],
        "steps": [
            {"detail": "Mở trình duyệt, truy cập trang đăng nhập", "expected": "Form đăng nhập hiển thị"},
            {"detail": "Nhập Số điện thoại đúng (tồn tại trong hệ thống)", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhập Password sai: wrong_password", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhấn nút ĐĂNG NHẬP", "expected": "Hiển thị thông báo lỗi, không có token"},
        ],
    },

    # =========================================================================
    # Module GDTK - Giao Diện Tài Khoản (Account UI)
    # =========================================================================
    "tests.test_account_module::test_account_login_page_ui_alignment_and_title": {
        "id": "GDTK_01",
        "description": "Kiểm tra bố cục và title trang đăng nhập",
        "technique": "UI / Layout Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Mở trình duyệt, truy cập trang đăng nhập", "expected": "Form đăng nhập hiển thị"},
            {"detail": "Kiểm tra title trang không trống", "expected": "Title hiển thị giá trị hợp lệ"},
            {"detail": "Kiểm tra vị trí căn chỉnh ô Username và Password", "expected": "Hai ô nằm cùng cột (x ≤ 5px sai lệch)"},
            {"detail": "Kiểm tra con trỏ chuột trên ô Username", "expected": "Cursor là 'auto' hoặc 'text'"},
            {"detail": "Kiểm tra link Quên Mật Khẩu trỏ đúng", "expected": "href kết thúc bằng /signIn"},
            {"detail": "Kiểm tra không có thanh cuộn ngang", "expected": "scrollWidth ≤ clientWidth + 1"},
        ],
    },

    "tests.test_account_module::test_account_login_invalid_keeps_values_and_shows_error": {
        "id": "GDTK_02",
        "description": "Đăng nhập sai: form giữ nguyên giá trị đã nhập và hiển thị lỗi",
        "technique": "Equivalence Partitioning (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [
            "Username: wrong_user",
            "Password: wrong_pass",
        ],
        "steps": [
            {"detail": "Mở trình duyệt, truy cập trang đăng nhập", "expected": "Form đăng nhập hiển thị"},
            {"detail": "Nhập Username: wrong_user và Password: wrong_pass", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhấn nút ĐĂNG NHẬP", "expected": "Thông báo lỗi chứa 'không đúng' hiển thị"},
            {"detail": "Kiểm tra ô Username và Password vẫn giữ giá trị đã nhập", "expected": "Giá trị nhập vẫn còn trong ô"},
        ],
    },

    "tests.test_account_module::test_account_login_keyboard_navigation_and_enter_submit": {
        "id": "GDTK_03",
        "description": "Điều hướng bàn phím: Tab và Enter trên form đăng nhập",
        "technique": "Usability Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [
            "Username: wrong_user",
            "Password: wrong_pass",
        ],
        "steps": [
            {"detail": "Mở trang đăng nhập, click vào ô Username", "expected": "Focus vào ô Username"},
            {"detail": "Nhập username rồi nhấn Tab", "expected": "Focus chuyển sang ô Password"},
            {"detail": "Nhập password rồi nhấn Enter", "expected": "Form được submit"},
            {"detail": "Kiểm tra thông báo lỗi", "expected": "Thông báo 'không đúng' hiển thị"},
        ],
    },

    "tests.test_account_module::test_account_signup_form_fields_and_layout": {
        "id": "GDTK_04",
        "description": "Kiểm tra form đăng ký hiển thị đủ trường và căn chỉnh đúng",
        "technique": "UI / Layout Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Mở trang đăng nhập, nhấn link Đăng Ký", "expected": "Form Đăng Ký Tài Khoản hiển thị"},
            {"detail": "Kiểm tra tiêu đề 'Đăng Ký Tài Khoản' hiển thị", "expected": "Tiêu đề hiển thị"},
            {"detail": "Kiểm tra đủ 5 trường: Username, SĐT, Họ tên, Mật khẩu, Xác nhận", "expected": "Tất cả 5 trường hiển thị"},
            {"detail": "Kiểm tra căn chỉnh ngang: Username và SĐT cùng hàng", "expected": "y sai lệch ≤ 5px"},
            {"detail": "Kiểm tra không có thanh cuộn ngang", "expected": "scrollWidth ≤ clientWidth + 1"},
        ],
    },

    "tests.test_account_module::test_account_forgot_password_link_is_clickable": {
        "id": "GDTK_05",
        "description": "Link Quên Mật Khẩu có thể click và điều hướng đúng",
        "technique": "Functional Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Mở trang đăng nhập", "expected": "Form đăng nhập hiển thị"},
            {"detail": "Click vào link Quên Mật Khẩu", "expected": "Trang điều hướng đến /signIn"},
            {"detail": "Kiểm tra nội dung trang sau khi click", "expected": "Trang có chứa 'Đăng Nhập'"},
        ],
    },

    "tests.test_account_module::test_account_profile_page_form_and_change_password_tab": {
        "id": "GDTK_06",
        "description": "Trang thông tin tài khoản và tab Thay Đổi Mật Khẩu hoạt động đúng",
        "technique": "Functional Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Đã đăng nhập thành công (qua API)",
        ],
        "test_data": [
            "Tài khoản test (sinh qua API)",
        ],
        "steps": [
            {"detail": "Mở trang thông tin tài khoản (đã đăng nhập)", "expected": "Trang thông tin hiển thị"},
            {"detail": "Kiểm tra các nhãn: Tên tài khoản, Họ và tên, SĐT, Email", "expected": "Đủ 4 nhãn hiển thị"},
            {"detail": "Kiểm tra căn chỉnh 2 cột form", "expected": "Sai lệch x ≤ 5px, y ≤ 5px"},
            {"detail": "Click tab THAY ĐỔI MẬT KHẨU", "expected": "Tab active và 2 ô mật khẩu hiển thị"},
        ],
    },

    "tests.test_account_module::test_account_profile_avatar_and_order_page_access": {
        "id": "GDTK_07",
        "description": "Avatar tài khoản không bị hỏng và trang đơn hàng truy cập được",
        "technique": "Functional Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Đã đăng nhập thành công (qua API)",
        ],
        "test_data": [
            "Tài khoản test (sinh qua API)",
        ],
        "steps": [
            {"detail": "Mở trang thông tin tài khoản", "expected": "Trang hiển thị"},
            {"detail": "Kiểm tra ảnh avatar không bị lỗi 4xx/5xx", "expected": "HTTP response OK cho ảnh avatar"},
            {"detail": "Truy cập trang Danh Sách Đơn Hàng", "expected": "Trang đơn hàng hiển thị với tiêu đề phù hợp"},
        ],
    },

    # =========================================================================
    # Module TK - Tìm Kiếm (Search)
    # =========================================================================
    "tests.test_search::test_search_with_matching_keyword[Adidas]": {
        "id": "TK_01",
        "description": "Tìm kiếm từ khóa 'Adidas' trả về kết quả sản phẩm",
        "technique": "Equivalence Partitioning (Valid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Có ít nhất 1 sản phẩm Adidas trong hệ thống",
        ],
        "test_data": ["Từ khóa: Adidas"],
        "steps": [
            {"detail": "Mở trang chủ", "expected": "Trang chủ hiển thị với ô tìm kiếm"},
            {"detail": "Nhập 'Adidas' vào ô tìm kiếm và submit", "expected": "Chuyển sang trang kết quả tìm kiếm"},
            {"detail": "Kiểm tra số lượng sản phẩm tìm được", "expected": "Có ít nhất 1 sản phẩm hiển thị"},
        ],
    },

    "tests.test_search::test_search_with_matching_keyword[Nike]": {
        "id": "TK_02",
        "description": "Tìm kiếm từ khóa 'Nike' trả về kết quả sản phẩm",
        "technique": "Equivalence Partitioning (Valid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Có ít nhất 1 sản phẩm Nike trong hệ thống",
        ],
        "test_data": ["Từ khóa: Nike"],
        "steps": [
            {"detail": "Mở trang chủ", "expected": "Trang chủ hiển thị với ô tìm kiếm"},
            {"detail": "Nhập 'Nike' vào ô tìm kiếm và submit", "expected": "Chuyển sang trang kết quả tìm kiếm"},
            {"detail": "Kiểm tra số lượng sản phẩm tìm được", "expected": "Có ít nhất 1 sản phẩm hiển thị"},
        ],
    },

    "tests.test_search::test_search_with_matching_keyword[Gi\u00e0y T\u00e2y]": {
        "id": "TK_03",
        "description": "Tìm kiếm từ khóa 'Giày Tây' trả về kết quả sản phẩm",
        "technique": "Equivalence Partitioning (Valid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Có ít nhất 1 sản phẩm Giày Tây trong hệ thống",
        ],
        "test_data": ["Từ khóa: Giày Tây"],
        "steps": [
            {"detail": "Mở trang chủ", "expected": "Trang chủ hiển thị với ô tìm kiếm"},
            {"detail": "Nhập 'Giày Tây' vào ô tìm kiếm và submit", "expected": "Chuyển sang trang kết quả tìm kiếm"},
            {"detail": "Kiểm tra số lượng sản phẩm tìm được", "expected": "Có ít nhất 1 sản phẩm hiển thị"},
        ],
    },

    "tests.test_search::test_search_with_no_result_keyword[zzzzzzzz_not_found_12345]": {
        "id": "TK_04",
        "description": "Tìm kiếm từ khóa không tồn tại → không có kết quả",
        "technique": "Equivalence Partitioning (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": ["Từ khóa: zzzzzzzz_not_found_12345"],
        "steps": [
            {"detail": "Mở trang chủ", "expected": "Trang chủ hiển thị với ô tìm kiếm"},
            {"detail": "Nhập từ khóa ngẫu nhiên không tồn tại và submit", "expected": "Chuyển sang trang kết quả"},
            {"detail": "Kiểm tra không có sản phẩm nào hiển thị", "expected": "Số lượng sản phẩm = 0"},
        ],
    },

    "tests.test_search::test_search_with_no_result_keyword[selenium_keyword_not_found_2026]": {
        "id": "TK_05",
        "description": "Tìm kiếm từ khóa test automation không tồn tại → không có kết quả",
        "technique": "Equivalence Partitioning (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": ["Từ khóa: selenium_keyword_not_found_2026"],
        "steps": [
            {"detail": "Mở trang chủ", "expected": "Trang chủ hiển thị với ô tìm kiếm"},
            {"detail": "Nhập từ khóa không tồn tại và submit", "expected": "Chuyển sang trang kết quả"},
            {"detail": "Kiểm tra không có sản phẩm nào hiển thị", "expected": "Số lượng sản phẩm = 0"},
        ],
    },

    # =========================================================================
    # Module GH - Giỏ Hàng (Cart)
    # =========================================================================
    "tests.test_cart_checkout_module::test_cart_page_grid_headers_totals_and_rows": {
        "id": "GH_01",
        "description": "Bảng giỏ hàng hiển thị đủ tiêu đề cột, sản phẩm và giá tiền",
        "technique": "UI / Layout Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Đã đăng nhập và có sản phẩm trong giỏ hàng (seed qua API)",
        ],
        "test_data": [
            "Sản phẩm được seed vào giỏ hàng qua store API",
        ],
        "steps": [
            {"detail": "Mở trang giỏ hàng (đã có sản phẩm)", "expected": "Trang giỏ hàng hiển thị"},
            {"detail": "Kiểm tra tiêu đề cột: Sản phẩm, Size, Màu, Đơn giá, Số lượng, Tổng phụ", "expected": "Đủ 6 tiêu đề hiển thị"},
            {"detail": "Kiểm tra ít nhất 1 dòng sản phẩm hiển thị", "expected": "rows ≥ 1"},
            {"detail": "Kiểm tra tên sản phẩm có trong nội dung trang", "expected": "Tên sản phẩm hiển thị"},
            {"detail": "Kiểm tra ít nhất 3 giá tiền định dạng VNĐ", "expected": "Có ≥ 3 text chứa ký hiệu tiền tệ"},
            {"detail": "Kiểm tra không có thanh cuộn ngang", "expected": "Layout không bị vỡ"},
        ],
    },

    "tests.test_cart_checkout_module::test_cart_page_voucher_input_and_button_alignment": {
        "id": "GH_02",
        "description": "Ô nhập mã voucher và nút Áp Dụng căn chỉnh đúng, nhập được giá trị",
        "technique": "UI / Layout Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Đã đăng nhập và có sản phẩm trong giỏ hàng",
        ],
        "test_data": [
            "Mã voucher test: SAI_MA_TEST",
        ],
        "steps": [
            {"detail": "Mở trang giỏ hàng", "expected": "Trang giỏ hàng hiển thị"},
            {"detail": "Kiểm tra vị trí ô voucher và nút Áp Dụng", "expected": "Nút nằm dưới ô input, x sai lệch ≤ 250px"},
            {"detail": "Nhập mã SAI_MA_TEST vào ô voucher và click Áp Dụng", "expected": "Ô voucher giữ giá trị 'SAI_MA_TEST'"},
        ],
    },

    "tests.test_cart_checkout_module::test_cart_page_product_images_are_not_broken": {
        "id": "GH_03",
        "description": "Ảnh sản phẩm trong giỏ hàng không bị hỏng (HTTP OK)",
        "technique": "Functional Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Đã đăng nhập và có sản phẩm trong giỏ hàng",
        ],
        "test_data": [
            "Ảnh sản phẩm được seed qua API",
        ],
        "steps": [
            {"detail": "Mở trang giỏ hàng", "expected": "Trang giỏ hàng hiển thị"},
            {"detail": "Lấy danh sách URL ảnh sản phẩm hiển thị", "expected": "Danh sách URL ảnh không rỗng"},
            {"detail": "Gửi HTTP GET tới từng URL ảnh (tối đa 3 ảnh đầu)", "expected": "Tất cả ảnh trả về HTTP 200 OK"},
        ],
    },

    # =========================================================================
    # Module TT - Thanh Toán (Checkout)
    # =========================================================================
    "tests.test_cart_checkout_module::test_checkout_page_layout_multiline_and_payment_controls": {
        "id": "TT_01",
        "description": "Trang Checkout: bố cục form, textarea và phương thức thanh toán đúng",
        "technique": "UI / Layout Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Đã đăng nhập và có dữ liệu checkout trong localStorage",
        ],
        "test_data": [
            "Sản phẩm và checkout data seed qua API",
        ],
        "steps": [
            {"detail": "Mở trang Checkout (đã có dữ liệu giỏ hàng)", "expected": "Form checkout hiển thị"},
            {"detail": "Kiểm tra nhãn: Họ và tên, Số điện thoại, Tỉnh/thành phố, Phương thức thanh toán", "expected": "Đủ 4 nhãn hiển thị"},
            {"detail": "Kiểm tra căn chỉnh trường Họ tên và SĐT cùng hàng", "expected": "y sai lệch ≤ 5px"},
            {"detail": "Kiểm tra textarea ghi chú có ít nhất 4 hàng", "expected": "rows ≥ 4"},
            {"detail": "Kiểm tra có 2 phương thức thanh toán: cash và payment", "expected": "Cả 2 option hiển thị"},
            {"detail": "Kiểm tra option 'Thanh toán online' bị vô hiệu hóa", "expected": "payment.disabled = true"},
            {"detail": "Kiểm tra không có thanh cuộn ngang", "expected": "Layout không bị vỡ"},
        ],
    },

    "tests.test_cart_checkout_module::test_checkout_form_values_persist_after_failed_submit": {
        "id": "TT_02",
        "description": "Giá trị form Checkout được giữ nguyên sau khi submit thất bại",
        "technique": "Functional Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Đã đăng nhập và có dữ liệu checkout",
        ],
        "test_data": [
            "Họ và tên: Nguyen Van A",
            "SĐT: 0912345678",
            "Địa chỉ: 123 duong test",
            "Ghi chú: ghi chu test",
        ],
        "steps": [
            {"detail": "Mở trang Checkout", "expected": "Form checkout hiển thị"},
            {"detail": "Nhập thông tin giao hàng (thiếu tỉnh/thành)", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhấn Đặt Hàng", "expected": "Form không chuyển trang (vẫn ở /checkout)"},
            {"detail": "Kiểm tra các trường vẫn giữ giá trị đã nhập", "expected": "fullName, phone, detail, notes còn nguyên"},
        ],
    },

    "tests.test_cart_checkout_module::test_checkout_cash_option_and_summary_headers": {
        "id": "TT_03",
        "description": "Chọn thanh toán tiền mặt và bảng tóm tắt đơn hàng hiển thị đúng",
        "technique": "Functional Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Đã đăng nhập và có dữ liệu checkout",
        ],
        "test_data": [
            "Phương thức thanh toán: Tiền mặt (cash)",
        ],
        "steps": [
            {"detail": "Mở trang Checkout", "expected": "Form checkout hiển thị"},
            {"detail": "Chọn radio button Tiền Mặt", "expected": "Radio 'cash' được chọn"},
            {"detail": "Kiểm tra radio 'thanh toán online' không được chọn", "expected": "payment.selected = false"},
            {"detail": "Kiểm tra bảng tóm tắt có tiêu đề: Sản phẩm, Giá", "expected": "Đủ 2 tiêu đề hiển thị"},
        ],
    },

    # =========================================================================
    # Module UI - Giao Diện Chung
    # =========================================================================
    "tests.test_ui::test_homepage_main_ui": {
        "id": "UI_01",
        "description": "Giao diện trang chủ hiển thị đủ thành phần chính",
        "technique": "UI / Layout Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Mở trang chủ Guangli Shop", "expected": "Trang chủ hiển thị"},
            {"detail": "Kiểm tra ô tìm kiếm có placeholder 'Tìm kiếm'", "expected": "Ô tìm kiếm hiển thị đúng"},
            {"detail": "Kiểm tra section 'SẢN PHẨM NỔI BẬT' hiển thị", "expected": "Section hiển thị"},
            {"detail": "Kiểm tra section 'SẢN PHẨM MỚI' hiển thị", "expected": "Section hiển thị"},
            {"detail": "Kiểm tra nút Đăng Nhập hiển thị trên nav", "expected": "Nút Đăng Nhập hiển thị"},
            {"detail": "Kiểm tra có ít nhất 1 sản phẩm trên trang chủ", "expected": "product_links_count > 0"},
        ],
    },

    "tests.test_ui::test_login_and_signup_ui": {
        "id": "UI_02",
        "description": "Giao diện form Đăng Nhập và Đăng Ký hiển thị đủ trường",
        "technique": "UI / Layout Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Mở trang chủ và click Đăng Nhập", "expected": "Form đăng nhập hiển thị"},
            {"detail": "Kiểm tra tiêu đề, ô username/phone, ô mật khẩu, nút ĐĂNG NHẬP", "expected": "Đủ các phần tử hiển thị"},
            {"detail": "Click chuyển sang form Đăng Ký", "expected": "Form Đăng Ký Tài Khoản hiển thị"},
            {"detail": "Kiểm tra tiêu đề 'Đăng Ký Tài Khoản' và 5 trường nhập", "expected": "Đủ tiêu đề và 5 trường"},
        ],
    },

    # =========================================================================
    # Module TNT - Đăng Ký (Register) - tests/test_register_module.py
    # =========================================================================
    "tests.test_register_module::test_register_empty_form": {
        "id": "TNT_01",
        "description": "Đăng ký khi bỏ trống toàn bộ form không được phép đăng ký thành công",
        "technique": "Equivalence Partitioning (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
            "Form Đăng Ký Tài Khoản đang hiển thị",
        ],
        "test_data": [
            "(Tất cả các trường để trống)",
        ],
        "steps": [
            {"detail": "Mở trình duyệt, truy cập form đăng ký", "expected": "Form Đăng Ký Tài Khoản hiển thị"},
            {"detail": "Không nhập bất kỳ thông tin nào", "expected": "Tất cả các trường vẫn trống"},
            {"detail": "Nhấn nút ĐĂNG KÝ", "expected": "Hiển thị thông báo lỗi hoặc URL vẫn ở trang đăng ký"},
        ],
    },

    "tests.test_register_module::test_register_password_mismatch": {
        "id": "TNT_02",
        "description": "Đăng ký khi mật khẩu và xác nhận mật khẩu không khớp",
        "technique": "Equivalence Partitioning (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [
            "Password: Abc@1234",
            "Confirm Password: Abc@5678 (không khớp)",
        ],
        "steps": [
            {"detail": "Mở form đăng ký", "expected": "Form Đăng Ký hiển thị"},
            {"detail": "Điền đầy đủ các trường hợp lệ, riêng Xác nhận mật khẩu nhập khác: Abc@5678", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhấn nút ĐĂNG KÝ", "expected": "Hiển thị lỗi 'Mật khẩu không khớp' hoặc đăng ký không thành công"},
        ],
    },

    "tests.test_register_module::test_register_short_password": {
        "id": "TNT_03",
        "description": "Đăng ký với mật khẩu 7 ký tự (dưới tối thiểu 8 ký tự) - Boundary Value",
        "technique": "Boundary Value Analysis (Invalid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [
            "Password: Abc@123 (7 ký tự)",
            "Confirm: Abc@123",
        ],
        "steps": [
            {"detail": "Mở form đăng ký", "expected": "Form Đăng Ký hiển thị"},
            {"detail": "Điền các trường hợp lệ, nhập mật khẩu 7 ký tự: Abc@123", "expected": "Dữ liệu được nhập"},
            {"detail": "Nhấn nút ĐĂNG KÝ", "expected": "Hiển thị lỗi mật khẩu quá ngắn hoặc đăng ký thất bại"},
        ],
    },

    "tests.test_register_module::test_register_navigate_to_login": {
        "id": "TNT_04",
        "description": "Từ trang đăng ký, click link 'Đăng Nhập' điều hướng đúng",
        "technique": "Navigation Testing",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Mở form đăng ký", "expected": "Form Đăng Ký hiển thị"},
            {"detail": "Tìm và click link 'Đăng Nhập' (phần 'Bạn Đã Có Tài Khoản Rồi?')", "expected": "Điều hướng sang form Đăng Nhập"},
            {"detail": "Kiểm tra ô username/phone và password hiển thị", "expected": "Form Đăng Nhập hiển thị đầy đủ"},
        ],
    },

    "tests.test_register_module::test_register_valid_success": {
        "id": "TNT_05",
        "description": "Đăng ký tài khoản mới thành công với đầy đủ thông tin hợp lệ qua UI",
        "technique": "Equivalence Partitioning (Valid)",
        "prerequisites": [
            "Truy cập được trang web https://guangli-shop.netlify.app/",
        ],
        "test_data": [
            "Username: (sinh ngẫu nhiên theo timestamp)",
            "SĐT: (10 chữ số ngẫu nhiên)",
            "Họ tên: Selenium Test User",
            "Password: Abcd123@",
        ],
        "steps": [
            {"detail": "Mở form đăng ký", "expected": "Form Đăng Ký Tài Khoản hiển thị"},
            {"detail": "Nhập đầy đủ thông tin hợp lệ vào tất cả các trường", "expected": "Dữ liệu được nhập thành công"},
            {"detail": "Nhấn nút ĐĂNG KÝ", "expected": "Đăng ký thành công, chuyển trang hoặc hiển thị thông báo thành công"},
        ],
    },

    "tests.test_runtime_audit::test_homepage_has_no_actionable_browser_console_errors": {
        "id": "AUD_01",
        "description": "Homepage should not emit SEVERE browser console errors during load",
        "technique": "Runtime Audit / Browser Console",
        "prerequisites": [
            "Website is reachable",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Open homepage", "expected": "Homepage loads successfully"},
            {"detail": "Read browser console logs", "expected": "No SEVERE entries are present"},
        ],
    },

    "tests.test_runtime_audit::test_login_page_has_no_actionable_browser_console_errors": {
        "id": "AUD_02",
        "description": "Login page should not emit SEVERE browser console errors",
        "technique": "Runtime Audit / Browser Console",
        "prerequisites": [
            "Website is reachable",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Open login page through UI navigation", "expected": "Login form is visible"},
            {"detail": "Read browser console logs", "expected": "No SEVERE entries are present"},
        ],
    },

    "tests.test_runtime_audit::test_homepage_visible_images_are_not_broken": {
        "id": "AUD_03",
        "description": "Visible homepage images should load without broken asset state",
        "technique": "UI / Asset Audit",
        "prerequisites": [
            "Website is reachable",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Open homepage", "expected": "Homepage loads successfully"},
            {"detail": "Inspect visible images", "expected": "No visible image has naturalWidth equal to zero"},
        ],
    },

    "tests.test_runtime_audit::test_homepage_same_origin_links_are_directly_resolvable": {
        "id": "AUD_04",
        "description": "Homepage same-origin links should be directly reachable without 404",
        "technique": "Deployment / Deep-Link Audit",
        "prerequisites": [
            "Website is reachable",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Open homepage", "expected": "Homepage loads successfully"},
            {"detail": "Request each same-origin href", "expected": "Each route responds with status code below 400"},
        ],
    },

    "tests.test_runtime_audit::test_checkout_page_has_no_actionable_browser_console_errors": {
        "id": "AUD_05",
        "description": "Checkout page with seeded session should not emit SEVERE browser console errors",
        "technique": "Runtime Audit / Business Flow",
        "prerequisites": [
            "Authenticated test account and seeded checkout data are available",
        ],
        "test_data": [
            "Authenticated user via API",
            "Checkout data seeded in localStorage",
        ],
        "steps": [
            {"detail": "Load authenticated checkout state", "expected": "User session is active"},
            {"detail": "Open SPA checkout route", "expected": "Checkout page is visible"},
            {"detail": "Read browser console logs", "expected": "No SEVERE entries are present"},
        ],
    },

    "tests.test_source_audit::test_signin_forgot_password_link_has_destination": {
        "id": "SRC_01",
        "description": "Liên kết Quên mật khẩu trên trang đăng nhập phải có đích điều hướng hợp lệ",
        "technique": "Source Audit / Navigation Contract",
        "prerequisites": [
            "Có source chuẩn của dự án WEB-MERN_t10-2024",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Mở file frontend/src/Pages/AuthSignIn/index.js", "expected": "Tìm thấy markup của trang đăng nhập"},
            {"detail": "Kiểm tra thẻ Link của Quên mật khẩu", "expected": "Thẻ Link phải khai báo thuộc tính to= cho route đích"},
        ],
    },

    "tests.test_source_audit::test_storefront_app_registers_forgot_password_route": {
        "id": "SRC_02",
        "description": "Router storefront phải khai báo route khôi phục mật khẩu",
        "technique": "Source Audit / Route Coverage",
        "prerequisites": [
            "Có source chuẩn của dự án WEB-MERN_t10-2024",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Mở file frontend/src/App.js", "expected": "Tìm thấy danh sách route của storefront"},
            {"detail": "Kiểm tra route forgot password", "expected": "Phải có ít nhất một route chứa forgot/reset password"},
        ],
    },

    "tests.test_source_audit::test_storefront_has_forgot_password_page_component": {
        "id": "SRC_03",
        "description": "Frontend storefront phải có component riêng cho chức năng quên mật khẩu",
        "technique": "Source Audit / Component Existence",
        "prerequisites": [
            "Có source chuẩn của dự án WEB-MERN_t10-2024",
        ],
        "test_data": [],
        "steps": [
            {"detail": "Kiểm tra thư mục frontend/src/Pages/ForgotPassword", "expected": "Phải tồn tại page component cho luồng quên mật khẩu"},
        ],
    },

    "tests.test_source_audit::test_signup_validation_returns_after_empty_username": {
        "id": "SRC_04",
        "description": "Validation đăng ký phải dừng submit ngay khi username rỗng",
        "technique": "Source Audit / Validation Flow",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["username = rỗng"],
        "steps": [
            {"detail": "Mở hàm signUp trong frontend/src/Pages/AuthSignUp/index.js", "expected": "Có nhánh if kiểm tra username rỗng"},
            {"detail": "Kiểm tra nhánh lỗi username", "expected": "Sau khi setAlertBox phải return để dừng submit"},
        ],
    },

    "tests.test_source_audit::test_signup_validation_returns_after_empty_phone": {
        "id": "SRC_05",
        "description": "Validation đăng ký phải dừng submit ngay khi số điện thoại rỗng",
        "technique": "Source Audit / Validation Flow",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["phone = rỗng"],
        "steps": [
            {"detail": "Mở hàm signUp trong frontend/src/Pages/AuthSignUp/index.js", "expected": "Có nhánh if kiểm tra phone rỗng"},
            {"detail": "Kiểm tra nhánh lỗi phone", "expected": "Sau khi setAlertBox phải return để dừng submit"},
        ],
    },

    "tests.test_source_audit::test_signup_validation_returns_after_empty_full_name": {
        "id": "SRC_06",
        "description": "Validation đăng ký phải dừng submit ngay khi họ tên rỗng",
        "technique": "Source Audit / Validation Flow",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["fullName = rỗng"],
        "steps": [
            {"detail": "Mở hàm signUp trong frontend/src/Pages/AuthSignUp/index.js", "expected": "Có nhánh if kiểm tra fullName rỗng"},
            {"detail": "Kiểm tra nhánh lỗi fullName", "expected": "Sau khi setAlertBox phải return để dừng submit"},
        ],
    },

    "tests.test_source_audit::test_signup_validation_returns_after_empty_password": {
        "id": "SRC_07",
        "description": "Validation đăng ký phải dừng submit ngay khi mật khẩu rỗng",
        "technique": "Source Audit / Validation Flow",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["password = rỗng"],
        "steps": [
            {"detail": "Mở hàm signUp trong frontend/src/Pages/AuthSignUp/index.js", "expected": "Có nhánh if kiểm tra password rỗng"},
            {"detail": "Kiểm tra nhánh lỗi password", "expected": "Sau khi setAlertBox phải return để dừng submit"},
        ],
    },

    "tests.test_source_audit::test_signup_validation_returns_after_confirm_mismatch": {
        "id": "SRC_08",
        "description": "Validation đăng ký phải dừng submit khi xác nhận mật khẩu không khớp",
        "technique": "Source Audit / Validation Flow",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["password != confirmPassword"],
        "steps": [
            {"detail": "Mở hàm signUp trong frontend/src/Pages/AuthSignUp/index.js", "expected": "Có nhánh if kiểm tra confirmPassword khác password"},
            {"detail": "Kiểm tra nhánh lỗi confirmPassword", "expected": "Sau khi setAlertBox phải return để dừng submit"},
        ],
    },

    "tests.test_source_audit::test_checkout_payment_values_match_backend_contract": {
        "id": "SRC_09",
        "description": "Giá trị paymentMethod ở frontend phải khớp whitelist của backend",
        "technique": "Source Audit / API Contract",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["Frontend radio values", "Backend Joi valid values"],
        "steps": [
            {"detail": "Đọc paymentMethod trong frontend/src/Pages/Checkout/index.js", "expected": "Thu được danh sách value của radio thanh toán"},
            {"detail": "Đọc validateOrder trong server/middlewares/validate.js", "expected": "Thu được danh sách Joi.valid cho paymentMethod"},
            {"detail": "Đối chiếu 2 danh sách", "expected": "Frontend và backend phải dùng cùng tập giá trị"},
        ],
    },

    "tests.test_source_audit::test_checkout_serializes_items_to_backend_shape": {
        "id": "SRC_10",
        "description": "Checkout phải map items sang đúng shape backend trước khi gửi API",
        "technique": "Source Audit / Payload Shape",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["checkoutData.items"],
        "steps": [
            {"detail": "Mở hàm handleCheckout trong frontend/src/Pages/Checkout/index.js", "expected": "Tìm thấy payload checkoutData"},
            {"detail": "Kiểm tra trường items", "expected": "Items phải được map về productId chuỗi thay vì gửi object product đã populate"},
        ],
    },

    "tests.test_source_audit::test_remove_cart_endpoint_uses_product_variant_identity": {
        "id": "SRC_11",
        "description": "API xóa giỏ hàng phải xác định item theo productId + size + color",
        "technique": "Source Audit / Business Rule",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["productId, size, color"],
        "steps": [
            {"detail": "Mở route DELETE /removeCart/:id trong server/routes/cartRoutes.js", "expected": "Tìm thấy logic xóa item khỏi cart"},
            {"detail": "Kiểm tra tiêu chí findIndex", "expected": "Phải so sánh đủ productId, size và color"},
        ],
    },

    "tests.test_source_audit::test_get_cart_route_enforces_owner_authorization": {
        "id": "SRC_12",
        "description": "API lấy giỏ hàng phải chặn truy cập chéo giữa các user",
        "technique": "Source Audit / Authorization",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["req.params.id", "req.user.id"],
        "steps": [
            {"detail": "Mở route GET /getCart/:id trong server/routes/cartRoutes.js", "expected": "Route đã được verifyToken bảo vệ"},
            {"detail": "Kiểm tra so sánh chủ sở hữu", "expected": "Phải so sánh req.user.id với id trong params"},
        ],
    },

    "tests.test_source_audit::test_add_cart_route_enforces_owner_authorization": {
        "id": "SRC_13",
        "description": "API thêm vào giỏ phải chặn giả mạo userId trong request body",
        "technique": "Source Audit / Authorization",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["req.body.userId", "req.user.id"],
        "steps": [
            {"detail": "Mở route POST /addCart trong server/routes/cartRoutes.js", "expected": "Route dùng verifyToken"},
            {"detail": "Kiểm tra so sánh chủ sở hữu", "expected": "Phải so sánh req.user.id với userId trong body"},
        ],
    },

    "tests.test_source_audit::test_update_cart_route_enforces_owner_authorization": {
        "id": "SRC_14",
        "description": "API cập nhật giỏ phải chặn giả mạo userId trong request body",
        "technique": "Source Audit / Authorization",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["req.body.userId", "req.user.id"],
        "steps": [
            {"detail": "Mở route PUT /updateCart trong server/routes/cartRoutes.js", "expected": "Route dùng verifyToken"},
            {"detail": "Kiểm tra so sánh chủ sở hữu", "expected": "Phải so sánh req.user.id với userId trong body"},
        ],
    },

    "tests.test_source_audit::test_remove_cart_route_enforces_owner_authorization": {
        "id": "SRC_15",
        "description": "API xóa khỏi giỏ phải chặn truy cập chéo giữa các user",
        "technique": "Source Audit / Authorization",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["req.params.id", "req.user.id"],
        "steps": [
            {"detail": "Mở route DELETE /removeCart/:id trong server/routes/cartRoutes.js", "expected": "Route dùng verifyToken"},
            {"detail": "Kiểm tra so sánh chủ sở hữu", "expected": "Phải so sánh req.user.id với id trong params"},
        ],
    },

    "tests.test_source_audit::test_create_order_route_enforces_owner_authorization": {
        "id": "SRC_16",
        "description": "API tạo đơn hàng phải chặn giả mạo userId trong payload",
        "technique": "Source Audit / Authorization",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["req.body.userId", "req.user.id"],
        "steps": [
            {"detail": "Mở route POST /create trong server/routes/orderRoutes.js", "expected": "Route dùng verifyToken"},
            {"detail": "Kiểm tra so sánh chủ sở hữu", "expected": "Phải so sánh req.user.id với userId trong body trước khi tạo đơn"},
        ],
    },

    "tests.test_source_conformance::test_storefront_routes_exist": {
        "id": "SCF_01",
        "description": "Storefront phải khai báo đầy đủ các route chính trong App.js",
        "technique": "Source Review / Route Coverage",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["Danh sách route trọng yếu của storefront"],
        "steps": [
            {"detail": "Mở file frontend/src/App.js", "expected": "Tìm thấy cấu hình router của storefront"},
            {"detail": "Đối chiếu danh sách route chuẩn", "expected": "Mỗi route trọng yếu đều được khai báo trong App.js"},
        ],
    },

    "tests.test_source_conformance::test_signin_source_contains_expected_controls": {
        "id": "SCF_02",
        "description": "Màn hình đăng nhập phải có đầy đủ state, ref và control cốt lõi",
        "technique": "Source Review / UI Conformance",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["Các snippet cốt lõi của AuthSignIn"],
        "steps": [
            {"detail": "Mở file frontend/src/Pages/AuthSignIn/index.js", "expected": "Tìm thấy mã nguồn trang đăng nhập"},
            {"detail": "Đối chiếu state, ref, API và navigation control", "expected": "Các control cốt lõi của trang đăng nhập đều tồn tại"},
        ],
    },

    "tests.test_source_conformance::test_signup_source_contains_expected_controls": {
        "id": "SCF_03",
        "description": "Màn hình đăng ký phải có đầy đủ state, ref và luồng submit cơ bản",
        "technique": "Source Review / UI Conformance",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["Các snippet cốt lõi của AuthSignUp"],
        "steps": [
            {"detail": "Mở file frontend/src/Pages/AuthSignUp/index.js", "expected": "Tìm thấy mã nguồn trang đăng ký"},
            {"detail": "Đối chiếu state, ref và endpoint submit", "expected": "Các control cốt lõi của trang đăng ký đều tồn tại"},
        ],
    },

    "tests.test_source_conformance::test_validation_source_contains_expected_contracts": {
        "id": "SCF_04",
        "description": "Middleware validation phải chứa các rule cốt lõi cho signup, signin và order",
        "technique": "Source Review / Validation Contract",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["Rule Joi của signup, signin, order"],
        "steps": [
            {"detail": "Mở file server/middlewares/validate.js", "expected": "Tìm thấy schema validation"},
            {"detail": "Đối chiếu các rule cốt lõi", "expected": "Các rule chính của signup, signin và order đều tồn tại"},
        ],
    },

    "tests.test_source_conformance::test_checkout_source_contains_expected_controls": {
        "id": "SCF_05",
        "description": "Trang checkout phải có đủ control địa chỉ và phương thức thanh toán cơ bản",
        "technique": "Source Review / Checkout UI",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["Các control cốt lõi của Checkout"],
        "steps": [
            {"detail": "Mở file frontend/src/Pages/Checkout/index.js", "expected": "Tìm thấy mã nguồn trang checkout"},
            {"detail": "Đối chiếu control địa chỉ, textarea và payment radio", "expected": "Các control cốt lõi đều tồn tại"},
        ],
    },

    "tests.test_source_conformance::test_cart_routes_source_contains_expected_business_logic": {
        "id": "SCF_06",
        "description": "Cart routes phải chứa các endpoint và logic biến thể cơ bản",
        "technique": "Source Review / Business Logic",
        "prerequisites": ["Có source chuẩn của dự án WEB-MERN_t10-2024"],
        "test_data": ["Các endpoint và snippet logic của cartRoutes"],
        "steps": [
            {"detail": "Mở file server/routes/cartRoutes.js", "expected": "Tìm thấy các route của giỏ hàng"},
            {"detail": "Đối chiếu endpoint và logic size/color", "expected": "Các đoạn logic cốt lõi của cartRoutes đều tồn tại"},
        ],
    },
}


from utils.project_doc_data import CUSTOM_EXTRA_TEST_CASES, RISK_TEST_CASES, TEST_CASE_GROUPS, TIEN_TEST_CASES


_TC62_META_FUNCTIONS = {
    "register": ("tests.test_tc62_suite::test_tc62_register", "Black-box / Register Validation"),
    "login": ("tests.test_tc62_suite::test_tc62_login", "Black-box / Login and Session"),
    "password": ("tests.test_tc62_suite::test_tc62_password", "Black-box / Password Security"),
    "cart": ("tests.test_tc62_suite::test_tc62_cart", "Business Flow / Cart"),
    "checkout": ("tests.test_tc62_suite::test_tc62_checkout", "Business Flow / Checkout"),
}


for _group in TEST_CASE_GROUPS:
    _base_key, _technique = _TC62_META_FUNCTIONS[_group["group_id"]]
    for _case in _group["cases"]:
        TEST_CASE_META[f"{_base_key}[{_case['code']}]"] = {
            "id": _case["code"],
            "description": _case["scenario"],
            "technique": _technique,
            "prerequisites": [
                f"Thuộc {_group['module']} trong phạm vi đồ án.",
                "Website public và source chuẩn sẵn sàng để đối chiếu UI/API/source-level check.",
            ],
            "test_data": [
                _case["action"],
            ],
            "steps": [
                {
                    "detail": f"Mở nhóm testcase {_group['title']}",
                    "expected": "Đúng ngữ cảnh nghiệp vụ cho test case hiện tại",
                },
                {
                    "detail": _case["action"],
                    "expected": _case["expected"],
                },
                {
                    "detail": f"Đối chiếu kết quả của testcase {_case['code']}",
                    "expected": "Kết quả thực tế phù hợp với đặc tả và bug finding liên quan",
                },
            ],
        }


for _case in TIEN_TEST_CASES:
    _code = _case["code"]
    TEST_CASE_META[f"tests.test_tien_test_cases::test_tien_case[{_code}]"] = {
        "id": _code,
        "description": _case["scenario"],
        "technique": "Test Case Của Tiến / Focused Functional Validation",
        "prerequisites": [
            "Website public và source chuẩn sẵn sàng để đối chiếu UI/API/source-level check.",
            "Bộ testcase này chạy riêng theo danh sách Test Case Của Tiến từ REG_13 đến VCH_08.",
        ],
        "test_data": [
            _case["action"],
        ],
        "steps": [
            {
                "detail": "Mở đúng ngữ cảnh chức năng theo mã test case của Tiến.",
                "expected": "Đúng module và dữ liệu đầu vào của testcase hiện tại.",
            },
            {
                "detail": _case["action"],
                "expected": _case["expected"],
            },
            {
                "detail": f"Đối chiếu kết quả của testcase {_code}.",
                "expected": "Kết quả thực tế phải đúng với yêu cầu mong đợi, hoặc report phải ghi rõ bug và bằng chứng lỗi.",
            },
        ],
        "severity": "HIGH" if _code.startswith(("REG", "LOG", "PWD")) else "MEDIUM",
    }


for _case in CUSTOM_EXTRA_TEST_CASES:
    _code = _case["code"]
    _uid = _case["unique_id"]
    TEST_CASE_META[f"tests.test_custom_extra_cases::test_custom_extra_case[{_uid}]"] = {
        "id": _code,
        "description": _case["scenario"],
        "technique": "Test Case Mới 66-85 / Focused Edge Case Validation",
        "prerequisites": [
            "Website public và source chuẩn sẵn sàng để đối chiếu UI/API/source-level check.",
            "Bộ testcase này chạy riêng theo nút Test Case Mới 66-85; các mã trùng được tách bằng unique_id nội bộ để không bỏ sót dòng nào.",
        ],
        "test_data": [
            _case["action"],
            f"Unique ID chạy tự động: {_uid}",
        ],
        "steps": [
            {
                "detail": "Mở đúng ngữ cảnh chức năng theo testcase mới.",
                "expected": "Đúng module và dữ liệu đầu vào của testcase hiện tại.",
            },
            {
                "detail": _case["action"],
                "expected": _case["expected"],
            },
            {
                "detail": f"Đối chiếu kết quả của testcase {_code} ({_uid}).",
                "expected": "Kết quả thực tế phải đúng với yêu cầu mong đợi; nếu không đúng thì report phải ghi rõ bug, bước tái hiện và hình ảnh giao diện.",
            },
        ],
        "severity": "HIGH" if _code.startswith("REG") else "MEDIUM",
    }


for _case in RISK_TEST_CASES:
    _code = _case["code"]
    _uid = _case["unique_id"]
    TEST_CASE_META[f"tests.test_risk_cases::test_risk_case[{_uid}]"] = {
        "id": _code,
        "description": _case["scenario"],
        "technique": "Risk Suite / Security and Critical Business Flow",
        "prerequisites": [
            "Website public và source chuẩn sẵn sàng để đối chiếu UI/API/source-level check.",
            "Bộ testcase này chạy riêng theo nút Run 6 Case Rủi Ro để xuất ảnh lỗi, dữ liệu xác thực và Bug_Report chi tiết.",
        ],
        "test_data": [
            _case["action"],
            f"Unique ID chạy tự động: {_uid}",
        ],
        "steps": [
            {
                "detail": "Mở đúng ngữ cảnh chức năng cần kiểm thử.",
                "expected": "Đúng module, đúng form hoặc đúng API endpoint theo testcase.",
            },
            {
                "detail": _case["action"],
                "expected": _case["expected"],
            },
            {
                "detail": f"Đối chiếu kết quả của testcase {_code} ({_uid}) và ghi bug nếu không đạt.",
                "expected": "Report phải có trạng thái pass/fail rõ ràng, bước tái hiện thủ công, dữ liệu input và ảnh giao diện khi fail.",
            },
        ],
        "severity": "HIGH" if _code.startswith(("CHK", "VCH")) else "MEDIUM",
    }


TEST_CASE_META.update(
    {
        "tests.test_tc62_suite::test_tc62_register[REG_01]": {
            "id": "REG_01",
            "description": "Đăng ký thành công (Happy Path)",
            "technique": "Black-box / Happy Path / Register",
            "prerequisites": [
                "Người dùng truy cập được website public Guangli Shop.",
                "Trang Đăng ký hiển thị đầy đủ các trường bắt buộc theo đặc tả: Tên, Email, SĐT, Mật khẩu, Nhập lại mật khẩu.",
            ],
            "test_data": [
                "Tên: Selenium Register User",
                "Email: user_hople@mail.test",
                "SĐT: số mới chưa tồn tại",
                "Password: Abcd123@",
                "Re-password: Abcd123@",
            ],
            "steps": [
                {"detail": "Mở trang chủ, chọn Đăng nhập rồi chuyển sang form Đăng ký.", "expected": "Form Đăng ký hiển thị đúng."},
                {"detail": "Kiểm tra có trường Email trên form.", "expected": "Form hiển thị input Email khả dụng."},
                {"detail": "Nhập đầy đủ dữ liệu hợp lệ vào Tên, Email, SĐT, Password và Re-password.", "expected": "Tất cả dữ liệu được nhập thành công."},
                {"detail": "Bấm nút Đăng ký.", "expected": "Hệ thống chuyển hướng về Đăng nhập hoặc mở bước OTP / thông báo đăng ký thành công."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_02]": {
            "id": "REG_02",
            "description": "Bỏ trống tất cả các trường bắt buộc",
            "technique": "Black-box / Required Validation",
            "prerequisites": [
                "Trang Đăng ký hiển thị và chưa nhập dữ liệu.",
            ],
            "test_data": [
                "Không nhập Username/Email/Phone/Password/Re-password.",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị ổn định."},
                {"detail": "Giữ trống toàn bộ các trường.", "expected": "Chưa có request đăng ký nào được gửi."},
                {"detail": "Bấm nút Đăng ký.", "expected": "Tại từng trường bắt buộc xuất hiện validation 'Vui lòng nhập...' hoặc trình duyệt chặn submit."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_03]": {
            "id": "REG_03",
            "description": "Đăng ký với Email đã tồn tại",
            "technique": "Equivalence Partitioning (Invalid)",
            "prerequisites": [
                "Hệ thống có sẵn ít nhất 1 tài khoản đã đăng ký email.",
                "Form Đăng ký có hỗ trợ input Email theo yêu cầu báo cáo.",
            ],
            "test_data": [
                "Email: existing.user@mail.test",
                "Các trường còn lại hợp lệ và chưa trùng.",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị đầy đủ."},
                {"detail": "Nhập Email đã tồn tại cùng các trường còn lại hợp lệ.", "expected": "Dữ liệu nhập thành công."},
                {"detail": "Bấm Đăng ký.", "expected": "Hệ thống báo 'Email đã được sử dụng' và không tạo tài khoản mới."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_04]": {
            "id": "REG_04",
            "description": "Đăng ký với SĐT đã tồn tại",
            "technique": "Equivalence Partitioning (Invalid)",
            "prerequisites": [
                "Hệ thống có sẵn ít nhất 1 tài khoản đã đăng ký số điện thoại.",
            ],
            "test_data": [
                "SĐT: số điện thoại đã tồn tại trong CSDL",
                "Các trường còn lại hợp lệ và không trùng.",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị đúng."},
                {"detail": "Nhập SĐT đã tồn tại và các trường còn lại hợp lệ.", "expected": "Dữ liệu được chấp nhận ở mức nhập liệu."},
                {"detail": "Bấm Đăng ký.", "expected": "Hệ thống báo 'Số điện thoại đã tồn tại' và chặn tạo tài khoản."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_05]": {
            "id": "REG_05",
            "description": "Định dạng Email không hợp lệ",
            "technique": "Boundary / Format Validation",
            "prerequisites": [
                "Form Đăng ký hỗ trợ trường Email.",
            ],
            "test_data": [
                "Email test 1: test@.com",
                "Email test 2: test.com",
                "Email test 3: test@domain",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị đầy đủ."},
                {"detail": "Nhập email sai định dạng cùng dữ liệu còn lại hợp lệ.", "expected": "Trường Email vẫn cho nhập dữ liệu để kiểm tra validation."},
                {"detail": "Bấm Đăng ký.", "expected": "Hiển thị lỗi 'Định dạng email không hợp lệ' và không tạo tài khoản."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_06]": {
            "id": "REG_06",
            "description": "Định dạng SĐT không hợp lệ (chứa chữ cái)",
            "technique": "Input Validation / Invalid Characters",
            "prerequisites": [
                "Form Đăng ký hiển thị trường SĐT.",
            ],
            "test_data": [
                "SĐT: 0901abc123",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị đúng."},
                {"detail": "Nhập SĐT chứa ký tự chữ vào ô số điện thoại.", "expected": "Hệ thống chặn không cho nhập chữ hoặc giữ nguyên để báo lỗi khi submit."},
                {"detail": "Bấm Đăng ký.", "expected": "Hiển thị lỗi định dạng SĐT và không cho đăng ký."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_07]": {
            "id": "REG_07",
            "description": "SĐT không đủ độ dài",
            "technique": "Boundary Value Analysis (Invalid)",
            "prerequisites": [
                "Form Đăng ký hiển thị trường SĐT.",
            ],
            "test_data": [
                "SĐT: 09012345",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị đúng."},
                {"detail": "Nhập SĐT chỉ có 8 số cùng dữ liệu còn lại hợp lệ.", "expected": "Dữ liệu được nhập nhưng chưa hợp lệ theo yêu cầu 10 số."},
                {"detail": "Bấm Đăng ký.", "expected": "Hiển thị lỗi 'Số điện thoại phải có 10 chữ số' hoặc lỗi độ dài tương đương."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_08]": {
            "id": "REG_08",
            "description": "Mật khẩu quá ngắn",
            "technique": "Boundary Value Analysis (Invalid)",
            "prerequisites": [
                "Form Đăng ký hiển thị trường Mật khẩu và Nhập lại mật khẩu.",
            ],
            "test_data": [
                "Password: 12345",
                "Re-password: 12345",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị đúng."},
                {"detail": "Nhập mật khẩu chỉ 5 ký tự.", "expected": "Dữ liệu được nhập vào hai trường password."},
                {"detail": "Bấm Đăng ký.", "expected": "Hiển thị lỗi 'Mật khẩu phải từ 8 ký tự trở lên' hoặc lỗi chuẩn password tương đương."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_09]": {
            "id": "REG_09",
            "description": "Xác nhận mật khẩu không khớp",
            "technique": "Equivalence Partitioning (Invalid)",
            "prerequisites": [
                "Form Đăng ký hiển thị hai trường password và re-password.",
            ],
            "test_data": [
                "Password: Abc@1234",
                "Re-password: Abc@1235",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị đúng."},
                {"detail": "Nhập password và re-password khác nhau.", "expected": "Hai giá trị được giữ nguyên trên form."},
                {"detail": "Bấm Đăng ký.", "expected": "Hiển thị lỗi 'Mật khẩu xác nhận không trùng khớp' và không tạo tài khoản."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_10]": {
            "id": "REG_10",
            "description": "Mã OTP không hợp lệ",
            "technique": "Black-box / OTP Negative Flow",
            "prerequisites": [
                "Sau khi submit đăng ký hợp lệ, hệ thống phải mở bước OTP.",
            ],
            "test_data": [
                "OTP nhập sai: 999999",
            ],
            "steps": [
                {"detail": "Hoàn tất bước đăng ký với dữ liệu hợp lệ.", "expected": "Hệ thống chuyển sang bước xác thực OTP."},
                {"detail": "Nhập mã OTP sai.", "expected": "Mã OTP được gửi đi để kiểm tra."},
                {"detail": "Xác nhận OTP.", "expected": "Hệ thống báo 'Mã xác thực không hợp lệ' và không kích hoạt tài khoản."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_11]": {
            "id": "REG_11",
            "description": "Mã OTP hết hạn",
            "technique": "Boundary / OTP Expiry",
            "prerequisites": [
                "Luồng OTP có hiển thị thời hạn hoặc cơ chế gửi lại mã.",
            ],
            "test_data": [
                "OTP hợp lệ nhưng nhập sau thời gian timeout quy định.",
            ],
            "steps": [
                {"detail": "Hoàn tất bước đăng ký để mở bước OTP.", "expected": "Dialog hoặc form OTP hiển thị."},
                {"detail": "Chờ quá thời gian hiệu lực của OTP.", "expected": "OTP chuyển sang trạng thái hết hạn."},
                {"detail": "Nhập lại OTP cũ và xác nhận.", "expected": "Hệ thống báo 'Mã xác thực đã hết hạn' hoặc yêu cầu gửi lại mã."},
            ],
        },
        "tests.test_tc62_suite::test_tc62_register[REG_12]": {
            "id": "REG_12",
            "description": "Kiểm thử bảo mật đăng ký với payload SQL Injection",
            "technique": "Security / SQL Injection",
            "prerequisites": [
                "Form Đăng ký cho phép nhập username từ giao diện.",
            ],
            "test_data": [
                "Username: ' OR 1=1 --",
                "Các trường còn lại hợp lệ.",
            ],
            "steps": [
                {"detail": "Mở form Đăng ký.", "expected": "Form hiển thị đúng."},
                {"detail": "Nhập payload nghi ngờ SQL Injection vào ô tên đăng nhập.", "expected": "Payload được hệ thống kiểm tra như dữ liệu đầu vào bình thường."},
                {"detail": "Bấm Đăng ký.", "expected": "Hệ thống từ chối ký tự không hợp lệ hoặc chặn tạo tài khoản, không phát sinh hành vi injection."},
            ],
        },
    }
)
