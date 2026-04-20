from pages.cart_page import CartPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


PRODUCT_DETAIL_TEXTS = [
    "Thương hiệu:",
    "Loại Danh mục:",
    "Mô Tả",
    "Thông Tin Thêm",
    "Đánh Giá Sản Phẩm",
    "Thêm Vào Giỏ Hàng",
]


def test_product_detail_page_ui(driver, step_logger):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)

    step_logger("Mo trang chu.")
    home_page.open()

    step_logger("Mo trang chi tiet san pham dau tien dang hien thi.")
    home_page.open_first_product()
    product_page.wait_until_loaded()

    step_logger("Kiem tra cac thanh phan chinh cua trang chi tiet san pham.")
    for text in PRODUCT_DETAIL_TEXTS:
        assert product_page.has_text(text)


def test_cart_page_empty_ui(driver, step_logger):
    home_page = HomePage(driver)
    cart_page = CartPage(driver)

    step_logger("Mo trang chu.")
    home_page.open()

    step_logger("Di chuyen sang trang gio hang.")
    home_page.go_to_cart()
    cart_page.wait_until_loaded()

    step_logger("Kiem tra giao dien gio hang trong truong hop chua co san pham.")
    assert cart_page.has_text("Giỏ Hàng Của Bạn")
    assert cart_page.has_text("Giỏ hàng của bạn đang trống")


def test_contact_page_ui(driver, step_logger):
    home_page = HomePage(driver)
    contact_page = ContactPage(driver)

    step_logger("Mo trang chu.")
    home_page.open()

    step_logger("Di chuyen sang trang lien he.")
    home_page.go_to_contact()
    contact_page.wait_until_loaded()

    step_logger("Kiem tra giao dien trang lien he.")
    assert contact_page.has_text("LIÊN HỆ VỚI CHÚNG TÔI")
    assert contact_page.has_text("Email hoặc số điện thoại của bạn")
    assert contact_page.has_text("GỬI LỜI NHẮN")
