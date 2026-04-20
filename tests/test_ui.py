from pages.home_page import HomePage
from pages.login_page import LoginPage


SEARCH_TEXT = "T\u00ecm ki\u1ebfm"
LOGIN_TEXT = "\u0110\u0103ng Nh\u1eadp"
FEATURED_TEXT = "S\u1ea2N PH\u1ea8M N\u1ed4I B\u1eacT"
NEW_PRODUCTS_TEXT = "S\u1ea2N PH\u1ea8M M\u1edaI"
LOGIN_TITLE_TEXT = "\u0110\u0103ng Nh\u1eadp"
USERNAME_OR_PHONE_TEXT = "T\u00ean t\u00e0i kho\u1ea3n ho\u1eb7c s\u1ed1 \u0111i\u1ec7n tho\u1ea1i"
PASSWORD_TEXT = "M\u1eadt kh\u1ea9u"
LOGIN_BUTTON_TEXT = "\u0110\u0102NG NH\u1eacP"
SIGNUP_TITLE_TEXT = "\u0110\u0103ng K\u00fd T\u00e0i Kho\u1ea3n"


def test_homepage_main_ui(driver, step_logger):
    home_page = HomePage(driver)

    step_logger("Mo trang chu Guangli Shop.")
    home_page.open()

    step_logger("Kiem tra o tim kiem va cac khoi giao dien chinh.")
    assert home_page.get_search_placeholder().startswith(SEARCH_TEXT)
    assert home_page.has_text(FEATURED_TEXT)
    assert home_page.has_text(NEW_PRODUCTS_TEXT)
    assert home_page.has_text(LOGIN_TEXT)

    step_logger("Kiem tra trang co it nhat 1 san pham hien thi.")
    assert home_page.get_visible_product_links_count() > 0


def test_login_and_signup_ui(driver, step_logger):
    login_page = LoginPage(driver)

    step_logger("Mo trang login tu trang chu.")
    login_page.open()

    step_logger("Kiem tra form Dang Nhap hien thi day du.")
    body_text = login_page.get_body_text()
    assert LOGIN_TITLE_TEXT in body_text
    assert USERNAME_OR_PHONE_TEXT in body_text
    assert PASSWORD_TEXT in body_text
    assert LOGIN_BUTTON_TEXT in body_text

    step_logger("Chuyen tu Dang Nhap sang Dang Ky.")
    login_page.go_to_signup()

    step_logger("Kiem tra form Dang Ky hien thi day du cac truong.")
    signup_text = login_page.get_body_text()
    assert SIGNUP_TITLE_TEXT in signup_text
    assert login_page.signup_fields_are_visible()
