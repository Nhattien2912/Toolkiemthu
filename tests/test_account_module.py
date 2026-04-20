import requests
from selenium.webdriver.common.keys import Keys

from pages.account_page import AccountPage
from pages.login_page import LoginPage
from pages.order_page import OrderPage


def assert_no_horizontal_scrollbar(driver):
    assert driver.execute_script(
        "return document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1;"
    )


def assert_images_load_ok(urls):
    for url in urls[:3]:
        if "via.placeholder.com" in url:
            continue
        response = requests.get(url, timeout=30)
        assert response.ok, f"Broken image: {url}"


def test_account_login_page_ui_alignment_and_title(driver, step_logger):
    login_page = LoginPage(driver)

    step_logger("Mo trang dang nhap de kiem tra bo cuc va title.")
    login_page.open()

    positions = login_page.get_login_field_positions()
    assert driver.title.strip() != ""
    assert abs(positions["username"]["x"] - positions["password"]["x"]) <= 5
    assert login_page.get_cursor_style(login_page.USERNAME_INPUT) in {"auto", "text"}
    assert login_page.get_forgot_password_link_href().endswith("/signIn")
    assert_no_horizontal_scrollbar(driver)


def test_account_login_invalid_keeps_values_and_shows_error(driver, step_logger):
    login_page = LoginPage(driver)

    step_logger("Mo trang dang nhap va gui form sai de kiem tra validation.")
    login_page.open()
    login_page.login("wrong_user", "wrong_pass")

    message = login_page.get_message().casefold()
    assert "không đúng" in message
    assert login_page.get_username_value() == "wrong_user"
    assert login_page.get_password_value() == "wrong_pass"


def test_account_login_keyboard_navigation_and_enter_submit(driver, step_logger):
    login_page = LoginPage(driver)

    step_logger("Mo trang dang nhap va kiem tra tab order username -> password.")
    login_page.open()
    username_input = driver.find_element(*login_page.USERNAME_INPUT)
    username_input.click()
    username_input.send_keys("wrong_user")
    username_input.send_keys(Keys.TAB)

    assert login_page.get_active_element_name() == "password"

    step_logger("Gui form bang phim Enter tren o mat khau.")
    driver.switch_to.active_element.send_keys("wrong_pass")
    driver.switch_to.active_element.send_keys(Keys.ENTER)
    assert "không đúng" in login_page.get_message().casefold()


def test_account_signup_form_fields_and_layout(driver, step_logger):
    login_page = LoginPage(driver)

    step_logger("Mo form dang ky de kiem tra truong nhap va canh le.")
    login_page.open()
    login_page.go_to_signup()

    positions = login_page.get_signup_field_positions()
    body_text = login_page.get_body_text()
    assert "Đăng Ký Tài Khoản" in body_text
    assert login_page.signup_fields_are_visible()
    assert abs(positions["username"]["y"] - positions["phone"]["y"]) <= 5
    assert abs(positions["fullName"]["x"] - positions["password"]["x"]) <= 5
    assert abs(positions["password"]["x"] - positions["confirmPassword"]["x"]) <= 5
    assert_no_horizontal_scrollbar(driver)


def test_account_forgot_password_link_is_clickable(driver, step_logger):
    login_page = LoginPage(driver)

    step_logger("Mo login page va click link Quen Mat Khau.")
    login_page.open()
    login_page.click_forgot_password_link()

    assert driver.current_url.endswith("/signIn")
    assert "Đăng Nhập" in login_page.get_body_text()


def test_account_profile_page_form_and_change_password_tab(driver, authenticated_session, step_logger):
    account_page = AccountPage(driver)

    step_logger("Mo trang thong tin tai khoan cua user da dang nhap.")
    account_page.open_spa()

    labels = account_page.get_visible_labels()
    positions = account_page.get_profile_input_positions()
    assert driver.title.strip() != ""
    assert "Tên tài khoản" in labels
    assert "Họ và tên" in labels
    assert "Số điện thoại" in labels
    assert "Email" in labels
    assert abs(positions["username"]["x"] - positions["phone"]["x"]) <= 5
    assert abs(positions["fullName"]["x"] - positions["email"]["x"]) <= 5
    assert abs(positions["username"]["y"] - positions["fullName"]["y"]) <= 5
    assert abs(positions["phone"]["y"] - positions["email"]["y"]) <= 5

    step_logger("Chuyen sang tab doi mat khau.")
    account_page.click_change_password_tab()
    tab_states = account_page.get_tab_states()
    assert tab_states["THAY ĐỔI MẬT KHẨU"] == "true"
    assert account_page.get_visible_password_fields_count() == 2


def test_account_profile_avatar_and_order_page_access(driver, authenticated_session, step_logger):
    account_page = AccountPage(driver)
    order_page = OrderPage(driver)

    step_logger("Mo trang tai khoan va kiem tra avatar khong bi hong.")
    account_page.open_spa()
    assert_images_load_ok(account_page.get_visible_image_sources())

    step_logger("Mo trang don hang tu module tai khoan.")
    order_page.open_spa()
    order_text = order_page.get_body_text()
    assert "Danh Sách Đơn Hàng" in order_text
    assert (
        "Không có đơn hàng nào" in order_text
        or "Không tìm thấy đơn hàng của bạn" in order_text
        or "Loading..." in order_text
    )
