import pytest

from pages.home_page import HomePage
from pages.product_page import ProductPage


PRODUCT_DETAIL_TEXTS = [
    "Th\u01b0\u01a1ng hi\u1ec7u:",
    "Lo\u1ea1i Danh m\u1ee5c:",
    "M\u00f4 T\u1ea3",
    "\u0110\u00e1nh Gi\u00e1 S\u1ea3n Ph\u1ea9m",
]


@pytest.mark.parametrize("product_index", range(6))
def test_homepage_visible_product_opens_detail_page(driver, step_logger, product_index):
    home_page = HomePage(driver)
    product_page = ProductPage(driver)

    step_logger("Mo trang chu de kiem tra product card.")
    home_page.open()

    visible_titles = home_page.get_visible_product_titles()
    if product_index >= len(visible_titles):
        pytest.skip("Khong du so luong product dang hien thi de test index nay.")

    selected_title = visible_titles[product_index]
    step_logger(f"Mo product card thu {product_index + 1}: {selected_title}")
    home_page.open_visible_product(product_index)
    product_page.wait_until_loaded()

    for text in PRODUCT_DETAIL_TEXTS:
        assert product_page.has_text(text)
    step_logger("Xac nhan trang chi tiet san pham hien thi day du thong tin co ban.")
