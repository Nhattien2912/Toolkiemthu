from config import (
    INVALID_LOGIN_MESSAGE,
    INVALID_PASSWORD,
    INVALID_USERNAME,
    SUCCESS_LOGIN_MESSAGE,
)
from pages.login_page import LoginPage
from utils.account_api import create_test_account


def test_login_success(driver, step_logger):
    account = create_test_account()
    login_page = LoginPage(driver)
    step_logger("Tao tai khoan test moi qua API.")
    login_page.open()
    step_logger("Mo trang chu va di vao form Dang Nhap.")
    login_page.login(account.username, account.password)
    step_logger(f"Dang nhap voi username: {account.username}")

    assert login_page.get_message() == SUCCESS_LOGIN_MESSAGE
    step_logger("Kiem tra message dang nhap thanh cong.")
    assert login_page.get_session_token() is not None
    assert account.username in login_page.get_session_user()
    step_logger("Xac nhan sessionStorage da luu token va thong tin user.")


def test_login_invalid(driver, step_logger):
    login_page = LoginPage(driver)
    login_page.open()
    step_logger("Mo form Dang Nhap.")
    login_page.login(INVALID_USERNAME, INVALID_PASSWORD)
    step_logger("Nhap tai khoan sai va gui form.")

    assert login_page.get_message() == INVALID_LOGIN_MESSAGE
    step_logger("Kiem tra thong bao dang nhap that bai.")
    assert login_page.get_session_token() is None
    step_logger("Xac nhan khong co token duoc luu.")


def test_login_success_persists_after_refresh(driver, step_logger):
    account = create_test_account()
    login_page = LoginPage(driver)
    step_logger("Tao tai khoan test moi de kiem tra refresh session.")
    login_page.open()
    login_page.login(account.username, account.password)
    step_logger("Dang nhap thanh cong va refresh trinh duyet.")

    assert login_page.get_message() == SUCCESS_LOGIN_MESSAGE
    driver.refresh()

    assert login_page.get_session_token() is not None
    assert account.username in login_page.get_session_user()
    step_logger("Xac nhan sessionStorage van giu token sau khi refresh.")


def test_login_invalid_with_existing_username(driver, step_logger):
    account = create_test_account()
    login_page = LoginPage(driver)
    step_logger("Tao tai khoan test moi de thu sai mat khau bang username hop le.")
    login_page.open()
    login_page.login(account.username, INVALID_PASSWORD)
    step_logger("Nhap username dung nhung mat khau sai.")

    assert login_page.get_message() == INVALID_LOGIN_MESSAGE
    assert login_page.get_session_token() is None
    step_logger("Xac nhan dang nhap that bai khi sai mat khau.")


def test_login_invalid_with_existing_phone(driver, step_logger):
    account = create_test_account()
    login_page = LoginPage(driver)
    step_logger("Tao tai khoan test moi de thu sai mat khau bang so dien thoai hop le.")
    login_page.open()
    login_page.login(account.phone, INVALID_PASSWORD)
    step_logger("Nhap so dien thoai dung nhung mat khau sai.")

    assert login_page.get_message() == INVALID_LOGIN_MESSAGE
    assert login_page.get_session_token() is None
    step_logger("Xac nhan dang nhap that bai khi dung phone nhung sai mat khau.")
