from selenium.webdriver.support.ui import WebDriverWait


class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def wait_until_loaded(self):
        self.wait.until(lambda driver: "/product/" in driver.current_url and "Thương hiệu:" in self.get_body_text())

    def get_body_text(self):
        return self.driver.find_element("tag name", "body").text

    def has_text(self, text):
        return text in self.get_body_text()
