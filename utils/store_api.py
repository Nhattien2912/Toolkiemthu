import json
import urllib.request
from dataclasses import dataclass

from config import API_BASE_URL


@dataclass
class SeededCart:
    product_id: str
    product_name: str
    size: str
    color: str
    total_price: int
    cart_data_json: str
    checkout_data_json: str


def _get_json(path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        url=f"{API_BASE_URL}{path}",
        headers=headers,
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _post_json(path, payload, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        url=f"{API_BASE_URL}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def seed_cart_with_featured_product(authenticated_account):
    featured_product = _get_json("/api/products/featured?perPage=1")["products"][0]
    product = _get_json(f"/api/products/{featured_product['_id']}")["product"]

    add_cart_payload = {
        "userId": authenticated_account.user_id,
        "productId": product["_id"],
        "quantity": 1,
        "size": product["size"][0],
        "color": product["colors"][0],
    }
    _post_json("/api/cart/addCart", add_cart_payload, authenticated_account.token)

    cart = _get_json(f"/api/cart/getCart/{authenticated_account.user_id}", authenticated_account.token)
    checkout_data = {
        "items": cart["items"],
        "totalPrice": cart["totalPrice"],
        "isVoucher": False,
        "voucherCode": "",
        "discountPercentage": 0,
        "appliedDate": "",
        "userId": authenticated_account.user_id,
    }

    first_item = cart["items"][0]
    return SeededCart(
        product_id=product["_id"],
        product_name=product["name"],
        size=first_item["size"],
        color=first_item["color"],
        total_price=cart["totalPrice"],
        cart_data_json=json.dumps(cart, ensure_ascii=False),
        checkout_data_json=json.dumps(checkout_data, ensure_ascii=False),
    )
