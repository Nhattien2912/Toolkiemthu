from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from random import randint

import pytest

from config import API_BASE_URL, BASE_URL
from utils.account_api import create_authenticated_account
from utils.project_doc_data import CUSTOM_EXTRA_TEST_CASES
from utils.store_api import seed_cart_with_featured_product


SOURCE_PROJECT_ROOT = Path(r"C:\Users\clubb\Desktop\WEB-MERN_t10-2024")


def _read_source(relative_path: str) -> str:
    path = SOURCE_PROJECT_ROOT / relative_path
    assert path.exists(), f"Thiếu file source cần kiểm tra: {path}"
    return path.read_text(encoding="utf-8", errors="replace")


SIGN_UP_SOURCE = _read_source("frontend/src/Pages/AuthSignUp/index.js")
PRODUCT_DETAILS_SOURCE = _read_source("frontend/src/Pages/ProductDetails/index.js")
CHECKOUT_SOURCE = _read_source("frontend/src/Pages/Checkout/index.js")
USER_ROUTES_SOURCE = _read_source("server/routes/userRoutes.js")
CART_ROUTES_SOURCE = _read_source("server/routes/cartRoutes.js")
ORDER_ROUTES_SOURCE = _read_source("server/routes/orderRoutes.js")
VOUCHER_ROUTES_SOURCE = _read_source("server/routes/voucherRoutes.js")
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


def _assert_has_message(status: int, body: dict, keywords: tuple[str, ...], message: str) -> None:
    serialized = _serialize(body)
    assert status in (400, 401, 403, 404) and any(keyword.lower() in serialized for keyword in keywords), (
        f"{message}. HTTP={status}, phản hồi={body}"
    )


def _assert_regex(source: str, pattern: str, message: str) -> None:
    assert re.search(pattern, source, flags=re.IGNORECASE | re.DOTALL), message


def _build_signup_payload(**overrides) -> dict:
    unique = f"{int(time.time())}{randint(100, 999)}"[-8:]
    payload = {
        "username": f"extra{unique}",
        "phone": f"09{unique}",
        "fullName": "Nguyễn Văn A",
        "password": "Abcd123@",
        "confirmPassword": "Abcd123@",
    }
    payload.update(overrides)
    return payload


def _api_signup(payload: dict):
    return _api_json("POST", "/api/user/signup", payload=payload)


def _api_add_cart(payload: dict, token: str | None):
    return _api_json("POST", "/api/cart/addCart", payload=payload, token=token)


def _api_get_cart(user_id: str, token: str):
    return _api_json("GET", f"/api/cart/getCart/{user_id}", token=token)


def _api_remove_cart(user_id: str, product_id: str, token: str):
    return _api_json("DELETE", f"/api/cart/removeCart/{user_id}", payload={"productId": product_id}, token=token)


def _api_create_order(payload: dict, token: str | None):
    return _api_json("POST", "/api/order/create", payload=payload, token=token)


def _get_featured_products(per_page: int = 2) -> list[dict]:
    status, body = _api_json("GET", f"/api/products/featured?perPage={per_page}")
    assert status == 200 and body.get("products"), f"Không lấy được sản phẩm nổi bật. HTTP={status}, phản hồi={body}"
    products = []
    for product in body["products"]:
        detail_status, detail_body = _api_json("GET", f"/api/products/{product['_id']}")
        assert detail_status == 200 and detail_body.get("product"), (
            f"Không lấy được chi tiết sản phẩm {product['_id']}. HTTP={detail_status}, phản hồi={detail_body}"
        )
        products.append(detail_body["product"])
    return products


def _seed_cart_api():
    authenticated_account = create_authenticated_account()
    seeded_cart = seed_cart_with_featured_product(authenticated_account)
    status, cart = _api_get_cart(authenticated_account.user_id, authenticated_account.token)
    assert status == 200, f"Không tải được giỏ hàng đã seed. HTTP={status}, phản hồi={cart}"
    return authenticated_account, seeded_cart, cart


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


def _build_order_payload(user_id: str, cart: dict, **overrides) -> dict:
    payload = {
        "fullName": "Nguyễn Văn A",
        "phone": "0912345678",
        "detail": "123 Lê Lợi, gần chợ Bến Thành",
        "notes": "Giao giờ hành chính",
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
    if code.startswith("REG"):
        return f"{base_url}/signUp"
    if code.startswith("CRT"):
        return f"{base_url}/cart"
    if code.startswith("CHK"):
        return f"{base_url}/checkout"
    return base_url


def _evidence_form_context(case: dict) -> tuple[str, dict[str, str]]:
    code = case["code"]
    uid = case["unique_id"]
    if code.startswith("REG"):
        data = {
            "fullName": "Nguyễn Văn A",
            "username": "extra_user_001",
            "email": "extra.user001@mail.test",
            "phone": "0912345678",
            "password": "Abcd123@",
            "confirmPassword": "Abcd123@",
        }
        if uid == "REG_18_CASE_SENSITIVE":
            data["username"] = "User123 / user123"
        elif uid == "REG_19_NUMERIC_USERNAME":
            data["username"] = "123456"
        elif uid == "REG_20_LONG_PHONE":
            data["phone"] = "091234567890123456"
        elif uid == "REG_22_UNICODE_USERNAME":
            data["username"] = "tiến123"
        return "register", data

    if code.startswith("CRT"):
        data = {
            "product": "Sản phẩm nổi bật đầu tiên",
            "productId": "Theo dữ liệu API sản phẩm",
            "size": "40",
            "color": "Đen",
            "quantity": "1",
        }
        if uid == "CRT_18_STOCK_ZERO":
            data.update({"stock": "0", "quantity": "1"})
        elif uid == "CRT_19_INVALID_SIZE":
            data["size"] = "999"
        elif uid == "CRT_20_INVALID_COLOR":
            data["color"] = "Màu không tồn tại"
        elif uid == "CRT_18_BAD_PRODUCT_ID":
            data["productId"] = "000000000000000000000000"
        return "cart", data

    if code.startswith("CHK"):
        data = {
            "fullName": "Nguyễn Văn A",
            "phone": "0912345678",
            "address": "123 Lê Lợi, Phường Bến Nghé, Quận 1, Hồ Chí Minh",
            "province": "Hồ Chí Minh",
            "district": "Quận 1",
            "ward": "Phường Bến Nghé",
            "detail": "123 Lê Lợi, gần chợ Bến Thành",
            "paymentMethod": "COD",
            "voucher": "GIAM100K" if uid == "CHK_25_TOTAL_AFTER_VOUCHER" else "",
            "notes": "Giao giờ hành chính",
            "items": "1 sản phẩm, size 40, màu Đen, số lượng 1",
        }
        if uid == "CHK_24_LONG_NOTES":
            data["notes"] = "Ghi chú dài hơn 255 ký tự"
        elif uid == "CHK_23_MISSING_PROVINCE":
            data["province"] = ""
        elif uid == "CHK_24_MISSING_DISTRICT":
            data["district"] = ""
        elif uid == "CHK_25_MISSING_WARD":
            data["ward"] = ""
        elif uid == "CHK_26_MISSING_DETAIL":
            data["detail"] = ""
            data["address"] = "Thiếu địa chỉ chi tiết"
        return "checkout", data

    return "general", {"action": case["action"]}


@pytest.mark.parametrize("case", CUSTOM_EXTRA_TEST_CASES, ids=lambda case: case["unique_id"])
def test_custom_extra_case(case, request, step_logger):
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

    if uid == "REG_18_CASE_SENSITIVE":
        unique = f"{int(time.time())}{randint(100, 999)}"[-6:]
        first_username = f"User{unique}"
        second_username = f"user{unique}"
        first_status, first_body = _api_signup(_build_signup_payload(username=first_username))
        assert first_status in (200, 201), f"REG_18 lỗi ở bước tạo username chữ hoa. HTTP={first_status}, phản hồi={first_body}"
        second_status, second_body = _api_signup(_build_signup_payload(username=second_username, phone=f"07{unique}1234"[:10]))
        if second_status in (200, 201):
            actual_username = second_body.get("user", {}).get("username", "")
            assert actual_username == second_username, (
                f"REG_18 không đạt: hệ thống cho tạo username khác hoa/thường thì phải lưu đúng UTF/case. "
                f"Username trả về={actual_username}, phản hồi={second_body}"
            )
        else:
            _assert_has_message(second_status, second_body, ("username", "trùng", "tồn tại", "hợp lệ"), "REG_18 không đạt: nếu không phân biệt hoa/thường thì phải báo trùng/không hợp lệ rõ ràng")
        return

    if uid == "REG_19_NUMERIC_USERNAME":
        payload = _build_signup_payload(username="123456")
        status, body = _api_signup(payload)
        _assert_has_message(status, body, ("username", "hợp lệ", "alphanum", "chữ"), "REG_19 không đạt: username toàn số phải bị từ chối")
        return

    if uid == "REG_20_LONG_PHONE":
        payload = _build_signup_payload(phone="091234567890123456")
        status, body = _api_signup(payload)
        _assert_has_message(status, body, ("phone", "điện thoại", "số", "hợp lệ"), "REG_20 không đạt: SĐT vượt độ dài phải bị từ chối")
        return

    if uid == "REG_22_UNICODE_USERNAME":
        payload = _build_signup_payload(username=f"tiến{int(time.time()) % 10000}")
        status, body = _api_signup(payload)
        assert status in (200, 201) and body.get("user", {}).get("username") == payload["username"], (
            f"REG_22 không đạt: username Unicode phải lưu đúng UTF-8 theo yêu cầu. HTTP={status}, phản hồi={body}"
        )
        return

    if uid == "CRT_18_STOCK_ZERO":
        source = PRODUCT_DETAILS_SOURCE + CART_ROUTES_SOURCE
        _assert_regex(
            source,
            r"productInStock|stock|inventory|outOfStock|soldOut|hết hàng|het hang",
            "CRT_18 không đạt: luồng thêm giỏ hàng chưa có kiểm tra tồn kho bằng 0 trước khi cho thêm sản phẩm.",
        )
        _assert_regex(
            CART_ROUTES_SOURCE,
            r"productInStock\s*[<=>]|quantity\s*[<=>]\s*product\.productInStock|product\.productInStock\s*[<=>]\s*quantity",
            "CRT_18 không đạt: API addCart chưa chặn quantity khi tồn kho bằng 0 hoặc không đủ hàng.",
        )
        return

    if uid == "CRT_19_INVALID_SIZE":
        account = create_authenticated_account()
        product = seed_cart_with_featured_product(account)
        payload = {"userId": account.user_id, "productId": product.product_id, "quantity": 1, "size": "999", "color": product.color}
        status, body = _api_add_cart(payload, account.token)
        _assert_has_message(status, body, ("size", "kích cỡ", "hợp lệ"), "CRT_19 không đạt: size không tồn tại phải bị chặn")
        return

    if uid == "CRT_20_INVALID_COLOR":
        account = create_authenticated_account()
        product = seed_cart_with_featured_product(account)
        payload = {"userId": account.user_id, "productId": product.product_id, "quantity": 1, "size": product.size, "color": "Màu không tồn tại"}
        status, body = _api_add_cart(payload, account.token)
        _assert_has_message(status, body, ("color", "màu", "hợp lệ"), "CRT_20 không đạt: màu không tồn tại phải bị chặn")
        return

    if uid == "CRT_21_CART_RELOAD":
        account, _, first_cart = _seed_cart_api()
        status, second_cart = _api_get_cart(account.user_id, account.token)
        assert status == 200 and second_cart.get("items") == first_cart.get("items"), (
            f"CRT_21 không đạt: sau khi reload/tải lại, dữ liệu giỏ hàng phải giữ nguyên. HTTP={status}, cart trước={first_cart}, cart sau={second_cart}"
        )
        return

    if uid == "CRT_22_REMOVE_LAST_ITEM":
        account, product, _ = _seed_cart_api()
        remove_status, remove_body = _api_remove_cart(account.user_id, product.product_id, account.token)
        assert remove_status == 200, f"CRT_22 không đạt ở bước xóa item cuối. HTTP={remove_status}, phản hồi={remove_body}"
        status, cart = _api_get_cart(account.user_id, account.token)
        if status == 200:
            assert cart.get("items") == [] and cart.get("totalPrice", 0) == 0, (
                f"CRT_22 không đạt: sau khi xóa item cuối, giỏ phải rỗng và totalPrice=0. HTTP={status}, cart={cart}"
            )
        else:
            assert status == 404, f"CRT_22 không đạt: giỏ rỗng nên trả 200 với items=[] hoặc 404, nhưng nhận HTTP={status}, phản hồi={cart}"
        return

    if uid == "CHK_23_VALID_CHECKOUT":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart), account.token)
        assert status == 201 and body.get("status") is True and body.get("order"), (
            f"CHK_23 không đạt: checkout hợp lệ phải tạo đơn thành công. HTTP={status}, phản hồi={body}"
        )
        return

    if uid == "CHK_24_LONG_NOTES":
        account, _, cart = _seed_cart_api()
        long_notes = "Ghi chú kiểm thử dài. " * 20
        status, body = _api_create_order(_build_order_payload(account.user_id, cart, notes=long_notes), account.token)
        assert status == 201, (
            f"CHK_24 không đạt: ghi chú dài phải được lưu hoặc cắt hợp lệ, không được reject/crash. HTTP={status}, phản hồi={body}"
        )
        saved_notes = body.get("order", {}).get("address", {}).get("notes", "")
        assert len(saved_notes) <= len(long_notes), f"CHK_24 không đạt: notes trả về bất thường. notes={saved_notes!r}"
        return

    if uid == "CHK_25_TOTAL_AFTER_VOUCHER":
        source = CHECKOUT_SOURCE + VOUCHER_ROUTES_SOURCE + ORDER_ROUTES_SOURCE
        _assert_regex(source, r"discountPercentage|voucherCode|finalPrice|discountValue|totalPrice", "CHK_25 không đạt: chưa thấy logic tính tổng tiền sau voucher.")
        _assert_regex(source, r"totalPrice\s*[-+*/]|finalPrice|discount", "CHK_25 không đạt: tổng tiền sau voucher cần được tính lại rõ ràng trước khi tạo đơn.")
        return

    if uid == "CHK_26_DOUBLE_SUBMIT":
        source = CHECKOUT_SOURCE + ORDER_ROUTES_SOURCE
        _assert_regex(
            source,
            r"isLoading|loading|disabled|debounce|processing|submitting|AbortController",
            "CHK_26 không đạt: chưa thấy cơ chế khóa nút/chống bấm đặt hàng nhiều lần liên tiếp.",
        )
        return

    if uid == "CHK_27_UNIQUE_ORDER_CODE":
        source = ORDER_ROUTES_SOURCE + _read_source("server/models/OrderModel.js")
        _assert_regex(source, r"orderCode|orderNumber|maDon|mã đơn|uuid|nanoid|unique", "CHK_27 không đạt: chưa thấy trường/cơ chế mã đơn hàng unique sau khi tạo đơn.")
        return

    if uid == "CRT_18_BAD_PRODUCT_ID":
        account = create_authenticated_account()
        payload = {"userId": account.user_id, "productId": "000000000000000000000000", "quantity": 1, "size": "40", "color": "Đen"}
        status, body = _api_add_cart(payload, account.token)
        _assert_has_message(status, body, ("sản phẩm", "không tồn tại", "product"), "CRT_18 không đạt: productId không tồn tại phải bị từ chối")
        return

    if uid == "CRT_19_NO_DISCOUNT_PRICE":
        account, _, cart = _seed_cart_api()
        expected_total = sum(item.get("price", 0) for item in cart.get("items", []))
        assert cart.get("totalPrice") == expected_total, (
            f"CRT_19 không đạt: khi không có giảm giá hoặc giá đã tính xong, totalPrice phải bằng tổng item price. "
            f"expected={expected_total}, actual={cart.get('totalPrice')}, cart={cart}"
        )
        return

    if uid == "CRT_20_CART_IMAGE":
        _, _, cart = _seed_cart_api()
        first_item = cart.get("items", [{}])[0]
        image_value = first_item.get("images") or first_item.get("image") or first_item.get("productId", {}).get("images")
        assert image_value, f"CRT_20 không đạt: item trong giỏ phải lưu ảnh sản phẩm đầu tiên. item={first_item}"
        return

    if uid == "CRT_21_MULTI_PRODUCT_TOTAL":
        account = create_authenticated_account()
        products = _get_featured_products(2)
        for product in products[:2]:
            payload = {
                "userId": account.user_id,
                "productId": product["_id"],
                "quantity": 1,
                "size": product["size"][0],
                "color": product["colors"][0],
            }
            status, body = _api_add_cart(payload, account.token)
            assert status == 200, f"CRT_21 không đạt ở bước thêm sản phẩm {product['_id']}. HTTP={status}, phản hồi={body}"
        status, cart = _api_get_cart(account.user_id, account.token)
        expected_total = sum(item.get("price", 0) for item in cart.get("items", []))
        assert status == 200 and cart.get("totalPrice") == expected_total and len(cart.get("items", [])) >= 1, (
            f"CRT_21 không đạt: totalPrice phải bằng tổng price của các item. HTTP={status}, expected={expected_total}, cart={cart}"
        )
        return

    if uid == "CRT_22_ADD_CART_RESPONSE":
        account = create_authenticated_account()
        product = _get_featured_products(1)[0]
        payload = {
            "userId": account.user_id,
            "productId": product["_id"],
            "quantity": 1,
            "size": product["size"][0],
            "color": product["colors"][0],
        }
        status, body = _api_add_cart(payload, account.token)
        assert status == 200 and body.get("status") is True and body.get("message") and body.get("cart"), (
            f"CRT_22 không đạt: addCart thành công phải trả status=true, message và cart. HTTP={status}, phản hồi={body}"
        )
        return

    if uid == "CHK_23_MISSING_PROVINCE":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart, province="", provinceCode=""), account.token)
        _assert_has_message(status, body, ("province", "tỉnh", "thành"), "CHK_23 không đạt: thiếu tỉnh/thành phải bị chặn")
        return

    if uid == "CHK_24_MISSING_DISTRICT":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart, district="", districtCode=""), account.token)
        _assert_has_message(status, body, ("district", "huyện", "quận"), "CHK_24 không đạt: thiếu quận/huyện phải bị chặn")
        return

    if uid == "CHK_25_MISSING_WARD":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart, ward="", wardCode=""), account.token)
        _assert_has_message(status, body, ("ward", "xã", "phường"), "CHK_25 không đạt: thiếu xã/phường phải bị chặn")
        return

    if uid == "CHK_26_MISSING_DETAIL":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart, detail=""), account.token)
        _assert_has_message(status, body, ("detail", "số nhà", "thôn", "địa chỉ"), "CHK_26 không đạt: thiếu địa chỉ chi tiết phải bị chặn")
        return

    if uid == "CHK_27_CREATE_ORDER_RESPONSE":
        account, _, cart = _seed_cart_api()
        status, body = _api_create_order(_build_order_payload(account.user_id, cart), account.token)
        assert status == 201 and body.get("status") is True and body.get("type") == "success" and body.get("order"), (
            f"CHK_27 không đạt: tạo đơn thành công phải trả status=true, type=success và thông tin order. HTTP={status}, phản hồi={body}"
        )
        return

    raise AssertionError(f"Chưa viết logic kiểm tra cho testcase mới: {uid}")
