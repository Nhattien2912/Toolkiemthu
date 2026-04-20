from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class CheckoutPage:
    TITLE_TEXT = "CHI TI\u1ebeT THANH TO\u00c1N"
    FULL_NAME_INPUT = (By.NAME, "fullName")
    PHONE_INPUT = (By.NAME, "phone")
    DETAIL_TEXTAREA = (By.NAME, "detail")
    NOTES_TEXTAREA = (By.NAME, "notes")
    PAYMENT_RADIOS = (By.CSS_SELECTOR, "input[type='radio'][name='radio-buttons-group']")
    SUMMARY_HEADERS = (By.CSS_SELECTOR, "table th")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='ĐẶT HÀNG']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def open_spa(self):
        self.driver.execute_script(
            "window.history.pushState({}, '', '/checkout'); window.dispatchEvent(new PopStateEvent('popstate'));"
        )
        self.wait_until_loaded()

    def wait_until_loaded(self):
        self.wait.until(lambda driver: driver.current_url.endswith("/checkout") and self.TITLE_TEXT in self.get_body_text())

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_text(self, text):
        return text in self.get_body_text()

    def get_visible_labels(self):
        labels = self.driver.find_elements(By.CSS_SELECTOR, "label")
        return [label.text.strip() for label in labels if label.is_displayed() and label.text.strip()]

    def get_form_field_positions(self):
        return {
            "fullName": self.driver.find_element(*self.FULL_NAME_INPUT).rect,
            "phone": self.driver.find_element(*self.PHONE_INPUT).rect,
            "detail": self.driver.find_element(*self.DETAIL_TEXTAREA).rect,
            "notes": self.driver.find_element(*self.NOTES_TEXTAREA).rect,
        }

    def get_textarea_rows(self):
        return {
            "detail": int(self.driver.find_element(*self.DETAIL_TEXTAREA).get_attribute("rows")),
            "notes": int(self.driver.find_element(*self.NOTES_TEXTAREA).get_attribute("rows")),
        }

    def get_payment_radios(self):
        return self.driver.find_elements(*self.PAYMENT_RADIOS)

    def select_payment_by_value(self, value):
        for radio in self.get_payment_radios():
            if radio.get_attribute("value") == value:
                self.driver.execute_script("arguments[0].click();", radio)
                return

        raise RuntimeError(f"Khong tim thay radio payment: {value}")

    def get_payment_states(self):
        states = {}
        for radio in self.get_payment_radios():
            states[radio.get_attribute("value")] = {
                "selected": radio.is_selected(),
                "disabled": radio.get_attribute("disabled") is not None,
            }
        return states

    def fill_basic_shipping_info(self, full_name, phone, detail, notes):
        fields = {
            self.FULL_NAME_INPUT: full_name,
            self.PHONE_INPUT: phone,
            self.DETAIL_TEXTAREA: detail,
            self.NOTES_TEXTAREA: notes,
        }

        for locator, value in fields.items():
            element = self.driver.find_element(*locator)
            element.clear()
            element.send_keys(value)

    def get_shipping_values(self):
        return {
            "fullName": self.driver.find_element(*self.FULL_NAME_INPUT).get_attribute("value"),
            "phone": self.driver.find_element(*self.PHONE_INPUT).get_attribute("value"),
            "detail": self.driver.find_element(*self.DETAIL_TEXTAREA).get_attribute("value"),
            "notes": self.driver.find_element(*self.NOTES_TEXTAREA).get_attribute("value"),
        }

    def click_place_order(self):
        for button in self.driver.find_elements(By.CSS_SELECTOR, "button"):
            if button.is_displayed() and "\u0111\u1eb7t h\u00e0ng" in button.text.strip().casefold():
                self.driver.execute_script("arguments[0].click();", button)
                return

        raise RuntimeError("Khong tim thay nut Dat Hang.")

    def get_summary_headers(self):
        return [header.text.strip() for header in self.driver.find_elements(*self.SUMMARY_HEADERS) if header.text.strip()]
