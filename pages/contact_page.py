from selenium.webdriver.support.ui import WebDriverWait


class ContactPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def wait_until_loaded(self):
        self.wait.until(lambda driver: driver.current_url.endswith("/contact") and "LIÊN HỆ VỚI CHÚNG TÔI" in self.get_body_text())

    def get_body_text(self):
        return self.driver.find_element("tag name", "body").text

    def has_text(self, text):
        return text in self.get_body_text()
