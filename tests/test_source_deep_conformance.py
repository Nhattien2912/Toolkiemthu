from __future__ import annotations

from pathlib import Path

import pytest


SOURCE_PROJECT_ROOT = Path(r"C:\Users\clubb\Desktop\WEB-MERN_t10-2024")


def _read_source(relative_path: str) -> str:
    path = SOURCE_PROJECT_ROOT / relative_path
    assert path.exists(), f"Missing source file: {path}"
    return path.read_text(encoding="utf-8", errors="replace")


HEADER_SOURCE = _read_source("frontend/src/Components/Header/index.js")
FOOTER_SOURCE = _read_source("frontend/src/Components/Footer/index.js")
USER_ROUTES_SOURCE = _read_source("server/routes/userRoutes.js")
PRODUCT_ROUTES_SOURCE = _read_source("server/routes/productsRoutes.js")
ORDER_MODEL_SOURCE = _read_source("server/models/OrderModel.js")


@pytest.mark.parametrize(
    "expected_snippet",
    [
        "SearchBox",
        "Navigation",
        'Link to="signIn"',
        'Link to="/my-account"',
        'Link to="/my-order"',
        'Link to="/list-heart"',
        'Link to="/cart"',
        "handleLogout",
        "localStorage.clear()",
        "sessionStorage.clear()",
        "formatCurrency",
        "context.cartData?.items ? (",
    ],
)
def test_header_source_contains_expected_account_and_cart_controls(expected_snippet):
    assert expected_snippet in HEADER_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        "socialMediaIcons",
        "FaFacebookF",
        "FaTwitter",
        "FaInstagram",
        "<footer>",
        "Bản quyền 2024.",
        "list-inline-item",
    ],
)
def test_footer_source_contains_expected_social_and_branding_controls(expected_snippet):
    assert expected_snippet in FOOTER_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        'router.post("/signup", authLimiter, validateSignup, async (req, res) => {',
        'router.post("/signin", authLimiter, validateSignin, async (req, res) => {',
        'router.post("/authentication/signin", async (req, res) => {',
        'router.post("/authWithGoogle", async (req, res) => {',
        'upload.single("avatar")',
        '"/change-password/:id"',
        '"/delete-user/:id"',
        'router.get("/me", verifyToken, async (req, res) => {',
        'router.post("/signout", (req, res) => {',
        'res.clearCookie("token"',
    ],
)
def test_user_routes_source_contains_expected_auth_endpoints(expected_snippet):
    assert expected_snippet in USER_ROUTES_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        'router.get("/", async (req, res) => {',
        'router.get("/all-products", async (req, res) => {',
        'router.get("/getProductSeller", async (req, res) => {',
        'router.get("/featured", async (req, res) => {',
        'router.get("/new", async (req, res) => {',
        'router.get("/cat", async (req, res) => {',
        'router.get("/related", async (req, res) => {',
        'router.get("/:id", async (req, res) => {',
        'router.delete("/:id", verifyToken, checkAdminOrOwner, async (req, res) => {',
        'router.post("/upload/remove", async (req, res) => {',
        'router.post("/upload", upload.array("images"), async (req, res) => {',
        '"/create"',
        'upload.array("images", 5)',
    ],
)
def test_product_routes_source_contains_expected_catalog_endpoints(expected_snippet):
    assert expected_snippet in PRODUCT_ROUTES_SOURCE


@pytest.mark.parametrize(
    "expected_snippet",
    [
        "userId: {",
        "items: [",
        "productId: {",
        "quantity: {",
        "price: {",
        "color: String",
        "size: String",
        "images: [String]",
        "isVouched: [",
        "totalPrice: {",
        "address: {",
        "paymentMethod: {",
        "status: {",
        'enum: ["Pending", "Packed", "In Transit", "Completed", "Cancelled"]',
        "timestamps: true",
    ],
)
def test_order_model_source_contains_expected_schema_fields(expected_snippet):
    assert expected_snippet in ORDER_MODEL_SOURCE
