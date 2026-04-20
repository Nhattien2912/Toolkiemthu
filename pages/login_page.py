from config import BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    USERNAME_INPUT = (By.NAME, "usernameOrPhone")
    PASSWORD_INPUT = (By.NAME, "password")
    ALERT_MESSAGE = (By.CSS_SELECTOR, ".MuiAlert-message")
    SIGNUP_USERNAME_INPUT = (By.NAME, "username")
    SIGNUP_PHONE_INPUT = (By.NAME, "phone")
    SIGNUP_FULLNAME_INPUT = (By.NAME, "fullName")
    SIGNUP_PASSWORD_INPUT = (By.NAME, "password")
    SIGNUP_CONFIRM_PASSWORD_INPUT = (By.NAME, "confirmPassword")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(., 'Qu\u00ean') or contains(., 'M\u1eadt Kh\u1ea9u')]")
    SIGNUP_EMAIL_CANDIDATES = (
        (By.NAME, "email"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.XPATH, "//input[contains(translate(@placeholder, 'EMAIL', 'email'), 'email')]"),
    )
    SIGNUP_OTP_CANDIDATES = (
        (By.NAME, "otp"),
        (By.NAME, "OTP"),
        (By.CSS_SELECTOR, "input[autocomplete='one-time-code']"),
        (By.CSS_SELECTOR, "input[inputmode='numeric'][maxlength='6']"),
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def find_login_link(self):
        candidates = self.driver.find_elements(By.CSS_SELECTOR, "a, button")

        for element in candidates:
            text = element.text.strip().lower()
            href = (element.get_attribute("href") or "").lower()

            if not element.is_displayed():
                continue

            if "đăng nhập" in text or href.endswith("/signin"):
                return element

        return None

    def find_submit_button(self):
        candidates = self.driver.find_elements(By.CSS_SELECTOR, "button")

        for element in candidates:
            text = element.text.strip().lower()

            if element.is_displayed() and "đăng nhập" in text:
                return element

        return None

    def find_signup_link(self):
        candidates = self.driver.find_elements(By.CSS_SELECTOR, "a, button")

        for element in candidates:
            text = element.text.strip().lower()
            href = (element.get_attribute("href") or "").lower()

            if not element.is_displayed():
                continue

            if "đăng ký" in text or href.endswith("/signup"):
                return element

        return None

    def open(self):
        self.driver.get(BASE_URL)
        login_link = self.wait.until(lambda driver: self.find_login_link())
        self.driver.execute_script("arguments[0].click();", login_link)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        submit_button = self.wait.until(lambda driver: self.find_submit_button())
        self.driver.execute_script("arguments[0].click();", submit_button)

    def get_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.ALERT_MESSAGE)).text

    def get_session_token(self):
        return self.driver.execute_script("return sessionStorage.getItem('token')")

    def get_session_user(self):
        return self.driver.execute_script("return sessionStorage.getItem('user')")

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def go_to_signup(self):
        signup_link = self.wait.until(lambda driver: self.find_signup_link())
        self.driver.execute_script("arguments[0].click();", signup_link)
        self.wait.until(EC.visibility_of_element_located(self.SIGNUP_USERNAME_INPUT))

    def signup_fields_are_visible(self):
        fields = [
            self.SIGNUP_USERNAME_INPUT,
            self.SIGNUP_PHONE_INPUT,
            self.SIGNUP_FULLNAME_INPUT,
            self.SIGNUP_PASSWORD_INPUT,
            self.SIGNUP_CONFIRM_PASSWORD_INPUT,
        ]
        return all(self.driver.find_element(*field).is_displayed() for field in fields)

    def get_username_value(self):
        return self.driver.find_element(*self.USERNAME_INPUT).get_attribute("value")

    def get_password_value(self):
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("value")

    def get_login_field_positions(self):
        return {
            "username": self.driver.find_element(*self.USERNAME_INPUT).rect,
            "password": self.driver.find_element(*self.PASSWORD_INPUT).rect,
        }

    def get_signup_field_positions(self):
        return {
            "username": self.driver.find_element(*self.SIGNUP_USERNAME_INPUT).rect,
            "phone": self.driver.find_element(*self.SIGNUP_PHONE_INPUT).rect,
            "fullName": self.driver.find_element(*self.SIGNUP_FULLNAME_INPUT).rect,
            "password": self.driver.find_element(*self.SIGNUP_PASSWORD_INPUT).rect,
            "confirmPassword": self.driver.find_element(*self.SIGNUP_CONFIRM_PASSWORD_INPUT).rect,
        }

    def get_cursor_style(self, locator):
        element = self.driver.find_element(*locator)
        return self.driver.execute_script("return window.getComputedStyle(arguments[0]).cursor;", element)

    def get_active_element_name(self):
        return self.driver.execute_script("return document.activeElement.name || document.activeElement.textContent || '';")

    def submit_with_enter(self, username, password):
        username_input = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        username_input.clear()
        username_input.send_keys(username)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def get_forgot_password_link_href(self):
        return self.wait.until(EC.visibility_of_element_located(self.FORGOT_PASSWORD_LINK)).get_attribute("href")

    def click_forgot_password_link(self):
        forgot_link = self.wait.until(EC.visibility_of_element_located(self.FORGOT_PASSWORD_LINK))
        self.driver.execute_script("arguments[0].click();", forgot_link)

    # ── Signup form helpers ──────────────────────────────────────────────────

    def find_visible_signup_email_input(self):
        for locator in self.SIGNUP_EMAIL_CANDIDATES:
            elements = self.driver.find_elements(*locator)
            for element in elements:
                if element.is_displayed():
                    return element
        return None

    def get_visible_otp_inputs(self):
        visible_inputs = []
        for locator in self.SIGNUP_OTP_CANDIDATES:
            for element in self.driver.find_elements(*locator):
                if element.is_displayed() and element not in visible_inputs:
                    visible_inputs.append(element)
        return visible_inputs

    def fill_signup_form(self, username, phone, full_name, password, confirm_password, email=None):
        self.wait.until(EC.visibility_of_element_located(self.SIGNUP_USERNAME_INPUT)).clear()
        self.driver.find_element(*self.SIGNUP_USERNAME_INPUT).send_keys(username)
        if email is not None:
            email_input = self.find_visible_signup_email_input()
            if email_input is not None:
                email_input.clear()
                email_input.send_keys(email)
        self.driver.find_element(*self.SIGNUP_PHONE_INPUT).clear()
        self.driver.find_element(*self.SIGNUP_PHONE_INPUT).send_keys(phone)
        self.driver.find_element(*self.SIGNUP_FULLNAME_INPUT).clear()
        self.driver.find_element(*self.SIGNUP_FULLNAME_INPUT).send_keys(full_name)
        self.driver.find_element(*self.SIGNUP_PASSWORD_INPUT).clear()
        self.driver.find_element(*self.SIGNUP_PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SIGNUP_CONFIRM_PASSWORD_INPUT).clear()
        self.driver.find_element(*self.SIGNUP_CONFIRM_PASSWORD_INPUT).send_keys(confirm_password)

    def click_signup_submit(self):
        for btn in self.driver.find_elements(By.CSS_SELECTOR, "button"):
            if btn.is_displayed() and "đăng ký" in btn.text.strip().lower():
                self.driver.execute_script("arguments[0].click();", btn)
                return
        raise RuntimeError("Không tìm thấy nút ĐĂNG KÝ trên trang")

    def get_alert_text(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.ALERT_MESSAGE)).text
        except Exception:
            return ""

    def click_login_link_from_signup(self):
        """Click 'Đăng Nhập' link from within the signup form."""
        for elem in self.driver.find_elements(By.CSS_SELECTOR, "a"):
            if "đăng nhập" in elem.text.strip().lower() and elem.is_displayed():
                self.driver.execute_script("arguments[0].click();", elem)
                return
        raise RuntimeError("Không tìm thấy link Đăng Nhập trên form đăng ký")
