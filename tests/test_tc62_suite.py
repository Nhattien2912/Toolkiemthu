from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from random import randint

import pytest
from selenium.webdriver.common.by import By

from config import API_BASE_URL, BASE_URL
from pages.account_page import AccountPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from utils.account_api import create_authenticated_account
from utils.project_doc_data import TEST_CASE_GROUPS
from utils.store_api import seed_cart_with_featured_product


SOURCE_PROJECT_ROOT = Path(r"C:\Users\clubb\Desktop\WEB-MERN_t10-2024")


def _read_source(relative_path: str) -> str:
    path = SOURCE_PROJECT_ROOT / relative_path
    assert path.exists(), f"Missing source file: {path}"
    return path.read_text(encoding="utf-8", errors="replace")


APP_SOURCE = _read_source("frontend/src/App.js")
HEADER_SOURCE = _read_source("frontend/src/Components/Header/index.js")
SIGN_IN_SOURCE = _read_source("frontend/src/Pages/AuthSignIn/index.js")
SIGN_UP_SOURCE = _read_source("frontend/src/Pages/AuthSignUp/index.js")
MY_ACCOUNT_SOURCE = _read_source("frontend/src/Pages/MyAccount/MyAccount.jsx")
PRODUCT_DETAILS_SOURCE = _read_source("frontend/src/Pages/ProductDetails/index.js")
QUANTITY_BOX_SOURCE = _read_source("frontend/src/Components/QuantityBox/index.js")
CHECKOUT_SOURCE = _read_source("frontend/src/Pages/Checkout/index.js")
VOUCHER_COMPONENT_SOURCE = _read_source("frontend/src/Components/Voucher/index.js")
USER_ROUTES_SOURCE = _read_source("server/routes/userRoutes.js")
CART_ROUTES_SOURCE = _read_source("server/routes/cartRoutes.js")
ORDER_ROUTES_SOURCE = _read_source("server/routes/orderRoutes.js")
VOUCHER_ROUTES_SOURCE = _read_source("server/routes/voucherRoutes.js")
AUTH_HELPERS_SOURCE = _read_source("server/helper/authHelpers.js")
USER_MODEL_SOURCE = _read_source("server/models/UserModel.js")


_GROUP_CASES = {group["group_id"]: group["cases"] for group in TEST_CASE_GROUPS}
REGISTER_CASES = _GROUP_CASES["register"]
LOGIN_CASES = _GROUP_CASES["login"]
PASSWORD_CASES = _GROUP_CASES["password"]
CART_CASES = _GROUP_CASES["cart"]
CHECKOUT_CASES = _GROUP_CASES["checkout"]


def _api_json(method: str, path: str, payload: dict | None = None, token: str | None = None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        url=f"{API_BASE_URL}{path}",
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw_body = response.read().decode("utf-8", errors="replace")
            try:
                body = json.loads(raw_body) if raw_body else {}
            except json.JSONDecodeError:
                body = {"raw": raw_body}
            return response.status, body
    except urllib.error.HTTPError as error:
        raw_body = error.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            body = {"raw": raw_body}
        return error.code, body


def _api_signup(payload: dict):
    return _api_json("POST", "/api/user/signup", payload=payload)


def _api_signin(username_or_phone: str, password: str):
    return _api_json(
        "POST",
        "/api/user/signin",
        payload={"usernameOrPhone": username_or_phone, "password": password},
    )


def _api_change_password(user_id: str, current_password: str | None, new_password: str | None, token: str | None = None):
    payload = {}
    if current_password is not None:
        payload["currentPassword"] = current_password
    if new_password is not None:
        payload["newPassword"] = new_password
    return _api_json("PUT", f"/api/user/change-password/{user_id}", payload=payload, token=token)


def _api_get_cart(user_id: str, token: str):
    return _api_json("GET", f"/api/cart/getCart/{user_id}", token=token)


def _api_add_cart(payload: dict, token: str):
    return _api_json("POST", "/api/cart/addCart", payload=payload, token=token)


def _api_update_cart(payload: dict, token: str):
    return _api_json("PUT", "/api/cart/updateCart", payload=payload, token=token)


def _api_remove_cart(user_id: str, product_id: str, token: str):
    return _api_json("DELETE", f"/api/cart/removeCart/{user_id}", payload={"productId": product_id}, token=token)


def _api_apply_voucher(payload: dict, token: str):
    return _api_json("POST", "/api/voucher/apply", payload=payload, token=token)


def _api_create_order(payload: dict, token: str):
    return _api_json("POST", "/api/order/create", payload=payload, token=token)


def _build_signup_payload(**overrides) -> dict:
    unique = f"{int(time.time())}{randint(100, 999)}"[-8:]
    payload = {
        "username": f"tc62reg{unique}",
        "phone": f"09{unique}",
        "fullName": "TC62 Selenium User",
        "password": "Abcd123@",
        "confirmPassword": "Abcd123@",
    }
    payload.update(overrides)
    return payload


def _create_raw_test_account():
    payload = _build_signup_payload()
    status, body = _api_signup(payload)
    assert status in (200, 201), f"Unable to create test account: status={status}, body={body}"
    return payload, body


def _load_authenticated_storage(driver, authenticated_account, checkout_data_json: str | None = None):
    driver.get(BASE_URL)
    driver.execute_script(
        """
        sessionStorage.setItem('token', arguments[0]);
        sessionStorage.setItem('user', arguments[1]);
        if (arguments[2]) {
            localStorage.setItem('checkoutData', arguments[2]);
        } else {
            localStorage.removeItem('checkoutData');
        }
        """,
        authenticated_account.token,
        authenticated_account.storage_user_json,
        checkout_data_json,
    )
    driver.refresh()


def _extract_block(source: str, anchor: str) -> str:
    start = source.find(anchor)
    assert start != -1, f"Anchor not found: {anchor}"
    brace_start = source.find("{", start)
    assert brace_start != -1, f"Opening brace not found for anchor: {anchor}"
    depth = 0
    for index in range(brace_start, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[brace_start:index + 1]
    raise AssertionError(f"Closing brace not found for anchor: {anchor}")


def _build_order_payload(user_id: str, cart: dict, payment_method: str = "COD") -> dict:
    return {
        "fullName": "TC62 Checkout User",
        "phone": "0912345678",
        "detail": "123 Test Street",
        "notes": "tc62 order",
        "paymentMethod": payment_method,
        "userId": user_id,
        "items": cart["items"],
        "isVoucher": False,
        "voucherCode": "",
        "discountPercentage": 0,
        "appliedDate": "",
        "province": "Ho Chi Minh",
        "provinceCode": "79",
        "district": "Thu Duc",
        "districtCode": "769",
        "ward": "Linh Trung",
        "wardCode": "27154",
        "date": "2026-04-15",
        "totalPrice": cart["totalPrice"],
    }


def _seed_cart_api():
    authenticated_account = create_authenticated_account()
    seeded_cart = seed_cart_with_featured_product(authenticated_account)
    status, cart = _api_get_cart(authenticated_account.user_id, authenticated_account.token)
    assert status == 200, f"Unable to load seeded cart: status={status}, body={cart}"
    return authenticated_account, seeded_cart, cart


def _assert_contains(text: str, needle: str, message: str) -> None:
    assert needle in text, message


def _assert_regex(text: str, pattern: str, message: str) -> None:
    assert re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL), message


def _open_register_form(driver, step_logger):
    login_page = LoginPage(driver)
    step_logger("Mo trang chu, vao Dang Nhap va chuyen sang form Dang Ky.")
    login_page.open()
    login_page.go_to_signup()
    return login_page


def _get_register_feedback(driver, login_page) -> str:
    parts = [login_page.get_alert_text(), login_page.get_body_text()]
    return "\n".join(part for part in parts if part).strip()


def _assert_registration_blocked(driver, login_page, expected_keywords: list[str], message: str) -> None:
    current_url = driver.current_url.lower()
    feedback = _get_register_feedback(driver, login_page).lower()
    invalid_fields = driver.execute_script(
        """
        return Array.from(document.querySelectorAll('input, textarea, select'))
          .filter((element) => {
            try {
              return typeof element.matches === 'function' && element.matches(':invalid');
            } catch (error) {
              return false;
            }
          })
          .map((element) => element.name || element.type || element.placeholder || element.id || 'field');
        """
    )
    has_expected_feedback = any(keyword.lower() in feedback for keyword in expected_keywords)
    stayed_on_auth_flow = "/signin" in current_url or "/signup" in current_url
    assert stayed_on_auth_flow or has_expected_feedback or bool(invalid_fields), (
        f"{message} | url={driver.current_url} | feedback={feedback[:400]} | invalid_fields={invalid_fields}"
    )


def _require_signup_email_input(login_page, case_code: str):
    email_input = login_page.find_visible_signup_email_input()
    assert email_input is not None, (
        f"{case_code} yeu cau truong Email tren form dang ky, nhung giao dien hien tai khong co input Email."
    )
    return email_input


def _enter_wrong_otp_if_present(login_page, value: str = "000000") -> bool:
    otp_inputs = login_page.get_visible_otp_inputs()
    if not otp_inputs:
        return False

    if len(otp_inputs) == 1:
        otp_inputs[0].clear()
        otp_inputs[0].send_keys(value)
        return True

    digits = list(value)
    for index, otp_input in enumerate(otp_inputs):
        otp_input.clear()
        otp_input.send_keys(digits[index] if index < len(digits) else "0")
    return True


@pytest.mark.parametrize("case", REGISTER_CASES, ids=lambda case: case["code"])
def test_tc62_register(case, driver, step_logger):
    step_logger(f"{case['code']} - {case['scenario']}")
    code = case["code"]

    if code == "REG_01":
        login_page = _open_register_form(driver, step_logger)
        step_logger("Kiem tra form co du truong Ten, Email, SDT, Mat khau va Xac nhan mat khau.")
        _require_signup_email_input(login_page, code)
        payload = _build_signup_payload()
        step_logger("Nhap du lieu hop le va gui form dang ky.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
            email=f"{payload['username']}@mail.test",
        )
        login_page.click_signup_submit()
        step_logger("Xac nhan dang ky thanh cong hoac hien buoc OTP.")
        success_feedback = _get_register_feedback(driver, login_page).lower()
        assert driver.current_url.lower().endswith("/signin") or "thanh cong" in success_feedback or bool(login_page.get_visible_otp_inputs()), (
            f"REG_01 yeu cau dang ky thanh cong hoac hien OTP. url={driver.current_url}, feedback={success_feedback[:400]}"
        )
        return

    if code == "REG_02":
        login_page = _open_register_form(driver, step_logger)
        step_logger("De trong tat ca truong va bam Dang Ky.")
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["vui long", "bat buoc", "required"],
            "REG_02 mong doi validation bat buoc xuat hien tren form dang ky",
        )
        return

    if code == "REG_03":
        login_page = _open_register_form(driver, step_logger)
        email_input = _require_signup_email_input(login_page, code)
        payload = _build_signup_payload()
        payload["email"] = "existing.user@mail.test"
        step_logger("Nhap email da ton tai trong he thong va gui form.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
            email=payload["email"],
        )
        assert email_input.get_attribute("value") == payload["email"]
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["email", "ton tai", "su dung"],
            "REG_03 mong doi duplicate email bi chan",
        )
        return

    if code == "REG_04":
        base_payload, _ = _create_raw_test_account()
        login_page = _open_register_form(driver, step_logger)
        payload = _build_signup_payload(phone=base_payload["phone"])
        step_logger("Nhap SDT da ton tai va gui form.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
        )
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["dien thoai", "ton tai"],
            "REG_04 mong doi SDT da ton tai bi chan",
        )
        return

    if code == "REG_05":
        login_page = _open_register_form(driver, step_logger)
        email_input = _require_signup_email_input(login_page, code)
        payload = _build_signup_payload()
        step_logger("Nhap email sai dinh dang test@.com va gui form.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
            email="test@.com",
        )
        assert email_input.get_attribute("value") == "test@.com"
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["email", "khong hop le", "invalid"],
            "REG_05 mong doi email sai dinh dang bi chan",
        )
        return

    if code == "REG_06":
        login_page = _open_register_form(driver, step_logger)
        payload = _build_signup_payload(phone="0901abc123")
        step_logger("Nhap SDT chua chu cai va quan sat field / validation.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
        )
        actual_phone_value = driver.find_element(By.NAME, "phone").get_attribute("value")
        if actual_phone_value != payload["phone"]:
            assert actual_phone_value.isdigit() or actual_phone_value == ""
            return
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["dien thoai", "khong hop le", "so"],
            "REG_06 mong doi SDT co chu cai bi chan",
        )
        return

    if code == "REG_07":
        login_page = _open_register_form(driver, step_logger)
        payload = _build_signup_payload(phone="09012345")
        step_logger("Nhap SDT ngan 8 so va gui form.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
        )
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["dien thoai", "10", "khong hop le"],
            "REG_07 mong doi SDT ngan bi chan",
        )
        return

    if code == "REG_08":
        login_page = _open_register_form(driver, step_logger)
        payload = _build_signup_payload(password="12345", confirmPassword="12345")
        step_logger("Nhap mat khau ngan 5 ky tu va gui form.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
        )
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["mat khau", "8", "khong hop le"],
            "REG_08 mong doi mat khau ngan bi chan",
        )
        return

    if code == "REG_09":
        login_page = _open_register_form(driver, step_logger)
        payload = _build_signup_payload()
        step_logger("Nhap password va confirm password khong khop.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password="Abc@1234",
            confirm_password="Abc@5678",
        )
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["xac nhan", "khop", "mat khau"],
            "REG_09 mong doi confirm password mismatch bi chan",
        )
        return

    if code == "REG_10":
        login_page = _open_register_form(driver, step_logger)
        payload = _build_signup_payload()
        step_logger("Gui form dang ky hop le de kiem tra buoc OTP.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
        )
        login_page.click_signup_submit()
        step_logger("Tim input OTP va thu nhap ma sai.")
        entered = _enter_wrong_otp_if_present(login_page, "999999")
        assert entered, (
            "REG_10 yeu cau co buoc OTP de test ma sai, nhung giao dien dang ky hien tai khong hien input OTP."
        )
        _assert_registration_blocked(
            driver,
            login_page,
            ["otp", "xac thuc", "khong hop le"],
            "REG_10 mong doi OTP sai bi chan",
        )
        return

    if code == "REG_11":
        login_page = _open_register_form(driver, step_logger)
        payload = _build_signup_payload()
        step_logger("Gui form dang ky hop le va kiem tra thong tin OTP het han / gui lai.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
        )
        login_page.click_signup_submit()
        body_text = login_page.get_body_text().lower()
        has_otp = bool(login_page.get_visible_otp_inputs())
        has_expiry_hint = any(token in body_text for token in ["otp", "het han", "gui lai", "resend", "countdown"])
        assert has_otp and has_expiry_hint, (
            "REG_11 yeu cau co co che OTP het han / gui lai, nhung giao dien hien tai khong cung cap."
        )
        return

    if code == "REG_12":
        login_page = _open_register_form(driver, step_logger)
        payload = _build_signup_payload(username="' OR 1=1 --")
        step_logger("Nhap payload SQL Injection vao username va gui form dang ky.")
        login_page.fill_signup_form(
            username=payload["username"],
            phone=payload["phone"],
            full_name=payload["fullName"],
            password=payload["password"],
            confirm_password=payload["confirmPassword"],
        )
        login_page.click_signup_submit()
        _assert_registration_blocked(
            driver,
            login_page,
            ["ky tu", "khong hop le", "invalid", "username"],
            "REG_12 mong doi he thong chan payload SQLi o username",
        )
        return

    if code == "REG_13":
        _assert_regex(
            USER_ROUTES_SOURCE + SIGN_UP_SOURCE,
            r"username\.trim\(\)|phone\.trim\(\)|fullName\.trim\(\)",
            "REG_13 expects signup input to be trimmed before validation/storage.",
        )
        return

    if code == "REG_14":
        _assert_regex(
            USER_ROUTES_SOURCE + SIGN_UP_SOURCE,
            r"username[^;\n]*(length|minLength)|minLength[^;\n]*username",
            "REG_14 expects a minimum username length validation.",
        )
        return

    if code == "REG_15":
        payload = _build_signup_payload(password="Abcd1234", confirmPassword="Abcd1234")
        status, body = _api_signup(payload)
        assert status == 400, f"REG_15 expects password without special char to be rejected, got status={status}, body={body}"
        return

    if code == "REG_16":
        payload = _build_signup_payload(fullName="<script>alert(1)</script>")
        status, body = _api_signup(payload)
        serialized_body = json.dumps(body, ensure_ascii=False).lower()
        assert status == 400 or "<script>" not in serialized_body, (
            f"REG_16 expects XSS fullName to be rejected or escaped, got status={status}, body={body}"
        )
        return

    if code == "REG_17":
        signup_source = SIGN_UP_SOURCE + USER_ROUTES_SOURCE
        assert ".trim()" in signup_source and ".toLowerCase()" in signup_source, (
            "REG_17 expects email/username input to be trimmed and lowercased before duplicate checks."
        )
        return

    if code == "REG_18":
        _assert_regex(
            USER_ROUTES_SOURCE + SIGN_UP_SOURCE,
            r"isValidPhone|/\\^\\[0-9\\]|replace\\(/\\D|type=[\"']tel[\"']",
            "REG_18 expects phone input to accept digits only or backend phone validation.",
        )
        return

    if code == "REG_19":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r"password\.length\s*<=|maxLength|128",
            "REG_19 expects an upper boundary for very long passwords.",
        )
        return

    if code == "REG_20":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r"username.*toLowerCase|collation|caseInsensitive",
            "REG_20 expects case-insensitive duplicate username detection.",
        )
        return

    if code == "REG_21":
        assert any(token in SIGN_UP_SOURCE for token in ("isLoading", "loading", "disabled", "setSubmitting")), (
            "REG_21 expects signup submit button to guard duplicate submissions."
        )
        return

    if code == "REG_22":
        payload = _build_signup_payload()
        status, body = _api_signup(payload)
        serialized_body = json.dumps(body, ensure_ascii=False).lower()
        assert status in (200, 201) and "password" not in serialized_body
        return

    if code == "REG_23":
        payload = _build_signup_payload()
        status, body = _api_signup(payload)
        user = body.get("user", {}) if isinstance(body, dict) else {}
        assert status in (200, 201) and user.get("isActive", True) is True
        return

    if code == "REG_24":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r"catch\s*\(error\)[\s\S]*handleError\(res,\s*error\)",
            "REG_24 expects signup route to pass server errors through handleError.",
        )
        return

    raise AssertionError(f"Unhandled register case: {code}")


@pytest.mark.parametrize("case", LOGIN_CASES, ids=lambda case: case["code"])
def test_tc62_login(case, request):
    step_logger = request.getfixturevalue("step_logger")
    step_logger(f"{case['code']} - {case['scenario']}")
    code = case["code"]

    if code == "LOG_01":
        payload, body = _create_raw_test_account()
        email = body.get("user", {}).get("email")
        assert email, "LOG_01 requires a created email value to test email login."
        status, signin_body = _api_signin(email, payload["password"])
        assert status == 200 and signin_body.get("success") is True, (
            f"LOG_01 expects email login support, but got status={status}, body={signin_body}"
        )
        return

    if code == "LOG_02":
        authenticated_account = create_authenticated_account()
        driver = request.getfixturevalue("driver")
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(authenticated_account.phone, authenticated_account.password)
        assert "thành công" in login_page.get_message().lower()
        return

    if code == "LOG_03":
        driver = request.getfixturevalue("driver")
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("", "")
        body_text = login_page.get_body_text().lower()
        assert "nhập" in body_text or login_page.get_alert_text()
        return

    if code == "LOG_04":
        authenticated_account = create_authenticated_account()
        status, body = _api_signin(authenticated_account.username, "WrongPass@123")
        assert status == 400 and "không đúng" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "LOG_05":
        assert "google" in SIGN_IN_SOURCE.lower() or "oauth" in SIGN_IN_SOURCE.lower(), (
            "LOG_05 expects Google OAuth login control/integration on sign-in page."
        )
        return

    if code == "LOG_06":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r'router\.post\("/signin",\s*authLimiter',
            "LOG_06 expects repeated-login protection on /signin via authLimiter or equivalent.",
        )
        return

    if code == "LOG_07":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r'if\s*\(!user\.isActive\)\s*{[^}]*403[^}]*vô hiệu hóa',
            "LOG_07 expects inactive accounts to be rejected with 403.",
        )
        return

    if code == "LOG_08":
        assert "rememberMe" in SIGN_IN_SOURCE and "localStorage.setItem" in SIGN_IN_SOURCE, (
            "LOG_08 expects a Remember Me control that persists login across browser restarts."
        )
        return

    if code == "LOG_09":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r'user\.role\s*!==\s*"admin"',
            "LOG_09 expects explicit admin authorization guard for admin access.",
        )
        return

    if code == "LOG_10":
        assert 'path="/my-account"' not in APP_SOURCE or "ProtectedRoute" in APP_SOURCE, (
            "LOG_10 expects private pages to be protected after logout/back navigation, but /my-account is exposed directly."
        )
        return

    if code == "LOG_11":
        authenticated_account = create_authenticated_account()
        wrong_case_password = authenticated_account.password.lower()
        status, body = _api_signin(authenticated_account.username, wrong_case_password)
        assert status == 400 and "không đúng" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "LOG_12":
        _assert_regex(
            SIGN_IN_SOURCE,
            r"postData\([^)]*usernameOrPhone\.trim\(\)",
            "LOG_12 expects username/email input to be trimmed before submitting login request.",
        )
        return

    if code == "LOG_13":
        status, body = _api_signin("missing_user_001", "Abcd123@")
        assert "không tồn tại" in json.dumps(body, ensure_ascii=False).lower(), (
            f"LOG_13 expects explicit account-not-found message, got status={status}, body={body}"
        )
        return

    if code == "LOG_14":
        _assert_regex(
            SIGN_IN_SOURCE,
            r"sessionStorage\.setItem\([^)]*token",
            "LOG_14 expects non-remember login to store token in sessionStorage.",
        )
        assert "localStorage.setItem" not in SIGN_IN_SOURCE or "remember" in SIGN_IN_SOURCE.lower(), (
            "LOG_14 expects localStorage token persistence only when Remember me is enabled."
        )
        return

    if code == "LOG_15":
        logout_source = HEADER_SOURCE + APP_SOURCE + SIGN_IN_SOURCE
        assert "sessionStorage.clear()" in logout_source and "localStorage.clear()" in logout_source, (
            "LOG_15 expects logout to clear both sessionStorage and localStorage."
        )
        return

    if code == "LOG_16":
        _assert_regex(
            SIGN_IN_SOURCE,
            r'type=["\']password["\']',
            "LOG_16 expects password input to use type=password.",
        )
        assert "autoComplete=\"current-password\"" in SIGN_IN_SOURCE or "autocomplete=\"current-password\"" in SIGN_IN_SOURCE.lower(), (
            "LOG_16 expects password input autocomplete to be current-password."
        )
        return

    if code == "LOG_17":
        status, body = _api_signin("", "Abcd123@")
        assert status == 400 and "bắt buộc" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "LOG_18":
        status, body = _api_signin("some_user", "")
        assert status == 400 and "mật khẩu" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "LOG_19":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r"isPhone[\s\S]*phone:\s*usernameOrPhone",
            "LOG_19 expects signin to query by phone when usernameOrPhone is numeric.",
        )
        return

    if code == "LOG_20":
        authenticated_account = create_authenticated_account()
        status, body = _api_signin(authenticated_account.username, authenticated_account.password)
        serialized = json.dumps(body, ensure_ascii=False).lower()
        assert status == 200 and "password" not in serialized
        return

    if code == "LOG_21":
        _assert_regex(AUTH_HELPERS_SOURCE, r"httpOnly\s*:\s*true", "LOG_21 expects auth cookie to be httpOnly.")
        _assert_regex(AUTH_HELPERS_SOURCE, r"sameSite", "LOG_21 expects auth cookie to define sameSite.")
        return

    if code == "LOG_22":
        _assert_regex(
            USER_ROUTES_SOURCE + APP_SOURCE,
            r"requireAuth|authMiddleware|verifyToken|user\.role\s*!==\s*[\"']admin[\"']",
            "LOG_22 expects admin routes to require auth and role guard.",
        )
        return

    if code == "LOG_23":
        assert "Tên đăng nhập, số điện thoại hoặc mật khẩu không đúng" in USER_ROUTES_SOURCE, (
            "LOG_23 expects a generic credential error message."
        )
        return

    if code == "LOG_24":
        logout_source = HEADER_SOURCE + APP_SOURCE
        assert "localStorage.clear()" in logout_source and "sessionStorage.clear()" in logout_source, (
            "LOG_24 expects logout to clear localStorage and sessionStorage."
        )
        return

    raise AssertionError(f"Unhandled login case: {code}")


@pytest.mark.parametrize("case", PASSWORD_CASES, ids=lambda case: case["code"])
def test_tc62_password(case, request):
    step_logger = request.getfixturevalue("step_logger")
    step_logger(f"{case['code']} - {case['scenario']}")
    code = case["code"]

    if code == "PWD_01":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(
            authenticated_account.user_id,
            authenticated_account.password,
            "Xyzc123@",
            authenticated_account.token,
        )
        assert status == 200 and body.get("success") is True
        return

    if code == "PWD_02":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(authenticated_account.user_id, None, None, authenticated_account.token)
        assert status == 400 and "bắt buộc" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "PWD_03":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(
            authenticated_account.user_id,
            "WrongCurrent@123",
            "Xyzc123@",
            authenticated_account.token,
        )
        assert status == 400 and "hiện tại" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "PWD_04":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(
            authenticated_account.user_id,
            authenticated_account.password,
            authenticated_account.password,
            authenticated_account.token,
        )
        assert status == 400, f"PWD_04 expects reject same password, got status={status}, body={body}"
        return

    if code == "PWD_05":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(
            authenticated_account.user_id,
            authenticated_account.password,
            "Abc12@",
            authenticated_account.token,
        )
        assert status == 400, f"PWD_05 expects short-password rejection, got status={status}, body={body}"
        return

    if code == "PWD_06":
        assert "confirmPassword" in MY_ACCOUNT_SOURCE and "confirm" in USER_ROUTES_SOURCE.lower(), (
            "PWD_06 expects confirm-new-password field and matching validation in change-password flow."
        )
        return

    if code == "PWD_07":
        assert any(token in MY_ACCOUNT_SOURCE for token in ("Visibility", "VisibilityOff", 'type="text"', "showPassword")), (
            "PWD_07 expects an eye icon / password visibility toggle on change-password inputs."
        )
        return

    if code == "PWD_08":
        _assert_regex(
            MY_ACCOUNT_SOURCE,
            r"localStorage\.clear\(\).*sessionStorage\.clear\(\).*navigate\(\"/signIn\"\)",
            "PWD_08 expects auto logout and redirect to sign-in after successful password change.",
        )
        return

    if code == "PWD_09":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(
            authenticated_account.user_id,
            authenticated_account.password,
            "Xyzc123@",
            authenticated_account.token,
        )
        assert status == 200, f"PWD_09 setup failed: {status}, {body}"
        old_status, old_body = _api_signin(authenticated_account.username, authenticated_account.password)
        assert old_status == 400 and "không đúng" in json.dumps(old_body, ensure_ascii=False).lower()
        return

    if code == "PWD_10":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(authenticated_account.user_id, authenticated_account.password, "Xyzc123@", None)
        assert status in (401, 403), f"PWD_10 expects unauthorized without token, got status={status}, body={body}"
        return

    if code == "PWD_11":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(
            authenticated_account.user_id,
            authenticated_account.password,
            "abcdefgh",
            authenticated_account.token,
        )
        assert status == 400, f"PWD_11 expects weak new password rejection, got status={status}, body={body}"
        return

    if code == "PWD_12":
        account_a = create_authenticated_account()
        account_b = create_authenticated_account()
        status, body = _api_change_password(account_b.user_id, account_b.password, "Xyzc123@", account_a.token)
        assert status in (401, 403), (
            f"PWD_12 expects user A cannot change user B password, got status={status}, body={body}"
        )
        return

    if code == "PWD_13":
        assert any(token in MY_ACCOUNT_SOURCE for token in ("isLoading", "loading", "disabled", "setSubmitting")), (
            "PWD_13 expects change-password submit button to guard double submit with loading/disabled state."
        )
        return

    if code == "PWD_14":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(authenticated_account.user_id, None, "Xyzc123@", authenticated_account.token)
        assert status == 400 and "hiện tại" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "PWD_15":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(authenticated_account.user_id, authenticated_account.password, None, authenticated_account.token)
        assert status == 400 and "mật khẩu" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "PWD_16":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r"hashPassword|bcrypt\.hash",
            "PWD_16 expects new password to be hashed before updating the database.",
        )
        return

    if code == "PWD_17":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(
            authenticated_account.user_id,
            authenticated_account.password,
            "Xyzc123@",
            authenticated_account.token,
        )
        serialized = json.dumps(body, ensure_ascii=False).lower()
        assert status == 200 and "password" not in serialized
        return

    if code == "PWD_18":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r"change-password[\s\S]*(requireAuth|authMiddleware|verifyToken)",
            "PWD_18 expects change-password route to require token/auth middleware.",
        )
        return

    if code == "PWD_19":
        _assert_regex(
            USER_ROUTES_SOURCE,
            r"change-password[\s\S]*isValidPassword|isValidPassword[\s\S]*change-password",
            "PWD_19 expects change-password to reuse password policy validation.",
        )
        return

    if code == "PWD_20":
        authenticated_account = create_authenticated_account()
        status, body = _api_change_password(
            "000000000000000000000000",
            authenticated_account.password,
            "Xyzc123@",
            authenticated_account.token,
        )
        assert status in (400, 404), f"PWD_20 expects clean not-found response, got status={status}, body={body}"
        return

    raise AssertionError(f"Unhandled password case: {code}")


@pytest.mark.parametrize("case", CART_CASES, ids=lambda case: case["code"])
def test_tc62_cart(case, request):
    step_logger = request.getfixturevalue("step_logger")
    step_logger(f"{case['code']} - {case['scenario']}")
    code = case["code"]

    if code == "CRT_01":
        authenticated_account, seeded_cart, cart = _seed_cart_api()
        assert cart.get("items"), "CRT_01 expects cart to contain newly added product."
        return

    if code == "CRT_02":
        authenticated_account = create_authenticated_account()
        featured_product = seed_cart_with_featured_product(authenticated_account)
        payload = {
            "userId": authenticated_account.user_id,
            "productId": featured_product.product_id,
            "quantity": 1,
            "size": "",
            "color": "",
        }
        status, body = _api_add_cart(payload, authenticated_account.token)
        assert status == 400 and "size" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CRT_03":
        assert "stock" in CART_ROUTES_SOURCE.lower() or "maxQuantity" in CART_ROUTES_SOURCE, (
            "CRT_03 expects add-to-cart flow to validate quantity against stock before saving cart."
        )
        return

    if code == "CRT_04":
        _assert_regex(
            CART_ROUTES_SOURCE,
            r"quantity\s*<=\s*0|quantity\s*<\s*1|Math\.max\(1",
            "CRT_04 expects quantity 0 or negative values to be blocked or normalized to 1.",
        )
        return

    if code == "CRT_05":
        authenticated_account = create_authenticated_account()
        seeded_cart = seed_cart_with_featured_product(authenticated_account)
        payload = {
            "userId": authenticated_account.user_id,
            "productId": seeded_cart.product_id,
            "quantity": 1,
            "size": seeded_cart.size,
            "color": seeded_cart.color,
        }
        status, body = _api_add_cart(payload, authenticated_account.token)
        assert status == 200, f"CRT_05 setup addCart failed: {status}, {body}"
        cart_status, cart = _api_get_cart(authenticated_account.user_id, authenticated_account.token)
        assert cart_status == 200
        matching_items = [item for item in cart["items"] if item["productId"]["_id"] == seeded_cart.product_id]
        assert len(matching_items) == 1 and matching_items[0]["quantity"] == 2
        return

    if code == "CRT_06":
        _assert_regex(
            CART_ROUTES_SOURCE,
            r"item\.size\s*===\s*size.*item\.color\s*===\s*color|item\.color\s*===\s*color.*item\.size\s*===\s*size",
            "CRT_06 expects different size/color variants to be separated in cart identity.",
        )
        return

    if code == "CRT_07":
        authenticated_account = create_authenticated_account()
        seeded_cart = seed_cart_with_featured_product(authenticated_account)
        payload = {
            "userId": authenticated_account.user_id,
            "productId": seeded_cart.product_id,
            "quantity": 2,
            "size": seeded_cart.size,
            "color": seeded_cart.color,
        }
        status, body = _api_update_cart(payload, authenticated_account.token)
        assert status == 200 and body.get("cart", {}).get("items", [{}])[0].get("quantity") == 2
        return

    if code == "CRT_08":
        assert "stock" in CART_ROUTES_SOURCE.lower(), (
            "CRT_08 expects updateCart to validate quantity against available stock."
        )
        return

    if code == "CRT_09":
        _assert_regex(
            QUANTITY_BOX_SOURCE,
            r'type="text".*readOnly',
            "CRT_09 expects quantity input to block free-text typing and accept only controlled numeric updates.",
        )
        return

    if code == "CRT_10":
        authenticated_account = create_authenticated_account()
        seeded_cart = seed_cart_with_featured_product(authenticated_account)
        status, _ = _api_remove_cart(authenticated_account.user_id, seeded_cart.product_id, authenticated_account.token)
        assert status == 200, f"CRT_10 removeCart failed with status={status}"
        return

    if code == "CRT_11":
        assert "localStorage.getItem(\"token\") || sessionStorage.getItem(\"token\")" not in PRODUCT_DETAILS_SOURCE, (
            "CRT_11 expects guest users to add items into a session cart without requiring auth token."
        )
        return

    if code == "CRT_12":
        _assert_regex(
            APP_SOURCE + CART_ROUTES_SOURCE,
            r"merge.*cart|session.*cart.*merge|guest.*cart.*merge",
            "CRT_12 expects guest cart to merge into user cart after login.",
        )
        return

    if code == "CRT_13":
        assert "context.setAlertBox" in PRODUCT_DETAILS_SOURCE and "catch" in PRODUCT_DETAILS_SOURCE and "message" in PRODUCT_DETAILS_SOURCE.split("catch", 1)[1], (
            "CRT_13 expects add-to-cart network failures to show a user-visible connection error."
        )
        return

    if code == "CRT_14":
        _assert_regex(
            CART_ROUTES_SOURCE,
            r"removeCart[\s\S]*(size|color)|(size|color)[\s\S]*removeCart",
            "CRT_14 expects remove/update cart identity to include size and color, not only productId.",
        )
        return

    if code == "CRT_15":
        assert not re.search(r"const\s*{[^}]*totalPrice[^}]*}\s*=\s*req\.body", CART_ROUTES_SOURCE, flags=re.DOTALL), (
            "CRT_15 expects cart total to be recalculated server-side, not accepted from req.body."
        )
        _assert_regex(
            CART_ROUTES_SOURCE,
            r"reduce\(|totalPrice\s*=|subtotal|price\s*\*",
            "CRT_15 expects cart route to calculate totals from item price and quantity.",
        )
        return

    if code == "CRT_16":
        account_a = create_authenticated_account()
        account_b = create_authenticated_account()
        seed_cart_with_featured_product(account_b)
        status, body = _api_get_cart(account_b.user_id, account_a.token)
        assert status in (401, 403), (
            f"CRT_16 expects user A cannot read user B cart, got status={status}, body={body}"
        )
        return

    if code == "CRT_17":
        authenticated_account = create_authenticated_account()
        featured_product = seed_cart_with_featured_product(authenticated_account)
        payload = {
            "userId": authenticated_account.user_id,
            "productId": featured_product.product_id,
            "quantity": 1,
            "size": featured_product.size,
            "color": featured_product.color,
        }
        status, body = _api_add_cart(payload, None)
        assert status in (401, 403), f"CRT_17 expects addCart without token to be rejected, got {status}, {body}"
        return

    if code == "CRT_18":
        authenticated_account = create_authenticated_account()
        payload = {"userId": authenticated_account.user_id, "quantity": 1, "size": "40", "color": "Black"}
        status, body = _api_add_cart(payload, authenticated_account.token)
        assert status == 400 and "product" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CRT_19":
        authenticated_account = create_authenticated_account()
        featured_product = seed_cart_with_featured_product(authenticated_account)
        payload = {
            "userId": authenticated_account.user_id,
            "productId": featured_product.product_id,
            "quantity": 1,
            "color": featured_product.color,
        }
        status, body = _api_add_cart(payload, authenticated_account.token)
        assert status == 400 and "size" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CRT_20":
        authenticated_account = create_authenticated_account()
        featured_product = seed_cart_with_featured_product(authenticated_account)
        payload = {
            "userId": authenticated_account.user_id,
            "productId": featured_product.product_id,
            "quantity": 1,
            "size": featured_product.size,
        }
        status, body = _api_add_cart(payload, authenticated_account.token)
        assert status == 400 and "color" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CRT_21":
        _assert_regex(
            CART_ROUTES_SOURCE,
            r"Number\.isInteger|parseInt|quantity\s*%\s*1|integer",
            "CRT_21 expects cart quantity to be validated as an integer.",
        )
        return

    if code == "CRT_22":
        _assert_regex(
            CART_ROUTES_SOURCE,
            r"removeCart[\s\S]*(reduce|totalPrice|subtotal|price\s*\*)",
            "CRT_22 expects removeCart to recalculate total after deleting an item.",
        )
        return

    if code == "CRT_23":
        _assert_regex(
            CART_ROUTES_SOURCE,
            r"req\.user\._id|req\.user\.id|userId\s*!==\s*req\.user",
            "CRT_23 expects cart routes to compare URL/body userId with authenticated user id.",
        )
        return

    if code == "CRT_24":
        authenticated_account = create_authenticated_account()
        seeded_cart = seed_cart_with_featured_product(authenticated_account)
        payload = {
            "userId": authenticated_account.user_id,
            "productId": seeded_cart.product_id,
            "quantity": 1,
            "size": seeded_cart.size,
            "color": seeded_cart.color,
        }
        status, body = _api_add_cart(payload, authenticated_account.token)
        assert status == 200, f"CRT_24 duplicate addCart failed: {status}, {body}"
        cart_status, cart = _api_get_cart(authenticated_account.user_id, authenticated_account.token)
        items = [item for item in cart.get("items", []) if item.get("productId", {}).get("_id") == seeded_cart.product_id]
        assert cart_status == 200 and len(items) == 1
        return

    raise AssertionError(f"Unhandled cart case: {code}")


@pytest.mark.parametrize("case", CHECKOUT_CASES, ids=lambda case: case["code"])
def test_tc62_checkout(case, request):
    step_logger = request.getfixturevalue("step_logger")
    step_logger(f"{case['code']} - {case['scenario']}")
    code = case["code"]

    if code == "CHK_01":
        authenticated_account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(authenticated_account.user_id, cart, "COD"), authenticated_account.token)
        assert status == 201 and body.get("status") is True
        return

    if code == "CHK_02":
        assert "path=\"/checkout\"" not in APP_SOURCE or "ProtectedRoute" in APP_SOURCE, (
            "CHK_02 expects checkout route to redirect when cart is empty, but route is exposed directly."
        )
        return

    if code == "CHK_03":
        authenticated_account, _, cart = _seed_cart_api()
        payload = _build_order_payload(authenticated_account.user_id, cart, "COD")
        payload["phone"] = ""
        status, body = _api_create_order(payload, authenticated_account.token)
        assert status == 400 and "vui lòng" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CHK_04":
        assert any(token in CHECKOUT_SOURCE.lower() for token in ("vnpay", "momo")), (
            "CHK_04 expects real online-payment gateway integration (Momo/VNPAY) in checkout flow."
        )
        return

    if code == "CHK_05":
        _assert_regex(
            ORDER_ROUTES_SOURCE + CHECKOUT_SOURCE,
            r"pending|chờ thanh toán|thanh toán thất bại",
            "CHK_05 expects a pending/failed status path when online payment is cancelled.",
        )
        return

    if code == "CHK_06":
        _assert_regex(
            VOUCHER_ROUTES_SOURCE,
            r"Voucher đã được áp dụng thành công|finalPrice",
            "CHK_06 expects valid voucher apply logic and discount calculation.",
        )
        return

    if code == "CHK_07":
        authenticated_account = create_authenticated_account()
        status, body = _api_apply_voucher({"code": "SAIBET", "totalPrice": 200000}, authenticated_account.token)
        assert status in (400, 404) and "voucher" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CHK_08":
        _assert_regex(
            VOUCHER_ROUTES_SOURCE,
            r"expirationDate|đã hết hạn",
            "CHK_08 expects voucher expiry validation.",
        )
        return

    if code == "CHK_09":
        _assert_regex(
            VOUCHER_ROUTES_SOURCE,
            r"minOrderValue|tối thiểu",
            "CHK_09 expects voucher minimum-order validation.",
        )
        return

    if code == "CHK_10":
        assert "setVoucherCode(\"\")" in CHECKOUT_SOURCE or "setVoucherCode(\"\")" in VOUCHER_COMPONENT_SOURCE, (
            "CHK_10 expects a user action to remove applied voucher and restore original total."
        )
        return

    if code == "CHK_11":
        _assert_regex(
            CHECKOUT_SOURCE + ORDER_ROUTES_SOURCE,
            r"shipping|shipFee|deliveryFee|phí ship",
            "CHK_11 expects dynamic shipping-fee calculation by address.",
        )
        return

    if code == "CHK_12":
        _assert_regex(
            ORDER_ROUTES_SOURCE,
            r"stock|inventory|quantity.*-=|findByIdAndUpdate",
            "CHK_12 expects successful checkout to decrement inventory in backend source.",
        )
        return

    if code == "CHK_13":
        _assert_regex(
            ORDER_ROUTES_SOURCE,
            r"stock|inventory|out of stock|hết hàng",
            "CHK_13 expects checkout to revalidate stock before creating order.",
        )
        return

    if code == "CHK_14":
        _assert_regex(
            ORDER_ROUTES_SOURCE + CHECKOUT_SOURCE,
            r"sendMail|nodemailer|mail|email",
            "CHK_14 expects order-confirmation email logic after successful checkout.",
        )
        return

    if code == "CHK_15":
        authenticated_account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(authenticated_account.user_id, cart, "COD"), authenticated_account.token)
        assert status == 201, f"CHK_15 order creation failed: {status}, {body}"
        cart_status, cart_body = _api_get_cart(authenticated_account.user_id, authenticated_account.token)
        assert cart_status == 404 or "không tồn tại" in json.dumps(cart_body, ensure_ascii=False).lower()
        return

    if code == "CHK_16":
        assert all(token not in CHECKOUT_SOURCE for token in ('value="cash"', "paymentMethod: 'cash'", 'paymentMethod: "cash"')), (
            "CHK_16 expects frontend paymentMethod to use backend enum values such as COD/Online, not cash/payment aliases."
        )
        _assert_regex(
            ORDER_ROUTES_SOURCE + CHECKOUT_SOURCE,
            r"COD|Online",
            "CHK_16 expects paymentMethod enum to be aligned between frontend and backend.",
        )
        return

    if code == "CHK_17":
        authenticated_account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(authenticated_account.user_id, cart, "COD"), None)
        assert status in (401, 403), f"CHK_17 expects create-order without token to be rejected, got status={status}, body={body}"
        return

    if code == "CHK_18":
        assert any(token in CHECKOUT_SOURCE for token in ("isLoading", "loading", "disabled", "setSubmitting")), (
            "CHK_18 expects checkout submit to be guarded against double submit."
        )
        return

    if code == "CHK_19":
        assert not re.search(r"const\s*{[^}]*totalPrice[^}]*}\s*=\s*req\.body", ORDER_ROUTES_SOURCE, flags=re.DOTALL), (
            "CHK_19 expects order total to be recalculated server-side, not trusted from req.body.totalPrice."
        )
        _assert_regex(
            ORDER_ROUTES_SOURCE,
            r"cart|items\.reduce|price\s*\*|discount|voucher",
            "CHK_19 expects order route to calculate total from cart items and voucher rules.",
        )
        return

    if code == "CHK_20":
        authenticated_account, _, cart = _seed_cart_api()
        payload = _build_order_payload(authenticated_account.user_id, cart, "COD")
        payload["phone"] = ""
        status, body = _api_create_order(payload, authenticated_account.token)
        assert status == 400 and "điện thoại" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CHK_21":
        authenticated_account, _, cart = _seed_cart_api()
        payload = _build_order_payload(authenticated_account.user_id, cart, "COD")
        payload["phone"] = "abc"
        status, body = _api_create_order(payload, authenticated_account.token)
        assert status == 400 and "điện thoại" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CHK_22":
        authenticated_account, _, cart = _seed_cart_api()
        payload = _build_order_payload(authenticated_account.user_id, cart, "COD")
        payload["detail"] = ""
        status, body = _api_create_order(payload, authenticated_account.token)
        assert status == 400 and any(word in json.dumps(body, ensure_ascii=False).lower() for word in ("địa chỉ", "vui lòng"))
        return

    if code == "CHK_23":
        authenticated_account, _, cart = _seed_cart_api()
        payload = _build_order_payload(authenticated_account.user_id, cart, "COD")
        payload.pop("paymentMethod", None)
        status, body = _api_create_order(payload, authenticated_account.token)
        assert status == 400 and "payment" in json.dumps(body, ensure_ascii=False).lower()
        return

    if code == "CHK_24":
        authenticated_account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(authenticated_account.user_id, cart, "COD"), authenticated_account.token)
        serialized = json.dumps(body, ensure_ascii=False).lower()
        assert status == 201 and any(token in serialized for token in ("_id", "orderid", "order_id", "mã"))
        return

    if code == "CHK_25":
        _assert_regex(
            VOUCHER_ROUTES_SOURCE + ORDER_ROUTES_SOURCE,
            r"usageLimit|usedCount|increment|decrement|\$inc",
            "CHK_25 expects voucher usage count/limit to be updated after successful use.",
        )
        return

    raise AssertionError(f"Unhandled checkout case: {code}")
