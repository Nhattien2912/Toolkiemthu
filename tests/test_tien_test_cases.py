from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from random import randint
from time import time

import pytest

from config import API_BASE_URL, BASE_URL
from utils.account_api import create_authenticated_account
from utils.project_doc_data import TIEN_TEST_CASES
from utils.store_api import seed_cart_with_featured_product


SOURCE_PROJECT_ROOT = Path(r"C:\Users\clubb\Desktop\WEB-MERN_t10-2024")


def _read_source(relative_path: str) -> str:
    path = SOURCE_PROJECT_ROOT / relative_path
    assert path.exists(), f"Thiếu file source cần kiểm tra: {path}"
    return path.read_text(encoding="utf-8", errors="replace")


APP_SOURCE = _read_source("frontend/src/App.js")
HEADER_SOURCE = _read_source("frontend/src/Components/Header/index.js")
SIGN_IN_SOURCE = _read_source("frontend/src/Pages/AuthSignIn/index.js")
SIGN_UP_SOURCE = _read_source("frontend/src/Pages/AuthSignUp/index.js")
PRODUCT_DETAILS_SOURCE = _read_source("frontend/src/Pages/ProductDetails/index.js")
CHECKOUT_SOURCE = _read_source("frontend/src/Pages/Checkout/index.js")
CART_ROUTES_SOURCE = _read_source("server/routes/cartRoutes.js")
ORDER_ROUTES_SOURCE = _read_source("server/routes/orderRoutes.js")
USER_ROUTES_SOURCE = _read_source("server/routes/userRoutes.js")
VOUCHER_ROUTES_SOURCE = _read_source("server/routes/voucherRoutes.js")


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
            return response.status, json.loads(raw_body) if raw_body else {}
    except urllib.error.HTTPError as error:
        raw_body = error.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            body = {"raw": raw_body}
        return error.code, body


def _build_signup_payload(**overrides) -> dict:
    unique = f"{int(time())}{randint(100, 999)}"[-8:]
    payload = {
        "username": f"tien{unique}",
        "phone": f"08{unique}",
        "fullName": "Tien Test User",
        "password": "Abcd123@",
        "confirmPassword": "Abcd123@",
    }
    payload.update(overrides)
    return payload


def _api_signup(payload: dict):
    return _api_json("POST", "/api/user/signup", payload=payload)


def _api_signin(username_or_phone: str, password: str):
    return _api_json(
        "POST",
        "/api/user/signin",
        payload={"usernameOrPhone": username_or_phone, "password": password},
    )


def _api_change_password(user_id: str, current_password: str | None, new_password: str | None, token: str | None):
    payload = {}
    if current_password is not None:
        payload["currentPassword"] = current_password
    if new_password is not None:
        payload["newPassword"] = new_password
    return _api_json("PUT", f"/api/user/change-password/{user_id}", payload=payload, token=token)


def _api_add_cart(payload: dict, token: str | None):
    return _api_json("POST", "/api/cart/addCart", payload=payload, token=token)


def _api_get_cart(user_id: str, token: str):
    return _api_json("GET", f"/api/cart/getCart/{user_id}", token=token)


def _api_create_order(payload: dict, token: str | None):
    return _api_json("POST", "/api/order/create", payload=payload, token=token)


def _build_order_payload(user_id: str, cart: dict, payment_method: str | None = "COD") -> dict:
    return {
        "fullName": "Nguyen Van A",
        "phone": "0912345678",
        "detail": "123 Test Street",
        "notes": "tien test order",
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
        "date": "2026-04-19",
        "totalPrice": cart["totalPrice"],
    }


def _seed_cart_api():
    authenticated_account = create_authenticated_account()
    seeded_cart = seed_cart_with_featured_product(authenticated_account)
    status, cart = _api_get_cart(authenticated_account.user_id, authenticated_account.token)
    assert status == 200, f"Không tải được giỏ hàng đã seed. HTTP={status}, phản hồi={cart}"
    return authenticated_account, seeded_cart, cart


def _assert_regex(text: str, pattern: str, message: str) -> None:
    assert re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL), message


def _web_context_url(code: str) -> str:
    base_url = BASE_URL.rstrip("/")
    if code.startswith("REG"):
        return f"{base_url}/signUp"
    if code.startswith(("LOG", "PWD")):
        return f"{base_url}/signIn"
    if code.startswith(("CRT", "VCH")):
        return f"{base_url}/cart"
    if code.startswith("CHK"):
        return f"{base_url}/checkout"
    return base_url


def _evidence_form_context(code: str, action: str) -> tuple[str, dict[str, str]]:
    if code.startswith("REG"):
        data = {
            "fullName": "Nguyễn Văn A",
            "username": "tien_user_001",
            "email": "tien.user001@mail.test",
            "phone": "0912345678",
            "password": "Abcd123@",
            "confirmPassword": "Abcd123@",
        }
        if code == "REG_13":
            data.update({"username": " user123 ", "phone": " 0912345678 "})
        elif code == "REG_14":
            data["phone"] = "0987 654 321"
        elif code == "REG_15":
            data.update({"password": "Abc@ 1234", "confirmPassword": "Abc@ 1234"})
        elif code == "REG_16":
            data["username"] = "user@@@"
        elif code == "REG_17":
            data["username"] = "u" * 260
        return "register", data

    if code.startswith("LOG"):
        data = {
            "usernameOrPhone": "tien_user_001",
            "password": "Abcd123@",
        }
        if code == "LOG_10":
            data["usernameOrPhone"] = " user123 "
        elif code == "LOG_11":
            data["password"] = " pass123 "
        return "login", data

    if code.startswith("PWD"):
        data = {
            "currentPassword": "Abcd123@",
            "newPassword": "Xyzc123@",
            "confirmPassword": "Xyzc123@",
            "token": "Không có token" if code == "PWD_06" else "Có token hợp lệ",
        }
        if code == "PWD_07":
            data.update({"newPassword": "Abcd123@", "confirmPassword": "Abcd123@"})
        return "password", data

    if code.startswith("CRT"):
        return "cart", {
            "product": "Sản phẩm nổi bật đầu tiên",
            "size": "40",
            "color": "Đen",
            "quantity": "999" if code == "CRT_12" else "1",
        }

    if code.startswith(("CHK", "VCH")):
        data = {
            "fullName": "Nguyễn Văn A",
            "phone": "0912345678",
            "address": "123 Lê Lợi, Phường Bến Nghé, Quận 1, TP.HCM",
            "paymentMethod": "COD",
            "voucher": "",
            "items": "1 sản phẩm, size 40, màu Đen, số lượng 1",
        }
        if code == "CHK_17":
            data["phone"] = "09abc12345"
        if code == "CHK_18":
            data["paymentMethod"] = "null"
        if code == "CHK_20":
            data["items"] = "[]"
        if code in {"CHK_06", "VCH_06"}:
            data["voucher"] = "GIAM100K"
        elif code in {"CHK_07", "VCH_07", "VCH_08"}:
            data["voucher"] = "SAIBET"
        elif code == "CHK_08":
            data["voucher"] = "EXPIRED100K"
        elif code == "CHK_09":
            data["voucher"] = "MIN500K"
        return "checkout", data

    return "general", {"action": action}


@pytest.mark.parametrize("case", TIEN_TEST_CASES, ids=lambda case: case["code"])
def test_tien_case(case, request, step_logger):
    code = case["code"]
    form_kind, form_data = _evidence_form_context(code, case["action"])
    request.node.evidence_url = _web_context_url(code)
    request.node.evidence_context = {
        "code": code,
        "scenario": case["scenario"],
        "action": case["action"],
        "expected": case["expected"],
        "form_kind": form_kind,
        "form_data": form_data,
    }
    step_logger(f"{code} - {case['scenario']}")

    if code == "REG_13":
        source = SIGN_UP_SOURCE + USER_ROUTES_SOURCE
        assert ".trim()" in source, "REG_13 không đạt: form đăng ký cần trim khoảng trắng đầu/cuối trước khi submit hoặc validation."
        return

    if code == "REG_14":
        payload = _build_signup_payload(phone="0987 654 321")
        status, body = _api_signup(payload)
        assert status == 400 and "điện thoại" in json.dumps(body, ensure_ascii=False).lower(), (
            f"REG_14 không đạt: SĐT có khoảng trắng phải báo lỗi không hợp lệ, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "REG_15":
        payload = _build_signup_payload(password="Abc@ 1234", confirmPassword="Abc@ 1234")
        status, body = _api_signup(payload)
        assert status == 400 and "mật khẩu" in json.dumps(body, ensure_ascii=False).lower(), (
            f"REG_15 không đạt: password chứa khoảng trắng phải bị từ chối, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "REG_16":
        payload = _build_signup_payload(username="user@@@")
        status, body = _api_signup(payload)
        assert status == 400 and any(word in json.dumps(body, ensure_ascii=False).lower() for word in ("username", "ký tự", "hợp lệ")), (
            f"REG_16 không đạt: username có ký tự đặc biệt phải bị chặn, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "REG_17":
        payload = _build_signup_payload(username="u" * 256)
        status, body = _api_signup(payload)
        assert status == 400 and any(word in json.dumps(body, ensure_ascii=False).lower() for word in ("username", "dài", "hợp lệ")), (
            f"REG_17 không đạt: username quá dài phải bị báo lỗi độ dài/không hợp lệ, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "LOG_10":
        account = create_authenticated_account()
        status, body = _api_signin(f" {account.username} ", account.password)
        assert status == 200 and body.get("success") is True, (
            f"LOG_10 không đạt: username có khoảng trắng đầu/cuối phải được trim và login thành công, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "LOG_11":
        account = create_authenticated_account()
        status, body = _api_signin(account.username, f" {account.password} ")
        assert status == 400 and "không đúng" in json.dumps(body, ensure_ascii=False).lower(), (
            f"LOG_11 không đạt: password có khoảng trắng phải đăng nhập thất bại, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "LOG_12":
        source = APP_SOURCE + HEADER_SOURCE + SIGN_IN_SOURCE
        assert "sessionStorage.getItem" in source and "sessionStorage.setItem" in source, (
            "LOG_12 không đạt: sau khi login cần có cơ chế lưu và đọc sessionStorage để refresh vẫn giữ trạng thái đăng nhập."
        )
        return

    if code == "LOG_13":
        protected_source = APP_SOURCE + HEADER_SOURCE
        assert "ProtectedRoute" in protected_source or "navigate(\"/signIn\")" in protected_source, (
            "LOG_13 không đạt: route protected cần chặn user đã logout và điều hướng về trang đăng nhập."
        )
        return

    if code == "PWD_06":
        account = create_authenticated_account()
        status, body = _api_change_password(account.user_id, account.password, "Xyzc123@", None)
        assert status in (401, 403), f"PWD_06 không đạt: đổi mật khẩu khi chưa đăng nhập phải bị chặn 401/403, nhưng nhận HTTP={status}, phản hồi={body}"
        return

    if code == "PWD_07":
        account = create_authenticated_account()
        status, body = _api_change_password(account.user_id, account.password, account.password, account.token)
        assert status == 400, f"PWD_07 không đạt: mật khẩu mới trùng mật khẩu cũ phải bị từ chối, nhưng nhận HTTP={status}, phản hồi={body}"
        return

    if code == "PWD_08":
        account = create_authenticated_account()
        new_password = "Xyzc123@"
        status, body = _api_change_password(account.user_id, account.password, new_password, account.token)
        assert status == 200, f"PWD_08 không đạt ở bước đổi mật khẩu: mong đợi HTTP 200, nhưng nhận HTTP={status}, phản hồi={body}"
        login_status, login_body = _api_signin(account.username, new_password)
        assert login_status == 200 and login_body.get("success") is True, (
            f"PWD_08 không đạt: sau khi đổi mật khẩu phải đăng nhập được bằng mật khẩu mới, nhưng nhận HTTP={login_status}, phản hồi={login_body}"
        )
        return

    if code == "CRT_12":
        account = create_authenticated_account()
        product = seed_cart_with_featured_product(account)
        payload = {"userId": account.user_id, "productId": product.product_id, "quantity": 999, "size": product.size, "color": product.color}
        status, body = _api_add_cart(payload, account.token)
        assert status == 400 or body.get("cart", {}).get("items", [{}])[0].get("quantity", 999) < 999, (
            f"CRT_12 không đạt: số lượng 999 phải bị giới hạn hoặc báo lỗi, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "CRT_13":
        account, _, cart = _seed_cart_api()
        assert cart.get("items"), f"CRT_13 không đạt: user={account.user_id} chưa có giỏ hàng mới sau khi thêm sản phẩm."
        return

    if code == "CRT_14":
        source = PRODUCT_DETAILS_SOURCE + CART_ROUTES_SOURCE
        _assert_regex(source, r"discount|sale|oldPrice|finalPrice|priceAfter", "CRT_14 không đạt: chưa thấy logic xử lý giá khuyến mãi trong luồng product/cart.")
        return

    if code == "CRT_15":
        account = create_authenticated_account()
        product = seed_cart_with_featured_product(account)
        payload = {"userId": account.user_id, "productId": product.product_id, "quantity": 1, "size": product.size, "color": product.color}
        second_status, second_body = _api_add_cart(payload, account.token)
        assert second_status == 200, f"CRT_15 không đạt: lần thêm sản phẩm thứ hai thất bại. HTTP={second_status}, phản hồi={second_body}"
        cart_status, cart = _api_get_cart(account.user_id, account.token)
        matching = [item for item in cart.get("items", []) if item.get("productId", {}).get("_id") == product.product_id]
        assert cart_status == 200 and len(matching) == 1, (
            f"CRT_15 không đạt: thêm liên tục cùng sản phẩm không được tạo dòng trùng, HTTP={cart_status}, số dòng khớp={len(matching)}, cart={cart}"
        )
        return

    if code == "CRT_16":
        account = create_authenticated_account()
        product = seed_cart_with_featured_product(account)
        payload = {"userId": account.user_id, "productId": product.product_id, "quantity": 1, "size": product.size, "color": product.color}
        status, body = _api_add_cart(payload, None)
        assert status in (401, 403), f"CRT_16 không đạt: API thêm giỏ hàng không token phải bị chặn 401/403, nhưng nhận HTTP={status}, phản hồi={body}"
        return

    if code == "CRT_17":
        account, _, cart = _seed_cart_api()
        expected_total = sum(
            item.get("quantity", 0) * item.get("productId", {}).get("price", 0)
            for item in cart.get("items", [])
        )
        assert cart.get("totalPrice") == expected_total, f"CRT_17 không đạt: tổng tiền mong đợi={expected_total}, tổng tiền thực tế={cart.get('totalPrice')}"
        return

    if code == "CHK_16":
        source = ORDER_ROUTES_SOURCE + CHECKOUT_SOURCE
        assert ".trim()" in source, "CHK_16 không đạt: thông tin checkout cần trim khoảng trắng đầu/cuối trước khi lưu đơn."
        return

    if code == "CHK_17":
        account, _, cart = _seed_cart_api()
        payload = _build_order_payload(account.user_id, cart)
        payload["phone"] = "09abc12345"
        status, body = _api_create_order(payload, account.token)
        assert status == 400 and "điện thoại" in json.dumps(body, ensure_ascii=False).lower(), (
            f"CHK_17 không đạt: SĐT checkout có chữ phải bị báo lỗi, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "CHK_18":
        account, _, cart = _seed_cart_api()
        payload = _build_order_payload(account.user_id, cart, None)
        status, body = _api_create_order(payload, account.token)
        assert status == 400 and "payment" in json.dumps(body, ensure_ascii=False).lower(), (
            f"CHK_18 không đạt: thiếu paymentMethod phải bị báo lỗi, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "CHK_19":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart), None)
        assert status in (401, 403), f"CHK_19 không đạt: đặt hàng khi chưa đăng nhập phải bị chặn 401/403, nhưng nhận HTTP={status}, phản hồi={body}"
        return

    if code == "CHK_20":
        account = create_authenticated_account()
        payload = _build_order_payload(account.user_id, {"items": [], "totalPrice": 0})
        status, body = _api_create_order(payload, account.token)
        assert status == 400 and any(word in json.dumps(body, ensure_ascii=False).lower() for word in ("items", "sản phẩm", "giỏ")), (
            f"CHK_20 không đạt: danh sách sản phẩm rỗng không được tạo đơn, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "CHK_21":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart), account.token)
        serialized = json.dumps(body, ensure_ascii=False).lower()
        assert status == 201 and ("pending" in serialized or "chờ" in serialized), (
            f"CHK_21 không đạt: sau khi đặt hàng trạng thái đơn phải là Pending/Chờ, nhưng nhận HTTP={status}, phản hồi={body}"
        )
        return

    if code == "CHK_22":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart), account.token)
        assert status == 201, f"CHK_22 không đạt ở bước tạo đơn hàng: mong đợi HTTP 201, nhưng nhận HTTP={status}, phản hồi={body}"
        cart_status, cart_body = _api_get_cart(account.user_id, account.token)
        assert cart_status == 404 or "không tồn tại" in json.dumps(cart_body, ensure_ascii=False).lower(), (
            f"CHK_22 không đạt: sau khi đặt hàng giỏ hàng phải bị xóa/rỗng, nhưng nhận HTTP={cart_status}, phản hồi={cart_body}"
        )
        return

    if code == "VCH_06":
        _assert_regex(VOUCHER_ROUTES_SOURCE, r"totalPrice\s*>=\s*.*minOrderValue|minOrderValue\s*<=\s*.*totalPrice", "VCH_06 không đạt: voucher phải hợp lệ khi tổng tiền bằng đúng minOrderValue.")
        return

    if code == "VCH_07":
        _assert_regex(VOUCHER_ROUTES_SOURCE, r"usageLimit|usedCount|limit", "VCH_07 không đạt: chưa thấy kiểm tra giới hạn lượt sử dụng voucher.")
        return

    if code == "VCH_08":
        _assert_regex(VOUCHER_ROUTES_SOURCE, r"\$inc|usedCount|usageLimit", "VCH_08 không đạt: chưa thấy cơ chế cập nhật/giới hạn số lần dùng voucher để tránh dùng vượt lượt.")
        return

    raise AssertionError(f"Chưa viết logic kiểm tra cho test case của Tiến: {code}")
