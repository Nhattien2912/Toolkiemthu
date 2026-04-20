from __future__ import annotations

import re
from pathlib import Path


SOURCE_PROJECT_ROOT = Path(r"C:\Users\clubb\Desktop\WEB-MERN_t10-2024")


def _read_source(relative_path: str) -> str:
    path = SOURCE_PROJECT_ROOT / relative_path
    assert path.exists(), f"Missing source file: {path}"
    return path.read_text(encoding="utf-8", errors="replace")


APP_SOURCE = _read_source("frontend/src/App.js")
SIGN_IN_SOURCE = _read_source("frontend/src/Pages/AuthSignIn/index.js")
SIGN_UP_SOURCE = _read_source("frontend/src/Pages/AuthSignUp/index.js")
CHECKOUT_SOURCE = _read_source("frontend/src/Pages/Checkout/index.js")
VALIDATE_SOURCE = _read_source("server/middlewares/validate.js")
CART_ROUTES_SOURCE = _read_source("server/routes/cartRoutes.js")
ORDER_ROUTES_SOURCE = _read_source("server/routes/orderRoutes.js")


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
                return source[brace_start : index + 1]

    raise AssertionError(f"Closing brace not found for anchor: {anchor}")


def _assert_block_has_return(source: str, anchor: str, case_label: str) -> None:
    block = _extract_block(source, anchor)
    assert "return;" in block, f"{case_label} should stop submit flow with `return;`."


def _assert_owner_guard(block: str, id_name: str, route_label: str) -> None:
    compares_owner = any(
        token in block
        for token in (
            f"req.user.id !== {id_name}",
            f"req.user.id != {id_name}",
            f"{id_name} !== req.user.id",
            f"{id_name} != req.user.id",
            f"req.user._id !== {id_name}",
            f"req.user._id != {id_name}",
            f"{id_name} !== req.user._id",
            f"{id_name} != req.user._id",
        )
    )
    assert "req.user" in block and compares_owner, (
        f"{route_label} should compare authenticated user with `{id_name}` before processing."
    )


def test_signin_forgot_password_link_has_destination():
    match = re.search(r"<Link(?P<attrs>[^>]*)>\s*Qu", SIGN_IN_SOURCE, flags=re.IGNORECASE | re.DOTALL)
    assert match, "Forgot password link markup should exist on sign-in page."
    assert "to=" in match.group("attrs"), "Forgot password link should declare a route destination with `to=`."


def test_storefront_app_registers_forgot_password_route():
    assert re.search(r'Route\s+path="/[^"]*forgot[^"]*"', APP_SOURCE, flags=re.IGNORECASE | re.DOTALL), (
        "Storefront router should expose a forgot-password route."
    )


def test_storefront_has_forgot_password_page_component():
    candidates = [
        SOURCE_PROJECT_ROOT / "frontend/src/Pages/ForgotPassword/index.js",
        SOURCE_PROJECT_ROOT / "frontend/src/Pages/ForgotPassword/ForgotPassword.jsx",
        SOURCE_PROJECT_ROOT / "frontend/src/Pages/ForgotPassword/ForgotPassword.js",
    ]
    assert any(path.exists() for path in candidates), (
        "Storefront frontend should include a dedicated forgot-password page component."
    )


def test_signup_validation_returns_after_empty_username():
    _assert_block_has_return(SIGN_UP_SOURCE, 'if (username === "")', "Empty username validation")


def test_signup_validation_returns_after_empty_phone():
    _assert_block_has_return(SIGN_UP_SOURCE, 'if (phone === "")', "Empty phone validation")


def test_signup_validation_returns_after_empty_full_name():
    _assert_block_has_return(SIGN_UP_SOURCE, 'if (fullName === "")', "Empty fullName validation")


def test_signup_validation_returns_after_empty_password():
    _assert_block_has_return(SIGN_UP_SOURCE, 'if (password === "")', "Empty password validation")


def test_signup_validation_returns_after_confirm_mismatch():
    _assert_block_has_return(
        SIGN_UP_SOURCE,
        "if (confirmPassword !== password)",
        "Confirm password mismatch validation",
    )


def test_checkout_payment_values_match_backend_contract():
    frontend_values = set(re.findall(r'FormControlLabel\s+value="([^"]+)"', CHECKOUT_SOURCE, flags=re.DOTALL))
    backend_match = re.search(
        r'paymentMethod:\s*Joi\.string\(\)\.valid\((?P<values>[^)]+)\)',
        VALIDATE_SOURCE,
        flags=re.DOTALL,
    )
    assert backend_match, "Backend validateOrder schema should declare valid paymentMethod values."

    backend_values = {
        value.strip().strip('"').strip("'")
        for value in backend_match.group("values").split(",")
        if value.strip()
    }
    assert frontend_values == backend_values, (
        f"Frontend payment values {sorted(frontend_values)} should match backend values {sorted(backend_values)}."
    )


def test_checkout_serializes_items_to_backend_shape():
    assert re.search(r"items:\s*context\.checkoutData\.items\.map\s*\(", CHECKOUT_SOURCE), (
        "Checkout payload should map cart items into backend shape with string productId values."
    )


def test_remove_cart_endpoint_uses_product_variant_identity():
    route_block = _extract_block(CART_ROUTES_SOURCE, 'router.delete("/removeCart/:id"')
    assert "size" in route_block and "color" in route_block, (
        "removeCart endpoint should receive and compare size/color, not only productId."
    )
    assert re.search(r"item\.size\s*===\s*size", route_block) and re.search(r"item\.color\s*===\s*color", route_block), (
        "removeCart findIndex should include size and color matching."
    )


def test_get_cart_route_enforces_owner_authorization():
    route_block = _extract_block(CART_ROUTES_SOURCE, 'router.get("/getCart/:id"')
    _assert_owner_guard(route_block, "id", "GET /api/cart/getCart/:id")


def test_add_cart_route_enforces_owner_authorization():
    route_block = _extract_block(CART_ROUTES_SOURCE, 'router.post("/addCart"')
    _assert_owner_guard(route_block, "userId", "POST /api/cart/addCart")


def test_update_cart_route_enforces_owner_authorization():
    route_block = _extract_block(CART_ROUTES_SOURCE, 'router.put("/updateCart"')
    _assert_owner_guard(route_block, "userId", "PUT /api/cart/updateCart")


def test_remove_cart_route_enforces_owner_authorization():
    route_block = _extract_block(CART_ROUTES_SOURCE, 'router.delete("/removeCart/:id"')
    _assert_owner_guard(route_block, "id", "DELETE /api/cart/removeCart/:id")


def test_create_order_route_enforces_owner_authorization():
    route_block = _extract_block(ORDER_ROUTES_SOURCE, 'router.post("/create", validateOrder, verifyToken')
    _assert_owner_guard(route_block, "userId", "POST /api/order/create")
