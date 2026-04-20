from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class AccountPage:
    TITLE_TEXT = "TH\u00d4NG TIN T\u00c0I KHO\u1ea2N C\u1ee6A B\u1ea0N"
    USERNAME_INPUT = (By.NAME, "username")
    FULLNAME_INPUT = (By.NAME, "fullName")
    PHONE_INPUT = (By.NAME, "phone")
    EMAIL_INPUT = (By.NAME, "email")
    ACCOUNT_TABS = (By.CSS_SELECTOR, "button[role='tab']")
    PASSWORD_INPUTS = (By.CSS_SELECTOR, "input[type='password']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def open_spa(self):
        self.driver.execute_script(
            "window.history.pushState({}, '', '/my-account'); window.dispatchEvent(new PopStateEvent('popstate'));"
        )
        self.wait_until_loaded()

    def wait_until_loaded(self):
        self.wait.until(lambda driver: driver.current_url.endswith("/my-account") and self.TITLE_TEXT in self.get_body_text())

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_visible_labels(self):
        labels = self.driver.find_elements(By.CSS_SELECTOR, "label")
        return [label.text.strip() for label in labels if label.is_displayed() and label.text.strip()]

    def get_profile_input_positions(self):
        return {
            "username": self.driver.find_element(*self.USERNAME_INPUT).rect,
            "fullName": self.driver.find_element(*self.FULLNAME_INPUT).rect,
            "phone": self.driver.find_element(*self.PHONE_INPUT).rect,
            "email": self.driver.find_element(*self.EMAIL_INPUT).rect,
        }

    def click_change_password_tab(self):
        for tab in self.driver.find_elements(*self.ACCOUNT_TABS):
            if tab.is_displayed() and "THAY \u0110\u1ed4I M\u1eacT KH\u1ea8U" in tab.text.upper():
                tab.click()
                self.wait.until(lambda driver: tab.get_attribute("aria-selected") == "true")
                return

        raise RuntimeError("Khong tim thay tab thay doi mat khau.")

    def get_tab_states(self):
        return {tab.text.strip(): tab.get_attribute("aria-selected") for tab in self.driver.find_elements(*self.ACCOUNT_TABS)}

    def get_visible_password_fields_count(self):
        return len([field for field in self.driver.find_elements(*self.PASSWORD_INPUTS) if field.is_displayed()])

    def get_password_field_positions(self):
        visible_fields = [field for field in self.driver.find_elements(*self.PASSWORD_INPUTS) if field.is_displayed()]
        return [field.rect for field in visible_fields]

    def get_visible_image_sources(self):
        return [image.get_attribute("src") for image in self.driver.find_elements(By.CSS_SELECTOR, "img") if image.is_displayed()]
