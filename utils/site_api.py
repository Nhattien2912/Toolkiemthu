import json
import urllib.request

from config import API_BASE_URL


def _get_json(path):
    with urllib.request.urlopen(f"{API_BASE_URL}{path}", timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def get_nav_category_names():
    data = _get_json("/api/category")
    return [item["name"] for item in data.get("categories", []) if item.get("type") == "nav"]


def get_search_keywords(limit=4):
    keywords = []

    for path in ("/api/products/featured?perPage=8", "/api/products/new?perPage=8"):
        data = _get_json(path)
        for product in data.get("products", []):
            brand = (product.get("brand") or "").strip()
            if brand and brand not in keywords:
                keywords.append(brand)

            if len(keywords) >= limit:
                return keywords[:limit]

    return keywords[:limit] or ["Adidas", "Nike"]
