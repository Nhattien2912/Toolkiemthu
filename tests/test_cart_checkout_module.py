import requests

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def assert_no_horizontal_scrollbar(driver):
    assert driver.execute_script(
        "return document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1;"
    )


def assert_images_load_ok(urls):
    for url in urls[:3]:
        response = requests.get(url, timeout=30)
        assert response.ok, f"Broken image: {url}"


def test_cart_page_grid_headers_totals_and_rows(driver, seeded_cart_session, step_logger):
    _, seeded_cart = seeded_cart_session
    cart_page = CartPage(driver)

    step_logger("Mo trang gio hang da duoc seed san pham.")
    cart_page.open_spa()

    headers = cart_page.get_table_headers()
    assert "Sản phẩm" in headers
    assert "Size" in headers
    assert "Màu" in headers
    assert "Đơn giá" in headers
    assert "Số lượng" in headers
    assert "Tổng phụ" in headers
    assert cart_page.get_visible_product_rows_count() >= 1
    assert seeded_cart.product_name[:10] in cart_page.get_body_text()
    assert len(cart_page.get_currency_texts()) >= 3
    assert len(cart_page.get_product_names()) == len(set(cart_page.get_product_names()))
    assert_no_horizontal_scrollbar(driver)


def test_cart_page_voucher_input_and_button_alignment(driver, seeded_cart_session, step_logger):
    cart_page = CartPage(driver)

    step_logger("Mo gio hang va kiem tra voucher input sau khi apply.")
    cart_page.open_spa()
    input_rect, button_rect = cart_page.get_voucher_and_button_positions()
    assert button_rect["y"] > input_rect["y"]
    assert abs(input_rect["x"] - button_rect["x"]) <= 250

    cart_page.fill_voucher_code("SAI_MA_TEST")
    cart_page.click_apply_voucher()
    assert cart_page.get_voucher_value() == "SAI_MA_TEST"


def test_cart_page_product_images_are_not_broken(driver, seeded_cart_session, step_logger):
    cart_page = CartPage(driver)

    step_logger("Mo gio hang va kiem tra hinh san pham khong bi hong.")
    cart_page.open_spa()
    assert_images_load_ok(cart_page.get_visible_image_sources())


def test_checkout_page_layout_multiline_and_payment_controls(driver, seeded_checkout_session, step_logger):
    checkout_page = CheckoutPage(driver)

    step_logger("Mo trang checkout va kiem tra bo cuc form.")
    checkout_page.open_spa()

    labels = checkout_page.get_visible_labels()
    positions = checkout_page.get_form_field_positions()
    textarea_rows = checkout_page.get_textarea_rows()
    payment_states = checkout_page.get_payment_states()

    assert driver.title.strip() != ""
    assert "Họ và tên" in labels
    assert "Số điện thoại" in labels
    assert "Tỉnh / thành phố" in labels
    assert "Phương thức thanh toán" in labels
    assert abs(positions["fullName"]["y"] - positions["phone"]["y"]) <= 5
    assert abs(positions["detail"]["x"] - positions["notes"]["x"]) <= 5
    assert textarea_rows["detail"] >= 1
    assert textarea_rows["notes"] >= 4
    assert set(payment_states) == {"cash", "payment"}
    assert payment_states["payment"]["disabled"] is True
    assert_no_horizontal_scrollbar(driver)


def test_checkout_form_values_persist_after_failed_submit(driver, seeded_checkout_session, step_logger):
    checkout_page = CheckoutPage(driver)

    step_logger("Mo checkout, nhap du lieu va submit thieu de kiem tra giu gia tri.")
    checkout_page.open_spa()
    checkout_page.fill_basic_shipping_info(
        full_name="Nguyen Van A",
        phone="0912345678",
        detail="123 duong test",
        notes="ghi chu test",
    )
    checkout_page.click_place_order()

    values = checkout_page.get_shipping_values()
    assert driver.current_url.endswith("/checkout")
    assert values["fullName"] == "Nguyen Van A"
    assert values["phone"] == "0912345678"
    assert values["detail"] == "123 duong test"
    assert values["notes"] == "ghi chu test"


def test_checkout_cash_option_and_summary_headers(driver, seeded_checkout_session, step_logger):
    checkout_page = CheckoutPage(driver)

    step_logger("Mo checkout va kiem tra radio thanh toan cung bang tom tat don hang.")
    checkout_page.open_spa()
    checkout_page.select_payment_by_value("cash")

    payment_states = checkout_page.get_payment_states()
    headers = checkout_page.get_summary_headers()
    assert payment_states["cash"]["selected"] is True
    assert payment_states["payment"]["selected"] is False
    assert "Sản phẩm" in headers
    assert "Giá" in headers
