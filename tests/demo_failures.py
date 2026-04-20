from pages.cart_page import CartPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.search_page import SearchPage


def test_demo_fail_homepage_placeholder(driver, step_logger):
    home_page = HomePage(driver)
    step_logger("Mo trang chu va co y so sanh sai placeholder.")
    home_page.open()
    assert home_page.get_search_placeholder() == "Sai placeholder de demo fail"


def test_demo_fail_homepage_missing_banner(driver, step_logger):
    home_page = HomePage(driver)
    step_logger("Mo trang chu va co y kiem tra text khong ton tai.")
    home_page.open()
    assert home_page.has_text("KHUYEN MAI 90% TOAN BO WEBSITE")


def test_demo_fail_homepage_product_count(driver, step_logger):
    home_page = HomePage(driver)
    step_logger("Mo trang chu va co y dat dieu kien so luong san pham qua lon.")
    home_page.open()
    assert home_page.get_visible_product_links_count() > 50


def test_demo_fail_invalid_login_expected_success(driver, step_logger):
    login_page = LoginPage(driver)
    step_logger("Mo form dang nhap va co y ky vong dang nhap sai nhung van thanh cong.")
    login_page.open()
    login_page.login("wrong_user_demo", "wrong_password_demo")
    assert login_page.get_session_token() is not None


def test_demo_fail_invalid_login_expected_wrong_message(driver, step_logger):
    login_page = LoginPage(driver)
    step_logger("Mo form dang nhap va co y so sanh sai thong bao.")
    login_page.open()
    login_page.login("wrong_user_demo", "wrong_password_demo")
    assert login_page.get_message() == "Dang nhap thanh cong 100 phan tram"


def test_demo_fail_search_expected_result_for_gibberish(driver, step_logger):
    home_page = HomePage(driver)
    search_page = SearchPage(driver)
    step_logger("Tim kiem tu khoa rac va co y ky vong co ket qua.")
    home_page.open()
    home_page.search("demo_fail_keyword_999999")
    search_page.wait_until_loaded()
    assert search_page.get_visible_product_links_count() > 0


def test_demo_fail_search_expected_no_result_for_valid_keyword(driver, step_logger):
    home_page = HomePage(driver)
    search_page = SearchPage(driver)
    step_logger("Tim kiem keyword hop le va co y ky vong khong co ket qua.")
    home_page.open()
    home_page.search("Adidas")
    search_page.wait_until_loaded()
    assert search_page.get_visible_product_links_count() == 0


def test_demo_fail_product_detail_wrong_text(driver, step_logger):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    step_logger("Mo product detail va co y check text sai.")
    home_page.open()
    home_page.open_first_product()
    product_page.wait_until_loaded()
    assert product_page.has_text("Mien phi van chuyen quoc te")


def test_demo_fail_cart_empty_wrong_message(driver, step_logger):
    home_page = HomePage(driver)
    cart_page = CartPage(driver)
    step_logger("Mo gio hang rong va co y ky vong thong diep sai.")
    home_page.open()
    home_page.go_to_cart()
    cart_page.wait_until_loaded()
    assert cart_page.has_text("Co 5 san pham trong gio hang cua ban")


def test_demo_fail_contact_wrong_title(driver, step_logger):
    home_page = HomePage(driver)
    contact_page = ContactPage(driver)
    step_logger("Mo trang lien he va co y check sai tieu de.")
    home_page.open()
    home_page.go_to_contact()
    contact_page.wait_until_loaded()
    assert contact_page.has_text("TRANG THANH TOAN")
