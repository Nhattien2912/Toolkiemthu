"""
Module TNT - Đăng Ký (Register)
Tự động hóa các test case đăng ký tài khoản trên https://guangli-shop.netlify.app/

Test IDs: TNT_01 → TNT_05
"""

import time
from random import randint

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage


def _unique_credentials():
    uid = f"{int(time.time())}{randint(100, 999)}"
    return {
        "username": f"testreg{uid[-8:]}",
        "phone":    f"09{uid[-8:]}",
        "fullname": "Selenium Test User",
        "password": "Abcd123@",
    }


def _open_signup(driver, login_page, step_logger):
    step_logger("Mo trang chu, click Dang Nhap roi chuyen sang form Dang Ky.")
    login_page.open()
    login_page.go_to_signup()


# TNT_01 ──────────────────────────────────────────────────────────────────────

def test_register_empty_form(driver, step_logger):
    """Submit form đăng ký khi bỏ trống tất cả trường → không được đăng ký thành công."""
    login_page = LoginPage(driver)
    _open_signup(driver, login_page, step_logger)

    step_logger("Khong nhap bat ky thong tin nao, nhan nut DANG KY.")
    login_page.click_signup_submit()

    step_logger("Kiem tra URL van o trang dang ky hoac co thong bao loi.")
    current_url = driver.current_url
    alert_text  = login_page.get_alert_text()

    still_on_signup = "/signup" in current_url or "/signIn" in current_url
    has_error = len(alert_text) > 0

    assert still_on_signup or has_error, (
        f"Form trong rong da bi submit thanh cong! URL: {current_url}, alert: '{alert_text}'"
    )
    step_logger(f"Xac nhan: URL={current_url!r}, alert={alert_text!r}")


# TNT_02 ──────────────────────────────────────────────────────────────────────

def test_register_password_mismatch(driver, step_logger):
    """Password và Confirm Password không khớp → không đăng ký được."""
    login_page = LoginPage(driver)
    creds = _unique_credentials()
    _open_signup(driver, login_page, step_logger)

    step_logger("Dien day du thong tin hop le, nhung Confirm Password khac mat khau chinh.")
    login_page.fill_signup_form(
        username=creds["username"],
        phone=creds["phone"],
        full_name=creds["fullname"],
        password="Abc@1234",
        confirm_password="Abc@5678",   # mismatch
    )

    step_logger("Nhan nut DANG KY.")
    login_page.click_signup_submit()

    step_logger("Kiem tra co loi hoac URL van o trang dang ky.")
    current_url = driver.current_url
    alert_text  = login_page.get_alert_text()

    still_on_signup = "/signup" in current_url or "/signIn" in current_url
    has_error = len(alert_text) > 0

    assert still_on_signup or has_error, (
        f"Mat khau khong khop nhung dang ky van thanh cong! URL: {current_url}"
    )
    step_logger(f"Xac nhan that bai: URL={current_url!r}, alert={alert_text!r}")


# TNT_03 ──────────────────────────────────────────────────────────────────────

def test_register_short_password(driver, step_logger):
    """Password 7 ký tự (dưới tối thiểu 8) → không đăng ký được (Boundary Value)."""
    login_page = LoginPage(driver)
    creds = _unique_credentials()
    _open_signup(driver, login_page, step_logger)

    step_logger("Dien thong tin hop le, mat khau chi 7 ky tu: Abc@123.")
    login_page.fill_signup_form(
        username=creds["username"],
        phone=creds["phone"],
        full_name=creds["fullname"],
        password="Abc@123",       # 7 chars
        confirm_password="Abc@123",
    )

    step_logger("Nhan nut DANG KY.")
    login_page.click_signup_submit()

    step_logger("Kiem tra co loi hoac URL van o trang dang ky.")
    current_url = driver.current_url
    alert_text  = login_page.get_alert_text()

    still_on_signup = "/signup" in current_url or "/signIn" in current_url
    has_error = len(alert_text) > 0

    assert still_on_signup or has_error, (
        f"Mat khau 7 ky tu nhung dang ky van thanh cong! URL: {current_url}"
    )
    step_logger(f"Xac nhan that bai (BVA): URL={current_url!r}, alert={alert_text!r}")


# TNT_04 ──────────────────────────────────────────────────────────────────────

def test_register_navigate_to_login(driver, step_logger):
    """Từ form đăng ký, click link 'Đăng Nhập' → chuyển về form đăng nhập."""
    login_page = LoginPage(driver)
    _open_signup(driver, login_page, step_logger)

    step_logger("Tim va click link 'Dang Nhap' tren form dang ky.")
    login_page.click_login_link_from_signup()

    step_logger("Kiem tra form Dang Nhap hien thi (o username hoac password phai visible).")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located(login_page.USERNAME_INPUT))

    body_text = login_page.get_body_text()
    assert "Đăng Nhập" in body_text, f"Khong chuyen sang form Dang Nhap. Body: {body_text[:200]}"
    step_logger("Xac nhan da chuyen sang form Dang Nhap thanh cong.")


# TNT_05 ──────────────────────────────────────────────────────────────────────

def test_register_valid_success(driver, step_logger):
    """Đăng ký tài khoản mới với đầy đủ thông tin hợp lệ → thành công qua UI."""
    login_page = LoginPage(driver)
    creds = _unique_credentials()
    _open_signup(driver, login_page, step_logger)

    step_logger(f"Dien day du thong tin hop le: username={creds['username']}, phone={creds['phone']}.")
    login_page.fill_signup_form(
        username=creds["username"],
        phone=creds["phone"],
        full_name=creds["fullname"],
        password=creds["password"],
        confirm_password=creds["password"],
    )

    step_logger("Nhan nut DANG KY.")
    login_page.click_signup_submit()

    step_logger("Kiem tra dang ky thanh cong: chuyen trang hoac hien thi thong bao thanh cong.")
    wait = WebDriverWait(driver, 20)

    # Accept success if: URL changed away from /signup, OR success alert shown
    def _success_condition(d):
        url = d.current_url
        if "/signup" not in url and "/signIn" not in url:
            return True
        try:
            alert = d.find_element(*login_page.ALERT_MESSAGE)
            if alert.is_displayed():
                text = alert.text.lower()
                return "thành công" in text or "success" in text
        except Exception:
            pass
        return False

    success = wait.until(_success_condition)
    assert success, (
        f"Dang ky that bai! URL: {driver.current_url}, alert: {login_page.get_alert_text()!r}"
    )
    step_logger(f"Dang ky thanh cong. URL hien tai: {driver.current_url}")
