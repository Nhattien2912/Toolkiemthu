from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from config import API_BASE_URL, BASE_URL
from utils.account_api import create_authenticated_account
from utils.project_doc_data import RISK_TEST_CASES
from utils.store_api import seed_cart_with_featured_product


SOURCE_PROJECT_ROOT = Path(r"C:\Users\clubb\Desktop\WEB-MERN_t10-2024")
XSS_PAYLOAD = "<script>alert('hack')</script>"
LONG_NOTES = "Ghi chú kiểm thử cực dài để kiểm tra giới hạn độ dài dữ liệu. " * 45


def _read_source(relative_path: str) -> str:
    path = SOURCE_PROJECT_ROOT / relative_path
    assert path.exists(), f"Thiếu file source cần kiểm tra: {path}"
    return path.read_text(encoding="utf-8", errors="replace")


HEADER_SOURCE = _read_source("frontend/src/Components/Header/index.js")
CHECKOUT_SOURCE = _read_source("frontend/src/Pages/Checkout/index.js")
VOUCHER_ROUTES_SOURCE = _read_source("server/routes/voucherRoutes.js")
ORDER_ROUTES_SOURCE = _read_source("server/routes/orderRoutes.js")
VALIDATE_SOURCE = _read_source("server/middlewares/validate.js")


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
        with urllib.request.urlopen(request, timeout=45) as response:
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


def _serialize(body: dict) -> str:
    return json.dumps(body, ensure_ascii=False).lower()


def _assert_regex(source: str, pattern: str, message: str) -> None:
    assert re.search(pattern, source, flags=re.IGNORECASE | re.DOTALL), message


def _api_get_cart(user_id: str, token: str):
    return _api_json("GET", f"/api/cart/getCart/{user_id}", token=token)


def _api_create_order(payload: dict, token: str | None):
    return _api_json("POST", "/api/order/create", payload=payload, token=token)


def _product_id_from_item(item: dict) -> str:
    product = item.get("productId")
    if isinstance(product, dict):
        return product.get("_id") or product.get("id") or ""
    return str(product or "")


def _normalize_order_items(cart: dict) -> list[dict]:
    items = []
    for item in cart.get("items", []):
        product_id = _product_id_from_item(item)
        assert product_id, f"Item trong giỏ hàng thiếu productId hợp lệ: {item}"
        items.append(
            {
                "productId": product_id,
                "quantity": item.get("quantity", 1),
                "price": item.get("price", 0),
            }
        )
    return items


def _seed_cart_api():
    authenticated_account = create_authenticated_account()
    seed_cart_with_featured_product(authenticated_account)
    status, cart = _api_get_cart(authenticated_account.user_id, authenticated_account.token)
    assert status == 200, f"Không tải được giỏ hàng đã seed. HTTP={status}, phản hồi={cart}"
    return authenticated_account, cart


def _build_order_payload(user_id: str, cart: dict, **overrides) -> dict:
    payload = {
        "fullName": "Nguyễn Văn A",
        "phone": "0912345678",
        "detail": "123 Lê Lợi, gần chợ Bến Thành",
        "notes": "Giao hàng giờ hành chính",
        "paymentMethod": "COD",
        "userId": user_id,
        "items": _normalize_order_items(cart),
        "isVoucher": False,
        "voucherCode": "",
        "discountPercentage": 0,
        "appliedDate": "",
        "province": "Hồ Chí Minh",
        "provinceCode": "79",
        "district": "Quận 1",
        "districtCode": "760",
        "ward": "Phường Bến Nghé",
        "wardCode": "26734",
        "date": "2026-04-19",
        "totalPrice": cart["totalPrice"],
    }
    payload.update(overrides)
    return payload


def _web_context_url(code: str) -> str:
    base_url = BASE_URL.rstrip("/")
    if code.startswith("LOG"):
        return base_url
    if code.startswith("VCH"):
        return f"{base_url}/cart"
    if code.startswith("CHK"):
        return f"{base_url}/checkout"
    return base_url


def _evidence_form_context(case: dict) -> tuple[str, dict[str, str]]:
    uid = case["unique_id"]
    if uid == "LOG_10_LOGOUT_FLOW":
        return "login", {
            "usernameOrPhone": "risk_user_001",
            "password": "Abcd123@",
            "token": "Token phải bị xóa sau logout",
            "expectedRedirect": "/signIn hoặc trang chủ",
        }

    if uid == "VCH_09_VOUCHER_TRIM":
        return "cart", {
            "voucher": " GIAM100K ",
            "cartTotal": ">= điều kiện tối thiểu của mã nếu mã tồn tại",
            "token": "Có token hợp lệ của khách hàng",
        }

    checkout_data = {
        "fullName": "Nguyễn Văn A",
        "phone": "0912345678",
        "address": "123 Lê Lợi, Phường Bến Nghé, Quận 1, Hồ Chí Minh",
        "province": "Hồ Chí Minh",
        "district": "Quận 1",
        "ward": "Phường Bến Nghé",
        "detail": "123 Lê Lợi, gần chợ Bến Thành",
        "notes": "Giao hàng giờ hành chính",
        "paymentMethod": "COD",
        "items": "1 sản phẩm hợp lệ, quantity=1",
        "token": "Có token hợp lệ của khách hàng",
    }
    if uid == "CHK_34_NOTES_LENGTH_LIMIT":
        checkout_data["notes"] = LONG_NOTES
    elif uid == "CHK_31_XSS_CHECKOUT":
        checkout_data["detail"] = XSS_PAYLOAD
        checkout_data["notes"] = XSS_PAYLOAD
        checkout_data["address"] = XSS_PAYLOAD
    elif uid == "CHK_35_DOUBLE_CLICK_PREVENTION":
        checkout_data["submitAction"] = 'Spam click nút "Xác nhận đặt hàng" liên tục'
    elif uid == "CHK_37_NEGATIVE_QUANTITY_API":
        checkout_data["items"] = 'items[0].quantity = -5, payload bị sửa qua F12/Network'
    return "checkout", checkout_data


@pytest.mark.parametrize("case", RISK_TEST_CASES, ids=lambda case: case["unique_id"])
def test_risk_case(case, request, step_logger):
    code = case["code"]
    uid = case["unique_id"]
    form_kind, form_data = _evidence_form_context(case)
    request.node.evidence_url = _web_context_url(code)
    request.node.evidence_context = {
        "code": code,
        "scenario": case["scenario"],
        "action": case["action"],
        "expected": case["expected"],
        "form_kind": form_kind,
        "form_data": form_data,
    }

    step_logger(f"{uid} / {code} - {case['scenario']}")
    step_logger(f"Dữ liệu kiểm thử: {case['action']}")
    step_logger(f"Kết quả mong đợi: {case['expected']}")

    if uid == "LOG_10_LOGOUT_FLOW":
        step_logger("Đối chiếu source Header: nút Đăng xuất phải xóa localStorage/sessionStorage và redirect.")
        _assert_regex(HEADER_SOURCE, r"handleLogout|Đăng xuất|Dang xuat|Logout", "LOG_10 không đạt: Header thiếu entry/nút đăng xuất.")
        _assert_regex(HEADER_SOURCE, r"localStorage\.clear\(\)|localStorage\.removeItem", "LOG_10 không đạt: logout phải xóa token/localStorage.")
        _assert_regex(HEADER_SOURCE, r"sessionStorage\.clear\(\)|sessionStorage\.removeItem", "LOG_10 không đạt: logout phải xóa sessionStorage.")
        _assert_regex(HEADER_SOURCE, r"setIsLogin\(false\)|setUserData\(\{\}\)|navigate\(\"/signIn\"\)", "LOG_10 không đạt: logout phải chuyển trạng thái khách vãng lai hoặc redirect.")
        return

    if uid == "VCH_09_VOUCHER_TRIM":
        step_logger("Đối chiếu source apply voucher: mã voucher có khoảng trắng phải được trim trước khi query DB.")
        _assert_regex(
            VOUCHER_ROUTES_SOURCE,
            r"code\s*=\s*code\.trim\(\)|code\.trim\(\)|req\.body\.code\.trim\(\)",
            'VCH_09 không đạt: API /api/voucher/apply chưa trim mã voucher trước khi tìm mã. Nhập " GIAM100K " có nguy cơ bị báo không tồn tại dù mã đúng.',
        )
        return

    if uid == "CHK_34_NOTES_LENGTH_LIMIT":
        step_logger("Đối chiếu form Checkout và backend: trường notes phải có maxlength hoặc backend phải cắt/giới hạn độ dài.")
        source = CHECKOUT_SOURCE + VALIDATE_SOURCE + ORDER_ROUTES_SOURCE
        _assert_regex(
            source,
            r"name=\"notes\"[\s\S]{0,300}(maxLength|maxlength)|notes\s*:\s*Joi\.string\(\)\.max\(|notes\.slice\(|notes\.substring\(",
            "CHK_34 không đạt: ô Notes chưa có maxlength/cắt chuỗi/Joi max, dữ liệu >2000 ký tự có thể đi thẳng xuống DB.",
        )
        return

    if uid == "CHK_31_XSS_CHECKOUT":
        step_logger("Gửi payload XSS vào API tạo đơn để kiểm tra backend có reject hoặc sanitize dữ liệu không.")
        account, cart = _seed_cart_api()
        payload = _build_order_payload(account.user_id, cart, detail=XSS_PAYLOAD, notes=XSS_PAYLOAD)
        status, body = _api_create_order(payload, account.token)
        serialized = _serialize(body)
        if status in (400, 422):
            assert any(word in serialized for word in ("script", "xss", "ký tự", "không hợp lệ", "invalid")), (
                f"CHK_31 không đạt: backend có reject nhưng message chưa rõ lý do XSS/ký tự không hợp lệ. HTTP={status}, phản hồi={body}"
            )
            return
        assert status == 201, f"CHK_31 không đạt: API trả trạng thái bất thường khi test XSS. HTTP={status}, phản hồi={body}"
        saved_address = body.get("order", {}).get("address", {})
        saved_text = json.dumps(saved_address, ensure_ascii=False)
        assert "<script" not in saved_text.lower(), (
            f"CHK_31 không đạt: backend lưu nguyên payload XSS vào đơn hàng, chưa sanitize/escape dữ liệu. "
            f"HTTP={status}, address lưu={saved_address}"
        )
        return

    if uid == "CHK_35_DOUBLE_CLICK_PREVENTION":
        step_logger("Đối chiếu source Checkout: submit button phải disabled theo loading hoặc có cơ chế idempotency.")
        source = CHECKOUT_SOURCE + ORDER_ROUTES_SOURCE
        has_loading_state = re.search(r"const\s+\[loading,\s*setLoading\]|setLoading\(true\)", source, flags=re.IGNORECASE)
        has_disabled_submit = re.search(r"<Button[\s\S]{0,260}type=\"submit\"[\s\S]{0,260}disabled=\{?\s*loading", CHECKOUT_SOURCE, flags=re.IGNORECASE)
        has_idempotency = re.search(r"idempotency|requestId|orderToken|unique\s*request|duplicate", source, flags=re.IGNORECASE)
        assert has_loading_state and (has_disabled_submit or has_idempotency), (
            "CHK_35 không đạt: có loading state nhưng nút submit chưa disabled theo loading và backend chưa có idempotency key, "
            "người dùng spam click có nguy cơ tạo trùng đơn."
        )
        return

    if uid == "CHK_37_NEGATIVE_QUANTITY_API":
        step_logger("Gửi payload API checkout với quantity=-5 để kiểm tra backend validate lại số lượng.")
        account, cart = _seed_cart_api()
        payload = _build_order_payload(account.user_id, cart)
        payload["items"][0]["quantity"] = -5
        status, body = _api_create_order(payload, account.token)
        serialized = _serialize(body)
        assert status in (400, 422) and any(word in serialized for word in ("quantity", "số lượng", "min", "lớn hơn", "không hợp lệ")), (
            f"CHK_37 không đạt: backend phải chặn quantity âm và trả lỗi rõ ràng. HTTP={status}, phản hồi={body}"
        )
        return

    raise AssertionError(f"Chưa viết logic kiểm tra cho risk testcase: {uid}")
