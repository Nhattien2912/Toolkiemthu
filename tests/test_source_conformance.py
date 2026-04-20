from __future__ import annotations

from pathlib import Path

import pytest


SOURCE_PROJECT_ROOT = Path(r"C:\Users\clubb\Desktop\WEB-MERN_t10-2024")


def _read_source(relative_path: str) -> str:
    path = SOURCE_PROJECT_ROOT / relative_path
    assert path.exists(), f"Missing source file: {path}"
    return path.read_text(encoding="utf-8", errors="replace")


APP_SOURCE = _read_source("frontend/src/App.js")
SIGN_IN_SOURCE = _read_source("frontend/src/Pages/AuthSignIn/index.js")
SIGN_UP_SOURCE = _read_source("frontend/src/Pages/AuthSignUp/index.js")
VALIDATE_SOURCE = _read_source("server/middlewares/validate.js")
CHECKOUT_SOURCE = _read_source("frontend/src/Pages/Checkout/index.js")
CART_ROUTES_SOURCE = _read_source("server/routes/cartRoutes.js")


@pytest.mark.parametrize(
    "expected_route",
    [
        'path="/"',
        'path="/cat/:id"',
        'path="/list-heart"',
        'path="/product/:id"',
        'path="/cart"',
        'path="/signIn"',
        'path="/signUp"',
        'path="/checkout"',
        'path="/my-order"',
        'path="/my-account"',
        'path="/search"',
        'path="/contact"',
    ],
)
def test_storefront_routes_exist(expected_route):
    assert expected_route in APP_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        'usernameOrPhone: ""',
        'password: ""',
        "usernameInputRef",
        "passwordInputRef",
        'postData("/api/user/signin"',
        'sessionStorage.setItem("user"',
        'history("/")',
        "handleGoogleSignIn",
        'autoComplete="current-password"',
        'to="/signUp"',
    ],
)
def test_signin_source_contains_expected_controls(expected_snippet):
    assert expected_snippet in SIGN_IN_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        'username: ""',
        'phone: ""',
        'fullName: ""',
        'password: ""',
        'confirmPassword: ""',
        "usernameRef",
        "phoneRef",
        "fullNameRef",
        "passwordRef",
        "confirmPasswordRef",
        'postData("/api/user/signup"',
        'history("/signIn")',
    ],
)
def test_signup_source_contains_expected_controls(expected_snippet):
    assert expected_snippet in SIGN_UP_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        "exports.validateSignup",
        "username: Joi.string().trim().alphanum().min(3).max(30).required()",
        "phone: Joi.string().pattern",
        "fullName: Joi.string().trim().min(3).max(100).required()",
        "confirmPassword: Joi.any()",
        'valid(Joi.ref("password"))',
        "exports.validateSignin",
        'paymentMethod: Joi.string().valid("COD", "Online").required()',
    ],
)
def test_validation_source_contains_expected_contracts(expected_snippet):
    assert expected_snippet in VALIDATE_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        'name="fullName"',
        'name="phone"',
        'name="detail"',
        'name="notes"',
        'value="cash"',
        'value="payment"',
        "fetchProvinces",
        "multiline",
    ],
)
def test_checkout_source_contains_expected_controls(expected_snippet):
    assert expected_snippet in CHECKOUT_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        'router.get("/getCart/:id"',
        'router.post("/addCart"',
        'router.put("/updateCart"',
        'router.delete("/removeCart/:id"',
        "item.size === size",
        "item.color === color",
    ],
)
def test_cart_routes_source_contains_expected_business_logic(expected_snippet):
    assert expected_snippet in CART_ROUTES_SOURCE
