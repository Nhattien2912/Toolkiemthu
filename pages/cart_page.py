from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    TITLE_TEXT = "Gi\u1ecf H\u00e0ng C\u1ee7a B\u1ea1n"
    VOUCHER_INPUT = (By.XPATH, "//input[@placeholder='Nh\u1eadp m\u00e3 gi\u1ea3m gi\u00e1']")
    PRODUCT_ROWS = (By.CSS_SELECTOR, "tbody tr")
    TABLE_HEADERS = (By.CSS_SELECTOR, "table th")
    ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='Đặt Hàng']")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, "table img")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def open_spa(self):
        self.driver.execute_script(
            "window.history.pushState({}, '', '/cart'); window.dispatchEvent(new PopStateEvent('popstate'));"
        )
        self.wait_until_loaded()

    def wait_until_loaded(self):
        self.wait.until(lambda driver: driver.current_url.endswith("/cart") and self.TITLE_TEXT in self.get_body_text())

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_text(self, text):
        return text in self.get_body_text()

    def get_table_headers(self):
        return [header.text.strip() for header in self.driver.find_elements(*self.TABLE_HEADERS) if header.text.strip()]

    def get_visible_product_rows_count(self):
        return len([row for row in self.driver.find_elements(*self.PRODUCT_ROWS) if row.is_displayed()])

    def get_product_names(self):
        product_links = self.driver.find_elements(By.CSS_SELECTOR, "tbody a[href*='/product/']")
        return [link.text.strip() for link in product_links if link.is_displayed() and link.text.strip()]

    def get_currency_texts(self):
        return [token for token in self.get_body_text().split() if "\u20ab" in token]

    def get_voucher_value(self):
        return self.driver.find_element(*self.VOUCHER_INPUT).get_attribute("value")

    def fill_voucher_code(self, code):
        voucher_input = self.driver.find_element(*self.VOUCHER_INPUT)
        voucher_input.clear()
        voucher_input.send_keys(code)

    def click_apply_voucher(self):
        for button in self.driver.find_elements(By.CSS_SELECTOR, "button"):
            if button.is_displayed() and "d\u1ee5ng" in button.text.strip().casefold():
                self.driver.execute_script("arguments[0].click();", button)
                return

        raise RuntimeError("Khong tim thay nut Ap Dung.")

    def get_voucher_and_button_positions(self):
        voucher_input = self.driver.find_element(*self.VOUCHER_INPUT)
        apply_button = None
        for button in self.driver.find_elements(By.CSS_SELECTOR, "button"):
            if button.is_displayed() and "d\u1ee5ng" in button.text.strip().casefold():
                apply_button = button
                break

        if apply_button is None:
            raise RuntimeError("Khong tim thay nut Ap Dung.")

        return voucher_input.rect, apply_button.rect

    def get_visible_image_sources(self):
        return [image.get_attribute("src") for image in self.driver.find_elements(*self.PRODUCT_IMAGES) if image.is_displayed()]
